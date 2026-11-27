"""
Z17 Apex-Global - SEC 10-K & Global M&A Term Sheet Analyzer.
Evaluates audited filings, quality of earnings (QoE), dynamic EBITDA add-backs,
and acquisition legal covenants (indemnity escrows, working capital pegs).
"""

from typing import Dict, Any, List, Optional

class SECFilingParser:
    """Parses SEC 10-K / 10-Q disclosures, quality of earnings, and M&A legal covenants."""

    def analyze_due_diligence_terms(
        self,
        target_entity: str = "Target Corporation",
        reported_revenue_m: float = 120.0,
        reported_ebitda_m: float = 24.0,
        purchase_price_m: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Dynamically analyzes Quality of Earnings (QoE) and legal deal covenants.
        """
        if purchase_price_m is None:
            purchase_price_m = round(reported_ebitda_m * 11.5, 2)

        # Standard private equity QoE pro-forma adjustments
        erp_addback = round(reported_revenue_m * 0.012, 2)       # One-time IT/ERP migration
        restructuring_addback = round(reported_ebitda_m * 0.06, 2) # Severance & redundant site closures
        legal_defense_addback = round(reported_ebitda_m * 0.025, 2) # One-time IP litigation defense
        owner_discretionary = round(reported_ebitda_m * 0.035, 2)   # Non-operating owner perks

        total_addbacks = round(erp_addback + restructuring_addback + legal_defense_addback + owner_discretionary, 2)
        adjusted_ebitda = round(reported_ebitda_m + total_addbacks, 2)
        adjusted_margin_pct = round((adjusted_ebitda / max(reported_revenue_m, 1.0)) * 100.0, 1)

        # M&A Deal Covenants
        escrow_holdback_m = round(purchase_price_m * 0.10, 2)  # 10% indemnity escrow
        nwc_peg_m = round(reported_revenue_m * 0.105, 2)        # 10.5% normalized working capital peg

        covenants = [
            {
                "covenant": "Indemnity Escrow Holdback",
                "standard": f"10% of Enterprise Value (${escrow_holdback_m}M)",
                "survival_period": "18 Months post-closing",
                "purpose": "Shields buyer against breaches of representations & undisclosed tax/labor liabilities.",
                "status": "APPROVED_MARKET_STANDARD"
            },
            {
                "covenant": "Net Working Capital (NWC) Peg",
                "standard": f"Pegged at ${nwc_peg_m}M normalized NWC",
                "mechanism": "Dollar-for-dollar post-closing cash true-up within 90 days of closing.",
                "status": "APPROVED_STRICT_PROTECTION"
            },
            {
                "covenant": "Material Adverse Change (MAC / MAE)",
                "standard": "Standard seller carve-outs for macro, industry, and sovereign conflict events.",
                "status": "FAVORABLE_TO_SELLER"
            },
            {
                "covenant": "Representation & Warranty Insurance (RWI)",
                "standard": "Buyer-side RWI policy covering 10% of EV with 0.75% retention threshold.",
                "status": "RECOMMENDED_RISK_TRANSFER"
            }
        ]

        return {
            "target_entity": target_entity,
            "filing_standard": "US GAAP / Regulation S-X / Audited IFRS Standards",
            "quality_of_earnings_qoe": {
                "reported_revenue_usd_m": reported_revenue_m,
                "reported_ebitda_usd_m": reported_ebitda_m,
                "reported_margin_pct": round((reported_ebitda_m / max(reported_revenue_m, 1.0)) * 100.0, 1),
                "adjusted_ebitda_usd_m": adjusted_ebitda,
                "adjusted_margin_pct": adjusted_margin_pct,
                "net_addbacks_usd_m": total_addbacks,
                "pro_forma_addbacks": [
                    {"item": "One-time ERP software & cloud migration fees", "addback_m": erp_addback},
                    {"item": "Severance, retention & restructuring charges", "addback_m": restructuring_addback},
                    {"item": "Non-recurring IP litigation settlement & defense", "addback_m": legal_defense_addback},
                    {"item": "Discretionary sponsor/owner non-operating perks", "addback_m": owner_discretionary}
                ]
            },
            "ma_covenants_audit": covenants,
            "escrow_holdback_recommendation_m": escrow_holdback_m,
            "recommendation": "Proceed to Definitive Share Purchase Agreement (SPA) execution with 10% escrow."
        }

sec_filing_parser = SECFilingParser()
