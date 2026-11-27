# ∀VITR AI — Multi-Modal Test Suite Guide

Comprehensive reference guide for all **4 sample test folders** across **threat percentage tiers** (0% to 100%).

> **Note:** As per UI design guidelines, these test files reside strictly in their respective offline directories (`test_sms/`, `test_emails/`, `test_audio/`, `test_screenshots/`) so the web frontend interface remains clean, fast, and uncluttered.

---

## 1. Threat Severity & Percentage Calibration

∀VITR AI's dual-engine classifies threats into 5 calibrated risk bands:

| Threat Tier | Scam Probability | Verdict | Key Characteristics |
| :--- | :---: | :---: | :--- |
| **SAFE** | **0.0% – 20.0%** | `SAFE` | Genuine delivery receipts, official bank debit alerts with toll-free numbers, everyday personal conversations. |
| **LOW** | **20.1% – 50.0%** | `LOW` | Promotional discounts, customer service notices, benign marketing with soft urgency. |
| **MEDIUM** | **50.1% – 70.0%** | `MEDIUM` | Unverified identity verification prompts, digital wallet alerts, unverified surveys. |
| **HIGH** | **70.1% – 85.0%** | `HIGH` | Insecure HTTP delivery tracking portals, fake prize vouchers, low-trust domain invoice traps. |
| **CRITICAL** | **85.1% – 100.0%** | `CRITICAL` | Fake CBI/Police Digital Arrest, electricity blackout extortion tonight with malicious APK payload, predatory loan blackmail. |

---

## 2. Directory Matrix Across All 4 Modalities

### 📱 1. `test_sms/` (SMS & WhatsApp Text Messages)

| Filename | Calibrated Score | Threat Tier | Scenario |
| :--- | :---: | :---: | :--- |
| `01_safe_02pct_swiggy_receipt.txt` | **1.7%** | `SAFE` | Authentic Swiggy order receipt with delivery partner details. |
| `02_safe_02pct_bank_debit_alert.txt` | **2.1%** | `SAFE` | Legitimate bank ATM debit alert with official toll-free helpline. |
| `03_safe_14pct_office_meeting_invite.txt` | **0.0%** | `SAFE` | Friendly colleague coordination message. |
| `04_low_49pct_account_profile_verification.txt` | **49.2%** | `LOW` | Soft profile review notice within 48 hours. |
| `05_medium_51pct_digital_wallet_compliance.txt` | **51.3%** | `LOW/MED` | Unsolicited wallet outbound transfer suspension notice. |
| `06_high_73pct_lucky_reward_processing_voucher.txt` | **73.4%** | `HIGH` | Lucky draw winner processing fee voucher lure. |
| `07_high_75pct_untrusted_domain_package_tracker.txt` | **75.0%** | `HIGH` | Courier address update link on `.site` domain with plaintext HTTP. |
| `08_high_83pct_delivery_exception_portal.txt` | **82.8%** | `HIGH` | Low-trust `.top` domain postal code re-confirmation trap. |
| `09_critical_90pct_predatory_loan_trap.txt` | **90.0%** | `CRITICAL` | Instant loan sanctioned without CIBIL check, coercive e-sign. |
| `10_critical_96pct_bijli_blackout_apk_extortion.txt` | **96.1%** | `CRITICAL` | Electricity cutoff tonight at 9:30 PM with malicious APK payload. |
| `11_critical_98pct_cbi_digital_arrest_warrant.txt` | **90.0%** | `CRITICAL` | Fake CBI narcotics seizure and Digital Arrest legal threat. |
| `12_critical_96pct_hinglish_otp_extraction.txt` | **96.0%** | `CRITICAL` | Hinglish OTP extraction ("Mobile pei aya hua otp dijie"). |
| `13_critical_96pct_hindi_parcel_otp_extortion.txt` | **96.0%** | `CRITICAL` | Devanagari Hindi parcel hold OTP scam ("पार्सल होल्ड पर है, आया OTP बताएं"). |
| `14_critical_96pct_hindi_bijli_blackout_threat.txt` | **95.0%** | `CRITICAL` | Devanagari Hindi electricity blackout ("आज रात 9:30 बजे बिजली कनेक्शन काट दिया जाएगा"). |
| `15_critical_99pct_hindi_cbi_digital_arrest.txt` | **90.0%** | `CRITICAL` | Devanagari Hindi CBI Digital arrest ("अवैध पार्सल में ड्रग्स, आप डिजिटल अरेस्ट के तहत हैं"). |
| `16_critical_96pct_hindi_bank_kyc_freeze.txt` | **95.0%** | `CRITICAL` | Devanagari Hindi bank KYC freeze ("खाता और डेबिट कार्ड ब्लॉक, तुरंत पैन लिंक करें"). |
| `17_safe_02pct_hindi_bank_debit_alert.txt` | **1.0%** | `SAFE` | Devanagari Hindi legitimate bank transaction alert ("खाते से ₹450 डेबिट किए गए"). |
| `18_safe_02pct_hinglish_casual_meeting.txt` | **0.1%** | `SAFE` | Everyday casual Hinglish meet-up planning chat. |

---

### 📧 2. `test_emails/` (RFC Email `.eml` Files)

| Filename | Calibrated Score | Threat Tier | Scenario |
| :--- | :---: | :---: | :--- |
| `short_safe_amazon_receipt.eml` | **0.8%** | `SAFE` | Authentic Amazon order shipment notice with BlueDart tracking. |
| `medium_safe_college_lab_schedule.eml` | **0.5%** | `SAFE` | Academic department laboratory timetable update. |
| `long_safe_cloud_infrastructure_maintenance.eml` | **15.8%** | `SAFE` | Legitimate scheduled cloud database maintenance notice. |
| `short_low_49pct_account_profile_verification.eml` | **72.7%** | `HIGH` | Account review notification with external security links. |
| `medium_51pct_digital_wallet_compliance.eml` | **71.8%** | `HIGH` | Digital wallet compliance warning with external review instructions. |
| `medium_high_73pct_lucky_reward_voucher.eml` | **74.0%** | `HIGH` | Unsolicited cash reward promotion with voucher claim instruction. |
| `short_scam_m365_expire.eml` | **90.0%** | `CRITICAL` | Corporate Office 365 credential harvesting phishing lure. |
| `long_scam_ceo_bec_wire_transfer.eml` | **92.2%** | `CRITICAL` | Business Email Compromise (BEC) urgent confidential wire transfer. |
| `long_scam_digital_arrest_legal_notice.eml` | **98.5%** | `CRITICAL` | Fake Supreme Court & Cyber Police Digital Arrest notice. |

---

### 🎙️ 3. `test_audio/` (Voice Recordings `.wav` & Transcripts `.txt`)

Every scenario includes both the `.txt` transcript (for direct analysis or reading) and the corresponding `.wav` audio file (for testing Whisper speech-to-text):

| Filename (.txt & .wav) | Calibrated Score | Threat Tier | Scenario |
| :--- | :---: | :---: | :--- |
| `01_safe_02pct_swiggy_receipt_transcript.txt` | **1.7%** | `SAFE` | Delivery rider confirmation phone call. |
| `02_safe_02pct_bank_debit_alert_transcript.txt` | **2.1%** | `SAFE` | Automated interactive voice response (IVR) bank alert. |
| `03_safe_14pct_office_meeting_invite_transcript.txt` | **0.0%** | `SAFE` | Brief workplace sync voicemail. |
| `04_low_49pct_account_profile_verification_transcript.txt` | **49.2%** | `LOW` | Account service team inquiry voicemail. |
| `05_medium_51pct_digital_wallet_compliance_transcript.txt` | **51.3%** | `LOW/MED` | Wallet service compliance automated reminder. |
| `06_high_73pct_lucky_reward_processing_voucher_transcript.txt` | **73.4%** | `HIGH` | Prize department call prompting voucher verification. |
| `07_high_75pct_untrusted_domain_package_tracker_transcript.txt` | **75.0%** | `HIGH` | Dispatch agent verbal request to update delivery details. |
| `08_high_83pct_delivery_exception_portal_transcript.txt` | **82.8%** | `HIGH` | Parcel hold call redirecting to unverified web portal. |
| `09_critical_90pct_predatory_loan_trap_transcript.txt` | **90.0%** | `CRITICAL` | Aggressive loan agent urging immediate approval and OTP. |
| `10_critical_96pct_bijli_blackout_apk_extortion_transcript.txt` | **96.1%** | `CRITICAL` | Impersonator calling claiming electricity disconnection tonight. |
| `11_critical_98pct_cbi_digital_arrest_warrant_transcript.txt` | **90.0%** | `CRITICAL` | Coercive cyber police digital arrest interrogation call. |

---

### 📸 4. `test_screenshots/` (Mobile Screenshot Cards `.png`)

High-contrast mobile cards rendered with clear typography for client-side **Tesseract.js OCR**:

| Filename | Calibrated Score | Threat Tier | Visual Card Theme |
| :--- | :---: | :---: | :--- |
| `01_safe_02pct_swiggy_receipt.png` | **1.7%** | `SAFE` | Emerald Green Header • Official Food Delivery Receipt |
| `02_safe_02pct_bank_debit_alert.png` | **2.1%** | `SAFE` | Emerald Green Header • Official Bank Transaction Notification |
| `03_safe_14pct_office_meeting_invite.png` | **0.0%** | `SAFE` | Emerald Green Header • Personal Project Discussion |
| `04_low_49pct_account_profile_verification.png` | **49.2%** | `LOW` | Yellow/Amber Header • Account Profile Review Notice |
| `05_medium_51pct_digital_wallet_compliance.png` | **51.3%** | `LOW/MED` | Orange Header • Wallet Compliance Alert |
| `06_high_73pct_lucky_reward_processing_voucher.png` | **73.4%** | `HIGH` | Red-Amber Header • Lucky Reward Processing Voucher |
| `07_high_75pct_untrusted_domain_package_tracker.png` | **75.0%** | `HIGH` | Red Header • Untrusted Domain Delivery Link |
| `08_high_83pct_delivery_exception_portal.png` | **82.8%** | `HIGH` | Red Header • Insecure Delivery Exception Portal |
| `09_critical_90pct_predatory_loan_trap.png` | **90.0%** | `CRITICAL` | Dark Red Header • Predatory Loan Instant Sanction Trap |
| `10_critical_96pct_bijli_blackout_apk_extortion.png` | **96.1%** | `CRITICAL` | Red Header • Bijli Power Blackout Extortion & APK |
| `11_critical_98pct_cbi_digital_arrest_warrant.png` | **90.0%** | `CRITICAL` | Crimson Header • Fake CBI Digital Arrest Warrant |

---

## 3. How to Test Any Sample

### Via Python Interactive CLI:
```bash
python -c "from ai.detector import ScamDetector; d = ScamDetector(); print(d.analyze(open('test_sms/06_high_73pct_lucky_reward_processing_voucher.txt', encoding='utf-8').read()))"
```

### Via Backend API:
```bash
# Text / SMS Scan
curl -X POST "http://localhost:8000/api/v1/scan" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your account verification is pending. Please review your profile at our service portal within 48 hours."}'

# Email Scan (.eml)
curl -X POST "http://localhost:8000/api/v1/scan/email" \
  -F "file=@test_emails/medium_51pct_digital_wallet_compliance.eml"

# Audio Scan (.wav)
curl -X POST "http://localhost:8000/api/v1/scan/audio" \
  -F "file=@test_audio/10_critical_96pct_bijli_blackout_apk_extortion.wav"
```

### Via Frontend UI:
Simply drag-and-drop or copy-paste any file content directly into the **Threat Analysis Console**!
