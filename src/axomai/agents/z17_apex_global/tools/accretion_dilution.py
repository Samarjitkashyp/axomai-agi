"""
Z17 Apex-Global - Public M&A Pro Forma EPS Accretion & Dilution Engine.
Computes pro forma earnings per share (EPS) impact, consideration mix (cash/debt/stock),
transaction financing costs, after-tax synergies, and break-even synergy hurdles.
"""

from typing import Dict, Any, Optional

class AccretionDilutionEngine:
    """Institutional Public M&A EPS Accretion / Dilution Analyzer."""

    def evaluate_merger_impact(
        self,
        acquirer_name: str = "Acquirer Corp",
        target_name: str = "Target Corp",
        acquirer_share_price: float = 120.0,
        acquirer_shares_out_m: float = 250.0,
        acquirer_net_income_m: float = 1800.0,
        target_share_price: float = 45.0,
        target_shares_out_m: float = 60.0,
        target_net_income_m: float = 180.0,
        offer_premium_pct: float = 25.0,
        cash_pct: float = 50.0,
        stock_pct: float = 50.0,
        debt_interest_rate_pct: float = 6.5,
        pre_tax_synergies_m: float = 45.0,
        tax_rate_pct: float = 25.0
    ) -> Dict[str, Any]:
        """
        Calculates post-merger EPS accretion/dilution across consideration tranches.
        """
        # Standalone metrics
        acquirer_standalone_eps = round(acquirer_net_income_m / acquirer_shares_out_m, 2)
        target_standalone_eps = round(target_net_income_m / target_shares_out_m, 2)
        
        # Offer price & transaction equity value
        offer_price_per_share = round(target_share_price * (1 + (offer_premium_pct / 100.0)), 2)
        transaction_equity_value_m = round(offer_price_per_share * target_shares_out_m, 2)

        # Consideration breakdown
        cash_consideration_m = round(transaction_equity_value_m * (cash_pct / 100.0), 2)
        stock_consideration_m = round(transaction_equity_value_m * (stock_pct / 100.0), 2)

        # New acquirer shares issued
        new_shares_issued_m = round(stock_consideration_m / acquirer_share_price, 2)
        pro_forma_shares_out_m = round(acquirer_shares_out_m + new_shares_issued_m, 2)

        # Financing cost (incremental interest expense on debt/cash used)
        pre_tax_interest_expense_m = round(cash_consideration_m * (debt_interest_rate_pct / 100.0), 2)
        after_tax_interest_expense_m = round(pre_tax_interest_expense_m * (1 - (tax_rate_pct / 100.0)), 2)

        # After-tax synergies
        after_tax_synergies_m = round(pre_tax_synergies_m * (1 - (tax_rate_pct / 100.0)), 2)

        # Pro Forma Net Income
        pro_forma_net_income_m = round(
            acquirer_net_income_m + target_net_income_m + after_tax_synergies_m - after_tax_interest_expense_m,
            2
        )

        # Pro Forma EPS
        pro_forma_eps = round(pro_forma_net_income_m / pro_forma_shares_out_m, 2)
        eps_change_dollars = round(pro_forma_eps - acquirer_standalone_eps, 2)
        eps_change_pct = round(((pro_forma_eps - acquirer_standalone_eps) / acquirer_standalone_eps) * 100.0, 2)

        is_accretive = eps_change_pct >= 0.0

        # Break-even pre-tax synergies if dilutive without synergies
        net_inc_without_synergies = acquirer_net_income_m + target_net_income_m - after_tax_interest_expense_m
        target_ni_needed_for_neutral = (acquirer_standalone_eps * pro_forma_shares_out_m)
        shortfall = max(0.0, target_ni_needed_for_neutral - net_inc_without_synergies)
        breakeven_pretax_synergies_m = round(shortfall / (1 - (tax_rate_pct / 100.0)), 2)

        return {
            "acquirer": acquirer_name,
            "target": target_name,
            "acquirer_standalone_eps": f"${acquirer_standalone_eps:,.2f}",
            "target_standalone_eps": f"${target_standalone_eps:,.2f}",
            "offer_price_per_share": f"${offer_price_per_share:,.2f} ({offer_premium_pct}% premium)",
            "transaction_equity_value_m": f"${transaction_equity_value_m:,.1f}M",
            "consideration_mix": {
                "cash_funded_m": f"${cash_consideration_m:,.1f}M ({cash_pct}%)",
                "stock_funded_m": f"${stock_consideration_m:,.1f}M ({stock_pct}%)",
                "new_shares_issued_m": f"{new_shares_issued_m:,.1f}M shares"
            },
            "pro_forma_shares_out_m": f"{pro_forma_shares_out_m:,.1f}M",
            "after_tax_synergies_m": f"${after_tax_synergies_m:,.1f}M",
            "after_tax_interest_cost_m": f"${after_tax_interest_expense_m:,.1f}M",
            "pro_forma_net_income_m": f"${pro_forma_net_income_m:,.1f}M",
            "pro_forma_eps": f"${pro_forma_eps:,.2f}",
            "accretion_dilution_dollars": f"{'+' if eps_change_dollars >= 0 else ''}${eps_change_dollars:,.2f}",
            "accretion_dilution_pct": f"{'+' if eps_change_pct >= 0 else ''}{eps_change_pct:.2f}%",
            "deal_verdict": "ACCRETIVE_TRANSACTION" if is_accretive else "DILUTIVE_TRANSACTION",
            "breakeven_pretax_synergies_m": f"${breakeven_pretax_synergies_m:,.1f}M"
        }

accretion_dilution_engine = AccretionDilutionEngine()
