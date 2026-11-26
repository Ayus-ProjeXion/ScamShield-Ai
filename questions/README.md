# ∀VITR AI — Master Technical Q&A & Evaluator Defense Guide

This directory houses the comprehensive collection of technical defense questions, architectural explanations, and real-world calibrated test examples asked by evaluators, judges, and developers.

> **PDF Version Available:** [Questions_That_Can_Be_Asked.pdf](file:///c:/Users/HP/OneDrive/Desktop/ScamShield-Ai/questions/Questions_That_Can_Be_Asked.pdf) (also mirrored directly to your Desktop).

---

## Table of Contents
1. [AI Scoring Engine & Threat Mathematics](#1-ai-scoring-engine--threat-mathematics)
   - [Q1: How is the Scam Percentage / Risk Score calculated?](#q1-how-is-the-scam-percentage--risk-score-calculated)
   - [Q2: What is the 70% scam tier about? (With real-world examples)](#q2-what-is-the-70-scam-tier-about)
2. [Zero-Knowledge Privacy & DPDP Act 2023 Compliance](#2-zero-knowledge-privacy--dpdp-act-2023-compliance)
   - [Q3: How does PII Masking work when someone inputs data?](#q3-how-does-pii-masking-work-when-someone-inputs-data)
3. [High-Performance Infrastructure](#3-high-performance-infrastructure)
   - [Q4: How does our LRU Threat Cache work?](#q4-how-does-our-lru-threat-cache-work)
   - [Q5: What is the role of Rate Limiting in our project?](#q5-what-is-the-role-of-rate-limiting-in-our-project)
4. [Forensics, Database & Public Defense](#4-forensics-database--public-defense)
   - [Q6: What is the use of storing the Case ID in the database?](#q6-what-is-the-use-of-storing-the-case-id-in-the-database)
   - [Q7: How can other people visiting the website see warnings on their screen?](#q7-how-can-other-people-visiting-the-website-see-warnings-on-their-screen)
   - [Q8: What happens when clicking 1930 and how does the Cyber Police draft work?](#q8-what-happens-when-clicking-1930-and-how-does-the-cyber-police-draft-work)
5. [Calibrated Test Suite Reference Table](#5-calibrated-test-suite-reference-table)

---

## 1. AI Scoring Engine & Threat Mathematics

### Q1: How is the Scam Percentage / Risk Score calculated?
Our engine uses a **Dual-Engine Architecture** combining calibrated Statistical Machine Learning with a 13-Rule Deterministic Security Automaton:

1. **Engine A (Classical ML Probability):** Text is vectorized using Scikit-Learn TF-IDF and passed to a Calibrated Logistic Regression model trained on 10,392 multi-modal samples. It outputs a continuous probability $P(\text{scam}) \in [0.0, 1.0]$.
2. **Engine B (Deterministic Rule Heuristics):** 13 pre-compiled regex rules inspect fatal patterns (OTP demands, peer UPI VPAs, fake CBI digital arrest, authority spoofing, untrusted .apk links, countdown timers).
3. **Dual-Verification Fusion:**
   - **Fatal Threat Floor:** If fatal rules trigger (OTP solicitation, UPI collect fraud), risk is clamped to a minimum **96.0% (CRITICAL)**.
   - **Authority Extortion:** If CBI/Police Digital Arrest or Electricity Cutoff matches, risk is clamped to **90.0% – 95.0%**.
   - **General Heuristics:** If 1 non-fatal heuristic matches, risk is clamped to **75.0% (HIGH)**.
   - **Zero Heuristic Dampening:** If zero rules trigger and the text is authentic (e.g. Swiggy receipt, bank debit alert), risk is suppressed to **< 3.5% (SAFE)**, eliminating false alarms.

---

### Q2: What is the 70% scam tier about?
The **HIGH Threat tier (70.0% – 85.0%)** represents deceptive communications that carry elevated suspicious indicators but stop short of immediate criminal blackout threats or OTP demands:

* **Example 1 (73.4% - Lucky Prize Processing Fee):**
  > *"Dear user, your phone number has won a cash reward in our lucky promotion. Reply immediately to receive the processing voucher."*
  * **Why 73.4%:** Triggers high statistical scam probability (97.9%) without fatal APK or OTP demands.
* **Example 2 (75.0% - Insecure Package Tracking Link):**
  > *"Order shipment notice: Your parcel requires address re-confirmation. Update your shipping address at http://track-package-support.site"*
  * **Why 75.0%:** Hits Rule 13 (Suspicious Free/Low-Trust Domain Extension) and Rule 14 (Insecure Plaintext HTTP link).
* **Example 3 (82.8% - Delivery Exception Notice):**
  > *"Notification: Your package delivery address is incomplete. Please confirm your postal code at http://delivery-support-desk.top to avoid delay."*
  * **Why 82.8%:** Coercive urgency combined with low-trust `.top` domain and credential redirection.

---

## 2. Zero-Knowledge Privacy & DPDP Act 2023 Compliance

### Q3: How does PII Masking work when someone inputs data?
PII (Personally Identifiable Information) masking is handled by `SecurityGuardian.sanitize_pii` in volatile RAM before anything is logged or committed to the database. It functions like an automated digital redaction marker:

* **Indian Mobile Numbers (10 digits):** `9876543210` $\rightarrow$ `987****210` (retains first 3 and last 3 for police/victim matching, masks middle 4).
* **Credit/Debit Cards (16 digits):** `4532-1234-5678-9012` $\rightarrow$ `XXXX-XXXX-XXXX-9012` (PCI-DSS compliant).
* **Aadhaar Numbers (12 digits):** `5432 1098 7654` $\rightarrow$ `XXXX-XXXX-7654` (complies with UIDAI masking norms).
* **PAN Cards (10 chars):** `ABCDE1234F` $\rightarrow$ `ABCXX****F`.

**Zero-Knowledge Screenshot Guarantee:** When users upload screenshots, **Tesseract.js OCR runs 100% inside their browser via WebAssembly (WASM)**. The raw photo is **never uploaded to our server (0 bytes transmitted)**. Only client-extracted text is sent, ensuring strict compliance with India's **Digital Personal Data Protection Act (DPDP Act 2023)**.

---

## 3. High-Performance Infrastructure

### Q4: How does our LRU Threat Cache work?
Managed by `LRUThreatCache` in `ai/security.py` with a capacity of 10,000 entries:

1. **The Viral Scam Problem:** When scammers blast 50,000 citizens with the identical electricity cutoff SMS, evaluating ML repeatedly wastes server CPU.
2. **Normalization & SHA-256 Fingerprint:** Incoming text is lowercased and whitespace-stripped, then converted into a 256-bit SHA-256 digital fingerprint (`key = sha256(text)`).
3. **Sub-Millisecond Cache Hit:** If the hash exists in RAM, the saved verdict is returned in **0.08 milliseconds (> 100x speedup with 0% CPU compute)**.
4. **LRU Eviction:** If cache exceeds 10,000 items, the oldest unrequested scam is automatically discarded (`popitem(last=False)`), keeping trending scams resident in RAM.

---

### Q5: What is the role of Rate Limiting in our project?
Rate limiting is enforced by the `AntiSpamBuffer` as the very first guard in `ai/detector.py`:

* **Layer 1 (1.5s Cooldown Buffer):** Enforces a 1.5-second pause between scans from the same client. This completely absorbs double-clicks and rapid button hammering.
* **Layer 2 (15 Scans / Minute Sliding Window):** Tracks timestamps over a rolling 60-second window. Any client exceeding 15 scans is paused with a clear countdown timer.
* **Security & Cost Value:** Stops botnet DoS attacks, protects computationally heavy Whisper audio transcription and OCR engines, and prevents cybercriminals from brute-force testing scam variations to reverse-engineer our detection rules.

---

## 4. Forensics, Database & Public Defense

### Q6: What is the use of storing the Case ID in the database?
When an incident is evaluated, our engine signs the risk score and threat level with a **256-bit HMAC-SHA256 signature** and generates an official Forensic Case ID (e.g. `#D3E256C81A092F`):

1. **Cryptographic Chain of Custody:** Proves mathematically that the threat score was generated by our engine and was not altered by a man-in-the-middle network attacker.
2. **Instant 1-Click Quick Lookup:** Users or investigating officers can paste the Case ID directly into the scanner search box to pull up the complete historical forensic record.
3. **Cross-Referencing for Law Enforcement:** Police officers on **Helpline 1930 / Chakshu** can reference the Case ID to correlate repeated complaints against the same criminal UPI ID or bank account.

---

### Q7: How can other people visiting the website see warnings on their screen?
Via our **Community Threat Intelligence Feed** (powered by Supabase PostgreSQL):

When a user scans or reports a new scam campaign, the backend stores the sanitized preview and extracted indicators of compromise (IOCs: fraud phone numbers, spoofed UPI handles, malicious domains) in the database. When other visitors browse the platform, the frontend polls `GET /api/v1/feed` to display trending cybercrime alerts in real time. Because all text is pre-sanitized by our PII engine, no victim's personal data is ever exposed to the public.

---

### Q8: What happens when clicking Helpline 1930 and how does the Cyber Police draft work?
Clicking the **1-Click Police Complaint Draft** button instantly formats an official legal incident dossier containing:

* **Incident Timestamp:** Exact UTC/IST timestamp.
* **Official Forensic Case ID:** `#D3E256...` for database traceability.
* **Automated Threat Assessment:** Threat level and probability score.
* **Detected Threat Categories:** Forensic breakdown of detected tactics (e.g. APK Malware, Blackout Extortion).
* **Action Requested:** Standard legal request requesting immediate freezing of perpetrator UPI accounts and phone line blocking under Sanchar Saathi (Chakshu).

---

## 5. Calibrated Test Suite Reference Table

| File / Test Scenario | Threat Tier | Calibrated Score | Key Security Trigger / Reason |
| :--- | :---: | :---: | :--- |
| `01_safe_02pct_swiggy_receipt` | `SAFE` | **1.7%** | Itemized Swiggy food delivery receipt with GPay UPI. |
| `02_safe_02pct_bank_debit_alert` | `SAFE` | **2.1%** | Legitimate ATM debit alert with official toll-free 18002664332 helpline. |
| `04_low_49pct_account_profile_verification` | `LOW` | **49.2%** | Account review notice without malicious links or coercive demands. |
| `05_medium_51pct_digital_wallet_compliance` | `LOW/MED` | **51.3%** | Digital wallet outbound transfer suspension notice. |
| `06_high_73pct_lucky_reward_processing_voucher` | `HIGH` | **73.4%** | Unsolicited cash reward promotion voucher lure. |
| `07_high_75pct_untrusted_domain_package_tracker` | `HIGH` | **75.0%** | Parcel address update link on `.site` domain with HTTP. |
| `08_high_83pct_delivery_exception_portal` | `HIGH` | **82.8%** | Insecure `.top` domain postal code re-confirmation trap. |
| `09_critical_90pct_predatory_loan_trap` | `CRITICAL` | **90.0%** | Instant Rs 50,000 loan without CIBIL check; predatory loan trap. |
| `10_critical_96pct_bijli_blackout_apk_extortion` | `CRITICAL` | **96.1%** | Power supply disconnection tonight at 9:30 PM with malicious APK payload. |
| `11_critical_98pct_cbi_digital_arrest_warrant` | `CRITICAL` | **90.0%** | Fake CBI Digital Arrest, 140g narcotics seizure threat. |
