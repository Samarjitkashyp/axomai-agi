"""
Y2 Urja - Green Energy, Carbon Credits & Smart Grid Agent.
Orchestrates rooftop solar/micro-hydro engineering feasibility, Levelized Cost of Energy (LCOE),
VCS/Verra carbon credit offset quantification, and open-access green PPA tariffs.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.y2_urja.tools.solar_hydro_feasibility import solar_hydro_engine
from axomai.agents.y2_urja.tools.carbon_credits import carbon_credits_engine
from axomai.agents.y2_urja.tools.ppa_grid_optimizer import ppa_grid_optimizer

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

class Y2UrjaAgent:
    """Enterprise Chief Energy Officer & Sovereign ESG Carbon Credit Strategist."""

    def __init__(self):
        self.name = "Y2 Urja"
        self.role = "Green Energy, Carbon Credits & Smart Grid Agent"

    def energy_stream(
        self,
        query: str,
        session_id: Optional[str] = "urja_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield {
            "type": "status",
            "stage": "green_energy_modeling",
            "message": "⚡ Y2 Urja: Computing solar/hydro LCOE, Verra VCS carbon offsets & Open Access PPA..."
        }

        # 1. Rooftop Solar Feasibility
        solar_data = solar_hydro_engine.evaluate_rooftop_solar_pv(roof_area_sqft=25000.0)

        # 2. Carbon Credit Quantification
        carbon_data = carbon_credits_engine.quantify_carbon_credits(
            clean_generation_kwh=solar_data["annual_generation_kwh"]
        )

        # 3. Open Access PPA Grid Optimization
        ppa_data = ppa_grid_optimizer.evaluate_green_open_access_ppa(
            monthly_consumption_kwh=120000.0, green_ppa_share_pct=70.0
        )

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "GREEN_ENERGY_AND_CARBON_OFFSET",
            "solar_feasibility": solar_data,
            "carbon_offset": carbon_data,
            "ppa_optimization": ppa_data,
            "tools_used": ["solar_hydro_engine", "carbon_credits_engine", "ppa_grid_optimizer"]
        }
        yield meta_event

        prompt = (
            f"You are Y2 Urja, Chief Energy Officer & Sovereign ESG Carbon Strategist.\n"
            f"User Goal / Inquiry: '{query}'\n\n"
            f"Rooftop Solar Yield & LCOE: {solar_data}\n"
            f"Carbon Credit Quantification: {carbon_data}\n"
            f"Open-Access PPA Optimization: {ppa_data}\n\n"
            "Formulate an authoritative, institutional-grade Green Energy & Carbon Credit Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present Energy Economics & Carbon Revenue in a clean Markdown Table:\n"
            "| Energy Parameter | Baseline Grid / Cost | Green Transition Value | Variance / Net Savings | Strategic Implication |\n"
            "| :--- | :--- | :--- | :--- | :--- |\n"
            "- Outline Verra VCS registration and PPA open access tariff structure.\n"
            "- Ensure every table row ends with a newline."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Y2 Urja, Sovereign Green Energy Strategist.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            s = solar_data
            c = carbon_data
            p = ppa_data
            full_answer = (
                f"### ⚡ Y2 Urja: Green Energy, Carbon Credits & Smart Grid Intelligence\n\n"
                f"**Asset Profile:** `{s['installation_type']}` | **Capacity:** `{s['installed_capacity_kwp']} kWp`\n\n"
                f"#### 📊 Green Energy Economics & Carbon Offsets Matrix\n\n"
                f"| Energy Parameter | Baseline Grid / Cost | Green Transition Value | Variance / Net Savings | Strategic Implication |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
                f"| **Electricity Tariff** | ₹{s['grid_tariff_inr_kwh']}/kWh (Discom) | ₹{s['levelized_cost_of_energy_lcoe_inr_kwh']}/kWh (LCOE) | -₹{s['grid_tariff_inr_kwh'] - s['levelized_cost_of_energy_lcoe_inr_kwh']:.2f}/kWh | Solar power eliminates grid premium |\n"
                f"| **Annual Energy Bill** | ₹{p['baseline_annual_bill_inr']:,.2f} | ₹{p['optimized_annual_bill_inr']:,.2f} | Saves: ₹{p['annual_cost_savings_inr']:,.2f} ({p['savings_percentage']}) | 70% Green Open-Access PPA integration |\n"
                f"| **Carbon Offset (VCS)** | 0 tCO2e Grid Average | {c['annual_carbon_credits_generated_tco2e']} tCO2e/yr | Revenue: ₹{c['annual_carbon_revenue_inr']:,.2f}/yr | Verified Carbon Standard (Verra) monetization |\n"
                f"| **Capital Amortization** | Initial: ₹{s['total_capex_inr']:,.2f} | Simple Payback: {s['simple_payback_years']} Years | 25-Year Plant Life | Asset provides 21 years of near-free clean power |\n\n"
                f"#### 🌿 Regulatory Framework & ESG Monetization\n\n"
                f"- **Green Open Access Qualification:** Project qualifies under the Ministry of Power 100 kW threshold.\n"
                f"- **Carbon Monetization:** `{c['monetization_route']}`.\n"
                f"- **ToD Peak Optimization:** `{p['peak_shifting_recommendation']}`.\n"
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

y2_urja_agent = Y2UrjaAgent()

