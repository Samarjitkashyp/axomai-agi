"""
Z17 Apex-Global - Institutional DCF & LBO Financial Valuation Engine.
Computes 5-Year Unlevered Free Cash Flow (FCFF), WACC vs Terminal Growth sensitivity matrix,
and Private Equity LBO Debt Waterfall with multi-tranche paydown, cash sweeps, and IRR sensitivity.
"""

from typing import Dict, Any, List

class ValuationEngine:
    """Computes Wall Street-grade DCF and Private Equity LBO models with full debt waterfalls."""

    def compute_dcf_valuation(
        self,
        base_revenue_usd_m: float = 120.0,
        ebitda_margin_pct: float = 22.0,
        revenue_growth_pct: float = 14.0,
        wacc_pct: float = 9.5,
        terminal_growth_pct: float = 2.5,
        exit_multiple: float = 11.5,
        tax_rate_pct: float = 25.0,
        capex_pct_rev: float = 4.0,
        nwc_change_pct_rev: float = 1.5,
        net_debt_usd_m: float = 35.0,
        shares_outstanding_m: float = 20.0
    ) -> Dict[str, Any]:
        """
        Builds a comprehensive 5-Year Unlevered Free Cash Flow (FCFF) DCF Model
        with 2D WACC vs Terminal Growth Sensitivity Table.
        """
        wacc = wacc_pct / 100.0
        g = terminal_growth_pct / 100.0
        growth_rate = revenue_growth_pct / 100.0
        tax_rate = tax_rate_pct / 100.0

        projected_rev = []
        projected_ebitda = []
        projected_ebiat = []
        projected_fcf = []
        pv_fcf = []

        curr_rev = base_revenue_usd_m
        for yr in range(1, 6):
            curr_rev *= (1 + growth_rate)
            ebitda = curr_rev * (ebitda_margin_pct / 100.0)
            # D&A assumed ~ 3.5% of revenue
            dna = curr_rev * 0.035
            ebit = max(0.0, ebitda - dna)
            ebiat = ebit * (1.0 - tax_rate)
            capex = curr_rev * (capex_pct_rev / 100.0)
            delta_nwc = curr_rev * (nwc_change_pct_rev / 100.0)
            
            # Unlevered Free Cash Flow = EBIAT + D&A - CapEx - Delta NWC
            fcf = round(ebiat + dna - capex - delta_nwc, 2)
            discount_factor = 1.0 / ((1.0 + wacc) ** yr)
            pv = round(fcf * discount_factor, 2)

            projected_rev.append(round(curr_rev, 2))
            projected_ebitda.append(round(ebitda, 2))
            projected_ebiat.append(round(ebiat, 2))
            projected_fcf.append(fcf)
            pv_fcf.append(pv)

        sum_pv_fcf = round(sum(pv_fcf), 2)

        # Gordon Growth Terminal Value: TV = FCF_5 * (1 + g) / (WACC - g)
        fcf_terminal = projected_fcf[-1] * (1.0 + g)
        terminal_value_gordon = round(fcf_terminal / max(wacc - g, 0.005), 2)
        pv_terminal_gordon = round(terminal_value_gordon / ((1.0 + wacc) ** 5), 2)

        # Exit Multiple Terminal Value: TV = EBITDA_5 * Exit Multiple
        terminal_value_multiple = round(projected_ebitda[-1] * exit_multiple, 2)
        pv_terminal_multiple = round(terminal_value_multiple / ((1.0 + wacc) ** 5), 2)

        enterprise_value_gordon = round(sum_pv_fcf + pv_terminal_gordon, 2)
        equity_value_gordon = round(enterprise_value_gordon - net_debt_usd_m, 2)
        implied_share_price_gordon = round(equity_value_gordon / max(shares_outstanding_m, 1.0), 2)

        enterprise_value_multiple = round(sum_pv_fcf + pv_terminal_multiple, 2)
        equity_value_multiple = round(enterprise_value_multiple - net_debt_usd_m, 2)
        implied_share_price_multiple = round(equity_value_multiple / max(shares_outstanding_m, 1.0), 2)

        # 5x5 WACC vs Terminal Growth Sensitivity Matrix
        wacc_spread = [round(wacc_pct - 1.0, 1), round(wacc_pct - 0.5, 1), wacc_pct, round(wacc_pct + 0.5, 1), round(wacc_pct + 1.0, 1)]
        g_spread = [round(terminal_growth_pct - 0.5, 1), terminal_growth_pct, round(terminal_growth_pct + 0.5, 1)]
        
        sensitivity_matrix = {}
        for w in wacc_spread:
            row = {}
            for tg in g_spread:
                w_dec = w / 100.0
                g_dec = tg / 100.0
                if w_dec > g_dec:
                    pv_t = (projected_fcf[-1] * (1.0 + g_dec) / (w_dec - g_dec)) / ((1.0 + w_dec) ** 5)
                    sum_pv = sum(projected_fcf[i] / ((1.0 + w_dec) ** (i + 1)) for i in range(5))
                    ev = round(sum_pv + pv_t, 1)
                    row[f"g_{tg}%"] = f"${ev}M"
                else:
                    row[f"g_{tg}%"] = "N/A"
            sensitivity_matrix[f"wacc_{w}%"] = row

        return {
            "wacc_pct": wacc_pct,
            "terminal_growth_pct": terminal_growth_pct,
            "forecast_years": ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
            "projected_revenue_m": projected_rev,
            "projected_ebitda_m": projected_ebitda,
            "projected_fcf_m": projected_fcf,
            "pv_fcf_5yr_usd_m": sum_pv_fcf,
            "gordon_growth_method": {
                "terminal_value_usd_m": terminal_value_gordon,
                "pv_terminal_value_usd_m": pv_terminal_gordon,
                "enterprise_value_usd_m": enterprise_value_gordon,
                "implied_equity_value_usd_m": equity_value_gordon,
                "implied_share_price_usd": implied_share_price_gordon
            },
            "exit_multiple_method": {
                "exit_multiple": f"{exit_multiple}x",
                "terminal_value_usd_m": terminal_value_multiple,
                "pv_terminal_value_usd_m": pv_terminal_multiple,
                "enterprise_value_usd_m": enterprise_value_multiple,
                "implied_equity_value_usd_m": equity_value_multiple,
                "implied_share_price_usd": implied_share_price_multiple
            },
            "net_debt_usd_m": net_debt_usd_m,
            "sensitivity_matrix_wacc_vs_g": sensitivity_matrix
        }

    def compute_lbo_returns(
        self,
        entry_enterprise_value_m: float = 300.0,
        entry_ebitda_m: float = 26.0,
        senior_debt_pct: float = 45.0,
        sub_debt_pct: float = 15.0,
        senior_interest_rate_pct: float = 6.5,
        sub_interest_rate_pct: float = 9.5,
        ebitda_growth_pct: float = 10.0,
        exit_multiple: float = 11.5,
        fcf_cash_sweep_pct: float = 75.0
    ) -> Dict[str, Any]:
        """
        Full 5-Year Private Equity LBO Debt Waterfall and Return Model.
        Tracks senior & subordinated debt tranches, interest amortization, cash sweep, MOIC & IRR.
        """
        total_debt_pct = senior_debt_pct + sub_debt_pct
        sponsor_equity_pct = 100.0 - total_debt_pct

        senior_debt_entry = round(entry_enterprise_value_m * (senior_debt_pct / 100.0), 2)
        sub_debt_entry = round(entry_enterprise_value_m * (sub_debt_pct / 100.0), 2)
        total_debt_entry = round(senior_debt_entry + sub_debt_entry, 2)
        sponsor_equity_entry = round(entry_enterprise_value_m * (sponsor_equity_pct / 100.0), 2)

        entry_leverage = round(total_debt_entry / max(entry_ebitda_m, 1.0), 2)

        # 5-Year Debt Waterfall
        senior_balance = senior_debt_entry
        sub_balance = sub_debt_entry
        curr_ebitda = entry_ebitda_m
        
        cumulative_interest = 0.0
        annual_debt_schedule = []

        for yr in range(1, 6):
            curr_ebitda *= (1 + (ebitda_growth_pct / 100.0))
            
            # Annual Interest
            senior_interest = senior_balance * (senior_interest_rate_pct / 100.0)
            sub_interest = sub_balance * (sub_interest_rate_pct / 100.0)
            total_interest = senior_interest + sub_interest
            cumulative_interest += total_interest

            # FCF Available for Debt Paydown (~50% of EBITDA after tax and capex)
            fcf_available = max(0.0, (curr_ebitda * 0.52) - total_interest)
            
            # Mandatory 5% senior debt amortization
            mand_amort = min(senior_balance, senior_debt_entry * 0.05)
            senior_balance -= mand_amort

            # Excess cash sweep towards Senior Debt first
            sweep_cash = fcf_available * (fcf_cash_sweep_pct / 100.0)
            senior_sweep = min(senior_balance, sweep_cash)
            senior_balance -= senior_sweep

            annual_debt_schedule.append({
                "year": f"Year {yr}",
                "ebitda": round(curr_ebitda, 2),
                "senior_debt_ending": round(senior_balance, 2),
                "sub_debt_ending": round(sub_balance, 2),
                "total_debt_ending": round(senior_balance + sub_balance, 2)
            })

        exit_ebitda = curr_ebitda
        exit_enterprise_value = round(exit_ebitda * exit_multiple, 2)
        ending_total_debt = round(senior_balance + sub_balance, 2)
        sponsor_exit_equity = round(exit_enterprise_value - ending_total_debt, 2)

        moic = round(sponsor_exit_equity / max(sponsor_equity_entry, 1.0), 2)
        irr_pct = round(((moic ** (1 / 5.0)) - 1) * 100.0, 2) if moic > 0 else 0.0
        exit_leverage = round(ending_total_debt / max(exit_ebitda, 1.0), 2)

        # 3x3 Exit Multiple vs Growth Sensitivity
        sens_multiples = [exit_multiple - 1.5, exit_multiple, exit_multiple + 1.5]
        irr_sensitivity = {}
        for m in sens_multiples:
            ev_sens = exit_ebitda * m
            eq_sens = ev_sens - ending_total_debt
            sens_moic = round(eq_sens / max(sponsor_equity_entry, 1.0), 2)
            sens_irr = round(((sens_moic ** (1 / 5.0)) - 1) * 100.0, 2) if sens_moic > 0 else 0.0
            irr_sensitivity[f"exit_{m:.1f}x"] = f"{sens_irr}% IRR ({sens_moic}x MOIC)"

        return {
            "entry_enterprise_value_m": entry_enterprise_value_m,
            "entry_ebitda_m": entry_ebitda_m,
            "entry_leverage_debt_to_ebitda": f"{entry_leverage}x",
            "sources_and_uses": {
                "senior_debt_entry_m": senior_debt_entry,
                "sub_debt_entry_m": sub_debt_entry,
                "total_debt_entry_m": total_debt_entry,
                "sponsor_equity_entry_m": sponsor_equity_entry,
                "equity_contribution_pct": f"{sponsor_equity_pct}%"
            },
            "debt_schedule_5yr": annual_debt_schedule,
            "exit_ebitda_y5_m": round(exit_ebitda, 2),
            "exit_multiple": f"{exit_multiple}x",
            "exit_enterprise_value_m": exit_enterprise_value,
            "ending_debt_m": ending_total_debt,
            "debt_paid_down_m": round(total_debt_entry - ending_total_debt, 2),
            "sponsor_exit_equity_m": sponsor_exit_equity,
            "multiple_on_invested_capital_moic": moic,
            "target_irr_pct": irr_pct,
            "exit_leverage_debt_to_ebitda": f"{exit_leverage}x",
            "irr_sensitivity_table": irr_sensitivity,
            "underwriting_verdict": "STRONG_BUY_OPPORTUNITY" if irr_pct >= 22.0 else ("SELECTIVE_BUY" if irr_pct >= 18.0 else "BELOW_HURDLE_RATE")
        }

valuation_engine = ValuationEngine()
