"""
Z11 Pragati - Assam Governance, Policy & MSME Scheme Agent.
Delivers authoritative guidance on Assam state policies, capital subsidies,
Mission Basundhara land governance, and government procurement rules.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.z11_pragati.tools.scheme_matcher import scheme_matcher

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

class Z11PragatiAgent:
    """Enterprise Chief Public Policy Officer & Assam State Governance Specialist."""

    def __init__(self):
        self.name = "Z11 Pragati"
        self.role = "Assam Governance, Policy & MSME Scheme Agent"

    def policy_stream(
        self,
        query: str,
        session_id: Optional[str] = "pragati_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield {
            "type": "status",
            "stage": "policy_matching",
            "message": "🏛️ Z11 Pragati: Matching venture profile with Assam State Subsidies & Mission Basundhara guidelines..."
        }

        matched = scheme_matcher.match_schemes(query)

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "ASSAM_POLICY_AND_SCHEMES",
            "matched_schemes_count": len(matched),
            "top_scheme": matched[0]["scheme_name"] if matched else "CMAAA",
            "schemes": matched,
            "tools_used": ["scheme_matcher"]
        }
        yield meta_event

        prompt = (
            f"You are Z11 Pragati, Chief Advisor on Assam State Policy & MSME Industrial Subsidies.\n"
            f"User Goal: '{query}'\n\n"
            f"Matched Assam Government Schemes & Land Frameworks:\n{str(matched)}\n\n"
            "Formulate an authoritative, official-grade State Policy & Incentives Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present Scheme Comparison as a clean GitHub Markdown Table with blank lines before and after:\n"
            "| Scheme Name | Department | Financial Benefit | Eligibility Criteria | Portal |\n"
            "| :--- | :--- | :--- | :--- | :--- |\n"
            "- Outline procedural step-by-step guidance for applying via Single Window Clearance / Ease of Doing Business Assam.\n"
            "- Ensure every table row ends with a newline."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z11 Pragati, Assam Policy Specialist.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = (
                f"### 🏛️ Z11 Pragati: Assam Policy & MSME Subsidies Dossier\n\n"
                f"**Jurisdiction:** Government of Assam • Department of Industries & Commerce\n\n"
                f"#### 📜 Matched State Schemes & Industrial Incentives\n\n"
                f"| Scheme Name | Department | Financial Benefit | Eligibility Criteria | Portal |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
            )
            for s in matched:
                full_answer += (
                    f"| **{s['scheme_name']}** | {s['department']} | {s['financial_benefit']} | "
                    f"{s['eligibility']} | `{s['application_portal']}` |\n"
                )
            full_answer += (
                f"\n#### 📑 Procedural Application Protocol:\n\n"
                f"1. **Single Window Clearance (Ease of Doing Business):** Register on `easeofdoingbusiness.assam.gov.in` to obtain composite commercial business clearance.\n"
                f"2. **Mission Basundhara Land Clearance:** Verify periodic patta status and execute registered commercial lease on `basundhara.assam.gov.in`.\n"
                f"3. **Capital Subsidy Claim:** File subsidy claim with General Manager, District Industries Centre (DIC) within 90 days of commercial commencement.\n"
            )
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": normalize_markdown(full_answer)}

z11_pragati_agent = Z11PragatiAgent()

