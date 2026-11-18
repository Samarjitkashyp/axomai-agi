"""
Z11 Pragati - Global Public Policy, Statutory Incentives & Sovereign Governance Agent.
Delivers authoritative guidance on National, Provincial/State, and Global industrial policies,
capital subsidies, single-window clearances, and public procurement frameworks.
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
    """Enterprise Chief Public Policy Officer & Sovereign Governance Specialist."""

    def __init__(self):
        self.name = "Z11 Pragati"
        self.role = "Public Policy, Statutory Incentives & Sovereign Governance Specialist"

    def policy_stream(
        self,
        query: str,
        session_id: Optional[str] = "pragati_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield {
            "type": "status",
            "stage": "policy_matching",
            "message": "🏛️ Z11 Pragati: Matching commercial profile with National, Provincial & Global Public Policy Incentives..."
        }

        matched = scheme_matcher.match_schemes(query)

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "PUBLIC_POLICY_AND_INCENTIVES",
            "matched_schemes_count": len(matched),
            "top_scheme": matched[0]["scheme_name"] if matched else "National Policy Framework",
            "schemes": matched,
            "tools_used": ["scheme_matcher"]
        }
        yield meta_event

        prompt = (
            f"You are Z11 Pragati, Chief Public Policy & Sovereign Governance Advisor.\n"
            f"User Goal: '{query}'\n\n"
            f"Matched Policy Subsidies & Regulatory Incentives:\n{str(matched)}\n\n"
            "Formulate an authoritative, official-grade Public Policy & Incentives Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present Scheme Comparison as a clean GitHub Markdown Table with blank lines before and after:\n"
            "| Scheme Name | Jurisdiction / Department | Financial Benefit | Eligibility Criteria | Portal |\n"
            "| :--- | :--- | :--- | :--- | :--- |\n"
            "- Outline procedural step-by-step guidance for applying via Single Window Clearance / Official Portals.\n"
            "- Ensure every table row ends with a newline."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z11 Pragati, Global Public Policy Specialist.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = (
                f"### 🏛️ Z11 Pragati: Sovereign Public Policy & Industrial Incentives Dossier\n\n"
                f"**Scope:** Multi-Jurisdiction National & Global Statutory Incentives Framework\n\n"
                f"#### 📜 Matched Policy Subsidies & Industrial Capital Frameworks\n\n"
                f"| Scheme Name | Jurisdiction / Department | Financial Benefit | Eligibility Criteria | Portal |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
            )
            for s in matched:
                full_answer += (
                    f"| **{s['scheme_name']}** | {s.get('jurisdiction', '')} • {s['department']} | {s['financial_benefit']} | "
                    f"{s['eligibility']} | `{s['application_portal']}` |\n"
                )
            full_answer += (
                f"\n#### 📑 Procedural Application Protocol:\n\n"
                f"1. **National Single Window Clearance (NSWS):** Onboard via `nsws.gov.in` to obtain composite commercial business approvals across central and provincial line ministries.\n"
                f"2. **Statutory Land & Lease Verification:** Verify land zoning, master plan compliance, and execute registered commercial lease agreements.\n"
                f"3. **Incentive Claim Filing:** Submit audited capital expenditure statements and commercial commencement certificate within the statutory notice window.\n"
            )
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": normalize_markdown(full_answer)}

z11_pragati_agent = Z11PragatiAgent()
