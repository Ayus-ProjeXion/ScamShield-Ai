# 🏗️ System Architecture & Data Flow — ScamShield AI

**Project:** ScamShield AI  
**Author & Lead Architect:** Ayusman Mishra ([@Ayus-ProjeXion](https://github.com/Ayus-ProjeXion))  
**Database:** Supabase (PostgreSQL 15+)  
**Version:** 1.0.0  

---

## 1. High-Level Architecture Topology

```
+-------------------------------------------------------------------------+
|                         Frontend Client (UI)                            |
|        Mission Control Dashboard / Real-Time Scanner Simulator          |
|                 (Dark Glassmorphism UI / Vite / HTML5)                  |
+------------------------------------+------------------------------------+
                                     |
                                HTTPS REST
                                     v
+------------------------------------+------------------------------------+
|                      Backend API Gateway (FastAPI)                      |
|  - Rate Limiter & Sanitize Input     - Token Authentication             |
|  - Threat Orchestrator               - Community Report Router          |
+-------------------+-------------------------------+---------------------+
                    |                               |
       Direct Query |                  Async Queue  |
                    v                               v
+-------------------+-------------------+   +-------+---------------------+
|        Deterministic Engine           |   |       AI Engine Worker      |
|  - Known IOC Matching (Blacklist/White)|  | - NLP Intent & Urgency      |
|  - Domain Entropy & Homoglyphs        |   | - Zero-Shot Categorization  |
|  - Regex Threat Signatures            |   | - Confidence Calibrator     |
+-------------------+-------------------+   +-------+---------------------+
                    \                               /
                     \                             /
                      v                           v
+-------------------------------------------------------------------------+
|                  Database Layer (Supabase PostgreSQL)                   |
|  - profiles                      - threat_scans                         |
|  - scam_classifications          - threat_iocs (Blacklist/Whitelist)    |
|  - community_reports             - audit_logs                           |
|  - Row-Level Security (RLS)      - GIN / B-Tree High Speed Indexes     |
+-------------------------------------------------------------------------+
```

---

## 2. Layer Responsibilities & 4-Member Workstream

1. **Database Layer (Lead: Ayusman | Branch: `database`):**
   - Supabase project configuration, migration scripts (`schema.sql`), triggers, RLS policies, and seed data.
2. **Backend API Layer (Branch: `backend`):**
   - RESTful API gateway, input normalization, Supabase client integration, and proxy protection for internal services.
3. **AI / Detection Engine (Branch: `ai-engine`):**
   - Heuristic feature extractor, embedding pipelines, LLM prompt engineering with JSON schema validation, and confidence calibration.
4. **Frontend Experience (Branch: `frontend`):**
   - Cyberpunk/Dark Glassmorphism dashboard, risk score visualizers, interactive multi-channel scanner, and live community report feed.

---

## 3. Data Flow Lifecycle

```
[User Input: SMS / URL / UPI]
           │
           ▼
[Backend /api/v1/scan] ──▶ [Deterministic Check in Supabase threat_iocs]
           │                       │
           │                       ├─▶ Match Found: Instant Response (< 50ms)
           │                       │   (Cached Critical Threat / Whitelisted Safe)
           ▼                       │
[No Instant Match] ◀───────────────┘
           │
           ▼
[AI Feature Extraction & Classification Pipeline]
           │
           ▼
[Consolidated Score: Deterministic + AI Probability]
           │
           ▼
[Write to Supabase: threat_scans & scam_classifications]
           │
           ▼
[Return Formatted Threat Assessment to Frontend]
```

---

## 4. Security & Compliance Posture

* **Row Level Security (RLS):** All Supabase tables enforce granular access controls. Authenticated users can only view their own scan history; public feeds expose only aggregated threat telemetry.
* **Environment Isolation:** `.env` files hold Supabase `SUPABASE_URL` and `SUPABASE_ANON_KEY` for client/read queries, and `SUPABASE_SERVICE_ROLE_KEY` strictly inside backend proxy containers.
