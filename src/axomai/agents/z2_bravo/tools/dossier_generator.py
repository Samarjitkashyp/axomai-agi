"""
Z2 Bravo Dossier Generator Engine.
Compiles deep web research, market benchmarks, competitor matrices,
and verified citations into an executive PDF or Word Dossier.
"""

import io
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import fitz
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

from axomai.config import settings

GENERATED_DIR = settings.STORAGE_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for dynamic 'Page X of Y' numbering and clean executive branding"""
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
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        w, h = self._pagesize

        # Top cyan accent header bar
        self.setFillColor(colors.HexColor("#0891b2"))
        self.rect(36, h - 18, w - 72, 3, fill=True, stroke=False)

        # Footer divider line
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(36, 32, w - 36, 32)

        # Footer branding & pagination
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(36, 20, "AxomAI AGI • Z2 Bravo Deep Web Intelligence Vault (Confidential & Grounded)")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(w - 36, 20, page_str)
        self.restoreState()


class DossierGeneratorEngine:
    """Generates publication-grade Research Dossiers in PDF and Word formats"""

    def generate_dossier_pdf(
        self,
        topic: str,
        summary: str,
        detailed_findings: str,
        sources: List[Dict[str, Any]],
        market_matrix: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Creates an executive PDF Research Dossier.
        """
        title = topic.strip().title()
        if not title.lower().endswith("dossier"):
            title += " — Intelligence Dossier"

        safe_name = re.sub(r'[^\w\-_\.]', '_', topic.lower()).strip('_')[:40]
        timestamp_id = uuid.uuid4().hex[:6]
        final_filename = f"{timestamp_id}_{safe_name}_dossier.pdf"
        final_path = GENERATED_DIR / final_filename

        doc = SimpleDocTemplate(
            str(final_path),
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=40,
            bottomMargin=45
        )

        avail_width = A4[0] - 72
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'DossierTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=17,
            leading=21,
            textColor=colors.HexColor('#0e7490'),
            spaceAfter=4
        )

        sub_style = ParagraphStyle(
            'DossierSub',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=12
        )

        h2_style = ParagraphStyle(
            'DossierH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#0f172a'),
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            'DossierBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor('#334155'),
            spaceAfter=8
        )

        cell_style = ParagraphStyle(
            'DossierCell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=7.5,
            leading=9.5,
            textColor=colors.HexColor('#334155')
        )

        header_cell_style = ParagraphStyle(
            'DossierHCell',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=10,
            textColor=colors.white
        )

        story = []

        # Header Title
        story.append(Paragraph(title, title_style))
        now_str = datetime.now().strftime("%B %d, %Y • %I:%M %p")
        meta_sub = f"Compiled by <b>Z2 Bravo (Autonomous Web Intelligence)</b> &nbsp;|&nbsp; Verified Sources: <b>{len(sources)}</b> &nbsp;|&nbsp; {now_str}"
        story.append(Paragraph(meta_sub, sub_style))

        # Executive Summary Box
        summary_content = [
            [Paragraph("<b>EXECUTIVE INTELLIGENCE BRIEFING</b>", ParagraphStyle('BriefH', parent=body_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#0e7490')))],
            [Paragraph(summary, body_style)]
        ]
        summary_table = Table(summary_content, colWidths=[avail_width])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdf4')),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0e7490')),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 10))

        # Market Matrix (If present)
        if market_matrix and "headers" in market_matrix and "rows" in market_matrix:
            story.append(Paragraph(market_matrix.get("title", "Market & Competitor Benchmark Matrix"), h2_style))
            m_headers = [Paragraph(str(h), header_cell_style) for h in market_matrix["headers"]]
            m_rows = [m_headers]
            for row in market_matrix["rows"]:
                m_rows.append([Paragraph(str(val), cell_style) for val in row])
            
            n_cols = len(market_matrix["headers"])
            col_w = avail_width / (n_cols or 1)
            matrix_tbl = Table(m_rows, colWidths=[col_w] * n_cols)
            matrix_tbl.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0e7490')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ]))
            story.append(matrix_tbl)
            story.append(Spacer(1, 10))

        # Deep Synthesis & Findings
        story.append(Paragraph("Synthesized Deep Web Findings", h2_style))
        for line in detailed_findings.split("\n"):
            line_str = line.strip()
            if not line_str:
                continue
            if line_str.startswith("#"):
                heading_clean = line_str.lstrip("#").strip()
                story.append(Paragraph(heading_clean, h2_style))
            elif line_str.startswith("-") or line_str.startswith("*"):
                bullet_clean = line_str.lstrip("-* ").strip()
                story.append(Paragraph(f"• &nbsp; {bullet_clean}", body_style))
            else:
                story.append(Paragraph(line_str, body_style))

        story.append(Spacer(1, 10))

        # Verified Web Citations Table
        if sources:
            story.append(Paragraph(f"Verified Evidence Sources ({len(sources)} Citations)", h2_style))
            src_headers = [Paragraph("Domain / Provider", header_cell_style), Paragraph("Article / Document Title", header_cell_style), Paragraph("Live Verified URL", header_cell_style)]
            src_rows = [src_headers]
            for s in sources[:8]:
                src_rows.append([
                    Paragraph(f"<b>{s.get('domain', 'Web Source')}</b>", cell_style),
                    Paragraph(s.get('title', 'N/A'), cell_style),
                    Paragraph(f"<font color='#0891b2'>{s.get('url', '')[:55]}...</font>", cell_style)
                ])
            src_table = Table(src_rows, colWidths=[avail_width * 0.25, avail_width * 0.45, avail_width * 0.30])
            src_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ]))
            story.append(src_table)

        doc.build(story, canvasmaker=NumberedCanvas)

        pdf_doc = fitz.open(final_path)
        page_count = len(pdf_doc)
        pdf_doc.close()

        file_size_kb = round(final_path.stat().st_size / 1024, 1)

        return {
            "success": True,
            "filename": f"{safe_name}_dossier.pdf",
            "saved_filename": final_filename,
            "download_url": f"/api/download/generated/{final_filename}",
            "file_type": "PDF",
            "file_size_kb": file_size_kb,
            "page_count": page_count,
            "description": f"Generated Executive Research Dossier '{title}' ({page_count} pages) cross-referencing {len(sources)} live web sources."
        }


dossier_generator_engine = DossierGeneratorEngine()

