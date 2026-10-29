<div align="center">

# 🚀 OpenJarvis Marketing AI
### **Autonomous 24/7 Self-Hosted Growth, Meta Ads & AI Sales Agent**
#### *With Zero-Screenshot Browser Vision (Agent-Reach), Voice AI & Instant WhatsApp CRM*

[![GitHub Stars](https://img.shields.io/github/stars/fsferdows/OpenJarvis-Marketing-AI?style=for-the-badge&logo=github&color=FFD700)](https://github.com/fsferdows/OpenJarvis-Marketing-AI)
[![GitHub Forks](https://img.shields.io/github/forks/fsferdows/OpenJarvis-Marketing-AI?style=for-the-badge&logo=github&color=00BFFF)](https://github.com/fsferdows/OpenJarvis-Marketing-AI)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Meta Graph API](https://img.shields.io/badge/Meta%20Graph%20API-v26.0-0668E1?style=for-the-badge&logo=meta)](https://developers.facebook.com)
[![Zero-Screenshot Vision](https://img.shields.io/badge/Browser%20Vision-Agent--Reach%20CDP-9B51E0?style=for-the-badge&logo=googlechrome)](https://github.com/Panniantong/Agent-Reach)
[![Local LLM](https://img.shields.io/badge/Local%20LLM-Ollama%20%7C%20Metal%20GPU-FF6B6B?style=for-the-badge&logo=ollama)](https://ollama.ai)
[![WhatsApp Real-time](https://img.shields.io/badge/WhatsApp-Instant%20Alerts-25D366?style=for-the-badge&logo=whatsapp)](https://wa.me/8801633309081)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<br/>

**A production-ready, 100% self-hosted AI Sales, Marketing Automation & Lead Engine.**  
Engineered to automate high-ticket lead generation, deploy hyper-targeted Meta ad campaigns, auto-respond to reel & post comments 24/7 (even with your laptop powered off), read browsers and social platforms in 0.2s without taking screenshots, negotiate deals with polite persuasive AI salesmanship, and dispatch instant booking alerts and CSV databases directly to WhatsApp.

[Explore Architecture](#-system-architecture) • [Core Superpowers](#-core-superpowers) • [Zero-Screenshot Vision](#-zero-screenshot-browser-vision-agent-reach) • [Quickstart in 60s](#-quickstart-guide) • [Developer Profile](#-meet-the-developer)

---

</div>

<br/>

## ⚡ Why OpenJarvis Marketing AI?

Most marketing automation tools force you into expensive monthly SaaS subscriptions, leak sensitive customer records into third-party clouds, and stop functioning the moment you shut your laptop. 

**OpenJarvis flips the script:**
* 🔒 **100% On-Device & Private:** Powered locally by **Ollama** (`qwen2.5:3b`, `llama3`, etc.) running on Apple Silicon Metal GPU / NVIDIA CUDA. Zero external LLM token bills.
* 🌐 **True 24/7 Autonomy (Laptop-Off Ready):** Seamlessly bridges local execution with native **Meta Cloud Automation** (Comment-to-Message & Instant Reply), ensuring continuous lead capture 24/7/365 even when your computer is asleep or powered down.
* 👁️ **Zero-Screenshot Browser Vision (Agent-Reach):** Inspects browser tabs, DOM tables, and live ad delivery in **0.2 seconds** via Chrome DevTools Protocol (CDP) without slow screenshots or OCR image clutter.
* 🎙️ **Interactive Voice Control Center:** Speak to Jarvis via your microphone; receive spoken voice responses and real-time dashboard analytics at `http://localhost:5050`.
* 🎯 **Precision Meta Ads Engine:** Deploys laser-focused multi-pin GPS radius campaigns ($3/day micro-boosts) that intelligently bypass category delivery dilution.
* 💬 **Polite Persuasive AI Salesman:** Speaks prestigious multilingual sales copy (English & Bengali), answers pricing, location, and amenity questions, and books high-ticket site visits.
* 📲 **WhatsApp Lead Dispatcher & Live CSV Engine:** Auto-extracts verified phone numbers from social comments, updates persistent local CSV spreadsheets, and shoots instant lead cards to the owner's WhatsApp (`+8801633309081`).

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph Traffic ["1. Traffic & Inbound Acquisition"]
        A["Meta Ads / Boosted Reels (v26.0)"] -->|"Comments / Queries"| B["User Inquiries & Reactions"]
    end

    subgraph AutonomousCore ["2. Autonomous AI Engine (24/7 Hybrid)"]
        B -->|"Cloud 24/7 (Laptop-Off)"| C["Meta Cloud Automations\n(Comment-to-DM & Instant Reply)"]
        B -->|"Local Daemon"| D["comment_responder.py\n(Intent & BD Phone Extractor)"]
        D --> E["sales_agent.py\n(Polite Persuasive Closer)"]
        E --> F["Local Ollama Engine\n(Apple Silicon GPU / CUDA)"]
    end

    subgraph VisionEngine ["3. Zero-Screenshot Browser Vision"]
        G["Live Browser Tabs (Brave / Chrome)"] -->|"CDP & DOM Bridge"| H["tools/browser_reach.py\n(Agent-Reach Architecture)"]
        H -->|"Sub-second Extraction"| I["Live Spend, Reach, Impressions & Metrics"]
        I --> F
    end

    subgraph DataEngine ["4. Local Storage & Lead Ledger"]
        E --> J["data/project_bookings.csv\n(Zero Cloud Leaks / 100% Self-Hosted)"]
        D --> K["data/leads.csv\n(Hot Leads Log)"]
        J --> L["data/Mollik_Builders_Bookings.csv\n(Clean Management Export)"]
    end

    subgraph Notification ["5. Instant Alerts & Control Center"]
        J --> M["whatsapp_dispatcher.py\n(1-Click Chat Link + Native Chime)"]
        L --> N["send_csv_to_whatsapp.py\n(Executive CSV Summary)"]
        M --> O["📲 Owner WhatsApp (+8801633309081)"]
        N --> O
        F --> P["OpenJarvis Dashboard (localhost:5050)\nVoice Mic + TTS + Live Analytics"]
    end

    style Traffic fill:#1a1c23,stroke:#0668E1,stroke-width:2px,color:#fff
    style AutonomousCore fill:#1a1c23,stroke:#FF6B6B,stroke-width:2px,color:#fff
    style VisionEngine fill:#1a1c23,stroke:#9B51E0,stroke-width:2px,color:#fff
    style DataEngine fill:#1a1c23,stroke:#00BFFF,stroke-width:2px,color:#fff
    style Notification fill:#1a1c23,stroke:#25D366,stroke-width:2px,color:#fff
```

---

## 👁️ Zero-Screenshot Browser Vision (Agent-Reach)

Unlike conventional web agents that take slow full-screen screenshots (`screencapture`) and bloat your disk with rasterized PNG images, OpenJarvis integrates **Agent-Reach** (`skills/agent-reach`) and a customized DOM bridge (`tools/browser_reach.py`):

* ⚡ **Sub-Second Execution (0.2s):** Directly extracts DOM text, metrics, and tables without screenshot latency or OCR errors.
* 🛡️ **Zero Disk Footprint:** No temporary PNG files, avoiding disk space exhaustion.
* 🔑 **Existing Session Reuse:** Automatically reads authenticated tabs (Meta Business Suite, Ads Manager, Facebook) without prompting for passwords or storing credentials.

```bash
# 1. Inspect all open browser tabs & URLs instantly
python3 tools/browser_reach.py tabs

# 2. Extract live Meta Ads Manager metrics in 0.2s
python3 tools/browser_reach.py meta-ads

# 3. Read complete text content of any tab without taking a screenshot
python3 tools/browser_reach.py read --tab 5 --len 2000

# 4. Extract specific DOM elements by CSS selector as structured JSON
python3 tools/browser_reach.py dom "table tr" --tab 5
```

---

## 🔥 Core Superpowers

### 1. 🎙️ OpenJarvis Voice & Web Control Center (`localhost:5050`)
* **Real-time Voice Pipeline:** Click 🎤 to speak voice instructions directly to Jarvis (*"Check Meta Ads"*, *"Show latest bookings"*, *"Explain pricing"*).
* **Hardware-Accelerated Inference:** Runs locally on `qwen2.5:3b` via Ollama with Apple Silicon Metal GPU acceleration.
* **Live Interactive Table:** Renders customer bookings from `data/project_bookings.csv` in real time with 1-click WhatsApp direct chat buttons (`wa.me/8801...`).

### 2. 🎯 Meta Ads Precision Deployment (`deploy_meta_ads.py`)
* Deploys and manages Facebook & Instagram Video Boost campaigns via Meta Graph API v26.0.
* Employs hyper-local 3km radius GPS pin drops (e.g. Uttara, Airport, Mirpur, Tongi, Khilkhet) with high-efficiency \$3/day budgeting.
* Avoids restrictive delivery dilution while maintaining 100% Meta policy compliance.

### 3. 💬 24/7 Comment Replier & Lead Extraction (`comment_responder.py`)
* Smart regex and NLP intent classification (`price_inquiry`, `location_inquiry`, `details_inquiry`, `phone_detected`).
* Automatic detection and sanitization of Bangladeshi mobile numbers (`017...`, `018...`, `+8801...`).
* Anti-bot safeguards: Randomized polite phrasing with human-like randomized reply delays (2.5s - 5.0s).

### 4. 📲 Instant WhatsApp Dispatcher (`whatsapp_dispatcher.py`)
* Automatically formats and delivers rich lead notification cards straight to the owner's WhatsApp (`+8801633309081`).
* macOS native notification banner with audio chime on every new hot booking.
* Complete daily CSV report compiled and sent with 1-click management review links.

### 5. 🧠 Comprehensive Agent Skills Library (50+ Skills)
Pre-loaded with battle-tested agent skills for SEO, CRO, copy editing, ad creative generation, ASO, schema validation, and competitor profiling based on the [Agent Skills Standard](https://agentskills.io).

---

## 💻 Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Local LLM** | Ollama (`qwen2.5:3b`) | 100% offline reasoning & natural Bengali/English dialogue |
| **Browser Vision** | Agent-Reach + CDP Bridge | Zero-screenshot DOM text & table extraction in 0.2s |
| **Frontend UI** | Modern Vanilla JS + CSS3 + Web Speech API | Zero-dependency, lightweight, voice-enabled control dashboard |
| **Backend Engine** | Python 3.10+ (Standard Library HTTP / Subprocess) | High-speed, self-hosted daemon running on `localhost:5050` |
| **Ads & API** | Meta Graph API v26.0 | Automated ad boosting, metrics monitoring, and comment fetching |
| **Database** | CSV / SQLite (Local Disk) | Zero-cloud, encrypted, persistent customer booking ledger |
| **Notifications**| macOS URI Protocol & `wa.me` Deep Links | Instant, zero-cost WhatsApp push delivery |

---

## ⚡ Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/fsferdows/OpenJarvis-Marketing-AI.git
cd OpenJarvis-Marketing-AI
```

### 2. Configure Environment Variables
Create `.env.marketing` in the root directory (see `.env.example`):
```env
META_ACCESS_TOKEN="your_meta_page_or_user_access_token"
AD_ACCOUNT_ID="act_your_account_id"
PAGE_ID="your_facebook_page_id"
OWNER_WHATSAPP="+8801633309081"
```

### 3. Launch the Local Ollama Engine
Make sure [Ollama](https://ollama.ai) is installed and run:
```bash
ollama run qwen2.5:3b
```

### 4. Start the OpenJarvis Local Control Center
```bash
python3 local_dashboard.py
```
Open your browser to: **`http://localhost:5050`**  
Click the **🎤 Microphone** button or quick-action chips to start commanding your AI agent!

### 5. See Browser Content (No Screenshots Needed!)
```bash
# List open tabs
python3 tools/browser_reach.py tabs

# Extract live Meta Ads metrics
python3 tools/browser_reach.py meta-ads
```

### 6. Run the Automated Comment Replier
```bash
# Preview replies safely
python3 comment_responder.py --dry-run

# Run in continuous 24/7 background loop
python3 comment_responder.py --loop --interval 60
```

### 7. Export Bookings & Dispatch to WhatsApp
```bash
python3 send_csv_to_whatsapp.py
```

---

## 📂 Project Structure

```
├── local_dashboard.py         # Web & Voice Control Center (localhost:5050)
├── sales_agent.py             # Conversational Real Estate Closer (Ollama)
├── comment_responder.py       # Facebook Reel/Post Comment Replier & Lead Hunter
├── deploy_meta_ads.py         # Automated Meta Ads Precision Manager
├── whatsapp_dispatcher.py     # Real-time WhatsApp Notification Router
├── send_csv_to_whatsapp.py    # Formatted CSV Report Generator & Exporter
├── booking_manager.py         # CLI Lead Management Utility
├── tools/
│   └── browser_reach.py       # Zero-Screenshot Browser Vision & DOM Bridge
├── data/
│   ├── project_bookings.csv   # Master persistent booking database
│   ├── leads.csv              # Extracted hot leads
│   └── whatsapp_outbox.json   # Outgoing alerts audit trail
├── skills/
│   ├── agent-reach/           # Zero-Screenshot Browser Vision Skill
│   └── ...                    # 50+ Agent Skills (SEO, CRO, Ads, Copywriting)
└── .env.example               # Configuration Template
```

---

## 👨‍💻 Meet the Developer

<div align="center">

### **FS Ferdows**
**Lead AI Architect & Autonomous Systems Engineer**

[![WhatsApp](https://img.shields.io/badge/WhatsApp-Chat%20Directly-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/8801633309081)
[![Email](https://img.shields.io/badge/Email-fsferdows%40icloud.com-EA4335?style=for-the-badge&logo=icloud&logoColor=white)](mailto:fsferdows@icloud.com)
[![YouTube](https://img.shields.io/badge/YouTube-@fsferdowsyt-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtube.com/@fsferdowsyt?si=03HdUXfd3jfuD0AZ)
[![GitHub](https://img.shields.io/badge/GitHub-fsferdows-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/fsferdows)

</div>

> *"I build autonomous AI systems that eliminate repetitive human friction, connect cutting-edge local LLMs with real-world marketing infrastructure, and turn raw digital traffic into verified, closed deals — 100% private, self-hosted, and relentless 24/7."*

**Areas of Specialization:**
* 🧠 Autonomous Multi-Agent Workflows & Local LLM Integration (Ollama, Apple Silicon GPU acceleration)
* 👁️ Zero-Screenshot Browser Vision & Headless DOM Automation (Agent-Reach, CDP)
* 📈 Performance Growth Engineering & Meta Graph API Automation
* 🛡️ Zero-Cloud Privacy Architectures & Custom Webhook Pipelines
* 💬 Multilingual Conversational Sales Systems (Bangla & English)

**Have a project or want to collaborate?**  
* 📱 **WhatsApp:** [`+8801633309081`](https://wa.me/8801633309081)  
* ✉️ **Email:** [`fsferdows@icloud.com`](mailto:fsferdows@icloud.com)  
* 🎥 **YouTube:** [`@fsferdowsyt`](https://youtube.com/@fsferdowsyt?si=03HdUXfd3jfuD0AZ)

---

## 🤝 Contributing

Contributions, issues, and feature requests are warmly welcomed!  
Feel free to check out the [Issues page](https://github.com/fsferdows/OpenJarvis-Marketing-AI/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: Add AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⭐ Star History

If this autonomous agent framework helped you optimize your marketing, save money on cloud tokens, or automate your lead generation, please consider giving it a **Star ⭐**!

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=fsferdows/OpenJarvis-Marketing-AI&type=Date)](https://star-history.com/#fsferdows/OpenJarvis-Marketing-AI&Date)

<br/>

**Built with ❤️ and Precision by FS Ferdows.**  
*Distributed under the MIT License.*

</div>
