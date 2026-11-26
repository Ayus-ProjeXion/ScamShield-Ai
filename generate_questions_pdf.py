"""
∀VITR AI — Comprehensive Technical Q&A & Evaluator Defense Guide Generator
Generates a publication-grade, professionally styled PDF containing all the core architectural
and technical questions asked by evaluators, judges, and developers with complete examples.

Saves to:
- questions/Questions_That_Can_Be_Asked.pdf
- C:\\Users\\HP\\OneDrive\\Desktop\\Questions_That_Can_Be_Asked.pdf
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(36, 756, "∀VITR AI (अवितृ) — COMPREHENSIVE TECHNICAL DEFENSE & EVALUATOR Q&A")
            self.setStrokeColor(colors.HexColor('#E2E8F0'))
            self.setLineWidth(0.75)
            self.line(36, 750, letter[0] - 36, 750)
            
        # Footer (all pages)
        self.setFont("Helvetica", 8)
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 36, 20, footer_text)
        self.drawString(36, 20, "CONFIDENTIAL — FOR ACADEMIC JURY, EVALUATOR DEFENSE & TECHNICAL AUDIT")
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.75)
        self.line(36, 30, letter[0] - 36, 30)
        self.restoreState()

def build_pdf(output_paths):
    for path in output_paths:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
    primary_path = output_paths[0]
    doc = SimpleDocTemplate(
        primary_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A')
    )

    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#475569')
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=4
    )

    q_style = ParagraphStyle(
        'Question',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor('#EA580C') # Saffron/Orange accent
    )

    ans_style = ParagraphStyle(
        'Answer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#1E293B')
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0F172A')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#FFFFFF')
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # Title & Banner
    story.append(Paragraph("∀VITR AI (अवितृ • The Protector) — Technical Defense Guide", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>The Master Technical Q&A Manual:</b> In-Depth Architectural Questions, Real-World Examples & Exact Math", sub_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#FF6F32'), spaceAfter=8))

    # =========================================================================
    # SECTION 1: AI SCORING & THREAT MATHEMATICS
    # =========================================================================
    story.append(Paragraph("1. AI Scoring Engine & Threat Mathematics", h1_style))
    
    q1 = (
        "Q1: How is the Scam Percentage / Risk Score calculated in our model?",
        "Our engine uses a <b>Dual-Engine Architecture</b> combining calibrated Statistical Machine Learning with a 13-Rule Deterministic Security Automaton:<br/><br/>"
        "1. <b>Engine A (Classical ML Probability):</b> Text is transformed via TF-IDF vectorization and passed to a Calibrated Logistic Regression model trained on 10,392 multi-modal samples. It outputs continuous probability <i>P(scam) &isin; [0.0, 1.0]</i>.<br/>"
        "2. <b>Engine B (Deterministic Rule Heuristics):</b> 13 pre-compiled regex rules inspect fatal patterns (OTP demands, peer UPI VPAs, fake CBI digital arrest, authority spoofing, untrusted .apk links, countdown timers).<br/>"
        "3. <b>Dual-Verification Fusion:</b><br/>"
        "&nbsp;&nbsp;&bull; <b>Fatal Threat Floor:</b> If fatal rules trigger (OTP solicitation, UPI collect fraud), risk is clamped to a minimum <b>96.0% (CRITICAL)</b>.<br/>"
        "&nbsp;&nbsp;&bull; <b>Authority Extortion:</b> If CBI/Police Digital Arrest or Electricity Cutoff matches, risk is clamped to <b>90.0% – 95.0%</b>.<br/>"
        "&nbsp;&nbsp;&bull; <b>General Heuristics:</b> If 1 non-fatal heuristic matches, risk is clamped to <b>75.0% (HIGH)</b>.<br/>"
        "&nbsp;&nbsp;&bull; <b>Zero Heuristic Dampening:</b> If zero rules trigger and the text is authentic (e.g. Swiggy receipt, bank debit alert), risk is suppressed to <b>&lt; 3.5% (SAFE)</b>, eliminating false alarms."
    )
    story.append(Paragraph(f"<b>{q1[0]}</b>", q_style))
    story.append(Spacer(1, 1))
    story.append(Paragraph(q1[1], ans_style))
    story.append(Spacer(1, 6))

    q2 = (
        "Q2: What is the 70% scam tier about? Can you give real-world example lines?",
        "The <b>HIGH Threat tier (70.0% – 85.0%)</b> represents deceptive communications that carry elevated suspicious indicators but stop short of immediate criminal blackout threats or OTP demands:<br/><br/>"
        "&bull; <b>Example 1 (73.4% - Lucky Prize Processing Fee):</b><br/>"
        "&nbsp;&nbsp;<i>'Dear user, your phone number has won a cash reward in our lucky promotion. Reply immediately to receive the processing voucher.'</i><br/>"
        "&nbsp;&nbsp;<u>Why 73.4%:</u> Triggers high statistical scam probability (97.9%) without fatal APK or OTP demands.<br/><br/>"
        "&bull; <b>Example 2 (75.0% - Insecure Package Tracking Link):</b><br/>"
        "&nbsp;&nbsp;<i>'Order shipment notice: Your parcel requires address re-confirmation. Update your shipping address at http://track-package-support.site'</i><br/>"
        "&nbsp;&nbsp;<u>Why 75.0%:</u> Hits Rule 13 (Suspicious Free/Low-Trust Domain Extension) and Rule 14 (Insecure Plaintext HTTP link).<br/><br/>"
        "&bull; <b>Example 3 (82.8% - Delivery Exception Notice):</b><br/>"
        "&nbsp;&nbsp;<i>'Notification: Your package delivery address is incomplete. Please confirm your postal code at http://delivery-support-desk.top to avoid delay.'</i><br/>"
        "&nbsp;&nbsp;<u>Why 82.8%:</u> Coercive urgency combined with low-trust .top domain and credential redirection."
    )
    story.append(Paragraph(f"<b>{q2[0]}</b>", q_style))
    story.append(Spacer(1, 1))
    story.append(Paragraph(q2[1], ans_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 2: PRIVACY & DATA PROTECTION
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Zero-Knowledge Privacy & DPDP Act 2023 Compliance", h1_style))

    q3 = (
        "Q3: How does PII Masking work when someone inputs data?",
        "PII (Personally Identifiable Information) masking is handled by <b>SecurityGuardian.sanitize_pii</b> in volatile RAM before anything is logged or committed to the database. It functions like an automated digital redaction marker:<br/><br/>"
        "&bull; <b>Indian Mobile Numbers (10 digits):</b> <code>9876543210</code> &rarr; <code>987****210</code> (retains first 3 and last 3 for police/victim matching, masks middle 4).<br/>"
        "&bull; <b>Credit/Debit Cards (16 digits):</b> <code>4532-1234-5678-9012</code> &rarr; <code>XXXX-XXXX-XXXX-9012</code> (PCI-DSS compliant).<br/>"
        "&bull; <b>Aadhaar Numbers (12 digits):</b> <code>5432 1098 7654</code> &rarr; <code>XXXX-XXXX-7654</code> (complies with UIDAI masking norms).<br/>"
        "&bull; <b>PAN Cards (10 chars):</b> <code>ABCDE1234F</code> &rarr; <code>ABCXX****F</code>.<br/><br/>"
        "<b>Zero-Knowledge Screenshot Guarantee:</b> When users upload screenshots, <b>Tesseract.js OCR runs 100% inside their browser via WebAssembly (WASM)</b>. The raw photo is <b>never uploaded to our server (0 bytes transmitted)</b>. Only client-extracted text is sent, ensuring strict compliance with India's <b>Digital Personal Data Protection Act (DPDP Act 2023)</b>."
    )
    story.append(Paragraph(f"<b>{q3[0]}</b>", q_style))
    story.append(Spacer(1, 1))
    story.append(Paragraph(q3[1], ans_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 3: HIGH-PERFORMANCE INFRASTRUCTURE
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("3. High-Performance Infrastructure (Cache & Rate Limiting)", h1_style))

    q4 = (
        "Q4: How does our LRU Threat Cache work?",
        "Managed by <b>LRUThreatCache</b> in <code>ai/security.py</code> with a capacity of 10,000 entries:<br/><br/>"
        "1. <b>The Viral Scam Problem:</b> When scammers blast 50,000 citizens with the identical electricity cutoff SMS, evaluating ML repeatedly wastes server CPU.<br/>"
        "2. <b>Normalization & SHA-256 Fingerprint:</b> Incoming text is lowercased and whitespace-stripped, then converted into a 256-bit SHA-256 digital fingerprint (<code>key = sha256(text)</code>).<br/>"
        "3. <b>Sub-Millisecond Cache Hit:</b> If the hash exists in RAM, the saved verdict is returned in <b>0.08 milliseconds (&gt; 100x speedup with 0% CPU compute)</b>.<br/>"
        "4. <b>LRU Eviction:</b> If cache exceeds 10,000 items, the oldest unrequested scam is automatically discarded (<code>popitem(last=False)</code>), keeping trending scams resident in RAM."
    )
    story.append(Paragraph(f"<b>{q4[0]}</b>", q_style))
    story.append(Spacer(1, 1))
    story.append(Paragraph(q4[1], ans_style))
    story.append(Spacer(1, 6))

    q5 = (
        "Q5: What is the role of Rate Limiting in our project?",
        "Rate limiting is enforced by the <b>AntiSpamBuffer</b> as the very first guard in <code>ai/detector.py</code>:<br/><br/>"
        "&bull; <b>Layer 1 (1.5s Cooldown Buffer):</b> Enforces a 1.5-second pause between scans from the same client. This completely absorbs double-clicks and rapid button hammering.<br/>"
        "&bull; <b>Layer 2 (15 Scans / Minute Sliding Window):</b> Tracks timestamps over a rolling 60-second window. Any client exceeding 15 scans is paused with a clear countdown timer.<br/>"
        "&bull; <b>Security & Cost Value:</b> Stops botnet DoS attacks, protects computationally heavy Whisper audio transcription and OCR engines, and prevents cybercriminals from brute-force testing scam variations to reverse-engineer our detection rules."
    )
    story.append(Paragraph(f"<b>{q5[0]}</b>", q_style))
    story.append(Spacer(1, 1))
    story.append(Paragraph(q5[1], ans_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 4: FORENSICS, DATABASE & PUBLIC DEFENSE
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("4. Forensics, Database & Cyber Police Integration", h1_style))

    q6 = (
        "Q6: What is the use of storing the Case ID in the database?",
        "When an incident is evaluated, our engine signs the risk score and threat level with a <b>256-bit HMAC-SHA256 signature</b> and generates an official Forensic Case ID (e.g. <code>#D3E256C81A092F</code>):<br/><br/>"
        "1. <b>Cryptographic Chain of Custody:</b> Proves mathematically that the threat score was generated by our engine and was not altered by a man-in-the-middle network attacker.<br/>"
        "2. <b>Instant 1-Click Quick Lookup:</b> Users or investigating officers can paste the Case ID directly into the scanner search box to pull up the complete historical forensic record.<br/>"
        "3. <b>Cross-Referencing for Law Enforcement:</b> Police officers on <b>Helpline 1930 / Chakshu</b> can reference the Case ID to correlate repeated complaints against the same criminal UPI ID or bank account."
    )
    story.append(Paragraph(f"<b>{q6[0]}</b>", q_style))
    story.append(Spacer(1, 1))
    story.append(Paragraph(q6[1], ans_style))
    story.append(Spacer(1, 6))

    q7 = (
        "Q7: How can other people visiting the website see warnings on their screen?",
        "Via our <b>Community Threat Intelligence Feed</b> (powered by Supabase PostgreSQL):<br/><br/>"
        "When a user scans or reports a new scam campaign, the backend stores the sanitized preview and extracted indicators of compromise (IOCs: fraud phone numbers, spoofed UPI handles, malicious domains) in the database. When other visitors browse the platform, the frontend polls <code>GET /api/v1/feed</code> to display trending cybercrime alerts in real time. Because all text is pre-sanitized by our PII engine, no victim's personal data is ever exposed to the public."
    )
    story.append(Paragraph(f"<b>{q7[0]}</b>", q_style))
    story.append(Spacer(1, 1))
    story.append(Paragraph(q7[1], ans_style))
    story.append(Spacer(1, 6))

    q8 = (
        "Q8: What happens when clicking Helpline 1930 and how does the Cyber Police draft work?",
        "In India, victims in shock often struggle to explain technical cyber-fraud details to police operators on <b>Helpline 1930</b> or the <b>cybercrime.gov.in</b> portal.<br/><br/>"
        "Clicking the <b>1-Click Police Complaint Draft</b> button instantly formats an official legal incident dossier containing:<br/>"
        "&bull; <b>Incident Timestamp:</b> Exact UTC/IST timestamp.<br/>"
        "&bull; <b>Official Forensic Case ID:</b> <code>#D3E256...</code> for database traceability.<br/>"
        "&bull; <b>Automated Threat Assessment:</b> Threat level and probability score.<br/>"
        "&bull; <b>Detected Threat Categories:</b> Forensic breakdown of detected tactics (e.g. APK Malware, Blackout Extortion).<br/>"
        "&bull; <b>Action Requested:</b> Standard legal request requesting immediate freezing of perpetrator UPI accounts and phone line blocking under Sanchar Saathi (Chakshu)."
    )
    story.append(Paragraph(f"<b>{q8[0]}</b>", q_style))
    story.append(Spacer(1, 1))
    story.append(Paragraph(q8[1], ans_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 5: CALIBRATED TEST SUITE REFERENCE TABLE
    # =========================================================================
    story.append(Paragraph("5. Calibrated Test Suite Quick-Lookup Table", h1_style))
    story.append(Paragraph("Pre-calibrated test cases across all 4 sample test folders:", ans_style))
    story.append(Spacer(1, 3))

    table_data = [
        [
            Paragraph("<b>File / Test Scenario</b>", table_header),
            Paragraph("<b>Tier</b>", table_header),
            Paragraph("<b>Score</b>", table_header),
            Paragraph("<b>Key Security Trigger / Reason</b>", table_header)
        ],
        [
            Paragraph("01_safe_02pct_swiggy_receipt", table_cell),
            Paragraph("SAFE", table_cell),
            Paragraph("1.7%", table_cell),
            Paragraph("Itemized Swiggy food delivery receipt with GPay UPI.", table_cell)
        ],
        [
            Paragraph("02_safe_02pct_bank_debit_alert", table_cell),
            Paragraph("SAFE", table_cell),
            Paragraph("2.1%", table_cell),
            Paragraph("Legitimate ATM debit alert with 18002664332 helpline.", table_cell)
        ],
        [
            Paragraph("04_low_49pct_account_profile_verification", table_cell),
            Paragraph("LOW", table_cell),
            Paragraph("49.2%", table_cell),
            Paragraph("Account review notice without links or coercive demands.", table_cell)
        ],
        [
            Paragraph("05_medium_51pct_digital_wallet_compliance", table_cell),
            Paragraph("LOW/MED", table_cell),
            Paragraph("51.3%", table_cell),
            Paragraph("Digital wallet transfer suspension notice.", table_cell)
        ],
        [
            Paragraph("06_high_73pct_lucky_reward_processing_voucher", table_cell),
            Paragraph("HIGH", table_cell),
            Paragraph("73.4%", table_cell),
            Paragraph("Unsolicited cash reward promotion voucher lure.", table_cell)
        ],
        [
            Paragraph("07_high_75pct_untrusted_domain_package_tracker", table_cell),
            Paragraph("HIGH", table_cell),
            Paragraph("75.0%", table_cell),
            Paragraph("Parcel address update link on .site domain with HTTP.", table_cell)
        ],
        [
            Paragraph("08_high_83pct_delivery_exception_portal", table_cell),
            Paragraph("HIGH", table_cell),
            Paragraph("82.8%", table_cell),
            Paragraph("Insecure .top domain postal code re-confirmation trap.", table_cell)
        ],
        [
            Paragraph("09_critical_90pct_predatory_loan_trap", table_cell),
            Paragraph("CRITICAL", table_cell),
            Paragraph("90.0%", table_cell),
            Paragraph("Instant Rs 50,000 loan without CIBIL check; predatory trap.", table_cell)
        ],
        [
            Paragraph("10_critical_96pct_bijli_blackout_apk_extortion", table_cell),
            Paragraph("CRITICAL", table_cell),
            Paragraph("96.1%", table_cell),
            Paragraph("Power supply disconnection tonight at 9:30 PM with APK.", table_cell)
        ],
        [
            Paragraph("11_critical_98pct_cbi_digital_arrest_warrant", table_cell),
            Paragraph("CRITICAL", table_cell),
            Paragraph("90.0%", table_cell),
            Paragraph("Fake CBI Digital Arrest, 140g narcotics seizure threat.", table_cell)
        ]
    ]

    t_samples = Table(table_data, colWidths=[2.2*inch, 0.8*inch, 0.7*inch, 3.5*inch])
    t_samples.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')])
    ]))
    story.append(t_samples)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated primary PDF: {primary_path}")

    # Copy to all destination paths
    import shutil
    for path in output_paths[1:]:
        shutil.copyfile(primary_path, path)
        print(f"Mirrored PDF to: {path}")

if __name__ == "__main__":
    targets = [
        os.path.join("questions", "Questions_That_Can_Be_Asked.pdf"),
        os.path.join(r"C:\Users\HP\OneDrive\Desktop", "Questions_That_Can_Be_Asked.pdf"),
        os.path.join(r"C:\Users\HP\OneDrive\Desktop\test data", "Questions_That_Can_Be_Asked.pdf"),
        os.path.join(r"C:\Users\HP\OneDrive\Desktop", "ScamShield_AI_Defense_Guide.pdf")
    ]
    build_pdf(targets)
