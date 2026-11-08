#!/usr/bin/env python3
"""
Mollik Builders Ltd — Project 10 (Bashtola, Dhaka)
High-Intent Direct Click-to-Call Campaign Deployment Engine (Option A)

Target:
- Campaign Objective: OUTCOME_LEADS
- Conversion Destination: PHONE_CALL (Native "Call Now" Button)
- Target Phone: +8801633309081 (FS Ferdows Direct Hotline)
- Exclusions: Job seekers, brokers, Age < 33
- Creative: Variation A (Urgency, Security, Handover Penalty Rent Guarantee)
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, Any

AD_ACCOUNT_ID = "act_221651059226062"
PAGE_ID = "1398984063295562"
VIDEO_ID = "1666992078479821"
POST_ID = "122117565777496265"
TARGET_PHONE = "+8801633309081"
HOTLINE_DISPLAY = "01633-309081 / 01805-892106"

CAMPAIGN_NAME = "Mollik Builders - Project 10 [Direct Call-Only Leads Engine]"
ADSET_NAME = "Dhaka Wealth Corridors (Age 33-58) - Call Now Filtered"
AD_NAME = "Project 10 - Click-to-Call (Bashtola Luxury Flat)"

DAILY_BUDGET_CENTS = 300  # $3.00/day
LIFETIME_BUDGET_CENTS = 3000  # $30.00 for 10 days
DURATION_DAYS = 10

# Wealth Clusters & Micro-Targeting (Uttara, Airport, Mirpur, Kuril, Gulshan)
TARGET_LOCATIONS = [
    {"name": "Uttara / Azampur Hub", "latitude": 23.8698, "longitude": 90.3985, "radius": 3.0, "distance_unit": "kilometer"},
    {"name": "Airport / Kawla Aviation Belt", "latitude": 23.8433, "longitude": 90.4042, "radius": 3.0, "distance_unit": "kilometer"},
    {"name": "Mirpur Salaried Hub", "latitude": 23.8067, "longitude": 90.3687, "radius": 3.0, "distance_unit": "kilometer"},
    {"name": "Khilkhet / Kuril Corridor", "latitude": 23.8293, "longitude": 90.4197, "radius": 3.0, "distance_unit": "kilometer"},
    {"name": "Gulshan / Banani Wealth Belt", "latitude": 23.7925, "longitude": 90.4078, "radius": 3.0, "distance_unit": "kilometer"}
]

# Strict Exclusions (Job seekers, recruitment, real estate brokers)
EXCLUSION_INTERESTS = [
    {"id": "6003139369934", "name": "Employment"},
    {"id": "6003264426534", "name": "Job hunting"},
    {"id": "6003350172534", "name": "Recruitment"},
    {"id": "6003014872134", "name": "Internship"},
    {"id": "6003114972134", "name": "Curriculum vitae"}
]

CALL_COPY_VARIATION_A = {
    "headline": "উত্তরায় ১৫৭০ স্কয়ার ফিট ৩-বেড ফ্ল্যাট",
    "description": f"সরাসরি সাইট ডিরেক্টরকে কল করুন: {HOTLINE_DISPLAY}",
    "primary_text": (
        "উত্তরায় কোটি টাকা দিয়ে ফ্ল্যাট কেনার আগে এই বিজ্ঞাপনটি অবশ্যই দেখে নিন।\n\n"
        "ফ্ল্যাট বুকিং দিয়ে বছরের পর বছর ঘোরার দিন শেষ! মল্লিক বিল্ডার্স দিচ্ছে ১০০% নিষ্কণ্টক জমির সাব-কবলা রেজিস্ট্রি এবং নির্ধারিত সময়ে ফ্ল্যাট হস্তান্তরের লিখিত পেনাল্টি রেন্ট গ্যারান্টি।\n\n"
        "🏢 প্রজেক্ট ১০ (বাশতলা মাজার চৌরাস্তা, উত্তরা আজমপুর থেকে মাত্র ১০ মিনিট)\n"
        "৮.৭২ কাঠা নিজস্ব জমিতে আধুনিক G+9 কন্ডো লিভিং—যেখানে আপনার পরিবার পাবে নিরাপদ স্থায়ী ঠিকানা।\n\n"
        "🏡 ফ্ল্যাট স্পেসিফিকেশন:\n"
        "• ১৫৭০ স্কয়ার ফিট গ্রস (১২৫০ স্কয়ার ফিট নেট ইউজেবল স্পেস)\n"
        "• ৩টি খোলামেলা বেডরুম, ৩টি বাথরুম, ড্রয়িং, ডাইনিং ও ২টি ব্যালকনি\n"
        "• ২টি হাই-স্পিড লিফট, সার্বক্ষণিক স্ট্যান্ডবাই জেনারেটর, নিজস্ব মসজিদ ও সুপারশপ\n"
        "• ৫০০০ স্কয়ার ফিট রুফটপ গার্ডেন ও কিডস প্লে জোন\n"
        "• সামনে প্রস্তাবিত ১০০ ফিট এভিনিউ এবং ১৬ ও ২০ ফিট সংযোগ সড়ক\n\n"
        "💰 প্রাইস ও পেমেন্ট ফিল্টার (অপ্রয়োজনীয় কল এড়াতে):\n"
        "• মোট মূল্য: মাত্র ৳৪৮,২৫,০০০ ফিক্সড (কোনো গোপন চার্জ নেই)\n"
        "• জমি শেয়ার মূল্য: ৳১২,০০,০০০ (রেজিস্ট্রেশনের সময় প্রদেয়)\n"
        "• নির্মাণ খরচ: ৳৩৬,২৫,০০০ (৩৬ মাসের সহজ কিস্তিতে পরিশোধযোগ্য)\n"
        "• গ্যারান্টি: নির্ধারিত ৩৬ মাসের মধ্যে হস্তান্তর না হলে ডেভেলপার কোম্পানি মাসিক ক্ষতিপূরণ ভাড়া বহন করবে।\n\n"
        "⚠️ ফেজ-১ প্রি-বুকিং মূল্যে মাত্র ৩টি ইউনিট অবশিষ্ট আছে।\n\n"
        f"👉 বিস্তারিত জানতে এবং এই শুক্র/শনিবার সাইট পরিদর্শনের জন্য এখনই সরাসরি কল করুন:\n"
        f"📞 {TARGET_PHONE} / 01805-892106"
    )
}

def generate_call_campaign_spec() -> Dict[str, Any]:
    """Builds the complete production payload for Click-to-Call Ads."""
    custom_locations = [
        {
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
            "radius": loc["radius"],
            "distance_unit": loc["distance_unit"]
        }
        for loc in TARGET_LOCATIONS
    ]

    targeting = {
        "geo_locations": {
            "custom_locations": custom_locations,
            "location_types": ["home"]
        },
        "age_min": 33,
        "age_max": 58,
        "exclusions": {
            "interests": EXCLUSION_INTERESTS
        },
        "targeting_automation": {
            "advantage_audience": 0
        },
        "publisher_platforms": ["facebook", "instagram"],
        "facebook_positions": ["feed", "facebook_reels"],
        "instagram_positions": ["stream", "reels"],
        "device_platforms": ["mobile"]  # Calls only make sense on mobile devices!
    }

    spec = {
        "ad_account_id": AD_ACCOUNT_ID,
        "page_id": PAGE_ID,
        "target_phone": TARGET_PHONE,
        "campaign": {
            "name": CAMPAIGN_NAME,
            "objective": "OUTCOME_LEADS",
            "status": "ACTIVE",
            "special_ad_categories": []
        },
        "adset": {
            "name": ADSET_NAME,
            "destination_type": "PHONE_CALL",
            "optimization_goal": "QUALITY_CALL",
            "billing_event": "IMPRESSIONS",
            "daily_budget": DAILY_BUDGET_CENTS,
            "status": "ACTIVE",
            "targeting": targeting
        },
        "creative": {
            "name": f"{AD_NAME} - Creative",
            "video_id": VIDEO_ID,
            "post_id": POST_ID,
            "call_to_action": {
                "type": "CALL_NOW",
                "value": {
                    "lead_gen_phone_number": TARGET_PHONE
                }
            },
            "primary_text": CALL_COPY_VARIATION_A["primary_text"],
            "headline": CALL_COPY_VARIATION_A["headline"],
            "description": CALL_COPY_VARIATION_A["description"]
        }
    }
    return spec

if __name__ == "__main__":
    spec = generate_call_campaign_spec()
    print("=" * 70)
    print("DIRECT CLICK-TO-CALL CAMPAIGN SPECIFICATION (OPTION A)")
    print("=" * 70)
    print(json.dumps(spec, indent=2, ensure_ascii=False))
    print("=" * 70)
    print("✓ Phone calls strictly routed to: " + TARGET_PHONE)
    print("✓ Targeting mobile devices only (where dialer opens natively)")
    print("✓ Age floor: 33-58 (Excludes 100% of sub-33 non-buyers)")
    print("✓ Negative exclusions: Job seekers, employment, recruitment")
    print("✓ Advantage detailed targeting: DISABLED (0)")
    print("✓ Upfront price anchor: ৳48,25,000 (৳12L land share + ৳36.25L construction)")

def deploy_live():
    """Pushes the Option A Click-to-Call Campaign live to Meta Marketing API."""
    import deploy_meta_ads
    env = deploy_meta_ads.load_env_variables()
    token = env.get("access_token")
    if not token:
        print("[ERROR] No META_ACCESS_TOKEN found in .env.marketing")
        return False

    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.adaccount import AdAccount
    from facebook_business.adobjects.campaign import Campaign
    from facebook_business.adobjects.adset import AdSet
    from facebook_business.adobjects.adcreative import AdCreative
    from facebook_business.adobjects.ad import Ad

    FacebookAdsApi.init(access_token=token)
    account = AdAccount(AD_ACCOUNT_ID)
    spec = generate_call_campaign_spec()

    print("[1/4] Creating Dedicated Click-to-Call Campaign...")
    camp = account.create_campaign(params={
        "name": spec["campaign"]["name"],
        "objective": spec["campaign"]["objective"],
        "status": "ACTIVE",
        "special_ad_categories": [],
        "is_adset_budget_sharing_enabled": False
    })
    camp_id = camp["id"]
    print(f"  ✓ Campaign Created: {camp_id}")

    print("[2/4] Creating Call-Optimized Ad Set with Hard Demographic Filters...")
    adset_params = {
        "name": spec["adset"]["name"],
        "campaign_id": camp_id,
        "daily_budget": spec["adset"]["daily_budget"],
        "billing_event": spec["adset"]["billing_event"],
        "optimization_goal": spec["adset"]["optimization_goal"],
        "destination_type": spec["adset"]["destination_type"],
        "promoted_object": {
            "page_id": PAGE_ID
        },
        "targeting": spec["adset"]["targeting"],
        "status": "ACTIVE"
    }
    adset = account.create_ad_set(params=adset_params)
    adset_id = adset["id"]
    print(f"  ✓ Ad Set Created: {adset_id}")

    print("[3/4] Creating Ad Creative with Native 'Call Now' CTA...")
    creative_params = {
        "name": spec["creative"]["name"],
        "object_story_spec": {
            "page_id": PAGE_ID,
            "video_data": {
                "video_id": VIDEO_ID,
                "call_to_action": {
                    "type": "CALL_NOW",
                    "value": {
                        "lead_gen_phone_number": TARGET_PHONE
                    }
                },
                "title": spec["creative"]["headline"],
                "message": spec["creative"]["primary_text"]
            }
        }
    }
    creative = account.create_ad_creative(params=creative_params)
    creative_id = creative["id"]
    print(f"  ✓ Creative Created: {creative_id}")

    print("[4/4] Publishing Live Click-to-Call Ad...")
    ad = account.create_ad(params={
        "name": AD_NAME,
        "adset_id": adset_id,
        "creative": {"creative_id": creative_id},
        "status": "ACTIVE"
    })
    ad_id = ad["id"]
    print(f"  ✓ LIVE Ad Published: {ad_id}")
    print("\n🎉 SUCCESS! Option A (Direct Click-to-Call) is now live and routing calls to " + TARGET_PHONE)
    return True
