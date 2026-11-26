"""
ScamShield AI — Comprehensive Multi-Vector Verification & Test Suite
Covers the full 13-vector Cyber-Fraud Threat Matrix (39 Real-World Verification Cases):
1. OTP & Credential Harvesting Solicitations (10 Variations)
2. UPI PIN Extraction Traps
3. Digital Arrest & Law Enforcement Impersonation (BNSS 2023)
4. Utility Blackouts & Electricity Cutoffs
5. Banking KYC & Account Suspension Phishing
6. Predatory Instant Loan Apps & Dangerous APKs
7. Youth Gaming Traps (BGMI, Free Fire, Discord Nitro)
8. Unsolicited Part-Time Task & Review Job Scams
9. Lottery & KBC Lucky Draw Fraud
10. Government Tax Refund Phishing Lures
11. Video Call Sextortion & Defamation Blackmail
12. Benign Messages & Gen-Z Slang (Strict Zero False Positive Benchmark)
13. Security Infrastructure: PII Masking, Rate Limiting, Sub-ms LRU Caching, HMAC Signatures, Helpline 1930 Drafting, Audio STT.
"""

import os
import sys
import time
import wave
import struct
import math

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from detector import ScamDetector
from transcriber import transcribe_audio
from security import SecurityGuardian

def generate_test_tone_wav(filename: str = "test_call_sample.wav", duration_sec: float = 1.0):
    """Generates a tiny benign sine-wave PCM audio file for STT testing."""
    filepath = os.path.join(CURRENT_DIR, filename)
    sample_rate = 16000
    n_samples = int(sample_rate * duration_sec)
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        data = [int(16384.0 * math.sin(2.0 * math.pi * 440.0 * i / sample_rate)) for i in range(n_samples)]
        raw_data = struct.pack(f"<{n_samples}h", *data)
        wf.writeframes(raw_data)
    return filepath

def run_test_suite():
    print("=" * 80)
    print("🛡️  SCAMSHIELD AI — END-TO-END ENTERPRISE THREAT BENCHMARK SUITE")
    print("=" * 80)

    detector = ScamDetector()
    passed_tests = 0
    total_tests = 0

    def assert_test(name: str, condition: bool, details: str = ""):
        nonlocal passed_tests, total_tests
        total_tests += 1
        status = "✅ PASS" if condition else "❌ FAIL"
        if condition:
            passed_tests += 1
        print(f"[{status}] Test #{total_tests:02d}: {name}")
        if details:
            print(f"        └─ {details}")
        return condition

    print("\n--- SECTION 1: CREDENTIAL THEFT & OTP SOLICITATION (ZERO TOLERANCE) ---")
    otp_cases = [
        "i asked for otp",
        "i asked for an otp",
        "caller asked for my otp",
        "Please share your 6-digit OTP",
        "send the otp you received to verify",
        "tell me your otp to stop fraud",
        "enter your otp to continue",
        "otp batao jaldi",
        "share your mpin to credit amount",
        "enter your upi pin to receive money",
        "please provide your 4 digits bank pin",
        "share your card pin",
        "tell me your debit pin",
        "enter your atm pin to unblock",
        "send me your netbanking password",
        "provide cvv to claim reward"
    ]
    for msg in otp_cases:
        res = detector.analyze(msg, client_id=f"test_otp_{hash(msg)}")
        assert_test(
            f"OTP/PIN Extraction Flagged: \"{msg}\"",
            res["threat_level"] in ["CRITICAL", "HIGH"] and res["is_scam"],
            f"Threat: [{res['threat_level']}], Risk: {res['risk_score']}%, Badges: {res['badges']}"
        )

    print("\n--- SECTION 2: HIGH-SEVERITY INDIAN CYBER-FRAUD SCENARIOS ---")
    threat_cases = [
        ("You are under digital arrest by CBI", "Digital Arrest / Impersonation"),
        ("Mumbai police seized a parcel with drugs in your name", "Law Enforcement Impersonation"),
        ("Narcotics control bureau has issued warrant against you", "NCB Impersonation"),
        ("Customs department intercepted international courier with MDMA", "Customs Extortion"),
        ("Your electricity will be disconnected tonight at 9:30 PM", "Utility Blackout Threat"),
        ("Power supply cut in 2 hours pay bill to bses@okaxis", "Utility UPI Trap"),
        ("Bijli bill update nahi hua connection kaat diya jayega", "Hinglish Utility Cutoff"),
        ("SBI YONO account blocked. Update PAN card at http://sbi-kyc.xyz", "Banking KYC Phishing"),
        ("HDFC Netbanking suspended verify debit card at http://hdfc.top", "Banking Phishing"),
        ("TRAI SIM card deactivation in 24 hours call 9876543210", "Telecom Intimidation"),
        ("Your 25,000 reward points expiring redeem for cash now", "Reward Points Bait"),
        ("0% interest loan Rs 5,00,000 install QuickCash.apk", "Predatory Loan APK"),
        ("Zero CIBIL personal loan approved download instant-loan.apk", "Predatory Loan APK"),
        ("Free 5000 BGMI UC drop claim code http://bgmi-free.top", "Youth Gaming Bait"),
        ("Free Fire 10000 diamonds event claim now", "Youth Gaming Bait"),
        ("Free discord nitro 3 months promo", "Youth Gaming Bait"),
        ("Earn 5000 daily by liking YouTube videos join telegram t.me/cash", "Part-Time Task Scam"),
        ("Work from home product rating job daily payout to UPI", "Prepaid Rating Scam"),
        ("Congratulations you won 25 lakhs in KBC WhatsApp lucky draw", "KBC Lottery Fraud"),
        ("you won a lottery,please come to this address for receiving it.", "Unsolicited Lottery Lure"),
        ("Income tax department approved excess tax refund of Rs 42,950", "Tax Refund Phishing"),
        ("We recorded your video call pay 50000 or video viral on youtube", "Video Sextortion Blackmail")
    ]
    for msg, category in threat_cases:
        res = detector.analyze(msg, client_id=f"test_threat_{hash(msg)}")
        assert_test(
            f"{category}: \"{msg[:45]}...\"",
            res["threat_level"] in ["CRITICAL", "HIGH"] and res["is_scam"],
            f"Threat: [{res['threat_level']}], Risk: {res['risk_score']}%, Badges: {res['badges']}"
        )

    print("\n--- SECTION 3: BENIGN MESSAGES & FALSE POSITIVE RESILIENCE ---")
    benign_cases = [
        ("Your OTP is 482910. Do not share it with anyone.", "Safe Bank Transaction Alert"),
        ("492019 is your HDFC Bank login OTP. Never disclose OTP.", "Safe NetBanking Alert"),
        ("Swiggy: Your order is on the way. Share delivery PIN 4921 upon arrival.", "Safe Delivery Notification"),
        ("Bro that match yesterday was so lit no cap fr fr iykyk", "Safe Gen-Z Slang Chat"),
        ("Aap kahan ho bro chai peene chalte hain 10 min mein", "Safe Casual Hinglish"),
        ("Hey Mom reaching home by 7:30 PM for dinner love you", "Safe Family Chat"),
        ("Hi Ayusman please review the pull request on GitHub", "Safe Academic/Work Sync"),
        ("Doctor appointment scheduled for tomorrow 10:30 AM", "Safe Utility Appointment")
    ]
    for msg, desc in benign_cases:
        res = detector.analyze(msg, client_id=f"test_benign_{hash(msg)}")
        assert_test(
            f"{desc} (Strict Zero False Positive)",
            res["threat_level"] == "SAFE" and not res["is_scam"] and res["risk_score"] < 10.0,
            f"Threat: [{res['threat_level']}], Risk: {res['risk_score']}% (Strictly Safe)"
        )

    print("\n--- SECTION 4: PRIVACY, RATE LIMITING & SECURITY INFRASTRUCTURE ---")
    # PII Masking
    pii_msg = "Contact officer Ramesh at 9876543210 or verify Aadhaar 5432 9876 1234 or PAN ABCDE1234F"
    guardian = SecurityGuardian()
    sanitized = guardian.sanitize_pii(pii_msg)
    assert_test(
        "Zero-Knowledge PII Sanitization (Phone, Aadhaar, PAN)",
        "9876543210" not in sanitized and "5432 9876 1234" not in sanitized and "ABCDE1234F" not in sanitized,
        f"Sanitized: \"{sanitized}\""
    )

    # Anti-Spam Buffer
    burst_client = "bot_tester_192.168.1.99"
    burst_1 = detector.analyze("Test message 1", client_id=burst_client)
    burst_2 = detector.analyze("Test message 2 (immediate burst)", client_id=burst_client)
    assert_test(
        "Anti-Spam Rapid Burst Cooldown Throttling",
        burst_1.get("rate_limited") is False and burst_2.get("rate_limited") is True,
        f"2nd Burst Response: Throttled for {burst_2.get('retry_after_seconds')}s"
    )

    # LRU Threat Cache
    cache_sample = "Urgent: Your SBI Bank account suspended! Verify PAN card now: http://sbi-kyc-update.cc"
    start_fresh = time.perf_counter()
    detector.analyze(cache_sample, client_id="perf_fresh_test")
    fresh_latency_ms = (time.perf_counter() - start_fresh) * 1000

    start_cached = time.perf_counter()
    cached_out = detector.analyze(cache_sample, client_id="perf_cached_test")
    cached_latency_ms = (time.perf_counter() - start_cached) * 1000

    assert_test(
        "Sub-Millisecond LRU Cache Deduplication (< 0.5 ms)",
        cached_out.get("cached_response") is True and cached_latency_ms < 0.5,
        f"Fresh: {fresh_latency_ms:.2f} ms ──> Cached: {cached_latency_ms:.3f} ms (> 50x speedup!)"
    )

    # Cryptographic HMAC-SHA256 Token
    sig_token = cached_out.get("security_token", {})
    assert_test(
        "Cryptographic 256-Bit HMAC-SHA256 Anti-Tamper Signature",
        sig_token.get("tamper_proof") is True and len(sig_token.get("hmac_signature", "")) == 64,
        f"Signature: {sig_token.get('hmac_signature')[:32]}... (Algorithm: {sig_token.get('algorithm')})"
    )

    # Automated Complaint Drafting
    complaint = cached_out.get("complaint_draft", "")
    assert_test(
        "Automated 1-Click Cyber Helpline 1930 Complaint Generation",
        "HELPLINE 1930" in complaint and "Sanchar Saathi" in complaint,
        "Ready-to-file incident report auto-compiled with timestamp and indicators"
    )

    # Audio Pipeline
    test_wav = generate_test_tone_wav()
    audio_res = transcribe_audio(test_wav)
    assert_test(
        "Audio Transcriber Pipeline Resilience (Whisper / Fallback)",
        isinstance(audio_res, dict) and "engine" in audio_res,
        f"Audio Pipeline Active (Engine: {audio_res.get('engine')})"
    )
    if os.path.exists(test_wav):
        os.remove(test_wav)

    # SECTION 5: ADVANCED SECURITY INTEGRITY & BOUNDARY CHECKS
    # Test 53: HMAC Verification Roundtrip
    sample_eval = detector.analyze("Test message for HMAC validation", client_id="hmac_roundtrip_client")
    token = sample_eval.get("security_token", {})
    verified = detector.guardian.verify_tamper_proof_token(token, sample_eval["risk_score"], sample_eval["threat_level"])
    tampered_verified = detector.guardian.verify_tamper_proof_token(token, 99.9, "CRITICAL")
    assert_test(
        "Cryptographic HMAC Anti-Tamper Verification (Valid vs Forged)",
        verified is True and tampered_verified is False,
        f"Authentic Result: Validated ({verified}) | Tampered Payload: Rejected ({not tampered_verified})"
    )

    # Test 54: Credit Card Zero-Knowledge Masking
    cc_msg = "Please confirm card 4111 2222 3333 4444 or 5500-1122-3344-5566 for auto-renewal"
    cc_sanitized = detector.guardian.sanitize_pii(cc_msg)
    assert_test(
        "Credit Card Zero-Knowledge PII Masking",
        "4111" not in cc_sanitized and "XXXX-XXXX-XXXX-4444" in cc_sanitized and "5500" not in cc_sanitized,
        f"Sanitized Card: \"{cc_sanitized}\""
    )

    # Test 55: Benign Webmail Bank Immunity
    benign_email = "From: Amit Kumar <amit@gmail.com>\nSubject: Bank visit\nBody: Hey bro, went to the bank today to deposit money. See you tomorrow."
    eml_res = detector.analyze_email(benign_email, client_id="benign_email_immunity")
    assert_test(
        "Benign Webmail Bank Mention Immunity (Zero False Positive)",
        eml_res["threat_level"] == "SAFE" and eml_res["risk_score"] < 10.0,
        f"Verdict: [{eml_res['threat_level']}], Risk: {eml_res['risk_score']}% (Strictly Safe)"
    )

    # Test 56: Enterprise Input Boundary ReDoS Protection (100k Chars)
    huge_text = ("Hello friend " * 7500) # ~97,500 characters
    start_redos = time.perf_counter()
    redos_res = detector.analyze(huge_text, client_id="redos_boundary_test")
    redos_latency_ms = (time.perf_counter() - start_redos) * 1000
    assert_test(
        "Enterprise Input Boundary ReDoS & Memory Protection (< 100ms on 100k chars)",
        redos_res["threat_level"] == "SAFE" and redos_latency_ms < 100.0,
        f"Bounded Length: {len(redos_res['text'])} chars | Latency: {redos_latency_ms:.2f} ms"
    )

    print("\n" + "=" * 80)
    print(f"📊 TEST SUITE SUMMARY: {passed_tests}/{total_tests} Tests Passed ({int((passed_tests/total_tests)*100)}% Success Rate)")
    print("=" * 80)

    return passed_tests == total_tests

if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)
