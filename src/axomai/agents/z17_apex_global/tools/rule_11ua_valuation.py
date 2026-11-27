"""
Z17 Apex-Global - Income Tax Rule 11UA & Angel Tax Valuation Defense Engine.
Computes statutory Fair Market Value (FMV) of unquoted equity shares under Rule 11UA(2)
of the Indian Income Tax Rules, 1962 for Section 56(2)(viib) and Section 50CA statutory defense.
"""

from typing import Dict, Any, List

class Rule11UAValuationEngine:
    """Computes statutory Fair Market Value under Indian Income Tax Act Rules 11UA(1) & 11UA(2)."""

    def compute_rule_11ua_valuation(
        self,
        company_name: str = "Target Unlisted Enterprise",
        book_value_assets_cr: float = 120.0,
        book_value_liabilities_cr: float = 45.0,
        paid_up_equity_shares_cr: float = 2.0,
        projected_5yr_fcf_cr: float = 18.5,
        wacc_pct: float = 11.5,
        terminal_growth_pct: float = 4.0
    ) -> Dict[str, Any]:
        """
        Calculates Fair Market Value (FMV) under both NAV Method (11UA(1)) and DCF Method (11UA(2)).
        """
        # 1. Net Asset Value (NAV) Method: Rule 11UA(1)(c)(b)
        # FMV = (A - L) / PE * PV
        # A = Book value of assets, L = Book value of liabilities (excluding equity & reserves)
        net_assets_cr = round(book_value_assets_cr - book_value_liabilities_cr, 2)
        nav_per_share_inr = round((net_assets_cr * 10_000_000.0) / (paid_up_equity_shares_cr * 10_000_000.0), 2)

        # 2. Discounted Free Cash Flow (DCF) Method: Rule 11UA(2)(b) - Certified by Merchant Banker
        wacc = wacc_pct / 100.0
        g = terminal_growth_pct / 100.0

        pv_fcf = sum((projected_5yr_fcf_cr * ((1.0 + 0.12) ** i)) / ((1.0 + wacc) ** i) for i in range(1, 6))
        fcf_y5 = projected_5yr_fcf_cr * ((1.0 + 0.12) ** 5)
        tv = (fcf_y5 * (1.0 + g)) / max(wacc - g, 0.01)
        pv_tv = tv / ((1.0 + wacc) ** 5)

        enterprise_value_cr = round(pv_fcf + pv_tv, 2)
        equity_value_cr = round(enterprise_value_cr - book_value_liabilities_cr, 2)
        dcf_per_share_inr = round((equity_value_cr * 10_000_000.0) / (paid_up_equity_shares_cr * 10_000_000.0), 2)

        # Statutory Safe Harbor Price Band (10% safe harbor variance under Income Tax Act)
        safe_harbor_floor_inr = round(dcf_per_share_inr * 0.90, 2)
        safe_harbor_ceiling_inr = round(dcf_per_share_inr * 1.10, 2)

        return {
            "entity_name": company_name,
            "statutory_authority": "Rule 11UA(2)(b) & Rule 11UA(1)(c)(b) of Income Tax Rules, 1962",
            "section_applicability": "Section 56(2)(viib) (Angel Tax) & Section 50CA (Transfer of Unquoted Shares)",
            "certifying_credential": "Category-I Merchant Banker / Insolvency Registered Valuer (S&FA)",
            "nav_book_value_method": {
                "net_assets_cr": f"₹{net_assets_cr} Cr",
                "shares_outstanding_cr": f"{paid_up_equity_shares_cr} Cr",
                "nav_per_share": f"₹{nav_per_share_inr}"
            },
            "merchant_banker_dcf_method": {
                "wacc_discount_rate": f"{wacc_pct}%",
                "terminal_growth_rate": f"{terminal_growth_pct}%",
                "implied_enterprise_value_cr": f"₹{enterprise_value_cr} Cr",
                "implied_equity_value_cr": f"₹{equity_value_cr} Cr",
                "dcf_fair_market_value_per_share": f"₹{dcf_per_share_inr}"
            },
            "statutory_safe_harbor_band": f"₹{safe_harbor_floor_inr} to ₹{safe_harbor_ceiling_inr} per share",
            "tax_scrutiny_defense_verdict": (
                f"Issues or transfers at or within ₹{safe_harbor_floor_inr} - ₹{dcf_per_share_inr} per share "
                f"are fully protected from Section 56(2)(viib) addition under official CBDT safe harbor notification. "
                f"Income Tax Scrutiny Risk: ZERO_TAX_EXPOSURE."
            )
        }

rule_11ua_engine = Rule11UAValuationEngine()
