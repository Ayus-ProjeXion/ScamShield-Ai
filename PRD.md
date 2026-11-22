# 📋 Product Requirements Document (PRD) — ScamShield AI

**Project:** ScamShield AI  
**Author & Lead Architect:** Ayusman Mishra ([@Ayus-ProjeXion](https://github.com/Ayus-ProjeXion))  
**Team:** 4 Members (Frontend, Backend, ML/Rule Engine, Database/Integration)  
**Target Submission Deadline:** December 6, 2026  
**Core Stack:** React + Tailwind CSS | Python FastAPI | Scikit-Learn (TF-IDF + Logistic Regression) | Supabase PostgreSQL  
**Version:** 1.1.0  
**Effective Date:** November 22, 2026  

---

## 1. Executive Summary & Core Objective

ScamShield AI is an ultra-fast, multi-channel scam detection and threat intelligence platform built to protect users from fraudulent SMS (smishing), phishing URLs, call transcripts, and deceptive payment requests. 

To ensure **absolute determinism, zero hallucinations, millisecond latency ($< 50\text{ ms}$), and guaranteed delivery by December 6, 2026**, the system strictly utilizes:
1. **Classical Machine Learning:** TF-IDF feature extraction with calibrated Logistic Regression.
2. **Deterministic Heuristic Rules:** Regex patterns, homoglyph domain detection, urgency linguistic cues, and known blacklist lookups.
3. **External Security APIs:** Real-time URL reputation and domain verification feeds.
4. **Relational Database Warehouse:** Supabase PostgreSQL 15+ with Row-Level Security (RLS).
5. **Architectural Guardrail:** Strictly avoids heavy Generative AI / Large Language Models (LLMs) to eliminate latency, unpredictable hallucinations, and cloud inference cost.

---

## 2. 4-Member Team Ownership Matrix

| Member | Workstream | Git Branch | Core Tech Stack | Primary Responsibilities |
| :--- | :--- | :--- | :--- | :--- |
| **Member 1** | Frontend UI | `frontend` | React, Vite, Tailwind CSS | Scanner dashboard, urgency risk meters, threat alert cards, crowdsourced report UI |
| **Member 2** | Backend API Gateway | `backend` | FastAPI, Uvicorn, Pydantic | REST endpoints (`/scan`, `/report`, `/feed`, `/health`), CORS, validation |
| **Member 3** | ML & Rule Engine | `ai-engine` | Scikit-learn, Pandas, NumPy | TF-IDF vectorizer, Logistic Regression model, deterministic regex & rule evaluators |
| **Member 4** | Database & Integration | `database` | Supabase PostgreSQL, SQL DDL | Schema migrations, RLS policies, seed fixtures, external URL reputation APIs, E2E tests |

---

## 3. Functional Requirements (FR)

* **FR-01: Multi-Channel Threat Scanning**
  - Accept SMS text, email snippets, call transcripts, raw URLs, and UPI handles via `POST /api/v1/scan`.
* **FR-02: Instant Rule-Based Filtering**
  - Evaluate known phishing keywords ("urgent account suspension", "KYC update required", "lottery prize claimed", "electricity cutoff").
  - Check extracted domains against Supabase `threat_iocs` blacklist and whitelist.
* **FR-03: Machine Learning Scam Probability**
  - Text processed through pre-trained TF-IDF vectorizer into Logistic Regression classifier returning probability $P(\text{scam}) \in [0.0, 1.0]$.
* **FR-04: Explainable Scoring**
  - Output composite risk score (0–100) and explicit, verifiable reasons (e.g. `["High urgency language", "Unregistered top-level domain", "Matches electricity bill scam pattern"]`).
* **FR-05: Crowdsourced Telemetry Feed**
  - Read community reports from Supabase `community_reports` and display live verified threat warnings.

---

## 4. Key Performance Targets
* **End-to-End Latency:** $< 60\text{ ms}$ per scan request.
* **Accuracy:** $> 95\%$ precision on SMS/Phishing benchmark datasets.
* **Uptime:** Zero dependency on paid third-party LLM rate-limits or token quotas.
