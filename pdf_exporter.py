"""
PDF export for meeting minutes using ReportLab (free, local).
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from datetime import datetime


PEACH = colors.HexColor("#FFCBA4")
PEACH_DARK = colors.HexColor("#E8956D")
CREAM = colors.HexColor("#FFF8F0")
BROWN = colors.HexColor("#5C3D2E")
LIGHT_PEACH = colors.HexColor("#FFE5D0")


def generate_pdf(data: dict, output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=22,
        textColor=BROWN,
        spaceAfter=6,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER
    )
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=PEACH_DARK,
        spaceBefore=14,
        spaceAfter=4,
        fontName='Helvetica-Bold'
    )
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=BROWN,
        spaceAfter=4,
        leading=15
    )
    meta_style = ParagraphStyle(
        'Meta',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor("#A0785A"),
        alignment=TA_CENTER,
        spaceAfter=2
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=10,
        textColor=BROWN,
        leftIndent=16,
        spaceAfter=3,
        leading=14
    )

    story = []

    # Title
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("🌸 Meeting Minutes", title_style))
    story.append(Paragraph(data.get("meeting_title", "Meeting"), title_style))
    story.append(Spacer(1, 0.2*cm))

    # Meta info
    if data.get("meeting_date"):
        story.append(Paragraph(f"📅 {data['meeting_date']}", meta_style))
    if data.get("participants"):
        story.append(Paragraph(f"👥 {data['participants']}", meta_style))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", meta_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=2, color=PEACH, spaceAfter=10))

    # Tags row
    badge_data = []
    if data.get("meeting_type"):
        badge_data.append(f"Type: {data['meeting_type']}")
    if data.get("sentiment"):
        badge_data.append(f"Sentiment: {data['sentiment']}")
    if badge_data:
        story.append(Paragraph("  ·  ".join(badge_data), meta_style))
        story.append(Spacer(1, 0.3*cm))

    # Summary
    story.append(Paragraph("Executive Summary", h2_style))
    story.append(Paragraph(data.get("summary", "N/A"), body_style))

    # Key Topics
    topics = data.get("key_topics", [])
    if topics:
        story.append(Paragraph("Key Topics", h2_style))
        for t in topics:
            story.append(Paragraph(f"• {t}", bullet_style))

    # Decisions
    decisions = data.get("decisions", [])
    if decisions:
        story.append(Paragraph("Decisions Made", h2_style))
        for d in decisions:
            story.append(Paragraph(f"✅ <b>{d.get('decision','')}</b>", bullet_style))
            if d.get('context'):
                story.append(Paragraph(f"   ↳ {d['context']}", ParagraphStyle(
                    'Sub', parent=body_style, leftIndent=24, fontSize=9,
                    textColor=colors.HexColor("#A0785A"))))

    # Action Items table
    action_items = data.get("action_items", [])
    if action_items:
        story.append(Paragraph("Action Items", h2_style))
        table_data = [["Task", "Owner", "Deadline", "Priority"]]
        for item in action_items:
            priority = item.get("priority", "Medium")
            table_data.append([
                Paragraph(item.get("task", ""), body_style),
                item.get("owner", "Unassigned"),
                item.get("deadline", "TBD"),
                priority
            ])

        col_widths = [9*cm, 3.5*cm, 3*cm, 2*cm]
        t = Table(table_data, colWidths=col_widths, repeatRows=1)

        priority_colors = {"High": colors.HexColor("#FF8C69"), "Medium": PEACH, "Low": LIGHT_PEACH}

        ts = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PEACH_DARK),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [CREAM, colors.white]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E8C4A0")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ])

        # Color-code priority cells
        for i, item in enumerate(action_items, start=1):
            priority = item.get("priority", "Medium")
            bg = priority_colors.get(priority, PEACH)
            ts.add('BACKGROUND', (3, i), (3, i), bg)
            ts.add('TEXTCOLOR', (3, i), (3, i), BROWN)
            ts.add('FONTNAME', (3, i), (3, i), 'Helvetica-Bold')

        t.setStyle(ts)
        story.append(t)

    # Follow-up Questions
    follow_ups = data.get("follow_up_questions", [])
    if follow_ups:
        story.append(Paragraph("Follow-up Questions", h2_style))
        for q in follow_ups:
            story.append(Paragraph(f"❓ {q}", bullet_style))

    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=PEACH, spaceAfter=8))
    story.append(Paragraph("Generated by Meeting Summarizer 🌸", meta_style))

    doc.build(story)
    return output_path
