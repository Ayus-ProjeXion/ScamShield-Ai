import os
import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_project_report(output_path="ScamShield_AI_Project_Report.docx"):
    doc = Document()

    # Configure Margins (0.8 inches)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Styles & Fonts
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x2D, 0x37, 0x48) # Dark slate

    # --- Title Banner ---
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("PROJECT SCAMSHIELD AI")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(26)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A) # Deep Navy

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(16)
    run_sub = sub_p.add_run("Real-Time Multi-Modal Scam Detection, Threat Intelligence & Prevention Platform")
    run_sub.font.name = 'Arial'
    run_sub.font.size = Pt(14)
    run_sub.font.color.rgb = RGBColor(0x4F, 0x46, 0xE5) # Indigo Accent

    # --- Metadata Table ---
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    meta_data = [
        ("Project Lead & Lead Architect", "Ayusman Mishra (@Ayus-ProjeXion)"),
        ("Team Structure", "4 Members (Database, Backend API, Frontend UI, AI Detection Engine)"),
        ("Git Repository", "https://github.com/Ayus-ProjeXion/ScamShield-Ai"),
        ("Active Git Branches", "main (Sacred Trunk), database, backend, frontend, ai-engine"),
        ("Report Generation Date", datetime.datetime.now().strftime("%B %d, %Y - %I:%M %p"))
    ]

    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.6)
        
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(v)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- Helper for Section Headings ---
    def add_section_header(title, level=1):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
        r = h.add_run(title)
        r.font.name = 'Arial'
        r.font.bold = True
        if level == 1:
            r.font.size = Pt(16)
            r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            # Add subtle bottom line under H1
            pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="4" w:color="4F46E5"/></w:pBdr>')
            h._p.get_or_add_pPr().append(pBdr)
        else:
            r.font.size = Pt(13)
            r.font.color.rgb = RGBColor(0x31, 0x2E, 0x81)
        return h

    # --- 1. Executive Summary ---
    add_section_header("1. Executive Summary & Mission")
    p = doc.add_paragraph(
        "Digital deception and financial fraud have expanded drastically, spanning deceptive phishing URLs, fraudulent SMS (smishing), "
        "malicious WhatsApp/Telegram impersonation, and fraudulent UPI/QR payment scams. "
        "ScamShield AI is engineered as a unified, real-time protection intelligence ecosystem that detects, explains, and neutralizes fraudulent content "
        "before harm occurs."
    )
    p.paragraph_format.space_after = Pt(6)
    
    p2 = doc.add_paragraph(
        "Built under the architectural direction of Ayusman Mishra (@Ayus-ProjeXion) and executed by a 4-member hackathon team, "
        "the system balances high-speed heuristic verification with multi-modal deep learning classification, backed by an enterprise-grade "
        "audit trail and PostgreSQL threat intelligence warehouse."
    )
    p2.paragraph_format.space_after = Pt(12)

    # --- 2. Team Workstream & Branching Strategy ---
    add_section_header("2. Team Workstream & Git Branching Matrix (4 Members)")
    doc.add_paragraph(
        "To maximize development velocity during the hackathon without merge conflicts, the project adheres to strict Spec-Driven Development (SDD) "
        "and isolated feature branching. Each team member owns an isolated layer of the platform:"
    )

    team_table = doc.add_table(rows=5, cols=4)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    team_table.autofit = False

    headers = ["Member Workstream", "Git Branch", "Core Responsibilities", "Key Deliverables"]
    col_widths = [Inches(1.5), Inches(1.2), Inches(2.2), Inches(1.9)]

    hdr_row = team_table.rows[0]
    for j, h_text in enumerate(headers):
        cell = hdr_row.cells[j]
        cell.width = col_widths[j]
        set_cell_background(cell, "4F46E5")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    team_data = [
        ("Database Architect (Ayusman - Lead)", "database", "PostgreSQL schema, migration scripts, Supabase setup, row-level security (RLS), threat indexing", "001_initial_schema.sql, ERD diagram, sample seed fixtures"),
        ("Backend Engineer", "backend", "FastAPI / Node API gateway, validation pipelines, external threat API proxies, deterministic rule engine", "REST API endpoints (/analyze, /report, /stats), rate-limiting"),
        ("AI / ML Detection Engineer", "ai-engine", "Scam classifier pipelines, NLP feature extraction, zero-shot fraud categorization, heuristic engines", "Inference service, prompt contracts, confusion matrix evals"),
        ("Frontend / UI Engineer", "frontend", "Dark glassmorphism user dashboard, chrome extension / simulator UI, alert notifications, risk gauges", "Interactive web UI, threat visualizer, responsive cards")
    ]

    for i, row_data in enumerate(team_data):
        row = team_table.rows[i + 1]
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = col_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if j == 1:
                r.bold = True
                r.font.name = 'Consolas'
                r.font.color.rgb = RGBColor(0x43, 0x38, 0xCA)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- 3. Architecture Strategy ---
    add_section_header("3. Architectural Strategy: Why Database First?")
    p = doc.add_paragraph()
    r = p.add_run("Architectural Decision (ADR-001): Prioritize Database Schema Before Backend Code")
    r.bold = True
    r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    
    reasons = [
        ("Contract-First Engineering: ", "The database schema serves as the single source of truth across all 4 team members. Backend endpoints, frontend interfaces, and AI payloads directly reflect the defined tables and field types."),
        ("Deterministic Threat Guardrails: ", "Scam types, confidence scores, threat severity levels (Critical, High, Medium, Low), and verification states must be strictly typed using SQL ENUMs to prevent runtime anomalies."),
        ("Parallelization Enablement: ", "Once the migration SQL and mock data seeds are committed on the 'database' branch, the Backend engineer can immediately scaffold ORM models, the AI engineer can write ingestion scripts, and the Frontend engineer can bind against fixed JSON structures without waiting for live APIs.")
    ]
    for bold_prefix, text in reasons:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        r_b = bp.add_run(bold_prefix)
        r_b.bold = True
        r_b.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        bp.add_run(text)

    # --- 4. Database Schema Specification ---
    add_section_header("4. Initial Database Schema Specification (PostgreSQL / Supabase)")
    doc.add_paragraph("The initial schema comprises four high-performance normalized tables designed for high-throughput scam scanning and reporting:")

    schema_tables = [
        ("1. users & profiles", "Manages user identities, API keys, notification tokens, and verification status."),
        ("2. threat_scans", "Stores incoming scan requests (SMS text, URL, email body, QR/UPI id), extracted metadata, sender signatures, and processing timestamps."),
        ("3. scam_classifications", "Contains AI inference outcomes, deterministic rule triggers, confidence score (0.00 - 1.00), threat classification category, and reasoning explanation."),
        ("4. community_reports & blacklists", "Crowdsourced scam reports, flagged UPI IDs, malicious phone numbers, and known phishing domain feeds with upvote/verification counts.")
    ]
    for title, desc in schema_tables:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        rb = p.add_run(f"{title}: ")
        rb.bold = True
        p.add_run(desc)

    # --- 5. Project Roadmap & Next Steps ---
    add_section_header("5. Phased Implementation Roadmap")
    phases = [
        ("Phase 1 - Database Layer (Current Active Step)", "Finalize 'schema.sql' with Supabase migration, create seed fixtures, and publish JSON interface contracts on 'database' branch."),
        ("Phase 2 - Backend Gateway & Heuristic Engine", "Scaffold FastAPI service, deterministic regex / pattern matching for known scam indicators, and integrate Supabase client on 'backend' branch."),
        ("Phase 3 - Multi-Modal AI Detection Engine", "Deploy LLM / zero-shot classification pipelines with structured JSON outputs and confidence calibration on 'ai-engine' branch."),
        ("Phase 4 - Frontend Mission Control Dashboard", "Build cyberpunk/dark-glassmorphism portal with real-time URL/SMS threat scanner, risk meter, and community report feed on 'frontend' branch."),
        ("Phase 5 - PR Review, Integration & Pitch Deck", "Run CodeRabbit review across branches, merge into 'main', and synthesize interactive demo and presentation.")
    ]
    for ph_title, ph_desc in phases:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        rb = p.add_run(f"{ph_title}: ")
        rb.bold = True
        p.add_run(ph_desc)

    # --- 6. Live Progress & Audit Log ---
    add_section_header("6. Execution Log & Audit Trail")
    audit_table = doc.add_table(rows=4, cols=3)
    audit_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    audit_table.autofit = False

    audit_headers = ["Timestamp", "Action / Milestone Completed", "Status"]
    audit_widths = [Inches(1.8), Inches(3.8), Inches(1.2)]
    hdr_row = audit_table.rows[0]
    for j, h_text in enumerate(audit_headers):
        cell = hdr_row.cells[j]
        cell.width = audit_widths[j]
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    audit_records = [
        ("Nov 22, 2026 - 15:09", "Cloned GitHub repo 'ScamShield-Ai' and transitioned from Smart Campus AI (saved clean on main)", "COMPLETED"),
        ("Nov 22, 2026 - 15:10", "Created and published 4 git team branches to GitHub: 'database', 'backend', 'frontend', 'ai-engine'", "COMPLETED"),
        ("Nov 22, 2026 - 15:11", "Generated live Word document report (ScamShield_AI_Project_Report.docx) for automated updates", "ACTIVE")
    ]

    for i, record in enumerate(audit_records):
        row = audit_table.rows[i + 1]
        for j, val in enumerate(record):
            cell = row.cells[j]
            cell.width = audit_widths[j]
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, 50, 50, 70, 70)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if j == 2:
                r.bold = True
                r.font.color.rgb = RGBColor(0x16, 0xA3, 0x4A) if "COMPLETED" in val else RGBColor(0x4F, 0x46, 0xE5)

    doc.save(output_path)
    print(f"Report successfully saved to {output_path}")

if __name__ == "__main__":
    create_project_report()
