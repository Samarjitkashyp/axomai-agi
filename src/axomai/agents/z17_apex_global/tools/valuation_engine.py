"""
Z17 Apex-Global - Institutional DCF & LBO Financial Valuation Engine.
Computes WACC, 5-Year Unlevered Free Cash Flow (FCFF), Terminal Value, and LBO returns.
"""

from typing import Dict, Any, List

class ValuationEngine:
    """Computes Wall Street-grade DCF and Private Equity LBO models."""

    def compute_dcf_valuation(
        self,
        base_fcf_usd_m: float = 25.0,
        revenue_growth_pct: float = 12.0,
        wacc_pct: float = 9.5,
        terminal_growth_pct: float = 2.5,
        net_debt_usd_m: float = 15.0,
        shares_outstanding_m: float = 10.0
    ) -> Dict[str, Any]:
        wacc = wacc_pct / 100.0
        g = terminal_growth_pct / 100.0
        growth_rate = revenue_growth_pct / 100.0

        projected_fcf = []
        pv_fcf = []
        curr_fcf = base_fcf_usd_m

        for yr in range(1, 6):
            curr_fcf = curr_fcf * (1 + growth_rate)
            projected_fcf.append(round(curr_fcf, 2))
            discount_factor = 1 / ((1 + wacc) ** yr)
            pv_fcf.append(round(curr_fcf * discount_factor, 2))

        sum_pv_fcf = sum(pv_fcf)

        # Terminal Value: TV = FCF_5 * (1 + g) / (WACC - g)
        fcf_terminal = projected_fcf[-1] * (1 + g)
        terminal_value = fcf_terminal / (wacc - g)
        pv_terminal_value = terminal_value / ((1 + wacc) ** 5)

        enterprise_value = round(sum_pv_fcf + pv_terminal_value, 2)
        equity_value = round(enterprise_value - net_debt_usd_m, 2)
        implied_share_price = round(equity_value / shares_outstanding_m, 2)

        return {
            "wacc_pct": wacc_pct,
            "terminal_growth_pct": terminal_growth_pct,
            "projected_fcf_5yr_usd_m": projected_fcf,
            "pv_fcf_5yr_usd_m": round(sum_pv_fcf, 2),
            "terminal_value_usd_m": round(terminal_value, 2),
            "pv_terminal_value_usd_m": round(pv_terminal_value, 2),
            "enterprise_value_usd_m": enterprise_value,
            "net_debt_usd_m": net_debt_usd_m,
            "implied_equity_value_usd_m": equity_value,
            "implied_share_price_usd": implied_share_price
        }

    def compute_lbo_returns(
        self,
        entry_enterprise_value_m: float = 150.0,
        debt_financing_pct: float = 60.0,
        exit_multiple: float = 11.5,
        target_ebitda_y5_m: float = 24.0
    ) -> Dict[str, Any]:
        sponsor_equity_entry = entry_enterprise_value_m * (1 - (debt_financing_pct / 100.0))
        exit_ev = target_ebitda_y5_m * exit_multiple
        # Assume 70% of initial debt paid down by Year 5
        remaining_debt = (entry_enterprise_value_m * (debt_financing_pct / 100.0)) * 0.30
        sponsor_equity_exit = exit_ev - remaining_debt

        moic = round(sponsor_equity_exit / sponsor_equity_entry, 2)
        irr_pct = round(((moic ** (1 / 5.0)) - 1) * 100, 2)

        return {
            "entry_ev_usd_m": entry_enterprise_value_m,
            "sponsor_initial_equity_usd_m": round(sponsor_equity_entry, 2),
            "exit_ev_usd_m": round(exit_ev, 2),
            "sponsor_exit_equity_usd_m": round(sponsor_equity_exit, 2),
            "multiple_on_invested_capital_moic": moic,
            "target_irr_pct": irr_pct,
            "underwriting_verdict": "STRONG_BUY_OPPORTUNITY" if irr_pct >= 20.0 else "TARGET_BELOW_HURDLE_RATE"
        }

valuation_engine = ValuationEngine()

