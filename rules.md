# 📜 Engineering Rules & Operational Guardrails — ScamShield AI

**Project:** ScamShield AI  
**Author & Lead Architect:** Ayusman Mishra ([@Ayus-ProjeXion](https://github.com/Ayus-ProjeXion))  
**Target Deadline:** December 6, 2026  
**Status:** Mandatory Across All 4 Team Members  

---

## 1. Git & Sacred Trunk Discipline

* **Rule 1.1: Sacred Trunk (`main`)**
  - Direct pushes to `main` are strictly prohibited during active feature development.
  - `main` must at all times remain clean, runnable, and presentation-ready.
* **Rule 1.2: Feature Branches (4-Member Standard)**
  - Member 1 (Frontend): `frontend`
  - Member 2 (Backend): `backend`
  - Member 3 (ML & Rules): `ai-engine`
  - Member 4 (Database & Integration): `database`

---

## 2. Model & Threat Detection Guardrails

* **Rule 2.1: Strictly Non-LLM Architecture**
  - No large language models (LLMs) or generative AI APIs (OpenAI, Claude, Gemini) are used in the core inference path.
  - Reasoning: Eliminates latency ($> 2\text{s}$), eliminates token costs, and guarantees 0% hallucination rate on threat assessments.
* **Rule 2.2: Dual Verification (ML + Rules)**
  - ML inference (TF-IDF + Logistic Regression) is combined with deterministic heuristic rules.
  - Known blacklisted IOCs immediately trigger `CRITICAL` threat classification, bypassing probabilistic scores.
* **Rule 2.3: Explainability Mandate**
  - Every flagged item must output distinct reason badges (e.g. `[Electricity Cutoff Pattern]`, `[Known Phishing Domain]`, `[High Urgency Tone]`).

---

## 3. Database & Credential Hygiene

* **Rule 3.1: Zero Client-Side Secrets**
  - Never put Supabase service-role keys or database passwords in frontend code.
* **Rule 3.2: Automated Project Report**
  - Maintain `ScamShield_AI_Project_Report.docx` via `generate_report.py`, automatically synchronized at every milestone.
