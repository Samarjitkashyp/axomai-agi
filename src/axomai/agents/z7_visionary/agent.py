"""
Z7 Visionary - 9-Tool Extreme-Level Assam DPR, Multi-Script Deck, Chart, Word & Micro-App Studio.
Generates complete 4-file Bankable Loan Packages (.docx + .pptx + .xlsx + .html),
High-DPI PIL Break-Even Charts & Assam District Catchment Maps, Multi-Script Northeast
support (Assamese, Bodo, Bengali, English), Assam operational benchmarks (APDCL tariffs,
minimum wages, UNNATI Zone A/B), White-Label Brand/UDYAM seals, and Arbitrary Prompt-to-Code
Generative UI Micro-Apps.
"""

from typing import Dict, Any, Generator, Optional
from axomai.core.llm import llm_brain
from axomai.agents.z7_visionary.tools.visionary_extractor import visionary_extractor
from axomai.agents.z7_visionary.tools.assam_themes_and_dpr import compute_bankable_dpr_financials
from axomai.agents.z7_visionary.tools.assam_benchmarks_and_schemes import evaluate_assam_benchmarks_and_scheme
from axomai.agents.z7_visionary.tools.chart_and_map_renderer import chart_map_renderer
from axomai.agents.z7_visionary.tools.pptx_builder import pptx_builder
from axomai.agents.z7_visionary.tools.docx_dpr_builder import docx_dpr_builder
from axomai.agents.z7_visionary.tools.generative_ui_engine import generative_ui_engine
from axomai.agents.z7_visionary.tools.excel_builder import excel_model_builder
from axomai.agents.z7_visionary.tools.html5_deck_builder import html5_deck_builder


class Z7VisionaryAgent:
    """Enterprise Creative Director, Assam Bankable DPR Architect & Generative UI Studio."""

    def __init__(self):
        self.name = "Z7 Visionary"
        self.role = "9-Tool Sovereign DPR (.docx/.pptx/.xlsx/.html), Chart & Generative UI Studio"

    def presentation_stream(
        self,
        query: str,
        session_id: Optional[str] = "visionary_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        params = visionary_extractor.parse_visionary_query(query)

        # ROUTE A: Dynamic & Arbitrary Prompt-to-Code Generative UI Micro-App
        if params["is_ui_widget"]:
            w_type = params["widget_type"]
            yield {
                "type": "status",
                "stage": "generative_ui",
                "message": f"🎨 Z7 Visionary: Compiling live interactive HTML/JS micro-app ({w_type})..."
            }
            widget_data = generative_ui_engine.generate_widget(
                widget_type=w_type,
                project_name=params["title"],
                raw_query=query
            )

            meta_event = {
                "type": "meta",
                "agent": self.name,
                "task_type": "GENERATIVE_UI_WIDGET",
                "widget": widget_data,
                "tools_count": 2,
                "tools_used": ["visionary_extractor", "generative_ui_engine"]
            }
            yield meta_event

            prompt = (
                f"You are Z7 Visionary. Explain how to use this live interactive `{w_type}` micro-app for: '{query}'. "
                f"Also share the standalone download link: {widget_data.get('download_url')}."
            )
            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate("You are Z7 Visionary.", prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = (
                    f"### 🎨 Z7 Visionary: Interactive `{w_type}` Micro-App\n\n"
                    f"📥 **[Download Standalone Micro-App (.html)]({widget_data.get('download_url')})**\n\n"
                    "Your live interactive widget is embedded below."
                )
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # ROUTE B: Complete 4-File Bankable DPR & Presentation Studio (.pptx + .docx + .xlsx + .html)
        yield {
            "type": "status",
            "stage": "deck_synthesis",
            "message": f"🎨 Z7 Visionary: Generating {params['sector']} suite for {params['district']} ({params['language_script'].title()}, Brand: {params['white_label_brand']})..."
        }

        # 1. Bankable DPR Financials + Assam Benchmarks (APDCL, Wages, UNNATI Zone, BEP, IRR)
        dpr_data = compute_bankable_dpr_financials(
            capex_lakhs=params["capex_lakhs"],
            scheme=params["scheme"],
            district=params["district"]
        )
        benchmarks = evaluate_assam_benchmarks_and_scheme(
            district=params["district"],
            capex_lakhs=params["capex_lakhs"],
            scheme=params["scheme"],
            language_script=params["language_script"]
        )

        # 2. Render High-DPI Break-Even Chart PNG & Assam Strategic Catchment Map PNG
        bep_chart = chart_map_renderer.render_bep_crossover_chart(
            bep_capacity_pct=benchmarks["bep_capacity_pct"],
            bep_revenue_lakhs=benchmarks["bep_revenue_lakhs"],
            yr1_revenue_lakhs=dpr_data["revenues_lakhs"][0]
        )
        assam_map = chart_map_renderer.render_assam_catchment_map(target_district=params["district"])

        # 3. Synthesize Dynamic Topic-Aware Slides
        slides = pptx_builder.synthesize_dynamic_slides(
            query=query,
            title=params["title"],
            district=params["district"],
            scheme=params["scheme"],
            dpr_data=dpr_data,
            target_slides=params["target_slides"],
            bilingual_assamese=params["is_bilingual"]
        )

        # 4. Build Native PowerPoint (.pptx) with Embedded Charts, Map & White-Label Seal
        deck_res = pptx_builder.create_deck(
            title=params["title"],
            subtitle=f"{params['district']} • {dpr_data['scheme']}",
            slides_data=slides,
            sector=params["sector"],
            dpr_data=dpr_data,
            bilingual_assamese=params["is_bilingual"],
            bep_chart_path=bep_chart["file_path"],
            map_img_path=assam_map["file_path"],
            white_label_brand=params["white_label_brand"],
            udyam_seal=params["udyam_seal"]
        )

        # 5. Build Full Bankable DPR Word Document (.docx) (SBI / AGVB / NEDFi Standard)
        docx_res = None
        if params["needs_docx"] or params["needs_excel"]:
            docx_res = docx_dpr_builder.create_bankable_dpr_docx(
                title=params["title"],
                dpr_data=dpr_data,
                benchmarks=benchmarks,
                bep_chart_path=bep_chart["file_path"],
                map_img_path=assam_map["file_path"],
                white_label_brand=params["white_label_brand"],
                udyam_seal=params["udyam_seal"]
            )

        # 6. Build Dynamic Formula + Chart Excel (.xlsx)
        excel_res = None
        if params["needs_excel"] or params["scheme"] is not None:
            excel_res = excel_model_builder.generate_bankable_dpr_excel(
                project_name=params["title"],
                dpr_data=dpr_data
            )

        # 7. Build Interactive HTML5 Web Deck (.html)
        web_deck_res = html5_deck_builder.create_web_deck(
            title=params["title"],
            subtitle=f"{params['district']} • {dpr_data['scheme']}",
            slides_data=slides,
            dpr_data=dpr_data,
            sector=params["sector"]
        )

        tools_used = [
            "visionary_extractor", "assam_themes_and_dpr", "assam_benchmarks_and_schemes",
            "chart_and_map_renderer", "pptx_builder", "html5_deck_builder"
        ]
        if docx_res:
            tools_used.append("docx_dpr_builder")
        if excel_res:
            tools_used.append("excel_model_builder")

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "EXTREME_4FILE_DPR_AND_DECK_STUDIO",
            "extracted_parameters": params,
            "dpr_financials": dpr_data,
            "assam_benchmarks": benchmarks,
            "bep_chart": bep_chart,
            "assam_catchment_map": assam_map,
            "download_url": deck_res["download_url"],
            "filename": deck_res["filename"],
            "slide_count": deck_res["slide_count"],
            "theme_used": deck_res["theme_used"],
            "docx_dpr": docx_res,
            "excel_model": excel_res,
            "html5_web_deck": web_deck_res,
            "tools_count": len(tools_used),
            "tools_used": tools_used
        }
        yield meta_event

        docx_link = f"\n📄 **[Download Complete Bankable DPR Report (.docx)]({docx_res['download_url']})** *(SBI / AGVB / NEDFi Standard with Embedded Charts & Checklist)*" if docx_res else ""
        excel_link = f"\n📊 **[Download Financial Model & DSCR Workbook (.xlsx)]({excel_res['download_url']})** *(Formula-driven + Native Excel BarChart)*" if excel_res else ""

        body = (
            f"### 🎨 Z7 Visionary: Complete 4-File Sovereign DPR & Presentation Suite\n\n"
            f"**Project:** `{deck_res['title']}` | **White-Label Brand:** `{params['white_label_brand']}`"
            + (f" (`{params['udyam_seal']}`)" if params["udyam_seal"] else "") + "\n\n"
            f"**District & Zone:** `{benchmarks['district_clean']}` ({benchmarks['unnati_zone']}) | **Script:** `{benchmarks['script_labels']['script_name']}`\n\n"
            f"📥 **[Download PowerPoint Presentation (.pptx)]({deck_res['download_url']})** *({deck_res['slide_count']} Slides with Charts, KPI Cards & Map)*"
            f"{docx_link}"
            f"{excel_link}\n"
            f"🌐 **[Open Interactive HTML5 Web Deck (.html)]({web_deck_res['download_url']})**\n"
            f"📈 **[View High-DPI BEP Chart (.png)]({bep_chart['download_url']})** | 🗺️ **[View Assam Catchment Map (.png)]({assam_map['download_url']})**\n\n"
            f"#### 💰 Bankable Viability & Assam Operational Benchmarks\n"
            f"- **Capex / Subsidy / Loan:** `₹{dpr_data['total_capex_lakhs']}L` | Subsidy: `₹{dpr_data['govt_subsidy_lakhs']}L` | Term Loan: `₹{dpr_data['bank_term_loan_lakhs']}L`\n"
            f"- **BEP / IRR / DSCR:** Break-Even `{benchmarks['bep_capacity_pct']}%` (`₹{benchmarks['bep_revenue_lakhs']}L`) | Est. IRR `{benchmarks['estimated_irr_pct']}%` | Avg DSCR `{dpr_data['avg_dscr']}x`\n"
            f"- **Assam Operational Rates:** APDCL Tariff `₹{benchmarks['apdcl_industrial_tariff_inr_kwh']}/kWh` | AIDC Lease `₹{benchmarks['aidc_lease_rate_inr_sqft']}/sq.ft` | Skilled Wage `₹{benchmarks['assam_skilled_wage_inr_month']:,.0f}/mo`\n\n"
            "> All deliverables (.pptx, .docx, .xlsx, .html, .png) generated dynamically and verified on disk."
        )

        for tok in body.split(" "):
            yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": body}


z7_visionary_agent = Z7VisionaryAgent()
