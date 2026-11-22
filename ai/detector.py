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

        # Generate human-readable explanation
        if is_scam:
            reasons = ", ".join(badges[:3]) if badges else "Suspicious linguistic patterns detected"
            explanation = f"High probability scam detected! Flagged for: {reasons}."
        else:
            explanation = "Message appears legitimate. No coercive urgency or malicious vectors detected."

        return {
            "text": text,
            "risk_score": final_risk,
            "threat_level": threat_level,
            "is_scam": is_scam,
            "ml_probability": ml_prob,
            "urgency_score": urgency_score,
            "badges": badges,
            "explanation": explanation
        }

if __name__ == "__main__":
    detector = ScamDetector()

    print("\n" + "="*60)
    print("🛡️ SCAMSHIELD AI — LIVE INFERENCE DEMO")
    print("="*60)

    test_samples = [
        "Dear consumer your electricity power will be disconnected tonight at 9:30 PM. Pay bill immediately to UPI: bses@okaxis",
        "Hello, this is Inspector Rathore from Mumbai Crime Branch. Your Aadhaar is linked to a seized narcotics parcel in Cambodia. Transfer Rs 2,00,000 immediately.",
        "Your SBI YONO account will be blocked today due to pending KYC. Click http://sbi-kyc-update.xyz to update.",
        "Hey Mom, I will reach home by 7:30 PM for dinner. Love you!",
        "Your Zomato order from Biryani Blues is arriving in 12 mins. Track delivery in app."
    ]

    for sample in test_samples:
        res = detector.analyze(sample)
        badge_str = " | ".join(res["badges"]) if res["badges"] else "None"
        print(f"\n📩 Message: \"{sample}\"")
        print(f"   🎯 Threat Level: [{res['threat_level']}]  Risk Score: {res['risk_score']}%  (ML: {int(res['ml_probability']*100)}%)")
        print(f"   🏷️ Badges: {badge_str}")
        print(f"   💡 Explanation: {res['explanation']}")
    print("\n" + "="*60)
