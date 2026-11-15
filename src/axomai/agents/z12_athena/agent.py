"""
Z12 Athena - Chief Human Resources Officer & Workforce Strategy Agent.
Orchestrates talent acquisition, regional compensation benchmarking,
Assam statutory labour compliance, and organizational headcount models.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.z12_athena.tools.salary_benchmark import salary_benchmark
from axomai.agents.z12_athena.tools.payroll_calculator import payroll_calculator

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

class Z12AthenaAgent:
    """Enterprise Chief Human Resources Officer & Workforce Planning Specialist."""

    def __init__(self):
        self.name = "Z12 Athena"
        self.role = "Talent Acquisition, Workforce Strategy & HR Payroll Agent"

    def hr_stream(
        self,
        query: str,
        session_id: Optional[str] = "athena_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield {
            "type": "status",
            "stage": "hr_benchmarking",
            "message": "👥 Z12 Athena: Modeling staffing headcounts, regional compensation bands & EPF/ESIC payroll..."
        }

        # Analyze target districts
        districts = [
            ("Guwahati (Kamrup Metro)", 2500),
            ("Dibrugarh", 1800),
            ("Nagaon", 1500)
        ]
        models = [salary_benchmark.get_district_staffing_model(d, sqft=s) for d, s in districts]
        total_hc = sum(m["total_headcount"] for m in models)
        total_monthly_wage = sum(m["monthly_payroll_inr"] for m in models)

        # Sample statutory breakdown for a typical ₹20,000 billing operator
        sample_payroll = payroll_calculator.compute_employee_payroll(20000.0)

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "HUMAN_RESOURCES_WORKFORCE_STRATEGY",
            "total_headcount": total_hc,
            "total_monthly_payroll_inr": total_monthly_wage,
            "districts_modeled": [d[0] for d in districts],
            "staffing_models": models,
            "sample_payroll_breakdown": sample_payroll,
            "tools_used": ["salary_benchmark", "payroll_calculator"]
        }
        yield meta_event

        prompt = (
            f"You are Z12 Athena, Chief Human Resources Officer & Workforce Strategist for Northeast India.\n"
            f"User Goal / Inquiry: '{query}'\n\n"
            f"District Staffing Models:\n{str(models)}\n\n"
            f"Statutory Payroll Structure (EPF/ESIC/PT):\n{str(sample_payroll)}\n\n"
            "Formulate an authoritative, boardroom-grade Workforce Strategy & Staffing Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present District Staffing Breakdown as a clean GitHub Markdown Table with blank lines before and after:\n"
            "| District | Store Area (sq.ft) | Total Headcount | Monthly Wage Budget (₹) | Key Roles Hired |\n"
            "| :--- | :--- | :--- | :--- | :--- |\n"
            "- Outline statutory compliance (Assam Minimum Wages, EPF 12%, ESIC 0.75%, Assam PT) and bilingual customer service training protocols.\n"
            "- Ensure every table row ends with a newline."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z12 Athena, Chief HR Officer.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = (
                f"### 👥 Z12 Athena: Workforce Planning & Regional Payroll Dossier\n\n"
                f"**Total Headcount Across Network:** `{total_hc} Employees` | **Monthly Wage Outlay:** `₹{total_monthly_wage:,.2f}`\n\n"
                f"#### 👔 District Staffing & Compensation Matrix\n\n"
                f"| District | Store Area (sq.ft) | Total Headcount | Monthly Wage Budget (₹) | Key Roles Hired |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
            )
            for m in models:
                full_answer += (
                    f"| **{m['district']}** | {m['sqft']} sq.ft | {m['total_headcount']} Staff | "
                    f"₹{m['monthly_payroll_inr']:,.2f} | Store Manager, Cashiers, Associates |\n"
                )
            full_answer += (
                f"\n#### 📑 Statutory Deductions & Take-Home (Sample ₹20,000 Gross Salary):\n\n"
                f"- **Employee EPF (12% of Basic):** ₹1,200.00\n"
                f"- **Employee ESIC (0.75%):** ₹150.00\n"
                f"- **Assam Professional Tax (PT):** ₹150.00\n"
                f"- **Net Take-Home Salary:** `₹18,500.00 / month`\n"
                f"- **Employer Contribution (EPF 12% + ESIC 3.25%):** ₹1,850.00 (Total CTC: ₹21,850.00)\n\n"
                f"#### 🎯 Workforce Onboarding Protocol:\n"
                f"1. **Bilingual Fluency Mandate:** 100% customer-facing staff must be fluent in Assamese and Hindi/English.\n"
                f"2. **POS & DPDP Training:** 3-day intensive workshop on digital billing, inventory barcode scanning, and customer data consent.\n"
            )
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": normalize_markdown(full_answer)}

z12_athena_agent = Z12AthenaAgent()

