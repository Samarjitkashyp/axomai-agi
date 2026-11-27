"""
Z7 Visionary - Assam Sector Brand Themes, Bilingual Assamese Labels & DPR Financials.
Provides executive color palettes for Assam Tea/Agri, Sualkuchi Silk/MSME,
Kaziranga Eco-Tourism, Sovereign Industrial DPR, and Dark Tech Boardroom,
plus bankable 5-year DSCR / Subsidy financials for CMAAA, UNNATI 2024, and PMEGP.
"""

from typing import Dict, Any, List, Optional


SECTOR_THEMES = {
    "ASSAM_TEA_AGRI": {
        "name": "Assam Tea & Agri-Export Heritage",
        "bg_rgb": (10, 28, 22),
        "card_rgb": (18, 45, 35),
        "accent_rgb": (212, 175, 55),
        "secondary_rgb": (52, 211, 153),
        "hex_bg": "#0a1c16",
        "hex_accent": "#d4af37",
        "assamese_subtitle": "অসম চাহ আৰু কৃষি-ৰপ্তানি উদ্যোগ"
    },
    "HERITAGE_SILK_MSME": {
        "name": "Sualkuchi Muga Silk & Assam MSME",
        "bg_rgb": (28, 16, 20),
        "card_rgb": (48, 26, 32),
        "accent_rgb": (245, 158, 11),
        "secondary_rgb": (244, 63, 94),
        "hex_bg": "#1c1014",
        "hex_accent": "#f59e0b",
        "assamese_subtitle": "অসমৰ মুগা শিল্প আৰু ক্ষুদ্ৰ-মজলীয়া উদ্যোগ"
    },
    "ECO_TOURISM_NATURE": {
        "name": "Kaziranga & Majuli Eco-Tourism",
        "bg_rgb": (12, 25, 36),
        "card_rgb": (20, 42, 58),
        "accent_rgb": (45, 212, 191),
        "secondary_rgb": (163, 230, 53),
        "hex_bg": "#0c1924",
        "hex_accent": "#2dd4bf",
        "assamese_subtitle": "কাজিৰঙা আৰু মাজুলী পৰিৱেশ-পৰ্যটন"
    },
    "SOVEREIGN_DPR_INDUSTRIAL": {
        "name": "Assam Industrial DPR & Govt Subsidy",
        "bg_rgb": (15, 23, 42),
        "card_rgb": (30, 41, 59),
        "accent_rgb": (56, 189, 248),
        "secondary_rgb": (34, 197, 94),
        "hex_bg": "#0f172a",
        "hex_accent": "#38bdf8",
        "assamese_subtitle": "বিস্তৃত প্ৰকল্প প্ৰতিবেদন (DPR) আৰু চৰকাৰী সাহায্য"
    },
    "TECH_BOARDROOM": {
        "name": "Executive Tech & Boardroom Dark",
        "bg_rgb": (10, 15, 30),
        "card_rgb": (20, 30, 52),
        "accent_rgb": (0, 229, 255),
        "secondary_rgb": (129, 140, 248),
        "hex_bg": "#0a0f1e",
        "hex_accent": "#00e5ff",
        "assamese_subtitle": "কাৰ্যবাহী কৌশলগত উপস্থাপন"
    }
}


def compute_bankable_dpr_financials(
    capex_lakhs: float = 50.0,
    scheme: Optional[str] = None,
    district: str = "Guwahati"
) -> Dict[str, Any]:
    """Computes 5-Year Revenue, EBITDA, Subsidy, Loan EMI & DSCR for Assam Bankable DPRs."""
    subsidy_pct = 0.0
    if scheme and "CMAAA" in scheme:
        subsidy_pct = 50.0
    elif scheme and "UNNATI" in scheme:
        subsidy_pct = 30.0
    elif scheme and "PMEGP" in scheme:
        subsidy_pct = 35.0
    elif scheme and "NABARD" in scheme:
        subsidy_pct = 33.3

    subsidy_lakhs = round(min(capex_lakhs * (subsidy_pct / 100.0), 500.0), 2)
    promoter_margin_lakhs = round(capex_lakhs * 0.15, 2)
    term_loan_lakhs = round(max(0.0, capex_lakhs - promoter_margin_lakhs - subsidy_lakhs), 2)

    years = ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    revenues_lakhs = []
    ebitda_lakhs = []
    pat_lakhs = []
    dscr_list = []

    base_rev = capex_lakhs * 1.45
    annual_debt_service = round((term_loan_lakhs / 5.0) + (term_loan_lakhs * 0.095), 2) if term_loan_lakhs > 0 else 1.0

    for i in range(5):
        rev = round(base_rev * ((1.22) ** i), 2)
        ebitda = round(rev * (0.24 + i * 0.01), 2)
        pat = round((ebitda - (capex_lakhs * 0.08) - (term_loan_lakhs * 0.08)) * 0.78, 2)
        dscr = round(ebitda / max(annual_debt_service, 0.5), 2)
        revenues_lakhs.append(rev)
        ebitda_lakhs.append(ebitda)
        pat_lakhs.append(pat)
        dscr_list.append(dscr)

    avg_dscr = round(sum(dscr_list) / len(dscr_list), 2)
    return {
        "district": district,
        "scheme": scheme or "Standard Commercial Term Loan",
        "total_capex_lakhs": capex_lakhs,
        "promoter_equity_lakhs": promoter_margin_lakhs,
        "govt_subsidy_lakhs": subsidy_lakhs,
        "bank_term_loan_lakhs": term_loan_lakhs,
        "annual_debt_service_lakhs": annual_debt_service,
        "years": years,
        "revenues_lakhs": revenues_lakhs,
        "ebitda_lakhs": ebitda_lakhs,
        "pat_lakhs": pat_lakhs,
        "dscr_series": dscr_list,
        "avg_dscr": avg_dscr,
        "bankability_verdict": "HIGHLY_BANKABLE (DSCR >= 1.50)" if avg_dscr >= 1.50 else "MARGINAL_DSCR"
    }
