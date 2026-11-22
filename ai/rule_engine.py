"""
ScamShield AI — Deterministic Security Heuristics & Rule Engine
Detects social engineering triggers, urgency framing, authority impersonation, and risky entities.
"""

import re
from typing import Dict, List, Any

# --- REGEX PATTERNS FOR HEURISTIC EVALUATION ---

URGENCY_PATTERNS = [
    (r"\b(immediately|urgent|urgently|within\s+\d+\s*(hours?|hrs?|mins?|minutes?))\b", "High Urgency Coercion"),
    (r"\b(tonight\s+at\s+\d+:\d+|\btoday\s+by\s+\d+:\d+|\bwithin\s+24\s*hrs?)\b", "Artificial Deadline Pressure"),
    (r"\b(power\s+will\s+be\s+disconnected|electricity\s+power\s+will\s+be\s+cut|supply\s+will\s+be\s+terminated)\b", "Utility Blackout Threat"),
    (r"\b(account\s+will\s+be\s+blocked|access\s+is\s+suspended|card\s+has\s+been\s+blocked)\b", "Account Suspension Intimidation"),
    (r"\b(avoid\s+fine|avoid\s+blackout|deactivated\s+in\s+24\s*hrs?)\b", "Penalty Intimidation"),
]

AUTHORITY_IMPERSONATION = [
    (r"\b(cbi|central\s+bureau\s+of\s+investigation|crime\s+branch|cyber\s+crime\s+cell|narcotics\s+control\s+bureau|ncb|police\s+officer|inspector)\b", "Law Enforcement Impersonation"),
    (r"\b(digital\s+arrest|non-bailable\s+warrant|arrest\s+warrant|money\s+laundering|seized.*drugs|international\s+courier|fedex.*drugs)\b", "Digital Arrest / Customs Extortion"),
    (r"\b(trai|telecom\s+regulatory|supreme\s+court|reserve\s+bank\s+of\s+india|rbi)\b", "Government Authority Spoofing"),
    (r"\b(electricity\s+officer|power\s+office|power\s+manager|meter\s+officer)\b", "Utility Official Impersonation"),
]

FINANCIAL_TRAPS = [
    (r"\b(transfer\s+rs\.?|pay\s+refundable|registration\s+fee|security\s+deposit|pay\s+pending\s+bill)\b", "Upfront Advance Fee Demand"),
    (r"\b(won\s+rs\.?|lucky\s+draw|kbc.*crorepati|cashback\s+reward|scratch\s+card)\b", "Unsolicited Lottery / Cashback Bait"),
    (r"\b(earn\s+rs\.?\s*\d+.*daily|like\s+youtube\s+videos|part-time\s+product\s+review|part-time\s+job)\b", "Part-time Task/Review Job Scam"),
    (r"\b(redeem.*points.*cash|reward\s+points\s+expiring)\b", "Reward Points Phishing"),
]

SUSPICIOUS_PAYMENT_AND_LINKS = [
    (r"https?://[^\s]+\.(xyz|top|online|site|link|info|me|click|club|live|tk|ml|ga|cf|gq)\b", "Suspicious Free/Low-Trust Domain Extension"),
    (r"https?://[^\s]+\.apk\b", "Dangerous Unofficial Android APK Download"),
    (r"[a-zA-Z0-9.\-_]+@(okaxis|ybl|paytm|apl|okhdfcbank|oksbi)\b", "Direct Peer UPI Payment Handle"),
    (r"\b(t\.me/[a-zA-Z0-9_\-]+)\b", "Redirection to Anonymous Telegram Channel"),
    (r"\bhttp://[^\s]+\b", "Insecure Plaintext HTTP Link"),
]

def evaluate_heuristics(text: str) -> Dict[str, Any]:
    """
    Evaluates input text against deterministic regex rule sets.
    Returns detected flags, calculated urgency score (0.0 to 1.0), and badges.
    """
    text_lower = text.lower()
    badges: List[str] = []
    matched_categories: List[str] = []

    # 1. Check Urgency
    urgency_hits = 0
    for pattern, badge in URGENCY_PATTERNS:
        if re.search(pattern, text_lower):
            badges.append(badge)
            urgency_hits += 1
            if "URGENCY" not in matched_categories:
                matched_categories.append("URGENCY")

    # 2. Check Authority Impersonation
    for pattern, badge in AUTHORITY_IMPERSONATION:
        if re.search(pattern, text_lower):
            badges.append(badge)
            if "IMPERSONATION" not in matched_categories:
                matched_categories.append("IMPERSONATION")

    # 3. Check Financial Traps
    for pattern, badge in FINANCIAL_TRAPS:
        if re.search(pattern, text_lower):
            badges.append(badge)
            if "FINANCIAL_BAIT" not in matched_categories:
                matched_categories.append("FINANCIAL_BAIT")

    # 4. Check Suspicious Links & UPI Handles
    for pattern, badge in SUSPICIOUS_PAYMENT_AND_LINKS:
        match = re.search(pattern, text_lower)
        if match:
            badges.append(badge)
            if "SUSPICIOUS_VECTOR" not in matched_categories:
                matched_categories.append("SUSPICIOUS_VECTOR")

    # Calculate calibrated heuristic urgency score
    raw_score = (urgency_hits * 0.25) + (len(matched_categories) * 0.2)
    urgency_score = min(1.0, round(raw_score, 2))

    # De-duplicate badges while preserving order
    unique_badges = list(dict.fromkeys(badges))

    return {
        "is_suspicious": len(unique_badges) > 0,
        "urgency_score": urgency_score,
        "matched_categories": matched_categories,
        "badges": unique_badges,
        "rule_hit_count": len(unique_badges),
    }

if __name__ == "__main__":
    test_msg = "Dear consumer your electricity power will be disconnected tonight at 9:30 PM. Pay pending bill immediately to UPI: bses@okaxis"
    print("Test Heuristics Evaluation:")
    result = evaluate_heuristics(test_msg)
    for k, v in result.items():
        print(f"  {k}: {v}")
