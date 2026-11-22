"""
ScamShield AI — Unified Multi-Modal Threat Detection Engine
Combines Classical ML (Logistic Regression) + Deterministic Security Heuristics.
"""

import os
import sys
from typing import Dict, Any, List

# Ensure ai directory is in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from rule_engine import evaluate_heuristics
import joblib

MODEL_PATH = os.path.join(CURRENT_DIR, "models", "scam_classifier.joblib")

class ScamDetector:
    """
    Dual-engine scam detector combining Machine Learning probability
    with deterministic regex security heuristics.
    """
    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        """Loads trained ML model pipeline or auto-trains if not found."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            # Auto-train if model file does not exist
            from train import train_and_evaluate
            print("Model not found on disk. Initiating training pipeline...")
            train_and_evaluate()
            self.model = joblib.load(self.model_path)

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyzes a message or transcribed phone call.
        Returns risk score (0-100%), threat severity level, and evidence badges.
        """
        if not text or not text.strip():
            return {
                "text": text,
                "risk_score": 0.0,
                "threat_level": "SAFE",
                "is_scam": False,
                "ml_probability": 0.0,
                "urgency_score": 0.0,
                "badges": [],
                "explanation": "No input text provided."
            }

        # 1. Run Machine Learning Model (Probability of Scam)
        ml_prob = 0.0
        if self.model:
            # Predict probability of class 1 (Scam)
            probs = self.model.predict_proba([text])[0]
            ml_prob = round(float(probs[1]), 4)

        # 2. Run Deterministic Security Heuristic Rules
        heuristic_res = evaluate_heuristics(text)
        urgency_score = heuristic_res["urgency_score"]
        badges: List[str] = list(heuristic_res["badges"])

        # 3. Combine Scores (Dual-Verification)
        # If deterministic rules flag critical triggers, elevate risk immediately
        if heuristic_res["rule_hit_count"] >= 3:
            combined_risk = max(ml_prob * 100, 92.0)
        elif heuristic_res["rule_hit_count"] >= 1:
            combined_risk = max(ml_prob * 100, 75.0)
        else:
            # Zero heuristic triggers: calibrated for benign personal & utility chats
            combined_risk = (ml_prob ** 2) * 60.0

        final_risk = round(min(100.0, max(0.0, combined_risk)), 1)

        # 4. Determine Threat Severity Level
        if final_risk >= 85.0:
            threat_level = "CRITICAL"
            is_scam = True
        elif final_risk >= 65.0:
            threat_level = "HIGH"
            is_scam = True
        elif final_risk >= 45.0 and heuristic_res["rule_hit_count"] > 0:
            threat_level = "MEDIUM"
            is_scam = False
        elif final_risk >= 20.0 or (heuristic_res["rule_hit_count"] == 0 and final_risk < 65.0):
            threat_level = "SAFE" if final_risk < 30.0 else "LOW"
            is_scam = False
        else:
            threat_level = "SAFE"
            is_scam = False

        # Add ML Badge if probability is high and corroborates security heuristics
        if ml_prob >= 0.70 and heuristic_res["rule_hit_count"] > 0 and "ML Model Fraud Trigger" not in badges:
            badges.insert(0, f"ML Pattern Match ({int(ml_prob*100)}% Confidence)")

        # 5. Build Explainability Breakdown (Why it's risky)
        why_its_risky: List[Dict[str, str]] = []
        for badge in badges:
            if "Urgency" in badge or "Deadline" in badge:
                why_its_risky.append({
                    "factor": badge,
                    "explanation": "Artificial time pressure detected. Scammers use short deadlines to create panic and stop you from verifying facts."
                })
            elif "Impersonation" in badge:
                why_its_risky.append({
                    "factor": badge,
                    "explanation": "Authority spoofing detected. Legitimate police, CBI, or customs officers never conduct 'digital arrests' or ask for money on phone/video calls."
                })
            elif "Utility Blackout" in badge:
                why_its_risky.append({
                    "factor": badge,
                    "explanation": "Utility cutoff threat detected. Real power/gas companies do not disconnect supply via personal SMS with personal contact numbers."
                })
            elif "UPI Payment" in badge:
                why_its_risky.append({
                    "factor": badge,
                    "explanation": "Personal peer-to-peer UPI handle detected. Official government agencies and utility boards never accept bill payments to personal UPI VPAs."
                })
            elif "Domain" in badge or "HTTP" in badge:
                why_its_risky.append({
                    "factor": badge,
                    "explanation": "Untrusted or insecure link detected. Phishing links mimic real bank portals to steal your passwords and PINs."
                })
            elif "Tax Refund" in badge:
                why_its_risky.append({
                    "factor": badge,
                    "explanation": "Tax refund lure detected. Income Tax Department directly credits verified bank accounts and never asks you to claim refunds via third-party web links."
                })
            elif "Hinglish" in badge:
                why_its_risky.append({
                    "factor": badge,
                    "explanation": "Hinglish regional coercion detected. Uses colloquial Hindi threats ('turant', 'aaj raat bijli cut', 'police karyawahi') to intimidate victims."
                })
            elif "Gaming" in badge:
                why_its_risky.append({
                    "factor": badge,
                    "explanation": "Gaming reward lure detected. Promises of free BGMI UC, Free Fire Diamonds, or Discord Nitro are phishing traps to steal account credentials."
                })
            elif "Loan" in badge:
                why_its_risky.append({
                    "factor": badge,
                    "explanation": "Predatory loan blackmail trap detected. Unofficial loan APKs harvest contact lists and gallery photos for extortion."
                })
            elif "ML Pattern" in badge:
                why_its_risky.append({
                    "factor": badge,
                    "explanation": f"Linguistic structure matches historical cyber-fraud patterns with {int(ml_prob*100)}% mathematical confidence."
                })

        # 6. Build Actionable Safety Advice & Recommendations
        recommendations: List[str] = []
        if is_scam or final_risk >= 50.0:
            recommendations.append("🛑 PROCEED WITH CAUTION: Do NOT click any links, download files, or transfer money.")
            if any("UPI" in b or "Advance Fee" in b for b in badges):
                recommendations.append("💳 Do NOT send money to the listed UPI ID or bank account.")
            if any("Utility" in b for b in badges):
                recommendations.append("💡 Check your bill independently by opening your official electricity provider app or portal (e.g. bsesdelhi.com).")
            if any("Impersonation" in b for b in badges):
                recommendations.append("👮 If anyone claims to be Police/CBI on a call, hang up immediately. Police never demand money for verification.")
            if any("Banking" in b or "Suspension" in b for b in badges):
                recommendations.append("🏦 Call your bank using ONLY the official phone number printed on the back of your debit card.")
            recommendations.append("🚨 If you suspect an active fraud, report it to the National Cyber Crime Helpline by dialing 1930 or visit cybercrime.gov.in.")
        else:
            recommendations.append("✅ Message appears safe, but always verify sender identity if sensitive information or money is requested.")

        disclaimer = "ScamShield AI provides automated probabilistic risk assessment to promote user vigilance. Always verify directly through verified official channels."

        return {
            "text": text,
            "risk_score": final_risk,
            "threat_level": threat_level,
            "is_scam": is_scam,
            "ml_probability": ml_prob,
            "urgency_score": urgency_score,
            "badges": badges,
            "why_its_risky": why_its_risky,
            "recommended_actions": recommendations,
            "disclaimer": disclaimer
        }

if __name__ == "__main__":
    detector = ScamDetector()

    print("\n" + "="*60)
    print("🛡️ SCAMSHIELD AI — LIVE INFERENCE DEMO")
    print("="*60)

    test_samples = [
        "Dear consumer your electricity power will be disconnected tonight at 9:30 PM. Pay bill immediately to UPI: bses@okaxis",
        "Aapka bijli bill update nahi hua hai, aaj raat 9:30 baje connection kaat diya jayega. Turant contact karein electricity officer se 9876543210 par.",
        "FREE 5000 BGMI UC drop fr fr no cap! Limited Season 30 event, claim code rn: http://bgmi-free-uc-drop.top/claim",
        "Pre-approved Personal Loan of Rs 5,00,000! 0% interest, Zero CIBIL score required. Install QuickCash Pro APK now: http://instant-loan-quickcash.apk",
        "Subject: Income Tax Refund Notice: Dear Taxpayer, an excess tax refund of Rs 42,950 has been approved. Update your bank account immediately at http://incometax-efiling-refund.xyz to claim within 24 hours.",
        "Bro that match yesterday was so lit no cap, ngl we cooked them fr fr iykyk!",
        "Aap kahan ho bro? Chai peene chalte hain 10 minute mein agar free ho toh.",
        "Hey Mom, I will reach home by 7:30 PM for dinner. Love you!"
    ]

    for sample in test_samples:
        res = detector.analyze(sample)
        badge_str = " | ".join(res["badges"]) if res["badges"] else "None"
        print(f"\n📩 Message: \"{sample}\"")
        print(f"   🎯 Threat Level: [{res['threat_level']}]  Risk Score: {res['risk_score']}%  (ML: {int(res['ml_probability']*100)}%)")
        print(f"   🏷️ Badges: {badge_str}")
        if res["why_its_risky"]:
            print("   🧐 Why It's Risky:")
            for item in res["why_its_risky"][:3]:
                print(f"      • {item['factor']}: {item['explanation']}")
        print("   💡 Recommended Actions:")
        for action in res["recommended_actions"][:3]:
            print(f"      {action}")
        print(f"   ⚖️ Disclaimer: {res['disclaimer']}")
    print("\n" + "="*60)
