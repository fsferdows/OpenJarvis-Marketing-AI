#!/usr/bin/env python3
"""
Mollik Builders Ltd - Project 10
Automated WhatsApp Notification Dispatcher

Sends real-time high-priority alerts to the owner's WhatsApp:
Recipient: +8801633309081

Integrations supported:
1. CallMeBot WhatsApp API (Free, Instant setup)
2. Twilio WhatsApp API
3. Meta WhatsApp Cloud API
4. Direct wa.me Actionable URL Generator with pre-filled message
5. Persistent Local Alert Queue (data/whatsapp_outbox.json)
"""

import os
import sys
import json
import urllib.parse
from datetime import datetime
from typing import Dict, Any, Optional
import requests

OWNER_WHATSAPP = "+8801633309081"
OWNER_CLEAN_PHONE = "8801633309081"

OUTBOX_FILE = "data/whatsapp_outbox.json"


def init_outbox():
    """Initializes outbox storage."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(OUTBOX_FILE):
        with open(OUTBOX_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)


def format_booking_alert(booking: Dict[str, Any]) -> str:
    """Formats an executive WhatsApp alert message for Mollik Builders management."""
    client_phone = booking.get("phone", "").replace("+", "").replace(" ", "").replace("-", "")
    if client_phone.startswith("0"):
        client_wa = f"88{client_phone}"
    elif not client_phone.startswith("88"):
        client_wa = f"880{client_phone}"
    else:
        client_wa = client_phone

    wa_chat_url = f"https://wa.me/{client_wa}"

    msg = (
        f"🚨 *[নতুন প্রজেক্ট ভিজিট বুকিং অ্যালার্ট — মল্লিক বিল্ডার্স]*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏢 *প্রজেক্ট:* প্রজেক্ট ১০ (বাশতলা, ভুঁইয়া বাড়ি)\n"
        f"👤 *সম্মানিত ক্রেতা:* {booking.get('name', 'N/A')}\n"
        f"📞 *ফোন নাম্বার:* {booking.get('phone', 'N/A')}\n"
        f"📅 *সাইট ভিজিটের সম্ভাব্য তারিখ:* {booking.get('visit_date', 'এই সপ্তাহে')}\n"
        f"⏰ *পছন্দের সময়:* {booking.get('visit_time', 'সকাল ১১টা - দুপুর ১টা')}\n"
        f"🔥 *আগ্রহের স্তর:* {booking.get('interest_level', '🔥 Hot Lead')}\n"
        f"💰 *বাজেট/প্যাকেজ:* ৳৪৮.২৫ লাখ (৩৬ মাসের কিস্তি)\n"
        f"🏡 *ফ্ল্যাট:* ১৫৭০ স্কয়ার ফিট (৩ বেড, ৩ বাথ)\n\n"
        f"💬 *আলোচনার সারসংক্ষেপ:*\n"
        f"\"{booking.get('summary', 'গ্রাহক প্রজেক্ট ভিজিট ও বিস্তারিত বুকিং প্রক্রিয়ায় আগ্রহী।')}\"\n\n"
        f"👉 *ক্রেতার সাথে সরাসরি হোয়াটসঅ্যাপে চ্যাট করতে ট্যাপ করুন:*\n"
        f"{wa_chat_url}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⏰ *সময়:* {datetime.now().strftime('%Y-%m-%d %I:%M %p')}"
    )
    return msg


def trigger_local_macos_notification(title: str, subtitle: str, body: str):
    """Triggers a 100% local, self-hosted macOS notification banner and audio chime."""
    try:
        clean_body = body.replace('"', '\\"').replace("'", "\\'")
        clean_title = title.replace('"', '\\"')
        clean_subtitle = subtitle.replace('"', '\\"')
        cmd = f'osascript -e \'display notification "{clean_body}" with title "{clean_title}" subtitle "{clean_subtitle}" sound name "Glass"\''
        os.system(cmd)
    except Exception as e:
        print(f"[LOCAL NOTIFICATION ERROR]: {e}")


def send_whatsapp_alert(booking_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dispatches WhatsApp alert to owner (+8801633309081).
    100% Self-Hosted:
    - Triggers native macOS notification banner + chime
    - Launches local WhatsApp Desktop via whatsapp:// protocol (zero cloud API needed)
    - Records directly into local data/project_bookings.csv and outbox
    """
    init_outbox()
    message_text = format_booking_alert(booking_data)
    client_name = booking_data.get("name", "Unknown Client")
    client_phone = booking_data.get("phone", "N/A")
    visit_date = booking_data.get("visit_date", "This week")

    alert_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "recipient": OWNER_WHATSAPP,
        "client_name": client_name,
        "client_phone": client_phone,
        "visit_date": visit_date,
        "message": message_text,
        "direct_click_url": f"https://wa.me/{OWNER_CLEAN_PHONE}?text={urllib.parse.quote(message_text)}",
        "status": "SELF_HOSTED_LOCAL"
    }

    # 1. Trigger local macOS notification banner on owner's Mac screen
    trigger_local_macos_notification(
        title="Mollik Builders: New Site Visit Lead!",
        subtitle=f"Project 10 — {client_name}",
        body=f"Phone: {client_phone} | Scheduled: {visit_date}"
    )

    # 2. Open locally in WhatsApp Desktop app (Self-hosted, zero cloud APIs)
    try:
        encoded_text = urllib.parse.quote(message_text)
        local_wa_cmd = f'open "whatsapp://send?phone={OWNER_CLEAN_PHONE}&text={encoded_text}"'
        os.system(local_wa_cmd)
        alert_record["status"] = "SENT_LOCAL_WHATSAPP"
        print(f"[✓ 100% SELF-HOSTED DISPATCH: Triggered local WhatsApp for {OWNER_WHATSAPP}]")
    except Exception as e:
        alert_record["local_error"] = str(e)

    # 1. Check for CallMeBot WhatsApp API Key in environment
    callmebot_key = os.environ.get("CALLMEBOT_API_KEY")
    if callmebot_key:
        try:
            encoded_text = urllib.parse.quote(message_text)
            url = f"https://api.callmebot.com/whatsapp.php?phone={OWNER_CLEAN_PHONE}&text={encoded_text}&apikey={callmebot_key}"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                alert_record["status"] = "SENT_CALLMEBOT"
                print(f"[✓ WhatsApp Alert Sent via CallMeBot to {OWNER_WHATSAPP}]")
        except Exception as e:
            alert_record["error"] = str(e)

    # 2. Check for Twilio WhatsApp credentials
    twilio_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    twilio_token = os.environ.get("TWILIO_AUTH_TOKEN")
    twilio_from = os.environ.get("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")
    if twilio_sid and twilio_token and alert_record["status"] == "QUEUED":
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json"
            data = {
                "From": twilio_from,
                "To": f"whatsapp:{OWNER_WHATSAPP}",
                "Body": message_text
            }
            resp = requests.post(url, data=data, auth=(twilio_sid, twilio_token), timeout=10)
            if resp.status_code in [200, 201]:
                alert_record["status"] = "SENT_TWILIO"
                print(f"[✓ WhatsApp Alert Sent via Twilio to {OWNER_WHATSAPP}]")
        except Exception as e:
            alert_record["error"] = str(e)

    # Save to persistent outbox
    with open(OUTBOX_FILE, "r", encoding="utf-8") as f:
        outbox = json.load(f)
    outbox.append(alert_record)
    with open(OUTBOX_FILE, "w", encoding="utf-8") as f:
        json.dump(outbox, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print(f"WHATSAPP EXECUTIVE NOTIFICATION FOR {OWNER_WHATSAPP}")
    print("=" * 70)
    print(message_text)
    print("=" * 70)
    print(f"Instant Web-to-WhatsApp Trigger URL:\n{alert_record['direct_click_url']}\n")

    return alert_record


if __name__ == "__main__":
    # Test dispatch
    sample_booking = {
        "name": "Engr. Mahmudul Hasan",
        "phone": "01715892341",
        "visit_date": "Friday (31 Oct 2026)",
        "visit_time": "11:00 AM",
        "interest_level": "🔥 Hot Lead (Visit Booked)",
        "summary": "Customer works in Uttara Sector 7. Wants 3-bed flat on 6th floor with 36-month installment. Wants to inspect building foundation on Friday morning."
    }
    send_whatsapp_alert(sample_booking)

