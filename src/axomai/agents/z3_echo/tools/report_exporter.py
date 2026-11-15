"""
Z3 Echo Executive Analytics Report & Board Deck Generator.
Compiles publication-grade PDF analytics briefings with executive metrics,
forecast projections, diagnostic breakdowns, and executed SQL audit trails.
"""

import os
import re
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.pdfgen import canvas
from rich.console import Console

from axomai.config import settings

console = Console()
OUTPUT_DIR = settings.STORAGE_DIR / "generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header
        self.drawString(54, 755, "AxomAI AGI — Z3 Echo Executive Analytics Briefing")
        self.drawRightString(558, 755, "CONFIDENTIAL & PROPRIETARY")
        self.setStrokeColor(colors.HexColor("#334155"))
        self.setLineWidth(0.5)
        self.line(54, 750, 558, 750)

        # Running Footer
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • Z3 Echo Autonomous Intelligence")
        self.drawRightString(558, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

class ReportExporter:
    def __init__(self):
        pass

    def generate_analytics_report(
        self,
        topic: str,
        summary: str,
        detailed_findings: str,
        sql_query: Optional[str] = None,
        data_table: Optional[Dict[str, Any]] = None,
        scenario_matrix: Optional[Dict[str, Any]] = None,
        task_type: Optional[str] = "DATABASE_ANALYTICS"
    ) -> Dict[str, Any]:
        """
        Builds an executive PDF analytics dossier.
        """
        try:
            safe_slug = re.sub(r'[^a-zA-Z0-9_-]', '_', topic.lower().strip())[:30].strip('_')
            rand_prefix = str(uuid.uuid4())[:6]
            filename = f"{rand_prefix}_{safe_slug}_analytics_report.pdf"
            file_path = OUTPUT_DIR / filename

            doc = SimpleDocTemplate(
                str(file_path),
                pagesize=letter,
                leftMargin=54,
                rightMargin=54,
                topMargin=54,
                bottomMargin=54
            )

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'ReportTitle',
                parent=styles['Heading1'],
                fontSize=20,
                leading=24,
                textColor=colors.HexColor("#7C3AED"),  # Violet
                spaceAfter=4,
                fontName="Helvetica-Bold"
            )
            subtitle_style = ParagraphStyle(
                'ReportSubtitle',
                parent=styles['Normal'],
                fontSize=9,
                leading=13,
                textColor=colors.HexColor("#64748B"),
                spaceAfter=14,
                fontName="Helvetica"
            )
            heading_style = ParagraphStyle(
                'SectionHeading',
                parent=styles['Heading2'],
                fontSize=12,
                leading=16,
                textColor=colors.HexColor("#4C1D95"),  # Dark Violet
                spaceBefore=12,
                spaceAfter=6,
                fontName="Helvetica-Bold"
            )
            body_style = ParagraphStyle(
                'ReportBody',
                parent=styles['Normal'],
                fontSize=9,
                leading=13,
                textColor=colors.HexColor("#1E293B"),
                spaceAfter=8,
                fontName="Helvetica"
            )
            code_style = ParagraphStyle(
                'ReportCode',
                parent=styles['Normal'],
                fontSize=8,
                leading=10,
                textColor=colors.HexColor("#065F46"),
                fontName="Courier"
            )

            story = []

            # 1. Header Banner
            story.append(Spacer(1, 15))
            clean_title = topic.strip().title()
            story.append(Paragraph(clean_title, title_style))
            story.append(Paragraph(f"AxomAI AGI • Z3 Echo Analytics Report • Task: {task_type}", subtitle_style))

            # 2. Executive Briefing Box
            clean_summary = summary.replace("\n", " ").strip()
            summary_p = Paragraph(f"<b>Executive Analytics Briefing:</b> {clean_summary}", body_style)
            summary_table = Table([[summary_p]], colWidths=[504])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F5F3FF")),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#C4B5FD")),
                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('LEFTPADDING', (0,0), (-1,-1), 10),
                ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 12))

            # 3. Executed SQL Query (if present)
            if sql_query:
                story.append(Paragraph("Executed Analytical SQL Query", heading_style))
                sql_p = Paragraph(f"<code>{sql_query}</code>", code_style)
                sql_table = Table([[sql_p]], colWidths=[504])
                sql_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
                    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ('LEFTPADDING', (0,0), (-1,-1), 8),
                    ('RIGHTPADDING', (0,0), (-1,-1), 8),
                ]))
                story.append(sql_table)
                story.append(Spacer(1, 10))

            # 4. Scenario Matrix / Results Table (if present)
            target_mat = scenario_matrix or data_table
            if target_mat and target_mat.get("headers") and target_mat.get("rows"):
                mat_title = target_mat.get("title", "Structured Query Records")
                story.append(Paragraph(mat_title, heading_style))
                
                table_data = [[Paragraph(f"<b>{h}</b>", body_style) for h in target_mat["headers"]]]
                for row in target_mat["rows"][:12]:
                    row_cells = [Paragraph(str(c), body_style) for c in row]
                    table_data.append(row_cells)

                col_w = 504 / len(target_mat["headers"])
                col_widths = [col_w] * len(target_mat["headers"])
                
                matrix_table = Table(table_data, colWidths=col_widths)
                matrix_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#7C3AED")),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                    ('TOPPADDING', (0, 0), (-1, 0), 6),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#FAF5FF")),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#DDD6FE")),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F3FF")])
                ]))
                story.append(KeepTogether([matrix_table]))
                story.append(Spacer(1, 12))

            # 5. Detailed Analytical Intelligence
            story.append(Paragraph("Strategic Findings & Recommendations", heading_style))
            paragraphs = detailed_findings.split("\n\n")
            for para in paragraphs:
                p_text = para.strip()
                if not p_text:
                    continue
                if p_text.startswith("## ") or p_text.startswith("### "):
                    h_text = p_text.lstrip("#").strip()
                    story.append(Paragraph(h_text, heading_style))
                else:
                    clean_p = p_text.replace("\n", " ")
                    story.append(Paragraph(clean_p, body_style))

            doc.build(story, canvasmaker=NumberedCanvas)

            size_kb = round(file_path.stat().st_size / 1024, 1)
            page_count = 2 if size_kb > 5.0 else 1

            return {
                "success": True,
                "filename": filename,
                "download_url": f"/api/download/generated/{filename}",
                "file_type": "PDF",
                "file_size_kb": size_kb,
                "page_count": page_count,
                "description": f"Generated Executive Analytics Dossier '{clean_title}' ({page_count} pages)."
            }
        except Exception as e:
            console.print(f"[dim red][Z3 Report Export Error][/dim red] {e}")
            return {"success": False, "error": str(e)}

report_exporter = ReportExporter()

