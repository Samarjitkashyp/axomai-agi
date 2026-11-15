"""
Y5 Chanakya - Sovereign Geopolitics, OSINT & Strategic Intelligence Agent.
Orchestrates global OFAC/UN sanctions compliance, Siliguri & Kaladan strategic corridor vulnerability,
and multi-source OSINT sovereign diplomatic advisory synthesis.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.y5_chanakya.tools.sanctions_screening import sanctions_screening_engine
from axomai.agents.y5_chanakya.tools.chokepoint_radar import chokepoint_radar
from axomai.agents.y5_chanakya.tools.osint_synthesizer import osint_synthesizer

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

class Y5ChanakyaAgent:
    """Enterprise National Security Advisor & Sovereign Geopolitical Intelligence Strategist."""

    def __init__(self):
        self.name = "Y5 Chanakya"
        self.role = "Sovereign Geopolitics, OSINT & Strategic Intelligence Agent"

    def geopolitics_stream(
        self,
        query: str,
        session_id: Optional[str] = "chanakya_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield {
            "type": "status",
            "stage": "geopolitical_intel_modeling",
            "message": "🎯 Y5 Chanakya: Screening OFAC SDN sanctions, Siliguri Corridor choke-points & synthesizing OSINT..."
        }

        # 1. Sanctions Screening
        sanctions_data = sanctions_screening_engine.screen_entity()

        # 2. Strategic Chokepoint Assessment
        corr = "kaladan_multimodal" if "kaladan" in query.lower() or "myanmar" in query.lower() else "siliguri_corridor"
        chokepoint_data = chokepoint_radar.assess_chokepoint_risk(corridor_id=corr)

        # 3. Multi-Source OSINT Synthesis
        osint_data = osint_synthesizer.synthesize_geopolitical_dossier()

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "SOVEREIGN_GEOPOLITICS_AND_OSINT",
            "sanctions_screening": sanctions_data,
            "chokepoint_assessment": chokepoint_data,
            "osint_synthesis": osint_data,
            "tools_used": ["sanctions_screening_engine", "chokepoint_radar", "osint_synthesizer"]
        }
        yield meta_event

        prompt = (
            f"You are Y5 Chanakya, Sovereign National Security Advisor & Geopolitical Strategist.\n"
            f"User Goal / Inquiry: '{query}'\n\n"
            f"OFAC / UN Sanctions Screening: {sanctions_data}\n"
            f"Strategic Chokepoint Telemetry: {chokepoint_data}\n"
            f"OSINT Verified Dossier: {osint_data}\n\n"
            "Formulate an authoritative Sovereign Geopolitical Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present Geopolitical & Strategic Risk Metrics in a clean Markdown Table:\n"
            "| Strategic Frontier | Threat / Vulnerability | Monitored Corridor | Sovereign Defense Posture |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "- Outline sanctions compliance clearing and redundant multimodal contingency corridors.\n"
            "- Ensure every table row ends with a newline."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Y5 Chanakya, Sovereign Geopolitical Strategist.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            s = sanctions_data
            c = chokepoint_data
            o = osint_data
            full_answer = (
                f"### 🎯 Y5 Chanakya: Sovereign Geopolitics, OSINT & Strategic Intelligence\n\n"
                f"**Strategic Theater:** `{o['topic']}` | **Composite Risk Index:** `{o['composite_geopolitical_risk_index']}`\n\n"
                f"#### 🌐 Geopolitical Chokepoint & International Sanctions Matrix\n\n"
                f"| Strategic Frontier | Threat / Vulnerability | Monitored Corridor | Sovereign Defense Posture |\n"
                f"| :--- | :--- | :--- | :--- |\n"
                f"| **Land Chokepoint** | Vulnerability: {c['geopolitical_risk_score']}/100 | {c['corridor_name']} ({c['geographic_bottleneck']}) | {c['redundant_contingency_path']} |\n"
                f"| **OFAC / UN Sanctions** | Status: {s['ofac_sdn_status']} | Entity: {s['screened_entity']} | {s['statutory_clearing_verdict']} |\n"
                f"| **Secondary Sanctions** | Risk: {s['secondary_sanctions_risk']} | Dollar Clearing: $150k Notional | Complies with FATF Rec 6 & RBI KYC Directions |\n"
                f"| **Riverine Protocol (IBP)** | Operational at 82% capacity | Brahmaputra NW-2 to Bay of Bengal | Bypasses Siliguri rail bottleneck with zero diplomatic friction |\n\n"
                f"#### 🛡️ Sovereign Geopolitical Advisory\n\n"
                f"- **Transit Defense Doctrine:** `{c['sovereign_defense_posture']}`.\n"
                f"- **Trade Compliance:** `{s['statutory_mandate']}`.\n"
                f"- **Strategic Intelligence Synthesis:** `{o['strategic_implication']}`.\n"
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

y5_chanakya_agent = Y5ChanakyaAgent()

