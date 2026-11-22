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
* **Rationale:**
  1. *Speed:* Real-time response time $< 50\text{ ms}$ vs $> 2000\text{ ms}$ for cloud LLMs.
  2. *Deterministic Trust:* In fraud prevention, hallucinations destroy user trust.
  3. *Cost & Resilience:* Eliminates API rate limits, paywalls, and offline degradation.
  4. *Deadline:* Allows team to finalize a rock-solid, production-grade MVP before December 6, 2026.

### ADR-003: Unified Monorepo with Clean Layer Separation
* **Decision:** House `frontend/`, `backend/`, and `database/` in a single Git repository under feature branches.
* **Rationale:** Facilitates cross-team integration tests and simplified deployment.

### ADR-004: Automated Living Project Report (.docx)
* **Decision:** Automatically update and maintain `ScamShield_AI_Project_Report.docx` via `generate_report.py` at every milestone.
* **Rationale:** The team always has a ready-to-submit project report with complete technical specifications and audit logs.
