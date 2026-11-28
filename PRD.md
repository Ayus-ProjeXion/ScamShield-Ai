# 📋 Product Requirements Document (PRD) — ∀VITR AI (अवितृ • The Protector)

**Project:** ∀VITR AI (formerly ScamShield AI)  
**Author & Lead Architect:** Ayusman Mishra ([@Ayus-ProjeXion](https://github.com/Ayus-ProjeXion))  
**Target Submission Deadline:** December 6, 2026  
**Core Stack:** React 18 + Vite 5 + Tailwind CSS | Python 3.12 FastAPI | Scikit-Learn ML | Tesseract.js WASM | Whisper STT | Supabase PostgreSQL  
**Version:** 2.0.0  
**Effective Date:** November 26, 2026  

---

## 1. Executive Summary & Core Objective

**∀VITR AI** (derived from the Sanskrit **अवितृ**, meaning *"The Protector"* or *"Defender"*) is an ultra-fast, multi-modal scam detection and threat intelligence platform built to protect citizens, enterprises, and financial systems from fraudulent SMS (smishing), phishing RFC emails, fraudulent voice calls, and scam screenshots.

To ensure **absolute determinism, zero hallucinations, sub-5ms inference, and guaranteed delivery by December 6, 2026**, the system strictly utilizes:
1. **Classical Machine Learning:** TF-IDF n-gram feature extraction with calibrated Logistic Regression trained on an industrial corpus of 10,392 multi-modal samples.
2. **Audio Voice Call Detection (OpenAI Whisper):** Automatic Speech-to-Text (STT) transcribing call audio to detect live voice fraud, digital arrest extortion, and law enforcement impersonation.
3. **Client-Side Zero-Knowledge Screenshot OCR (Tesseract.js WASM):** Fully browser-contained text extraction with native `Ctrl + V` clipboard paste, ensuring 0 bytes of sensitive user images leave the client (DPDP Act 2023 compliance).
4. **RFC Email Header & Webmail Spoofing Parser:** Deep RFC 822 analysis detecting domain spoofing, free webmail impersonation (`@gmail.com` claiming to be Tax/Police), and business email compromise (BEC).
5. **Deterministic Heuristic Threat Matrix:** 13-vector security matrix incorporating the **Bharatiya Nagarik Suraksha Sanhita (BNSS 2023)** to flag fabricated police warrants, utility blackouts, and peer UPI extortion.
6. **Relational Database Warehouse:** Supabase PostgreSQL 15+ with hardened Row-Level Security (RLS) policies and non-blocking `asyncio.to_thread` event loop integration.
7. **Architectural Guardrail:** Strictly avoids Generative AI / LLM APIs in the critical inference path to prevent hallucinations, high latency, and cloud API dependencies.

---

## 2. 4-Member Team Ownership Matrix

| Member | Workstream | Git Branch | Core Tech Stack | Primary Responsibilities |
| :--- | :--- | :--- | :--- | :--- |
| **Member 1** | Frontend UI & OCR | `frontend` | React 18, Vite, Tailwind CSS, Tesseract.js | 4-modality scanner dashboard, on-device OCR, circular risk gauge, live feed carousel, report modal |
| **Member 2** | Backend API Gateway | `backend` | FastAPI, Uvicorn, Python-Multipart | REST endpoints (`/scan/text`, `/scan/email`, `/scan/audio`, `/report`, `/feed`), Whisper orchestration |
| **Member 3** | ML & Detection Engine | `ai-engine` | Scikit-learn, Whisper STT, Pandas | TF-IDF vectorizer, Logistic Regression model, 13-vector deterministic security heuristics engine |
| **Member 4** | Database & Integration (Lead) | `database` | Supabase PostgreSQL, SQL DDL | Schema migrations, RLS hardening, call scan indexing, seed fixtures, external security APIs, E2E tests |

---

## 3. Core Functional Requirements (FR)

### FR-01: Multi-Channel Threat Scanning
* **SMS & Messaging:** Direct text paste scanning for smishing, lottery, and job scam patterns.
* **RFC Email (.eml):** Header analysis for free webmail authority spoofing, executive BEC, and tax phishing.
* **Voice Call Recordings (Whisper STT):** Accepts uploaded audio (`.mp3`, `.wav`) or microphone recording, transcribes speech with Whisper, and classifies fraud indicators.
* **Screenshot & Image OCR (Tesseract.js WASM):** 100% on-device text extraction from WhatsApp chats, fake payment receipts, electricity cutoff notices, and FIR letters.

### FR-02: Zero-Knowledge Client-Side OCR Execution
* Direct `Ctrl + V` clipboard paste listener anywhere in the dashboard.
* In-browser WebAssembly execution via `tesseract.js` worker threads.
* Complete image isolation: raw screenshot bytes never touch any remote server, preserving user confidentiality under the Digital Personal Data Protection (DPDP) Act 2023.

### FR-03: Audio Call Scam Analysis Pipeline (Whisper)
* Ingestion of audio recording via `POST /api/v1/scan/audio`.
* Fast transcription using OpenAI Whisper (`base` / `tiny` model).
* NLP analysis of transcribed dialogue:
  - Caller authority impersonation cues (*"I am calling from CBI / Customs / Police / Bank fraud unit"*).
  - High-pressure extortion words (*"Digital arrest"*, *"Drug parcel intercepted"*, *"Immediate fund transfer"*).
  - OTP and sensitive credential requests.
* Output: Full transcript, overall call risk score, and recommended defensive actions.

### FR-04: Machine Learning Scam Probability
* Text and audio transcripts processed through TF-IDF into Logistic Regression classifier returning $P(\text{scam}) \in [0.0, 1.0]$.
* Continuous probability output driving animated glowing UI risk meters without post-hoc Platt scaling overhead.

### FR-05: 13-Vector Deterministic Threat Matrix
* Grounded in 13 deterministic security categories:
  1. Credential Harvesting (OTP/PIN/CVV)
  2. UPI PIN Extraction Cashback Traps
  3. Digital Arrest Extortion (BNSS 2023)
  4. Utility & Electricity Blackouts
  5. Banking KYC & Account Suspension
  6. Predatory Loan APKs & Malware
  7. Youth Gaming Bait (BGMI UC / Free Fire Diamonds)
  8. Unsolicited Part-Time Job / Task Scams
  9. Lottery & KBC Lucky Draw Fraud
  10. Government Tax Refund Phishing Lures
  11. Video Call Sextortion & Defamation Blackmail
  12. Direct Peer-to-Peer VPAs & Untrusted TLDs
  12B. Courier & Customs Extortion (Receipt-Aware Context)
  13. Regional Hinglish Coercion Triggers

### FR-06: Cryptographic Anti-Tampering Engine
* Emits a 256-bit **HMAC-SHA256 signature** with a random cryptographic nonce and UNIX timestamp for every scan.
* Protects forensic integrity against man-in-the-middle proxy alteration on public networks.

### FR-07: 1-Click Police & 1930 Helpline Complaint Formatter
* Automatically drafts formal legal complaint text tailored for immediate submission to the **National Cyber Crime Reporting Portal (1930 / cybercrime.gov.in)** and DoT's **Chakshu Portal**.

### FR-08: In-Memory Threat Caching & Anti-Spam Buffer
* **LRU Threat Cache:** In-memory SHA-256 hash lookup serving duplicate viral scam messages in `< 0.1 ms`.
* **Anti-Spam Sliding Buffer:** Protects the inference engine from automated bot floods and denial-of-service degradation.

### FR-09: Crowdsourced Telemetry Feed
* Community reporting mechanism stored in Supabase `community_reports` to warn users of ongoing regional scam calls and malicious numbers.
* RLS policies constrain client submissions to `status = 'PENDING'` to prevent feed poisoning.

### FR-10: WhatsApp Cyber Shield (Zero-Download Verification Gateway)
* Direct message forwarding to verified ∀VITR AI WhatsApp Helpline (`+91 91193 01930`).
* Real-time automated reply with threat breakdown, risk percentage, and 1-tap **1930 Cyber Crime Helpline** linkage.
* Twilio TwiML and Meta Graph API compatible webhook endpoint (`/api/v1/webhook/whatsapp`).
* 0 MB download footprint for 500 million citizens across all devices.
