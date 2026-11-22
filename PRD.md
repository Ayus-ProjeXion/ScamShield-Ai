# 📋 Product Requirements Document (PRD) — ScamShield AI

**Project:** ScamShield AI  
**Author & Lead Architect:** Ayusman Mishra ([@Ayus-ProjeXion](https://github.com/Ayus-ProjeXion))  
**Team:** 4 Members (Database, Backend API, Frontend UI, AI Detection Engine)  
**Database Backend:** Supabase (PostgreSQL 15+)  
**Version:** 1.0.0  
**Effective Date:** November 22, 2026  

---

## 1. Executive Summary & Vision

ScamShield AI is an enterprise-grade, multi-modal fraud detection and threat intelligence platform designed to protect citizens, students, and organizations from the exploding epidemic of digital deception. The platform intercepts, analyzes, and explains threats across multiple vectors:
* **Phishing & Lookalike URLs:** Spoofed banking, e-commerce, and university portals.
* **Smishing & Social Messaging:** Fraudulent SMS, WhatsApp, and Telegram messages containing urgency triggers.
* **UPI & Payment Scams:** Deceptive payment requests, fake cashback links, and compromised VPA IDs.
* **Impersonation & Social Engineering:** Fraudulent job offers, fake lottery winnings, and impersonated authority figures.

---

## 2. Problem Statement & User Personas

### 2.1 The Problem
Existing spam filters are siloed, slow, and opaque. Users receive suspicious messages and have no instant, reliable way to verify legitimacy. When they do fall victim, reporting is fragmented and manual, allowing cybercriminals to exploit thousands before domain take-downs occur.

### 2.2 User Personas
1. **Everyday Consumer / Student:** Wants instant clarity on whether a text message, QR code, or link is safe before clicking or paying.
2. **Fraud Analyst / Security Admin:** Requires a central telemetry dashboard to track emerging attack patterns, verify community reports, and push IOC updates.
3. **Application Developer / Enterprise:** Integrates ScamShield via REST APIs to sanitize user-submitted links and payment IDs.

---

## 3. Core Functional Requirements (FR)

* **FR-01: Multi-Channel Threat Ingestion**
  - Accept text, URL strings, sender identifiers (phone numbers, email addresses), and UPI VPA IDs via REST endpoints.
* **FR-02: Hybrid Detection Pipeline**
  - **Deterministic Rule Engine:** Instant regex, domain entropy checks, and known-bad blacklists (zero false negatives on known threats).
  - **AI / NLP Classifier:** Multi-label classification to identify manipulation tactics, linguistic urgency, and impersonation.
* **FR-03: Supabase PostgreSQL Intelligence Store**
  - Normalized relational store for scans, IOCs (Indicators of Compromise), classifications, and community flags.
  - Strict Row-Level Security (RLS) guaranteeing data privacy.
* **FR-04: Transparent Risk Explanation**
  - Return human-readable explanations: Threat Level (Safe, Low, Medium, High, Critical), Category, and concrete "Reasons Why" (e.g., "Homoglyph domain impersonating SBI", "Urgency language detected").
* **FR-05: Crowdsourced Threat Intelligence**
  - Community reporting mechanism with upvoting and analyst verification workflow.

---

## 4. Non-Functional Requirements (NFR)

* **NFR-01: Low Latency Scanning:** API response time $< 350\text{ ms}$ for deterministic checks; $< 1.2\text{ s}$ for full AI inference.
* **NFR-02: Zero Client-Side Secrets:** Zero exposure of Supabase `service_role` secrets or LLM provider keys in frontend code.
* **NFR-03: Offline Fallback:** Local heuristic tables and offline cache ensure uptime even during cloud API interruptions.
* **NFR-04: High Data Integrity:** Relational foreign keys, ACID compliance, and audit logging on Supabase PostgreSQL.
