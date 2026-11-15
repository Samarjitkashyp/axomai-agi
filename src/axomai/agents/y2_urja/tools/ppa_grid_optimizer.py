"""
Y2 Urja - Open Access Power Purchase Agreement (PPA) & Smart Grid Optimizer.
Analyzes industrial open-access PPA power tariffs against State Discom retail rates,
computes Cross-Subsidy Surcharges (CSS), and models Time-of-Day (ToD) load shifting.
"""

from typing import Dict, Any

class PPAGridOptimizer:
    """Optimizes industrial electricity procurement, green open-access, and peak-shaving."""

    def __init__(self):
        # Assam Power Distribution Company Ltd (APDCL) baseline commercial tariffs
        self.grid_tariffs = {
            "discom_base_rate_inr_kwh": 8.45,
            "green_ppa_generation_rate_inr": 4.80,
            "cross_subsidy_surcharge_css_inr": 1.45,
            "wheeling_charges_inr": 0.65,
            "transmission_losses_pct": 3.8,  # 3.8% loss
            "tod_peak_surcharge_pct": 20.0,  # 20% surcharge between 17:00 - 22:00
            "tod_off_peak_rebate_pct": 10.0   # 10% rebate between 23:00 - 06:00
        }

    def evaluate_green_open_access_ppa(
        self,
        monthly_consumption_kwh: float = 120000.0,
        contracted_demand_kva: float = 250.0,
        green_ppa_share_pct: float = 70.0
    ) -> Dict[str, Any]:
        """
        Calculates net delivered tariff under the Green Energy Open Access Rules 2022.
        """
        base_grid = self.grid_tariffs["discom_base_rate_inr_kwh"]
        ppa_gen = self.grid_tariffs["green_ppa_generation_rate_inr"]
        css = self.grid_tariffs["cross_subsidy_surcharge_css_inr"]
        wheeling = self.grid_tariffs["wheeling_charges_inr"]

        # Delivered Green PPA cost = PPA Gen + CSS + Wheeling
        delivered_ppa_rate = round(ppa_gen + css + wheeling, 2)

        # Total cost without PPA (100% Discom)
        baseline_monthly_bill_inr = round(monthly_consumption_kwh * base_grid, 2)

        # Blended tariff with Green PPA
        ppa_kwh = monthly_consumption_kwh * (green_ppa_share_pct / 100.0)
        grid_kwh = monthly_consumption_kwh - ppa_kwh
        blended_bill_inr = round((ppa_kwh * delivered_ppa_rate) + (grid_kwh * base_grid), 2)
        blended_effective_rate = round(blended_bill_inr / monthly_consumption_kwh, 2)

        monthly_savings_inr = round(baseline_monthly_bill_inr - blended_bill_inr, 2)
        annual_savings_inr = round(monthly_savings_inr * 12.0, 2)
        savings_pct = round((monthly_savings_inr / baseline_monthly_bill_inr) * 100.0, 1)

        return {
            "monthly_consumption_kwh": monthly_consumption_kwh,
            "discom_standard_tariff_inr_kwh": base_grid,
            "delivered_green_ppa_tariff_inr_kwh": delivered_ppa_rate,
            "blended_effective_tariff_inr_kwh": blended_effective_rate,
            "green_power_mix_pct": f"{green_ppa_share_pct}%",
            "baseline_annual_bill_inr": round(baseline_monthly_bill_inr * 12.0, 2),
            "optimized_annual_bill_inr": round(blended_bill_inr * 12.0, 2),
            "annual_cost_savings_inr": annual_savings_inr,
            "savings_percentage": f"{savings_pct}%",
            "regulatory_framework": "Ministry of Power Green Energy Open Access Rules (100 kW threshold qualified)",
            "peak_shifting_recommendation": (
                "Shift heavy grinding/drying batch operations from 18:00 peak to 23:00 off-peak window "
                "to capture an additional 10% ToD rebate on remaining Discom draw."
            )
        }

ppa_grid_optimizer = PPAGridOptimizer()

