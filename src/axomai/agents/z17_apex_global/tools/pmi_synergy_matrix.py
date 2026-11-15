"""
Z17 Apex-Global - Post-Merger Integration (PMI) & Synergy Realization Matrix.
Models Day-1 to Day-100 corporate integration milestones, run-rate cost synergies,
procurement scale discounts, and probability-weighted implementation haircuts.
"""

from typing import Dict, Any, List

class PMISynergyMatrix:
    """Models corporate M&A post-closing operational synergies and integration milestones."""

    def __init__(self):
        pass

    def calculate_synergy_roadmap(
        self,
        target_revenue_millions: float = 120.0,
        target_operating_expenses_millions: float = 85.0,
        discount_rate_wacc: float = 0.095
    ) -> Dict[str, Any]:
        """
        Quantifies operational cost and revenue synergies across functional pillars:
        - SG&A / Corporate Overhead reduction
        - IT / ERP Cloud license consolidation
        - Supply chain & procurement scale discounts
        """
        # Hard Cost Synergies (Annual Run-Rate)
        sga_synergy = round(target_operating_expenses_millions * 0.08, 2)     # 8% SG&A rationalization
        it_erp_synergy = round(target_operating_expenses_millions * 0.045, 2)  # 4.5% IT systems consolidation
        procurement_synergy = round(target_operating_expenses_millions * 0.035, 2) # 3.5% COGS procurement bulk savings

        total_gross_cost_synergies = round(sga_synergy + it_erp_synergy + procurement_synergy, 2)

        # Implementation costs (one-time severance, retention, migration fees)
        one_time_integration_costs = round(total_gross_cost_synergies * 1.25, 2)

        # Haircut (20% risk buffer for integration friction)
        synergy_haircut_pct = 0.20
        net_annual_run_rate_synergies = round(total_gross_cost_synergies * (1.0 - synergy_haircut_pct), 2)

        # Capitalized Synergy Present Value (Perpetuity at WACC)
        capitalized_synergy_value = round((net_annual_run_rate_synergies / discount_rate_wacc) - one_time_integration_costs, 2)

        milestones = [
            {"day": "Day 1 (Closing)", "action": "Assume control, issue joint employee communication, secure key customer contracts, establish Integration Management Office (IMO)."},
            {"day": "Day 30", "action": "Harmonize sales territories, merge procurement vendor rate cards, launch executive retention pools."},
            {"day": "Day 60", "action": "Consolidate duplicate software licenses, initiate finance ERP data migration to SAP/NetSuite."},
            {"day": "Day 100", "action": "Finalize organizational redesign, eliminate redundant back-office layers, achieve 60% run-rate synergy exit velocity."}
        ]

        return {
            "target_revenue_millions": f"${target_revenue_millions:,.1f}M",
            "target_opex_millions": f"${target_operating_expenses_millions:,.1f}M",
            "annual_synergies_breakdown": {
                "sga_rationalization_millions": sga_synergy,
                "it_systems_consolidation_millions": it_erp_synergy,
                "procurement_scale_savings_millions": procurement_synergy,
                "total_gross_annual_run_rate_millions": total_gross_cost_synergies,
                "net_annual_run_rate_post_haircut_millions": net_annual_run_rate_synergies,
            },
            "one_time_integration_capex_millions": one_time_integration_costs,
            "net_capitalized_synergy_enterprise_value_millions": capitalized_synergy_value,
            "integration_milestones": milestones,
            "strategic_verdict": (
                f"Net annualized synergy potential of ${net_annual_run_rate_synergies}M justifies up to "
                f"${capitalized_synergy_value}M in incremental acquisition premium."
            )
        }

pmi_synergy_matrix = PMISynergyMatrix()

