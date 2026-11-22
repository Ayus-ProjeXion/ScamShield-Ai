# 🏗️ System Architecture & Data Flow — ScamShield AI

**Project:** ScamShield AI  
**Author & Lead Architect:** Ayusman Mishra ([@Ayus-ProjeXion](https://github.com/Ayus-ProjeXion))  
**Target Deadline:** December 6, 2026  
**Version:** 1.2.0  

---

## 1. High-Level Architecture Topology

```
+-----------------------------------------------------------------------------------+
|                        React Frontend Client (Vite + Tailwind)                    |
|  - Text Scanner Tab (SMS, Email, WhatsApp)                                        |
|  - URL Scanner Tab (Homoglyphs, Lookalike domains)                                |
|  - Voice Call Scanner Tab (Audio File Upload / Mic Recording for Whisper STT)     |
|  - Dynamic Threat Severity Meter (Safe, Moderate, Critical)                       |
|  - Evidence Breakdown & Live Community Threat Feed                                |
+-----------------------------------------+-----------------------------------------+
                                          |
                                     HTTPS REST
                                          v
+-----------------------------------------+-----------------------------------------+
|                          FastAPI Backend API Gateway                              |
|  - Input Validation & Normalization         - Rate Limiting & Proxy Protection    |
|  - Audio Ingestion & File Preprocessing     - Pipeline Orchestration              |
+-------------------+---------------------+--------------------+--------------------+
                    |                     |                    |
        Audio Call  |       Deterministic |         Vectorized |
        Payload     v       Lookup        v         Inference  v
+-------------------+---+ +---------------+----+ +-------------+--------------------+
|   Whisper STT Engine  | | Rule Heuristics    | |  Scikit-Learn ML Service        |
| - OpenAI Whisper STT  | | - Blacklist IOCs   | | - TF-IDF Vectorizer             |
| - Audio Transcription | | - RegEx Urgency    | | - Logistic Regression Classifier |
| - Speech Timestamps   | | - Homoglyph Check  | | - Calibrated Scam Probability    |
+-------------------+---+ +---------------+----+ +-------------+--------------------+
                    \                     |                    /
                     \                    |                   /
                      v                   v                  v
+-----------------------------------------------------------------------------------+
|                     Threat Consolidation & Explanation Engine                     |
|  - Computes Unified Risk Score (0 - 100)                                          |
|  - Identifies Triggered Evidence Chips & Psychological Manipulation Cues         |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                      Database Layer (Supabase PostgreSQL)                         |
|  - profiles                         - threat_scans (Text & Audio Call Transcripts)|
|  - scam_classifications             - threat_iocs (Blacklist / Whitelist)         |
|  - community_reports                - audit_logs                                  |
|  - Row-Level Security (RLS)         - High-Speed B-Tree / GIN Indexes             |
+-----------------------------------------------------------------------------------+
```

---

## 2. Voice Call Scam Analysis Flow (Whisper Pipeline)

```
[User Uploads Call Audio (.mp3/.wav)]
               │
               ▼
[POST /api/v1/scan/audio (FastAPI)]
               │
               ▼
[OpenAI Whisper Engine (STT)]
               │
               ├──▶ Transcribes audio to text dialogue
               └──▶ Extracts speech duration & key phrases
               │
               ▼
[ScamShield Analysis Pipeline]
               │
               ├──▶ Heuristic Rule Engine: Detects "CBI", "Customs", "Digital Arrest", "OTP"
               └──▶ Scikit-Learn Model: Predicts fraud likelihood from transcript
               │
               ▼
[Supabase Storage & Logging]
               │
               ├──▶ Writes scan record to public.threat_scans (channel='CALL')
               └──▶ Writes classification & evidence to public.scam_classifications
               │
               ▼
[Frontend Response]
  - Full Transcript with flagged manipulation phrases
  - Overall Threat Gauge (e.g. 94% Critical Scam)
  - Defensive Guidance ("Hang up immediately. Government agencies never demand money over phone.")
```
