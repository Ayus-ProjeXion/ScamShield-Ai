"""
ScamShield AI — Test Screenshot Generator
Generates realistic, high-contrast mobile/desktop screenshot test cases in test_screenshots/
for demonstrating the multi-modal on-device OCR Threat Scanner.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "test_screenshots"
PUBLIC_DIR = os.path.join("frontend", "public", "test_screenshots")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PUBLIC_DIR, exist_ok=True)

# Select best available Windows font
FONT_PATH = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "segoeui.ttf")
if not os.path.exists(FONT_PATH):
    FONT_PATH = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "arial.ttf")

def get_font(size: int, bold: bool = False):
    try:
        if bold:
            bold_path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "segoeuib.ttf")
            if os.path.exists(bold_path):
                return ImageFont.truetype(bold_path, size)
            arial_bold = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "arialbd.ttf")
            if os.path.exists(arial_bold):
                return ImageFont.truetype(arial_bold, size)
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def create_card_image(
    filename: str,
    title: str,
    badge_text: str,
    lines: list,
    header_color: tuple = (255, 111, 50),
    is_safe: bool = False
):
    # Standard mobile card dimensions (720x960)
    width, height = 720, 960
    bg_color = (248, 249, 250) if is_safe else (255, 255, 255)
    
    img = Image.new("RGB", (width, height), color=(235, 238, 242))
    draw = ImageDraw.Draw(img)
    
    # Outer Card
    margin = 30
    draw.rounded_rectangle(
        [(margin, margin), (width - margin, height - margin)],
        radius=20,
        fill=bg_color,
        outline=(210, 215, 222),
        width=2
    )
    
    # Card Header Banner
    header_h = 100
    banner_color = (34, 197, 94) if is_safe else header_color
    draw.rounded_rectangle(
        [(margin, margin), (width - margin, margin + header_h)],
        radius=20,
        fill=banner_color
    )
    # Fix bottom corners of header
    draw.rectangle([(margin, margin + 40), (width - margin, margin + header_h)], fill=banner_color)
    
    # Header Title
    title_font = get_font(26, bold=True)
    draw.text((margin + 25, margin + 25), title, font=title_font, fill=(255, 255, 255))
    
    badge_font = get_font(16, bold=True)
    badge_bg = (20, 83, 45) if is_safe else (153, 27, 27)
    draw.rounded_rectangle(
        [(margin + 25, margin + 62), (margin + 200, margin + 88)],
        radius=8,
        fill=badge_bg
    )
    draw.text((margin + 35, margin + 65), badge_text, font=badge_font, fill=(255, 255, 255))
    
    # Content Lines
    y = margin + header_h + 35
    body_font = get_font(21, bold=False)
    bold_body = get_font(21, bold=True)
    
    for item in lines:
        if isinstance(item, tuple):
            prefix, text = item
            draw.text((margin + 30, y), prefix, font=bold_body, fill=(24, 24, 27))
            offset_x = margin + 30 + int(draw.textlength(prefix, font=bold_body)) + 8
            draw.text((offset_x, y), text, font=body_font, fill=(55, 65, 81))
            y += 42
        elif item == "---":
            draw.line([(margin + 25, y + 10), (width - margin - 25, y + 10)], fill=(229, 231, 235), width=2)
            y += 28
        else:
            draw.text((margin + 30, y), item, font=body_font, fill=(55, 65, 81))
            y += 38
            
    # Bottom Verified / Anti-Tamper Bar
    bottom_y = height - margin - 50
    draw.line([(margin + 25, bottom_y), (width - margin - 25, bottom_y)], fill=(229, 231, 235), width=1)
    footer_font = get_font(14, bold=False)
    footer_text = "ScamShield AI • Verified Forensic Test Case • On-Device OCR Benchmark"
    draw.text((margin + 30, bottom_y + 16), footer_text, font=footer_font, fill=(156, 163, 175))
    
    # Save to test_screenshots/ and frontend/public/test_screenshots/
    primary_path = os.path.join(OUTPUT_DIR, filename)
    public_path = os.path.join(PUBLIC_DIR, filename)
    img.save(primary_path, "PNG")
    img.save(public_path, "PNG")
    print(f"[✓] Generated: {primary_path} ({width}x{height})")

def main():
    print("=" * 70)
    print("🛡️  SCAMSHIELD AI — TEST SCREENSHOT GENERATOR")
    print("=" * 70)
    
    # 1. Digital Arrest CBI Legal Threat
    create_card_image(
        filename="scam_whatsapp_cbi_digital_arrest.png",
        title="CENTRAL BUREAU OF INVESTIGATION (CBI)",
        badge_text="🚨 IMMEDIATE ARREST",
        header_color=(220, 38, 38),
        lines=[
            ("AGENCY:", "Cyber Crime Cell & Narcotics Interception Bureau"),
            ("CASE NO:", "CBI-DEL-2026-9912 / FIR-302"),
            ("TO ACCUSED:", "Citizen Identity Verification Hold"),
            "---",
            "FINAL LEGAL WARNING FOR NARCOTICS CONSIGNMENT",
            "",
            "A consignment with your Aadhaar ID was seized at Delhi Airport.",
            "Contents seized: 140g MDMA narcotics and 5 counterfeit passports.",
            "",
            ("STATUS:", "YOU ARE UNDER IMMEDIATE DIGITAL ARREST."),
            "",
            "Do NOT disconnect this communication or transfer to anyone.",
            "Local police and flying squad will raid your residential premises.",
            "",
            ("CALL DESK:", "+91 98765 43210 immediately for verification."),
            ("MANDATE:", "Pay surety clearance fee of Rs 48,500 to official escrow.")
        ]
    )

    # 2. Electricity KYC Disconnection Scam
    create_card_image(
        filename="scam_electricity_bill_cutoff.png",
        title="MAHAVITARAN ELECTRICITY BOARD",
        badge_text="⚡ URGENT BLACKOUT",
        header_color=(234, 88, 12),
        lines=[
            ("UTILITY:", "Maharashtra State Electricity Distribution Co. (MSEDCL)"),
            ("CONSUMER NO:", "028471920194 (Subdivision Central)"),
            ("BILL AMOUNT:", "Rs 1,840.00 (Pending Verification)"),
            "---",
            "IMMEDIATE POWER DISCONNECTION NOTICE",
            "",
            "Dear Consumer, your Bijli (Electricity) bill was not updated.",
            "Power supply will be DISCONNECTED TONIGHT at 09:30 PM",
            "by the local Electricity Officer.",
            "",
            ("ACTION REQUIRED:", "Immediately call Officer at 9876543210."),
            "",
            "To avoid immediate blackout and disconnection fee:",
            "Install MahaVitaran_Update.apk to verify your UPI payment.",
            "Link: http://bit.ly/mhavitaran-bill-verify"
        ]
    )

    # 3. WhatsApp Work-From-Home Job Scam
    create_card_image(
        filename="scam_whatsapp_part_time_job.png",
        title="GLOBAL MARKETING ALLIANCE LTD",
        badge_text="💼 PREPAID TASK TRAP",
        header_color=(202, 138, 4),
        lines=[
            ("RECRUITER:", "Jessica from Global YouTube Media Talent"),
            ("OFFER:", "Part-Time YouTube Video Review Partner"),
            ("DAILY INCOME:", "Rs 3,000 - 8,000 / Day (Work From Home)"),
            "---",
            "DAILY TASK RECRUITMENT PROGRAM",
            "",
            "Hi Dear, simple work! Just like 3 YouTube videos per task.",
            "Earn Rs 150 per like, paid instantly to your bank account.",
            "",
            ("NEXT STEP:", "Deposit registration fee of Rs 1,500 to activate wallet."),
            ("UPI ID:", "taskdeposit@icici (Merchant Escrow Account)"),
            "",
            "Immediate withdrawal guaranteed right after task completion!",
            "Join our official Telegram VIP group: t.me/vip_task_earn"
        ]
    )

    # 4. Fake Payment App Screenshot (Google Pay / PhonePe)
    create_card_image(
        filename="scam_fake_upi_payment_receipt.png",
        title="GOOGLE PAY — PAYMENT CONFIRMATION",
        badge_text="💳 SPOOFED RECEIPT",
        header_color=(37, 99, 235),
        lines=[
            ("PAYMENT TO:", "Sharma Electronic Retail Store"),
            ("UPI ID:", "customsclear@axis (Disguised Personal VPA)"),
            ("AMOUNT PAID:", "INR 24,500.00"),
            ("TXN ID:", "UPI-Ref-438901928120 on 26-Nov-2026"),
            "---",
            "TRANSACTION NOTICE & HOLD STATUS",
            "",
            "Payment is currently ON HOLD at Mumbai Customs clearance gateway.",
            "Overseas consignment #FX-884012 requires clearance fee.",
            "",
            ("ESCROW NOTICE:", "Pay balance to UPI customsclear@axis."),
            "Pay within 40 minutes to avoid MHA FIR registration.",
            "Verify portal: http://customs-clearance-desk.online"
        ]
    )

    # 5. Safe Swiggy Delivery Receipt (Zero False Alarm)
    create_card_image(
        filename="safe_swiggy_delivery_receipt.png",
        title="SWIGGY — ORDER RECEIPT #SW-881920",
        badge_text="✅ SAFE ORDER",
        header_color=(34, 197, 94),
        is_safe=True,
        lines=[
            ("MERCHANT:", "Punjab Grill Restaurant (Bandra West)"),
            ("DELIVERED TO:", "Flat 402, Galaxy Apartments, Mumbai"),
            ("PAYMENT METHOD:", "Google Pay UPI (A/C XX1290)"),
            "---",
            "ITEMS DELIVERED:",
            "• 1x Paneer Butter Masala (Rs 280.00)",
            "• 2x Butter Naan (Rs 90.00)",
            "• Packaging & Delivery Charge (Rs 50.00)",
            "",
            ("TOTAL PAID:", "INR 420.00 (Taxes Included)"),
            "",
            ("DELIVERY PARTNER:", "Rahul Kumar (Rating: 4.9 ★)"),
            "Status: Delivered at 12:45 PM on 26-Nov-2026.",
            "",
            "Enjoy your food! Need help? Contact Swiggy in-app support."
        ]
    )

    # 6. Safe Bank Transaction Notification (Zero False Alarm)
    create_card_image(
        filename="safe_bank_transaction_alert.png",
        title="HDFC BANK — OFFICIAL TRANSACTION ALERT",
        badge_text="✅ SAFE BANK ALERT",
        header_color=(34, 197, 94),
        is_safe=True,
        lines=[
            ("ACCOUNT:", "Savings Account XX1290"),
            ("TRANSACTION:", "ATM Cash Withdrawal"),
            ("AMOUNT:", "INR 2,500.00 Debited"),
            ("DATE/TIME:", "26-Nov-2026 at 11:42 AM IST"),
            ("LOCATION:", "ATM HDFC001 - Bandra West Branch"),
            "---",
            ("AVAILABLE BALANCE:", "INR 34,210.45"),
            "",
            "If this transaction was done by you, no action is needed.",
            "",
            "If this transaction was NOT done by you, immediately call",
            "HDFC Bank official toll-free customer care at 18002664332",
            "or visit our official website at https://www.hdfcbank.com."
        ]
    )
    
    print("=" * 70)
    print("🎉 All 6 test screenshots successfully generated in:")
    print("   • ./test_screenshots/")
    print("   • ./frontend/public/test_screenshots/")
    print("=" * 70)

if __name__ == "__main__":
    main()
