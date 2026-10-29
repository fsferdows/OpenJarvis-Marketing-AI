# Mollik Builders Ltd — Project 10
## Performance Marketing & Lead Automation Engine

This documentation outlines the automated lead generation, ad boosting, and customer response system deployed for **Mollik Builders Ltd — Project 10 (Bashtola, Bhuiyan Bari, Dhaka)**.

---

### 📂 Architecture Overview

```
marketing skills/
├── deploy_meta_ads.py        # Meta Marketing API Deployer (5 GPS Pins, Age 30-55, $3/day)
├── comment_responder.py      # Automated Video Comment Responder & Phone Extractor
├── customer_lead_bot.py      # Conversational Lead Bot for Customer Inquiries
├── leads_manager.py          # Sales Dashboard CLI (List, Search, Export Leads)
└── data/
    ├── leads.csv             # Centralized database of qualified buyer phone numbers
    ├── LEADS_REPORT.md       # Auto-generated formatted management report
    └── comment_replies.json  # Anti-spam state preventing duplicate replies
```

---

### 🚀 1. The Active Boosted Ad
* **Campaign:** `Mollik Builders - Project 10 [10-Day Video Boost]` (ID: `120255594274270063`)
* **Ad Set:** `Dhaka North & Airport Belt - 3km GPS Pins (10 Days @ $3/day)` (ID: `120255594363430063`)
* **Ad:** `Project 10 - Video Ad (Bashtola, Uttara)` (ID: `120255594364360063`)
* **Live Video URL:** [https://www.facebook.com/reel/1666992078479821](https://www.facebook.com/reel/1666992078479821)
* **Targeting:** 5 GPS coordinate pins (3 km radius each):
  1. Uttara / Azampur Hub (`23.8698, 90.3985`)
  2. Airport / Kawla Aviation Belt (`23.8433, 90.4042`)
  3. Tongi Industrial Belt (`23.9015, 90.4022`)
  4. Mirpur Salaried Hub (`23.8067, 90.3687`)
  5. Khilkhet / Kuril Corridor (`23.8293, 90.4197`)
* **Budget & Schedule:** \$3.00 USD/day for 10 Days (\$30 total).

---

### 💬 2. Auto-Replying to Video Comments (`comment_responder.py`)
Monitors comments on the boosted video post, categorizes questions, replies with natural Bengali copy, and captures phone numbers.

* **To test in Dry-Run mode:**
  ```bash
  python3 comment_responder.py --dry-run
  ```
* **To run continuously in background:**
  ```bash
  python3 comment_responder.py --loop --interval 60
  ```

---

### 🤖 3. Customer Messenger & Chat Bot (`customer_lead_bot.py`)
Simulates or processes direct customer conversations, answers questions on pricing, 36-month installment, 1570 sqft specs, and location, and prompts for the buyer's contact number.

* **Run conversation test:**
  ```bash
  python3 customer_lead_bot.py
  ```

---

### 📊 4. Leads Management Dashboard (`leads_manager.py`)
View, search, and export captured buyer leads:

* **View all active leads:**
  ```bash
  python3 leads_manager.py --list
  ```
* **Search by phone number or name:**
  ```bash
  python3 leads_manager.py --search "017"
  ```
* **Add a manual walk-in or incoming phone call:**
  ```bash
  python3 leads_manager.py --add "Rafiqul Islam" "01819283746" --notes "Wants 5th floor flat, site visit this Friday"
  ```
* **Export Markdown summary report:**
  ```bash
  python3 leads_manager.py --export
  ```

---

### 🎯 5. Sales Team Script & Closing Protocol
When a lead is captured in `data/leads.csv`:
1. **Response Time:** Call within 5–15 minutes.
2. **Elevator Pitch:**
   > *"আসসালামু আলাইকুম [নাম] ভাই! মল্লিক বিল্ডার্স থেকে প্রজেক্ট ১০ (বাশতলা) নিয়ে যোগাযোগ করছি। আমাদের ১৫৭০ স্কয়ার ফিটের ৩-বেড লাক্সারি ফ্ল্যাটটি জমি শেয়ারিং পদ্ধতিতে সর্বমোট মাত্র ৪৮.২৫ লাখে পাচ্ছেন, সাথে রয়েছে ৩৬ মাসের সহজ কিস্তি এবং নির্ধারিত সময়ে হস্তান্তরের লিখিত পেনাল্টি রেন্ট গ্যারান্টি। আগামী শুক্র বা শনিবার সরাসরি সাইট ভিজিটের জন্য কি একটি স্লট বুক করে দেব?"*
3. **Send WhatsApp Brochure:** Send the 1570 sqft floor plan and project video to their WhatsApp number immediately.

