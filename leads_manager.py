#!/usr/bin/env python3
"""
Mollik Builders Ltd - Project 10
Leads Manager & Sales Dashboard

Features:
- Real-time lead tracking from video comments and messenger bot
- Clean terminal summary table with hot leads highlighted
- Search leads by phone number or name
- Add manual walk-in / phone call leads
- Export leads to Markdown report or Excel-ready CSV
"""

import os
import sys
import csv
from datetime import datetime
from typing import List, Dict, Any

LEADS_FILE = "data/leads.csv"


def load_leads() -> List[Dict[str, str]]:
    """Loads all captured leads from CSV."""
    if not os.path.exists(LEADS_FILE):
        return []
    leads = []
    with open(LEADS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    return leads


def display_leads(leads: List[Dict[str, str]]):
    """Prints a clean, formatted table of leads."""
    if not leads:
        print("\n[INFO] No leads recorded yet in data/leads.csv.")
        return

    print("\n" + "=" * 90)
    print(f"MOLLIK BUILDERS LTD — 'PROJECT 10' REAL-TIME LEADS TRACKER ({len(leads)} Total)")
    print("=" * 90)
    print(f"{'#':<3} | {'Timestamp':<19} | {'Source':<14} | {'Name':<18} | {'Phone':<13} | {'Status'}")
    print("-" * 90)

    for i, lead in enumerate(leads, 1):
        ts = lead.get("Timestamp", "")[:19]
        source = lead.get("Source", "")[:14]
        name = lead.get("Customer_Name", "")[:18]
        phone = lead.get("Phone", "")
        status = lead.get("Status", "New")
        print(f"{i:<3} | {ts:<19} | {source:<14} | {name:<18} | {phone:<13} | {status}")

    print("=" * 90 + "\n")


def add_manual_lead(name: str, phone: str, notes: str = "Direct Phone Call"):
    """Adds a manual lead to the system."""
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.exists(LEADS_FILE)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Source", "Customer_Name", "User_ID", "Phone", "Notes", "Status"])
        writer.writerow([timestamp, "Manual_Call", name, "N/A", phone, notes, "New - Hot Lead"])

    print(f"\n[✓] Lead successfully added: {name} ({phone})")


def search_leads(query: str):
    """Searches leads by phone number or name."""
    leads = load_leads()
    query_lower = query.lower()
    matches = [
        l for l in leads
        if query_lower in l.get("Phone", "").lower()
        or query_lower in l.get("Customer_Name", "").lower()
        or query_lower in l.get("Notes", "").lower()
    ]
    print(f"\nFound {len(matches)} match(es) for '{query}':")
    display_leads(matches)


def export_markdown_report():
    """Generates a clean Markdown report for team management."""
    leads = load_leads()
    report_path = "data/LEADS_REPORT.md"
    os.makedirs("data", exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Mollik Builders Ltd — Project 10: Leads Report\n\n")
        f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        f.write(f"*Total Captured Leads: {len(leads)}*\n\n")
        f.write("| # | Date & Time | Lead Source | Customer Name | Phone Number | Status | Notes |\n")
        f.write("|---|---|---|---|---|---|---|\n")

        for i, lead in enumerate(leads, 1):
            f.write(
                f"| {i} | {lead.get('Timestamp')} | {lead.get('Source')} | "
                f"{lead.get('Customer_Name')} | **{lead.get('Phone')}** | "
                f"`{lead.get('Status')}` | {lead.get('Notes', '').replace('|', '-')} |\n"
            )

    print(f"\n[✓] Formatted Markdown report generated at: {report_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Mollik Builders Leads Management")
    parser.add_argument("--list", action="store_true", help="List all captured leads")
    parser.add_argument("--search", type=str, help="Search lead by name or phone")
    parser.add_argument("--add", nargs=2, metavar=("NAME", "PHONE"), help="Manually add lead: --add 'Rahim' '01712345678'")
    parser.add_argument("--notes", type=str, default="Direct Phone Inquiry", help="Notes for manually added lead")
    parser.add_argument("--export", action="store_true", help="Export leads to data/LEADS_REPORT.md")

    args = parser.parse_args()

    if args.add:
        add_manual_lead(args.add[0], args.add[1], args.notes)
    elif args.search:
        search_leads(args.search)
    elif args.export:
        export_markdown_report()
    else:
        display_leads(load_leads())


if __name__ == "__main__":
    main()

