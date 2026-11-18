"""
Z12 Athena - Global & National Salary Benchmarking & Workforce Sizing Tool.
Maintains structured compensation bands and headcount models across Tier 1, Tier 2, and Tier 3 markets.
"""

from typing import Dict, Any, List, Optional

TIER_SALARY_BANDS = {
    "tier_1_metro": {
        "store_manager": {"min": 55000, "median": 70000, "max": 95000},
        "asst_manager": {"min": 35000, "median": 45000, "max": 58000},
        "billing_pos_operator": {"min": 24000, "median": 28000, "max": 35000},
        "sales_associate": {"min": 20000, "median": 24000, "max": 30000},
        "inventory_clerk": {"min": 22000, "median": 26000, "max": 32000},
        "security_housekeeping": {"min": 16000, "median": 18500, "max": 22000}
    },
    "tier_2_hub": {
        "store_manager": {"min": 32000, "median": 40000, "max": 52000},
        "asst_manager": {"min": 22000, "median": 27000, "max": 34000},
        "billing_pos_operator": {"min": 16000, "median": 19000, "max": 23000},
        "sales_associate": {"min": 14000, "median": 17000, "max": 21000},
        "inventory_clerk": {"min": 15000, "median": 18000, "max": 22000},
        "security_housekeeping": {"min": 12000, "median": 13500, "max": 15000}
    },
    "tier_3_regional": {
        "store_manager": {"min": 24000, "median": 30000, "max": 38000},
        "asst_manager": {"min": 18000, "median": 22000, "max": 26000},
        "billing_pos_operator": {"min": 13500, "median": 15500, "max": 18500},
        "sales_associate": {"min": 12000, "median": 14000, "max": 16500},
        "inventory_clerk": {"min": 13000, "median": 15000, "max": 17500},
        "security_housekeeping": {"min": 10500, "median": 11500, "max": 13000}
    }
}

# Cross-Industry Dynamic Compensation Multipliers
INDUSTRY_SALARY_FACTORS = {
    "tech_software": {"entry": 45000, "mid": 95000, "senior": 185000, "lead": 280000, "director": 420000},
    "data_ai": {"entry": 55000, "mid": 115000, "senior": 210000, "lead": 320000, "director": 500000},
    "healthcare_pharma": {"entry": 35000, "mid": 75000, "senior": 140000, "lead": 220000, "director": 380000},
    "civil_epc": {"entry": 30000, "mid": 65000, "senior": 125000, "lead": 195000, "director": 350000},
    "finance_accounting": {"entry": 32000, "mid": 70000, "senior": 135000, "lead": 210000, "director": 380000},
    "logistics_supply_chain": {"entry": 25000, "mid": 50000, "senior": 95000, "lead": 150000, "director": 260000},
    "general_commercial": {"entry": 20000, "mid": 40000, "senior": 75000, "lead": 120000, "director": 200000}
}

class SalaryBenchmarkEngine:
    """Computes staffing model, headcounts, and monthly wage budgets across market tiers."""

    def benchmark_role(self, role_title: str, location: str = "Tier 2 Hub") -> Dict[str, Any]:
        """Dynamically benchmarks compensation for ANY professional job role across any location."""
        r_lower = role_title.lower()
        loc_lower = location.lower()
        
        # Location tier factor
        if any(c in loc_lower for c in ["mumbai", "delhi", "bengaluru", "bangalore", "london", "singapore", "new york", "san francisco", "tier 1"]):
            tier_multiplier = 1.35
            tier_name = "Tier 1 Metro / Global Hub"
        elif any(c in loc_lower for c in ["rural", "town", "tier 3", "district"]):
            tier_multiplier = 0.75
            tier_name = "Tier 3 Regional Market"
        else:
            tier_multiplier = 1.0
            tier_name = "Tier 2 Growth Hub"

        # Industry category matching
        if any(k in r_lower for k in ["ai", "machine learning", "data scientist", "nlp"]):
            base_curve = INDUSTRY_SALARY_FACTORS["data_ai"]
        elif any(k in r_lower for k in ["software", "developer", "engineer", "devops", "cloud", "backend", "frontend"]):
            base_curve = INDUSTRY_SALARY_FACTORS["tech_software"]
        elif any(k in r_lower for k in ["doctor", "physician", "pharmacist", "nurse", "medical", "clinical"]):
            base_curve = INDUSTRY_SALARY_FACTORS["healthcare_pharma"]
        elif any(k in r_lower for k in ["civil", "structural", "project manager", "site", "epc", "embankment"]):
            base_curve = INDUSTRY_SALARY_FACTORS["civil_epc"]
        elif any(k in r_lower for k in ["finance", "accountant", "audit", "treasury", "cfo", "controller"]):
            base_curve = INDUSTRY_SALARY_FACTORS["finance_accounting"]
        elif any(k in r_lower for k in ["fleet", "logistics", "supply chain", "warehouse", "freight"]):
            base_curve = INDUSTRY_SALARY_FACTORS["logistics_supply_chain"]
        else:
            base_curve = INDUSTRY_SALARY_FACTORS["general_commercial"]

        # Seniority level detection
        if any(k in r_lower for k in ["chief", "c-level", "vp", "director", "head"]):
            base_val = base_curve["director"]
        elif any(k in r_lower for k in ["lead", "principal", "manager", "staff"]):
            base_val = base_curve["lead"]
        elif any(k in r_lower for k in ["senior", "sr", "expert"]):
            base_val = base_curve["senior"]
        elif any(k in r_lower for k in ["junior", "associate", "intern", "entry", "fresher"]):
            base_val = base_curve["entry"]
        else:
            base_val = base_curve["mid"]

        median = round(base_val * tier_multiplier)
        min_salary = round(median * 0.80)
        max_salary = round(median * 1.30)

        return {
            "role": role_title.title(),
            "location": location.title(),
            "tier_classification": tier_name,
            "monthly_min_inr": min_salary,
            "monthly_median_inr": median,
            "monthly_max_inr": max_salary,
            "annual_ctc_median_inr": median * 12
        }

    def get_district_staffing_model(self, district: str, sqft: int = 2000) -> Dict[str, Any]:
        d_lower = district.lower()
        if any(c in d_lower for c in ["mumbai", "delhi", "bengaluru", "bangalore", "london", "singapore", "new york", "hyderabad", "chennai"]):
            tier_key = "tier_1_metro"
            tier_label = "Tier 1 Mega Metro"
        elif any(c in d_lower for c in ["regional", "tier 3", "rural", "town"]):
            tier_key = "tier_3_regional"
            tier_label = "Tier 3 Regional Market"
        else:
            tier_key = "tier_2_hub"
            tier_label = "Tier 2 Commercial Growth Hub"

        bands = TIER_SALARY_BANDS[tier_key]

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
                ("Store Lead / Manager", 1, bands["store_manager"]["median"]),
                ("Multi-Role Associate (POS/Sales)", 2, bands["sales_associate"]["median"]),
                ("Security / Support", 1, bands["security_housekeeping"]["median"]),
            ]

        total_staff = sum(h[1] for h in headcount)
        monthly_base_payroll = sum(h[1] * h[2] for h in headcount)

        breakdown = [
            {"role": h[0], "count": h[1], "median_salary_inr": h[2], "total_role_cost_inr": h[1] * h[2]}
            for h in headcount
        ]

        return {
            "district": district.title(),
            "market_jurisdiction": district.title(),
            "tier_classification": tier_label,
            "sqft": sqft,
            "commercial_sqft": sqft,
            "total_headcount": total_staff,
            "monthly_payroll_inr": monthly_base_payroll,
            "monthly_base_payroll_inr": monthly_base_payroll,
            "annualized_base_payroll_inr": monthly_base_payroll * 12,
            "roles_breakdown": breakdown
        }

salary_benchmark = SalaryBenchmarkEngine()
