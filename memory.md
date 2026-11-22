# 🧠 Project Memory & Architectural Decision Log (ADR) — ScamShield AI

**Project:** ScamShield AI  
**Author & Lead Architect:** Ayusman Mishra ([@Ayus-ProjeXion](https://github.com/Ayus-ProjeXion))  
**Submission Deadline:** December 6, 2026  
**Last Updated:** November 22, 2026  

---

## 1. Project Inception & Timeline Context

* **Genesis:** ScamShield AI was established for the hackathon competition with a target completion deadline of **December 6, 2026**.
* **Team Structure:** 4 dedicated members assigned to isolated feature branches:
  - Member 1: React Frontend (`frontend`)
  - Member 2: FastAPI Backend (`backend`)
  - Member 3: ML Model & Rule Engine (`ai-engine`)
  - Member 4: Database & Integration (Ayusman - Lead | `database`)

---

## 2. Architectural Decisions Log (ADR)

### ADR-001: Start with Database Schema (Supabase PostgreSQL)
* **Decision:** Build and publish the Supabase PostgreSQL relational schema on `database` first.
* **Rationale:** Establishes the immutable contract and mock seeds so Frontend, Backend, and ML engineers can develop concurrently without blocking.

### ADR-002: Exclude Generative AI / LLMs in Favor of Classical ML + Rule Engine
* **Decision:** Reject Generative AI (LLMs) in favor of Scikit-Learn (TF-IDF + Logistic Regression) coupled with deterministic rule engines.
* **Rationale:** Eliminates latency, cost, and hallucination risks; ensures predictable performance under judging conditions.

### ADR-003: OpenAI Whisper Integration for Voice Call Scam Detection
* **Decision:** Incorporate OpenAI Whisper Speech-to-Text (STT) into the backend to transcribe phone call audio recordings before downstream NLP and manipulation classification.
* **Rationale:** Fraudulent calls (FedEx parcel extortion, fake police/CBI calls, electricity cut threats) represent over 60% of financial losses in India. Adding audio call scam detection transforms ScamShield AI from a text-only tool into a comprehensive multi-modal defense system.

### ADR-004: Unified Monorepo with Clean Layer Separation
* **Decision:** House `frontend/`, `backend/`, and `database/` in a single Git repository under feature branches.
* **Rationale:** Simplifies local testing, cross-member integration, and cloud deployment.

### ADR-005: Automated Living Project Report (.docx)
* **Decision:** Automatically update and maintain `ScamShield_AI_Project_Report.docx` via `generate_report.py` at every milestone.
* **Rationale:** The team always has a ready-to-submit project report with complete technical specifications and audit logs without manual assembly.
