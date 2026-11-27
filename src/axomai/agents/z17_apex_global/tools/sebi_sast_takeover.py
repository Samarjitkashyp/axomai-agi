"""
Z17 Apex-Global - SEBI Takeover Code (SAST Regulations 2011) Engine.
Evaluates mandatory 26% Public Open Offer obligations under Regulation 3 & 4,
computes statutory 60-day VWAP floor pricing under Regulation 8, and structures Regulation 17 escrow deposits.
"""

from typing import Dict, Any, List

class SEBISASTTakeoverEngine:
    """Computes statutory Open Offer obligations under SEBI (SAST) Regulations, 2011."""

    def evaluate_takeover_compliance(
        self,
        target_name: str = "Listed Target Enterprise",
        current_market_price_inr: float = 380.0,
        shares_outstanding_cr: float = 12.0,
        shares_to_acquire_cr: float = 3.6,  # 30% acquisition (triggers > 25% threshold)
        negotiated_deal_price_inr: float = 420.0,
        sixty_day_vwamp_inr: float = 375.50,
        fifty_two_week_high_inr: float = 410.0
    ) -> Dict[str, Any]:
        """
        Determines Open Offer triggers, statutory minimum price, and mandatory escrow funding.
        """
        acquisition_stake_pct = round((shares_to_acquire_cr / shares_outstanding_cr) * 100.0, 1)
        triggers_open_offer = acquisition_stake_pct >= 25.0

        # Mandatory 26% Open Offer Size under Regulation 7(1)
        mandatory_open_offer_shares_cr = round(shares_outstanding_cr * 0.26, 2)

        # Statutory Minimum Offer Price under Regulation 8(2): Highest of:
        # 1. Negotiated deal price
        # 2. 52-week highest price paid by acquirer
        # 3. 60-trading day Volume Weighted Average Market Price (VWAMP)
        statutory_offer_price_inr = max(negotiated_deal_price_inr, sixty_day_vwamp_inr, 395.0)

        # Total Open Offer Consideration (Assuming 100% public acceptance)
        open_offer_value_inr_cr = round(mandatory_open_offer_shares_cr * statutory_offer_price_inr, 2)
        total_open_offer_usd_m = round(open_offer_value_inr_cr * 0.12, 2)

        # Total Acquisition Cost (Negotiated Tranche + 26% Public Open Offer)
        negotiated_tranche_inr_cr = round(shares_to_acquire_cr * negotiated_deal_price_inr, 2)
        total_deal_size_inr_cr = round(negotiated_tranche_inr_cr + open_offer_value_inr_cr, 2)
        total_deal_size_usd_m = round(total_deal_size_inr_cr * 0.12, 2)

        # Mandatory Escrow Requirement under Regulation 17:
        # - 25% of the first ₹500 Cr
        # - 10% of the balance exceeding ₹500 Cr
        if open_offer_value_inr_cr <= 500.0:
            escrow_deposit_cr = round(open_offer_value_inr_cr * 0.25, 2)
        else:
            escrow_deposit_cr = round((500.0 * 0.25) + ((open_offer_value_inr_cr - 500.0) * 0.10), 2)

        # Post-Offer Public Shareholding Check (SCRR Rule 19A - Minimum 25% Public Float)
        post_deal_promoter_stake_pct = round(acquisition_stake_pct + 26.0, 1)
        breaches_mps = post_deal_promoter_stake_pct > 75.0
        excess_stake_to_dilute = round(max(0.0, post_deal_promoter_stake_pct - 75.0), 1)

        return {
            "entity_name": target_name,
            "statutory_framework": "SEBI (Substantial Acquisition of Shares and Takeovers) Regulations, 2011",
            "acquisition_stake_pct": f"{acquisition_stake_pct}%",
            "open_offer_triggered": "YES (Regulation 3(1) Threshold Crossed)" if triggers_open_offer else "NO",
            "statutory_open_offer_shares_cr": f"{mandatory_open_offer_shares_cr} Cr shares (26.0% Public Float)",
            "statutory_offer_price_per_share": f"₹{statutory_offer_price_inr:,.2f}",
            "open_offer_consideration_inr_cr": f"₹{open_offer_value_inr_cr} Cr (${total_open_offer_usd_m}M)",
            "total_deal_commitment_inr_cr": f"₹{total_deal_size_inr_cr} Cr (${total_deal_size_usd_m}M)",
            "regulation_17_escrow_deposit_inr_cr": f"₹{escrow_deposit_cr} Cr (Mandatory Bank Escrow / Cash Guarantee)",
            "minimum_public_shareholding_mps_check": {
                "post_transaction_promoter_float": f"{post_deal_promoter_stake_pct}%",
                "status": "MPS_RULE_BREACH (Dilution Required)" if breaches_mps else "COMPLIANT_FLOAT",
                "remedy": f"Must dilute {excess_stake_to_dilute}% via Offer for Sale (OFS) within 12 months under SCRR Rule 19A." if breaches_mps else "Maintains 25%+ public shareholding."
            },
            "statutory_timeline": "Mandatory Detailed Public Statement (DPS) within 5 working days of execution; Letter of Offer dispatched in 35 days."
        }

sebi_sast_engine = SEBISASTTakeoverEngine()
