import os
import sys
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_api_suite():
    print("=" * 80)
    print("🛡️  SCAMSHIELD AI — FASTAPI BACKEND API GATEWAY TEST SUITE")
    print("=" * 80)
    
    passed = 0
    total = 0
    
    def check(title, condition, detail=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"[✅ PASS] Test #{total:02d}: {title}")
            if detail:
                print(f"        └─ {detail}")
        else:
            print(f"[❌ FAIL] Test #{total:02d}: {title}")
            if detail:
                print(f"        └─ {detail}")

    # 1. Root Endpoint
    r = client.get("/")
    check(
        "Root Discovery Endpoint (GET /)",
        r.status_code == 200 and "endpoints" in r.json(),
        f"Status: {r.status_code} | Project: {r.json().get('project')}"
    )

    # 2. Health Endpoint
    r = client.get("/health")
    h = r.json()
    check(
        "System Health & Metrics (GET /health)",
        r.status_code == 200 and h.get("status") == "HEALTHY" and h.get("model_loaded") is True,
        f"AI Engine: {h.get('ai_engine_status')} | Latency: {h.get('avg_inference_latency_ms')} ms"
    )

    # 3. Text Scan - Scam SMS
    r = client.post("/api/v1/scan/text", json={
        "text": "Your SBI account is suspended! Please share your 6-digit OTP immediately.",
        "client_id": "api_test_scam_1",
        "channel": "SMS"
    })
    res_scam = r.json()
    check(
        "Text Scan Endpoint: SMS Threat Detection (POST /api/v1/scan/text)",
        r.status_code == 200 and res_scam.get("threat_level") == "CRITICAL" and res_scam.get("is_scam") is True,
        f"Verdict: [{res_scam.get('threat_level')}] ({res_scam.get('risk_score')}%) | Badges: {res_scam.get('badges')[:2]}"
    )

    # 4. Text Scan - Cryptographic HMAC Token
    token = res_scam.get("security_token", {})
    check(
        "Scan Response Cryptographic HMAC-SHA256 Token",
        token.get("tamper_proof") is True and len(token.get("hmac_signature", "")) == 64,
        f"Signature: {token.get('hmac_signature')[:32]}... (Algorithm: {token.get('algorithm')})"
    )

    # 5. Text Scan - Safe Everyday Chat
    r = client.post("/api/v1/scan/text", json={
        "text": "Hey bro, reaching home in 10 minutes see you for dinner.",
        "client_id": "api_test_safe_1",
        "channel": "WHATSAPP"
    })
    res_safe = r.json()
    check(
        "Text Scan Endpoint: Safe Message (Zero False Positive)",
        r.status_code == 200 and res_safe.get("threat_level") == "SAFE" and res_safe.get("risk_score") < 10.0,
        f"Verdict: [{res_safe.get('threat_level')}], Risk: {res_safe.get('risk_score')}%"
    )

    # 6. Email Scan with RFC Headers
    email_sample = """From: SBI Support <sbi.kyc.verification@gmail.com>
Subject: URGENT: NetBanking Access Blocked
Body: Dear Customer, verify your PAN immediately at http://sbi-unblock.xyz to avoid suspension."""
    r = client.post("/api/v1/scan/email", json={
        "email_text": email_sample,
        "client_id": "api_test_email_1"
    })
    res_email = r.json()
    check(
        "Email Scan Endpoint: RFC Headers & Webmail Spoofing (POST /api/v1/scan/email)",
        r.status_code == 200 and res_email.get("threat_level") == "CRITICAL",
        f"Verdict: [{res_email.get('threat_level')}] | Badges: {res_email.get('badges')[:2]}"
    )

    # 7. Audio Call Upload & Transcription
    test_audio_path = os.path.join("test_audio", "bank_otp_scam.wav")
    if os.path.exists(test_audio_path):
        with open(test_audio_path, "rb") as f:
            r = client.post(
                "/api/v1/scan/audio",
                files={"file": ("bank_otp_scam.wav", f, "audio/wav")},
                data={"client_id": "api_test_audio_1"}
            )
        res_audio = r.json()
        check(
            "Audio Upload & Transcription Scan Endpoint (POST /api/v1/scan/audio)",
            r.status_code == 200 and res_audio.get("channel") == "CALL" and res_audio.get("threat_level") == "CRITICAL",
            f"Verdict: [{res_audio.get('threat_level')}] | Engine: {res_audio.get('audio_meta', {}).get('transcription_engine')}"
        )
    else:
        check("Audio Upload Scan Endpoint", False, f"File not found: {test_audio_path}")

    # 8. Retrieve Past Scan by ID
    scan_id = res_scam.get("scan_id")
    r = client.get(f"/api/v1/scan/{scan_id}")
    check(
        f"Retrieve Scan by UUID (GET /api/v1/scan/{{id}})",
        r.status_code == 200 and r.json().get("scan_id") == scan_id,
        f"Retrieved Scan ID: {scan_id} | Threat: {r.json().get('threat_level')}"
    )

    # 9. Submit Community Scam Report
    r = client.post("/api/v1/report", json={
        "ioc_value": "+919876500000",
        "ioc_type": "PHONE_NUMBER",
        "category": "IMPERSONATION",
        "title": "Fake Police Digital Arrest Caller",
        "description": "Caller claiming to be from Mumbai Cyber Cell demanding funds."
    })
    res_rep = r.json()
    check(
        "Submit Community Report (POST /api/v1/report)",
        r.status_code == 200 and res_rep.get("status") == "PENDING",
        f"Report ID: {res_rep.get('id')} | IOC: {res_rep.get('ioc_value')}"
    )

    # 10. List Community Reports
    r = client.get("/api/v1/reports")
    check(
        "List Community Reports (GET /api/v1/reports)",
        r.status_code == 200 and r.json().get("total") >= 1,
        f"Total Reports: {r.json().get('total')}"
    )

    # 11. Live Threat Intelligence Feed
    r = client.get("/api/v1/feed")
    check(
        "Threat Intelligence Feed (GET /api/v1/feed)",
        r.status_code == 200 and r.json().get("total_count") >= 1,
        f"Verified Feed Items: {r.json().get('total_count')}"
    )

    # 12. Input Validation (Empty Text -> 422 Error)
    r = client.post("/api/v1/scan/text", json={"text": ""})
    check(
        "Input Validation Boundary (Pydantic min_length -> 422 Unprocessable)",
        r.status_code == 422,
        f"Status: {r.status_code} (Properly Rejected Invalid Payload)"
    )

    # 13. Copilot Chat - Why Flagged
    r = client.post("/api/v1/copilot/chat", json={
        "message": "Why is this message flagged as 96% scam?",
        "scan_context": res_scam
    })
    c_res = r.json()
    check(
        "AI Copilot Endpoint - Threat Explanation (POST /api/v1/copilot/chat)",
        r.status_code == 200 and ("critical" in c_res.get("reply", "").lower() or "scam" in c_res.get("reply", "").lower()) and len(c_res.get("suggested_chips", [])) > 0,
        f"Engine: {c_res.get('engine_used')} | Latency: {c_res.get('latency_ms')} ms"
    )

    # 14. Copilot Chat - Legal Provisions Grounding
    r = client.post("/api/v1/copilot/chat", json={
        "message": "What legal action or IPC section can be filed for this?",
        "scan_context": res_scam
    })
    c_law = r.json()
    check(
        "AI Copilot Endpoint - Legal & Evidence Grounding (POST /api/v1/copilot/chat)",
        r.status_code == 200 and ("66D" in c_law.get("reply") or "BNS" in c_law.get("reply")),
        f"Grounded Sections: IT Act 66D / BNS 318(4) confirmed in reply"
    )

    # 15. WhatsApp Bot Webhook - Greeting Handshake (TwiML XML)
    r = client.post("/api/v1/webhook/whatsapp", data={
        "Body": "hi",
        "From": "whatsapp:+919876543210"
    })
    check(
        "WhatsApp Bot Webhook: Greeting & Discovery (POST /api/v1/webhook/whatsapp)",
        r.status_code == 200 and "<Response><Message>" in r.text and "1930" in r.text,
        f"Response Type: {r.headers.get('content-type')} | TwiML generated successfully"
    )

    # 16. WhatsApp Bot Webhook - Forwarded Scam Message Analysis (TwiML XML)
    r = client.post("/api/v1/webhook/whatsapp", data={
        "Body": "URGENT: Your Bijli bill was not updated. Power supply disconnected at 9:30 PM call 9876543210 or install MahaVitaran.apk",
        "From": "whatsapp:+919876543210"
    })
    check(
        "WhatsApp Bot Webhook: Scam Forwarding Interception (POST /api/v1/webhook/whatsapp)",
        r.status_code == 200 and "CRITICAL" in r.text and "1930" in r.text and "MHA GOVT OF INDIA" in r.text,
        f"Status: {r.status_code} | High-risk threat card & 1930 Cyber helpline returned"
    )

    # 17. WhatsApp Simulator Endpoint (JSON for Web UI & Mobile Preview)
    r = client.post("/api/v1/webhook/whatsapp/simulate", json={
        "message": "CENTRAL BUREAU OF INVESTIGATION NOTICE: You are under DIGITAL ARREST. Transfer funds or arrest warrant issued.",
        "sender": "+91 91234 56789"
    })
    sim_data = r.json()
    check(
        "WhatsApp Bot Interactive Simulator (POST /api/v1/webhook/whatsapp/simulate)",
        r.status_code == 200 and sim_data.get("is_scam") is True and sim_data.get("quick_dial") == "1930",
        f"Risk: {sim_data.get('risk_score')}% | Formatted Reply Length: {len(sim_data.get('whatsapp_formatted_reply', ''))} chars"
    )

    print("\n" + "=" * 80)
    print(f"📊 BACKEND API TEST SUMMARY: {passed}/{total} Tests Passed ({int((passed/total)*100)}% Success Rate)")
    print("=" * 80)
    return passed == total

if __name__ == "__main__":
    success = test_api_suite()
    sys.exit(0 if success else 1)
