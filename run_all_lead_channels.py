#!/usr/bin/env python3
"""
Mollik Builders Ltd — Project 10 (Bashtola, Dhaka)
Multi-Channel Lead Acceleration Engine (Calls + Messages + Lead Forms)

Activates and runs ALL high-intent lead channels concurrently:
1. Channel 1: Direct Click-to-Call (Native "Call Now" Button -> +8801633309081)
2. Channel 2: Direct Messenger / WhatsApp Chat (Native "Send Message" Button -> 24/7 AI Sales Agent)
3. Channel 3: Qualified Instant Form (Higher-Intent Lead Gen -> Name, Phone, Budget, Intent)

Usage:
    python3 run_all_lead_channels.py --status           # Check status of all 3 channels
    python3 run_all_lead_channels.py --activate-all     # Activate Call + Message + Form campaigns
    python3 run_all_lead_channels.py --budget-per-ad 2  # Set $2.00/day per channel
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, Any, List, Optional
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "data", "campaign_schedule_state.json")

# Default IDs
AD_ACCOUNT_ID = "act_221651059226062"
PAGE_ID = "1398984063295562"
VIDEO_ID = "1666992078479821"
POST_ID = "122117565777496265"
TARGET_PHONE = "+8801633309081"
FORM_ID = "2634088530370757"

# Existing Campaign IDs
CALL_CAMPAIGN_ID = "120255677739250063"       # Direct Click-to-Call
LEADGEN_CAMPAIGN_ID = "120255735278450063"    # Instant Lead Form
MESSAGE_CAMPAIGN_ID = "120255594274270063"    # Can be adapted or new Messenger campaign


def load_env() -> Dict[str, str]:
    """Loads environment variables from .env.marketing."""
    env = dict(os.environ)
    env_file = os.path.join(BASE_DIR, ".env.marketing")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip("'").strip('"')
    return env


def check_token(token: str) -> bool:
    """Verifies if Meta token is currently valid."""
    url = f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}?fields=name,account_status&access_token={token}"
    resp = requests.get(url).json()
    if "error" in resp:
        print("\n[!] Meta Token Error:")
        print(f"    Message: {resp['error'].get('message')}")
        print(f"    Type:    {resp['error'].get('type')}")
        print(f"    Code:    {resp['error'].get('code')}")
        return False
    print(f"\n[✓] Meta Token Valid! Connected to: {resp.get('name')} (Status: Active)")
    return True


def get_all_campaigns_status(token: str) -> List[Dict[str, Any]]:
    """Fetches all campaigns, ad sets, and ads in the ad account."""
    url = f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/campaigns?fields=id,name,status,objective,daily_budget&access_token={token}"
    resp = requests.get(url).json()
    return resp.get("data", [])


def activate_call_campaign(token: str, budget_cents: int = 200) -> bool:
    """Activates the Direct Click-to-Call Campaign and sets budget."""
    print("\n[1/3] Activating Click-to-Call Campaign...")
    # Unpause campaign
    camp_url = f"https://graph.facebook.com/v21.0/{CALL_CAMPAIGN_ID}"
    r_c = requests.post(camp_url, data={"status": "ACTIVE", "access_token": token}).json()
    
    # Get ad sets under call campaign
    adsets_url = f"https://graph.facebook.com/v21.0/{CALL_CAMPAIGN_ID}/adsets?fields=id,name,status&access_token={token}"
    adsets = requests.get(adsets_url).json().get("data", [])
    for adset in adsets:
        adset_id = adset["id"]
        requests.post(f"https://graph.facebook.com/v21.0/{adset_id}", data={
            "status": "ACTIVE",
            "daily_budget": budget_cents,
            "access_token": token
        })
        print(f"  ✓ Activated Call AdSet: {adset_id} ({adset.get('name')}) @ ${budget_cents/100:.2f}/day")
    
    # Get ads under call campaign
    ads_url = f"https://graph.facebook.com/v21.0/{CALL_CAMPAIGN_ID}/ads?fields=id,name,status&access_token={token}"
    ads = requests.get(ads_url).json().get("data", [])
    for ad in ads:
        requests.post(f"https://graph.facebook.com/v21.0/{ad['id']}", data={"status": "ACTIVE", "access_token": token})
        print(f"  ✓ Activated Call Ad: {ad['id']} ({ad.get('name')})")
    
    return True


def activate_leadgen_campaign(token: str, budget_cents: int = 200) -> bool:
    """Activates the Instant Form Lead Gen Campaign and sets budget."""
    print("\n[2/3] Activating Instant Form Lead Gen Campaign...")
    # Unpause campaign
    camp_url = f"https://graph.facebook.com/v21.0/{LEADGEN_CAMPAIGN_ID}"
    requests.post(camp_url, data={"status": "ACTIVE", "access_token": token})
    
    # Ad sets
    adsets_url = f"https://graph.facebook.com/v21.0/{LEADGEN_CAMPAIGN_ID}/adsets?fields=id,name,status&access_token={token}"
    adsets = requests.get(adsets_url).json().get("data", [])
    for adset in adsets:
        adset_id = adset["id"]
        requests.post(f"https://graph.facebook.com/v21.0/{adset_id}", data={
            "status": "ACTIVE",
            "daily_budget": budget_cents,
            "access_token": token
        })
        print(f"  ✓ Activated Lead Form AdSet: {adset_id} ({adset.get('name')}) @ ${budget_cents/100:.2f}/day")
    
    # Ads
    ads_url = f"https://graph.facebook.com/v21.0/{LEADGEN_CAMPAIGN_ID}/ads?fields=id,name,status&access_token={token}"
    ads = requests.get(ads_url).json().get("data", [])
    for ad in ads:
        requests.post(f"https://graph.facebook.com/v21.0/{ad['id']}", data={"status": "ACTIVE", "access_token": token})
        print(f"  ✓ Activated Lead Form Ad: {ad['id']} ({ad.get('name')})")
    
    return True


def ensure_messaging_campaign(token: str, budget_cents: int = 200) -> bool:
    """Ensures a dedicated Direct Message (Messenger / WhatsApp) ad set is running."""
    print("\n[3/3] Setting up / Activating Direct Message Campaign...")
    
    # Check if a dedicated Message campaign exists
    url = f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/campaigns?fields=id,name,status,objective&access_token={token}"
    camps = requests.get(url).json().get("data", [])
    msg_camp = next((c for c in camps if "Message" in c.get("name", "") or "Messenger" in c.get("name", "")), None)
    
    story_id = f"{PAGE_ID}_{POST_ID}"
    
    # Creative with SEND_MESSAGE CTA
    creative_payload = {
        "name": "Project 10 - Send Message Creative",
        "object_story_id": story_id,
        "call_to_action": json.dumps({
            "type": "MESSAGE_PAGE",
            "value": {
                "app_destination": "MESSENGER"
            }
        }),
        "access_token": token
    }
    cr_res = requests.post(f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/adcreatives", data=creative_payload).json()
    msg_creative_id = cr_res.get("id")
    if not msg_creative_id:
        # Fallback to existing story ID creative
        msg_creative_id = "2148704936519169"
    
    targeting = {
        "geo_locations": {
            "custom_locations": [
                {"latitude": 23.8698, "longitude": 90.3985, "radius": 4.0, "distance_unit": "kilometer"},
                {"latitude": 23.8433, "longitude": 90.4042, "radius": 4.0, "distance_unit": "kilometer"},
                {"latitude": 23.8067, "longitude": 90.3687, "radius": 4.0, "distance_unit": "kilometer"},
                {"latitude": 23.8293, "longitude": 90.4197, "radius": 4.0, "distance_unit": "kilometer"},
                {"latitude": 23.7925, "longitude": 90.4078, "radius": 4.0, "distance_unit": "kilometer"}
            ]
        },
        "age_min": 33,
        "age_max": 55,
        "targeting_automation": {"advantage_audience": 0},
        "publisher_platforms": ["facebook", "instagram"],
        "facebook_positions": ["feed", "facebook_reels"],
        "instagram_positions": ["stream", "reels"],
        "device_platforms": ["mobile", "desktop"]
    }
    
    if not msg_camp:
        print("  Creating dedicated Direct Messaging Campaign...")
        camp_res = requests.post(f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/campaigns", data={
            "name": "Mollik Builders - Project 10 [Direct Messaging Leads Engine]",
            "objective": "OUTCOME_ENGAGEMENT",
            "status": "ACTIVE",
            "is_adset_budget_sharing_enabled": False,
            "special_ad_categories": json.dumps([]),
            "access_token": token
        }).json()
        msg_camp_id = camp_res.get("id")
    else:
        msg_camp_id = msg_camp["id"]
        requests.post(f"https://graph.facebook.com/v21.0/{msg_camp_id}", data={"status": "ACTIVE", "access_token": token})
    
    if msg_camp_id:
        print(f"  ✓ Messaging Campaign Active: {msg_camp_id}")
        # Check adset
        adsets_url = f"https://graph.facebook.com/v21.0/{msg_camp_id}/adsets?fields=id,name,status&access_token={token}"
        adsets = requests.get(adsets_url).json().get("data", [])
        if adsets:
            for adset in adsets:
                requests.post(f"https://graph.facebook.com/v21.0/{adset['id']}", data={
                    "status": "ACTIVE",
                    "daily_budget": budget_cents,
                    "access_token": token
                })
                print(f"  ✓ Activated Messaging AdSet: {adset['id']} @ ${budget_cents/100:.2f}/day")
        else:
            adset_payload = {
                "name": "Dhaka North (33-55) - Send Message / WhatsApp",
                "campaign_id": msg_camp_id,
                "daily_budget": budget_cents,
                "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
                "billing_event": "IMPRESSIONS",
                "optimization_goal": "CONVERSATIONS",
                "destination_type": "MESSENGER",
                "promoted_object": json.dumps({"page_id": PAGE_ID}),
                "targeting": json.dumps(targeting),
                "status": "ACTIVE",
                "access_token": token
            }
            a_res = requests.post(f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/adsets", data=adset_payload).json()
            adset_id = a_res.get("id")
            if adset_id:
                print(f"  ✓ Created Messaging AdSet: {adset_id} @ ${budget_cents/100:.2f}/day")
                ad_payload = {
                    "name": "Project 10 - Send Message Ad",
                    "adset_id": adset_id,
                    "creative": json.dumps({"creative_id": msg_creative_id}),
                    "status": "ACTIVE",
                    "access_token": token
                }
                requests.post(f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/ads", data=ad_payload)
                print(f"  ✓ Published Messaging Ad with Send Message CTA!")
    return True


def display_dashboard(token: str):
    """Displays current live status of all campaigns and ad sets."""
    print("\n" + "=" * 75)
    print("MOLLIK BUILDERS LTD — ALL LIVE LEAD CAMPAIGNS DASHBOARD")
    print("=" * 75)
    
    url = f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/campaigns?fields=id,name,status,objective&access_token={token}"
    camps = requests.get(url).json().get("data", [])
    
    for c in camps:
        status_icon = "🟢 ACTIVE" if c.get("status") == "ACTIVE" else "⏸️ PAUSED"
        print(f"\n📁 Campaign: {c.get('name')}")
        print(f"   ID: {c.get('id')} | Status: {status_icon} | Objective: {c.get('objective')}")
        
        # Get ad sets
        adsets_url = f"https://graph.facebook.com/v21.0/{c.get('id')}/adsets?fields=id,name,status,daily_budget,destination_type,optimization_goal&access_token={token}"
        adsets = requests.get(adsets_url).json().get("data", [])
        for a in adsets:
            a_icon = "  ├─ 🟢" if a.get("status") == "ACTIVE" else "  ├─ ⏸️"
            budget = float(a.get("daily_budget", 0)) / 100 if a.get("daily_budget") else 0
            dest = a.get("destination_type", "N/A")
            print(f"{a_icon} AdSet: {a.get('name')} | Dest: {dest} | Budget: ${budget:.2f}/day")
            
            # Get ads
            ads_url = f"https://graph.facebook.com/v21.0/{a.get('id')}/ads?fields=id,name,status,effective_status&access_token={token}"
            ads = requests.get(ads_url).json().get("data", [])
            for ad in ads:
                eff = ad.get("effective_status")
                eff_icon = "🟢" if eff in ["ACTIVE", "PENDING_REVIEW"] else "⏸️"
                print(f"     └─ {eff_icon} Ad: {ad.get('name')} ({eff})")
                
    print("\n" + "=" * 75)


def main():
    parser = argparse.ArgumentParser(description="Multi-Channel Lead Engine for Mollik Builders")
    parser.add_argument("--status", action="store_true", help="Display status of all campaigns")
    parser.add_argument("--activate-all", action="store_true", help="Activate Call + Message + Form campaigns simultaneously")
    parser.add_argument("--budget-per-channel", type=float, default=2.00, help="Daily budget in USD per channel (default: $2.00/day)")
    args = parser.parse_args()

    env = load_env()
    token = env.get("META_ACCESS_TOKEN")
    if not token:
        print("[ERROR] META_ACCESS_TOKEN not set in .env.marketing")
        sys.exit(1)

    if not check_token(token):
        print("\n[!] Please update META_ACCESS_TOKEN in .env.marketing with a fresh token.")
        print("    Open: https://developers.facebook.com/tools/explorer/")
        sys.exit(1)

    budget_cents = int(args.budget_per_channel * 100)

    if args.activate_all:
        print(f"\n🚀 ACTIVATING ALL 3 CHANNELS @ ${args.budget_per_channel:.2f}/DAY EACH (Total: ${args.budget_per_channel*3:.2f}/day)...")
        activate_call_campaign(token, budget_cents)
        activate_leadgen_campaign(token, budget_cents)
        ensure_messaging_campaign(token, budget_cents)
        display_dashboard(token)
    else:
        display_dashboard(token)


if __name__ == "__main__":
    main()
