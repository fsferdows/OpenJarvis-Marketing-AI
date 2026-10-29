#!/usr/bin/env python3
"""
Mollik Builders Ltd - Project 10
Senior AI Real Estate Sales Consultant & Booking Engine

Key Features:
- Polite, prestigious, high-converting salesman persona
- Conversational state tracking (Qualification -> Value Prop -> Site Visit Close)
- Automated Extraction of Booking Details (Name, Phone, Visit Date/Time, Unit interest)
- Automatic CSV Lead & Booking Logging (data/project_bookings.csv)
- Automatic WhatsApp Executive Dispatcher to Owner (+8801633309081)
"""

import os
import re
import sys
import json
import csv
from datetime import datetime
from typing import Dict, Any, Tuple, Optional
import whatsapp_dispatcher

BOOKINGS_CSV = "data/project_bookings.csv"

BD_PHONE_REGEX = re.compile(r"(?:\+?880|0)?1[3-9]\d{8}\b")

# Knowledge Base & Value Proposition
KB = {
    "project": "Mollik Builders Ltd — Project 10",
    "location": "Bhuiyan Bari, Bashtola (Near Mazar Chowrasta, 10 mins from Azampur Uttara, 15 mins from HSIA Airport)",
    "specs": "1570 sqft gross (1250 sqft net usable), 3 Bed, 3 Bath, Drawing, Dining, 2 Balconies",
    "building": "G+9 (10-story modern condominium) on 8.72 Katha land",
    "amenities": "2 High-speed Elevators, 5000 sqft Landscaped Rooftop Garden, In-house Mosque, Super Shop, 24/7 Generator Backup, CCTV & Security",
    "roads": "20ft & 16ft wide connected roads, 100ft proposed front road",
    "pricing": "Land Share: ৳12,00,000 + Construction: ৳36,25,000 = Total: ৳48,25,000",
    "installment": "36-month flexible installment facility",
    "guarantee": "Written penalty rent compensation guarantee if handover exceeds 36 months; Sub-kabla land share registry"
}


def init_bookings_csv():
    """Initializes the professional bookings CSV database."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(BOOKINGS_CSV):
        with open(BOOKINGS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Booking_ID",
                "Timestamp",
                "Customer_Name",
                "Customer_Phone",
                "WhatsApp_Direct_Link",
                "Interest_Level",
                "Preferred_Visit_Date",
                "Preferred_Time_Slot",
                "Unit_Type",
                "Budget_Confirmed",
                "Conversation_Summary",
                "Owner_Alert_Status",
                "Sales_Next_Action",
                "Booking_Status"
            ])


def get_next_booking_id() -> str:
    """Generates sequential Booking ID: MB-P10-101, MB-P10-102..."""
    init_bookings_csv()
    count = 100
    try:
        with open(BOOKINGS_CSV, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            if len(rows) > 1:
                count += (len(rows) - 1)
    except Exception:
        pass
    return f"MB-P10-{count + 1}"


def record_project_booking(
    name: str,
    phone: str,
    visit_date: str = "This Week",
    visit_time: str = "11:00 AM",
    summary: str = "",
    interest_level: str = "🔥 Hot Lead (Visit Booked)"
) -> Dict[str, Any]:
    """Records full booking into CSV and triggers WhatsApp notification to owner."""
    init_bookings_csv()
    booking_id = get_next_booking_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Clean phone for direct wa.me URL
    clean_p = phone.replace("+", "").replace(" ", "").replace("-", "")
    if clean_p.startswith("0"):
        wa_p = f"88{clean_p}"
    elif not clean_p.startswith("88"):
        wa_p = f"880{clean_p}"
    else:
        wa_p = clean_p

    wa_direct_link = f"https://wa.me/{wa_p}"

    booking_row = [
        booking_id,
        timestamp,
        name,
        phone,
        wa_direct_link,
        interest_level,
        visit_date,
        visit_time,
        "1570 sqft (3 Bed, 3 Bath, G+9)",
        "৳48.25 Lakh (36-Mo Installment)",
        summary,
        f"Alert dispatched to {whatsapp_dispatcher.OWNER_WHATSAPP}",
        "Call customer to confirm site meeting & share Google Maps location",
        "Site Visit Scheduled"
    ]

    with open(BOOKINGS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(booking_row)

    print(f"\n[✓ BOOKING RECORDED IN CSV: {booking_id}]")
    print(f"  File: {BOOKINGS_CSV}")

    # Dispatch automatic WhatsApp alert to owner
    booking_alert_payload = {
        "booking_id": booking_id,
        "name": name,
        "phone": phone,
        "visit_date": visit_date,
        "visit_time": visit_time,
        "interest_level": interest_level,
        "summary": summary
    }
    whatsapp_dispatcher.send_whatsapp_alert(booking_alert_payload)

    return booking_alert_payload


def process_sales_conversation(user_message: str, customer_name: str = "সম্মানিত ক্রেতা", context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Polite, professional real estate salesman logic:
    - Answers inquiries with prestige
    - Overcomes hesitation with legal & penalty guarantees
    - Always proposes and secures a physical site visit appointment
    """
    if context is None:
        context = {}

    msg_lower = user_message.lower()
    phone_match = BD_PHONE_REGEX.search(user_message)

    # 1. Phone number detected -> Book Site Visit & Trigger WhatsApp alert
    if phone_match:
        phone_num = phone_match.group(0)
        
        # Detect if day/time mentioned
        visit_date = "আগামী শুক্র/শনিবার (সুবিধাজনক সময়ে)"
        if any(d in msg_lower for d in ["friday", "শুক্রবার", "sukrobar", "shukrobar"]):
            visit_date = "শুক্রবার (সকাল ১১:০০ টা)"
        elif any(d in msg_lower for d in ["saturday", "শনিবার", "sonibar"]):
            visit_date = "শনিবার (দুপুর ১২:০০ টা)"
        elif any(d in msg_lower for d in ["tomorrow", "কাল", "kalke", "kalke"]):
            visit_date = "আগামীকাল (বিকাল ৪:০০ টা)"

        summary_note = f"ক্রেতা ফোন নাম্বার প্রদান করেছেন। প্রজেক্ট ১০-এর ১৫৭০ স্কয়ার ফিট ফ্ল্যাট বুকিং ও সাইট পরিদর্শনে আগ্রহী। ({user_message})"
        
        record_project_booking(
            name=customer_name,
            phone=phone_num,
            visit_date=visit_date,
            visit_time="সকাল ১১:০০ টা",
            summary=summary_note,
            interest_level="🔥 Hot Lead (Visit Booked)"
        )

        response_text = (
            f"অসংখ্য ধন্যবাদ শ্রদ্ধেয় {customer_name}! আপনার মোবাইল নাম্বারটি ({phone_num}) আমাদের সিস্টেমে যত্নসহকারে নিবন্ধিত হয়েছে।\n\n"
            f"📅 আমরা আপনার জন্য 'প্রজেক্ট ১০' পরিদর্শনের একটি বিশেষ স্লট নির্ধারণ করেছি:\n"
            f"• সম্ভাব্য সময়: {visit_date}\n"
            f"• লোকেশন: ভুঁইয়া বাড়ি, বাশতলা (আজমপুর উত্তরা থেকে মাত্র ১০ মিনিট)\n\n"
            "আমাদের সিনিয়র সেলস এক্সিকিউটিভ অতি শীঘ্রই আপনার সাথে সরাসরি যোগাযোগ করে "
            "হোয়াটসঅ্যাপে গুগল ম্যাপস লোকেশন পিন এবং প্রজেক্টের সম্পূর্ণ আর্কিটেকচারাল ব্রোশার পাঠিয়ে দেবেন।\n\n"
            "জরুরি যেকোনো সহায়তার জন্য আপনিও সরাসরি কল করতে পারেন:\n"
            "📞 01805-892106\n"
            "📞 01633-309081\n\n"
            "মল্লিক বিল্ডার্স লিমিটেডের সাথে আপনার স্বপ্নের নীড় গড়ার পথচলা নিরাপদ ও আনন্দময় হোক।"
        )
        return {
            "reply": response_text,
            "action": "BOOKING_CONFIRMED",
            "phone": phone_num,
            "visit_date": visit_date
        }

    # 2. Price / Installment Inquiry
    if any(k in msg_lower for k in ["price", "cost", "dam", "taka", "দাম", "কত", "কিস্তি", "kisti", "লাখ", "টাকা", "বাজেট"]):
        response_text = (
            f"আসসালামু আলাইকুম শ্রদ্ধেয় {customer_name}। মল্লিক বিল্ডার্স লিমিটেডে আপনাকে আন্তরিক স্বাগতম।\n\n"
            "উত্তরার সন্নিকটে আমাদের 'প্রজেক্ট ১০'-এ ১৫৭০ স্কয়ার ফিটের সুবিশাল ৩-বেড বিলাসবহুল ফ্ল্যাটের মোট মূল্য জমি শেয়ারিং পদ্ধতিতে অত্যন্ত সাশ্রয়ী:\n\n"
            "💰 সম্পূর্ণ আর্থিক হিসাব:\n"
            "• জমি শেয়ার মূল্য: ৳১২,০০,০০০ (নিষ্কণ্টক সাব-কবলা রেজিস্ট্রি)\n"
            "• আধুনিক নির্মাণ খরচ: ৳৩৬,২৫,০০০\n"
            "👉 সর্বমোট ফ্ল্যাট মূল্য: মাত্র ৳৪৮,২৫,০০০ টাকা!\n\n"
            "✨ বিশেষ পরিশোধ সুবিধা:\n"
            "• সম্পূর্ণ নির্মাণ খরচ ৩৬ মাসের সহজ কিস্তিতে পরিশোধযোগ্য।\n"
            "• আইনি সুরক্ষা: নির্ধারিত ৩৬ মাসের মধ্যে হস্তান্তর না হলে ডেভেলপার কোম্পানি লিখিত চুক্তি অনুযায়ী ক্ষতিপূরণ ভাড়া পরিশোধ করবে!\n\n"
            "স্যার, উত্তরায় যেখানে একটি ফ্ল্যাটের মূল্য কোটি টাকা ছাড়িয়ে যায়, সেখানে মাত্র ১০ মিনিটের দূরত্বে এত চমৎকার সুযোগ সীমিত কিছু শেয়ারের জন্য অবশিষ্ট রয়েছে।\n\n"
            "সরাসরি সাইট পরিদর্শন এবং আপনার পরিবারের পছন্দ অনুযায়ী ফ্লোর দেখার জন্য আপনার মোবাইল নাম্বারটি কি দেওয়া যাবে? আমি আপনার জন্য একটি ভিজিট অ্যাপয়েন্টমেন্ট বুক করে দিচ্ছি।"
        )
        return {"reply": response_text, "action": "PRICE_EXPLAINED"}

    # 3. Location / Distance Inquiry
    if any(k in msg_lower for k in ["location", "address", "kothay", "জায়গা", "লোকেশন", "ঠিকানা", "কোথায়", "উত্তরা", "road", "রাস্তা"]):
        response_text = (
            f"আসসালামু আলাইকুম {customer_name} স্যার।\n\n"
            "আমাদের 'প্রজেক্ট ১০' এর অবস্থান অত্যন্ত চমৎকার ও দ্রুত বর্ধনশীল আবাসিক এলাকায়:\n\n"
            "📍 সুনির্দিষ্ট ঠিকানা:\n"
            "ভুঁইয়া বাড়ি, বাশতলা (মাজার চৌরাস্তা সংলগ্ন, ঢাকা)।\n\n"
            "🚗 যাতায়াত ও আধুনিক যোগাযোগ:\n"
            "• আজমপুর উত্তরা থেকে মাত্র ১০ মিনিটের দূরত্ব\n"
            "• হযরত শাহজালাল আন্তর্জাতিক বিমানবন্দর থেকে মাত্র ১৫ মিনিট\n"
            "• ২০ ও ১৬ ফিট প্রশস্ত সংযোগ সড়ক এবং সামনে সুবিশাল ১০০ ফিট প্রস্তাবিত এভিনিউ\n\n"
            "কোলাহলমুক্ত, উন্মুক্ত আলো-বাতাস সমৃদ্ধ পরিবেশ যা আপনার পরিবারের মানসিক প্রশান্তির জন্য আদর্শ।\n\n"
            "স্যার, নিজের চোখে প্রজেক্টের অবস্থান ও প্রশস্ত সড়ক দেখতে আগামী শুক্র বা শনিবার সরাসরি সাইট ঘুরে দেখার জন্য আপনার ফোন নাম্বারটি প্রদান করুন, আমাদের প্রতিনিধি আপনাকে লোকেশন ম্যাপ পাঠিয়ে রিসিভ করবে।"
        )
        return {"reply": response_text, "action": "LOCATION_EXPLAINED"}

    # 4. Specifications / Living Amenities Inquiry
    if any(k in msg_lower for k in ["sqft", "bed", "size", "স্কয়ার", "ফ্লোর", "প্ল্যান", "সুবিধা", "amenities", "lift", "লিফট"]):
        response_text = (
            f"ধন্যবাদ শ্রদ্ধেয় {customer_name}। 'প্রজেক্ট ১০'-এ আমরা নিশ্চিত করেছি প্রিমিয়াম কনডো লিভিংয়ের সকল আধুনিক আয়োজন:\n\n"
            "🏡 ফ্ল্যাট স্পেসিফিকেশন:\n"
            "• ১৫৭০ স্কয়ার ফিট গ্রস (১২৫০ স্কয়ার ফিট নেট ইউজেবল স্পেস)\n"
            "• ৩টি বড় বেডরুম, ৩টি আধুনিক বাথরুম, সুবিশাল খোলামেলা ড্রয়িং ও ডাইনিং স্পেস\n"
            "• আলো-বাতাসে পরিপূর্ণ ২টি প্রশস্ত বারান্দা\n\n"
            "🏢 কন্ডোমিনিয়ামের এক্সক্লুসিভ সুবিধাসমূহ:\n"
            "• ৮.৭২ কাঠা জমির ওপর নান্দনিক ১০ তলা (G+9) আর্কিটেকচার\n"
            "• ২টি বিশ্বমানের হাই-স্পিড প্যাসেঞ্জার লিফট\n"
            "• ৫,০০০ স্কয়ার ফিটের সুবিশাল ল্যান্ডস্কেপড রুফটপ গার্ডেন ও কিডস প্লে জোন\n"
            "• কমপ্লেক্সের ভেতরেই নিজস্ব নামাজ ঘর (মসজিদ) এবং ডেইলি সুপার শপ\n"
            "• সার্বক্ষণিক অটোমেটিক জেনারেটর ব্যাকআপ ও ২৪ ঘণ্টা সিসিটিভি নিরাপত্তা\n\n"
            "ফ্ল্যাটটির আর্কিটেকচারাল ফ্লোর প্ল্যান ও ভিডিও ব্রোশার আপনার হোয়াটসঅ্যাপে দেখতে চাইলে আপনার নাম্বারটি ইনবক্স করুন।"
        )
        return {"reply": response_text, "action": "SPECS_EXPLAINED"}

    # 5. Site Visit / Booking Intent
    if any(k in msg_lower for k in ["visit", "ভিজিট", "দেখা", "dekhte", "booking", "বুকিং", "dekha"]):
        response_text = (
            f"নিশ্চয়ই {customer_name} স্যার! আপনার মতো একজন রুচিশীল ক্রেতাকে আমাদের প্রজেক্টে স্বাগত জানাতে আমরা আনন্দিত হব।\n\n"
            "সরাসরি সাইট পরিদর্শন করলে আপনি জমির অবস্থান, রাস্তার প্রশস্ততা এবং নির্মাণ সামগ্রীর গুণগত মান নিজেই যাচাই করতে পারবেন।\n\n"
            "📅 আপনার সুবিধার জন্য কোন দিনটি ভালো হবে?\n"
            "১. আগামী শুক্রবার সকাল ১১:০০ টা\n"
            "২. আগামী শনিবার দুপুর ১২:০০ টা\n"
            "৩. আপনার পছন্দমতো অন্য যেকোনো দিন\n\n"
            "অনুগ্রহ করে আপনার যোগাযোগের মোবাইল নাম্বারটি প্রদান করুন, যাতে আমরা আপনার ভিজিট স্লটটি কনফার্ম করে সাইটের গুগল লোকেশন ম্যাপ হোয়াটসঅ্যাপে পাঠিয়ে দিতে পারি।"
        )
        return {"reply": response_text, "action": "PROPOSING_VISIT"}

    # Default Polite Welcome & Sales Pitch
    default_text = (
        f"আসসালামু আলাইকুম শ্রদ্ধেয় {customer_name}! মল্লিক বিল্ডার্স লিমিটেডে আপনাকে আন্তরিক স্বাগতম।\n\n"
        "ঢাকা উত্তরায় যারা নিজের স্বপ্নের ঠিকানা খুঁজছেন, তাদের জন্য আজমপুর থেকে মাত্র ১০ মিনিট দূরত্বে বাশতলায় আমাদের 'প্রজেক্ট ১০' দিচ্ছে "
        "৮.৭২ কাঠার ওপর G+9 আধুনিক কন্ডোমিনিয়ামে ১৫৭০ স্কয়ার ফিট ৩-বেড ফ্ল্যাট মাত্র ৪৮.২৫ লাখ টাকায় (৩৬ মাসের সহজ কিস্তিতে)!\n\n"
        "আপনার সুবিধার্থে প্রজেক্ট ১০-এর কোন বিষয়টি জানতে চাচ্ছেন?\n"
        "১. 💰 জমি শেয়ার ও ৩৬ মাসের কিস্তির সম্পূর্ণ হিসাব\n"
        "২. 📍 সঠিক লোকেশন ম্যাপ ও উত্তরার সাথে যাতায়াত\n"
        "৩. 🏢 ১৫৭০ স্কয়ার ফিট ফ্ল্যাটের ফ্লোর প্ল্যান ও সুবিধাসমূহ\n"
        "৪. 🤝 সাইট ভিজিট বুকিং ও নিষ্কণ্টক আইনি দলিলপত্র\n\n"
        "অথবা সরাসরি কথা বলতে ও ভিজিট স্লট বুক করতে আপনার মোবাইল নাম্বারটি লিখে পাঠান।"
    )
    return {"reply": default_text, "action": "WELCOME"}


def simulate_full_sales_experience():
    """Runs a complete simulated conversation demonstrating professional salesman dialogue."""
    print("\n" + "=" * 75)
    print("MOLLIK BUILDERS: AI SALES CONSULTANT & AUTOMATED BOOKING DEMO")
    print("=" * 75)

    conversations = [
        ("Dr. Shafiqul Islam", "ভাই আপনাদের প্রজেক্টের দাম কত? কিস্তিতে দেওয়া যাবে?"),
        ("Dr. Shafiqul Islam", "লোকেশনটা উত্তরা আজমপুর থেকে কত দূর? রাস্তা কেমন?"),
        ("Dr. Shafiqul Islam", "ফ্ল্যাটের সাইজ আর ভেতরে কী কী সুবিধা আছে?"),
        ("Dr. Shafiqul Islam", "আমি শুক্রবার সকালে স্বচক্ষে দেখতে চাই। আমার নাম্বার 01718992233।")
    ]

    for speaker, msg in conversations:
        print(f"\n👤 [{speaker}]: \"{msg}\"")
        result = process_sales_conversation(msg, customer_name=speaker)
        print(f"\n🤖 [Mollik Builders Sales Advisor]:\n{result['reply']}")
        print("-" * 75)


if __name__ == "__main__":
    init_bookings_csv()
    simulate_full_sales_experience()

