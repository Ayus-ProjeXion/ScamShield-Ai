"""
ScamShield AI — Live Interactive Terminal Scanner
Allows you to test any text, SMS, email, WhatsApp message, or URL live in your terminal!
"""

import os
import sys
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from detector import ScamDetector

def main():
    print("=" * 65)
    print("🛡️  SCAMSHIELD AI — LIVE INTERACTIVE MULTI-MODAL SCANNER")
    print("   Type or paste any SMS, URL, Email, or path to an Audio Call (.wav)")
    print("   Type 'exit' or 'quit' to close the scanner.")
    print("=" * 65)

    detector = ScamDetector()

    while True:
        try:
            print("\n" + "-" * 65)
            user_input = input("👉 Enter message or audio path (.wav, .mp3) to scan:\n> ").strip()
            
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("\nExiting ScamShield AI scanner. Stay safe online! 🛡️")
                break

            # Use unique request token so interactive developer testing doesn't get rate-limited
            req_id = f"cli_{time.time()}"
            
            # Check if input is an audio file
            is_audio = user_input.lower().endswith(('.wav', '.mp3', '.m4a', '.ogg')) or (os.path.isfile(user_input) and any(user_input.lower().endswith(ext) for ext in ['.wav', '.mp3', '.m4a']))
            
            if is_audio:
                print(f"🎙️ Detected audio file: '{user_input}'. Transcribing spoken speech...")
                result = detector.analyze_audio(user_input, client_id=req_id)
                if result.get("transcription_engine"):
                    print(f"🗣️ Transcribed Text: \"{result.get('transcribed_text')}\"")
                    print(f"⚙️ STT Engine: [{result.get('transcription_engine')}]")
            else:
                result = detector.analyze(user_input, client_id=req_id)

            if result.get("rate_limited"):
                print(f"\n⏳ [RATE LIMITED]: {result['why_its_risky'][0]['explanation']}")
                print(f"   {result['recommended_actions'][0]}")
                continue

            print("\n" + "=" * 65)
            print("🔍 SCAN RESULTS")
            print("=" * 65)
            
            # Severity color/styling
            threat = result["threat_level"]
            score = result["risk_score"]
            ml_p = int(result["ml_probability"] * 100)

            print(f"🎯 Threat Severity : [{threat}]")
            print(f"📊 Fraud Risk Score: {score}% (ML Confidence: {ml_p}%)")
            print(f"⚡ Is Scam Detected: {'YES 🚨' if result['is_scam'] else 'NO (Safe) ✅'}")
            print(f"🔒 Tamper-Proof ID : {result['security_token']['hmac_signature'][:24]}... (HMAC-SHA256)")

            if result["badges"]:
                print(f"🏷️  Evidence Badges: {' | '.join(result['badges'])}")

            if result["why_its_risky"]:
                print("\n🧐 Why It's Risky (Explainable Breakdown):")
                for item in result["why_its_risky"]:
                    print(f"   • {item['factor']}: {item['explanation']}")

            if result["recommended_actions"]:
                print("\n💡 Recommended Actions & Safety Guidelines:")
                for action in result["recommended_actions"]:
                    print(f"   {action}")

            if result["complaint_draft"]:
                print("\n📋 1-Click Helpline 1930 / Cyber Crime Complaint Draft:")
                print(result["complaint_draft"])

            print(f"\n⚖️  Disclaimer: {result['disclaimer']}")

        except KeyboardInterrupt:
            print("\n\nSession terminated by user. Goodbye! 🛡️")
            break
        except Exception as e:
            print(f"\n❌ Error during scan: {e}")

if __name__ == "__main__":
    main()
