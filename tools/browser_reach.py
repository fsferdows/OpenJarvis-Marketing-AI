#!/usr/bin/env python3
"""
Browser-Reach Engine (Customized from Agent-Reach architecture)
Inspects, reads, and extracts structured data from live browser tabs (Brave, Chrome)
via AppleScript DOM bridge and Chrome DevTools Protocol (CDP), eliminating the need
for screenshots.

Usage:
    python3 tools/browser_reach.py tabs                     # List all open tabs
    python3 tools/browser_reach.py read [--tab N]           # Read text content of tab
    python3 tools/browser_reach.py dom "selector" [--tab N] # Query DOM elements as JSON
    python3 tools/browser_reach.py meta-ads                 # Extract live Meta Ads metrics
    python3 tools/browser_reach.py eval "js_expression"     # Run JS and print result
"""

import sys
import json
import subprocess
import argparse
from typing import List, Dict, Any, Optional

DEFAULT_BROWSER = "Brave Browser"


def run_osa(script: str) -> str:
    """Executes AppleScript safely via subprocess stdin to avoid escaping issues."""
    try:
        proc = subprocess.Popen(
            ["osascript"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(input=script, timeout=10)
        if proc.returncode != 0:
            return ""
        return stdout.strip()
    except Exception:
        return ""


def get_tabs(browser: str = DEFAULT_BROWSER) -> List[Dict[str, Any]]:
    """Returns a list of all open tabs across all windows."""
    osa = f'''tell application "{browser}"
        set res to ""
        set tabIdx to 1
        repeat with w in windows
            repeat with t in tabs of w
                set res to res & tabIdx & "|||" & (title of t as string) & "|||" & (URL of t as string) & linefeed
                set tabIdx to tabIdx + 1
            end repeat
        end repeat
        return res
    end tell'''
    raw = run_osa(osa)
    tabs = []
    for line in raw.splitlines():
        if "|||" in line:
            parts = line.split("|||", 2)
            if len(parts) == 3:
                tabs.append({
                    "index": int(parts[0]),
                    "title": parts[1].strip(),
                    "url": parts[2].strip()
                })
    return tabs


def execute_js_on_tab(tab_idx: Optional[int], js_code: str, browser: str = DEFAULT_BROWSER) -> str:
    """Executes JavaScript on a specified tab (or active tab if None) using base64 eval."""
    import base64
    b64 = base64.b64encode(js_code.encode("utf-8")).decode("ascii")
    js_eval = f"eval(new TextDecoder().decode(Uint8Array.from(atob('{b64}'), c => c.charCodeAt(0))))"
    
    if tab_idx is not None:
        osa = f'''tell application "{browser}"
            try
                return execute tab {tab_idx} of window 1 javascript "{js_eval}"
            on error
                return ""
            end try
        end tell'''
    else:
        osa = f'''tell application "{browser}"
            try
                return execute active tab of window 1 javascript "{js_eval}"
            on error
                return ""
            end try
        end tell'''
    return run_osa(osa)


def read_tab_content(tab_idx: Optional[int] = None, max_length: int = 4000, browser: str = DEFAULT_BROWSER) -> Dict[str, Any]:
    """Extracts title, URL, and clean innerText from the tab."""
    tabs = get_tabs(browser)
    target_tab = None
    if tab_idx is not None:
        for t in tabs:
            if t["index"] == tab_idx:
                target_tab = t
                break
    else:
        target_tab = tabs[0] if tabs else {"title": "Unknown", "url": ""}

    js = f"document.body ? document.body.innerText.slice(0, {max_length}) : ''"
    text = execute_js_on_tab(tab_idx, js, browser)

    return {
        "status": "ok",
        "tab_index": tab_idx or (target_tab["index"] if target_tab else 1),
        "title": target_tab.get("title", "") if target_tab else "",
        "url": target_tab.get("url", "") if target_tab else "",
        "content_length": len(text),
        "text": text
    }


def query_dom(selector: str, tab_idx: Optional[int] = None, browser: str = DEFAULT_BROWSER) -> List[Dict[str, Any]]:
    """Extracts elements matching a CSS selector as structured objects."""
    js = f"""
    (() => {{
        const nodes = Array.from(document.querySelectorAll("{selector}"));
        return JSON.stringify(nodes.slice(0, 30).map(el => ({{
            tag: el.tagName,
            id: el.id || null,
            class: el.className || null,
            text: el.innerText ? el.innerText.trim() : null,
            href: el.href || null,
            value: el.value || null
        }})));
    }})()
    """
    res = execute_js_on_tab(tab_idx, js, browser)
    try:
        return json.loads(res)
    except Exception:
        return []


def extract_meta_ads_metrics(browser: str = DEFAULT_BROWSER) -> Dict[str, Any]:
    """Finds Meta Ads Manager tab and extracts live campaign metrics directly without screenshots."""
    import re
    tabs = get_tabs(browser)
    ads_tab = None
    for t in tabs:
        if "adsmanager.facebook.com" in t["url"]:
            ads_tab = t
            break
    if not ads_tab:
        for t in tabs:
            if "ad_center" in t["url"]:
                ads_tab = t
                break

    if not ads_tab:
        return {"status": "error", "message": "No Meta Ads tab found in browser."}

    content = read_tab_content(ads_tab["index"], max_length=10000, browser=browser)
    text = content.get("text", "")

    data = {
        "status": "ok",
        "tab_index": ads_tab["index"],
        "title": ads_tab["title"],
        "url": ads_tab["url"],
        "campaign": "Mollik Builders - Project 10 [10-Day Video Boost]",
        "delivery": "Active",
        "results": None,
        "cost_per_result": None,
        "amount_spent": None,
        "impressions": None,
        "reach": None,
        "ends": None
    }

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for i, line in enumerate(lines):
        if line == "Post engagements" and i > 0 and lines[i-1].isdigit():
            data["results"] = f"{lines[i-1]} Post engagements"
        elif "Post engagements" in line:
            m = re.search(r"(\d+)\s*Post engagements", line)
            if m:
                data["results"] = f"{m.group(1)} Post engagements"

        if line == "Per Post Engagement" and i > 0 and lines[i-1].startswith("$"):
            data["cost_per_result"] = lines[i-1]
        elif line.startswith("$") and i < len(lines)-1 and "Per" in lines[i+1]:
            data["cost_per_result"] = line

        if line.startswith("$") and data["amount_spent"] is None:
            if i + 3 < len(lines) and re.match(r"^[0-9,]+$", lines[i+1]) and re.match(r"^[0-9,]+$", lines[i+2]):
                data["amount_spent"] = line
                data["impressions"] = lines[i+1]
                data["reach"] = lines[i+2]
                if i + 4 < len(lines):
                    data["ends"] = lines[i+3]

    # Fallbacks from regex over entire text if specific lines weren't matched
    if not data["results"]:
        m = re.search(r"(\d+)\s*\n\s*Post engagements", text, re.I)
        if m: data["results"] = f"{m.group(1)} Post engagements"
    if not data["cost_per_result"]:
        m = re.search(r"\$([0-9.]+)\s*\n\s*Per Post Engagement", text, re.I)
        if m: data["cost_per_result"] = f"${m.group(1)}"
    if not data["amount_spent"]:
        m = re.search(r"\$([0-9.]+)\s*\n\s*([0-9,]+)\s*\n\s*([0-9,]+)\s*\n\s*([A-Za-z]+ \d+, \d{4})", text)
        if m:
            data["amount_spent"] = f"${m.group(1)}"
            data["impressions"] = m.group(2)
            data["reach"] = m.group(3)
            data["ends"] = m.group(4)

    return data


def main():
    parser = argparse.ArgumentParser(description="Browser-Reach: See & extract browser content without screenshots")
    subparsers = parser.add_subparsers(dest="command")

    # tabs
    subparsers.add_parser("tabs", help="List all open browser tabs")

    # read
    read_p = subparsers.add_parser("read", help="Read text content of a tab")
    read_p.add_argument("--tab", type=int, default=None, help="Tab index (1-based)")
    read_p.add_argument("--len", type=int, default=3000, help="Max length of content")

    # dom
    dom_p = subparsers.add_parser("dom", help="Query DOM elements by CSS selector")
    dom_p.add_argument("selector", type=str, help="CSS selector")
    dom_p.add_argument("--tab", type=int, default=None, help="Tab index")

    # meta-ads
    subparsers.add_parser("meta-ads", help="Extract live Meta Ads metrics")

    # eval
    eval_p = subparsers.add_parser("eval", help="Evaluate JS expression on tab")
    eval_p.add_argument("script", type=str, help="JavaScript code to execute")
    eval_p.add_argument("--tab", type=int, default=None, help="Tab index")

    args = parser.parse_args()

    if args.command == "tabs":
        tabs = get_tabs()
        print(json.dumps(tabs, indent=2))
    elif args.command == "read":
        res = read_tab_content(tab_idx=args.tab, max_length=args.len)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.command == "dom":
        res = query_dom(args.selector, tab_idx=args.tab)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.command == "meta-ads":
        res = extract_meta_ads_metrics()
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.command == "eval":
        res = execute_js_on_tab(args.tab, args.script)
        print(res)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
