"""
Z7 Visionary - Dynamic Presentation, DPR, Excel & Generative UI Extractor.
Parses natural language prompts to extract project topic, target Assam/Indian district,
sector theme (Tea, Silk/Handloom, Eco-Tourism, Tech/SaaS, Manufacturing/DPR),
Govt scheme (CMAAA, UNNATI 2024, PMEGP, NABARD), bilingual Assamese flag,
Capex/Investment INR amount, and specific UI widget type (Land Converter, EMI/Subsidy,
Tea Yield, KPI Dashboard, or ROI Simulator).
"""

import re
from typing import Dict, Any, Optional


class VisionaryQueryExtractor:
    """Extracts structured presentation, DPR, spreadsheet, and UI app parameters."""

    ASSAM_DISTRICTS = [
        "guwahati", "kamrup", "changsari", "boko", "dibrugarh", "jorhat", "silchar",
        "tinsukia", "nagaon", "tezpur", "sonitpur", "sivasagar", "majuli", "kaziranga",
        "sualkuchi", "barpeta", "dhubri", "bongaigaon", "lakhimpur", "golaghat", "karimganj"
    ]

    def parse_visionary_query(self, query: str) -> Dict[str, Any]:
        q_lower = query.lower()

        # 1. Detect Mode (UI Widget vs Deck/DPR/Excel)
        is_ui_widget = any(k in q_lower for k in [
            "calculator", "roi", "simulator", "generative ui", "interactive widget",
            "bigha", "katha", "lessa", "land converter", "emi", "dashboard", "micro-app"
        ])
        widget_type = "ROI_SIMULATOR"
        if any(k in q_lower for k in ["bigha", "katha", "lessa", "land converter", "assam land"]):
            widget_type = "ASSAM_LAND_CONVERTER"
        elif any(k in q_lower for k in ["emi", "loan", "subsidy", "cmaaa", "pmegp", "dscr"]):
            widget_type = "LOAN_SUBSIDY_EMI"
        elif any(k in q_lower for k in ["tea", "yield", "garden", "estate"]):
            widget_type = "TEA_YIELD_SIMULATOR"
        elif any(k in q_lower for k in ["kpi", "dashboard", "metrics", "chart"]):
            widget_type = "KPI_DASHBOARD"

        # 2. Detect Sector Theme
        sector = "TECH_BOARDROOM"
        if any(k in q_lower for k in ["tea", "chai", "agri", "bamboo", "agarwood", "horticulture"]):
            sector = "ASSAM_TEA_AGRI"
        elif any(k in q_lower for k in ["silk", "muga", "sualkuchi", "handloom", "weaving", "craft", "msme"]):
            sector = "HERITAGE_SILK_MSME"
        elif any(k in q_lower for k in ["tourism", "kaziranga", "majuli", "resort", "hotel", "eco"]):
            sector = "ECO_TOURISM_NATURE"
        elif any(k in q_lower for k in ["dpr", "cmaaa", "unnati", "pmegp", "nabard", "bank loan", "factory", "plant", "cold storage"]):
            sector = "SOVEREIGN_DPR_INDUSTRIAL"

        # 3. Detect Assam Govt Scheme & District
        scheme = None
        if "cmaaa" in q_lower or "atmanirbhar" in q_lower:
            scheme = "CMAAA (Chief Minister's Atmanirbhar Asom Abhijan)"
        elif "unnati" in q_lower:
            scheme = "UNNATI 2024 (North East Transformative Industrialization Scheme)"
        elif "pmegp" in q_lower:
            scheme = "PMEGP (Prime Minister's Employment Generation Programme)"
        elif "nabard" in q_lower:
            scheme = "NABARD Agri-Infrastructure & Cold-Chain Subsidy"

        district = "Guwahati (Kamrup Metro)"
        for d in self.ASSAM_DISTRICTS:
            if d in q_lower:
                district = d.title()
                break

        # 4. Bilingual Assamese Flag
        is_bilingual_assamese = any(k in q_lower for k in ["assamese", "axomiya", "asomiya", "অসমীয়া", "bilingual"])

        # 5. Extract Capex / Project Investment (INR Lakhs)
        capex_lakhs = 50.0
        m_cr = re.search(r'(?:capex|investment|budget|project cost|loan|outlay)[^.\n]{0,25}?(?:inr|rs\.?|₹)\s*(\d[\d,]*(?:\.\d+)?)\s*(?:cr|crore)\b', q_lower)
        m_lakh = re.search(r'(?:capex|investment|budget|project cost|loan|outlay)[^.\n]{0,25}?(?:inr|rs\.?|₹)\s*(\d[\d,]*(?:\.\d+)?)\s*(?:lakh|lac|l)\b', q_lower)
        if m_cr:
            capex_lakhs = float(m_cr.group(1).replace(",", "")) * 100.0
        elif m_lakh:
            capex_lakhs = float(m_lakh.group(1).replace(",", ""))

        # 6. Extract Slide Count & Excel/HTML5 Need
        m_slides = re.search(r'(\d{1,2})\s*slides?\b', q_lower)
        target_slides = max(5, min(15, int(m_slides.group(1)))) if m_slides else 8

        needs_excel = any(k in q_lower for k in [
            "excel", "xlsx", "spreadsheet", "financial model", "dpr", "capex",
            "retail", "branch", "expansion", "budget", "p&l", "dscr", "cmaaa", "unnati", "pmegp"
        ])

        # Clean Topic Title
        clean_title = re.sub(r'^(create|build|make|generate|design|prepare)\s+(a|an|the)?\s*', '', query.strip(), flags=re.IGNORECASE)
        clean_title = clean_title[:70].strip().rstrip(".")
        if len(clean_title) < 5:
            clean_title = "Executive Strategic Presentation"

        return {
            "title": clean_title.title(),
            "sector": sector,
            "scheme": scheme,
            "district": district,
            "is_bilingual_assamese": is_bilingual_assamese,
            "capex_lakhs": capex_lakhs,
            "target_slides": target_slides,
            "needs_excel": needs_excel,
            "is_ui_widget": is_ui_widget,
            "widget_type": widget_type,
            "raw_query": query
        }


visionary_extractor = VisionaryQueryExtractor()
