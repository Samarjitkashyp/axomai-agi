"""
Y1 Annapurna - Sovereign Agri-Science & Commodity Futures Agent.
Orchestrates micro-climate IMD radar forecasts, precision soil NPK chemistry,
and MCX / NCDEX agricultural commodity futures pricing and hedging.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.y1_annapurna.tools.weather_microclimate import weather_microclimate_engine
from axomai.agents.y1_annapurna.tools.soil_chemistry import soil_chemistry_engine
from axomai.agents.y1_annapurna.tools.commodity_futures import commodity_futures_engine

def normalize_markdown(text: str) -> str:
    """Ensures headings, tables, and lists always have clean double newlines."""
    text = re.sub(r'^[ \t]+(#{1,4}\s+)', r'\1', text, flags=re.MULTILINE)
    text = re.sub(r'\n[ \t]+(#{1,4}\s+)', r'\n\n\1', text)
    text = re.sub(r'([^\n])\s*(#{1,4}\s+)', r'\1\n\n\2', text)
    text = re.sub(r'^([^|\n]+)[ \t]*(\|.+)$', r'\1\n\n\2', text, flags=re.MULTILINE)
    text = re.sub(r'\|\s*\|', '|\n|', text)
    text = re.sub(r'([^\n])\s*(\n?-\s+\*\*)', r'\1\n\n- **', text)
    text = re.sub(r'([^\n])\s*(\n?-\s+)', r'\1\n- ', text)
    return text

class Y1AnnapurnaAgent:
    """Enterprise Chief Agronomist & Sovereign Commodity Trading Strategist."""

    def __init__(self):
        self.name = "Y1 Annapurna"
        self.role = "Sovereign Agri-Science & Commodity Futures Agent"

    def agri_stream(
        self,
        query: str,
        session_id: Optional[str] = "annapurna_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield {
            "type": "status",
            "stage": "agri_science_modeling",
            "message": "🌾 Y1 Annapurna: Modeling micro-climate radar, precision soil NPK deficits & MCX futures basis..."
        }

        # 1. Micro-Climate Weather Forecast
        dist = "dibrugarh" if "dibrugarh" in query.lower() else ("jorhat" if "jorhat" in query.lower() else "kamrup")
        weather_data = weather_microclimate_engine.forecast_agronomic_weather(district=dist, forecast_horizon_days=7)

        # 2. Precision Soil Chemistry
        crop = "paddy_rice" if "rice" in query.lower() or "paddy" in query.lower() else "tea"
        soil_data = soil_chemistry_engine.prescribe_soil_nutrition(crop_type=crop, soil_ph=4.3)

        # 3. Commodity Futures & Basis
        comm_name = "joha_rice" if crop == "paddy_rice" else "assam_orthodox_tea"
        futures_data = commodity_futures_engine.price_commodity_futures(commodity_name=comm_name, tenor_months=3)

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "SOVEREIGN_AGRI_SCIENCE_AND_FUTURES",
            "weather_forecast": weather_data,
            "soil_chemistry": soil_data,
            "commodity_futures": futures_data,
            "tools_used": ["weather_microclimate_engine", "soil_chemistry_engine", "commodity_futures_engine"]
        }
        yield meta_event

        prompt = (
            f"You are Y1 Annapurna, Chief Agronomist & Sovereign Agri-Commodity Derivatives Strategist.\n"
            f"User Goal / Inquiry: '{query}'\n\n"
            f"IMD Doppler Micro-Climate: {weather_data}\n"
            f"Soil NPK & Fertilizer Prescription: {soil_data}\n"
            f"MCX / NCDEX Commodity Futures Pricing: {futures_data}\n\n"
            "Formulate an authoritative, institutional-grade Agri-Science & Commodity Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present Agronomic & Financial Metrics in a clean Markdown Table:\n"
            "| Agro-Financial Dimension | Current Parameter | Targeted Threshold | Strategic Recommendation |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "- Outline soil NPK amendment protocols and MCX futures hedging ratios.\n"
            "- Ensure every table row ends with a newline."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Y1 Annapurna, Sovereign Agri-Science Strategist.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            w = weather_data
            s = soil_data
            f = futures_data
            full_answer = (
                f"### 🌾 Y1 Annapurna: Sovereign Agri-Science & Commodity Futures Intelligence\n\n"
                f"**Agro-Climatic Zone:** `{w['target_district']} Valley` | **Crop Focus:** `{s['crop']}`\n\n"
                f"#### 📊 Agronomic Soil, Weather & MCX Futures Matrix\n\n"
                f"| Agro-Financial Dimension | Current Parameter | Targeted Threshold | Strategic Recommendation |\n"
                f"| :--- | :--- | :--- | :--- |\n"
                f"| **Micro-Climate QPF** | {w['projected_cumulative_rainfall_mm']} mm (7-Day) | Doppler: {w['doppler_radar_reflectivity_dbz']} dBZ | {w['crop_spray_suitability']} |\n"
                f"| **Soil pH & Acidity** | pH {s['soil_ph']} ({s['ph_status']}) | Optimal: 4.5 – 5.5 | {s['ph_remediation']} |\n"
                f"| **Soil Nutrition (NPK)** | Deficit: {s['nutrient_deficits_kg_ha']['nitrogen_n']}kg N / {s['nutrient_deficits_kg_ha']['phosphorus_p']}kg P | Target 140N / 45P / 120K | Apply {s['fertilizer_prescriptions_kg_ha']['commercial_urea_46n']}kg Urea + {s['fertilizer_prescriptions_kg_ha']['single_super_phosphate_16p']}kg SSP/ha |\n"
                f"| **MCX Futures (3-Month)** | ₹{f['theoretical_futures_price_inr_per_kg']}/kg | Spot: ₹{f['spot_price_inr_per_kg']}/kg | {f['market_curve_structure']}; Hedge Ratio $\\beta={f['optimal_hedge_ratio_beta']}$ |\n\n"
                f"#### 🌾 Agronomic Advisory & Risk Mitigation\n\n"
                f"- **Yield Lift Potential:** `{s['yield_enhancement_potential']}` via split-dose nitrogen scheduling.\n"
                f"- **Hedging Execution:** `{f['hedging_verdict']}`.\n"
                f"- **Drainage & Flood Safeguard:** `{w['agronomic_action']}`.\n"
            )
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        cleaned = normalize_markdown(full_answer)
        yield {
            "type": "final",
            "content": cleaned,
            "agent": self.name,
            "role": self.role
        }

y1_annapurna_agent = Y1AnnapurnaAgent()

