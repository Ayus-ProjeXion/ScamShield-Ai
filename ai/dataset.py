"""
ScamShield AI — Curated Threat & Safe Message Corpus
Covers real-world Indian cyber-fraud vectors and benign communications.
"""

from typing import List, Tuple

# Label 1 = SCAM / FRAUD, Label 0 = SAFE / BENIGN
TRAINING_SAMPLES: List[Tuple[str, int, str]] = [
    # --- PHISHING & SMISHING (Label: 1) ---
    ("Dear customer, please share your 6-digit OTP to verify your account or netbanking will be suspended.", 1, "OTP_SOLICITATION"),
    ("I asked for OTP to verify your instant loan approval of Rs 5,00,000. Send immediately.", 1, "OTP_SOLICITATION"),
    ("Caller asked for my OTP claiming to be Mumbai Police Cyber Cell officer.", 1, "OTP_SOLICITATION"),
    ("Sir apna OTP batao turant warna account freeze kar diya jayega bank manager dwara.", 1, "OTP_SOLICITATION"),
    ("Enter your UPI PIN to claim scratch card cashback of Rs 2,500 directly in account.", 1, "PIN_EXTRACTION"),
    ("Dear SBI user, your YONO account will be blocked today due to pending KYC. Click http://sbi-kyc-update.xyz to update Pan Card immediately.", 1, "BANKING_PHISHING"),
    ("URGENT: Your HDFC netbanking access is suspended! Login to http://hdfc-verify-access.top to verify your debit card credentials.", 1, "BANKING_PHISHING"),
    ("Dear ICICI customer, 25,000 reward points expiring in 24 hours. Redeem cash Rs.12,500 now at http://icici-points-cash.online", 1, "REWARD_PHISHING"),
    ("Axis Bank Alert: Unauthorized transaction of Rs 49,999 detected. If not done by you, cancel immediately at http://axis-dispute-portal.link", 1, "BANKING_PHISHING"),
    ("Dear customer your SIM card will be deactivated in 24 hrs by TRAI due to incomplete verification. Call 9876543210 or click http://trai-verify.info", 1, "TELECOM_PHISHING"),
    ("Your PNB credit card has been blocked due to suspicious activity. Visit http://pnb-card-reactivate.site to restore access.", 1, "BANKING_PHISHING"),
    ("Kotak Bank: Dear user your KYC has expired. Download our quick verification APK from http://kotak-quick-verify.apk to avoid fine of Rs 5000.", 1, "MALICIOUS_APP"),
    ("Your Netflix subscription payment failed! Account on hold. Update billing immediately: http://netflix-billing-renew.me", 1, "CREDENTIAL_HARVESTING"),

    # --- ELECTRICITY & UTILITY CUTOFF FRAUD (Label: 1) ---
    ("Dear Consumer, your electricity power will be disconnected tonight at 9:30 PM from the power office because your previous month bill was not updated. Please immediately contact our electricity officer Mr. Sharma at 9876543210. Thank you.", 1, "ELECTRICITY_CUTOFF"),
    ("URGENT NOTICE: BSES Power disconnection order issued for meter #48291. Power will be cut in 2 hours. Pay pending bill of Rs. 1420 to UPI officer: bses-billing@okaxis", 1, "ELECTRICITY_CUTOFF"),
    ("Tata Power Alert: Your home electric supply will be terminated today at 8:00 PM due to unpaid surcharge. Call power manager 8765432109 immediately to avoid blackout.", 1, "ELECTRICITY_CUTOFF"),
    ("Mahavitaran warning: Tonight 9 PM power line cutoff scheduled for non-payment. Update receipt on WhatsApp 9123456789 or power will be terminated permanently.", 1, "ELECTRICITY_CUTOFF"),
    ("Urgent: Gas pipeline supply to your flat will be stopped today at 6 PM. Pay security deposit on UPI indanegas@ybl or connection cancelled.", 1, "UTILITY_FRAUD"),

    # --- DIGITAL ARREST & EXTORTION CALL TRANSCRIPTS (Label: 1) ---
    ("Hello, this is Inspector Vikram Rathore from Mumbai Crime Branch. We have seized a FedEx international courier containing 5 passports and 140 grams of MDMA drugs linked to your Aadhaar card. You are under digital arrest. Transfer Rs. 2,00,000 to government escrow account for verification or local police will arrive in 30 minutes.", 1, "DIGITAL_ARREST_EXTORTION"),
    ("This is Customs Department at New Delhi IGI Airport. An illegal parcel in your name from Taiwan has been intercepted. The parcel has narcotics and counterfeit money. You are facing an arrest warrant. Connect to CBI video call immediately.", 1, "DIGITAL_ARREST_EXTORTION"),
    ("Greetings from Supreme Court of India. A legal notice and non-bailable warrant has been registered under your PAN number for money laundering. Contact Cyber Police officer immediately or your bank accounts will be frozen today.", 1, "DIGITAL_ARREST_EXTORTION"),
    ("FedEx automated security alert: Your parcel to Cambodia is on hold due to prohibited chemicals. Press 9 to speak with Mumbai Narcotics officer immediately.", 1, "DIGITAL_ARREST_EXTORTION"),

    # --- LOTTERY, PART-TIME JOB & UPI FRAUDS (Label: 1) ---
    ("Congratulations! You won Rs. 25,00,000 in Kaun Banega Crorepati WhatsApp lucky draw #7821. Contact KBC manager Rana Pratap on 9823456781 to claim prize after paying registration fee Rs. 1,500.", 1, "LOTTERY_FRAUD"),
    ("Work from home opportunity! Earn Rs 3,000 to Rs 8,000 daily by just liking YouTube videos and rating Google Maps. No experience needed. Join Telegram: t.me/earn_daily_cash", 1, "JOB_SCAM"),
    ("Amazon HR hiring! Part-time product review job. Daily payout Rs 5,000 directly to UPI. Deposit refundable training fee of Rs 500 to begin: amazon-jobs@paytm", 1, "JOB_SCAM"),
    ("You received a cashback reward of Rs 2,499 from Google Pay! Click here to accept into your bank account: http://gpay-reward-claim.top/accept", 1, "UPI_FRAUD"),
    ("Dear PhonePe user, send Rs 1 to UPI verify-cashback@ybl to instantly unlock your scratch card worth Rs 1,999.", 1, "UPI_FRAUD"),

    # --- SAFE & BENIGN MESSAGES (Label: 0) ---
    ("Your SBI OTP for login is 482910. Valid for 5 minutes. Do not share this OTP with anyone, including bank staff.", 0, "SAFE_OTP"),
    ("HDFC Bank: Rs. 1,450.00 debited from account **4821 on 22-NOV-26 at SWIGGY BANGALORE. Available balance: Rs. 34,210.00.", 0, "SAFE_TRANSACTION"),
    ("Hey bro, are we meeting at the cafe around 6 PM today? Let me know if you are free.", 0, "SAFE_CHAT"),
    ("Mom, I have reached the airport safely. Boarding starts at 7:15 PM. Will call you once I land.", 0, "SAFE_CHAT"),
    ("Your Zomato order from Biryani Blues is on the way! Delivery partner Ramesh is arriving in 12 mins.", 0, "SAFE_DELIVERY"),
    ("Amazon: Your package containing 'Wireless Mouse' has been delivered to your front door. Rate your delivery.", 0, "SAFE_DELIVERY"),
    ("Flipkart: Out for delivery! Your order will be delivered by 8 PM today by delivery agent Rahul (Call: 9811223344). Share OTP 4491 only upon delivery.", 0, "SAFE_DELIVERY"),
    ("Hi Ayusman, please review the pull request for the database schema when you get some time. Thanks!", 0, "SAFE_WORK"),
    ("Reminder: Doctor appointment with Dr. Mehta scheduled for tomorrow Monday at 10:30 AM at Apollo Hospital.", 0, "SAFE_UTILITY"),
    ("Airtel Thanks: Your daily 1.5 GB data quota has reached 50%. Recharge with Rs 19 to get 1GB additional data.", 0, "SAFE_TELECOM"),
    ("Can you please send me the class notes for today's machine learning lecture? Missed the first 20 minutes.", 0, "SAFE_CHAT"),
    ("ICICI Bank: Statement for your Savings Account **9012 for the month of October 2026 is ready to view on iMobile app.", 0, "SAFE_STATEMENT"),
    ("Uber: Your ride with driver Satish is confirmed. Vehicle: White Swift Dzire (DL 1Z A 4821). PIN: 2910.", 0, "SAFE_RIDE"),
    ("Hey guys, the hackathon presentation is on Dec 6. Let's do a sync call tonight at 9 PM on Google Meet.", 0, "SAFE_WORK"),
    ("Your electricity bill for consumer #982104 has been generated. Amount: Rs 1,120. Due date: 05-DEC-2026. Pay via official portal at https://www.bsesdelhi.com", 0, "SAFE_BILL"),
    ("Good morning! Hope you have a wonderful day ahead.", 0, "SAFE_GREETING"),
    ("Happy Birthday bro! Wishing you great success, good health and happiness always.", 0, "SAFE_GREETING"),
    ("Did you finish watching the football match last night? What an incredible comeback in extra time!", 0, "SAFE_CHAT"),
    ("Please find attached the project report and presentation slides for tomorrow's review meeting.", 0, "SAFE_WORK"),
    ("Hey dad, I submitted my assignment on the university portal. Heading home now.", 0, "SAFE_CHAT"),
    ("Can we reschedule our meeting to 4 PM? Something came up with the client.", 0, "SAFE_WORK"),
    ("Thanks for helping me with the code earlier, really appreciate it!", 0, "SAFE_CHAT"),
    ("Your appointment at the dental clinic is confirmed for Saturday at 11 AM.", 0, "SAFE_UTILITY"),
    ("Blinkit: Your grocery delivery has been placed successfully. Order will arrive in 9 minutes.", 0, "SAFE_DELIVERY"),
    ("Hey, don't forget to bring your laptop charger tomorrow for the hackathon session.", 0, "SAFE_CHAT"),
    ("Great job on the presentation today, everyone was impressed with the live demo!", 0, "SAFE_CHAT"),
    ("Hey sister, can you send me the Wi-Fi password for the router?", 0, "SAFE_CHAT"),
    ("Let's order some pizza for lunch while we finish writing the backend APIs.", 0, "SAFE_CHAT"),
    ("College notice: Semester end examinations will commence from December 15. Check student portal for hall tickets.", 0, "SAFE_UTILITY"),
    ("Your train ticket for PNR 2849102849 is confirmed. Coach B3, Berth 42 (Side Lower). Have a safe journey.", 0, "SAFE_TRAVEL"),
]

import os
import csv
from typing import List, Tuple

DATA_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "full_scam_training_corpus.csv")

def get_training_data() -> Tuple[List[str], List[int], List[str]]:
    """
    Returns texts, labels, and categories.
    Prefers the full aggregated dataset (5,600+ samples) when available.
    """
    if os.path.exists(DATA_CSV):
        texts, labels, sources = [], [], []
        try:
            with open(DATA_CSV, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if len(row) >= 3:
                        texts.append(row[0])
                        labels.append(int(row[1]))
                        sources.append(row[2])
            if texts:
                return texts, labels, sources
        except Exception:
            pass

    # Fallback to curated in-memory samples
    texts = [sample[0] for sample in TRAINING_SAMPLES]
    labels = [sample[1] for sample in TRAINING_SAMPLES]
    categories = [sample[2] for sample in TRAINING_SAMPLES]
    return texts, labels, categories
