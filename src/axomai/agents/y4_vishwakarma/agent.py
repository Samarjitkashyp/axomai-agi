"""
Y4 Vishwakarma - Mega Infrastructure, EPC & Civil Digital Twin Agent.
Orchestrates Primavera 4D Earned Value Management (SPI/CPI), contractual Liquidated Damages,
FIDIC Clause 8.4 / 20.1 engineering dispute arbitration, and Zone-V seismic slope stability.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.y4_vishwakarma.tools.primavera_delay_engine import primavera_delay_engine
from axomai.agents.y4_vishwakarma.tools.fidic_contract_auditor import fidic_contract_auditor
from axomai.agents.y4_vishwakarma.tools.seismic_embankment_safety import seismic_embankment_engine

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

class Y4VishwakarmaAgent:
    """Enterprise Chief Infrastructure Officer & Sovereign EPC Civil Engineering Specialist."""

    def __init__(self):
        self.name = "Y4 Vishwakarma"
        self.role = "Mega Infrastructure, EPC & Civil Digital Twin Agent"

    def infra_stream(
        self,
        query: str,
        session_id: Optional[str] = "vishwakarma_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield {
            "type": "status",
            "stage": "civil_infra_modeling",
            "message": "🏗️ Y4 Vishwakarma: Analyzing Primavera 4D EVM delay, FIDIC Clause 8.4 EoT & Zone-V seismic slope..."
        }

        # 1. Primavera 4D EVM Schedule Delay
        evm_data = primavera_delay_engine.evaluate_epc_schedule_evm()

        # 2. FIDIC Engineering Dispute Claim Audit
        fidic_data = fidic_contract_auditor.audit_contractor_claim()

        # 3. Seismic Zone-V Slope Stability
        seismic_data = seismic_embankment_engine.evaluate_embankment_stability()

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "MEGA_INFRASTRUCTURE_AND_EPC_CIVIL",
            "evm_schedule_delay": evm_data,
            "fidic_contract_audit": fidic_data,
            "seismic_slope_safety": seismic_data,
            "tools_used": ["primavera_delay_engine", "fidic_contract_auditor", "seismic_embankment_engine"]
        }
        yield meta_event

        prompt = (
            f"You are Y4 Vishwakarma, Chief Infrastructure Officer & Sovereign Civil Engineering Strategist.\n"
            f"User Goal / Inquiry: '{query}'\n\n"
            f"Primavera 4D EVM Schedule Performance: {evm_data}\n"
            f"FIDIC Contract Claim Admissibility: {fidic_data}\n"
            f"IS 1893:2016 Zone-V Seismic Stability: {seismic_data}\n\n"
            "Formulate an authoritative Mega Infrastructure & EPC Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present Engineering & Contractual Metrics in a clean Markdown Table:\n"
            "| Project Engineering Parameter | Monitored Metric | Target Milestone | Legal / Structural Consequence |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "- Outline critical path schedule recovery and seismic slope reinforcement.\n"
            "- Ensure every table row ends with a newline."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Y4 Vishwakarma, Sovereign EPC Civil Engineer.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            p = evm_data
            f = fidic_data
            s = seismic_data
            full_answer = (
                f"### 🏗️ Y4 Vishwakarma: Mega Infrastructure, EPC & Civil Digital Twin\n\n"
                f"**Project Target:** `{p['project_name']}` | **Budget at Completion:** `{p['budget_at_completion_bac_cr']}`\n\n"
                f"#### 📊 Earned Value Schedule, FIDIC Claims & Seismic Safety Matrix\n\n"
                f"| Project Engineering Parameter | Monitored Metric | Target Milestone | Legal / Structural Consequence |\n"
                f"| :--- | :--- | :--- | :--- |\n"
                f"| **Schedule Performance (SPI)** | {p['schedule_performance_index_spi']} ({p['schedule_variance_sv_cr']}) | SPI $\\ge 1.00$ | Delayed +{p['projected_completion_duration_months']} |\n"
                f"| **Cost Performance (CPI)** | {p['cost_performance_index_cpi']} ({p['cost_variance_cv_cr']}) | CPI $\\ge 1.00$ | Estimate at Completion: {p['estimate_at_completion_eac_cr']} |\n"
                f"| **Contractual Delay Penalties** | {p['liquidated_damages_exposure_cr']} | Enforceable under Clause 8.7 | Liquidated damages exposure capped at 10% |\n"
                f"| **FIDIC Claim Admissibility** | {f['statutory_time_bar_status']} | 28-Day Bar Rule (Clause 20.1) | {int(f['dab_adjudication_success_probability']*100)}% DAB Settlement Probability; Rec: {f['recommended_settlement_eot_days']} Days EoT |\n"
                f"| **Zone-V Seismic Factor of Safety** | FoS: {s['seismic_zone_v_factor_of_safety']} (Seismic) | Threshold: {s['statutory_safety_threshold']} | {s['structural_integrity_verdict']} |\n\n"
                f"#### 🌉 Civil Engineering Remediation & Risk Mitigation\n\n"
                f"- **EoT Claim Protocol:** `{p['critical_path_action']}`.\n"
                f"- **Commercial Dispute Strategy:** `{f['legal_engineering_verdict']}`.\n"
                f"- **Seismic Slope Armor:** `{s['engineering_recommendation']}`.\n"
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

y4_vishwakarma_agent = Y4VishwakarmaAgent()

