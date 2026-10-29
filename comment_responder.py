#!/usr/bin/env python3
"""
Mollik Builders Ltd - Project 10
Automated Comment Responder & Lead Extraction Engine

Features:
- Monitors comments on the boosted post/video (Page Post ID: 122117565777496265)
- Smart Intent Classification (Price/Installment, Location, Details/Brochure, Contact, Phone Left)
- Natural Bengali replies with varied copy (anti-bot / anti-spam safeguards)
- Automatic Lead Capture: Detects Bangladeshi phone numbers in comments and saves to leads.csv
- Prevents duplicate replies using a persistent SQLite/JSON state
"""

import os
import re
import sys
import time
import json
import random
import csv
from datetime import datetime
from typing import Dict, Any, List, Optional
import requests
import sales_agent

# Default Project Details & Configuration
DEFAULT_PAGE_ID = "1398984063295562"
DEFAULT_POST_ID = "122117565777496265"  # Exact post ID for Project 10 Reel
CANONICAL_STORY_ID = f"{DEFAULT_PAGE_ID}_{DEFAULT_POST_ID}"

STATE_DIR = "data"
STATE_FILE = os.path.join(STATE_DIR, "comment_replies.json")
LEADS_FILE = os.path.join(STATE_DIR, "leads.csv")

# Phone Regex for Bangladesh numbers (e.g. 017xxxxxxxx, 018xxxxxxxx, +8801xxxxxxxxx)
BD_PHONE_REGEX = re.compile(r"(?:\+?880|0)?1[3-9]\d{8}\b")

# Response Templates with High-Converting Variations
REPLY_TEMPLATES = {
    "phone_detected": [
        "ধন্যবাদ আপনার মোবাইল নাম্বার দেওয়ার জন্য! আমাদের সিনিয়র সেলস টিম থেকে খুব দ্রুত আপনার সাথে সরাসরি যোগাযোগ করে 'প্রজেক্ট ১০'-এর বিস্তারিত ব্রোশার ও মূল্য তালিকা হোয়াটসঅ্যাপে প্রদান করা হবে। অথবা যেকোনো প্রয়োজনে এখনই কল করতে পারেন: 01805-892106 / 01633-309081।",
        "অসংখ্য ধন্যবাদ! আমরা আপনার সাথে শীঘ্রই সরাসরি যোগাযোগ করছি। মল্লিক বিল্ডার্স লিমিটেডের পক্ষ থেকে আপনার জন্য শুভকামনা। জরুরি প্রয়োজনে কল করুন: 01805-892106।"
    ],
    "price_inquiry": [
        "আসসালামু আলাইকুম! মল্লিক বিল্ডার্স 'প্রজেক্ট ১০'-এ ১৫৭০ স্কয়ার ফিট ৩-বেড বিলাসবহুল ফ্ল্যাটের মোট মূল্য মাত্র ৪৮.২৫ লাখ টাকা (জমি শেয়ার ১২ লাখ + নির্মাণ ৩৬.২৫ লাখ)। রয়েছে ৩৬ মাসের সহজ কিস্তির সুবিধা! বিস্তারিত বুকিং তথ্যের জন্য কল বা হোয়াটসঅ্যাপ করুন: 01805-892106 অথবা 01633-309081।",
        "ধন্যবাদ আপনার আগ্রহের জন্য। আমাদের জমি শেয়ারিং প্রাইসিং: জমি শেয়ার ৳১২ লাখ এবং নির্মাণ খরচ ৳৩৬.২৫ লাখ = সর্বমোট ৳৪৮.২৫ লাখ। ৩৬ মাসের সহজ কিস্তিতে পরিশোধযোগ্য। সরাসরি সাইট ভিজিট ও পেপারস যাচাই করতে এখনই কল করুন: 01805-892106।",
        "শুভেচ্ছা! প্রজেক্ট ১০-এ ৩ বেড, ৩ বাথের ১৫৭০ স্কয়ার ফিট ফ্ল্যাট পাচ্ছেন মাত্র ৪৮.২৫ লাখে। ৩৬ মাসের ফ্লেক্সিবল কিস্তির ব্যবস্থা রয়েছে। নির্ধারিত সময়ে হস্তান্তর না হলে ক্ষতিপূরণ ভাড়ার নিশ্চয়তা! বিস্তারিত জানতে কল করুন: 01805-892106 / 01633-309081।"
    ],
    "location_inquiry": [
        "আসসালামু আলাইকুম! প্রজেক্টটি ঢাকা উত্তরার সন্নিকটে 'ভুঁইয়া বাড়ি, বাশতলা' (মাজার চৌরাস্তা সংলগ্ন) অবস্থিত। আজমপুর উত্তরা থেকে মাত্র ১০ মিনিট এবং হযরত শাহজালাল বিমানবন্দর থেকে ১৫ মিনিটের দূরত্ব। সরাসরি সাইট লোকেশন ম্যাপ ও ভিজিটের জন্য কল করুন: 01805-892106।",
        "ধন্যবাদ! আমাদের 'প্রজেক্ট ১০' এর অবস্থান: বাশতলা, ভুঁইয়া বাড়ি (মাজার চৌরাস্তা সংলগ্ন)। উত্তরা আজমপুর থেকে মাত্র ১০ মিনিটের পথ। ২০ ও ১৬ ফিট সংযোগ সড়ক এবং সামনে প্রস্তাবিত ১০০ ফিট রোড রয়েছে। সরাসরি ভিজিট করতে কল করুন: 01805-892106 / 01633-309081।"
    ],
    "details_inquiry": [
        "আসসালামু আলাইকুম! 'প্রজেক্ট ১০'-এ থাকছে ৮.৭২ কাঠার ওপর G+9 আধুনিক কন্ডো লিভিং। ১৫৭০ স্কয়ার ফিট গ্রস (১২৫০ স্কয়ার ফিট নেট ইউজেবল), ৩ বেড, ৩ বাথ, ড্রয়িং-ডাইনিং, ২টি লিফট, নিজস্ব মসজিদ, সুপার শপ ও ৫০০০ স্কয়ার ফিট রুফটপ গার্ডেন। বিস্তারিত ব্রোশার পেতে হোয়াটসঅ্যাপ করুন: 01805-892106।",
        "ধন্যবাদ আপনার কমেন্টের জন্য। প্রজেক্টের সম্পূর্ণ ব্রোশার, ফ্লোর প্ল্যান ও ভিডিও পেতে অনুগ্রহ করে আমাদের ইনবক্সে মেসেজ দিন অথবা সরাসরি কল/হোয়াটসঅ্যাপ করুন: 01805-892106 / 01633-309081।"
    ],
    "general": [
        "আসসালামু আলাইকুম! মল্লিক বিল্ডার্স লিমিটেডের প্রজেক্টে আগ্রহ প্রকাশের জন্য ধন্যবাদ। উত্তরা সংলগ্ন বাশতলায় ১৫৭০ স্কয়ার ফিট ৩-বেড ফ্ল্যাট মাত্র ৪৮.২৫ লাখে ৩৬ মাসের কিস্তিতে নিশ্চিত করতে আজই যোগাযোগ করুন: 01805-892106 / 01633-309081।",
        "ধন্যবাদ! আপনার যেকোনো প্রশ্ন, সাইট ভিজিট বা বুকিংয়ের জন্য আমাদের ইনবক্স করুন অথবা সরাসরি কল করুন: 01805-892106।"
    ]
}


def load_env() -> Dict[str, str]:
    """Loads environment variables from .env or .env.marketing."""
    env = {}
    for filename in [".env.marketing", ".env"]:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env[k.strip()] = v.strip().strip("'").strip('"')
    return env


def init_storage():
    """Initializes state and leads storage files."""
    os.makedirs(STATE_DIR, exist_ok=True)
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"processed_comment_ids": []}, f, indent=2)

    if not os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Source", "Customer_Name", "User_ID", "Phone", "Comment_Text", "Status"])


def get_processed_ids() -> set:
    """Returns set of already answered comment IDs."""
    if not os.path.exists(STATE_FILE):
        return set()
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("processed_comment_ids", []))
    except Exception:
        return set()


def mark_comment_processed(comment_id: str):
    """Marks a comment ID as processed."""
    processed = get_processed_ids()
    processed.add(comment_id)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"processed_comment_ids": list(processed)}, f, indent=2)


def save_lead(name: str, user_id: str, phone: str, text: str, source: str = "Video_Comment"):
    """Saves captured lead into leads.csv and project_bookings.csv, and triggers WhatsApp alert."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, source, name, user_id, phone, text, "New"])
    print(f"\n[🔥 NEW HOT LEAD CAPTURED FROM COMMENT!]")
    print(f"  Name:  {name}")
    print(f"  Phone: {phone}")
    print(f"  Note:  {text}")
    print(f"  Saved to: {LEADS_FILE}\n")

    # Record into project bookings database and dispatch WhatsApp notification to owner (+8801633309081)
    sales_agent.record_project_booking(
        name=name,
        phone=phone,
        visit_date="এই সপ্তাহে (সুবিধাজনক সময়ে)",
        visit_time="সকাল ১১:০০ টা",
        summary=f"ফেসবুক ভিডিও কমেন্ট থেকে সরাসরি ফোন নাম্বার দিয়েছেন: \"{text}\"",
        interest_level="🔥 Hot Lead (Video Comment)"
    )


def classify_intent(text: str) -> str:
    """Classifies user comment intent based on keyword triggers."""
    text_lower = text.lower()

    # 1. Check if phone number is present
    if BD_PHONE_REGEX.search(text):
        return "phone_detected"

    # 2. Price / Cost / Installment
    price_keywords = [
        "price", "daam", "dam", "cost", "taka", "tk", "কত", "দাম", "টাকা", "প্রাইস",
        "কিস্তি", "kisti", "installment", "rate", "budget", "বাজেট", "খরচ", "লাখ", "lakh"
    ]
    if any(kw in text_lower for kw in price_keywords):
        return "price_inquiry"

    # 3. Location / Address / Distance
    loc_keywords = [
        "location", "address", "kothay", "where", "জায়গা", "লোকেশন", "ঠিকানা",
        "কোথায়", "uttara", "road", "রাস্তা", "ম্যাপ", "map", "বাস্থলা", "বাশতলা"
    ]
    if any(kw in text_lower for kw in loc_keywords):
        return "location_inquiry"

    # 4. Details / Floor plan / Brochure / Handover
    details_keywords = [
        "detail", "details", "বিবরণ", "প্ল্যান", "ফ্লোর", "floor", "plan", "sqft",
        "স্কয়ার", "handover", "হস্তান্তর", "brochure", "বুকিং", "booking", "visit", "ভিজিট"
    ]
    if any(kw in text_lower for kw in details_keywords):
        return "details_inquiry"

    return "general"


def fetch_comments(access_token: str, post_id: str) -> List[Dict[str, Any]]:
    """Fetches comments from Facebook Graph API for the post."""
    url = f"https://graph.facebook.com/v26.0/{post_id}/comments"
    params = {
        "access_token": access_token,
        "fields": "id,from,message,created_time",
        "limit": 50,
        "order": "reverse_chronological"
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    if "error" in data:
        print(f"[API ERROR] {data['error'].get('message')}")
        return []
    return data.get("data", [])


def post_reply(access_token: str, comment_id: str, reply_text: str) -> bool:
    """Posts a reply to a comment via Graph API."""
    url = f"https://graph.facebook.com/v26.0/{comment_id}/comments"
    params = {
        "access_token": access_token,
        "message": reply_text
    }
    resp = requests.post(url, data=params)
    data = resp.json()
    if "error" in data:
        print(f"[REPLY FAILED for {comment_id}]: {data['error'].get('message')}")
        return False
    print(f"[REPLIED SUCCESS to {comment_id}]: {data.get('id')}")
    return True


def process_comments(access_token: str, post_id: str, dry_run: bool = False):
    """Fetches new comments and replies intelligently."""
    processed = get_processed_ids()
    comments = fetch_comments(access_token, post_id)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Polled {len(comments)} comments from post {post_id}.")

    for c in comments:
        c_id = c.get("id")
        if not c_id or c_id in processed:
            continue

        message = c.get("message", "").strip()
        from_user = c.get("from", {})
        user_name = from_user.get("name", "Interested Buyer")
        user_id = from_user.get("id", "Unknown")

        if not message:
            continue

        print(f"\n[NEW COMMENT DETECTED]")
        print(f"  From:    {user_name} ({user_id})")
        print(f"  Comment: \"{message}\"")

        # Check for phone number
        phone_match = BD_PHONE_REGEX.search(message)
        if phone_match:
            phone_num = phone_match.group(0)
            save_lead(user_name, user_id, phone_num, message)

        intent = classify_intent(message)
        reply_template = random.choice(REPLY_TEMPLATES[intent])

        print(f"  Intent:  {intent}")
        print(f"  Reply:   \"{reply_template}\"")

        if dry_run:
            print("  [DRY-RUN] Reply logged, not posted to API.")
            mark_comment_processed(c_id)
        else:
            success = post_reply(access_token, c_id, reply_template)
            if success:
                mark_comment_processed(c_id)
                # Polite human-like delay to prevent Facebook rate limiting
                time.sleep(random.uniform(2.5, 5.0))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Mollik Builders Automated Comment Responder")
    parser.add_argument("--dry-run", action="store_true", help="Preview replies without sending to Facebook")
    parser.add_argument("--loop", action="store_true", help="Run continuously in a loop polling every N seconds")
    parser.add_argument("--interval", type=int, default=60, help="Poll interval in seconds (default: 60)")
    parser.add_argument("--post-id", type=str, default=CANONICAL_STORY_ID, help="Post ID to monitor")
    args = parser.parse_args()

    init_storage()
    env = load_env()
    token = env.get("META_ACCESS_TOKEN")

    if not token and not args.dry_run:
        print("[ERROR] META_ACCESS_TOKEN is required in .env.marketing")
        sys.exit(1)

    print("=" * 65)
    print("MOLLIK BUILDERS: AUTOMATED COMMENT RESPONDER & LEAD EXTRACTOR")
    print(f"Target Post: {args.post_id}")
    print(f"Storage:     {STATE_FILE} | Leads: {LEADS_FILE}")
    print(f"Mode:        {'DRY-RUN' if args.dry_run else 'LIVE'} (Loop: {args.loop})")
    print("=" * 65)

    if args.loop:
        print(f"[INFO] Running loop every {args.interval} seconds. Press Ctrl+C to stop.\n")
        try:
            while True:
                process_comments(token or "DUMMY_TOKEN", args.post_id, dry_run=args.dry_run)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n[INFO] Stopped comment responder.")
    else:
        process_comments(token or "DUMMY_TOKEN", args.post_id, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

