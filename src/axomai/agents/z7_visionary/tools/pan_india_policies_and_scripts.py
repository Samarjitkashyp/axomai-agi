"""
Z7 Visionary - Pan-India State Industrial Policy, Discom Tariff & 12-Language Script Engine.
Covers major Indian industrial hubs (Maharashtra, Gujarat, Karnataka, Tamil Nadu,
Uttar Pradesh, Telangana, Odisha, Rajasthan, Delhi-NCR, Assam/NE) with real Discom
commercial/industrial power tariffs, state capital subsidy schemes (PSI, SIPCOT, PLI, UNNATI),
and 12+ Scheduled Indian Languages multi-script presentation headers.
"""

from typing import Dict, Any, Optional


PAN_INDIA_STATES = {
    "maharashtra": {"city": "Mumbai / Pune", "scheme": "Maharashtra PSI (Package Scheme of Incentives)", "subsidy_pct": 30.0, "discom": "MSEDCL", "tariff_kwh": 9.20, "lease_sqft": 55.0},
    "gujarat": {"city": "Ahmedabad / Surat / GIFT City", "scheme": "Gujarat Industrial & IT/ITeS Policy", "subsidy_pct": 25.0, "discom": "DGVCL / UGVCL", "tariff_kwh": 7.80, "lease_sqft": 42.0},
    "karnataka": {"city": "Bengaluru / Mysuru", "scheme": "Karnataka EV, Aerospace & Industrial Policy", "subsidy_pct": 25.0, "discom": "BESCOM", "tariff_kwh": 8.65, "lease_sqft": 62.0},
    "tamil nadu": {"city": "Chennai / Coimbatore", "scheme": "Tamil Nadu SIPCOT Industrial Subsidy", "subsidy_pct": 25.0, "discom": "TANGEDCO", "tariff_kwh": 8.10, "lease_sqft": 45.0},
    "uttar pradesh": {"city": "Noida / Lucknow / Kanpur", "scheme": "UP Industrial Investment & Employment Promotion Policy", "subsidy_pct": 30.0, "discom": "PVVNL / UPPCL", "tariff_kwh": 8.30, "lease_sqft": 38.0},
    "telangana": {"city": "Hyderabad", "scheme": "Telangana T-IDEA / T-PRIDE Industrial Incentive", "subsidy_pct": 25.0, "discom": "TSSPDCL", "tariff_kwh": 8.40, "lease_sqft": 48.0},
    "odisha": {"city": "Bhubaneswar / Rourkela", "scheme": "Odisha Industrial Policy Resolution (IPR)", "subsidy_pct": 30.0, "discom": "TPCODL", "tariff_kwh": 6.90, "lease_sqft": 24.0},
    "delhi": {"city": "Delhi-NCR", "scheme": "Central PLI / MSME Credit Linked Capital Subsidy", "subsidy_pct": 20.0, "discom": "TPDDL / BSES", "tariff_kwh": 9.50, "lease_sqft": 70.0},
    "assam": {"city": "Guwahati / Jorhat", "scheme": "UNNATI 2024 / CMAAA Assam", "subsidy_pct": 35.0, "discom": "APDCL", "tariff_kwh": 7.15, "lease_sqft": 18.0}
}

CITY_TO_STATE = {
    "mumbai": "maharashtra", "pune": "maharashtra", "nagpur": "maharashtra",
    "ahmedabad": "gujarat", "surat": "gujarat", "gift city": "gujarat", "vadodara": "gujarat",
    "bengaluru": "karnataka", "bangalore": "karnataka", "mysuru": "karnataka",
    "chennai": "tamil nadu", "coimbatore": "tamil nadu",
    "noida": "uttar pradesh", "lucknow": "uttar pradesh", "kanpur": "uttar pradesh",
    "hyderabad": "telangana",
    "bhubaneswar": "odisha",
    "delhi": "delhi", "new delhi": "delhi", "gurugram": "delhi",
    "guwahati": "assam", "jorhat": "assam", "dibrugarh": "assam", "silchar": "assam"
}

INDIAN_12_SCRIPTS = {
    "hindi": {"script": "Hindi (हिन्दी)", "dpr_header": "विस्तृत परियोजना रिपोर्ट (Bankable DPR)", "summary": "कार्यकारी सारांश"},
    "marathi": {"script": "Marathi (मराठी)", "dpr_header": "सविस्तर प्रकल्प अहवाल (Bankable DPR)", "summary": "कार्यकारी सारांश"},
    "gujarati": {"script": "Gujarati (ગુજરાતી)", "dpr_header": "વિગતવાર પ્રોજેક્ટ રિપોર્ટ (Bankable DPR)", "summary": "કાર્યકારી સારાંશ"},
    "tamil": {"script": "Tamil (தமிழ்)", "dpr_header": "விரிவான திட்ட அறிக்கை (Bankable DPR)", "summary": "செயல் சுருக்கம்"},
    "telugu": {"script": "Telugu (తెలుగు)", "dpr_header": "వివరణాత్మక ప్రాజెక్ట్ నివేదిక (Bankable DPR)", "summary": "కార్యనిర్వాహక సారాంశం"},
    "kannada": {"script": "Kannada (ಕನ್ನಡ)", "dpr_header": "ವಿವರವಾದ ಯೋಜನಾ ವರದಿ (Bankable DPR)", "summary": "ಕಾರ್ಯನಿರ್ವಾಹಕ ಸಾರಾಂಶ"},
    "punjabi": {"script": "Punjabi (ਪੰਜਾਬੀ)", "dpr_header": "ਵਿਸਤ੍ਰਿਤ ਪ੍ਰੋਜੈਕਟ ਰਿਪੋਰਟ (Bankable DPR)", "summary": "ਕਾਰਜਕਾਰੀ ਸਾਰ"},
    "odia": {"script": "Odia (ଓଡ଼ିଆ)", "dpr_header": "ବିସ୍ତୃତ ପ୍ରକଳ୍ପ ରିପୋର୍ଟ (Bankable DPR)", "summary": "କାର୍ଯ୍ୟନିର୍ବାହୀ ସାରାଂଶ"},
    "assamese": {"script": "Assamese (অসমীয়া)", "dpr_header": "বিস্তৃত প্ৰকল্প প্ৰতিবেদন (Bankable DPR)", "summary": "কাৰ্যবাহী সাৰাংশ"},
    "bengali": {"script": "Bengali (বাংলা)", "dpr_header": "বিস্তারিত প্রকল্প প্রতিবেদন (Bankable DPR)", "summary": "নির্বাহী সারসংক্ষেপ"},
    "bodo": {"script": "Bodo (बड़ो)", "dpr_header": "गुवार बिथांखि फोरमायथि (Bankable DPR)", "summary": "गाहाय सुंद' मोनसे"},
    "english": {"script": "English", "dpr_header": "Detailed Project Report (Bankable DPR)", "summary": "Executive Summary"}
}


def resolve_pan_india_policy(query: str, language_script: str = "english") -> Dict[str, Any]:
    """Resolves state policy, Discom power tariff, and multi-script labels across all of India."""
    q_lower = query.lower()
    detected_state = None

    for st in PAN_INDIA_STATES:
        if st in q_lower:
            detected_state = st
            break
    if not detected_state:
        for city, st in CITY_TO_STATE.items():
            if city in q_lower:
                detected_state = st
                break

    is_pan_india = detected_state is not None and detected_state != "assam"
    st_key = detected_state or "assam"
    st_data = PAN_INDIA_STATES[st_key]

    # Check if PLI explicitly requested
    scheme_override = st_data["scheme"]
    subsidy_pct = st_data["subsidy_pct"]
    if "pli" in q_lower:
        scheme_override = "Central Production Linked Incentive (PLI) Scheme"
        subsidy_pct = 25.0

    # Detect Pan-India language script
    lang_key = language_script
    for k in INDIAN_12_SCRIPTS:
        if k in q_lower:
            lang_key = k
            break

    return {
        "state": st_key.title(),
        "is_pan_india_non_assam": is_pan_india,
        "industrial_hub": st_data["city"],
        "applicable_state_scheme": scheme_override,
        "state_subsidy_pct": subsidy_pct,
        "discom_utility": st_data["discom"],
        "power_tariff_inr_kwh": st_data["tariff_kwh"],
        "industrial_lease_sqft_inr": st_data["lease_sqft"],
        "language_script": lang_key,
        "script_labels": INDIAN_12_SCRIPTS.get(lang_key, INDIAN_12_SCRIPTS["english"])
    }
