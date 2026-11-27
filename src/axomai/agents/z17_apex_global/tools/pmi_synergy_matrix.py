"""
Z17 Apex-Global - Post-Merger Integration (PMI) & Synergy Realization Matrix.
Models Day-1 to Day-100 corporate integration milestones, run-rate cost synergies,
procurement scale discounts, and probability-weighted implementation haircuts.
"""

from typing import Dict, Any, List

class PMISynergyMatrix:
    """Models corporate M&A post-closing operational synergies and integration milestones."""

    def calculate_synergy_roadmap(
        self,
        target_name: str = "Target Corporation",
        target_revenue_m: float = 120.0,
        target_ebitda_m: float = 24.0,
        target_operating_expenses_m: float = 85.0,
        discount_rate_wacc: float = 0.095
    ) -> Dict[str, Any]:
        """
        Quantifies operational cost and revenue synergies across functional pillars:
        - SG&A / Corporate Overhead reduction
        - IT / ERP Cloud license consolidation
        - Supply chain & procurement scale discounts
        """
        # Hard Cost Synergies (Annual Run-Rate)
        sga_synergy = round(target_operating_expenses_m * 0.085, 2)     # 8.5% SG&A rationalization
        it_erp_synergy = round(target_operating_expenses_m * 0.045, 2)  # 4.5% IT systems consolidation
        procurement_synergy = round(target_operating_expenses_m * 0.04, 2) # 4.0% COGS procurement bulk savings

        total_gross_cost_synergies = round(sga_synergy + it_erp_synergy + procurement_synergy, 2)

        # Implementation costs (one-time severance, retention, migration fees ~ 1.2x annual savings)
        one_time_integration_costs = round(total_gross_cost_synergies * 1.20, 2)

        # Haircut (20% risk buffer for integration execution friction)
        synergy_haircut_pct = 0.20
        net_annual_run_rate_synergies = round(total_gross_cost_synergies * (1.0 - synergy_haircut_pct), 2)

        # Capitalized Synergy Present Value (Perpetuity at WACC minus one-time integration capex)
        capitalized_synergy_value = round((net_annual_run_rate_synergies / discount_rate_wacc) - one_time_integration_costs, 2)

        milestones = [
            {
                "timeline": "Day 1 (Closing)",
                "action": f"Establish Integration Management Office (IMO) at {target_name}, secure executive retention pool, ensure customer contract continuity."
            },
            {
                "timeline": "Day 30",
                "action": "Harmonize sales compensation and territories, eliminate redundant vendor contracts, deploy unified finance controls."
            },
            {
                "timeline": "Day 60",
                "action": "Consolidate duplicate SaaS/ERP cloud software licenses, initiate supply chain vendor volume renegotiations."
            },
            {
                "timeline": "Day 100",
                "action": "Complete organizational restructuring, eliminate redundant back-office administrative layers, reach 65% exit synergy velocity."
            }
        ]

        return {
            "target_name": target_name,
            "target_revenue_m": f"${target_revenue_m:,.1f}M",
            "target_opex_m": f"${target_operating_expenses_m:,.1f}M",
            "annual_synergies_breakdown": {
                "sga_rationalization_m": sga_synergy,
                "it_systems_consolidation_m": it_erp_synergy,
                "procurement_scale_savings_m": procurement_synergy,
                "total_gross_annual_run_rate_m": total_gross_cost_synergies,
                "net_annual_run_rate_post_haircut_m": net_annual_run_rate_synergies
            },
            "one_time_integration_capex_m": one_time_integration_costs,
            "net_capitalized_synergy_enterprise_value_m": capitalized_synergy_value,
            "integration_milestones": milestones,
            "strategic_verdict": (
                f"Net annualized synergy potential of ${net_annual_run_rate_synergies}M justifies up to "
                f"${capitalized_synergy_value}M in incremental purchase price premium."
            )
        }

pmi_synergy_matrix = PMISynergyMatrix()
