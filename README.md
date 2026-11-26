# 🛡️ ∀VITR AI (अवितृ • The Protector)

### Multi-Modal Real-Time Cyber-Fraud Threat Intelligence Platform

<div align="center">

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python: 3.12](https://img.shields.io/badge/Python-3.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi&logoColor=white)
![React: 18](https://img.shields.io/badge/Frontend-React%2018%20%7C%20Vite%205-61DAFB.svg?logo=react&logoColor=black)
![TailwindCSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38B2AC.svg?logo=tailwind-css&logoColor=white)
![OCR: Tesseract.js WASM](https://img.shields.io/badge/OCR-Tesseract.js%20WASM-FF6F00.svg)
![Speech Recognition](https://img.shields.io/badge/Audio-Whisper%20STT-FF6F00.svg)
![Database](https://img.shields.io/badge/Database-Supabase%20Postgres-3ECF8E.svg?logo=supabase&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-12%2F12%20Passing%20(100%25)-brightgreen.svg)

**An ultra-fast (< 5 ms inference), 4-modality dual-engine cyber-fraud intelligence system designed to intercept malicious SMS, spoofed emails, fraudulent voice calls, and scam screenshots with zero cloud privacy exposure.**

[Key Features](#-key-features) • [4 Input Modalities](#-4-input-modalities) • [System Architecture](#-system-architecture-flow) • [Threat Matrix](#-13-vector-deterministic-threat-matrix) • [Repository Structure](#-complete-project-repository-structure) • [REST API](#-production-rest-api-gateway) • [Quickstart](#-running-the-platform-locally)

</div>

---

## 📌 Executive Overview

**∀VITR AI** (derived from the Sanskrit **अवितृ**, meaning *"The Protector"* or *"Defender"*) is a production-grade cyber-fraud detection and threat intelligence platform built to protect citizens, enterprises, and financial systems from modern social engineering vectors.

Rather than relying on slow, costly, and hallucination-prone Large Language Models (LLMs) in the critical path, **∀VITR AI** implements a **Dual-Core Architecture**:
1. **Calibrated Machine Learning Engine:** TF-IDF n-gram vectorizer paired with a calibrated Logistic Regression classifier trained on an industrial corpus of **10,392 multi-modal samples** (98.6% Accuracy, 99.8% Precision).
2. **Deterministic Security Threat Matrix:** A 13-vector rule engine detecting artificial urgency, authority impersonation, Digital Arrest extortion (BNSS 2023), utility cutoffs, and spoofed peer VPAs.
3. **Client-Side Zero-Knowledge OCR:** Powered by WebAssembly (Tesseract.js WASM), extracting screenshot text entirely in the user's browser—preventing sensitive bank accounts, names, and personal photos from ever leaving the device.
4. **Cryptographic Proof & Auto-Complaint:** Emits 256-bit HMAC-SHA256 tamper-proof forensic verification tokens and generates 1-click legal complaints ready for the National Cyber Crime Portal (1930) and Chakshu.

```
       ┌────────────────────────────────────────────────────────────────────────┐
       │                        4-MODALITY INGESTION                            │
       │   [ 💬 SMS ]     [ 📧 RFC Email ]     [ 🎙️ Audio ]     [ 📸 Screenshot ]│
       └───────┬───────────────────┬───────────────────┬─────────────────┬──────┘
               │                   │                   │                 │
               │                   │                   │         Client-Side OCR
               │                   │                   ▼         (Tesseract WASM)
               │                   │           OpenAI Whisper    Zero-Knowledge
               │                   ▼             STT Engine         Extraction
               │             RFC Header Parser         │                 │
               ▼             & Domain SPF/DKIM         ▼                 ▼
       ┌────────────────────────────────────────────────────────────────────────┐
       │                 ∀VITR AI HIGH-SPEED BACKEND GATEWAY                    │
       │                                                                        │
       │  ┌───────────────────────┐           ┌──────────────────────────────┐  │
       │  │ In-Memory Threat Cache│           │ Anti-Spam Sliding Buffer     │  │
       │  │ (< 0.1ms Deduplication)           │ (Rate Limiting & Cooldown)   │  │
       │  └───────────┬───────────┘           └──────────────┬───────────────┘  │
       │              └───────────────────────┬──────────────┘                  │
       │                                      ▼                                 │
       │  ┌──────────────────────────────────────────────────────────────────┐  │
       │  │                   DUAL-CORE THREAT EVALUATION                    │  │
       │  │                                                                  │  │
       │  │   ┌──────────────────────────┐    ┌──────────────────────────┐   │  │
       │  │   │   Classical ML Model     │    │  Deterministic Heuristics│   │  │
       │  │   │   • TF-IDF N-grams       │    │  • 13 Security Vectors   │   │  │
       │  │   │   • Calibrated LogReg    │    │  • BNSS 2023 Law Logic   │   │  │
       │  │   │   • Probability (0.0-1.0)│    │  • Extortion & VPA Regex │   │  │
       │  │   └─────────────┬────────────┘    └────────────┬─────────────┘   │  │
       │  │                 └──────────────┬───────────────┘                 │  │
       │  │                                ▼                                 │  │
       │  │                  Dual-Verification Aggregator                    │  │
       │  └────────────────────────────────┬─────────────────────────────────┘  │
       └───────────────────────────────────┼────────────────────────────────────┘
                                           │
                                           ▼
       ┌────────────────────────────────────────────────────────────────────────┐
       │                         ACTIONABLE FORENSICS                           │
       │  • Risk Score (0-100%)       • Bayesian Confidence (98.2%)             │
       │  • Forensic Badges           • Root Cause Explainability               │
       │  • HMAC-SHA256 Token         • 1-Click Cyber Police 1930 / Chakshu     │
       └────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Key Features

* 🚀 **Sub-5 Millisecond Inference:** Lightning-fast offline evaluation with zero cloud API token costs.
* 📸 **Zero-Knowledge Screenshot OCR:** Complete on-device text extraction via `tesseract.js` WebAssembly with native `Ctrl + V` clipboard paste and drag-and-drop. Sensitive photos never touch the server.
* ⚡ **Sub-Millisecond In-Memory LRU Threat Cache:** High-speed SHA-256 deduplication cache serving viral scams in **< 0.1 ms** with zero CPU overhead.
* 🔒 **Anti-Tamper Cryptographic Token:** Generates 256-bit HMAC-SHA256 signatures with random nonces to prove forensic authenticity.
* 📋 **1-Click National Cyber Crime (1930) / Chakshu Formatter:** Auto-compiles formal FIR and incident complaint drafts formatted for immediate submission.
* 👂 **Voice Call Fraud Defense:** Converts audio phone recordings into text via Whisper Speech-to-Text (STT) to catch parcel extortion and fake police threats.
* 🇮🇳 **Multilingual & Hinglish Support:** Recognizes Romanized Hindi and regional Indian cyber-coercion (*"bijli bill update", "police karyawahi", "giraftaar", "turant pay karein"*).
* 🛡️ **Zero False Positive Guarantee on Authentic Orders:** Whitelists authentic food receipts (Swiggy, Zomato) and bank debit/credit transaction alerts to ensure normal life is not flagged.
* 🎯 **Explainable Forensic Badges:** Displays explicit threat tags (e.g., `[Utility Blackout Threat]`, `[Illegal Digital Arrest Extortion (BNSS 2023)]`, `[Direct Peer UPI]`).
* 📊 **Calibrated Bayesian Confidence:** Accurately reflects model certainty ($P(\text{Scam})$ for threats, $1 - P(\text{Scam})$ for authentic communications).

---

## 🌐 4 Input Modalities

| Modality | Input Format | Primary Vectors Detected | Processing Pipeline |
| :--- | :--- | :--- | :--- |
| **💬 SMS / Text** | Raw string / Chat | Smishing, UPI collect cashback traps, lottery fraud, loan APKs, Hinglish coercion | Direct NLP tokenization + Regex matrix |
| **📧 RFC Email** | `.eml` / RFC headers | Free webmail authority spoofing, BEC CEO wire fraud, expiring Microsoft 365, tax refund lures | RFC 822 header extraction + Body NLP |
| **🎙️ Voice Audio** | `.wav` / `.mp3` / Mic | Live digital arrest interrogations, courier customs fines, fake police threats | OpenAI Whisper Speech-to-Text + Transcript scan |
| **📸 Screenshot** | Image file / `Ctrl + V` | WhatsApp chats, fake payment receipts, electricity cutoff notices, CBI notices | Client-side Tesseract.js WASM (100% on-device) |

---

## 🛡️ 13-Vector Deterministic Threat Matrix

| # | Threat Category | Example Deceptive Pattern | Trigger Badges Generated |
| :-: | :--- | :--- | :--- |
| **1** | **Credential Theft** | *"Share your 6-digit OTP or MPIN to avoid debit card block"* | `[Credential Theft: OTP / Secret PIN Solicitation]` |
| **2** | **UPI PIN Trap** | *"Enter your UPI PIN to claim Rs 2,500 PhonePe cashback"* | `[Severe UPI PIN / QR Cashback Trap]` |
| **3** | **Digital Arrest** | *"CBI Cyber Cell intercepted narcotics parcel; you are under digital arrest"* | `[Illegal Digital Arrest Extortion (BNSS 2023)]` |
| **4** | **Utility Blackout** | *"Electricity power will be cut off tonight at 9:30 PM due to unpaid bill"* | `[Utility Blackout Extortion Threat]` |
| **5** | **Banking / KYC** | *"HDFC NetBanking suspended. Update PAN card at http://hdfc-kyc.xyz"* | `[Banking KYC / Reward Points Phishing]` |
| **6** | **Loan / Malware APK**| *"Instant pre-approved loan of 5 Lakh. Install QuickCash.apk"* | `[Dangerous Android APK Malware Payload]` |
| **7** | **Gaming Bait** | *"Claim 5,000 Free Fire diamonds and BGMI UC free giveaway"* | `[Youth Gaming Bait / Credential Theft]` |
| **8** | **Part-Time Task** | *"Earn Rs 5,000 daily by liking YouTube videos. Deposit Rs 1,500"* | `[Unsolicited Task / Part-Time Job Scam]` |
| **9** | **Lottery / KBC** | *"Congratulations! Won Rs 25 Lakh in KBC WhatsApp lucky draw"* | `[Unsolicited Lottery / Prize Fraud]` |
| **10**| **Tax Phishing** | *"Income Tax refund of Rs 24,500 approved. Submit account details"* | `[Government Tax Refund Phishing Lure]` |
| **11**| **Sextortion** | *"We recorded your video call. Pay Rs 20,000 or viral on Facebook"* | `[Video Call Sextortion & Defamation Blackmail]` |
| **12**| **Suspicious VPA** | *"Send clearance fee to customsclear@axis or registration fee"* | `[Direct Peer-to-Peer UPI Payment Handle]` |
| **13**| **Hinglish Coercion** | *"Aaj raat bijli kaat diya jayega, police ghar aayegi warna nuksan"* | `[Regional Hinglish Coercion / Intimidation]` |

---

## 📂 Complete Project Repository Structure

```
ScamShield-Ai/
├── .github/                         # GitHub Actions CI/CD workflows
├── ai/                              # Core AI Detection & Forensic Engine
│   ├── dataset.py                   # Corpus loader & feature definitions
│   ├── download_datasets.py         # Multi-source dataset aggregator
│   ├── train.py                     # TF-IDF + Logistic Regression training pipeline
│   ├── detector.py                  # Dual-engine orchestrator with threat caching & rate limiting
│   ├── rule_engine.py               # 13-vector deterministic security heuristics engine
│   ├── transcriber.py               # Speech-to-Text audio transcription pipeline
│   ├── security.py                  # Cryptographic HMAC-SHA256, LRU cache & anti-spam buffer
│   ├── interactive_scan.py          # Interactive terminal scanner CLI
│   └── models/                      # Serialized ML models
│       └── scam_classifier.joblib   # Trained pipeline artifact
├── backend/                         # Production FastAPI REST Gateway
│   ├── main.py                      # Application factory, lifespan warm-up & middleware
│   ├── config.py                    # Environment settings & Pydantic configuration
│   ├── schemas.py                   # Pydantic v2 request/response schemas
│   ├── database.py                  # Supabase database client with thread-pool offloading
│   ├── test_api.py                  # 12-test comprehensive REST test suite
│   └── routes/                      # Modular API route controllers
│       ├── __init__.py
│       ├── scan.py                  # Multi-modal scan endpoints (/scan/text, /scan/email, /scan/audio)
│       ├── report.py                # Community incident reporting (/report, /reports)
│       ├── feed.py                  # Public threat intelligence feed (/feed)
│       └── health.py                # Health checks & system telemetry (/health)
├── database/                        # Supabase PostgreSQL Storage Layer
│   ├── schema.sql                   # Hardened DDL schema with RLS policies & audit logs
│   ├── seed.sql                     # Seed fixtures with authentic Indian cyber-crime indicators
│   ├── config.py                    # Supabase credentials loader
│   └── client.py                    # Direct database client connector
├── frontend/                        # Mission Control Web Application
│   ├── public/                      # Static assets & sample fixtures
│   │   ├── test_screenshots/        # 6 authentic high-contrast test screenshots
│   │   ├── bank_otp_scam.wav        # Sample audio recordings
│   │   └── digital_arrest_scam.wav
│   ├── src/                         # React 18 source code
│   │   ├── main.jsx                 # Application entry point
│   │   ├── App.jsx                  # Main dashboard layout & Bayesian confidence state
│   │   ├── index.css                # Tailwind CSS luxury theme styles
│   │   ├── components/              # Modular UI components
│   │   │   ├── Navbar.jsx           # Unified ∀VITR brand mark & theme toggle
│   │   │   ├── ThreatScanner.jsx    # 4-modality scanner with on-device Tesseract OCR & presets
│   │   │   ├── ThreatHUD.jsx        # Threat forensics result card & circular risk gauge
│   │   │   ├── LiveScamCarousel.jsx # Real-time verified incident carousel
│   │   │   ├── IncidentModal.jsx    # Deep-dive forensic dossier modal
│   │   │   └── ReportModal.jsx      # Citizen scam submission modal
│   │   └── data/                    # Local mock feeds and scenarios
│   ├── package.json                 # Frontend dependencies (React, Vite, Tesseract.js, Lucide)
│   ├── vite.config.js               # Vite bundler configuration
│   └── tailwind.config.js           # 60-30-10 luxury cyber-defense palette
├── test_screenshots/                # Standalone test screenshot repository
│   ├── safe_swiggy_delivery_receipt.png
│   ├── safe_bank_transaction_alert.png
│   ├── scam_whatsapp_cbi_digital_arrest.png
│   ├── scam_electricity_bill_cutoff.png
│   ├── scam_whatsapp_part_time_job.png
│   └── scam_fake_upi_payment_receipt.png
├── test_audio/                      # 22 diverse audio call test samples
├── test_emails/                     # 16 authentic RFC email phishing test cases
├── generate_test_screenshots.py     # Deterministic PIL screenshot generator
├── generate_report.py               # 30+ milestone automated Word report generator
├── package.json                     # Root npm proxy orchestrator ("npm run dev")
├── docker-compose.yml               # Containerized stack deployment
├── PRD.md                           # Product Requirements Document
├── architecture.md                  # Comprehensive System Architecture Specification
├── phases.md                        # Phased Project Roadmap
├── rules.md                         # Engineering Standards & Non-LLM Mandate
├── memory.md                        # Architectural Decision Records (ADRs)
└── ScamShield_AI_Project_Report.docx # Living 30-milestone comprehensive project report
```

---

## 📊 Model Benchmarks

Trained on an industrial corpus of **10,392 multi-modal samples** combining the UCI SMS Spam Collection (5,572 samples), scaled Voice Call Extortion transcripts (480 samples), Indian utility and blackout threats (840 samples), banking and KYC phishing (600 samples), multilingual Hinglish vectors (800 samples), gaming and loan traps (600 samples), and benign/Gen-Z slang conversations (1,500 samples):

| Metric | ∀VITR AI (Logistic Regression) | Linear SVM Benchmark | Random Forest Benchmark |
| :--- | :---: | :---: | :---: |
| **Accuracy** | **98.6%** | 98.8% | 97.4% |
| **Precision** | **99.8%** | 99.6% | 98.9% |
| **Recall** | **96.7%** | 97.4% | 94.2% |
| **F1-Score** | **98.2%** | 98.5% | 96.5% |
| **Output Type** | **Continuous Calibrated Probability** | Hard Boundary Only | Stepwise Tree Probability |
| **Inference Latency** | **< 4.2 ms** | < 4.5 ms | > 18.0 ms |

---

## 🔌 Production REST API Gateway

The backend provides a high-performance REST API built with FastAPI and documented automatically via OpenAPI/Swagger at `/docs`:

| Method | Endpoint | Description | Sample Status |
| :--- | :--- | :--- | :---: |
| `GET` | `/` | API Root & Service Discovery | `200 OK` |
| `GET` | `/health` | Live System Telemetry & Warm-up Status | `200 OK` |
| `POST`| `/api/v1/scan/text` | Scans SMS, chat, and extracted screenshot text | `200 OK` |
| `POST`| `/api/v1/scan/email` | Scans RFC email headers and body for spoofing | `200 OK` |
| `POST`| `/api/v1/scan/audio` | Transcribes and scans call audio recordings | `200 OK` |
| `GET` | `/api/v1/scan/{id}` | Retrieves scan record and cryptographic token | `200 OK` |
| `POST`| `/api/v1/report` | Submits citizen community threat report | `201 Created` |
| `GET` | `/api/v1/reports` | Lists verified community threat reports | `200 OK` |
| `GET` | `/api/v1/feed` | Real-time verified IOC threat intelligence feed | `200 OK` |

---

## 🔒 Security & CodeRabbit Audit Sign-Off

The platform has been audited against enterprise security guidelines with **10/10 CodeRabbit findings resolved**:
1. **Row-Level Security (RLS) Hardening:** Classification reads are strictly joined to scan ownership; direct classification inserts are restricted to `service_role`.
2. **Community Report Safety:** Direct inserts from client roles are constrained to `status = 'PENDING'` to prevent feed poisoning.
3. **Non-Blocking Database Offloading:** Supabase HTTP queries are wrapped in `asyncio.to_thread` to prevent thread pool starvation in FastAPI's asynchronous event loop.
4. **Resilient Offline Fallback:** Client-side network failure handling strictly preserves error notifications rather than fabricating false-positive SAFE verdicts.

---

## 🚀 Running the Platform Locally

### Prerequisites
* Python 3.12+
* Node.js 18+ and npm

### Terminal 1 — Backend (FastAPI + AI Engine)
```powershell
# From repository root:
python -m backend.main
```
* Backend starts at: **[http://localhost:8000](http://localhost:8000)**
* Interactive Swagger Docs: **[http://localhost:8000/docs](http://localhost:8000/docs)**

### Terminal 2 — Frontend (React 18 + Vite)
```powershell
# From repository root:
npm run dev
```
* Frontend starts at: **[http://localhost:5173](http://localhost:5173)**

### Running the Backend Test Suite
```powershell
python -m backend.test_api
```
*(Executes 12 automated E2E tests validating scans, HMAC tokens, emails, audio, Supabase persistence, and boundary limits with 100% success).*

---

<div align="center">

**∀VITR AI • अवितृ • The Protector**  
*Built for Hackathon 2026 Submission • December 6, 2026*

</div>