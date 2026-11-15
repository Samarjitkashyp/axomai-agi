"""
Z14 Horizon - Global Cross-Border Trade & FX Intelligence Agent.
Orchestrates multi-currency exchange risk, Garman-Kohlhagen FX options & Zero-Cost Collars,
HS Code customs duties, UCP 600 Letter of Credit audits, EU CBAM carbon tariffs, and freight demurrage.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.z14_horizon.tools.fx_engine import fx_engine
from axomai.agents.z14_horizon.tools.customs_tariff_engine import customs_tariff_engine
from axomai.agents.z14_horizon.tools.fx_options import fx_options_engine
from axomai.agents.z14_horizon.tools.swift_lc_auditor import swift_lc_auditor
from axomai.agents.z14_horizon.tools.cbam_engine import cbam_engine
from axomai.agents.z14_horizon.tools.freight_demurrage_engine import freight_demurrage_engine

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

class Z14HorizonAgent:
    """Enterprise Chief International Trade Officer & Global FX Strategist."""

    def __init__(self):
        self.name = "Z14 Horizon"
        self.role = "Global Cross-Border Trade & FX Intelligence Agent"

    def trade_stream(
        self,
        query: str,
        session_id: Optional[str] = "horizon_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield {
            "type": "status",
            "stage": "global_trade_modeling",
            "message": "🌐 Z14 Horizon: Computing FX forward/options collars, UCP 600 LC audit, CBAM carbon tax & freight..."
        }

        # 1. Spot and Forward hedge calculations
        fx_conv = fx_engine.convert_currency(100000.0, from_curr="USD", to_curr="INR")
        fx_hedge = fx_engine.compute_forward_hedge(100000.0, base_currency="USD", quote_currency="INR", tenor_months=6)

        # 2. Advanced Garman-Kohlhagen Zero-Cost Collar
        collar = fx_options_engine.calculate_zero_cost_collar(
            spot=fx_conv["effective_exchange_rate"], notional=100000.0, tenor_months=6, pair="USDINR"
        )

        # 3. Customs tariff & landed cost
        customs_data = customs_tariff_engine.calculate_landed_import_cost(
            cif_value_inr=fx_conv["converted_amount"], hs_code="8471", trade_partner="United States"
        )

        # 4. SWIFT MT700 / UCP 600 Compliance Sample Audit
        lc_audit = swift_lc_auditor.audit_lc_presentation(
            lc_terms={
                "31D_expiry_date": "2026-12-31",
                "44C_latest_shipment": "2026-11-30",
                "45A_goods_description": "Assam Orthodox Black Tea Grade TGFOP",
                "32B_amount": 100000.0,
                "39A_tolerance_pct": 5.0,
                "44A_loading_port": "Kolkata Port"
            },
            commercial_invoice={
                "goods_description": "Assam Orthodox Black Tea Grade TGFOP",
                "total_amount": 102500.0
            },
            bill_of_lading={
                "shipped_on_board_date": "2026-11-20",
                "loading_port": "Kolkata Port"
            }
        )

        # 5. EU CBAM & Freight Demurrage
        cbam_data = cbam_engine.calculate_cbam_liability(
            sector="tea_agri", shipment_weight_metric_tons=25.0
        )
        freight_data = freight_demurrage_engine.calculate_multimodal_shipping(
            route="kolkata_to_rotterdam", cargo_weight_kg=25000.0, cargo_volume_cbm=65.0, container_count_40ft=2
        )

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "GLOBAL_CROSS_BORDER_TRADE_AND_FX",
            "notional_usd": 100000.0,
            "fx_conversion": fx_conv,
            "forward_hedge": fx_hedge,
            "zero_cost_collar": collar,
            "customs_landed_cost": customs_data,
            "swift_lc_audit": lc_audit,
            "cbam_liability": cbam_data,
            "freight_economics": freight_data,
            "tools_used": [
                "fx_engine", "customs_tariff_engine", "fx_options_engine",
                "swift_lc_auditor", "cbam_engine", "freight_demurrage_engine"
            ]
        }
        yield meta_event

        prompt = (
            f"You are Z14 Horizon, Chief International Trade Officer & FX Risk Strategist.\n"
            f"User Goal / Inquiry: '{query}'\n\n"
            f"FX Forward Hedge: {fx_hedge}\n"
            f"Garman-Kohlhagen Zero-Cost Collar: {collar}\n"
            f"SWIFT MT700 / UCP 600 LC Audit: {lc_audit}\n"
            f"EU CBAM Carbon Tax Liability: {cbam_data}\n"
            f"Ocean vs Air Freight: {freight_data}\n\n"
            "Formulate an authoritative, institutional-grade Global Trade & FX Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present Currency Hedging & Options Collar in a clean Markdown Table:\n"
            "| Trade Parameter | Baseline Spot | 6-Month Forward Lock | Zero-Cost Collar Range | Strategic Implication |\n"
            "| :--- | :--- | :--- | :--- | :--- |\n"
            "- Include UCP 600 trade finance compliance and EU CBAM carbon tariff liabilities.\n"
            "- Ensure every table row ends with a newline."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z14 Horizon, Global Trade Strategist.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = (
                f"### 🌐 Z14 Horizon: Global Cross-Border Trade & FX Intelligence\n\n"
                f"**Trade Notional Base:** `$100,000 USD` | **Spot Rate:** `₹{fx_hedge['spot_rate']}/USD`\n\n"
                f"#### 💱 Foreign Exchange Hedging & Garman-Kohlhagen Options Matrix\n\n"
                f"| Trade Parameter | Baseline Spot | 6-Month Forward Lock | Zero-Cost Collar Range | Strategic Implication |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
                f"| **USD / INR Rate** | ₹{fx_hedge['spot_rate']:.2f} | ₹{fx_hedge['forward_rate']:.2f} | Floor: ₹{collar['put_floor_strike']} / Cap: ₹{collar['call_cap_strike']} | Collar completely eliminates net premium cost |\n"
                f"| **Hedged Total (INR)** | ₹{fx_hedge['unhedged_spot_total']:,.2f} | ₹{fx_hedge['hedged_total_quote']:,.2f} | ₹{collar['hedged_value_floor_inr']:,.2f} - ₹{collar['hedged_value_cap_inr']:,.2f} | Downside floor locked at ₹{collar['put_floor_strike']}/$ |\n"
                f"| **Customs Tariff (HS 8471)** | BCD 0% (ITA-1) | Effective: {customs_data['effective_tariff_rate_pct']}% | IGST 18% | Duty-free IT hardware import scheme |\n\n"
                f"#### 📜 UCP 600 Letter of Credit & Regulatory Compliance\n\n"
                f"- **SWIFT MT700 Audit Status:** `{lc_audit['status']}` (Compliance Score: `{lc_audit['compliance_score']}/100`).\n"
                f"- **Bank Negotiation Acceptance Probability:** `{int(lc_audit['bank_acceptance_probability']*100)}%`.\n"
                f"- **EU CBAM Carbon Border Tax:** Embedded emissions `{cbam_data['total_embedded_emissions_tco2e']} tCO2e` with net EU tariff liability of `€{cbam_data['net_cbam_liability_eur']:,.2f}` (`₹{cbam_data['net_cbam_liability_inr']:,.2f}`).\n"
                f"- **Multimodal Shipping:** Ocean freight for 2x40ft containers is `₹{freight_data['ocean_freight']['total_cost_inr']:,.2f}` (Transit: `{freight_data['ocean_freight']['transit_time_days']}`).\n"
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

z14_horizon_agent = Z14HorizonAgent()
