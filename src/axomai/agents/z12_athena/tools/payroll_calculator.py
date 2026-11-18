"""
Z12 Athena - Statutory Payroll & Compliance Calculator.
Calculates EPF (12%), ESIC (0.75%), Assam Professional Tax, and net take-home salary.
"""

from typing import Dict, Any

class PayrollCalculator:
    """Calculates statutory deductions for Indian & Assam jurisdiction."""

    def compute_employee_payroll(self, gross_salary: float) -> Dict[str, Any]:
        basic_da = gross_salary * 0.50 # typically 50% of gross
        hra = gross_salary * 0.30
        special_allowance = gross_salary * 0.20

        # EPF: 12% of Basic + DA (capped at ₹15,000 basic unless voluntary)
        epf_wage_base = min(basic_da, 15000.0)
        employee_epf = round(epf_wage_base * 0.12, 2)
        employer_epf = round(epf_wage_base * 0.12, 2)

        # ESIC: Applicable if Gross <= 21,000
        if gross_salary <= 21000.0:
            employee_esic = round(gross_salary * 0.0075, 2) # 0.75%
            employer_esic = round(gross_salary * 0.0325, 2) # 3.25%
        else:
            employee_esic = 0.0
            employer_esic = 0.0

        # Statutory Professional Tax (PT) - Standard Slabs
        if gross_salary > 25000:
            pt = 208.0
        elif gross_salary > 15000:
            pt = 150.0
        elif gross_salary > 10000:
            pt = 100.0
        else:
            pt = 0.0

        total_deductions = round(employee_epf + employee_esic + pt, 2)
        net_in_hand = round(gross_salary - total_deductions, 2)
        total_ctc = round(gross_salary + employer_epf + employer_esic, 2)

        return {
            "gross_salary": gross_salary,
            "basic_da": round(basic_da, 2),
            "hra": round(hra, 2),
            "special_allowance": round(special_allowance, 2),
            "employee_epf": employee_epf,
            "employer_epf": employer_epf,
            "employee_esic": employee_esic,
            "employer_esic": employer_esic,
            "professional_tax": pt,
            "assam_professional_tax": pt, # backward-compatible alias
            "total_employee_deductions": total_deductions,
            "net_in_hand_salary": net_in_hand,
            "total_monthly_ctc": total_ctc
        }

payroll_calculator = PayrollCalculator()

