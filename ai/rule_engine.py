"""
ScamShield AI — Deterministic Security Heuristics & Comprehensive Threat Matrix
Implements a 13-vector Semantic Cybersecurity Concept Engine:
1. Credential Harvesting (OTP, PIN, MPIN, CVV, NetBanking passwords)
2. UPI PIN Extraction Fraud ("enter pin to receive money")
3. Authority Impersonation & Digital Arrest (BNSS 2023 compliance)
4. Essential Utility Blackouts (Electricity, Gas, Water cutoffs)
5. Banking, KYC & Account Suspension Intimidation
6. Predatory Loan APKs & Executable Malware Payloads
7. Youth Gaming Bait & Credential Traps (BGMI, Free Fire, Discord Nitro)
8. Unsolicited Part-Time Task & Review Job Scams
9. Lottery & KBC Lucky Draw Fraud
10. Government Tax Refund Phishing Lures
11. Video Call Sextortion & Defamation Blackmail
12. Untrusted Low-Trust Domains, Plaintext HTTP & Peer UPI Handles
13. Hinglish Regional Coercion Triggers
"""

import re
from typing import Dict, List, Any

def evaluate_heuristics(text: str) -> Dict[str, Any]:
    """
    Evaluates input text against the complete 13-vector threat matrix.
    Returns detected flags, calculated urgency score (0.0 to 1.0), and badges.
    """
    text_lower = text.lower()
    badges: List[str] = []
    matched_categories: List[str] = []
    urgency_hits = 0

    # -------------------------------------------------------------
    # 1. CREDENTIAL HARVESTING (OTP, PIN, MPIN, CVV, Passwords)
    # -------------------------------------------------------------
    has_cred_term = bool(re.search(
        r'\b(pin|mpin|tpin|cvv|cvc|otp|one\s*time\s*password|passcode|password|passphrase|verification\s*code|security\s*code|card\s*details|card\s*number|expiry\s*date|bank\s*details|account\s*details|netbanking\s*password|credentials)\b',
        text_lower
    ))
    
    if has_cred_term:
        is_safe_delivery = bool(re.search(
            r'\b(delivery\s*pin|ride\s*pin|share\s+(with\s+)?(driver|delivery)\s+(only|upon\s+arrival)?|share\s+delivery\s*pin|pin\s+only\s+upon\s+delivery)\b',
            text_lower
        ))
        has_negative_warning = bool(re.search(
            r'\b(do\s*not|never|don\'?t|strictly\s*not|should\s*not)\s+(share|disclose|give|tell|forward|enter)\b|\bbank\s*never\s*asks?\b',
            text_lower
        ))
        
        # Clean text by removing protective disclaimers
        clean_text = re.sub(r'\b(do\s*not|never|don\'?t|strictly\s*not|should\s*not)\s+(share|disclose|give|tell|forward|enter)\b', '', text_lower)
        clean_text = re.sub(r'\bbank\s*never\s*asks?\b', '', clean_text)
        
        has_extraction_intent = bool(re.search(
            r'\b(ask(ed|ing)?|provide|share|send|give|tell|forward|enter|submit|input|confirm|verify|update|disclose|batao|bhejo|de\s*do|boliye(ga)?|bataiye(ga)?|likho|daalo|need|require|demanding?|what\s+is|please)\b',
            clean_text
        ))
        
        if not is_safe_delivery:
            if has_extraction_intent or (not has_negative_warning and len(text_lower.split()) <= 4):
                badges.append("Credential Theft: OTP / Secret PIN Solicitation")
                matched_categories.append("CREDENTIAL_HARVEST")
                urgency_hits += 2

    # -------------------------------------------------------------
    # 2. UPI PIN TO RECEIVE FRAUD
    # -------------------------------------------------------------
    has_upi_term = bool(re.search(r'\b(upi\s*pin|mpin)\b', text_lower))
    has_qr_term = bool(re.search(r'\b(qr|qr\s*code|merchant\s*qr)\b', text_lower))
    has_receive_intent = bool(re.search(r'\b(receive|claim|accept|credit|cashback|reward|paane|bonus)\b', text_lower))
    
    if (has_upi_term and has_receive_intent) or \
       (has_qr_term and has_receive_intent) or \
       re.search(r'\b(scan\s*qr\s*code\s*to\s*receive|send\s*rs\.?\s*1\s*to\s*verify)\b', text_lower):
        badges.append("Severe UPI PIN / QR Cashback Trap")
        matched_categories.append("UPI_FRAUD")
        urgency_hits += 2

    # -------------------------------------------------------------
    # 3. DIGITAL ARREST & AUTHORITY IMPERSONATION (BNSS 2023)
    # -------------------------------------------------------------
    has_authority = bool(re.search(
        r'\b(cbi|central\s*bureau|police|crime\s*branch|narcotics|ncb|customs|enforcement\s*directorate|\bed\b|nia|trai|rbi|supreme\s*court|interpol|cyber\s*cell|inspector|thanedaar|daroga|adhikari)\b',
        text_lower
    ))
    has_coercion = bool(re.search(
        r'\b(digital\s*arrest|arrest\s*warrant|non-bailable|money\s*laundering|seized|parcel|contraband|mdma|drugs|charas|ganja|illegal\s*courier|fedex|dhl|escrow|court\s*notice|giraftaar|giraftari|jail|case\s*darj|police\s*karyawahi)\b',
        text_lower
    ))
    
    if "digital arrest" in text_lower:
        badges.append("Illegal Digital Arrest Extortion (BNSS 2023)")
        matched_categories.append("IMPERSONATION")
        urgency_hits += 2
    elif has_authority and has_coercion:
        badges.append("Law Enforcement Impersonation & Extortion")
        matched_categories.append("IMPERSONATION")
        urgency_hits += 2
    elif has_authority:
        badges.append("Government/Authority Spoofing")
        matched_categories.append("IMPERSONATION")
        urgency_hits += 1

    # -------------------------------------------------------------
    # 4. ESSENTIAL UTILITY / ELECTRICITY BLACKOUT THREAT
    # -------------------------------------------------------------
    has_utility = bool(re.search(
        r'\b(electricity|bijli|bijli\s*vibhag|bijli\s*office|power|power\s*office|power\s*supply|meter|gas\s*pipeline|water\s*supply|bses|tata\s*power|mahavitaran|uppcl|bescom)\b',
        text_lower
    ))
    has_disconnection = bool(re.search(
        r'\b(disconnect(ed|ing)?|cutoff|line\s*cut|cut|kaat\s*diya|kaat\s*denge|kaat\s*diya\s*jayega|band\s*kar\s*diya\s*jayega|band\s*hoga|terminated|blackout)\b',
        text_lower
    ))
    
    if has_utility and has_disconnection:
        badges.append("Utility Blackout Extortion Threat")
        matched_categories.append("UTILITY_BLACKOUT")
        urgency_hits += 2

    # -------------------------------------------------------------
    # 5. BANKING & KYC SUSPENSION / REWARD EXPIRATION
    # -------------------------------------------------------------
    has_bank = bool(re.search(
        r'\b(sbi|yono|hdfc|icici|axis|pnb|kotak|bank|khata|bank\s*khata|khate|netbanking|credit\s*card|debit\s*card|atm\s*card|sim\s*card|telecom|airtel|jio)\b',
        text_lower
    ))
    has_suspension = bool(re.search(
        r'\b(blocked|suspended|deactivated|freeze|hold|kyc\s*expired|update\s*pan|verify\s*pan|deactivation\s*in|band\s*ho\s*jayega|band\s*kar\s*diya|rok\s*diya)\b',
        text_lower
    ))
    has_generic_kyc = bool(re.search(
        r'\b(kyc\s*(pending|update|expired|required|verification)|update\s*(your\s*)?(pan|aadhaar|kyc)|link\s*(your\s*)?(pan|aadhaar)|aadhaar\s*(link|update)|pan\s*(link|update|jodein)|aadhaar\s*jodein)\b',
        text_lower
    ))
    
    has_reward_trap = bool(re.search(
        r'\b(reward\s*points?.*?(expir|redeem|cash)|redeem.*?(points?|cash|voucher)|points?.*?expir(ing|ed|e))\b',
        text_lower
    ))
    
    if (has_bank and has_suspension) or has_generic_kyc or has_reward_trap:
        badges.append("Banking KYC / Reward Points Phishing")
        matched_categories.append("BANKING_PHISHING")
        urgency_hits += 1

    # -------------------------------------------------------------
    # 5B. ACCOUNT VERIFICATION & GENERIC PHISHING LINK LURES
    # -------------------------------------------------------------
    if re.search(r'\b(click\s+(this\s+)?(link|here|below)\s+(to\s+)?verify|verify\s+(your\s+)?(account|identity|details)|login\s+to\s+verify|update\s+billing)\b', text_lower):
        badges.append("Suspicious Account Verification / Phishing Link Lure")
        matched_categories.append("PHISHING_LINK")
        urgency_hits += 1

    # -------------------------------------------------------------
    # 5C. UNSOLICITED MONEY DEMANDS
    # -------------------------------------------------------------
    if re.search(r'\b(send\s+(me\s+)?money|transfer\s+(me\s+)?money|give\s+(me\s+)?money|paise\s+(bhejo|transfer|do))\b', text_lower):
        badges.append("Unsolicited Advance Money Transfer Request")
        matched_categories.append("SUSPICIOUS_PAYMENT")
        urgency_hits += 1

    # -------------------------------------------------------------
    # 6. PREDATORY LOAN APKS, MALWARE PAYLOADS & ADVANCE FEE LOAN TRAPS
    # -------------------------------------------------------------
    has_apk = bool(re.search(r'\.apk\b|\b(install|download)\s+.*?\bapk\b', text_lower))
    has_loan = bool(re.search(r'\b(instant\s*loan|0%\s*interest|zero\s*cibil|no\s*cibil|pre-approved\b.*?\bloan|loan\s*recovery|recovery\s*agent|blackmail\s*contacts)\b', text_lower))
    has_advance_loan_fee = bool(re.search(
        r'\b(loan|sanction|disbursal)\b.*?\b(processing\s*fee|security\s*fee|file\s*charge|disbursal\s*fee|refundable\s*(security|fee)|clearance\s*charge)\b|\b(processing\s*fee|security\s*fee|file\s*charge|refundable\s*(security|fee))\b.*?\b(loan|disbursal|disbursed)\b',
        text_lower
    ))
    has_malware_file = bool(re.search(r'\.(exe|bat|scr|vbs|iso)\b', text_lower))

    if has_apk:
        badges.append("Dangerous Android APK Malware Payload")
        matched_categories.append("MALICIOUS_PAYLOAD")
        urgency_hits += 2
    if has_malware_file:
        badges.append("Executable Malware Payload Link")
        matched_categories.append("MALICIOUS_PAYLOAD")
        urgency_hits += 2
    if has_loan or has_advance_loan_fee:
        if has_advance_loan_fee:
            badges.append("Advance Fee Loan Fraud / Upfront Deposit Trap")
        else:
            badges.append("Predatory Blackmail Loan App Trap")
        matched_categories.append("LOAN_TRAP")
        urgency_hits += 1

    # -------------------------------------------------------------
    # 7. GAMING PHISHING & YOUTH BAIT
    # -------------------------------------------------------------
    has_game_term = bool(re.search(
        r'\b(bgmi|pubg|free\s*fire|robux|roblox|discord\s*nitro|steam|valorant|genshin)\b',
        text_lower
    ))
    has_game_bait = bool(re.search(
        r'\b(free\s*(uc|diamonds?|robux|nitro|skins?|gift\s*card|pass|drop)|giveaway|claim\s*(code|diamonds?|uc|robux)|unlimited\s*(uc|diamonds?))\b',
        text_lower
    ))
    if has_game_bait or (has_game_term and re.search(r'\b(free|drop|gift|claim|airdrop|hack)\b', text_lower)):
        badges.append("Youth Gaming Bait / Credential Theft")
        matched_categories.append("GAMING_BAIT")
        urgency_hits += 1

    # -------------------------------------------------------------
    # 8. PART-TIME TASK & JOB FRAUD
    # -------------------------------------------------------------
    has_job_term = bool(re.search(
        r'\b(job|work\s*from\s*home|part\s*time|online\s*work|daily\s*task|rating\s*job|hiring|vacancy|naukri|kam\s*karein|ghar\s*baithe|rating\s*work)\b',
        text_lower
    ))
    has_job_lure = bool(re.search(
        r'\b(earn\s*(\d+|daily|money|rs)|daily\s*(\d+\s*)?(payout|income|salary|earning|payment)|(youtube|video)\s*like|like\s*(youtube\s*)?videos?|(hotel|google)\s*(rating|review)|google\s*maps?\s*rating|telegram\s*(task|channel)|product\s*rating|deposit\s*to\s*earn|kamao|kamayein|paisa\s*kamao|daily\s*kamai|roz\s*kamayein)\b',
        text_lower
    ))
    if has_job_lure or (has_job_term and re.search(r'\b(earn\s*\d+|daily\s*income|no\s*experience|daily\s*payout|telegram|kamayein|kamao|bank\s*transfer|earning|rating)\b', text_lower)):
        badges.append("Unsolicited Task / Part-Time Job Scam")
        matched_categories.append("JOB_SCAM")
        urgency_hits += 1

    # -------------------------------------------------------------
    # 9. LOTTERY, PRIZE & KBC FRAUD
    # -------------------------------------------------------------
    has_lottery_term = bool(re.search(
        r'\b(lottery|lucky\s*draw|jackpot|bumper\s*prize|mega\s*prize|kbc|cash\s*prize|reward\s*money|contest\s*prize|gift\s*hamper|inam|puraskar|bumper\s*inam)\b',
        text_lower
    ))
    has_win_intent = bool(re.search(
        r'\b(won|win(ner)?|selected|claim|receive|collect|awarded|chosen|congrat(ulation)?s?|j(ee|i)t(a|e|i)|chuna\s*gaya|mubarak|badhai)\b',
        text_lower
    ))
    if has_lottery_term and has_win_intent:
        badges.append("Unsolicited Lottery / Prize Fraud")
        matched_categories.append("LOTTERY_FRAUD")
        urgency_hits += 2
    elif re.search(r'\b(won\s*(rs\.?|\d+)\s*(lakhs?|crore)|kbc.*lucky\s*draw|lottery.*winner|whatsapp\s*lucky\s*draw)\b', text_lower):
        badges.append("Unsolicited Lottery / Prize Fraud")
        matched_categories.append("LOTTERY_FRAUD")
        urgency_hits += 2
        
    # Unclaimed inheritance / foreign estate advance fee fraud
    has_inheritance_term = bool(re.search(
        r'\b(unclaimed\s*(deposit|fund|estate|inheritance|money)|foreign\s*beneficiary|probate\s*(registry|fee|court)|next\s*of\s*kin|estate\s*of\s*late|inheritance\s*fund)\b',
        text_lower
    ))
    if has_inheritance_term:
        badges.append("Unclaimed Inheritance / Foreign Estate Fraud")
        matched_categories.append("LOTTERY_FRAUD")
        urgency_hits += 2

    # -------------------------------------------------------------
    # 10. TAX REFUND & CORPORATE EMAIL PHISHING (BEC)
    # -------------------------------------------------------------
    if re.search(r'\b(income\s*tax|it\s*department|tax\s*department|gst|tds).*?(refund|notice|penalty|demand|discrepancy|approved)\b', text_lower) or \
       re.search(r'\b(tax\s*refund|tds\s*refund|excess\s*tax)\b', text_lower):
        badges.append("Government Tax Refund Phishing Lure")
        matched_categories.append("TAX_PHISHING")
        urgency_hits += 1
    if re.search(r'\b(office\s*365|microsoft\s*365|corporate\s+email|vpn\s+certificate|sso\s+credentials).*?expir\w*\b', text_lower):
        badges.append("Corporate Credential Harvesting")
        matched_categories.append("EMAIL_PHISHING")
        urgency_hits += 1

    # -------------------------------------------------------------
    # 10B. FREE WEBMAIL SPOOFING ON OFFICIAL / FINANCIAL ENTITIES
    # -------------------------------------------------------------
    from_match = re.search(r'^from:\s*(.+)$', text, re.IGNORECASE | re.MULTILINE)
    has_free_webmail = bool(re.search(r'[a-zA-Z0-9.\-_]+@(gmail|yahoo|hotmail|outlook|rediffmail|live|protonmail)\.com\b', text_lower))
    official_authority_regex = r'\b(income\s*tax|it\s*department|cbi|police|customs|rbi|trai|sbi|hdfc|icici|axis|bank(\s+(support|service|care|centre|center|alert|security|branch))?|microsoft|office\s*365|apple\s*support|ceo|managing\s*director|barrister|fedex|dhl)\b'

    is_webmail_spoof = False
    if has_free_webmail:
        if from_match:
            from_line = from_match.group(1).lower()
            if re.search(r'@(gmail|yahoo|hotmail|outlook|rediffmail|live|protonmail)\.com\b', from_line) and \
               re.search(official_authority_regex, from_line):
                is_webmail_spoof = True
        if not is_webmail_spoof and re.search(r'\b(official\s+(notice|notification|summons|communication)|we\s+are\s+(from|writing\s+from)|this\s+is\s+(the\s+)?(official\s+)?(customer\s*care|fraud\s*control|investigation\s*cell|cyber\s*cell|customs\s*office|income\s*tax|support\s*team))\b', text_lower):
            if re.search(official_authority_regex, text_lower) and not re.search(r'\b(my\s+email|send\s+to\s+my|contact\s+me\s+at)\b', text_lower):
                is_webmail_spoof = True

    if is_webmail_spoof:
        badges.append("Official Entity Impersonation on Free Webmail")
        matched_categories.append("EMAIL_PHISHING")
        urgency_hits += 2

    # -------------------------------------------------------------
    # 11. SEXTORTION & VIDEO CALL BLACKMAIL
    # -------------------------------------------------------------
    has_blackmail_media = bool(re.search(
        r'\b(video\s*call|private\s*(video|photo|pic|recorded|call)s?|nude\s*(video|photo|pic)s?|recorded\s*(your|video|call|audio)|shared\s*with\s*(all\s*)?(contacts|family|friends)|viral\s*on\s*(youtube|social|facebook|instagram)|send\s*to\s*(your\s*)?(family|friends|contacts)|viral\s*kar\s*(denge|dunga)|gharwalon\s*ko\s*bhejo)\b',
        text_lower
    ))
    has_blackmail_demand = bool(re.search(
        r'\b(pay|money|viral|delete|recording|rupees|transfer|leak|ruin|paise\s*bhejo|rupaye\s*transfer|warna\s*viral|(send|transfer|pay)\s*(\d+|rs|money))\b',
        text_lower
    ))
    if has_blackmail_media and has_blackmail_demand:
        badges.append("Video Call Sextortion & Defamation Blackmail")
        matched_categories.append("BLACKMAIL")
        urgency_hits += 2

    # -------------------------------------------------------------
    # 12. SUSPICIOUS PAYMENT & UNTRUSTED DOMAINS
    # -------------------------------------------------------------
    if re.search(r'[a-zA-Z0-9.\-_]+@(okaxis|ybl|paytm|apl|okhdfcbank|oksbi)\b', text_lower):
        badges.append("Direct Peer-to-Peer UPI Payment Handle")
        matched_categories.append("SUSPICIOUS_PAYMENT")
    if re.search(r'\b[a-zA-Z0-9\-_]+\.(xyz|top|online|site|link|info|me|click|club|live|tk|ml|ga|cf|gq|cc|work|rest)\b', text_lower):
        badges.append("Suspicious Free / Low-Trust Domain Extension")
        matched_categories.append("SUSPICIOUS_DOMAIN")
        urgency_hits += 1
    if re.search(r'http://[^\s]+\b', text_lower):
        badges.append("Insecure Plaintext HTTP Link")
        matched_categories.append("INSECURE_LINK")

    # -------------------------------------------------------------
    # 12B. FAKE COURIER / DELIVERY FEE EXTORTION
    # -------------------------------------------------------------
    # Exclude authentic food orders, grocery receipts, and e-commerce delivery confirmations
    is_legit_receipt = bool(re.search(
        r'\b(swiggy|zomato|order\s*#|delivered\s*(to|at)|delivery\s*partner|items\s*(ordered|delivered)|enjoy\s*your\s*(food|meal)|subtotal|grand\s*total|taxes\s*included)\b',
        text_lower
    ))
    
    has_courier = bool(re.search(r'\b(courier|parcel|consignment|india\s*post|fedex|dhl|bluedart|dtdc)\b', text_lower))
    has_courier_extortion = bool(re.search(
        r'\b(customs\s*(fee|duty|clearance|penalty|hold)|clearance\s*fee|unregistered\s*(shipment|parcel)|(parcel|consignment|package)\s*(on\s*hold|held|seized)|(pay|transfer)\s*.*(release|customs|delivery\s*fee\s*to\s*receive))\b',
        text_lower
    ))
    
    if not is_legit_receipt and (has_courier and has_courier_extortion):
        badges.append("Fake Delivery / Courier Fee Extortion")
        matched_categories.append("SUSPICIOUS_PAYMENT")
        urgency_hits += 1

    # -------------------------------------------------------------
    # 13. HINGLISH REGIONAL COERCION
    # -------------------------------------------------------------
    if re.search(r'\b(turant|aaj\s*raat|kaat\s*diya\s*jayega|band\s*ho\s*jayega|police\s*karyawahi|police\s*ghar\s*aayegi|giraftaar|jail\s*jana|kanooni\s*karyawahi|court\s*mein\s*pesh|warna\s*nuksan|case\s*darj|fir\s*darj|chalaan|jurmana)\b', text_lower):
        badges.append("Regional Hinglish Coercion / Intimidation")
        matched_categories.append("HINGLISH_COERCION")
        urgency_hits += 1

    # Calibrate urgency score
    raw_score = (urgency_hits * 0.25) + (len(matched_categories) * 0.15)
    urgency_score = min(1.0, round(raw_score, 2))

    unique_badges = list(dict.fromkeys(badges))
    return {
        "is_suspicious": len(unique_badges) > 0,
        "urgency_score": urgency_score,
        "matched_categories": list(dict.fromkeys(matched_categories)),
        "badges": unique_badges,
        "rule_hit_count": len(unique_badges),
    }

if __name__ == "__main__":
    test_msg = "Dear consumer your electricity power will be disconnected tonight at 9:30 PM. Pay pending bill immediately to UPI: bses@okaxis"
    print("Test Heuristics Evaluation:")
    result = evaluate_heuristics(test_msg)
    for k, v in result.items():
        print(f"  {k}: {v}")
