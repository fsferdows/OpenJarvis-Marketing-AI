# OpenJarvis Marketing AI — Technical Architecture

Engineered by **FS Ferdows** ([@fsferdows](https://github.com/fsferdows)).

## 1. Overview
OpenJarvis Marketing AI is an autonomous, self-hosted system that unifies performance ad management, conversational lead conversion, and real-time WhatsApp CRM dispatching.

```
Incoming Web Traffic / Meta Ads
             │
             ▼
   [Meta Cloud Automations] ──(24/7 Laptop-Off)──► Instant Messenger DM
             │
   (Comment Webhook / API)
             ▼
   [Local OpenJarvis Engine] (localhost:5050)
             │
             ├──► Intent Extraction (comment_responder.py)
             ├──► Local LLM Inference (qwen2.5:3b via Ollama)
             ├──► Lead Database (data/project_bookings.csv)
             └──► WhatsApp Push Dispatcher (whatsapp_dispatcher.py)
```

## 2. Key Modules
- `local_dashboard.py`: Zero-dependency Web Speech API voice dashboard running on Python standard library.
- `sales_agent.py`: High-converting multi-turn AI closer trained for real estate and high-ticket service bookings.
- `comment_responder.py`: Automated post/reel comment listener with regex phone extraction for Bangladesh (+880).
- `whatsapp_dispatcher.py`: Desktop protocol URI router with zero third-party cloud costs.
- `send_csv_to_whatsapp.py`: Daily executive database compiler and automated reporting engine.
