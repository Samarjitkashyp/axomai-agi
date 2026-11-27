"""
Z7 Visionary - Dynamic Presentation, DPR, Excel, White-Label & Generative UI Extractor.
Extracts topic, Assam district, sector theme, Govt scheme, multi-script language
(Assamese, Bodo, Bengali, English), Capex INR, White-Label Brand Name/UDYAM/CIN,
and Generative UI mode (including arbitrary prompt-to-code micro-apps).
"""

import re
from typing import Dict, Any, Optional


class VisionaryQueryExtractor:
    """Extracts structured presentation, DPR, spreadsheet, white-label, and UI parameters."""

    ASSAM_DISTRICTS = [
        "guwahati", "kamrup", "changsari", "boko", "dibrugarh", "jorhat", "silchar",
        "tinsukia", "nagaon", "tezpur", "sonitpur", "sivasagar", "majuli", "kaziranga",
        "sualkuchi", "barpeta", "dhubri", "bongaigaon", "lakhimpur", "golaghat", "karimganj",
        "kokrajhar"
    ]

    def parse_visionary_query(self, query: str) -> Dict[str, Any]:
        q_lower = query.lower()

        # 1. Detect Mode (UI Widget vs Deck/DPR/Excel/Docx)
        is_ui_widget = any(k in q_lower for k in [
            "calculator", "roi", "simulator", "generative ui", "interactive widget",
            "bigha", "katha", "lessa", "land converter", "emi", "dashboard", "micro-app",
            "bill estimator", "yield calculator"
        ])
        widget_type = "CUSTOM_DYNAMIC_APP"
        if any(k in q_lower for k in ["bigha", "katha", "lessa", "land converter", "assam land"]):
            widget_type = "ASSAM_LAND_CONVERTER"
        elif any(k in q_lower for k in ["emi", "loan", "subsidy", "cmaaa", "pmegp", "dscr"]):
            widget_type = "LOAN_SUBSIDY_EMI"
        elif any(k in q_lower for k in ["tea yield", "tea estate", "plucking"]):
            widget_type = "TEA_YIELD_SIMULATOR"
        elif any(k in q_lower for k in ["kpi", "dashboard"]):
            widget_type = "KPI_DASHBOARD"
        elif any(k in q_lower for k in ["roi calculator", "roi simulator"]):
            widget_type = "ROI_SIMULATOR"

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

        district = "Guwahati"
        for d in self.ASSAM_DISTRICTS:
            if d in q_lower:
                district = d.title()
                break

        # 4. Multi-Script Language Detection (Assamese, Bodo, Bengali, English)
        language_script = "english"
        if any(k in q_lower for k in ["assamese", "axomiya", "asomiya", "অসমীয়া"]):
            language_script = "assamese"
        elif any(k in q_lower for k in ["bodo", "बड़ो", "btr"]):
            language_script = "bodo"
        elif any(k in q_lower for k in ["bengali", "bangla", "বাংলা"]):
            language_script = "bengali"
        is_bilingual = language_script != "english" or "bilingual" in q_lower

        # 5. Extract Capex / Project Investment (INR Lakhs)
        capex_lakhs = 50.0
        m_cr = re.search(r'(?:capex|investment|budget|project cost|loan|outlay)[^.\n]{0,25}?(?:inr|rs\.?|₹)\s*(\d[\d,]*(?:\.\d+)?)\s*(?:cr|crore)\b', q_lower)
        m_lakh = re.search(r'(?:capex|investment|budget|project cost|loan|outlay)[^.\n]{0,25}?(?:inr|rs\.?|₹)\s*(\d[\d,]*(?:\.\d+)?)\s*(?:lakh|lac|l)\b', q_lower)
        if m_cr:
            capex_lakhs = float(m_cr.group(1).replace(",", "")) * 100.0
        elif m_lakh:
            capex_lakhs = float(m_lakh.group(1).replace(",", ""))

        # 6. White-Label Brand Kit & UDYAM/CIN Seal Extraction
        brand_match = re.search(r'(?:brand|company|firm|prepared by|white-label)[:\s]+([A-Za-z0-9\s&\.\-]+?)(?:\s+with|\s+udyam|\s+cin|,|\.|$)', query, re.IGNORECASE)
        white_label_brand = brand_match.group(1).strip() if brand_match else "AxomAI Sovereign Advisory"

        udyam_match = re.search(r'\b(UDYAM-[A-Z]{2}-\d{2}-\d{7})\b', query, re.IGNORECASE)
        udyam_seal = udyam_match.group(1).upper() if udyam_match else None

        # 6b. Dynamic Financial & VC/IPO Parameter Extraction (eliminates static defaults when specified)
        def _extract_num(pattern: str) -> Optional[float]:
            m = re.search(pattern, q_lower)
            if m:
                try:
                    return float(m.group(1).replace(",", ""))
                except Exception:
                    return None
            return None

        growth_pct = _extract_num(r'(?:growth|cagr)\s*(?:rate|of|:|=|at)?\s*(\d+(?:\.\d+)?)\s*%')
        ebitda_margin_pct = _extract_num(r'(?:ebitda|margin)\s*(?:margin|of|:|=|at)?\s*(\d+(?:\.\d+)?)\s*%')
        interest_rate_pct = _extract_num(r'(?:interest|roi|rate)\s*(?:rate|of|:|=|at)?\s*(\d+(?:\.\d+)?)\s*%')
        cac_inr = _extract_num(r'\bcac\b[^.\n]{0,15}?(?:inr|rs\.?|₹)?\s*(\d[\d,]*(?:\.\d+)?)')
        ltv_inr = _extract_num(r'\bltv\b[^.\n]{0,15}?(?:inr|rs\.?|₹)?\s*(\d[\d,]*(?:\.\d+)?)')
        pre_money_cr = _extract_num(r'pre[-\s]?money(?:\s*valuation)?[^.\n]{0,15}?(?:inr|rs\.?|₹)?\s*(\d[\d,]*(?:\.\d+)?)\s*(?:cr|crore)?')
        runway_val = _extract_num(r'\brunway\b[^.\n]{0,15}?(\d+)\s*(?:months?|mos?|m)\b')
        runway_months = int(runway_val) if runway_val else None
        tam_cr = _extract_num(r'\btam\b[^.\n]{0,15}?(?:inr|rs\.?|₹)?\s*(\d[\d,]*(?:\.\d+)?)\s*(?:cr|crore)?')

        # 7. Output Formats Needed
        m_slides = re.search(r'(\d{1,2})\s*slides?\b', q_lower)
        target_slides = max(5, min(15, int(m_slides.group(1)))) if m_slides else 8

        needs_excel = any(k in q_lower for k in [
            "excel", "xlsx", "spreadsheet", "financial model", "dpr", "capex",
            "retail", "branch", "expansion", "budget", "p&l", "dscr", "cmaaa", "unnati", "pmegp"
        ])
        needs_docx = any(k in q_lower for k in [
            "docx", "word", "project report", "dpr", "bankable", "sbi", "agvb", "nedfi", "cmaaa", "unnati", "pmegp"
        ])

        clean_title = re.sub(r'^(create|build|make|generate|design|prepare)\s+(a|an|the)?\s*', '', query.strip(), flags=re.IGNORECASE)
        clean_title = clean_title[:70].strip().rstrip(".")
        if len(clean_title) < 5:
            clean_title = "Executive Strategic Presentation"

        return {
            "title": clean_title.title(),
            "sector": sector,
            "scheme": scheme,
            "district": district,
            "language_script": language_script,
            "is_bilingual": is_bilingual,
            "is_bilingual_assamese": language_script == "assamese" or is_bilingual,
            "capex_lakhs": capex_lakhs,
            "growth_pct": growth_pct,
            "ebitda_margin_pct": ebitda_margin_pct,
            "interest_rate_pct": interest_rate_pct,
            "cac_inr": cac_inr,
            "ltv_inr": ltv_inr,
            "pre_money_cr": pre_money_cr,
            "runway_months": runway_months,
            "tam_cr": tam_cr,
            "white_label_brand": white_label_brand,
            "udyam_seal": udyam_seal,
            "target_slides": target_slides,
            "needs_excel": needs_excel,
            "needs_docx": needs_docx,
            "is_ui_widget": is_ui_widget,
            "widget_type": widget_type,
            "raw_query": query
        }


visionary_extractor = VisionaryQueryExtractor()
