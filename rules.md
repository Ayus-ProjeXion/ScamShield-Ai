# 📜 Engineering Rules & Operational Guardrails — ScamShield AI

**Project:** ScamShield AI  
**Author & Lead Architect:** Ayusman Mishra ([@Ayus-ProjeXion](https://github.com/Ayus-ProjeXion))  
**Effective Date:** November 2026  
**Status:** Mandatory Across All 4 Team Members  

---

## 1. Git & Sacred Trunk Discipline

* **Rule 1.1: Sacred Trunk (`main`)**
  - Pushing directly to `main` is strictly prohibited during active feature development.
  - `main` must at all times contain clean, working, and presentation-ready code.
* **Rule 1.2: Strict Feature Branching**
  - Database schema & migrations: `database`
  - Backend API & controllers: `backend`
  - AI & detection models: `ai-engine`
  - Frontend UI & client interactions: `frontend`
* **Rule 1.3: Pull Requests & Peer Review**
  - Merges into `main` require code reviews (via CodeRabbit CLI or Lead review by Ayusman).

---

## 2. Supabase & Database Integrity

* **Rule 2.1: Contract-First Migrations**
  - No table or column may be created directly via ad-hoc dashboard clicks without an accompanying SQL migration file under `database/migrations/`.
* **Rule 2.2: Strict Typing & Enums**
  - Never store raw unvalidated strings for severity or categories. Use PostgreSQL `ENUM` types (`threat_severity`, `scam_category`, `scan_channel`).
* **Rule 2.3: Zero Client-Side Service Keys**
  - NEVER expose `SUPABASE_SERVICE_ROLE_KEY` in frontend code, HTML, or public repositories.
  - Public web clients may only access Supabase using `anon` keys protected by Row-Level Security (RLS).

---

## 3. Threat Detection Guardrails

* **Rule 3.1: Hybrid Verifications (No Pure-LLM Decisions)**
  - An LLM must NEVER be the sole decider of a threat without deterministic IOC verification.
  - Known blacklisted indicators (URLs, phone numbers, UPI VPAs) trigger immediate definitive flags.
* **Rule 3.2: Explainability by Default**
  - Every detected threat must return an actionable human explanation detailing *why* it was flagged. Opaque scores without reasons are forbidden.

---

## 4. UI/UX & Glassmorphism Standards

* **Rule 4.1: No Unstyled Elements**
  - All components must comply with the dark cyberpunk glassmorphism theme (`--bg-card`, `--border-color`, glowing hover states).
* **Rule 4.2: Visual Urgency Colors**
  - 🔴 Red (`#ef4444`): Critical Threat / Phishing / Financial Risk
  - 🟡 Amber (`#f59e0b`): Suspicious / Unverified / High Urgency Language
  - 🟢 Green (`#10b981`): Safe / Clean Domain / Verified Entity

---

## 5. Documentation & Automated Report Synchronization

* **Rule 5.1: Synchronized SDD Suite**
  - Maintain the 6 core spec blueprints: `PRD.md`, `architecture.md`, `rules.md`, `phases.md`, `design.md`, `memory.md`.
* **Rule 5.2: Word Report Maintenance**
  - As development advances, all technical decisions and progress milestones must be reflected in `ScamShield_AI_Project_Report.docx` without needing manual reminders.
