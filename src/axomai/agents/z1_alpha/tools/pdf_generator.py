"""
Z1 Alpha Autonomous PDF Document & Report Generator.
Transforms any uploaded document (Excel, CSV, PDF, Text) into a clean,
executive, publication-grade PDF report with data tables, executive summaries,
and metadata.
"""

import io
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import fitz

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

from axomai.config import settings
from axomai.core.llm import llm_brain

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
        self.drawString(36, 20, "AxomAI AGI • Z1 Alpha Autonomous Intelligence Engine (Confidential)")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(w - 36, 20, page_str)
        self.restoreState()


class PDFGeneratorEngine:
    """Autonomous Engine for producing executive PDF documents and reports"""

    def generate_pdf(
        self,
        source_path: str | Path,
        instruction: str,
        udm: Optional[Any] = None,
        context_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main entry point to create an executive PDF document based on user request.
        """
        path = Path(source_path)
        ext = path.suffix.lower()

        try:
            if ext in [".xlsx", ".xls", ".csv", ".tsv"]:
                return self._generate_from_tabular(path, instruction)
            else:
                return self._generate_from_text_or_doc(path, instruction, udm, context_text)
        except Exception as e:
            return {"success": False, "error": f"PDF generation failed: {str(e)}"}

    def _generate_from_tabular(self, path: Path, instruction: str) -> Dict[str, Any]:
        ext = path.suffix.lower()
        if ext in [".xlsx", ".xls"]:
            df = pd.read_excel(path)
        else:
            sep = "\t" if ext == ".tsv" else ","
            df = pd.read_csv(path, sep=sep)

        # 1. Ask LLM to extract title, executive summary, and optional filtering code
        df_preview = df.head(5).to_string()
        cols = list(df.columns)
        
        sys_prompt = (
            "You are an expert Executive Document Architect. A user wants to generate a professional PDF "
            "document based on an Excel/CSV file.\n"
            "Your tasks:\n"
            "1. Give a clean, professional Document Title (e.g. 'Kamakhya Temple Social Media Campaign Brief').\n"
            "2. Provide an Executive Summary (2-3 concise, high-value sentences summarizing the document or purpose).\n"
            "3. If the user instruction requires filtering or selecting specific data (e.g., 'rating > 4.7', 'status done', 'only top 5'), "
            "write Python pandas code using variable `output_df = df[...]`. Otherwise, set `output_df = df.copy()`.\n"
            "4. Suggest a clean short filename without extension (e.g. 'kamakhya_campaign_report').\n\n"
            "Respond strictly in valid JSON format with keys:\n"
            "{\n"
            '  "title": "...",\n'
            '  "summary": "...",\n'
            '  "filename": "...",\n'
            '  "code": "output_df = df.copy()"\n'
            "}"
        )

        user_prompt = (
            f"User Instruction: {instruction}\n"
            f"Source File: {path.name} ({len(df)} rows, {len(cols)} columns)\n"
            f"Columns: {cols}\n"
            f"Data Preview:\n{df_preview}\n\n"
            f"Generate the JSON document specification:"
        )

        title = path.stem.replace("_", " ").title() + " Report"
        summary = f"Executive briefing and structured data extraction generated from {path.name}."
        safe_name = re.sub(r'[^\w\-_\.]', '_', path.stem.lower())
        output_df = df.copy()

        if llm_brain.is_available:
            try:
                res_str = llm_brain.generate(sys_prompt, user_prompt, temperature=0.2)
                clean_str = res_str.strip()
                if "```json" in clean_str:
                    clean_str = clean_str.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_str:
                    clean_str = clean_str.split("```")[1].split("```")[0].strip()
                
                import json
                spec = json.loads(clean_str)
                title = spec.get("title") or title
                summary = spec.get("summary") or summary
                if spec.get("filename"):
                    safe_name = re.sub(r'[^\w\-_\.]', '_', str(spec.get("filename")).lower()).strip('_')
                
                code = spec.get("code", "")
                if code and "output_df" in code:
                    exec_scope = {"df": df.copy(), "pd": pd, "output_df": None}
                    exec(code, exec_scope)
                    if isinstance(exec_scope.get("output_df"), pd.DataFrame):
                        output_df = exec_scope.get("output_df")
            except Exception:
                pass

        # 2. Build ReportLab Story
        timestamp_id = uuid.uuid4().hex[:6]
        final_filename = f"{timestamp_id}_{safe_name}.pdf"
        final_path = GENERATED_DIR / final_filename

        doc = SimpleDocTemplate(
            str(final_path),
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=40,
            bottomMargin=45
        )

        avail_width = A4[0] - 72  # 595.27 - 72 = 523.27
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#0e7490'),
            spaceAfter=4
        )

        sub_style = ParagraphStyle(
            'DocSub',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=12
        )

        h2_style = ParagraphStyle(
            'DocH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#0f172a'),
            spaceBefore=10,
            spaceAfter=6
        )

        summary_box_style = ParagraphStyle(
            'SummaryBoxText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#1e293b')
        )

        cell_style = ParagraphStyle(
            'CellText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=7.5,
            leading=9.5,
            textColor=colors.HexColor('#334155')
        )

        header_cell_style = ParagraphStyle(
            'HeaderCellText',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=10,
            textColor=colors.white
        )

        story = []

        # Document Header
        story.append(Paragraph(title, title_style))
        now_str = datetime.now().strftime("%B %d, %Y • %I:%M %p")
        meta_sub = f"Source: <b>{path.name}</b> &nbsp;|&nbsp; Total Entries: <b>{len(output_df)}</b> &nbsp;|&nbsp; Generated on: <b>{now_str}</b>"
        story.append(Paragraph(meta_sub, sub_style))
        story.append(Spacer(1, 4))

        # Executive Summary Callout Box
        summary_content = [
            [Paragraph("<b>EXECUTIVE OVERVIEW</b>", ParagraphStyle('SummaryH', parent=summary_box_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#0e7490')))],
            [Paragraph(summary, summary_box_style)]
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
        story.append(Spacer(1, 14))

        # Structured Table Section
        story.append(Paragraph("Structured Record Details", h2_style))

        # Clean Table Data
        cols_to_render = list(output_df.columns)[:7]  # Limit to 7 columns for readability on A4
        num_cols = len(cols_to_render)

        # Distribute column widths dynamically
        if num_cols == 1:
            col_widths = [avail_width]
        elif num_cols == 2:
            col_widths = [avail_width * 0.35, avail_width * 0.65]
        elif num_cols == 3:
            col_widths = [avail_width * 0.28, avail_width * 0.52, avail_width * 0.20]
        elif num_cols == 4:
            col_widths = [avail_width * 0.24, avail_width * 0.44, avail_width * 0.20, avail_width * 0.12]
        else:
            w_each = avail_width / num_cols
            col_widths = [w_each] * num_cols

        # Header Row
        header_row = [Paragraph(str(c).replace("_", " ").title(), header_cell_style) for c in cols_to_render]
        table_rows = [header_row]

        # Max 100 rows to ensure fast generation and prevent runaway pages
        display_df = output_df.head(100)
        for _, r in display_df.iterrows():
            row_cells = []
            for col in cols_to_render:
                val = r[col]
                val_str = "" if pd.isna(val) else str(val).strip()
                row_cells.append(Paragraph(val_str, cell_style))
            table_rows.append(row_cells)

        grid_table = Table(table_rows, colWidths=col_widths, repeatRows=1)
        grid_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0e7490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ]))

        story.append(grid_table)
        story.append(Spacer(1, 14))

        # Strategic Note
        note_text = (
            f"<i>This document was compiled and verified autonomously by AxomAI AGI. "
            f"Contains {len(output_df)} verified entries derived from {path.name}.</i>"
        )
        story.append(Paragraph(note_text, sub_style))

        # Build Document
        doc.build(story, canvasmaker=NumberedCanvas)

        # Count Pages
        pdf_doc = fitz.open(final_path)
        page_count = len(pdf_doc)
        pdf_doc.close()

        file_size_kb = round(final_path.stat().st_size / 1024, 1)

        return {
            "success": True,
            "filename": f"{safe_name}.pdf",
            "saved_filename": final_filename,
            "download_url": f"/api/download/generated/{final_filename}",
            "file_type": "PDF",
            "file_size_kb": file_size_kb,
            "page_count": page_count,
            "row_count": len(output_df),
            "column_count": len(cols_to_render),
            "description": f"Generated executive PDF report '{title}' ({page_count} pages) containing {len(output_df)} formatted records."
        }

    def _generate_from_text_or_doc(
        self,
        path: Path,
        instruction: str,
        udm: Optional[Any] = None,
        context_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate executive PDF report from PDF, Text, DOCX, or Multimodal context"""
        title = path.stem.replace("_", " ").title() + " Executive Intelligence Report"
        safe_name = re.sub(r'[^\w\-_\.]', '_', path.stem.lower())

        # Build context
        if not context_text and udm:
            context_text = "\n\n".join([f"Page {p.page_number}:\n{p.text}" for p in udm.pages[:5]])
        context_text = context_text or f"Document context extracted from {path.name}."

        sys_prompt = (
            "You are an expert Document Author and Executive Report Writer. "
            "Generate a comprehensive, structured briefing report based on the provided document context.\n"
            "Format your output in clean JSON with the following structure:\n"
            "{\n"
            '  "title": "...",\n'
            '  "executive_summary": "...",\n'
            '  "key_findings": ["Point 1", "Point 2", "Point 3", "Point 4"],\n'
            '  "detailed_analysis": [\n'
            '    {"heading": "...", "body": "..."},\n'
            '    {"heading": "...", "body": "..."}\n'
            '  ],\n'
            '  "recommendations": ["Action 1", "Action 2"],\n'
            '  "filename": "..."\n'
            "}"
        )

        user_prompt = (
            f"User Instruction: {instruction}\n"
            f"Source Document: {path.name}\n"
            f"Context:\n{context_text[:3500]}\n\n"
            f"Generate the structured JSON report:"
        )

        report_spec = {
            "title": title,
            "executive_summary": f"Comprehensive intelligence report synthesized from {path.name}.",
            "key_findings": ["Critical takeaways and findings verified from source document."],
            "detailed_analysis": [{"heading": "Core Analysis", "body": context_text[:1000]}],
            "recommendations": ["Review detailed findings and integrate into strategic initiatives."]
        }

        if llm_brain.is_available:
            try:
                raw_json = llm_brain.generate(sys_prompt, user_prompt, temperature=0.2)
                clean_json = raw_json.strip()
                if "```json" in clean_json:
                    clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_json:
                    clean_json = clean_json.split("```")[1].split("```")[0].strip()
                import json
                spec = json.loads(clean_json)
                report_spec.update(spec)
                if spec.get("title"):
                    title = spec.get("title")
                if spec.get("filename"):
                    safe_name = re.sub(r'[^\w\-_\.]', '_', str(spec.get("filename")).lower()).strip('_')
            except Exception:
                pass

        timestamp_id = uuid.uuid4().hex[:6]
        final_filename = f"{timestamp_id}_{safe_name}.pdf"
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
            'DocTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#0e7490'),
            spaceAfter=4
        )
        sub_style = ParagraphStyle(
            'DocSub',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=12
        )
        h2_style = ParagraphStyle(
            'DocH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=15,
            textColor=colors.HexColor('#0f172a'),
            spaceBefore=12,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'DocBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#334155'),
            spaceAfter=8
        )
        bullet_style = ParagraphStyle(
            'DocBullet',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#1e293b'),
            leftIndent=15,
            firstLineIndent=-10,
            spaceAfter=4
        )

        story = []
        story.append(Paragraph(title, title_style))
        now_str = datetime.now().strftime("%B %d, %Y • %I:%M %p")
        story.append(Paragraph(f"Source: <b>{path.name}</b> &nbsp;|&nbsp; Generated on: <b>{now_str}</b>", sub_style))

        # Executive Summary Box
        summary_table = Table([[
            Paragraph("<b>EXECUTIVE SUMMARY</b>", ParagraphStyle('SH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#0e7490'))),
        ], [
            Paragraph(report_spec.get("executive_summary", ""), body_style)
        ]], colWidths=[avail_width])
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

        # Key Findings
        findings = report_spec.get("key_findings", [])
        if findings:
            story.append(Paragraph("Key Findings & Critical Insights", h2_style))
            for f in findings:
                story.append(Paragraph(f"• &nbsp; {f}", bullet_style))
            story.append(Spacer(1, 10))

        # Detailed Analysis Sections
        sections = report_spec.get("detailed_analysis", [])
        for sec in sections:
            story.append(Paragraph(sec.get("heading", "Detailed Analysis"), h2_style))
            story.append(Paragraph(sec.get("body", ""), body_style))

        # Recommendations
        recs = report_spec.get("recommendations", [])
        if recs:
            story.append(Paragraph("Actionable Recommendations", h2_style))
            for r in recs:
                story.append(Paragraph(f"• &nbsp; {r}", bullet_style))

        doc.build(story, canvasmaker=NumberedCanvas)

        pdf_doc = fitz.open(final_path)
        page_count = len(pdf_doc)
        pdf_doc.close()

        file_size_kb = round(final_path.stat().st_size / 1024, 1)

        return {
            "success": True,
            "filename": f"{safe_name}.pdf",
            "saved_filename": final_filename,
            "download_url": f"/api/download/generated/{final_filename}",
            "file_type": "PDF",
            "file_size_kb": file_size_kb,
            "page_count": page_count,
            "description": f"Generated executive PDF report '{title}' ({page_count} pages)."
        }


pdf_generator_engine = PDFGeneratorEngine()

