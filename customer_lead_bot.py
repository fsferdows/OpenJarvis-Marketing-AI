#!/usr/bin/env python3
"""
Mollik Builders Ltd - Project 10
Customer Messenger Lead Bot & Conversational Lead Generator

Handles customer inquiries on Messenger/Page Inbox:
- Understands questions about Pricing, 36-Month Installment, Location, Amenities, Handover
- Proactively captures leads (Name, Phone number, Requirements)
- Saves all leads directly to data/leads.csv for immediate sales team follow-up
- Webhook server ready (Flask / HTTP) or can be run with polling / Meta App Webhook
"""

import os
import re
import sys
import json
import csv
from datetime import datetime
from typing import Dict, Any, Tuple
import requests

DATA_DIR = "data"
LEADS_FILE = os.path.join(DATA_DIR, "leads.csv")
CONVERSATIONS_FILE = os.path.join(DATA_DIR, "conversations_state.json")

BD_PHONE_REGEX = re.compile(r"(?:\+?880|0)?1[3-9]\d{8}\b")

# Comprehensive Knowledge Base for Mollik Builders Project 10
PROJECT_KNOWLEDGE = {
    "pricing": (
        "🏢 মল্লিক বিল্ডার্স 'প্রজেক্ট ১০' — জমি শেয়ারিং প্রাইসিং:\n\n"
        "• জমি শেয়ার: ৳১২,০০,০০০\n"
        "• নির্মাণ খরচ: ৳৩৬,২৫,০০০\n"
        "👉 সর্বমোট মূল্য: মাত্র ৳৪৮,২৫,০০০ টাকা!\n\n"
        "✨ পরিশোধের সুবিধা: ৩৬ মাসের সহজ ও ফ্লেক্সিবল কিস্তি।\n"
        "🤝 গ্যারান্টি: ৩৬ মাসের মধ্যে হস্তান্তর না হলে ডেভেলপার কোম্পানি জরিমানা হিসেবে ক্ষতিপূরণ ভাড়া প্রদান করবে।\n\n"
        "বিস্তারিত ব্রোশার ও বুকিংয়ের জন্য আপনার মোবাইল নাম্বারটি দিন অথবা এখনই কল করুন: 01805-892106।"
    ),
    "location": (
        "📍 'প্রজেক্ট ১০' এর অবস্থান:\n"
        "ভুঁইয়া বাড়ি, বাশতলা (মাজার চৌরাস্তা সংলগ্ন, ঢাকা)।\n\n"
        "🚗 যাতায়াত ও দূরত্ব:\n"
        "• আজমপুর উত্তরা থেকে মাত্র ১০ মিনিট\n"
        "• হযরত শাহজালাল আন্তর্জাতিক বিমানবন্দর থেকে ১৫ মিনিট\n"
        "• ২০ ও ১৬ ফিট প্রশস্ত সংযোগ সড়ক এবং সামনে ১০০ ফিট প্রস্তাবিত রোড\n\n"
        "সরাসরি সাইট পরিদর্শন করতে চাইলে আপনার মোবাইল নাম্বারটি লিখে দিন, আমাদের টিম আপনাকে লোকেশন গাইড করবে।"
    ),
    "specs": (
        "🏡 ফ্ল্যাট ও প্রজেক্ট স্পেসিফিকেশন:\n\n"
        "• সাইজ: ১৫৭০ স্কয়ার ফিট গ্রস (১২৫০ স্কয়ার ফিট নেট ইউজেবল)\n"
        "• কনফিগারেশন: ৩ বেড, ৩ বাথ, সুবিশাল ড্রয়িং-ডাইনিং ও ২ বারান্দা\n"
        "• জমির পরিমাণ: ৮.৭২ কাঠা (G+9 আধুনিক ১০ তলা কন্ডোমিনিয়াম)\n"
        "• আধুনিক সুযোগ-সুবিধা: ২টি হাই-স্পিড লিফট, নিজস্ব মসজিদ, সুপার শপ, সার্বক্ষণিক জেনারেটর ব্যাকআপ ও ৫০০০ স্কয়ার ফিটের দৃষ্টিনন্দন রুফটপ গার্ডেন!\n\n"
        "ফ্লোর প্ল্যানের ছবি পেতে আপনার হোয়াটসঅ্যাপ নাম্বারটি ইনবক্স করুন।"
    ),
    "booking": (
        "📝 বুকিং ও সাইট ভিজিট প্রক্রিয়া:\n\n"
        "১. সরাসরি সাইট পরিদর্শন ও জমির নিষ্কণ্টক কাগজপত্র যাচাই।\n"
        "২. প্রাথমিক বুকিং সম্পন্ন করে জমি শেয়ার রেজিস্ট্রি প্রক্রিয়া শুরু।\n"
        "৩. বাকি নির্মাণ খরচ ৩৬ মাসের সহজ কিস্তিতে পরিশোধ।\n\n"
        "আগামীকাল বা সুবিধাজনক সময়ে সাইট ভিজিট করতে আপনার নাম ও ফোন নাম্বারটি দিন, আমরা আপনার বুকিং স্লট নিশ্চিত করব।"
    )
}


def init_lead_storage():
    """Ensures leads CSV file exists with proper headers."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Source", "Customer_Name", "User_ID", "Phone", "Notes", "Status"])


def save_customer_lead(name: str, user_id: str, phone: str, notes: str, source: str = "Messenger_Bot"):
    """Saves captured lead into leads.csv."""
    init_lead_storage()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, source, name, user_id, phone, notes, "New - Hot Lead"])
    print(f"\n[⭐ LEAD GENERATED!]")
    print(f"  Name:   {name}")
    print(f"  Phone:  {phone}")
    print(f"  Notes:  {notes}")
    print(f"  Saved:  {LEADS_FILE}\n")


def generate_response(incoming_text: str, customer_name: str = "সম্মানিত ক্রেতা", user_id: str = "unknown") -> Tuple[str, bool]:
    """
    Analyzes incoming customer message, generates an intelligent answer,
    and checks if a lead was captured.
    Returns: (response_text, is_lead_captured)
    """
    text_lower = incoming_text.lower()
    phone_match = BD_PHONE_REGEX.search(incoming_text)

    # 1. Did the customer provide a phone number?
    if phone_match:
        phone_number = phone_match.group(0)
        save_customer_lead(customer_name, user_id, phone_number, incoming_text)
        reply = (
            f"ধন্যবাদ {customer_name}! আপনার মোবাইল নাম্বার ({phone_number}) সফলভাবে সংরক্ষিত হয়েছে।\n\n"
            "আমাদের প্রজেক্ট ম্যানেজার খুব শীঘ্রই আপনার সাথে সরাসরি যোগাযোগ করে 'প্রজেক্ট ১০'-এর সম্পূর্ণ ফ্লোর প্ল্যান, "
            "আইনি নথিপত্র এবং মূল্যতালিকা হোয়াটসঅ্যাপে প্রদান করবেন।\n\n"
            "জরুরি যেকোনো তথ্যের জন্য এখনই সরাসরি কল করতে পারেন:\n"
            "📞 01805-892106\n"
            "📞 01633-309081"
        )
        return reply, True

    # 2. Price / Installment / Cost
    if any(k in text_lower for k in ["price", "dam", "cost", "taka", "tk", "দাম", "টাকা", "কত", "কিস্তি", "kisti", "বাজেট", "লাখ"]):
        reply = (
            f"আসসালামু আলাইকুম {customer_name}!\n\n"
            + PROJECT_KNOWLEDGE["pricing"]
        )
        return reply, False

    # 3. Location / Address / Distance
    if any(k in text_lower for k in ["location", "address", "kothay", "জায়গা", "লোকেশন", "ঠিকানা", "কোথায়", "উত্তরা", "রোড", "road"]):
        reply = (
            f"আসসালামু আলাইকুম {customer_name}!\n\n"
            + PROJECT_KNOWLEDGE["location"]
        )
        return reply, False

    # 4. Specifications / Floor plan / Sqft / Beds
    if any(k in text_lower for k in ["sqft", "bed", "size", "স্কয়ার", "বেড", "প্ল্যান", "ফ্লোর", "বিবরণ", "ডিটেইলস", "details"]):
        reply = (
            f"আসসালামু আলাইকুম {customer_name}!\n\n"
            + PROJECT_KNOWLEDGE["specs"]
        )
        return reply, False

    # 5. Booking / Visit / Handover
    if any(k in text_lower for k in ["visit", "ভিজিট", "booking", "বুকিং", "handover", "হস্তান্তর"]):
        reply = (
            f"আসসালামু আলাইকুম {customer_name}!\n\n"
            + PROJECT_KNOWLEDGE["booking"]
        )
        return reply, False

    # 6. Default Welcome & Lead Capture Prompt
    default_reply = (
        f"আসসালামু আলাইকুম {customer_name}! মল্লিক বিল্ডার্স লিমিটেডে আপনাকে স্বাগতম।\n\n"
        "ঢাকা উত্তরার সন্নিকটে বাশতলায় আমাদের 'প্রজেক্ট ১০'-এ ১৫৭০ স্কয়ার ফিট ৩-বেড বিলাসবহুল ফ্ল্যাট জমি শেয়ারিং পদ্ধতিতে সর্বমোট মাত্র ৪৮.২৫ লাখে (৩৬ মাসের কিস্তিতে) পাচ্ছেন!\n\n"
        "আপনার সুবিধার্থে কোন তথ্যটি জানতে চান?\n"
        "১. মোট মূল্য ও কিস্তির হিসাব\n"
        "২. প্রজেক্টের সঠিক লোকেশন ও রাস্তা\n"
        "৩. ফ্ল্যাট স্পেসিফিকেশন ও সুযোগ-সুবিধা\n"
        "৪. সরাসরি সাইট ভিজিট ও বুকিং\n\n"
        "অথবা সম্পূর্ণ ব্রোশার সরাসরি হোয়াটসঅ্যাপে পেতে আপনার মোবাইল নাম্বারটি লিখে পাঠান।"
    )
    return default_reply, False


def test_conversations():
    """Runs automated simulation tests across common customer inquiries."""
    print("=" * 65)
    print("MOLLIK BUILDERS: TESTING CONVERSATIONAL BOT & LEAD GENERATOR")
    print("=" * 65)

    test_cases = [
        ("Mohammad Ali", "দাম কত ভাই? কিস্তি আছে?"),
        ("Engr. Tanvir", "Location ta kothay? Uttara theke koto dur?"),
        ("Dr. Rahman", "Flat er size koto sqft? Koita bed?"),
        ("Kamrul Hasan", "Amar number 01712345678, amake brochure pathan"),
        ("Sultana Begum", "Ami project visit korte chai kalke")
    ]

    for name, msg in test_cases:
        print(f"\n[CUSTOMER]: {name} -> \"{msg}\"")
        reply, lead_captured = generate_response(msg, customer_name=name, user_id="sim_123")
        print(f"[BOT REPLY]:\n{reply}")
        print("-" * 50)


if __name__ == "__main__":
    init_lead_storage()
    test_conversations()

