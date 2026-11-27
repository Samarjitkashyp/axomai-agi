"""
Z7 Visionary - Dynamic Multi-Slide PowerPoint (.pptx) Builder with Native Charts,
KPI Cards, Tables, Assam Sector Themes & Bilingual Assamese/English Support.
"""

import json
import uuid
from typing import Dict, Any, List, Optional
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

from axomai.config import settings
from axomai.core.llm import llm_brain
from axomai.agents.z7_visionary.tools.assam_themes_and_dpr import SECTOR_THEMES


class PPTXBuilder:
    """Builds boardroom-grade .pptx decks with dynamic LLM content, native charts, KPI cards & tables."""

    def __init__(self):
        self.output_dir = settings.STORAGE_DIR / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def synthesize_dynamic_slides(
        self,
        query: str,
        title: str,
        district: str,
        scheme: Optional[str],
        dpr_data: Dict[str, Any],
        target_slides: int = 8,
        bilingual_assamese: bool = False
    ) -> List[Dict[str, Any]]:
        """Generates topic-specific slide outlines via LLM or intelligent structured fallback."""
        content_slide_count = max(3, target_slides - 4)  # Title + KPI + Chart + Table are added natively

        if llm_brain.is_available:
            bilingual_inst = (
                "Include Assamese (অসমীয়া Unicode) subtitle/translations alongside English in headings or key bullets."
                if bilingual_assamese else
                "Use crisp, authoritative executive English."
            )
            prompt = (
                f"Generate exactly {content_slide_count} presentation slides in strict JSON array format for:\n"
                f"Topic: '{query}'\n"
                f"Target District/Region: {district} | Govt Scheme: {scheme or 'Commercial Enterprise'}\n"
                f"Capex: ₹{dpr_data['total_capex_lakhs']} Lakhs | Year-5 Projected Revenue: ₹{dpr_data['revenues_lakhs'][-1]} Lakhs.\n"
                f"{bilingual_inst}\n"
                "Output ONLY valid JSON array of objects: [{\"heading\": \"...\", \"bullets\": [\"...\", \"...\", \"...\"]}]."
            )
            try:
                raw = llm_brain.generate("You are a Boardroom Presentation Architect. Output JSON array only.", prompt, temperature=0.3)
                clean = raw.strip()
                if "```json" in clean:
                    clean = clean.split("```json")[1].split("```")[0].strip()
                elif "```" in clean:
                    clean = clean.split("```")[1].split("```")[0].strip()
                parsed = json.loads(clean)
                if isinstance(parsed, list) and len(parsed) >= 2 and "heading" in parsed[0]:
                    return parsed[:content_slide_count]
            except Exception:
                pass

        # Dynamic topic-aware structured fallback (NO generic static text!)
        scheme_label = scheme or "Private & Institutional Capital"
        return [
            {
                "heading": f"Executive Vision & Opportunity in {district}" + (" (প্ৰকল্পৰ মূল লক্ষ্য)" if bilingual_assamese else ""),
                "bullets": [
                    f"Strategic venture focused on {title} anchored in {district}, Assam & Northeast Corridor.",
                    f"Total Project Outlay: ₹{dpr_data['total_capex_lakhs']} Lakhs backed by {scheme_label}.",
                    f"Projected Year-1 Revenue of ₹{dpr_data['revenues_lakhs'][0]} Lakhs scaling to ₹{dpr_data['revenues_lakhs'][-1]} Lakhs by Year 5."
                ]
            },
            {
                "heading": f"Means of Finance & Subsidy Architecture" + (" (পুঁজি আৰু চৰকাৰী সাহায্য)" if bilingual_assamese else ""),
                "bullets": [
                    f"Promoter Equity Contribution (15%): ₹{dpr_data['promoter_equity_lakhs']} Lakhs.",
                    f"Eligible Government Capital Subsidy: ₹{dpr_data['govt_subsidy_lakhs']} Lakhs under {scheme_label}.",
                    f"Bank Term Loan Requirement: ₹{dpr_data['bank_term_loan_lakhs']} Lakhs | Avg DSCR: {dpr_data['avg_dscr']}x ({dpr_data['bankability_verdict']})."
                ]
            },
            {
                "heading": f"Operations, Supply Chain & Market Catchment ({district})",
                "bullets": [
                    f"Direct distribution reach across {district} and Upper/Lower Assam commercial hubs.",
                    "Automated inventory buffering and monsoon-resilient logistics staging.",
                    "ISO-grade quality assurance, digital billing, and GST compliance integration."
                ]
            },
            {
                "heading": "90-Day Execution & Commercial Rollout Plan",
                "bullets": [
                    "Days 1–30: Site finalization, statutory clearances, and DPR submission to lending bank.",
                    "Days 31–60: Machinery procurement, interior fit-outs, and local talent onboarding.",
                    "Days 61–90: Pilot launch, initial B2B/B2C order fulfillment, and subsidy claim filing."
                ]
            }
        ][:content_slide_count]

    def create_deck(
        self,
        title: str,
        subtitle: str,
        slides_data: List[Dict[str, Any]],
        sector: str = "TECH_BOARDROOM",
        dpr_data: Optional[Dict[str, Any]] = None,
        bilingual_assamese: bool = False,
        bep_chart_path: Optional[str] = None,
        map_img_path: Optional[str] = None,
        white_label_brand: str = "AxomAI Sovereign Advisory",
        udyam_seal: Optional[str] = None
    ) -> Dict[str, Any]:
        theme = SECTOR_THEMES.get(sector, SECTOR_THEMES["TECH_BOARDROOM"])
        bg_rgb = RGBColor(*theme["bg_rgb"])
        card_rgb = RGBColor(*theme["card_rgb"])
        accent_rgb = RGBColor(*theme["accent_rgb"])
        sec_rgb = RGBColor(*theme["secondary_rgb"])

        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        blank_layout = prs.slide_layouts[6]

        # SLIDE 1: EXECUTIVE TITLE SLIDE
        s1 = prs.slides.add_slide(blank_layout)
        s1.background.fill.solid()
        s1.background.fill.fore_color.rgb = bg_rgb

        # Left accent bar
        bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.8), Inches(0.12), Inches(3.6))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent_rgb
        bar.line.fill.background()

        tx1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.0))
        tf1 = tx1.text_frame
        tf1.word_wrap = True
        p1 = tf1.paragraphs[0]
        p1.text = title
        p1.font.bold = True
        p1.font.size = Pt(40)
        p1.font.color.rgb = accent_rgb

        p2 = tf1.add_paragraph()
        assamese_line = f"\n{theme['assamese_subtitle']}" if bilingual_assamese else ""
        seal_txt = f" • UDYAM: {udyam_seal}" if udyam_seal else ""
        p2.text = f"\n{subtitle}{assamese_line}\n{white_label_brand}{seal_txt} • {theme['name']}"
        p2.font.size = Pt(18)
        p2.font.color.rgb = RGBColor(203, 213, 225)

        # SLIDE 2: KPI SNAPSHOT CARDS (if DPR/financial data present)
        if dpr_data:
            s_kpi = prs.slides.add_slide(blank_layout)
            s_kpi.background.fill.solid()
            s_kpi.background.fill.fore_color.rgb = bg_rgb

            hdr = s_kpi.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.0))
            hp = hdr.text_frame.paragraphs[0]
            hp.text = "Key Financial & Project Viability Snapshot" + (" (আৰ্থিক সাৰাংশ)" if bilingual_assamese else "")
            hp.font.bold = True
            hp.font.size = Pt(28)
            hp.font.color.rgb = RGBColor(255, 255, 255)

            kpis = [
                ("Total Project Capex", f"₹{dpr_data['total_capex_lakhs']} L"),
                ("Govt Subsidy Eligible", f"₹{dpr_data['govt_subsidy_lakhs']} L"),
                ("Year-5 Projected Revenue", f"₹{dpr_data['revenues_lakhs'][-1]} L"),
                ("Average DSCR Ratio", f"{dpr_data['avg_dscr']}x")
            ]
            for idx, (lbl, val) in enumerate(kpis):
                left = Inches(0.8 + idx * 3.0)
                card = s_kpi.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.2), Inches(2.7), Inches(2.6))
                card.fill.solid()
                card.fill.fore_color.rgb = card_rgb
                card.line.color.rgb = accent_rgb
                ctf = card.text_frame
                ctf.word_wrap = True
                cp1 = ctf.paragraphs[0]
                cp1.text = f"\n{val}"
                cp1.font.bold = True
                cp1.font.size = Pt(30)
                cp1.font.color.rgb = sec_rgb if idx % 2 else accent_rgb
                cp1.alignment = PP_ALIGN.CENTER
                cp2 = ctf.add_paragraph()
                cp2.text = f"\n{lbl}"
                cp2.font.size = Pt(14)
                cp2.font.color.rgb = RGBColor(203, 213, 225)
                cp2.alignment = PP_ALIGN.CENTER

        # SLIDES 3+: DYNAMIC CONTENT SLIDES
        for s in slides_data:
            slide = prs.slides.add_slide(blank_layout)
            slide.background.fill.solid()
            slide.background.fill.fore_color.rgb = bg_rgb

            hbox = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.7), Inches(1.1))
            htf = hbox.text_frame
            htf.word_wrap = True
            hp = htf.paragraphs[0]
            hp.text = s.get("heading", "Strategic Insight")
            hp.font.bold = True
            hp.font.size = Pt(26)
            hp.font.color.rgb = accent_rgb

            cbox = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
            ctf = cbox.text_frame
            ctf.word_wrap = True
            for i, bullet in enumerate(s.get("bullets", [])):
                bp = ctf.paragraphs[0] if i == 0 else ctf.add_paragraph()
                bp.text = f"▸  {bullet}"
                bp.font.size = Pt(19)
                bp.font.color.rgb = RGBColor(226, 232, 240)
                bp.space_after = Pt(16)

        # NATIVE CHART SLIDE + 5-YEAR TABLE SLIDE (if DPR data present)
        if dpr_data:
            # Native Bar Chart Slide
            s_chart = prs.slides.add_slide(blank_layout)
            s_chart.background.fill.solid()
            s_chart.background.fill.fore_color.rgb = bg_rgb

            chdr = s_chart.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.9))
            chp = chdr.text_frame.paragraphs[0]
            chp.text = "5-Year Revenue & EBITDA Growth Trajectory (₹ Lakhs)"
            chp.font.bold = True
            chp.font.size = Pt(26)
            chp.font.color.rgb = RGBColor(255, 255, 255)

            chart_data = CategoryChartData()
            chart_data.categories = dpr_data["years"]
            chart_data.add_series("Revenue (₹ Lakhs)", dpr_data["revenues_lakhs"])
            chart_data.add_series("EBITDA (₹ Lakhs)", dpr_data["ebitda_lakhs"])

            chart_frame = s_chart.shapes.add_chart(
                XL_CHART_TYPE.COLUMN_CLUSTERED,
                Inches(0.9), Inches(1.5), Inches(11.5), Inches(5.3),
                chart_data
            )
            chart = chart_frame.chart
            chart.has_legend = True

            # Native 5-Year Financial Table Slide
            s_tbl = prs.slides.add_slide(blank_layout)
            s_tbl.background.fill.solid()
            s_tbl.background.fill.fore_color.rgb = bg_rgb

            thdr = s_tbl.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.9))
            thp = thdr.text_frame.paragraphs[0]
            thp.text = f"5-Year Bankable DPR Financial Schedule — {dpr_data['district']}"
            thp.font.bold = True
            thp.font.size = Pt(26)
            thp.font.color.rgb = RGBColor(255, 255, 255)

            tbl_shape = s_tbl.shapes.add_table(6, 5, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.5))
            tbl = tbl_shape.table
            headers = ["Projection Year", "Revenue (₹L)", "EBITDA (₹L)", "Net Profit PAT (₹L)", "DSCR Ratio"]
            for c_idx, h_text in enumerate(headers):
                cell = tbl.cell(0, c_idx)
                cell.fill.solid()
                cell.fill.fore_color.rgb = accent_rgb
                p = cell.text_frame.paragraphs[0]
                p.text = h_text
                p.font.bold = True
                p.font.size = Pt(14)
                p.font.color.rgb = RGBColor(10, 15, 30)

            for r_idx in range(5):
                row_vals = [
                    dpr_data["years"][r_idx],
                    f"₹{dpr_data['revenues_lakhs'][r_idx]}",
                    f"₹{dpr_data['ebitda_lakhs'][r_idx]}",
                    f"₹{dpr_data['pat_lakhs'][r_idx]}",
                    f"{dpr_data['dscr_series'][r_idx]}x"
                ]
                for c_idx, val in enumerate(row_vals):
                    cell = tbl.cell(r_idx + 1, c_idx)
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = card_rgb
                    p = cell.text_frame.paragraphs[0]
                    p.text = val
                    p.font.size = Pt(14)
                    p.font.color.rgb = RGBColor(255, 255, 255)

        # EMBEDDED HIGH-DPI CHARTS & ASSAM CATCHMENT MAP SLIDES
        for img_path, slide_title in [
            (bep_chart_path, "Break-Even Point (BEP) Crossover Chart"),
            (map_img_path, "Assam Strategic Catchment & Highway Corridor Map")
        ]:
            if img_path:
                s_img = prs.slides.add_slide(blank_layout)
                s_img.background.fill.solid()
                s_img.background.fill.fore_color.rgb = bg_rgb
                ihdr = s_img.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.8))
                ihp = ihdr.text_frame.paragraphs[0]
                ihp.text = slide_title
                ihp.font.bold = True
                ihp.font.size = Pt(26)
                ihp.font.color.rgb = accent_rgb
                s_img.shapes.add_picture(img_path, Inches(0.9), Inches(1.3), width=Inches(11.5))

        filename = f"deck_{uuid.uuid4().hex[:8]}.pptx"
        file_path = self.output_dir / filename
        prs.save(str(file_path))

        return {
            "filename": filename,
            "file_path": str(file_path),
            "download_url": f"/api/download/generated/{filename}",
            "slide_count": len(prs.slides),
            "title": title,
            "theme_used": theme["name"]
        }


pptx_builder = PPTXBuilder()
