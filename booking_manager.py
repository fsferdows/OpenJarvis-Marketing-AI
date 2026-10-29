#!/usr/bin/env python3
"""
Mollik Builders Ltd — Project 10
Executive Project Booking Manager & Sales Dashboard

Manages:
- Professional CSV Bookings & Inquiries (data/project_bookings.csv)
- Site visit schedules
- Automated WhatsApp Dispatches to Owner (+8801633309081)
- Formatted Markdown & Excel reporting
"""

import os
import sys
import csv
from datetime import datetime
from typing import List, Dict, Any
import whatsapp_dispatcher

BOOKINGS_CSV = "data/project_bookings.csv"
REPORT_MD = "data/PROJECT_BOOKINGS_REPORT.md"


def load_bookings() -> List[Dict[str, str]]:
    """Loads all bookings from CSV."""
    if not os.path.exists(BOOKINGS_CSV):
        return []
    bookings = []
    with open(BOOKINGS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            bookings.append(row)
    return bookings


def display_bookings(bookings: List[Dict[str, str]], title: str = "EXECUTIVE PROJECT BOOKINGS"):
    """Displays a clean, professional executive table."""
    if not bookings:
        print("\n[INFO] No bookings recorded yet in data/project_bookings.csv.")
        return

    print("\n" + "=" * 110)
    print(f"MOLLIK BUILDERS LTD — {title} ({len(bookings)} Total Records)")
    print("Owner WhatsApp: +8801633309081 | Project: Project 10 (Bashtola, Uttara 10-Min Belt)")
    print("=" * 110)
    print(f"{'ID':<11} | {'Date & Time':<17} | {'Client Name':<20} | {'Phone':<13} | {'Visit Date':<22} | {'Status'}")
    print("-" * 110)

    for b in bookings:
        b_id = b.get("Booking_ID", "")
        ts = b.get("Timestamp", "")[:16]
        name = b.get("Customer_Name", "")[:20]
        phone = b.get("Customer_Phone", "")
        v_date = b.get("Preferred_Visit_Date", "")[:22]
        status = b.get("Booking_Status", "Scheduled")
        print(f"{b_id:<11} | {ts:<17} | {name:<20} | {phone:<13} | {v_date:<22} | {status}")

    print("=" * 110 + "\n")


def export_executive_report():
    """Generates a high-level executive report in Markdown."""
    bookings = load_bookings()
    os.makedirs("data", exist_ok=True)

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("# Mollik Builders Ltd — Project 10: Executive Bookings Report\n\n")
        f.write(f"> **Report Generated:** {datetime.now().strftime('%Y-%m-%d %I:%M %p')}\n")
        f.write(f"> **Owner WhatsApp Notification Target:** `+8801633309081`\n")
        f.write(f"> **Total Registered Bookings & Leads:** `{len(bookings)}`\n\n")
        f.write("---\n\n")
        f.write("### 📋 Client Visit Appointments & Inquiry Log\n\n")
        f.write("| Booking ID | Client Name | Phone Number | WhatsApp Link | Scheduled Visit Date | Budget / Package | Status |\n")
        f.write("|---|---|---|---|---|---|---|\n")

        for b in bookings:
            wa_link = f"[Chat on WhatsApp]({b.get('WhatsApp_Direct_Link')})" if b.get('WhatsApp_Direct_Link') else "N/A"
            f.write(
                f"| `{b.get('Booking_ID')}` | **{b.get('Customer_Name')}** | "
                f"`{b.get('Customer_Phone')}` | {wa_link} | "
                f"**{b.get('Preferred_Visit_Date')}** | {b.get('Budget_Confirmed')} | "
                f"`{b.get('Booking_Status')}` |\n"
            )

        f.write("\n---\n\n")
        f.write("### 🏢 Project 10 Highlights\n")
        f.write("- **Location:** Bhuiyan Bari, Bashtola (10 mins from Azampur Uttara, 15 mins from HSIA Airport)\n")
        f.write("- **Flat Size:** 1570 sqft Gross (1250 sqft net usable), 3 Bed, 3 Bath, Drawing, Dining, 2 Balconies\n")
        f.write("- **Pricing:** Land Share ৳12,00,000 + Construction ৳36,25,000 = Total ৳48,25,000\n")
        f.write("- **Handover Guarantee:** 36-Month installment with penalty rent compensation\n")

    print(f"\n[✓ Executive Report generated: {REPORT_MD}]")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Mollik Builders Executive Booking Manager")
    parser.add_argument("--list", action="store_true", help="List all site visit bookings")
    parser.add_argument("--export", action="store_true", help="Export executive Markdown report")
    parser.add_argument("--hot", action="store_true", help="Filter hot leads with visit booked")
    parser.add_argument("--test-alert", action="store_true", help="Send a test notification to owner WhatsApp (+8801633309081)")

    args = parser.parse_args()
    bookings = load_bookings()

    if args.test_alert:
        test_payload = {
            "name": "Barrister Faisal Ahmed",
            "phone": "01819283746",
            "visit_date": "Saturday (12:00 PM)",
            "visit_time": "12:00 PM",
            "interest_level": "🔥 Hot Lead (Test Alert)",
            "summary": "Customer confirmed interest in 1570 sqft 3-bed flat. Testing automated WhatsApp dispatch to +8801633309081."
        }
        whatsapp_dispatcher.send_whatsapp_alert(test_payload)
    elif args.hot:
        hot = [b for b in bookings if "Hot" in b.get("Interest_Level", "") or "Visit" in b.get("Booking_Status", "")]
        display_bookings(hot, title="HOT SITE VISIT BOOKINGS")
    elif args.export:
        export_executive_report()
    else:
        display_bookings(bookings)


if __name__ == "__main__":
    main()

