---
name: agent-reach
description: Read-only access to browser content, open tabs, DOM text, and social platforms without taking screenshots. Use when inspecting browser tabs, checking live Meta Ads metrics, reading web pages, or extracting structured page data.
metadata:
  version: 1.6.0
  author: Panniantong / FS Ferdows
  homepage: https://github.com/Panniantong/Agent-Reach
---

# Agent Reach & Browser Vision (Zero-Screenshot Engine)

Agent Reach provides direct, structured, read-only access to browser sessions, open tabs, and live web platforms (Meta Ads, Facebook, Twitter/X, YouTube, GitHub, Reddit, and Web) **without taking screenshots**.

## Core Capabilities

Instead of running slow `screencapture` commands or analyzing rasterized PNG images, use the built-in `tools/browser_reach.py` DOM and CDP bridge to extract exact text, table cells, and metrics directly from the browser in sub-second time.

### Quick Commands

```bash
# 1. List all open browser tabs (with title, URL, and tab index)
python3 tools/browser_reach.py tabs

# 2. Read live text content from a specific tab (or active tab)
python3 tools/browser_reach.py read --tab <index> --len 3000

# 3. Query specific DOM elements by CSS selector as JSON
python3 tools/browser_reach.py dom "table tr" --tab <index>
python3 tools/browser_reach.py dom "button, a" --tab <index>

# 4. Extract live Meta Ads Manager / Ad Center metrics instantly
python3 tools/browser_reach.py meta-ads

# 5. Evaluate custom JavaScript on any open tab
python3 tools/browser_reach.py eval "document.title" --tab <index>
```

## When to Use

1. **Inspecting Live Ad Delivery & Performance:**  
   Run `python3 tools/browser_reach.py meta-ads` to get live spend, reach, impressions, and post engagements directly from Meta Ads Manager.
2. **Reading Web Pages & Social Platforms:**  
   Run `python3 tools/browser_reach.py read --tab <index>` to extract the complete article, post, or comments without image OCR latency.
3. **Automating Form / Tab Navigation:**  
   Run `python3 tools/browser_reach.py eval "document.querySelector('...').click()"` to trigger browser actions natively.

## Error Handling

* **Tab Not Found:** Run `python3 tools/browser_reach.py tabs` to refresh the index list.
* **Empty Content:** If a page is loading dynamically, wait 1-2 seconds and re-run `read`.
* **Login Required:** Agent Reach accesses existing authenticated sessions from your active browser profile without reading password vaults or leaking credentials.
