# 🏗️ System Architecture & Data Flow — ScamShield AI

**Project:** ScamShield AI  
**Author & Lead Architect:** Ayusman Mishra ([@Ayus-ProjeXion](https://github.com/Ayus-ProjeXion))  
**Target Deadline:** December 6, 2026  
**Version:** 1.1.0  

---

## 1. High-Level Architecture Topology

```
+-------------------------------------------------------------------------+
|                    React Frontend Client (Vite + Tailwind)              |
|        - Multi-Channel Scan Input (SMS, URL, Email, Call Transcript)    |
|        - Dynamic Threat Severity Meter (Safe, Moderate, Critical)       |
|        - Explainable Evidence Breakdown & Community Threat Feed         |
+------------------------------------+------------------------------------+
                                     |
                                HTTPS REST
                                     v
+------------------------------------+------------------------------------+
|                      FastAPI Backend Gateway (app/main.py)              |
|        - Input Sanitization & Entity Extraction (URLs, Phones, VPAs)    |
|        - Orchestration Service: Rule Engine + ML Model Pipeline        |
+-------------------+-------------------------------+---------------------+
                    |                               |
     Deterministic  |                  Vectorized   |
     Lookup         v                  Inference    v
+-------------------+---------------+   +-----------+---------------------+
|        Deterministic Rule Engine  |   |    Scikit-Learn ML Service      |
|  - Threat IOC Lookup (Supabase)   |   | - TF-IDF Feature Extraction     |
|  - Domain Entropy & Homoglyphs    |   | - Logistic Regression Classifier|
|  - Regex Threat Heuristics        |   | - Calibrated Scam Probability   |
+-------------------+---------------+   +-----------+---------------------+
                    \                               /
                     \       Weighted Score        /
                      v      Consolidation        v
+-------------------------------------------------------------------------+
|                  Database Layer (Supabase PostgreSQL)                   |
|  - profiles                      - threat_scans                         |
|  - scam_classifications          - threat_iocs (Blacklist / Whitelist)  |
|  - community_reports             - audit_logs                           |
|  - Row-Level Security (RLS)      - High-Speed B-Tree / GIN Indexes      |
+-------------------------------------------------------------------------+
```

---

## 2. Directory Structure Contract

```text
ScamShield-Ai/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ThreatScanner.jsx
│   │   │   ├── RiskGauge.jsx
│   │   │   ├── ThreatFeed.jsx
│   │   │   └── EvidenceCard.jsx
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── vite.config.js
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── scan.py
│   │   │   ├── reports.py
│   │   │   └── health.py
│   │   ├── services/
│   │   │   ├── rule_engine.py
│   │   │   ├── ml_classifier.py
│   │   │   ├── external_api.py
│   │   │   └── supabase_client.py
│   │   ├── models/
│   │   │   └── ml_model.pkl
│   │   └── schemas/
│   │       ├── scan_schema.py
│   │       └── report_schema.py
│   └── requirements.txt
├── database/
│   ├── schema.sql
│   └── seed.sql
├── PRD.md
├── architecture.md
├── rules.md
├── phases.md
├── design.md
├── memory.md
└── ScamShield_AI_Project_Report.docx
```
