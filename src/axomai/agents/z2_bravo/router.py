"""
Z2 Bravo Intent Router & Query Planner.
Analyzes user web research inquiries, classifies research task types,
and generates optimal search query vectors.
"""

import re
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Tuple
from axomai.core.llm import llm_brain

class ResearchTaskType(str, Enum):
    MARKET_ANALYSIS = "MARKET_ANALYSIS"
    COMPETITOR_BENCHMARK = "COMPETITOR_BENCHMARK"
    FACT_CHECK_NEWS = "FACT_CHECK_NEWS"
    CROSS_DOC_RESEARCH = "CROSS_DOC_RESEARCH"
    DOSSIER_EXPORT = "DOSSIER_EXPORT"
    DEEP_RESEARCH = "DEEP_RESEARCH"

class ResearchRouter:
    """Plans research vectors and routes queries for Z2 Bravo"""

    def plan_research(self, query: str, has_active_document: bool = False) -> Dict[str, Any]:
        q = query.lower().strip()
        params: Dict[str, Any] = {}

        # 1. Dossier Export request
        if any(w in q for w in ["dossier", "pdf report", "download report", "full report", "pdf bana", "word report", "export dossier"]):
            task_type = ResearchTaskType.DOSSIER_EXPORT
            params["format"] = "docx" if any(w in q for w in ["word", "doc", "docx"]) else "pdf"

        # 2. Cross-Document intelligence request (if active doc is present)
        elif has_active_document and any(w in q for w in ["compare", "market", "competitor", "is document", "sheet ke sath", "hamare product", "benchmarking"]):
            task_type = ResearchTaskType.CROSS_DOC_RESEARCH

        # 3. Competitor benchmarking
        elif any(w in q for w in ["vs", "versus", "compare", "competitor", "benchmarking", "pricing comparison", "alternatives"]):
            task_type = ResearchTaskType.COMPETITOR_BENCHMARK
            params["requires_matrix"] = True

        # 4. Market Analysis & Industry trends
        elif any(w in q for w in ["market size", "market share", "cagr", "growth", "industry trends", "outlook", "projection", "forecast"]):
            task_type = ResearchTaskType.MARKET_ANALYSIS

        # 5. Fact checking & news verification
        elif any(w in q for w in ["fact check", "sach hai kya", "real or fake", "latest news", "official announcement", "kya ye sach", "verified"]):
            task_type = ResearchTaskType.FACT_CHECK_NEWS

        else:
            task_type = ResearchTaskType.DEEP_RESEARCH

        # Generate strategic search query vectors
        search_queries = self._generate_search_vectors(query, task_type)
        params["search_queries"] = search_queries

        return {
            "task_type": task_type,
            "params": params
        }

    def _generate_search_vectors(self, query: str, task_type: ResearchTaskType) -> List[str]:
        """
        Uses LLM or heuristic fallback to formulate 2-3 high-yield search engine queries.
        """
        from axomai.agents.z2_bravo.tools.web_search import clean_conversational_query
        today_str = datetime.now().strftime("%B %d, %Y")
        current_year = datetime.now().strftime("%Y")

        # If it specifically targets Assam commercial expansion, provide instant ultra-fast query vectors
        q_lower = query.lower()
        if "assam" in q_lower and ("retail" in q_lower or "district" in q_lower or "branch" in q_lower):
            return [
                "Kamrup Metropolitan commercial retail market Assam",
                "Nagaon retail market commercial trade Assam",
                "Dibrugarh commercial retail market Assam"
            ]

        if llm_brain.is_available:
            try:
                sys_prompt = (
                    f"You are an expert Web Search Intelligence Strategist. Today's date is {today_str}.\n"
                    "Given the user's research topic, output exactly 2 to 3 concise, distinct search queries "
                    "that will retrieve the most authoritative, recent, and relevant data from Google/DuckDuckGo.\n"
                    "Rules:\n"
                    "1. One query per line, no numbering, no bullets, no quotes.\n"
                    f"2. For time-sensitive, today, or recent topics, target {current_year} or 'today live' / 'latest'. Never use past years like 2024 unless specifically asked.\n"
                    "3. For market up/down questions, query major indices like Sensex, Nifty, Dow Jones, S&P 500.\n"
                    "4. Keep each query strictly between 3 to 6 high-intent search keywords. Never output full sentences."
                )
                raw = llm_brain.generate(sys_prompt, f"User Research Topic: {query}", temperature=0.1)
                lines = [line.strip().lstrip("-*1234. ") for line in raw.strip().splitlines() if line.strip()]
                if lines:
                    return lines[:3]
            except Exception:
                pass

        # Fallback heuristic query vectors
        base = clean_conversational_query(query)
        if "market" in q_lower and ("up" in q_lower or "down" in q_lower or "today" in q_lower):
            return [
                "stock market today live indices Sensex Nifty",
                f"share market today news {current_year}",
                "global stock market up down today"
            ]
        elif task_type == ResearchTaskType.COMPETITOR_BENCHMARK:
            return [base, f"{base} comparison specs pricing", f"{base} market share"]
        elif task_type == ResearchTaskType.MARKET_ANALYSIS:
            return [base, f"{base} market size growth trends {current_year}", f"{base} industry outlook"]
        elif task_type == ResearchTaskType.FACT_CHECK_NEWS:
            return [base, f"{base} official news announcement", f"{base} fact check"]
        else:
            return [base, f"{base} overview analysis", f"{base} key findings"]


research_router = ResearchRouter()

