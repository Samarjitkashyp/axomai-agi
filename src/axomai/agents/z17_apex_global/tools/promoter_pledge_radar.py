"""
Z17 Apex-Global - Promoter Share Pledge & Margin Call Liquidation Radar.
Monitors promoter share encumbrance on BSE/NSE, calculates NBFC lender margin call triggers,
and quantifies free-fall stock crash probabilities driven by pledge invocations.
"""

from typing import Dict, Any

class PromoterPledgeRadar:
    """Monitors promoter equity pledging and models collateral liquidation margin calls."""

    def analyze_promoter_pledges(
        self,
        company_name: str = "Target Listed Entity",
        current_share_price_inr: float = 450.0,
        total_shares_outstanding_cr: float = 10.0,
        promoter_holding_pct: float = 62.5,
        pledged_shares_pct_of_promoter: float = 48.0,
        lender_cover_ratio_required: float = 2.0
    ) -> Dict[str, Any]:
        """
        Calculates encumbered equity volume, loan amounts raised, and margin call trigger thresholds.
        """
        promoter_shares_cr = round(total_shares_outstanding_cr * (promoter_holding_pct / 100.0), 2)
        pledged_shares_cr = round(promoter_shares_cr * (pledged_shares_pct_of_promoter / 100.0), 2)
        unencumbered_shares_cr = round(promoter_shares_cr - pledged_shares_cr, 2)

        # Market Value of Pledged Shares
        pledged_market_value_cr = round(pledged_shares_cr * current_share_price_inr, 2)
        
        # Loan Raised against shares (assuming 50% LTV / 2.0x collateral cover)
        estimated_loan_raised_cr = round(pledged_market_value_cr / lender_cover_ratio_required, 2)
        estimated_loan_usd_m = round(estimated_loan_raised_cr * 0.12, 2)

        # Margin Call Trigger Level:
        # If collateral value drops below 1.4x loan, lender issues 24-hr margin call;
        # If below 1.25x, lender dumps shares on open exchange.
        margin_call_price_inr = round((estimated_loan_raised_cr * 1.40) / max(pledged_shares_cr, 0.01), 2)
        price_drop_to_margin_call_pct = round(((current_share_price_inr - margin_call_price_inr) / current_share_price_inr) * 100.0, 1)

        forced_liquidation_price_inr = round((estimated_loan_raised_cr * 1.25) / max(pledged_shares_cr, 0.01), 2)

        # Risk Classification
        if pledged_shares_pct_of_promoter >= 60.0:
            risk_tier = "CATASTROPHIC_PROMOTER_DEFAULT_RISK"
            actionable_advisory = "Extreme distress: NBFCs possess de facto control of the equity float; hostile takeover vulnerability."
        elif pledged_shares_pct_of_promoter >= 35.0:
            risk_tier = "CRITICAL_MARGIN_CALL_EXPOSURE"
            actionable_advisory = f"High vulnerability: A {price_drop_to_margin_call_pct}% drop to ₹{margin_call_price_inr} triggers automatic NBFC block liquidations."
        elif pledged_shares_pct_of_promoter >= 15.0:
            risk_tier = "MODERATE_ENCUMBRANCE"
            actionable_advisory = "Manageable pledge levels; requires covenant capping additional promoter borrowings."
        else:
            risk_tier = "PRISTINE_UNENCUMBERED_HOLDING"
            actionable_advisory = "Promoter equity float is clean with minimal debt encumbrance."

        return {
            "entity_name": company_name,
            "current_share_price": f"₹{current_share_price_inr:,.2f}",
            "promoter_holding_pct": f"{promoter_holding_pct}%",
            "pledged_shares_as_pct_of_promoter": f"{pledged_shares_pct_of_promoter}%",
            "total_pledged_shares_cr": f"{pledged_shares_cr} Cr shares",
            "unencumbered_promoter_shares_cr": f"{unencumbered_shares_cr} Cr shares",
            "market_value_of_pledged_equity_cr": f"₹{pledged_market_value_cr:,.2f} Cr",
            "estimated_promoter_debt_secured_cr": f"₹{estimated_loan_raised_cr:,.2f} Cr (${estimated_loan_usd_m}M)",
            "margin_call_trigger_price": f"₹{margin_call_price_inr:,.2f} (-{price_drop_to_margin_call_pct}%)",
            "forced_market_dump_price": f"₹{forced_liquidation_price_inr:,.2f}",
            "pledge_risk_classification": risk_tier,
            "underwriting_advisory": actionable_advisory
        }

promoter_pledge_radar = PromoterPledgeRadar()
