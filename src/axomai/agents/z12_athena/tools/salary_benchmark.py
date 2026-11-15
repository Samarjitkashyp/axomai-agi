"""
Z12 Athena - Regional Salary Benchmarking & Workforce Sizing Tool.
Maintains structured compensation bands and headcount models across Assam districts.
"""

from typing import Dict, Any, List

REGIONAL_SALARY_BANDS = {
    "guwahati": {
        "store_manager": {"min": 32000, "median": 38000, "max": 48000},
        "asst_manager": {"min": 22000, "median": 26000, "max": 32000},
        "billing_pos_operator": {"min": 16000, "median": 18500, "max": 22000},
        "sales_associate": {"min": 14000, "median": 16500, "max": 19500},
        "inventory_clerk": {"min": 15000, "median": 17500, "max": 21000},
        "security_housekeeping": {"min": 11500, "median": 12500, "max": 14000}
    },
    "dibrugarh": {
        "store_manager": {"min": 26000, "median": 32000, "max": 40000},
        "asst_manager": {"min": 19000, "median": 23000, "max": 27000},
        "billing_pos_operator": {"min": 14500, "median": 16500, "max": 19000},
        "sales_associate": {"min": 12500, "median": 14500, "max": 17000},
        "inventory_clerk": {"min": 13500, "median": 15500, "max": 18000},
        "security_housekeeping": {"min": 10500, "median": 11500, "max": 13000}
    },
    "nagaon": {
        "store_manager": {"min": 24000, "median": 28000, "max": 35000},
        "asst_manager": {"min": 18000, "median": 21000, "max": 25000},
        "billing_pos_operator": {"min": 13500, "median": 15000, "max": 17500},
        "sales_associate": {"min": 11500, "median": 13500, "max": 16000},
        "inventory_clerk": {"min": 12500, "median": 14500, "max": 17000},
        "security_housekeeping": {"min": 10500, "median": 11200, "max": 12500}
    }
}

class SalaryBenchmarkEngine:
    """Computes staffing model, headcounts, and monthly wage budgets."""

    def get_district_staffing_model(self, district: str, sqft: int = 2000) -> Dict[str, Any]:
        key = "guwahati" if "guwahati" in district.lower() or "kamrup" in district.lower() else ("dibrugarh" if "dibrugarh" in district.lower() else "nagaon")
        bands = REGIONAL_SALARY_BANDS[key]

        # Sizing model based on sqft
        if sqft >= 2200:
            headcount = [
                ("Store Manager", 1, bands["store_manager"]["median"]),
                ("Asst Store Manager", 1, bands["asst_manager"]["median"]),
                ("Senior Billing Executive", 2, bands["billing_pos_operator"]["median"]),
                ("Retail Sales Associates", 4, bands["sales_associate"]["median"]),
                ("Inventory / Backroom Lead", 1, bands["inventory_clerk"]["median"]),
                ("Security & Maintenance", 2, bands["security_housekeeping"]["median"]),
            ]
        elif sqft >= 1600:
            headcount = [
                ("Store Manager", 1, bands["store_manager"]["median"]),
                ("Billing Executive", 1, bands["billing_pos_operator"]["median"]),
                ("Retail Sales Associates", 3, bands["sales_associate"]["median"]),
                ("Inventory Clerk", 1, bands["inventory_clerk"]["median"]),
                ("Security & Housekeeping", 1, bands["security_housekeeping"]["median"]),
            ]
        else:
            headcount = [
                ("Store Manager / Lead", 1, bands["store_manager"]["median"]),
                ("Billing Operator", 1, bands["billing_pos_operator"]["median"]),
                ("Retail Sales Associates", 2, bands["sales_associate"]["median"]),
                ("Security & Housekeeping", 1, bands["security_housekeeping"]["median"]),
            ]

        total_headcount = sum(item[1] for item in headcount)
        monthly_payroll_inr = sum(item[1] * item[2] for item in headcount)

        return {
            "district": district.title(),
            "sqft": sqft,
            "total_headcount": total_headcount,
            "monthly_payroll_inr": monthly_payroll_inr,
            "annual_payroll_inr": monthly_payroll_inr * 12,
            "staff_breakdown": [
                {"role": r, "count": c, "monthly_salary_inr": s, "subtotal_inr": c * s}
                for r, c, s in headcount
            ]
        }

salary_benchmark = SalaryBenchmarkEngine()

