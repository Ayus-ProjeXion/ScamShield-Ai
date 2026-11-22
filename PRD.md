# 📋 Product Requirements Document (PRD) — ScamShield AI

**Project:** ScamShield AI  
**Author & Lead Architect:** Ayusman Mishra ([@Ayus-ProjeXion](https://github.com/Ayus-ProjeXion))  
**Team:** 4 Members (Frontend, Backend, ML/Rule Engine, Database/Integration)  
**Target Submission Deadline:** December 6, 2026  
**Core Stack:** React + Tailwind CSS | Python FastAPI | Scikit-Learn ML | Whisper STT | Supabase PostgreSQL  
**Version:** 1.2.0  
**Effective Date:** November 22, 2026  

---

## 1. Executive Summary & Core Objective

ScamShield AI is an ultra-fast, multi-channel scam detection and threat intelligence platform built to protect users from fraudulent SMS (smishing), phishing URLs, **fraudulent voice calls**, and deceptive payment requests. 

To ensure **absolute determinism, zero hallucinations, real-time response, and guaranteed delivery by December 6, 2026**, the system strictly utilizes:
1. **Classical Machine Learning:** TF-IDF feature extraction with calibrated Logistic Regression.
2. **Audio Voice Call Detection (OpenAI Whisper):** Automatic Speech-to-Text (STT) transcribing call audio to detect live voice fraud, extortion, and impersonation.
3. **Deterministic Heuristic Rules:** Regex patterns, homoglyph domain detection, urgency linguistic cues, and known blacklist lookups.
4. **External Security APIs:** Real-time URL reputation and domain verification feeds.
5. **Relational Database Warehouse:** Supabase PostgreSQL 15+ with Row-Level Security (RLS).
6. **Architectural Guardrail:** Avoids heavy Generative AI / LLM APIs in the critical inference path to prevent hallucinations, high latency, and cloud costs.

---

## 2. 4-Member Team Ownership Matrix

| Member | Workstream | Git Branch | Core Tech Stack | Primary Responsibilities |
| :--- | :--- | :--- | :--- | :--- |
| **Member 1** | Frontend UI | `frontend` | React, Vite, Tailwind CSS | Scanner dashboard, audio call uploader/recorder, urgency risk gauges, evidence cards |
| **Member 2** | Backend API Gateway | `backend` | FastAPI, Uvicorn, Python-Multipart | REST endpoints (`/scan/text`, `/scan/audio`, `/report`, `/feed`), Whisper orchestration |
| **Member 3** | ML & Detection Engine | `ai-engine` | Scikit-learn, Whisper STT, Pandas | TF-IDF vectorizer, Logistic Regression model, voice transcript feature extractor |
| **Member 4** | Database & Integration (Lead) | `database` | Supabase PostgreSQL, SQL DDL | Schema migrations, call scan indexing, seed fixtures, external security APIs, E2E tests |

---

## 3. Core MVP Functional Requirements (FR)

### FR-01: Multi-Channel Threat Scanning
* **SMS & Messaging:** Direct text paste scanning for smishing, lottery, and job scam patterns.
* **URL & Web Links:** Homoglyph detection, domain entropy, SSL verification, and blacklist checking.
* **UPI & Payment Identifiers:** Fraudulent VPA and QR code extortion checks.
* **Voice Call Recordings (Whisper STT):** Accepts uploaded audio (`.mp3`, `.wav`, `.m4a`) or microphone recording, transcribes speech with Whisper, and classifies fraud indicators.

### FR-02: Audio Call Scam Analysis Pipeline (Whisper)
* Ingestion of audio recording via `POST /api/v1/scan/audio`.
* Fast transcription using OpenAI Whisper (`base` / `tiny` model).
* NLP analysis of transcribed dialogue:
  - Caller authority impersonation cues (*"I am calling from CBI / Customs / Police / Bank fraud unit"*).
  - High-pressure extortion words (*"Digital arrest"*, *"Drug parcel intercepted"*, *"Immediate fund transfer"*).
  - OTP and sensitive credential requests.
* Output: Full transcript with timestamped flagged sentences, overall call risk score, and recommended defensive actions.

### FR-03: Machine Learning Scam Probability
* Text and audio transcripts processed through TF-IDF into Logistic Regression classifier returning $P(\text{scam}) \in [0.0, 1.0]$.

### FR-04: Transparent Evidence-Grounded Explanation
* Detailed breakdown chips (`[Authority Impersonation]`, `[Digital Arrest Threat]`, `[Urgency Framing]`) explaining *why* the interaction was flagged.

### FR-05: Crowdsourced Telemetry Feed
* Community reporting mechanism stored in Supabase `community_reports` to warn users of ongoing regional scam calls and malicious numbers.
