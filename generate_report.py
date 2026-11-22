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
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    meta_data = [
        ("Project Lead & Lead Architect", "Ayusman Mishra (@Ayus-ProjeXion)"),
        ("Team Structure", "4 Members (Database, Backend API, Frontend UI, AI Detection Engine)"),
        ("Database Infrastructure", "Supabase PostgreSQL 15+ with Row-Level Security (RLS)"),
        ("Git Repository", "https://github.com/Ayus-ProjeXion/ScamShield-Ai"),
        ("Active Git Branches", "main, database (Active Workstream), backend, frontend, ai-engine"),
        ("Last Report Synchronization", datetime.datetime.now().strftime("%B %d, %Y - %I:%M %p"))
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
            pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="4" w:color="4F46E5"/></w:pBdr>')
            h._p.get_or_add_pPr().append(pBdr)
        else:
            r.font.size = Pt(13)
            r.font.color.rgb = RGBColor(0x31, 0x2E, 0x81)
        return h

    # --- 1. Executive Summary ---
    add_section_header("1. Executive Summary & Problem Scope")
    p = doc.add_paragraph(
        "Digital deception and financial fraud in India and globally have surged exponentially, spanning spoofed banking URLs, "
        "malicious SMS (smishing), fraudulent WhatsApp impersonation, and deceitful UPI QR code traps. "
        "ScamShield AI is engineered as an enterprise-grade multi-modal fraud detection and threat intelligence system that intercepts, "
        "analyzes, explains, and neutralizes fraudulent digital interactions in real time."
    )
    p.paragraph_format.space_after = Pt(6)
    
    p2 = doc.add_paragraph(
        "Led by Ayusman Mishra (@Ayus-ProjeXion) with a 4-member hackathon engineering squad, the platform couples ultra-fast deterministic "
        "heuristic checking with multi-label AI intent classification, backed by a production-ready Supabase PostgreSQL data store "
        "and complete Spec-Driven Development (SDD) documentation suite."
    )
    p2.paragraph_format.space_after = Pt(12)

    # --- 2. Team Workstream & Git Branching Matrix ---
    add_section_header("2. Team Workstream & Git Branching Matrix (4 Members)")
    doc.add_paragraph(
        "To enable simultaneous high-velocity development without merge conflicts, the project enforces strict Spec-Driven Development (SDD) "
        "and dedicated feature branches:"
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
        ("Database Architect (Ayusman - Lead)", "database", "Supabase PostgreSQL schema, migration SQL, RLS policies, threat IOC indexing, mock seed fixtures", "database/schema.sql, database/seed.sql, SDD suite"),
        ("Backend Engineer", "backend", "FastAPI / Node API gateway, validation pipelines, external threat API proxies, deterministic rule engine", "REST API endpoints (/scan, /report, /feed), rate-limiting"),
        ("AI / ML Detection Engineer", "ai-engine", "Scam classifier pipelines, NLP feature extraction, zero-shot fraud categorization, heuristic engines", "Inference service, prompt contracts, confusion matrix evals"),
        ("Frontend / UI Engineer", "frontend", "Dark glassmorphism user dashboard, multi-vector scanner simulator, alert notifications, risk gauges", "Interactive web UI, threat visualizer, responsive cards")
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

    # --- 3. Supabase Schema Architecture ---
    add_section_header("3. Supabase PostgreSQL Schema Specification (database/schema.sql)")
    doc.add_paragraph(
        "The relational database schema is deployed on Supabase PostgreSQL 15+ with active Row-Level Security (RLS) "
        "and automated updated_at triggers across all major entities:"
    )

    schema_table = doc.add_table(rows=7, cols=3)
    schema_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    schema_table.autofit = False

    s_headers = ["Table Name", "Primary Columns & Types", "Security & Access Control (RLS)"]
    s_widths = [Inches(1.8), Inches(3.2), Inches(1.8)]

    hdr_row = schema_table.rows[0]
    for j, h_text in enumerate(s_headers):
        cell = hdr_row.cells[j]
        cell.width = s_widths[j]
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    tables_info = [
        ("profiles", "id (UUID PK, FK auth.users), full_name (TEXT), email (TEXT UNIQUE), role (user_role), reputation_score (INT)", "Public viewable; users can update own profile."),
        ("threat_iocs", "id (UUID PK), ioc_type (ioc_type ENUM), ioc_value (TEXT UNIQUE), severity (threat_severity), category, is_blacklisted (BOOL)", "Publicly readable by client scanner; editable by admins."),
        ("threat_scans", "id (UUID PK), user_id (UUID FK), channel (scan_channel), raw_payload (TEXT), extracted_domain, extracted_phone, extracted_vpa", "Public insert allowed for scan tool; users view own scans."),
        ("scam_classifications", "id (UUID PK), scan_id (UUID FK), overall_severity, overall_risk_score (0-100), primary_category, deterministic_match, ai_confidence, explanation", "Read access linked to scan visibility; service-role inserts."),
        ("community_reports", "id (UUID PK), reporter_id (UUID FK), ioc_value, ioc_type, category, title, description, upvote_count, status", "Publicly readable threat feed; authenticated users can submit."),
        ("audit_logs", "id (UUID PK), actor_id (UUID FK), action (TEXT), entity_type, entity_id, details (JSONB), ip_address, created_at", "Strictly restricted to Security Analysts & Admins.")
    ]

    for i, t_data in enumerate(tables_info):
        row = schema_table.rows[i + 1]
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(t_data):
            cell = row.cells[j]
            cell.width = s_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if j == 0:
                r.bold = True
                r.font.name = 'Consolas'
                r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- 4. Synchronized SDD Documentation Suite ---
    add_section_header("4. Spec-Driven Development (SDD) Blueprint Suite")
    doc.add_paragraph("ScamShield AI maintains 6 fully synchronized markdown blueprints in the project root:")

    sdd_items = [
        ("PRD.md: ", "Complete Product Requirements Document detailing user personas, functional and non-functional specifications, and multi-channel detection requirements."),
        ("architecture.md: ", "End-to-end system topology, data flow lifecycle diagram, Supabase client/service proxy security model, and microservice interfaces."),
        ("rules.md: ", "Engineering operational guardrails: Sacred Trunk (`main`), zero client-side service keys, deterministic threat scoring, and dark glassmorphism design contracts."),
        ("phases.md: ", "Five-phase execution roadmap mapping milestones to team branches (`database`, `backend`, `ai-engine`, `frontend`, `main`)."),
        ("design.md: ", "UI/UX design system: Cyberpunk Mission Control theme tokens (`#0a0d14`, `#6366f1`, `#10b981`), typography hierarchy, and interactive risk gauge specs."),
        ("memory.md: ", "Architectural Decision Records (ADRs) logging project inception, database-first strategy, and state transitions.")
    ]
    for prefix, desc in sdd_items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        rb = p.add_run(prefix)
        rb.bold = True
        rb.font.color.rgb = RGBColor(0x31, 0x2E, 0x81)
        p.add_run(desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- 5. Execution Audit Log ---
    add_section_header("5. Project Execution & Audit Log")
    audit_table = doc.add_table(rows=6, cols=3)
    audit_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    audit_table.autofit = False

    audit_headers = ["Timestamp", "Milestone / Action Completed", "Status"]
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
        ("Nov 22, 2026 - 15:09", "Cloned GitHub repo 'ScamShield-Ai' and cleanly saved 'smart-campus-ai' on origin/main", "COMPLETED"),
        ("Nov 22, 2026 - 15:10", "Created and published 4 git team branches to GitHub: 'database', 'backend', 'frontend', 'ai-engine'", "COMPLETED"),
        ("Nov 22, 2026 - 15:11", "Generated automated living Word report (ScamShield_AI_Project_Report.docx)", "COMPLETED"),
        ("Nov 22, 2026 - 15:14", "Switched to 'database' branch; authored full 6-file SDD suite (PRD, architecture, rules, phases, design, memory)", "COMPLETED"),
        ("Nov 22, 2026 - 15:15", "Authored database/schema.sql (Supabase PostgreSQL DDL, ENUMs, RLS, Indexes) and database/seed.sql", "COMPLETED")
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
