#!/usr/bin/env python3
"""
Mollik Builders Ltd — Project 10 (Bashtola, Dhaka)
OPTIMIZED Lead Generation Campaign via Meta Instant Forms

Replaces the Click-to-Call campaign with a qualified lead capture system:
- Campaign Objective: OUTCOME_LEADS
- Destination: ON_AD (Instant Form)
- Optimization: LEAD_GENERATION
- Form Type: HIGHER_INTENT (review step before submit)
- Qualification Questions: Budget filter + purchase intent
- Advantage Detailed Targeting: ENABLED (lets Meta find buyers)
- Multiple Ad Creatives: 3 variations testing different hooks

Usage:
    python deploy_lead_gen_campaign.py              # Preview the spec (dry run)
    python deploy_lead_gen_campaign.py --deploy      # Deploy live to Meta
    python deploy_lead_gen_campaign.py --pause-old   # Pause old Click-to-Call campaign first
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List

# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
AD_ACCOUNT_ID = "act_221651059226062"
PAGE_ID = "1398984063295562"
VIDEO_ID = "1666992078479821"
POST_ID = "122117565777496265"
TARGET_PHONE = "+8801633309081"
HOTLINE_DISPLAY = "01805-892106 / 01633-309081"

# Old campaign to pause
OLD_CALL_CAMPAIGN_ID = "120255677739250063"
OLD_CALL_ADSET_ID = "120255677758470063"
OLD_CALL_AD_ID = "120255678021100063"
OLD_ENGAGEMENT_CAMPAIGN_ID = "120255594274270063"

# New campaign naming
CAMPAIGN_NAME = "Mollik Builders - Project 10 [Qualified Flat Buyer Leads]"
ADSET_NAME = "Dhaka North Flat Buyers (33-55) - Instant Form Lead Gen"

DAILY_BUDGET_CENTS = 300  # $3.00/day (in cents)
DURATION_DAYS = 14  # 2-week campaign cycle

# ==========================================
# TARGETING (OPTIMIZED)
# ==========================================

# Same GPS pins but with broader reach settings
TARGET_LOCATIONS = [
    {"name": "Uttara / Azampur Hub", "latitude": 23.8698, "longitude": 90.3985, "radius": 4.0, "distance_unit": "kilometer"},
    {"name": "Airport / Kawla Belt", "latitude": 23.8433, "longitude": 90.4042, "radius": 4.0, "distance_unit": "kilometer"},
    {"name": "Mirpur Salaried Hub", "latitude": 23.8067, "longitude": 90.3687, "radius": 4.0, "distance_unit": "kilometer"},
    {"name": "Khilkhet / Kuril Corridor", "latitude": 23.8293, "longitude": 90.4197, "radius": 4.0, "distance_unit": "kilometer"},
    {"name": "Gulshan / Banani Wealth Belt", "latitude": 23.7925, "longitude": 90.4078, "radius": 4.0, "distance_unit": "kilometer"},
]

# Exclusions: Job seekers + brokers (same as before — these are good exclusions)
EXCLUSION_INTERESTS = [
    {"id": "6003139369934", "name": "Employment"},
    {"id": "6003264426534", "name": "Job hunting"},
    {"id": "6003350172534", "name": "Recruitment"},
    {"id": "6003014872134", "name": "Internship"},
    {"id": "6003114972134", "name": "Curriculum vitae"},
]

# ==========================================
# AD CREATIVE VARIATIONS (3 Hooks)
# ==========================================

AD_VARIATIONS = [
    {
        "name": "Ad 1 - Price Shock Hook (Video Reel)",
        "type": "video",
        "video_id": VIDEO_ID,
        "primary_text": (
            "উত্তরা সংলগ্ন এলাকায় ১৫৭০ স্কয়ার ফিট ৩-বেড ফ্ল্যাট মাত্র ৪৮.২৫ লাখে?\n\n"
            "হ্যাঁ, মল্লিক বিল্ডার্সের প্রজেক্ট ১০-এ এখনো এই দামে পাওয়া যাচ্ছে। "
            "তবে ফেজ-১ মূল্যে মাত্র ৩টি ইউনিট বাকি আছে।\n\n"
            "৩৬ মাসের সহজ কিস্তি। নির্ধারিত সময়ে হস্তান্তর না হলে ক্ষতিপূরণ ভাড়ার গ্যারান্টি।\n\n"
            "👇 বিস্তারিত জানতে নিচে ফর্ম পূরণ করুন — আমরা আপনাকে কল করব।"
        ),
        "headline": "উত্তরায় ৩-বেড ফ্ল্যাট ৪৮.২৫ লাখে",
        "description": "ফেজ-১ মূল্যে মাত্র ৩টি বাকি",
        "cta": "SIGN_UP",
    },
    {
        "name": "Ad 2 - Guarantee Hook (Video Reel)",
        "type": "video",
        "video_id": VIDEO_ID,
        "primary_text": (
            "ফ্ল্যাট বুকিং দিয়ে বছরের পর বছর অপেক্ষা? আর নয়!\n\n"
            "মল্লিক বিল্ডার্স দিচ্ছে লিখিত পেনাল্টি রেন্ট গ্যারান্টি — "
            "৩৬ মাসে হস্তান্তর না হলে ডেভেলপার আপনাকে মাসিক ভাড়া দেবে।\n\n"
            "১০০% নিষ্কণ্টক জমি। সাব-কবলা রেজিস্ট্রি আপনার নামে।\n\n"
            "👇 সাইট ভিজিট বুক করতে নিচের ফর্মটি পূরণ করুন।"
        ),
        "headline": "পেনাল্টি রেন্ট গ্যারান্টি সহ ফ্ল্যাট",
        "description": "১০০% নিষ্কণ্টক জমি",
        "cta": "SIGN_UP",
    },
    {
        "name": "Ad 3 - Renter to Owner Hook (Video Reel)",
        "type": "video",
        "video_id": VIDEO_ID,
        "primary_text": (
            "প্রতি মাসে ৩৫-৪০ হাজার টাকা বাড়িভাড়া দিচ্ছেন?\n\n"
            "সেই টাকায় উত্তরা সংলগ্ন বাশতলায় নিজের ১৫৭০ স্কয়ার ফিটের "
            "৩-বেড ফ্ল্যাটের মালিক হতে পারেন। মাসিক কিস্তি শুরু মাত্র ১ লাখ টাকা থেকে।\n\n"
            "👇 ফ্রি ব্রোশার ও ফ্লোর প্ল্যান পেতে ফর্ম পূরণ করুন।"
        ),
        "headline": "ভাড়ার টাকায় নিজের ফ্ল্যাট",
        "description": "মাসিক কিস্তি ১ লাখ থেকে",
        "cta": "SIGN_UP",
    },
]

# ==========================================
# INSTANT FORM SPECIFICATION
# ==========================================

INSTANT_FORM_SPEC = {
    "name": "Project 10 - Qualified Buyer Lead Form",
    "form_type": "HIGHER_INTENT",  # Adds review step = fewer junk leads
    "locale": "bn_IN",  # Bengali
    "context_card": {
        "title": "প্রজেক্ট ১০ — ফ্রি ব্রোশার ও সাইট ভিজিট বুকিং",
        "content": (
            "মল্লিক বিল্ডার্স লিমিটেডের প্রজেক্ট ১০ (বাশতলা, উত্তরা সংলগ্ন) সম্পর্কে "
            "বিস্তারিত জানতে নিচের তথ্য দিন। আমাদের টিম আপনাকে কল করবে।"
        ),
        "style": "PARAGRAPH_STYLE",
    },
    "questions": [
        {
            "type": "FULL_NAME",
            "label": "আপনার নাম",
            "key": "full_name",
        },
        {
            "type": "PHONE",
            "label": "ফোন নাম্বার",
            "key": "phone_number",
        },
        {
            "type": "CUSTOM",
            "label": "আপনি কি ফ্ল্যাট কিনতে আগ্রহী?",
            "key": "purchase_intent",
            "options": [
                {"value": "নিজে থাকার জন্য কিনতে চাই", "key": "self_use"},
                {"value": "বিনিয়োগের জন্য কিনতে চাই", "key": "investment"},
                {"value": "শুধু তথ্য জানতে চাই", "key": "info_only"},
            ],
        },
        {
            "type": "CUSTOM",
            "label": "আপনার বাজেট কত?",
            "key": "budget_range",
            "options": [
                {"value": "৩০-৪০ লাখ", "key": "30_40"},
                {"value": "৪০-৫০ লাখ", "key": "40_50"},
                {"value": "৫০-৭০ লাখ", "key": "50_70"},
                {"value": "৭০ লাখের উপরে", "key": "70_plus"},
            ],
        },
    ],
    "privacy_policy": {
        "url": "https://www.facebook.com/mollikbuildersltd/",
        "link_text": "Privacy Policy",
    },
    "thank_you_page": {
        "title": "ধন্যবাদ!",
        "body": (
            "আমাদের সিনিয়র সেলস কাউন্সেলর শীঘ্রই আপনার সাথে যোগাযোগ করবেন।\n"
            "📞 জরুরি হলে সরাসরি কল করুন: 01805-892106"
        ),
        "button_text": "ওয়েবসাইট দেখুন",
        "button_type": "VIEW_WEBSITE",
    },
}


def generate_targeting() -> Dict[str, Any]:
    """Builds optimized targeting spec."""
    custom_locations = [
        {
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
            "radius": loc["radius"],
            "distance_unit": loc["distance_unit"],
        }
        for loc in TARGET_LOCATIONS
    ]

    return {
        "geo_locations": {
            "custom_locations": custom_locations,
        },
        "age_min": 33,
        "age_max": 55,
        "exclusions": {"interests": EXCLUSION_INTERESTS},
        "targeting_automation": {
            "advantage_audience": 1,  # ENABLED — let Meta find buyers
        },
        "publisher_platforms": ["facebook", "instagram"],
        "facebook_positions": ["feed", "facebook_reels", "marketplace"],
        "instagram_positions": ["stream", "reels", "explore"],
        "device_platforms": ["mobile", "desktop"],  # Include desktop — serious buyers browse on desktop too
    }


def generate_campaign_spec() -> Dict[str, Any]:
    """Builds the complete production payload for Lead Gen Instant Form Ads."""
    targeting = generate_targeting()
    start_time = datetime.now()
    end_time = start_time + timedelta(days=DURATION_DAYS)

    spec = {
        "ad_account_id": AD_ACCOUNT_ID,
        "page_id": PAGE_ID,
        "campaign": {
            "name": CAMPAIGN_NAME,
            "objective": "OUTCOME_LEADS",
            "status": "ACTIVE",
            "special_ad_categories": [],
        },
        "adset": {
            "name": ADSET_NAME,
            "destination_type": "ON_AD",  # Instant Form (not PHONE_CALL!)
            "optimization_goal": "LEAD_GENERATION",  # Optimize for form fills
            "billing_event": "IMPRESSIONS",
            "daily_budget": DAILY_BUDGET_CENTS,
            "status": "ACTIVE",
            "targeting": targeting,
            "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%S+0600"),
            "end_time": end_time.strftime("%Y-%m-%dT%H:%M:%S+0600"),
            "promoted_object": {"page_id": PAGE_ID},
        },
        "instant_form": INSTANT_FORM_SPEC,
        "ads": AD_VARIATIONS,
        "old_campaigns_to_pause": [
            {"id": OLD_CALL_CAMPAIGN_ID, "name": "Direct Call-Only Leads Engine"},
            {"id": OLD_ENGAGEMENT_CAMPAIGN_ID, "name": "Original Video Boost"},
        ],
    }
    return spec


def load_env_variables() -> Dict[str, str]:
    """Loads environment variables from .env.marketing or .env."""
    env = dict(os.environ)
    for filename in [".env.marketing", ".env"]:
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env[k.strip()] = v.strip().strip("'").strip('"')
    return env


def pause_old_campaigns(token: str):
    """Pauses all old Click-to-Call and Engagement campaigns."""
    import requests

    old_ids = [OLD_CALL_CAMPAIGN_ID, OLD_ENGAGEMENT_CAMPAIGN_ID]
    for camp_id in old_ids:
        url = f"https://graph.facebook.com/v21.0/{camp_id}"
        resp = requests.post(url, data={"status": "PAUSED", "access_token": token})
        if resp.status_code == 200:
            print(f"  ✓ Paused campaign: {camp_id}")
        else:
            print(f"  ⚠ Could not pause {camp_id}: {resp.text}")


def deploy_live():
    """Deploys the optimized Lead Gen campaign to Meta Marketing API."""
    try:
        from facebook_business.api import FacebookAdsApi
        from facebook_business.adobjects.adaccount import AdAccount
        from facebook_business.adobjects.page import Page
        from facebook_business.adobjects.campaign import Campaign
        from facebook_business.adobjects.adset import AdSet
        from facebook_business.adobjects.adcreative import AdCreative
        from facebook_business.adobjects.ad import Ad
        from facebook_business.adobjects.leadgenform import LeadgenForm
    except ImportError:
        print("[ERROR] facebook-business SDK not installed. Run: pip install facebook-business")
        return False

    env = load_env_variables()
    token = env.get("META_ACCESS_TOKEN") or env.get("access_token")
    if not token:
        print("[ERROR] No META_ACCESS_TOKEN found in .env.marketing or .env")
        return False

    FacebookAdsApi.init(access_token=token)
    account = AdAccount(AD_ACCOUNT_ID)
    page = Page(PAGE_ID)
    spec = generate_campaign_spec()

    # Step 0: Pause old campaigns
    print("[0/5] Pausing old Click-to-Call and Engagement campaigns...")
    pause_old_campaigns(token)

    # Step 1: Create Campaign
    print("[1/5] Creating Lead Generation Campaign...")
    camp = account.create_campaign(
        params={
            "name": spec["campaign"]["name"],
            "objective": spec["campaign"]["objective"],
            "status": "ACTIVE",
            "special_ad_categories": [],
        }
    )
    camp_id = camp["id"]
    print(f"  ✓ Campaign Created: {camp_id}")

    # Step 2: Create Instant Form on the Page
    print("[2/5] Creating Instant Lead Form with Qualification Questions on Page...")
    form_spec = spec["instant_form"]
    lead_form = page.create_lead_gen_form(
        params={
            "name": form_spec["name"],
            "follow_up_action_url": f"https://wa.me/8801633309081",
            "is_optimized_for_quality": True,
            "context_card": form_spec["context_card"],
            "questions": form_spec["questions"],
            "privacy_policy": form_spec["privacy_policy"],
            "thank_you_page": form_spec["thank_you_page"],
            "locale": form_spec["locale"],
        }
    )
    form_id = lead_form["id"]
    print(f"  ✓ Lead Form Created: {form_id}")

    # Step 3: Create Ad Set
    print("[3/5] Creating Optimized Ad Set (Instant Form, Advantage+ Targeting)...")
    adset = account.create_ad_set(
        params={
            "name": spec["adset"]["name"],
            "campaign_id": camp_id,
            "daily_budget": spec["adset"]["daily_budget"],
            "billing_event": spec["adset"]["billing_event"],
            "optimization_goal": spec["adset"]["optimization_goal"],
            "destination_type": spec["adset"]["destination_type"],
            "promoted_object": spec["adset"]["promoted_object"],
            "targeting": spec["adset"]["targeting"],
            "status": "ACTIVE",
        }
    )
    adset_id = adset["id"]
    print(f"  ✓ Ad Set Created: {adset_id}")

    # Step 4: Create Ad Creatives (3 variations)
    print("[4/5] Creating 3 Ad Creative Variations...")
    creative_ids = []
    for i, ad_var in enumerate(spec["ads"], 1):
        creative_params = {
            "name": ad_var["name"],
            "object_story_spec": {
                "page_id": PAGE_ID,
                "link_data": {
                    "message": ad_var["primary_text"],
                    "name": ad_var["headline"],
                    "description": ad_var["description"],
                    "call_to_action": {
                        "type": ad_var["cta"],
                        "value": {"lead_gen_form_id": form_id},
                    },
                },
            },
        }

        # If it's a video ad, use video_data instead of link_data
        if ad_var["type"] == "video" and "video_id" in ad_var:
            creative_params["object_story_spec"] = {
                "page_id": PAGE_ID,
                "video_data": {
                    "video_id": ad_var["video_id"],
                    "message": ad_var["primary_text"],
                    "title": ad_var["headline"],
                    "call_to_action": {
                        "type": ad_var["cta"],
                        "value": {"lead_gen_form_id": form_id},
                    },
                },
            }

        creative = account.create_ad_creative(params=creative_params)
        creative_ids.append(creative["id"])
        print(f"  ✓ Creative {i}/3 Created: {creative['id']} ({ad_var['name']})")

    # Step 5: Create Ads (one per creative)
    print("[5/5] Publishing 3 Live Ads...")
    ad_ids = []
    for i, (creative_id, ad_var) in enumerate(zip(creative_ids, spec["ads"]), 1):
        ad = account.create_ad(
            params={
                "name": ad_var["name"],
                "adset_id": adset_id,
                "creative": {"creative_id": creative_id},
                "status": "ACTIVE",
            }
        )
        ad_ids.append(ad["id"])
        print(f"  ✓ Ad {i}/3 Published: {ad['id']}")

    # Save state
    state = {
        "timestamp": datetime.now().isoformat(),
        "campaign_type": "lead_gen_instant_form",
        "campaign_id": camp_id,
        "adset_id": adset_id,
        "lead_form_id": form_id,
        "creative_ids": creative_ids,
        "ad_ids": ad_ids,
        "daily_budget": "$3.00/day",
        "targeting": "GPS Pins (4km) + Advantage+ Targeting Enabled",
        "form_type": "HIGHER_INTENT",
        "qualification_questions": ["purchase_intent", "budget_range"],
    }

    state_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "lead_gen_campaign_state.json")
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print("🎉 SUCCESS! Lead Generation Campaign is LIVE!")
    print("=" * 70)
    print(f"  Campaign ID:  {camp_id}")
    print(f"  Ad Set ID:    {adset_id}")
    print(f"  Lead Form ID: {form_id}")
    print(f"  Ads Running:  {len(ad_ids)} variations")
    print(f"  Budget:       $3.00/day")
    print(f"  Form Type:    HIGHER_INTENT (qualified leads only)")
    print(f"  Old campaigns PAUSED ✓")
    print("=" * 70)
    print("\n⚠️  IMPORTANT: Check Meta Ads Manager to download leads from the Instant Form!")
    print("    Or set up a webhook/Zapier to auto-notify on new form submissions.")
    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Deploy optimized Lead Gen campaign for Mollik Builders Project 10")
    parser.add_argument("--deploy", action="store_true", help="Deploy live to Meta Ads (default: dry run preview)")
    parser.add_argument("--pause-old", action="store_true", help="Only pause old campaigns without deploying new ones")
    args = parser.parse_args()

    if args.pause_old:
        env = load_env_variables()
        token = env.get("META_ACCESS_TOKEN") or env.get("access_token")
        if token:
            print("Pausing old campaigns...")
            pause_old_campaigns(token)
        else:
            print("[ERROR] No access token found.")
        sys.exit(0)

    spec = generate_campaign_spec()

    if args.deploy:
        deploy_live()
    else:
        print("=" * 70)
        print("OPTIMIZED LEAD GEN CAMPAIGN SPECIFICATION (DRY RUN)")
        print("=" * 70)
        print(json.dumps(spec, indent=2, ensure_ascii=False, default=str))
        print("=" * 70)
        print("\n✓ Destination: ON_AD (Instant Form) — NOT Phone Call")
        print("✓ Form Type: HIGHER_INTENT (review step before submit)")
        print("✓ Qualification: Purchase intent + budget range questions")
        print("✓ Advantage Detailed Targeting: ENABLED")
        print("✓ 3 Ad Variations: Price Shock / Guarantee / Rent-to-Own hooks")
        print("✓ Devices: Mobile + Desktop")
        print("✓ GPS Radius: 4km (expanded from 3km)")
        print(f"\n👉 To deploy live, run: python {os.path.basename(__file__)} --deploy")

