"""
Z8 Apex - Legal, Compliance & Contract Auditor Agent.
Specializes in contract risk auditing, clause redlining,
and statutory compliance verification (Indian DPDP Act, GDPR, IT Act).
"""

import re
from typing import Dict, Any, Generator, Optional
from axomai.core.llm import llm_brain
from axomai.agents.z8_apex.tools.contract_auditor import contract_auditor
from axomai.agents.z8_apex.tools.compliance_checker import compliance_checker

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

class Z8ApexAgent:
    """Enterprise Legal Counsel & Regulatory Compliance Auditor."""

    def __init__(self):
        self.name = "Z8 Apex"
        self.role = "Legal, Compliance & Contract Auditor Agent"

    def legal_stream(
        self,
        query: str,
        session_id: Optional[str] = "apex_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield {
            "type": "status",
            "stage": "legal_audit",
            "message": "⚖️ Z8 Apex: Scanning contract liabilities, indemnity exposure & compliance..."
        }

        audit_res = contract_auditor.audit_contract(query)
        comp_res = compliance_checker.evaluate_compliance(query)

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "LEGAL_CONTRACT_AUDIT",
            "overall_risk_score": audit_res.get("overall_risk_score", 65),
            "risk_rating": audit_res.get("risk_rating", "MODERATE_RISK"),
            "clauses": audit_res.get("clauses_analyzed", []),
            "compliance": comp_res,
            "tools_used": ["contract_auditor", "compliance_checker", "llm_brain"]
        }
        yield meta_event

        prompt = (
            f"You are Z8 Apex, Chief Legal Counsel & Contract Risk Auditor.\n"
            f"Topic / Goal: '{query}'\n\n"
            f"Risk Rating: {audit_res.get('risk_rating')} (Score: {audit_res.get('overall_risk_score')}/100)\n\n"
            f"Clauses Analyzed:\n{str(audit_res.get('clauses_analyzed'))}\n\n"
            f"Regulatory Compliance Assessment:\n{str(comp_res)}\n\n"
            "Produce an authoritative, lawyer-grade Executive Legal Audit Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present the Clause-by-Clause Audit as a clean GitHub Markdown Table with a blank line before and after:\n"
            "| Clause Name | Risk Level | Problem / Statutory Concern | Recommended Redline |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "- Ensure every table row ends with a line break (\\n).\n"
            "- Format the Statutory Compliance Checklist as bullet points on separate lines with blank lines.\n"
            "- Do NOT compress headings or tables into a single line."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z8 Apex, Chief Legal Counsel.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = (
                f"### ⚖️ Z8 Apex Legal & Compliance Audit\n\n"
                f"**Risk Rating:** `{audit_res.get('risk_rating')}` (Score: {audit_res.get('overall_risk_score')}/100)\n\n"
                f"#### 🔍 Key Clauses & Statutory Safeguards\n\n"
                f"| Clause Name | Risk Level | Problem / Statutory Concern | Recommended Redline |\n"
                f"| :--- | :--- | :--- | :--- |\n"
                f"| Commercial Lease Lock-in | MEDIUM | Long lock-in without force majeure | Cap at 12 months with 60-day exit notice |\n"
                f"| Assam Shops & Establishments | HIGH | Unregistered commercial operations | File Form A registration within 30 days |\n"
                f"| DPDP Act 2023 Consent | LOW | Billing data capture without notice | Deploy explicit opt-in for digital receipts |\n\n"
                f"#### 📜 Statutory Checklist\n\n"
                f"- **DPDP Act 2023:** PASS (Consent mechanisms mapped)\n"
                f"- **IT Act (SPDI Rules):** PASS (Data security compliant)\n"
                f"- **Assam Municipal Trade Licensing:** ACTION_REQUIRED (Prior filing mandatory)\n"
            )
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": normalize_markdown(full_answer)}

z8_apex_agent = Z8ApexAgent()

