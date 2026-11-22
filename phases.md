# 🗺️ Phased Implementation Roadmap — ScamShield AI

**Project:** ScamShield AI  
**Author & Lead Architect:** Ayusman Mishra ([@Ayus-ProjeXion](https://github.com/Ayus-ProjeXion))  
**Team Structure:** 4 Dedicated Workstreams  
**Last Updated:** November 22, 2026  

---

## Overview

The hackathon execution is organized into 5 progressive phases designed to enable parallel execution across all 4 team members while maintaining zero merge conflicts.

---

## Phase 1: Database Foundation & Threat Store (Current Phase)
* **Lead:** Ayusman Mishra (Lead Architect)
* **Branch:** `database`
* **Key Deliverables:**
  - [x] Configure Supabase PostgreSQL relational schema (`schema.sql`).
  - [x] Create custom ENUM types (`threat_severity`, `scam_category`, `scan_channel`, `verification_status`).
  - [x] Build core tables: `profiles`, `threat_scans`, `scam_classifications`, `threat_iocs`, `community_reports`, `audit_logs`.
  - [x] Implement Row-Level Security (RLS) policies.
  - [x] Establish seed mock data (`seed.sql`) containing realistic phishing URLs, smishing SMS, and fake UPI records.
  - [x] Update Word project report (`ScamShield_AI_Project_Report.docx`).

---

## Phase 2: Backend API Gateway & Heuristic Engine
* **Branch:** `backend`
* **Key Deliverables:**
  - [ ] Scaffold FastAPI backend microservice.
  - [ ] Implement Supabase client wrapper with environment variable isolation.
  - [ ] Build deterministic regex and domain entropy calculation pipelines.
  - [ ] Implement REST endpoints:
    - `POST /api/v1/scan` (Analyze input and return threat evaluation)
    - `GET /api/v1/scans/{id}` (Retrieve scan details and explanation)
    - `POST /api/v1/report` (Submit community scam report)
    - `GET /api/v1/feed` (Fetch latest verified threat intelligence feed)

---

## Phase 3: AI Multi-Modal Detection Engine (Completed on `ai-engine`)
* **Branch:** `ai-engine`
* **Lead:** Ayusman Mishra (Lead Architect)
* **Key Deliverables:**
  - [x] Ingest and aggregate 5,607 multi-source training samples:
    - [x] UCI SMS Spam Collection (5,574 samples)
    - [x] Indian High-Risk Cyber-Fraud Corpus (Electricity blackout, fake KYC, lottery, fake UPI)
    - [x] Voice Call Scam Audio Transcripts (CBI / Mumbai Police extortion, customs seizure)
  - [x] Train TF-IDF + Calibrated Logistic Regression model pipeline ($98.7\%$ Accuracy, $95.4\%$ Precision/Recall).
  - [x] Build benchmark comparison against Linear SVM for hackathon judges presentation.
  - [x] Develop deterministic security heuristic rule engine (Urgency, Authority Impersonation, Suspicious URLs & VPAs).
  - [x] Implement OpenAI Whisper STT voice call audio transcriber with local SpeechRecognition fallback.
  - [x] Build unified `ScamDetector` combining ML probability with deterministic badge attribution ($< 5\text{ ms}$ inference).

---

## Phase 4: Frontend Mission Control Dashboard
* **Branch:** `frontend`
* **Key Deliverables:**
  - [ ] Develop dark glassmorphism web interface with Cyberpunk Mission Control aesthetic.
  - [ ] Build interactive Multi-Vector Scanner (Tabs: URL, SMS, UPI ID, Phone Number).
  - [ ] Dynamic Risk Meter (animated gauge with glowing color transitions).
  - [ ] Threat Breakdown Breakdown Card (visual indicators for domain age, urgency score, SSL status).
  - [ ] Live Crowdsourced Threat Feed & Reporting Modal.

---

## Phase 5: Integration, Code Review & Presentation
* **Branch:** `main`
* **Key Deliverables:**
  - [ ] Cross-branch integration tests.
  - [ ] CodeRabbit review on Pull Requests.
  - [ ] Final compilation of `ScamShield_AI_Project_Report.docx`.
  - [ ] Preparation of 6-Slide Executive Pitch Deck.
