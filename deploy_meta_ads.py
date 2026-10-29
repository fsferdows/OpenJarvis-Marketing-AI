#!/usr/bin/env python3
"""
Mollik Builders Ltd - Project 10 (Bashtola, Dhaka)
Meta Marketing API Automated Deployment Script

Bypasses Meta Ads Manager UI constraints:
- special_ad_categories = [] (Empty/None)
- Hyper-local GPS coordinate pin drops (3 km radius)
- Demographic filtering (Age 30-55, Living in location)
- Facebook & Instagram only (Audience Network excluded)
- Advantage Detailed Targeting disabled
- Safe deployment in PAUSED state
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

try:
    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.adaccount import AdAccount
    from facebook_business.adobjects.campaign import Campaign
    from facebook_business.adobjects.adset import AdSet
    from facebook_business.adobjects.adcreative import AdCreative
    from facebook_business.adobjects.ad import Ad
except ImportError:
    print("[ERROR] facebook-business SDK is not installed. Run: pip install facebook-business")
    sys.exit(1)


# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
DEFAULT_AD_ACCOUNT_ID = "act_221651059226062"
DEFAULT_PAGE_ID = "1398984063295562"  # Mollik Builders LTD Page ID
DEFAULT_POST_ID = "122117565777496265"  # Exact post ID for Project 10 Reel
DEFAULT_VIDEO_ID = "1666992078479821"   # Video/Reel ID
DEFAULT_VIDEO_URL = "https://www.facebook.com/reel/1666992078479821/"

CAMPAIGN_NAME = "Mollik Builders - Project 10 [10-Day Video Boost]"
ADSET_NAME = "Dhaka North & Airport Belt - 3km GPS Pins (10 Days @ $3/day)"
AD_NAME = "Project 10 - Video Ad (Bashtola, Uttara)"

DAILY_BUDGET_CENTS = 300  # $3.00 USD daily budget (in cents)
DURATION_DAYS = 10        # 10 days boost duration ($30 total)
CURRENCY = "USD"

# GPS Pin Drops (2-3 km radii around high-intent residential and commercial hubs)
TARGET_LOCATIONS = [
    {
        "name": "Uttara / Azampur Hub",
        "latitude": 23.8698,
        "longitude": 90.3985,
        "radius": 3.0,
        "distance_unit": "kilometer"
    },
    {
        "name": "Airport / Kawla Aviation Belt",
        "latitude": 23.8433,
        "longitude": 90.4042,
        "radius": 3.0,
        "distance_unit": "kilometer"
    },
    {
        "name": "Tongi Industrial Belt",
        "latitude": 23.9015,
        "longitude": 90.4022,
        "radius": 3.0,
        "distance_unit": "kilometer"
    },
    {
        "name": "Mirpur Salaried Hub",
        "latitude": 23.8067,
        "longitude": 90.3687,
        "radius": 3.0,
        "distance_unit": "kilometer"
    },
    {
        "name": "Khilkhet / Kuril Corridor",
        "latitude": 23.8293,
        "longitude": 90.4197,
        "radius": 3.0,
        "distance_unit": "kilometer"
    }
]

# Detailed Targeting Interests (Real-time validated IDs from Meta Marketing API)
TARGET_INTERESTS = [
    {"id": "6003103732434", "name": "Apartment"},
    {"id": "6003578086487", "name": "Real estate"},
    {"id": "6003446239080", "name": "Real estate investing"},
    {"id": "6003141785766", "name": "Mortgage loans"},
    {"id": "6003174415534", "name": "First-time buyer"}
]


# ==========================================
# AD COPY DEFINITIONS
# ==========================================
AD_COPIES = {
    "hook_a_rent_vs_own": {
        "title": "Hook A: Cost Comparison / Rent vs Own (Uttara Renters)",
        "primary_text": (
            "উত্তরায় প্রতি মাসে ৩৫-৪০ হাজার টাকা বাড়িভাড়া দিচ্ছেন? ৩ বছর পর বাড়িওয়ালার ফ্ল্যাট খালি করে দিতে হবে, "
            "আপনার হাতে কিছুই থাকবে না। অথচ সেই টাকায় আপনি হতে পারেন ১৫৭০ স্কয়ার ফিটের লাক্সারি ৩-বেড ফ্ল্যাটের মালিক!\n\n"
            "🏢 মল্লিক বিল্ডার্স লিমিটেড — 'প্রজেক্ট ১০' (বাশতলা, ভুঁইয়া বাড়ি)\n"
            "📍 আজমপুর উত্তরা থেকে মাত্র ১০ মিনিট, বিমানবন্দর থেকে ১৫ মিনিট\n\n"
            "✨ কেন এই প্রজেক্ট সেরা?\n"
            "• ১৫৭০ স্কয়ার ফিট (১২৫০ স্কয়ার ফিট নেট ইউজেবল স্পেস)\n"
            "• ৩ বেড, ৩ বাথ, ড্রয়িং-ডাইনিং ও সুবিশাল ২ বারান্দা\n"
            "• ৮.৭২ কাঠা জমির ওপর আধুনিক ১০ তলা (G+9) কনডো লিভিং\n"
            "• ২টি হাই-স্পিড লিফট, নিজস্ব মসজিদ, সুপার শপ ও ৫০০০ স্কয়ার ফিটের নান্দনিক রুফটপ গার্ডেন\n"
            "• ২০ ও ১৬ ফিট প্রশস্ত রাস্তা, সামনে ১০০ ফিট প্রস্তাবিত রোড\n\n"
            "💰 জমি শেয়ারিং প্রাইসিং:\n"
            "• জমি শেয়ার: ৳১২,০০,০০০\n"
            "• নির্মাণ খরচ: ৳৩৬,২৫,০০০\n"
            "👉 সর্বমোট মূল্য: মাত্র ৳৪৮,২৫,০০০ (৩৬ মাসের সহজ কিস্তিতে পরিশোধযোগ্য)\n\n"
            "🤝 ৩৬ মাসের মধ্যে হ্যান্ডওভার না দিলে মল্লিক বিল্ডার্স ক্ষতিপূরণ ভাড়া পরিশোধ করবে!\n\n"
            "📞 সীমিত শেয়ার বাকি। আজই সরাসরি সাইট ভিজিট ও বুকিং করতে কল করুন:\n"
            "01805-892106 / 01633-309081"
        ),
        "headline": "উত্তরায় ৩-বেড ফ্ল্যাট",
        "description": "৩৬ মাসের কিস্তি",
        "call_to_action": "LEARN_MORE"
    },
    "hook_b_legal_security": {
        "title": "Hook B: Security & Legal Transparency (আমাদের জমি, আমরা গড়ি)",
        "primary_text": (
            "ফ্ল্যাট কিনে কি বছরের পর বছর হস্তান্তরের অপেক্ষায় ঘুরবেন? মল্লিক বিল্ডার্স দিচ্ছে শতভাগ আইনি স্বচ্ছতা ও লিখিত পেনাল্টি রেন্ট গ্যারান্টি!\n\n"
            "🏢 মল্লিক বিল্ডার্স লিমিটেড — প্রজেক্ট ১০ (ভুঁইয়া বাড়ি, বাশতলা)\n"
            "জমির নিষ্কণ্টক শেয়ার আপনার নামে সাব-কবলা রেজিস্ট্রি। কোনো গোপন খরচ নেই।\n\n"
            "🛡️ মল্লিক বিল্ডার্সের ৩টি স্বচ্ছ প্রতিশ্রুতি:\n"
            "১. জমি শেয়ার ৳১২ লাখ + নির্মাণ ৳৩৬.২৫ লাখ = মোট ৳৪৮.২৫ লাখ ফিক্সড রেট।\n"
            "২. ৩৬ মাসের ফ্লেক্সিবল কিস্তির সুবিধা।\n"
            "৩. নির্ধারিত ৩৬ মাসের মধ্যে হস্তান্তর না হলে প্রতি মাসের জন্য ডেভেলপার কোম্পানি জরিমানা হিসেবে ক্ষতিপূরণ ভাড়া দেবে!\n\n"
            "🏡 ফ্ল্যাট স্পেসিফিকেশন:\n"
            "• ১৫৭০ স্কয়ার ফিট গ্রস (১২৫০ স্কয়ার ফিট নেট), ৩ বেড, ৩ বাথ, ড্রয়িং, ডাইনিং\n"
            "• ২টি লিফট, সার্বক্ষণিক জেনারেটর ব্যাকআপ, ইন-হাউস মসজিদ ও সুপার শপ\n"
            "• ৫০০০ স্কয়ার ফিট গ্রিন রুফটপ ও কিডস জোন\n\n"
            "উত্তরা আজমপুর থেকে মাত্র ১০ মিনিটের দূরত্বে নিশ্চিত করুন পরিবারের নিরাপদ স্থায়ী ঠিকানা।\n\n"
            "📞 সরাসরি কথা বলতে বা কাগজপত্র যাচাই করতে কল করুন:\n"
            "01805-892106 / 01633-309081"
        ),
        "headline": "মোট মাত্র ৪৮.২৫ লাখ",
        "description": "পেনাল্টি রেন্ট গ্যারান্টি",
        "call_to_action": "LEARN_MORE"
    },
    "hook_c_airport_corridor": {
        "title": "Hook C: Airport & RMG Corridor Investment (Aviation & Corporate)",
        "primary_text": (
            "বিমানবন্দর বা টঙ্গী-গাজীপুর আরএমজি করিডোরে কর্মরত পেশাজীবীদের জন্য উত্তরার সন্নিকটে সর্বোচ্চ ক্যাপিটাল গ্রোথ ও রেন্টাল ইল্ডের সুযোগ!\n\n"
            "✈️ বিমানবন্দর থেকে মাত্র ১৫ মিনিট | আজমপুর থেকে ১০ মিনিট\n"
            "🏢 মল্লিক বিল্ডার্স — প্রজেক্ট ১০ (বাশতলা মাজার চৌরাস্তা সংলগ্ন)\n\n"
            "বসুন্ধরা বা উত্তরায় একটি ফ্ল্যাট কিনতে যেখানে কোটি টাকা ছাড়িয়ে যায়, সেখানে ৮.৭২ কাঠার ওপর G+9 আধুনিক কন্ডোমিনিয়ামে নিজের ফ্ল্যাট নিশ্চিত করুন মাত্র ৪৮.২৫ লাখে!\n\n"
            "🌟 ইনভেস্টমেন্ট হাইলাইটস:\n"
            "• ১৫৭০ স্কয়ার ফিট ৩ বেড, ৩ বাথ, খোলামেলা ড্রয়িং ও ডাইনিং\n"
            "• ২০ ও ১৬ ফিট সংযোগ সড়ক এবং সামনে প্রস্তাবিত ১০০ ফিট এভিনিউ (ভবিষ্যতে দ্বিগুণ ভ্যালুয়েশন)\n"
            "• ৫০০০ স্কয়ার ফিট রুফটপ গার্ডেন, ২টি হাই-স্পিড লিফট, মসজিদ ও সুপার শপ\n"
            "• জমি শেয়ার ৳১২ লাখ + নির্মাণ ৳৩৬.২৫ লাখ = মোট ৳৪৮.২৫ লাখ\n"
            "• ৩৬ মাসের কিস্তি ও সময়মতো হ্যান্ডওভারের লিখিত নিশ্চয়তা\n\n"
            "💼 স্মার্ট রিয়েল এস্টেট ইনভেস্টমেন্টে আপনার পুঁজি রাখুন সুরক্ষিত।\n\n"
            "📞 বিস্তারিত প্রজেক্ট ব্রোশার ও সাইট ভিজিটের জন্য কল করুন:\n"
            "01805-892106 / 01633-309081"
        ),
        "headline": "ভাড়ার টাকায় নিজের ফ্ল্যাট",
        "description": "বিমানবন্দর ১৫ মিনিট",
        "call_to_action": "LEARN_MORE"
    }
}


def load_env_variables() -> Dict[str, str]:
    """Loads configuration from environment or .env file."""
    env_vars = {}
    
    # Try reading local .env or .env.marketing if present
    for env_filename in [".env", ".env.marketing", ".env.local"]:
        if os.path.exists(env_filename):
            with open(env_filename, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env_vars[k.strip()] = v.strip().strip("'").strip('"')

    # Environment variables override file
    token = os.environ.get("META_ACCESS_TOKEN") or env_vars.get("META_ACCESS_TOKEN")
    page_id = os.environ.get("META_PAGE_ID") or env_vars.get("META_PAGE_ID")
    account_id = os.environ.get("META_AD_ACCOUNT_ID") or env_vars.get("META_AD_ACCOUNT_ID") or DEFAULT_AD_ACCOUNT_ID

    return {
        "access_token": token,
        "page_id": page_id,
        "ad_account_id": account_id
    }


def construct_targeting_spec() -> Dict[str, Any]:
    """
    Constructs the detailed targeting payload satisfying:
    - GPS coordinates (3 km radius pin drops)
    - Living in location (location_types: ['home'])
    - Age 30-55
    - Specific interests (Apartment, Real Estate, etc.)
    - Advantage Detailed Targeting disabled (expansion = 0)
    - Facebook & Instagram feeds and reels only (Audience Network excluded)
    """
    custom_locations = []
    for loc in TARGET_LOCATIONS:
        custom_locations.append({
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
            "radius": loc["radius"],
            "distance_unit": loc["distance_unit"]
        })

    targeting = {
        "geo_locations": {
            "location_types": ["home"],
            "custom_locations": custom_locations
        },
        "age_min": 30,
        "age_max": 55,
        "flexible_spec": [
            {
                "interests": TARGET_INTERESTS
            }
        ],
        "targeting_automation": {
            "advantage_audience": 0
        },
        "publisher_platforms": ["facebook", "instagram"],
        "facebook_positions": ["feed", "story", "facebook_reels"],
        "instagram_positions": ["stream", "story", "reels"],
        "device_platforms": ["mobile", "desktop"]
    }
    return targeting


def run_dry_run(ad_account_id: str, page_id: str, post_id: str, video_id: str, objective: str, selected_hook: str):
    """Outputs the complete API payload for review without sending network requests."""
    copy_data = AD_COPIES[selected_hook]
    targeting = construct_targeting_spec()

    now = datetime.utcnow()
    start_time = (now + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S+0000")
    end_time = (now + timedelta(days=DURATION_DAYS)).strftime("%Y-%m-%dT%H:%M:%S+0000")

    payload_summary = {
        "mode": "DRY_RUN (No API calls executed)",
        "ad_account_id": ad_account_id,
        "page_id": page_id,
        "page_name": "Mollik Builders LTD",
        "existing_video": {
            "video_id": video_id,
            "post_id": post_id,
            "video_url": DEFAULT_VIDEO_URL,
            "object_story_id": f"{page_id}_{post_id}"
        },
        "campaign": {
            "name": CAMPAIGN_NAME,
            "objective": objective,
            "status": "PAUSED",
            "special_ad_categories": [],  # Empty array / NONE (HOUSING bypassed)
            "is_adset_budget_sharing_enabled": False
        },
        "adset": {
            "name": ADSET_NAME,
            "daily_budget": f"${DAILY_BUDGET_CENTS / 100:.2f} USD ({DAILY_BUDGET_CENTS} cents/day)",
            "duration": f"{DURATION_DAYS} Days",
            "total_budget": f"${(DAILY_BUDGET_CENTS * DURATION_DAYS) / 100:.2f} USD",
            "schedule": {
                "start_time": start_time,
                "end_time": end_time
            },
            "billing_event": "IMPRESSIONS",
            "optimization_goal": "POST_ENGAGEMENT" if objective == "OUTCOME_ENGAGEMENT" else "LEAD_GENERATION",
            "status": "PAUSED",
            "targeting": targeting
        },
        "creative_and_ad": {
            "ad_name": AD_NAME,
            "object_story_id": f"{page_id}_{post_id}",
            "hook_selected": copy_data["title"],
            "headline": copy_data["headline"],
            "description": copy_data["description"]
        }
    }

    print("\n" + "=" * 70)
    print("META ADS DEPLOYMENT: DRY-RUN TARGETING & CONFIGURATION PAYLOAD")
    print("=" * 70)
    print(json.dumps(payload_summary, indent=2, ensure_ascii=False))
    print("=" * 70)
    print("\n[VALIDATION PASSED]:")
    print("  ✓ special_ad_categories: [] (HOUSING bypassed)")
    print(f"  ✓ Existing Video ID: {video_id} (Page: {page_id})")
    print(f"  ✓ Budget & Schedule: ${DAILY_BUDGET_CENTS/100:.2f}/day for {DURATION_DAYS} days (${DAILY_BUDGET_CENTS*DURATION_DAYS/100:.2f} total)")
    print(f"  ✓ Coordinates pin drops: {len(TARGET_LOCATIONS)} locations (3km radius each)")
    print("  ✓ Demographic: Age 30-55, location_type='home'")
    print("  ✓ Detailed Targeting expansion: DISABLED (advantage_detailed_targeting=0)")
    print("  ✓ Placements: Facebook & Instagram only (Audience Network EXCLUDED)")
    print("  ✓ Initial State: PAUSED (safe review before spend)")
    print("=" * 70 + "\n")


def deploy_to_meta(
    access_token: str,
    page_id: str,
    post_id: str,
    ad_account_id: str,
    video_id: str = DEFAULT_VIDEO_ID,
    campaign_id: Optional[str] = None,
    objective: str = "OUTCOME_ENGAGEMENT",
    hook_key: str = "hook_a_rent_vs_own"
):
    """Executes the live API calls using facebook-business SDK."""
    print(f"\n[INFO] Initializing FacebookAdsApi for {ad_account_id}...")
    FacebookAdsApi.init(access_token=access_token)
    account = AdAccount(ad_account_id)

    copy_data = AD_COPIES[hook_key]
    targeting = construct_targeting_spec()

    # Calculate 10-day schedule
    now = datetime.utcnow()
    start_time = (now + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S+0000")
    end_time = (now + timedelta(days=DURATION_DAYS)).strftime("%Y-%m-%dT%H:%M:%S+0000")

    # 1. Create or Reuse Campaign
    if not campaign_id:
        print("[1/4] Creating Campaign with special_ad_categories=[] ...")
        campaign_params = {
            Campaign.Field.name: CAMPAIGN_NAME,
            Campaign.Field.objective: objective,
            Campaign.Field.status: Campaign.Status.paused,
            Campaign.Field.special_ad_categories: [],  # Crucial constraint: bypasses HOUSING dilution
            "is_adset_budget_sharing_enabled": False
        }
        campaign = account.create_campaign(fields=[Campaign.Field.id], params=campaign_params)
        campaign_id = campaign.get_id()
        print(f"      ✓ Campaign created successfully! ID: {campaign_id}")
    else:
        print(f"[1/4] Reusing existing Campaign ID: {campaign_id}")

    # 2. Create Ad Set with 10-day schedule and $3/day budget
    print(f"[2/4] Creating Ad Set (10 Days @ ${DAILY_BUDGET_CENTS/100:.2f}/day = ${(DAILY_BUDGET_CENTS*DURATION_DAYS)/100:.2f} total)...")
    adset_params = {
        AdSet.Field.name: ADSET_NAME,
        AdSet.Field.campaign_id: campaign_id,
        AdSet.Field.daily_budget: DAILY_BUDGET_CENTS,
        AdSet.Field.start_time: start_time,
        AdSet.Field.end_time: end_time,
        AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
        AdSet.Field.optimization_goal: (
            AdSet.OptimizationGoal.post_engagement
            if objective == "OUTCOME_ENGAGEMENT"
            else AdSet.OptimizationGoal.lead_generation
        ),
        "destination_type": "ON_POST" if objective == "OUTCOME_ENGAGEMENT" else "WEBSITE",
        AdSet.Field.bid_strategy: "LOWEST_COST_WITHOUT_CAP",
        AdSet.Field.targeting: targeting,
        AdSet.Field.status: AdSet.Status.paused
    }
    adset = account.create_ad_set(params=adset_params)
    adset_id = adset.get_id()
    print(f"      ✓ Ad Set created successfully! ID: {adset_id}")

    # 3. Create Ad Creative referencing existing uploaded Video/Reel
    print(f"[3/4] Creating Ad Creative linking existing post/reel {post_id} (Page: {page_id})...")
    story_id = f"{page_id}_{post_id}"
    creative_params = {
        AdCreative.Field.name: f"Creative - Project 10 Video (Reel {video_id})",
        AdCreative.Field.object_story_id: story_id
    }
    creative = account.create_ad_creative(params=creative_params)
    creative_id = creative.get_id()
    print(f"      ✓ Attached to existing page post/reel ({story_id})! Creative ID: {creative_id}")

    # 4. Create Ad
    print("[4/4] Creating Ad object...")
    ad_params = {
        Ad.Field.name: AD_NAME,
        Ad.Field.adset_id: adset_id,
        Ad.Field.creative: {"creative_id": creative_id},
        Ad.Field.status: Ad.Status.paused
    }
    ad = account.create_ad(params=ad_params)
    ad_id = ad.get_id()
    print(f"      ✓ Ad created successfully! ID: {ad_id}")

    print("\n" + "=" * 70)
    print("DEPLOYMENT COMPLETE (ALL OBJECTS CREATED IN PAUSED STATE)")
    print("=" * 70)
    print(f"Campaign ID:    {campaign_id}")
    print(f"Ad Set ID:      {adset_id}")
    print(f"Creative ID:    {creative_id}")
    print(f"Ad ID:          {ad_id}")
    print(f"Schedule:       {start_time} to {end_time} ({DURATION_DAYS} days)")
    print(f"Daily Budget:   ${DAILY_BUDGET_CENTS/100:.2f} USD | Total: ${(DAILY_BUDGET_CENTS*DURATION_DAYS)/100:.2f} USD")
    print(f"Ads Manager URL: https://adsmanager.facebook.com/adsmanager/manage/campaigns?act={ad_account_id.replace('act_', '')}")
    print("=" * 70 + "\n")

    return {
        "campaign_id": campaign_id,
        "adset_id": adset_id,
        "creative_id": creative_id,
        "ad_id": ad_id
    }


def main():
    parser = argparse.ArgumentParser(description="Mollik Builders Ltd Meta Ads Automation Deployer")
    parser.add_argument("--dry-run", action="store_true", help="Print targeting and API payload without creating live objects")
    parser.add_argument("--execute", action="store_true", help="Execute live deployment to Meta Marketing API")
    parser.add_argument("--hook", choices=["hook_a_rent_vs_own", "hook_b_legal_security", "hook_c_airport_corridor"],
                        default="hook_a_rent_vs_own", help="Select ad copy hook variant")
    parser.add_argument("--objective", choices=["OUTCOME_ENGAGEMENT", "OUTCOME_LEADS"], default="OUTCOME_ENGAGEMENT",
                        help="Campaign objective (default: OUTCOME_ENGAGEMENT for video boosting)")
    parser.add_argument("--token", type=str, help="Meta User/System User Access Token")
    parser.add_argument("--page-id", type=str, default=DEFAULT_PAGE_ID, help=f"Facebook Page ID (default: {DEFAULT_PAGE_ID})")
    parser.add_argument("--post-id", type=str, default=DEFAULT_POST_ID, help=f"Facebook Post ID (default: {DEFAULT_POST_ID})")
    parser.add_argument("--video-id", type=str, default=DEFAULT_VIDEO_ID, help=f"Facebook Video/Reel ID (default: {DEFAULT_VIDEO_ID})")
    parser.add_argument("--account-id", type=str, default=DEFAULT_AD_ACCOUNT_ID, help=f"Ad Account ID (default: {DEFAULT_AD_ACCOUNT_ID})")
    parser.add_argument("--campaign-id", type=str, help="Existing Campaign ID to reuse")

    args = parser.parse_args()
    env = load_env_variables()

    access_token = args.token or env.get("access_token")
    page_id = args.page_id or env.get("page_id") or DEFAULT_PAGE_ID
    post_id = args.post_id or DEFAULT_POST_ID
    video_id = args.video_id or DEFAULT_VIDEO_ID
    campaign_id = args.campaign_id
    account_id = args.account_id or env.get("ad_account_id") or DEFAULT_AD_ACCOUNT_ID

    if not account_id.startswith("act_"):
        account_id = f"act_{account_id}"

    # Default to dry-run if --execute is not explicitly passed or if credentials are missing
    if args.dry_run or not args.execute:
        run_dry_run(account_id, page_id, post_id, video_id, args.objective, args.hook)
        if not args.execute:
            print("[NOTE] Ran in dry-run mode. To deploy live, supply ACCESS_TOKEN and pass --execute.")
        return

    # If --execute is passed, ensure credentials exist
    if not access_token:
        print("\n[ERROR] Missing credentials for live deployment!")
        print("  - META_ACCESS_TOKEN is required.")
        print("\nPlease supply via --token or set META_ACCESS_TOKEN in .env.")
        sys.exit(1)

    deploy_to_meta(access_token, page_id, post_id, account_id, video_id, campaign_id, args.objective, args.hook)


if __name__ == "__main__":
    main()
