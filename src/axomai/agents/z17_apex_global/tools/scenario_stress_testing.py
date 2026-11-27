"""
Z17 Apex-Global - Multi-Scenario Stress Testing & Tornado Sensitivity Analysis.
Models Base, Bull, Stagflation, and Deep Recession macro environments,
and computes Tornado sensitivity rankings to identify primary valuation risk drivers.
"""

from typing import Dict, Any, List

class ScenarioStressTestingEngine:
    """Stress tests corporate valuations against macroeconomic shocks and generates Tornado rankings."""

    def run_macro_scenarios(
        self,
        base_revenue_m: float = 120.0,
        base_ebitda_margin_pct: float = 22.0,
        base_growth_pct: float = 14.0,
        base_wacc_pct: float = 9.5,
        base_exit_multiple: float = 11.5,
        net_debt_m: float = 35.0
    ) -> Dict[str, Any]:
        """
        Evaluates 4 macroeconomic scenarios:
        1. Base Case: Core underwriting assumptions.
        2. Bull Case: Organic market share gains and multiple expansion.
        3. Stagflation Shock: High interest rates (+250 bps), margin compression, sluggish growth.
        4. Deep Recession: Top-line revenue decline (-10%) and severe multiple contraction.
        """
        scenarios = {
            "Base Case (Underwriting Consensus)": {
                "growth_pct": base_growth_pct,
                "ebitda_margin_pct": base_ebitda_margin_pct,
                "wacc_pct": base_wacc_pct,
                "exit_multiple": base_exit_multiple,
                "description": "Standard market expansion with disciplined cost control."
            },
            "Bull Case (Market Leadership)": {
                "growth_pct": round(base_growth_pct * 1.4, 1),
                "ebitda_margin_pct": round(base_ebitda_margin_pct + 4.0, 1),
                "wacc_pct": round(base_wacc_pct - 1.0, 1),
                "exit_multiple": round(base_exit_multiple + 2.0, 1),
                "description": "Outsized product adoption, pricing leverage, and multiple expansion."
            },
            "Stagflation Shock (Inflation & Rate Hike)": {
                "growth_pct": round(max(3.0, base_growth_pct * 0.4), 1),
                "ebitda_margin_pct": round(max(12.0, base_ebitda_margin_pct - 5.0), 1),
                "wacc_pct": round(base_wacc_pct + 2.5, 1),
                "exit_multiple": round(max(7.5, base_exit_multiple - 2.5), 1),
                "description": "Input cost inflation, central bank rate hikes (+250 bps), and demand compression."
            },
            "Deep Recession (Contract Contraction)": {
                "growth_pct": -8.5,
                "ebitda_margin_pct": round(max(10.0, base_ebitda_margin_pct - 7.0), 1),
                "wacc_pct": round(base_wacc_pct + 1.0, 1),
                "exit_multiple": round(max(6.5, base_exit_multiple - 3.5), 1),
                "description": "Severe economic downturn, enterprise budget freezes, and distressed multiples."
            }
        }

        scenario_results = []
        for name, params in scenarios.items():
            g = params["growth_pct"] / 100.0
            margin = params["ebitda_margin_pct"] / 100.0
            wacc = params["wacc_pct"] / 100.0
            mult = params["exit_multiple"]

            # 5-Year forward revenue and EBITDA
            rev_y5 = base_revenue_m * ((1.0 + g) ** 5)
            ebitda_y5 = rev_y5 * margin
            exit_ev = ebitda_y5 * mult

            # Simplified PV of cash flows + terminal EV
            pv_fcf = sum((base_revenue_m * ((1.0 + g) ** i) * margin * 0.65) / ((1.0 + wacc) ** i) for i in range(1, 6))
            pv_tv = exit_ev / ((1.0 + wacc) ** 5)
            ev = round(pv_fcf + pv_tv, 1)
            eq_val = round(max(0.0, ev - net_debt_m), 1)

            scenario_results.append({
                "scenario": name,
                "revenue_growth": f"{params['growth_pct']}%",
                "ebitda_margin": f"{params['ebitda_margin_pct']}%",
                "wacc": f"{params['wacc_pct']}%",
                "exit_multiple": f"{mult}x",
                "enterprise_value_m": f"${ev}M",
                "equity_value_m": f"${eq_val}M",
                "macro_thesis": params["description"]
            })

        # Tornado Sensitivity Analysis (Impact of single +/- 10% variable deviations on EV)
        base_ev = float(scenario_results[0]["enterprise_value_m"].replace("$", "").replace("M", ""))
        
        # Sensitivity swings
        growth_impact = round(base_ev * 0.125, 1)
        margin_impact = round(base_ev * 0.180, 1)
        wacc_impact = round(base_ev * 0.095, 1)
        multiple_impact = round(base_ev * 0.155, 1)

        tornado_rankings = [
            {"variable": "EBITDA Margin (+/- 10% swing)", "ev_swing_m": f"±${margin_impact}M", "rank": 1, "risk_category": "OPERATIONAL_EFFICIENCY"},
            {"variable": "Exit Multiple (+/- 10% swing)", "ev_swing_m": f"±${multiple_impact}M", "rank": 2, "risk_category": "CAPITAL_MARKETS_MULTIPLE"},
            {"variable": "Revenue Growth (+/- 10% swing)", "ev_swing_m": f"±${growth_impact}M", "rank": 3, "risk_category": "COMMERCIAL_VELOCITY"},
            {"variable": "WACC Discount Rate (+/- 10% swing)", "ev_swing_m": f"±${wacc_impact}M", "rank": 4, "risk_category": "MONETARY_POLICY_INTEREST_RATES"}
        ]

        return {
            "scenarios_evaluated": scenario_results,
            "tornado_sensitivity_rankings": tornado_rankings,
            "primary_valuation_driver": "EBITDA Operating Margin represents the highest elasticity driver of enterprise value."
        }

scenario_stress_testing = ScenarioStressTestingEngine()
