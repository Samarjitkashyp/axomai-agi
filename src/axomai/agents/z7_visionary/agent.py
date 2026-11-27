"""
Z7 Visionary - 13-Tool Pan-India & Assam Presentation, Bankable DPR, VC Pitch, SME IPO & UI Studio.
"""

import re
from typing import Dict, Any, Generator, Optional
from axomai.core.llm import llm_brain
from axomai.agents.z7_visionary.tools.visionary_extractor import visionary_extractor
from axomai.agents.z7_visionary.tools.assam_themes_and_dpr import compute_bankable_dpr_financials
from axomai.agents.z7_visionary.tools.assam_benchmarks_and_schemes import evaluate_assam_benchmarks_and_scheme
from axomai.agents.z7_visionary.tools.pan_india_policies_and_scripts import resolve_pan_india_policy
from axomai.agents.z7_visionary.tools.vc_startup_and_ipo_engine import vc_ipo_engine
from axomai.agents.z7_visionary.tools.brand_kit_and_doc_ingestor import brand_doc_ingestor
from axomai.agents.z7_visionary.tools.chart_and_map_renderer import chart_map_renderer
from axomai.agents.z7_visionary.tools.pptx_builder import pptx_builder
from axomai.agents.z7_visionary.tools.surgical_slide_editor import surgical_slide_editor
from axomai.agents.z7_visionary.tools.docx_dpr_builder import docx_dpr_builder
from axomai.agents.z7_visionary.tools.generative_ui_engine import generative_ui_engine
from axomai.agents.z7_visionary.tools.excel_builder import excel_model_builder
from axomai.agents.z7_visionary.tools.html5_deck_builder import html5_deck_builder


class Z7VisionaryAgent:
    """Pan-India Presentation Architect, VC/IPO Deck Studio, DPR Builder & Micro-App Compiler."""

    def __init__(self):
        self.name = "Z7 Visionary"
        self.role = "13-Tool Pan-India Presentation, VC Pitch, SME IPO, Bankable DPR & UI Studio"

    def presentation_stream(
        self,
        query: str,
        session_id: Optional[str] = "visionary_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        params = visionary_extractor.parse_visionary_query(query)
        q_lower = query.lower()

        # ROUTE 0: Surgical Slide Edit on Existing .pptx
        pptx_m = re.search(r'\b(deck_[a-zA-Z0-9_]+\.pptx)\b', query)
        if pptx_m and any(k in q_lower for k in ["edit slide", "update slide", "change slide"]):
            slide_m = re.search(r'slide\s+(\d+)', q_lower)
            s_num = int(slide_m.group(1)) if slide_m else 2
            edit_res = surgical_slide_editor.edit_existing_slide(
                source_filename=pptx_m.group(1),
                slide_number=s_num,
                new_heading=f"Updated Slide {s_num}: {params['title'][:45]}"
            )
            yield {"type": "meta", "agent": self.name, "task_type": "SURGICAL_SLIDE_EDIT", "edit_result": edit_res, "tools_count": 1, "tools_used": ["surgical_slide_editor"]}
            msg = f"### ✂️ Z7 Visionary: Surgical Slide Edit Complete\n\nUpdated Slide `{edit_res.get('edited_slide_number')}` -> **[Download Edited Deck (.pptx)]({edit_res.get('download_url')})**"
            for tok in msg.split(" "):
                yield {"type": "token", "content": tok + " "}
            yield {"type": "done", "answer": msg}
            return

        # ROUTE A: Dynamic & Arbitrary Prompt-to-Code Generative UI Micro-App
        if params["is_ui_widget"]:
            w_type = params["widget_type"]
            yield {"type": "status", "stage": "generative_ui", "message": f"🎨 Z7 Visionary: Compiling live interactive HTML/JS micro-app ({w_type})..."}
            kpi_metrics = None
            if w_type == "KPI_DASHBOARD":
                kpi_metrics = compute_bankable_dpr_financials(
                    capex_lakhs=params["capex_lakhs"],
                    scheme=params["scheme"],
                    district=params["district"],
                    growth_pct=params.get("growth_pct"),
                    ebitda_margin_pct=params.get("ebitda_margin_pct"),
                    interest_rate_pct=params.get("interest_rate_pct"),
                )
            widget_data = generative_ui_engine.generate_widget(
                widget_type=w_type,
                project_name=params["title"],
                raw_query=query,
                metrics=kpi_metrics,
            )
            yield {"type": "meta", "agent": self.name, "task_type": "GENERATIVE_UI_WIDGET", "widget": widget_data, "tools_count": 2, "tools_used": ["visionary_extractor", "generative_ui_engine"]}
            msg = f"### 🎨 Z7 Visionary: Interactive `{w_type}` Micro-App\n\n📥 **[Download Standalone Micro-App (.html)]({widget_data.get('download_url')})**\n\nYour live interactive widget is embedded below."
            for tok in msg.split(" "):
                yield {"type": "token", "content": tok + " "}
            yield {"type": "done", "answer": msg}
            return

        # ROUTE B: Pan-India + Assam Full Studio (.pptx + .docx + .xlsx + .html + Brand Kit + VC/IPO)
        pan_india = resolve_pan_india_policy(query, language_script=params["language_script"])
        vc_ipo = vc_ipo_engine.compute_vc_or_ipo_metrics(
            query,
            capex_lakhs=params["capex_lakhs"],
            cac_inr=params.get("cac_inr"),
            ltv_inr=params.get("ltv_inr"),
            pre_money_cr=params.get("pre_money_cr"),
            runway_months=params.get("runway_months"),
            tam_cr=params.get("tam_cr"),
        )

        # Live URL Brand Kit Extraction if a website URL is provided
        url_m = re.search(r'(https?://[^\s\)\],\'"]+)', query)
        live_brand = brand_doc_ingestor.extract_brand_kit_from_url(url_m.group(1)) if url_m else None
        doc_context = brand_doc_ingestor.ingest_uploaded_document(doc_id)

        active_brand = live_brand["brand_name"] if live_brand else params["white_label_brand"]
        active_scheme = params["scheme"] or (pan_india["applicable_state_scheme"] if pan_india["is_pan_india_non_assam"] else None)
        active_location = pan_india["industrial_hub"] if pan_india["is_pan_india_non_assam"] else params["district"]

        yield {
            "type": "status",
            "stage": "deck_synthesis",
            "message": f"🎨 Z7 Visionary: Building {vc_ipo['mode']} suite for {active_location} ({pan_india['state']}, Script: {pan_india['script_labels']['script']}, Brand: {active_brand})..."
        }

        # 1. Financials + State Benchmarks
        dpr_data = compute_bankable_dpr_financials(
            capex_lakhs=params["capex_lakhs"],
            scheme=active_scheme,
            district=active_location,
            growth_pct=params.get("growth_pct"),
            ebitda_margin_pct=params.get("ebitda_margin_pct"),
            interest_rate_pct=params.get("interest_rate_pct"),
        )
        benchmarks = evaluate_assam_benchmarks_and_scheme(district=params["district"], capex_lakhs=params["capex_lakhs"], scheme=active_scheme, language_script=pan_india["language_script"])
        # Override script labels & tariff with Pan-India state policy if non-Assam
        benchmarks["script_labels"] = {
            "script_name": pan_india["script_labels"]["script"],
            "dpr_title": pan_india["script_labels"]["dpr_header"],
            "viability": pan_india["script_labels"]["summary"]
        }
        if pan_india["is_pan_india_non_assam"]:
            benchmarks["unnati_zone"] = f"{pan_india['state']} ({pan_india['discom_utility']} Industrial Zone)"
            benchmarks["apdcl_industrial_tariff_inr_kwh"] = pan_india["power_tariff_inr_kwh"]
            benchmarks["aidc_lease_rate_inr_sqft"] = pan_india["industrial_lease_sqft_inr"]

        # 2. High-DPI Break-Even Chart PNG & Catchment Map PNG (Assam OR Pan-India Corridor)
        bep_chart = chart_map_renderer.render_bep_crossover_chart(
            bep_capacity_pct=benchmarks["bep_capacity_pct"],
            bep_revenue_lakhs=benchmarks["bep_revenue_lakhs"],
            yr1_revenue_lakhs=dpr_data["revenues_lakhs"][0]
        )
        assam_map = (
            chart_map_renderer.render_pan_india_corridor_map(target_hub=pan_india["industrial_hub"], target_state=pan_india["state"])
            if pan_india["is_pan_india_non_assam"]
            else chart_map_renderer.render_assam_catchment_map(target_district=params["district"])
        )

        # 3. Synthesize Slides (inject VC/IPO slides & Document Ingestion context if present)
        ctx_query = f"{query}\nDocument Context: {doc_context[:800]}" if doc_context else query
        slides = pptx_builder.synthesize_dynamic_slides(
            query=ctx_query,
            title=params["title"],
            district=active_location,
            scheme=active_scheme,
            dpr_data=dpr_data,
            target_slides=params["target_slides"],
            bilingual_assamese=(pan_india["language_script"] != "english")
        )
        if vc_ipo["is_vc_or_ipo"]:
            slides = vc_ipo["specialized_slides"] + slides[:max(2, len(slides) - len(vc_ipo["specialized_slides"]))]

        # 4. Build Native PowerPoint (.pptx)
        deck_res = pptx_builder.create_deck(
            title=params["title"],
            subtitle=f"{active_location}, {pan_india['state']} • {dpr_data['scheme']}",
            slides_data=slides,
            sector=params["sector"],
            dpr_data=dpr_data,
            bilingual_assamese=(pan_india["language_script"] != "english"),
            bep_chart_path=bep_chart["file_path"],
            map_img_path=assam_map["file_path"] if assam_map else None,
            white_label_brand=active_brand,
            udyam_seal=params["udyam_seal"]
        )

        # 5. Build Bankable DPR Word (.docx)
        docx_res = None
        if params["needs_docx"] or params["needs_excel"]:
            docx_res = docx_dpr_builder.create_bankable_dpr_docx(
                title=params["title"],
                dpr_data=dpr_data,
                benchmarks=benchmarks,
                bep_chart_path=bep_chart["file_path"],
                map_img_path=assam_map["file_path"] if assam_map else None,
                white_label_brand=active_brand,
                udyam_seal=params["udyam_seal"]
            )

        # 6. Build Dynamic Excel (.xlsx)
        excel_res = None
        if params["needs_excel"] or active_scheme is not None:
            excel_res = excel_model_builder.generate_bankable_dpr_excel(project_name=params["title"], dpr_data=dpr_data)

        # 7. Build Interactive HTML5 Pitchbook with Scenario Slider
        web_deck_res = html5_deck_builder.create_web_deck(
            title=params["title"],
            subtitle=f"{active_location}, {pan_india['state']} • {dpr_data['scheme']}",
            slides_data=slides,
            dpr_data=dpr_data,
            sector=params["sector"],
            custom_accent_hex=live_brand["accent_hex"] if live_brand else None
        )

        tools_used = [
            "visionary_extractor", "pan_india_policies_and_scripts", "vc_ipo_engine",
            "brand_doc_ingestor", "assam_themes_and_dpr", "assam_benchmarks_and_schemes",
            "chart_and_map_renderer", "pptx_builder", "html5_deck_builder"
        ]
        if docx_res:
            tools_used.append("docx_dpr_builder")
        if excel_res:
            tools_used.append("excel_model_builder")

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "PAN_INDIA_SOVEREIGN_DECK_STUDIO",
            "pan_india_policy": pan_india,
            "vc_ipo_metrics": vc_ipo,
            "live_brand_kit": live_brand,
            "dpr_financials": dpr_data,
            "assam_benchmarks": benchmarks,
            "bep_chart": bep_chart,
            "assam_catchment_map": assam_map,
            "download_url": deck_res["download_url"],
            "filename": deck_res["filename"],
            "slide_count": deck_res["slide_count"],
            "docx_dpr": docx_res,
            "excel_model": excel_res,
            "html5_web_deck": web_deck_res,
            "tools_count": len(tools_used),
            "tools_used": tools_used
        }
        yield meta_event

        vc_section = ""
        if vc_ipo["is_vc_or_ipo"]:
            vc_section = (
                f"\n#### 🚀 {vc_ipo['mode']} Metrics\n"
                f"- **TAM / SAM / SOM:** `₹{vc_ipo['tam_cr']:,.0f} Cr` / `₹{vc_ipo['sam_cr']:,.0f} Cr` / `₹{vc_ipo['som_cr']:,.1f} Cr`\n"
                f"- **Fundraise / Post-Money / Dilution:** `₹{vc_ipo['raise_cr']} Cr` | `₹{vc_ipo['post_money_valuation_cr']} Cr` | `{vc_ipo['dilution_pct']}%` Dilution\n"
                f"- **Unit Economics:** CAC `₹{vc_ipo['cac_inr']:,.0f}` | LTV `₹{vc_ipo['ltv_inr']:,.0f}` (`{vc_ipo['ltv_cac_ratio']}x`) | Runway `{vc_ipo['runway_months']} Months`\n"
            )

        docx_link = f"\n📄 **[Download Complete Bankable DPR Report (.docx)]({docx_res['download_url']})**" if docx_res else ""
        excel_link = f"\n📊 **[Download Financial Model & DSCR Workbook (.xlsx)]({excel_res['download_url']})**" if excel_res else ""

        body = (
            f"### 🎨 Z7 Visionary: Pan-India Sovereign Presentation & DPR Suite\n\n"
            f"**Project:** `{deck_res['title']}` | **Brand:** `{active_brand}`"
            + (f" (`{live_brand['accent_hex']}`)" if live_brand else "") + "\n\n"
            f"**State / Hub:** `{active_location}, {pan_india['state']}` ({pan_india['discom_utility']} `₹{pan_india['power_tariff_inr_kwh']}/kWh`) | **Language:** `{pan_india['script_labels']['script']}`\n\n"
            f"📥 **[Download PowerPoint Deck (.pptx)]({deck_res['download_url']})** *({deck_res['slide_count']} Slides)*"
            f"{docx_link}{excel_link}\n"
            f"🌐 **[Open Interactive HTML5 Pitchbook with Scenario Slider (.html)]({web_deck_res['download_url']})**\n"
            f"{vc_section}\n"
            "> All deliverables generated dynamically and verified on disk."
        )

        for tok in body.split(" "):
            yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": body}


z7_visionary_agent = Z7VisionaryAgent()
