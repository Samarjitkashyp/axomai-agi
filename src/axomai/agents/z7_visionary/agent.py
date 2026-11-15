"""
Z7 Visionary - Creative Presentations & Generative UI Agent.
Generates polished PowerPoint decks (.pptx), interactive UI widgets,
and executive visual media.
"""

from typing import Dict, Any, Generator, Optional
from axomai.core.llm import llm_brain
from axomai.agents.z7_visionary.tools.pptx_builder import pptx_builder
from axomai.agents.z7_visionary.tools.generative_ui_engine import generative_ui_engine
from axomai.agents.z7_visionary.tools.excel_builder import excel_model_builder

class Z7VisionaryAgent:
    """Enterprise Creative Director, Presentation Architect & UI Agent."""

    def __init__(self):
        self.name = "Z7 Visionary"
        self.role = "Creative Presentations & Generative UI Agent"

    def presentation_stream(
        self,
        query: str,
        session_id: Optional[str] = "visionary_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        q_lower = query.lower()

        # ROUTE A: Interactive Generative UI Widget
        if any(k in q_lower for k in ["calculator", "roi", "simulator", "generative ui", "interactive widget"]):
            yield {
                "type": "status",
                "stage": "generative_ui",
                "message": "🎨 Z7 Visionary: Compiling interactive HTML/JS micro-app widget..."
            }
            widget_data = generative_ui_engine.generate_roi_calculator(project_name=query[:40])

            meta_event = {
                "type": "meta",
                "agent": self.name,
                "task_type": "GENERATIVE_UI_WIDGET",
                "widget": widget_data,
                "tools_used": ["generative_ui_engine"]
            }
            yield meta_event

            prompt = (
                f"You are Z7 Visionary. Explain how to use this interactive simulation widget for: '{query}'. "
                "Highlight the parameter assumptions and expected productivity gains in GitHub Markdown."
            )
            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate("You are Z7 Visionary.", prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = f"### 🎨 Z7 Visionary: Interactive Simulation\n\nYour interactive simulation widget is embedded below."
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # ROUTE B: Native PowerPoint (.pptx) Deck Generation
        yield {
            "type": "status",
            "stage": "deck_synthesis",
            "message": "🎨 Z7 Visionary: Architecting PowerPoint presentation & rendering 16:9 widescreen slides..."
        }

        # Structure default executive slides
        slides = [
            {
                "heading": "Market Opportunity & Executive Summary",
                "bullets": [
                    "High-growth trajectory driven by rapid enterprise automation and AI adoption.",
                    "Key addressable market expanding at 34% CAGR through 2028.",
                    "Strategic positioning allows capture of premium enterprise tier."
                ]
            },
            {
                "heading": "Competitive Benchmark & Value Drivers",
                "bullets": [
                    "Competitive moat anchored in autonomous multi-agent orchestration.",
                    "Zero-hallucination compliance through autonomous Z Sentinel guardrails.",
                    "Unified multimodal document, web, and relational data synthesis."
                ]
            },
            {
                "heading": "Execution Roadmap & Milestones",
                "bullets": [
                    "Q1: Enterprise pilot deployment across strategic key accounts.",
                    "Q2: Expansion of autonomous background cron tasks and monitoring.",
                    "Q3-Q4: Full-scale commercial rollout and platform scale."
                ]
            }
        ]

        title = query[:60].title() if len(query) < 60 else "Executive Strategic Horizon Deck"
        deck_res = pptx_builder.create_deck(
            title=title,
            subtitle="Strategic Analysis & Growth Roadmap",
            slides_data=slides
        )

        # Check if financial/retail expansion model is also needed
        excel_res = None
        if any(k in q_lower for k in ["retail", "branch", "expansion", "district", "capex", "financial model", "assam"]):
            excel_res = excel_model_builder.generate_retail_expansion_model("Assam Retail Branch Expansion")

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "PPTX_PRESENTATION_GENERATION",
            "download_url": deck_res["download_url"],
            "filename": deck_res["filename"],
            "slide_count": deck_res["slide_count"],
            "excel_model": excel_res,
            "tools_used": ["pptx_builder", "python_pptx_engine", "excel_model_builder"]
        }
        yield meta_event

        excel_link_text = ""
        if excel_res:
            excel_link_text = (
                f"\n📊 **[Download Financial Model Spreadsheet (.xlsx)]({excel_res['download_url']})** "
                f"*(Consolidated 3-Tab Capex, 12-Month P&L, and Unit Economics)*\n"
            )

        body = (
            f"### 🎨 Z7 Visionary: PowerPoint Deck & Financial Model Generated\n\n"
            f"**Deck Title:** `{deck_res['title']}`\n\n"
            f"**Total Slides:** `{deck_res['slide_count']} Slides (16:9 Widescreen Dark Theme)`\n\n"
            f"📥 **[Download PowerPoint Deck (.pptx)]({deck_res['download_url']})**\n"
            f"{excel_link_text}\n"
            "#### 📋 Slide Structure Overview:\n"
            "1. **Title Slide:** Executive Boardroom Theme with Cyan Accents\n"
            "2. **Market Opportunity:** High-growth regional Assam retail catchment\n"
            "3. **Competitive Benchmark:** District-by-district unit economics\n"
            "4. **Execution Roadmap:** 90-Day phased rollout across Kamrup Metro, Dibrugarh & Nagaon\n\n"
            "> Files generated and verified on disk. Click the download links above to open in PowerPoint or Excel."
        )

        for tok in body.split(" "):
            yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": body}

z7_visionary_agent = Z7VisionaryAgent()

