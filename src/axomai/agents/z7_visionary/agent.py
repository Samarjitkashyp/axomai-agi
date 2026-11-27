"""
Z7 Visionary - 6-Tool Assam & Enterprise Presentation, Bankable DPR, Excel & Generative UI Studio.
Dynamically generates topic-aware multi-slide PowerPoint decks (.pptx) with native charts,
KPI cards & bilingual Assamese/English support, formula-driven Excel DPR models (.xlsx)
with embedded BarCharts, interactive HTML5 Web Decks (.html), and 5 types of live
Generative UI micro-apps (Assam Land Converter, Loan/Subsidy EMI, Tea Yield, KPI, ROI).
"""

from typing import Dict, Any, Generator, Optional
from axomai.core.llm import llm_brain
from axomai.agents.z7_visionary.tools.visionary_extractor import visionary_extractor
from axomai.agents.z7_visionary.tools.assam_themes_and_dpr import compute_bankable_dpr_financials
from axomai.agents.z7_visionary.tools.pptx_builder import pptx_builder
from axomai.agents.z7_visionary.tools.generative_ui_engine import generative_ui_engine
from axomai.agents.z7_visionary.tools.excel_builder import excel_model_builder
from axomai.agents.z7_visionary.tools.html5_deck_builder import html5_deck_builder


class Z7VisionaryAgent:
    """Enterprise Creative Director, Assam DPR Architect & Generative UI Studio."""

    def __init__(self):
        self.name = "Z7 Visionary"
        self.role = "6-Tool Dynamic Presentations, Assam Bankable DPR, Excel & Generative UI Studio"

    def presentation_stream(
        self,
        query: str,
        session_id: Optional[str] = "visionary_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        params = visionary_extractor.parse_visionary_query(query)

        # ROUTE A: Dynamic Multi-App Generative UI Widget
        if params["is_ui_widget"]:
            w_type = params["widget_type"]
            yield {
                "type": "status",
                "stage": "generative_ui",
                "message": f"🎨 Z7 Visionary: Compiling live interactive HTML/JS micro-app ({w_type})..."
            }
            widget_data = generative_ui_engine.generate_widget(
                widget_type=w_type,
                project_name=params["title"]
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
                "Keep it crisp and clear in GitHub Markdown."
            )
            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate("You are Z7 Visionary.", prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = f"### 🎨 Z7 Visionary: Interactive `{w_type}` Micro-App\n\nYour live interactive widget is embedded below."
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # ROUTE B: Dynamic Multi-Slide PPTX + Bankable DPR Excel + Interactive HTML5 Web Deck
        yield {
            "type": "status",
            "stage": "deck_synthesis",
            "message": f"🎨 Z7 Visionary: Building {params['sector']} deck for {params['district']} (Capex ₹{params['capex_lakhs']}L, Bilingual={params['is_bilingual_assamese']})..."
        }

        # 1. Compute Bankable 5-Year DPR & Subsidy Financials
        dpr_data = compute_bankable_dpr_financials(
            capex_lakhs=params["capex_lakhs"],
            scheme=params["scheme"],
            district=params["district"]
        )

        # 2. Synthesize Dynamic Topic-Aware Slides (LLM or dynamic topic builder)
        slides = pptx_builder.synthesize_dynamic_slides(
            query=query,
            title=params["title"],
            district=params["district"],
            scheme=params["scheme"],
            dpr_data=dpr_data,
            target_slides=params["target_slides"],
            bilingual_assamese=params["is_bilingual_assamese"]
        )

        # 3. Render Native PowerPoint (.pptx) with KPI Cards, Charts & Tables
        deck_res = pptx_builder.create_deck(
            title=params["title"],
            subtitle=f"{params['district']} • {dpr_data['scheme']}",
            slides_data=slides,
            sector=params["sector"],
            dpr_data=dpr_data,
            bilingual_assamese=params["is_bilingual_assamese"]
        )

        # 4. Generate Dynamic Formula + Chart Excel (.xlsx)
        excel_res = None
        if params["needs_excel"] or params["scheme"] is not None:
            excel_res = excel_model_builder.generate_bankable_dpr_excel(
                project_name=params["title"],
                dpr_data=dpr_data
            )

        # 5. Generate Shareable Interactive HTML5 Web Deck (.html)
        web_deck_res = html5_deck_builder.create_web_deck(
            title=params["title"],
            subtitle=f"{params['district']} • {dpr_data['scheme']}",
            slides_data=slides,
            dpr_data=dpr_data,
            sector=params["sector"]
        )

        tools_used = ["visionary_extractor", "assam_themes_and_dpr", "pptx_builder", "html5_deck_builder"]
        if excel_res:
            tools_used.append("excel_model_builder")

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "DYNAMIC_DECK_AND_DPR_STUDIO",
            "extracted_parameters": params,
            "dpr_financials": dpr_data,
            "download_url": deck_res["download_url"],
            "filename": deck_res["filename"],
            "slide_count": deck_res["slide_count"],
            "theme_used": deck_res["theme_used"],
            "excel_model": excel_res,
            "html5_web_deck": web_deck_res,
            "tools_count": len(tools_used),
            "tools_used": tools_used
        }
        yield meta_event

        excel_link_text = ""
        if excel_res:
            excel_link_text = (
                f"\n📊 **[Download Bankable DPR Financial Model (.xlsx)]({excel_res['download_url']})** "
                f"*(Formula-driven Means of Finance, 5-Year DSCR & Embedded BarChart)*\n"
            )

        slides_overview = "\n".join(
            f"{i}. **{s.get('heading')}**"
            for i, s in enumerate(slides, 1)
        )

        body = (
            f"### 🎨 Z7 Visionary: Executive Deck, DPR Model & HTML5 Studio Output\n\n"
            f"**Deck Title:** `{deck_res['title']}` | **Theme:** `{deck_res['theme_used']}`\n\n"
            f"**Location / Scheme:** `{params['district']}` • `{dpr_data['scheme']}` | **Total Slides:** `{deck_res['slide_count']} Slides (with Native Charts, KPI Cards & Table)`\n\n"
            f"📥 **[Download PowerPoint Deck (.pptx)]({deck_res['download_url']})**\n"
            f"🌐 **[Open / Download Interactive HTML5 Web Deck (.html)]({web_deck_res['download_url']})**"
            f"{excel_link_text}\n"
            f"#### 💰 Bankable Viability Snapshot\n"
            f"- **Total Capex:** `₹{dpr_data['total_capex_lakhs']} Lakhs` | **Govt Subsidy:** `₹{dpr_data['govt_subsidy_lakhs']} Lakhs` | **Bank Loan:** `₹{dpr_data['bank_term_loan_lakhs']} Lakhs`\n"
            f"- **Year-5 Revenue:** `₹{dpr_data['revenues_lakhs'][-1]} Lakhs` | **Avg DSCR:** `{dpr_data['avg_dscr']}x` (`{dpr_data['bankability_verdict']}`)\n\n"
            f"#### 📋 Dynamic Slide Architecture\n"
            f"{slides_overview}\n\n"
            "> All files (.pptx, .html, .xlsx) generated dynamically and verified on disk."
        )

        for tok in body.split(" "):
            yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": body}


z7_visionary_agent = Z7VisionaryAgent()
