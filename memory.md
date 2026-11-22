# 🧠 Project Memory & Architectural Decision Log (ADR) — ScamShield AI

**Project:** ScamShield AI  
**Author & Lead Architect:** Ayusman Mishra ([@Ayus-ProjeXion](https://github.com/Ayus-ProjeXion))  
**Last Updated:** November 22, 2026  

---

## 1. Project Inception & Hackathon Context

* **Genesis:** ScamShield AI was initiated during the hackathon cycle as a rapid-response, multi-modal scam prevention system.
* **Leadership & Team Allocation:**
  - Led by Ayusman Mishra (@Ayus-ProjeXion) as Lead Architect & Database Engineer.
  - 4 specialized team members covering Database, Backend, Frontend, and AI Detection.
* **Previous Project Preservation:**
  - `smart-campus-ai` was cleanly saved, committed, and synced to `origin/main`.
  - Development actively pivots to `ScamShield-Ai` under `C:\Users\HP\OneDrive\Desktop\ScamShield-Ai`.

---

## 2. Architectural Decisions Log (ADR)

### ADR-001: Start with Database Schema (Supabase PostgreSQL)
* **Decision:** Build and deploy the database schema on branch `database` prior to backend API or frontend development.
* **Rationale:** The database acts as the immutable data contract. Establishing tables, enums, and foreign keys first unblocks all 4 team members simultaneously and prevents breaking schema changes later.

### ADR-002: Dual-Engine Threat Detection (Deterministic + AI)
* **Decision:** Decouple instantaneous heuristic/IOC matching from LLM-based linguistic analysis.
* **Rationale:** LLMs are prone to latency and hallucinations. Known phishing domains and blacklisted UPI IDs must be flagged instantly in $< 50\text{ ms}$ with 100% deterministic accuracy. AI is reserved for novel, zero-day social engineering text.

### ADR-003: Supabase as Central Managed Backend
* **Decision:** Adopt Supabase for managed PostgreSQL, Row-Level Security (RLS), real-time change events, and built-in auth integration.
* **Rationale:** Maximizes hackathon velocity without sacrificing production-grade SQL standards, indexing, or ACID guarantees.

### ADR-004: Automated Living Project Report (.docx)
* **Decision:** Maintain `ScamShield_AI_Project_Report.docx` via `generate_report.py`, automatically updated at every engineering step.
* **Rationale:** Ensures hackathon submission deliverables and project reports are ready on demand without manual last-minute assembly.

---

## 3. Current Session State & Immediate Next Action

* **Current Status:**
  - Git branches created and pushed to GitHub (`main`, `database`, `backend`, `frontend`, `ai-engine`).
  - Active branch switched to `database`.
  - Spec-Driven Development (SDD) suite synchronized (`PRD.md`, `architecture.md`, `rules.md`, `phases.md`, `design.md`, `memory.md`).
* **Next Immediate Action:**
  - Create `database/schema.sql` (Supabase migration script) and `database/seed.sql`.
  - Re-generate `ScamShield_AI_Project_Report.docx` with updated architecture and schema specifications.
