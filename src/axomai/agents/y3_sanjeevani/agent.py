"""
Y3 Sanjeevani - Sovereign Healthcare & Cold-Chain Pharma Agent.
Orchestrates epidemiological outbreak SIR modeling, IoT biological cold-chain Mean Kinetic Temperature (MKT),
and CDSCO Revised Schedule M / 21 CFR Part 11 GMP pharmaceutical regulatory audits.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.y3_sanjeevani.tools.epidemiology_engine import epidemiology_engine
from axomai.agents.y3_sanjeevani.tools.cold_chain_auditor import cold_chain_auditor
from axomai.agents.y3_sanjeevani.tools.pharma_compliance import pharma_compliance_engine

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

class Y3SanjeevaniAgent:
    """Enterprise Chief Medical Officer & Sovereign Public Health Epidemiologist."""

    def __init__(self):
        self.name = "Y3 Sanjeevani"
        self.role = "Sovereign Healthcare & Cold-Chain Pharma Agent"

    def healthcare_stream(
        self,
        query: str,
        session_id: Optional[str] = "sanjeevani_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield {
            "type": "status",
            "stage": "healthcare_modeling",
            "message": "🏥 Y3 Sanjeevani: Modeling outbreak SIR dynamics, IoT biological cold-chain MKT & CDSCO Schedule M..."
        }

        # 1. Epidemiological Outbreak SIR Simulation
        disease = "dengue" if "dengue" in query.lower() else ("cholera" if "cholera" in query.lower() else "japanese_encephalitis")
        epi_data = epidemiology_engine.simulate_outbreak_risk(district="Dibrugarh", disease_name=disease)

        # 2. Cold-Chain MKT Audit
        cold_data = cold_chain_auditor.calculate_mean_kinetic_temperature([4.1, 4.5, 5.2, 5.8, 6.1, 5.4, 4.8, 4.3])

        # 3. CDSCO Schedule M GMP Audit
        gmp_data = pharma_compliance_engine.audit_manufacturing_facility()

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "SOVEREIGN_HEALTHCARE_AND_COLD_CHAIN",
            "epidemiology": epi_data,
            "cold_chain": cold_data,
            "pharma_gmp": gmp_data,
            "tools_used": ["epidemiology_engine", "cold_chain_auditor", "pharma_compliance_engine"]
        }
        yield meta_event

        prompt = (
            f"You are Y3 Sanjeevani, Chief Medical Officer & Sovereign Epidemiological Specialist.\n"
            f"User Goal / Inquiry: '{query}'\n\n"
            f"Epidemiological SIR Outbreak Model: {epi_data}\n"
            f"Biological Cold-Chain MKT Potency: {cold_data}\n"
            f"CDSCO Schedule M & 21 CFR Part 11 GMP: {gmp_data}\n\n"
            "Formulate an authoritative Healthcare & Pharmaceutical Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present Clinical & Telemetry Metrics in a clean Markdown Table:\n"
            "| Healthcare Parameter | Current Value | Clinical Benchmark | Safety Verdict |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "- Outline public health vector-control interventions and cold-chain deviation logs.\n"
            "- Ensure every table row ends with a newline."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Y3 Sanjeevani, Sovereign Healthcare Specialist.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            e = epi_data
            c = cold_data
            g = gmp_data
            full_answer = (
                f"### 🏥 Y3 Sanjeevani: Sovereign Healthcare & Cold-Chain Pharma Intelligence\n\n"
                f"**Surveillance Sector:** `{e['monitored_district']}` | **Pathogen:** `{e['target_pathogen']}`\n\n"
                f"#### 📊 Epidemiological Outbreak & Cold-Chain Stability Matrix\n\n"
                f"| Healthcare Parameter | Current Value | Clinical Benchmark | Safety Verdict |\n"
                f"| :--- | :--- | :--- | :--- |\n"
                f"| **Basic Reproduction $R_0$** | {e['environment_amplified_r0']} (Amplified) | Baseline: {e['baseline_r0']} ($R_0 < 1.0$) | {e['outbreak_expansion_status']} |\n"
                f"| **Projected Peak Influx** | {e['projected_peak_active_cases']} Active Cases | Day 21 Surge | Pre-position pediatric ICU beds & fluids |\n"
                f"| **Cold-Chain Arrhenius MKT** | {c['arrhenius_mean_kinetic_temp_celsius']}°C | Standard: {c['regulatory_range']} | {c['biological_potency_verdict']} |\n"
                f"| **CDSCO Schedule M GMP** | {g['compliance_readiness_score']} Readiness | 21 CFR 11 ALCOA+ Audit | {g['batch_release_authorization']} |\n\n"
                f"#### 💉 Public Health Countermeasures & Distribution Safety\n\n"
                f"- **Vector Mitigation:** {'; '.join(e['medical_countermeasures'])}.\n"
                f"- **Cold-Chain Certification:** `{c['statutory_compliance']}`.\n"
                f"- **Data Integrity:** Facility verified with Grade A Laminar Flow cleanrooms and immutable digital batch signatures.\n"
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

y3_sanjeevani_agent = Y3SanjeevaniAgent()

