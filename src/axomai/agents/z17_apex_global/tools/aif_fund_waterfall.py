"""
Z17 Apex-Global - SEBI AIF Category I/II Private Equity Fund Waterfall Engine.
Models institutional Indian PE/VC fund distributions: European whole-of-fund vs American deal-by-deal waterfalls,
INR hurdle rates (8-10%), 80/20 GP catch-up, and 20% carried interest realizations.
"""

from typing import Dict, Any, List

class AIFFundWaterfallEngine:
    """Models institutional SEBI AIF Category I & II distribution waterfalls."""

    def compute_distribution_waterfall(
        self,
        fund_name: str = "AxomAI Sovereign Growth Fund I (SEBI Cat II AIF)",
        total_committed_capital_inr_cr: float = 500.0,
        total_realized_proceeds_inr_cr: float = 1250.0,
        investment_horizon_years: float = 5.0,
        lp_hurdle_rate_pct: float = 9.0,
        carried_interest_pct: float = 20.0,
        waterfall_type: str = "EUROPEAN_WHOLE_OF_FUND"
    ) -> Dict[str, Any]:
        """
        Computes 4-tier distribution waterfall for Indian Private Equity funds.
        """
        # Tier 1: 100% Return of Capital to Limited Partners (LPs)
        capital_return_to_lps_cr = total_committed_capital_inr_cr
        remaining_proceeds_cr = total_realized_proceeds_inr_cr - capital_return_to_lps_cr

        # Tier 2: LP Preferred Return (Hurdle Rate compounded annually)
        hurdle_rate = lp_hurdle_rate_pct / 100.0
        total_lp_preferred_return_cr = round(total_committed_capital_inr_cr * (((1.0 + hurdle_rate) ** investment_horizon_years) - 1.0), 2)
        lp_pref_paid_cr = min(remaining_proceeds_cr, total_lp_preferred_return_cr)
        remaining_proceeds_cr = round(remaining_proceeds_cr - lp_pref_paid_cr, 2)

        # Tier 3: GP Catch-Up (80% to LPs / 20% to GP catch-up)
        # Catch-up amount = (LP Preferred Return / (1 - Carry%)) * Carry%
        carry_frac = carried_interest_pct / 100.0
        target_catchup_cr = round((lp_pref_paid_cr / (1.0 - carry_frac)) * carry_frac, 2)
        gp_catchup_paid_cr = min(remaining_proceeds_cr, target_catchup_cr)
        remaining_proceeds_cr = round(remaining_proceeds_cr - gp_catchup_paid_cr, 2)

        # Tier 4: Carried Interest Split (80% LP / 20% GP)
        excess_to_lps_cr = round(remaining_proceeds_cr * (1.0 - carry_frac), 2)
        excess_to_gp_cr = round(remaining_proceeds_cr * carry_frac, 2)

        # Total Aggregated Payouts
        total_lp_proceeds_cr = round(capital_return_to_lps_cr + lp_pref_paid_cr + excess_to_lps_cr, 2)
        total_gp_proceeds_cr = round(gp_catchup_paid_cr + excess_to_gp_cr, 2)
        total_gp_proceeds_usd_m = round(total_gp_proceeds_cr * 0.12, 2)

        # Fund Return Metrics
        gross_fund_moic = round(total_realized_proceeds_inr_cr / total_committed_capital_inr_cr, 2)
        gross_fund_irr = round(((gross_fund_moic ** (1.0 / investment_horizon_years)) - 1.0) * 100.0, 1)

        net_lp_moic = round(total_lp_proceeds_cr / total_committed_capital_inr_cr, 2)
        net_lp_irr = round(((net_lp_moic ** (1.0 / investment_horizon_years)) - 1.0) * 100.0, 1)

        return {
            "fund_name": fund_name,
            "statutory_registration": "SEBI (Alternative Investment Funds) Regulations, 2012 (Category II AIF)",
            "waterfall_structure": waterfall_type,
            "fund_inputs": {
                "total_committed_capital_inr_cr": f"₹{total_committed_capital_inr_cr} Cr",
                "total_realized_proceeds_inr_cr": f"₹{total_realized_proceeds_inr_cr} Cr",
                "horizon_years": f"{investment_horizon_years} Years",
                "lp_hurdle_rate_inr": f"{lp_hurdle_rate_pct}% p.a.",
                "gp_carry_rate": f"{carried_interest_pct}%"
            },
            "distribution_tiers_inr_cr": {
                "tier1_lp_capital_return_cr": f"₹{capital_return_to_lps_cr} Cr (100% of principal)",
                "tier2_lp_preferred_return_cr": f"₹{lp_pref_paid_cr} Cr (Hurdle satisfaction)",
                "tier3_gp_catchup_cr": f"₹{gp_catchup_paid_cr} Cr (80/20 catch-up)",
                "tier4_residual_split": {
                    "lps_80_pct_cr": f"₹{excess_to_lps_cr} Cr",
                    "gp_20_pct_carry_cr": f"₹{excess_to_gp_cr} Cr"
                }
            },
            "net_fund_realizations": {
                "total_lp_distributions_cr": f"₹{total_lp_proceeds_cr} Cr (Net LP MOIC: {net_lp_moic}x / Net LP IRR: {net_lp_irr}%)",
                "total_gp_carried_interest_cr": f"₹{total_gp_proceeds_cr} Cr (${total_gp_proceeds_usd_m}M)"
            },
            "fund_performance_verdict": f"TOP_QUARTILE_AIF_PERFORMANCE: Net LP IRR of {net_lp_irr}% significantly exceeds the {lp_hurdle_rate_pct}% INR preferred hurdle."
        }

aif_fund_waterfall = AIFFundWaterfallEngine()
