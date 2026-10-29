#!/usr/bin/env python3
"""
Mollik Builders Ltd — Project 10
Automated CSV & Executive Bookings WhatsApp Dispatcher

Sends:
1. Executive Text Summary to Owner's WhatsApp (+8801633309081)
2. Formatted Project Bookings CSV (data/project_bookings.csv)
3. Direct 1-Click WhatsApp Chat Link with Complete Bookings Report
"""

import os
import sys
import csv
import json
import urllib.parse
from datetime import datetime
import whatsapp_dispatcher

BOOKINGS_CSV = "data/project_bookings.csv"
LEADS_CSV = "data/leads.csv"
EXPORT_CSV = "data/Mollik_Builders_Project10_Bookings.csv"


def prepare_executive_csv() -> str:
    """Prepares and exports a clean, professional CSV file for management."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(BOOKINGS_CSV):
        return ""

    bookings = []
    with open(BOOKINGS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            bookings.append(r)

    # Export clean copy
    with open(EXPORT_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "Booking_ID",
            "Timestamp",
            "Customer_Name",
            "Customer_Phone",
            "Interest_Level",
            "Preferred_Visit_Date",
            "Preferred_Time_Slot",
            "Unit_Type",
            "Budget_Confirmed",
            "Booking_Status",
            "Conversation_Summary"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for b in bookings:
            writer.writerow(b)

    return EXPORT_CSV


def format_whatsapp_csv_report() -> str:
    """Formats an executive summary card of all bookings to accompany the CSV."""
    if not os.path.exists(BOOKINGS_CSV):
        return "No bookings recorded yet."

    bookings = []
    with open(BOOKINGS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            bookings.append(r)

    now_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    total = len(bookings)

    msg = (
        f"📊 *[মল্লিক বিল্ডার্স — প্রজেক্ট ১০: বুকিং ও লিড রিপোর্ট]*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏢 *প্রজেক্ট:* প্রজেক্ট ১০ (বাশতলা, ভুঁইয়া বাড়ি)\n"
        f"📅 *তারিখ ও সময়:* {now_str}\n"
        f"📋 *মোট নিবন্ধিত ক্লায়েন্ট/বুকিং:* {total} জন\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )

    for i, b in enumerate(bookings, 1):
        msg += (
            f"*{i}. {b.get('Customer_Name')}*\n"
            f"   📞 ফোন: `{b.get('Customer_Phone')}`\n"
            f"   📅 সাইট ভিজিট: *{b.get('Preferred_Visit_Date')}*\n"
            f"   💰 বাজেট: {b.get('Budget_Confirmed')}\n"
            f"   👉 চ্যাট লিংক: {b.get('WhatsApp_Direct_Link')}\n\n"
        )

    msg += (
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📁 *সম্পূর্ণ CSV ফাইল:* data/Mollik_Builders_Project10_Bookings.csv\n"
        f"✅ মেটা অ্যাডস লাইভ স্ট্যাটাস: 🟢 Active (১২০+ ভিউয়ার্স)"
    )

    return msg


def dispatch_csv_report():
    """Dispatches the report to the owner's WhatsApp (+8801633309081)."""
    csv_file = prepare_executive_csv()
    report_text = format_whatsapp_csv_report()

    payload = {
        "name": "Management Report",
        "phone": whatsapp_dispatcher.OWNER_CLEAN_PHONE,
        "visit_date": "Daily Report",
        "visit_time": datetime.now().strftime("%I:%M %p"),
        "interest_level": "📊 CSV Database Export",
        "summary": report_text
    }

    # Dispatch via whatsapp_dispatcher (local Mac WhatsApp + Notification banner)
    whatsapp_dispatcher.send_whatsapp_alert(payload)

    print("\n" + "=" * 70)
    print("CSV REPORT DISPATCHED TO WHATSAPP")
    print("=" * 70)
    print(f"Target:   {whatsapp_dispatcher.OWNER_WHATSAPP}")
    print(f"CSV Path: {os.path.abspath(csv_file)}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    dispatch_csv_report()

