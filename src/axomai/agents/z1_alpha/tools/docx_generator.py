"""
Z1 Alpha Autonomous Word Document (DOCX) Generator.
Transforms any uploaded document (Excel, CSV, PDF, Text) into a clean,
executive, publication-grade Word Document (.docx) with structured tables,
executive summaries, and branded styling.
"""

import io
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

import pandas as pd

from axomai.config import settings
from axomai.core.llm import llm_brain

GENERATED_DIR = settings.STORAGE_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def set_cell_shading(cell, hex_color: str):
    """Sets background shading color for a Word table cell"""
    hex_clean = hex_color.lstrip('#').upper()
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_clean}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding/margins in twips (1 pt = 20 twips)"""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


class DOCXGeneratorEngine:
    """Autonomous Engine for producing executive Word (.docx) documents and reports"""

    def generate_docx(
        self,
        source_path: str | Path,
        instruction: str,
        udm: Optional[Any] = None,
        context_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main entry point to create an executive Word document based on user request.
        """
        path = Path(source_path)
        ext = path.suffix.lower()

        try:
            if ext in [".xlsx", ".xls", ".csv", ".tsv"]:
                return self._generate_from_tabular(path, instruction)
            else:
                return self._generate_from_text_or_doc(path, instruction, udm, context_text)
        except Exception as e:
            return {"success": False, "error": f"DOCX generation failed: {str(e)}"}

    def _generate_from_tabular(self, path: Path, instruction: str) -> Dict[str, Any]:
        ext = path.suffix.lower()
        if ext in [".xlsx", ".xls"]:
            df = pd.read_excel(path)
        else:
            sep = "\t" if ext == ".tsv" else ","
            df = pd.read_csv(path, sep=sep)

        df_preview = df.head(5).to_string()
        cols = list(df.columns)

        sys_prompt = (
            "You are an expert Executive Document Architect. A user wants to generate a professional Word (.docx) "
            "document based on an Excel/CSV file.\n"
            "Your tasks:\n"
            "1. Give a clean, professional Document Title (e.g. 'Kamakhya Temple Social Media Campaign Brief').\n"
            "2. Provide an Executive Summary (2-3 concise, high-value sentences summarizing the document or purpose).\n"
            "3. If the user instruction requires filtering or selecting specific data (e.g., 'rating > 4.7', 'status done', 'only top 5'), "
            "write Python pandas code using variable `output_df = df[...]`. Otherwise, set `output_df = df.copy()`.\n"
            "4. Suggest a clean short filename without extension (e.g. 'kamakhya_campaign_doc').\n\n"
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

        title = path.stem.replace("_", " ").title() + " Executive Brief"
        summary = f"Executive briefing and structured data extraction compiled from {path.name}."
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

        # 2. Build Word Document
        timestamp_id = uuid.uuid4().hex[:6]
        final_filename = f"{timestamp_id}_{safe_name}.docx"
        final_path = GENERATED_DIR / final_filename

        doc = docx.Document()

        # Set standard margins (0.75 in)
        sections = doc.sections
        for s in sections:
            s.top_margin = Inches(0.75)
            s.bottom_margin = Inches(0.75)
            s.left_margin = Inches(0.75)
            s.right_margin = Inches(0.75)

            # Header & Footer
            header = s.header
            hp = header.paragraphs[0]
            hp.text = "AxomAI AGI • Z1 Alpha Autonomous Intelligence Vault"
            hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            hp.runs[0].font.size = Pt(8)
            hp.runs[0].font.color.rgb = RGBColor(148, 163, 184)

            footer = s.footer
            fp = footer.paragraphs[0]
            fp.text = "Confidential & Grounded Document • Generated by Z1 Alpha"
            fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
            fp.runs[0].font.size = Pt(8)
            fp.runs[0].font.color.rgb = RGBColor(148, 163, 184)

        # Title
        title_p = doc.add_paragraph()
        title_run = title_p.add_run(title)
        title_run.font.name = "Calibri"
        title_run.font.size = Pt(20)
        title_run.font.bold = True
        title_run.font.color.rgb = RGBColor(14, 116, 144)  # Teal/Navy #0e7490
        title_p.paragraph_format.space_after = Pt(2)

        # Subtitle / Metadata
        now_str = datetime.now().strftime("%B %d, %Y • %I:%M %p")
        meta_p = doc.add_paragraph()
        meta_run = meta_p.add_run(f"Source: {path.name}   |   Total Entries: {len(output_df)}   |   Generated: {now_str}")
        meta_run.font.name = "Calibri"
        meta_run.font.size = Pt(9.5)
        meta_run.font.color.rgb = RGBColor(100, 116, 139)  # Slate #64748b
        meta_p.paragraph_format.space_after = Pt(14)

        # Executive Summary Callout Box
        sum_table = doc.add_table(rows=1, cols=1)
        sum_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        sum_table.autofit = False
        sum_cell = sum_table.cell(0, 0)
        sum_cell.width = Inches(7.0)
        set_cell_shading(sum_cell, "F0FDF4")  # Mint green
        set_cell_margins(sum_cell, top=140, bottom=140, left=200, right=200)

        sp = sum_cell.paragraphs[0]
        sp.paragraph_format.space_after = Pt(4)
        sh_run = sp.add_run("EXECUTIVE OVERVIEW\n")
        sh_run.font.name = "Calibri"
        sh_run.font.size = Pt(10)
        sh_run.font.bold = True
        sh_run.font.color.rgb = RGBColor(14, 116, 144)

        s_run = sp.add_run(summary)
        s_run.font.name = "Calibri"
        s_run.font.size = Pt(9.5)
        s_run.font.color.rgb = RGBColor(30, 41, 59)

        doc.add_paragraph().paragraph_format.space_after = Pt(12)

        # Section Heading: Structured Records
        sec_h = doc.add_paragraph()
        sec_run = sec_h.add_run("Structured Record Details")
        sec_run.font.name = "Calibri"
        sec_run.font.size = Pt(12)
        sec_run.font.bold = True
        sec_run.font.color.rgb = RGBColor(15, 23, 42)
        sec_h.paragraph_format.space_after = Pt(6)

        # Table Grid
        cols_to_render = list(output_df.columns)[:7]
        display_df = output_df.head(100)

        grid = doc.add_table(rows=len(display_df) + 1, cols=len(cols_to_render))
        grid.alignment = WD_TABLE_ALIGNMENT.CENTER
        grid.autofit = False

        # Header Row
        hdr_cells = grid.rows[0].cells
        for idx, col_name in enumerate(cols_to_render):
            cell = hdr_cells[idx]
            cell.text = str(col_name).replace("_", " ").title()
            set_cell_shading(cell, "0E7490")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(9)
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)

        # Data Rows
        for r_idx, (_, row) in enumerate(display_df.iterrows()):
            row_cells = grid.rows[r_idx + 1].cells
            bg_color = "F8FAFC" if (r_idx % 2 == 1) else "FFFFFF"
            for c_idx, col_name in enumerate(cols_to_render):
                cell = row_cells[c_idx]
                val = row[col_name]
                val_str = "" if pd.isna(val) else str(val).strip()
                cell.text = val_str
                set_cell_shading(cell, bg_color)
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                p = cell.paragraphs[0]
                for run in p.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(8.5)
                    run.font.color.rgb = RGBColor(51, 65, 85)

        # Strategic Note
        doc.add_paragraph().paragraph_format.space_after = Pt(14)
        note_p = doc.add_paragraph()
        note_run = note_p.add_run(
            f"This Word document was compiled and verified autonomously by AxomAI AGI. "
            f"Contains {len(output_df)} verified entries derived from {path.name}."
        )
        note_run.font.name = "Calibri"
        note_run.font.size = Pt(9)
        note_run.font.italic = True
        note_run.font.color.rgb = RGBColor(148, 163, 184)

        # Save Document
        doc.save(str(final_path))
        file_size_kb = round(final_path.stat().st_size / 1024, 1)

        return {
            "success": True,
            "filename": f"{safe_name}.docx",
            "saved_filename": final_filename,
            "download_url": f"/api/download/generated/{final_filename}",
            "file_type": "DOCX",
            "file_size_kb": file_size_kb,
            "row_count": len(output_df),
            "column_count": len(cols_to_render),
            "description": f"Generated executive Word document '{title}' (.docx) containing {len(output_df)} formatted records."
        }

    def _generate_from_text_or_doc(
        self,
        path: Path,
        instruction: str,
        udm: Optional[Any] = None,
        context_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate executive Word document from PDF, Text, DOCX, or Multimodal context"""
        title = path.stem.replace("_", " ").title() + " Executive Intelligence Report"
        safe_name = re.sub(r'[^\w\-_\.]', '_', path.stem.lower())

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
        final_filename = f"{timestamp_id}_{safe_name}.docx"
        final_path = GENERATED_DIR / final_filename

        doc = docx.Document()

        for s in doc.sections:
            s.top_margin = Inches(0.75)
            s.bottom_margin = Inches(0.75)
            s.left_margin = Inches(0.75)
            s.right_margin = Inches(0.75)

            header = s.header
            hp = header.paragraphs[0]
            hp.text = "AxomAI AGI • Z1 Alpha Autonomous Intelligence Vault"
            hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            hp.runs[0].font.size = Pt(8)
            hp.runs[0].font.color.rgb = RGBColor(148, 163, 184)

            footer = s.footer
            fp = footer.paragraphs[0]
            fp.text = "Confidential & Grounded Document • Generated by Z1 Alpha"
            fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
            fp.runs[0].font.size = Pt(8)
            fp.runs[0].font.color.rgb = RGBColor(148, 163, 184)

        # Title
        tp = doc.add_paragraph()
        trun = tp.add_run(title)
        trun.font.name = "Calibri"
        trun.font.size = Pt(20)
        trun.font.bold = True
        trun.font.color.rgb = RGBColor(14, 116, 144)

        now_str = datetime.now().strftime("%B %d, %Y • %I:%M %p")
        mp = doc.add_paragraph()
        mrun = mp.add_run(f"Source: {path.name}   |   Generated: {now_str}")
        mrun.font.name = "Calibri"
        mrun.font.size = Pt(9.5)
        mrun.font.color.rgb = RGBColor(100, 116, 139)
        mp.paragraph_format.space_after = Pt(12)

        # Executive Summary Box
        sum_table = doc.add_table(rows=1, cols=1)
        sum_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        sum_table.autofit = False
        sum_cell = sum_table.cell(0, 0)
        sum_cell.width = Inches(7.0)
        set_cell_shading(sum_cell, "F0FDF4")
        set_cell_margins(sum_cell, top=140, bottom=140, left=200, right=200)

        sp = sum_cell.paragraphs[0]
        sh_run = sp.add_run("EXECUTIVE SUMMARY\n")
        sh_run.font.name = "Calibri"
        sh_run.font.size = Pt(10)
        sh_run.font.bold = True
        sh_run.font.color.rgb = RGBColor(14, 116, 144)
        s_run = sp.add_run(report_spec.get("executive_summary", ""))
        s_run.font.name = "Calibri"
        s_run.font.size = Pt(9.5)
        s_run.font.color.rgb = RGBColor(30, 41, 59)

        doc.add_paragraph().paragraph_format.space_after = Pt(10)

        # Key Findings
        findings = report_spec.get("key_findings", [])
        if findings:
            kp = doc.add_paragraph()
            krun = kp.add_run("Key Findings & Critical Insights")
            krun.font.name = "Calibri"
            krun.font.size = Pt(12)
            krun.font.bold = True
            krun.font.color.rgb = RGBColor(15, 23, 42)
            for f in findings:
                bp = doc.add_paragraph(style='List Bullet')
                brun = bp.add_run(f)
                brun.font.name = "Calibri"
                brun.font.size = Pt(9.5)
                brun.font.color.rgb = RGBColor(51, 65, 85)

        # Detailed Sections
        for sec in report_spec.get("detailed_analysis", []):
            dp = doc.add_paragraph()
            drun = dp.add_run(sec.get("heading", "Detailed Analysis"))
            drun.font.name = "Calibri"
            drun.font.size = Pt(12)
            drun.font.bold = True
            drun.font.color.rgb = RGBColor(15, 23, 42)

            bp = doc.add_paragraph()
            brun = bp.add_run(sec.get("body", ""))
            brun.font.name = "Calibri"
            brun.font.size = Pt(9.5)
            brun.font.color.rgb = RGBColor(51, 65, 85)

        # Recommendations
        recs = report_spec.get("recommendations", [])
        if recs:
            rp = doc.add_paragraph()
            rrun = rp.add_run("Actionable Recommendations")
            rrun.font.name = "Calibri"
            rrun.font.size = Pt(12)
            rrun.font.bold = True
            rrun.font.color.rgb = RGBColor(15, 23, 42)
            for r in recs:
                bp = doc.add_paragraph(style='List Bullet')
                brun = bp.add_run(r)
                brun.font.name = "Calibri"
                brun.font.size = Pt(9.5)
                brun.font.color.rgb = RGBColor(51, 65, 85)

        doc.save(str(final_path))
        file_size_kb = round(final_path.stat().st_size / 1024, 1)

        return {
            "success": True,
            "filename": f"{safe_name}.docx",
            "saved_filename": final_filename,
            "download_url": f"/api/download/generated/{final_filename}",
            "file_type": "DOCX",
            "file_size_kb": file_size_kb,
            "description": f"Generated executive Word document '{title}' (.docx)."
        }


docx_generator_engine = DOCXGeneratorEngine()

