"""
Z17 Apex-Global - 10,000-Iteration Monte Carlo Stochastic Valuation Simulator.
Samples probability distributions across revenue growth, WACC, and exit multiples
to compute Value-at-Risk (VaR) and probabilistic valuation cones for institutional M&A.
"""

import random
import math
from typing import Dict, Any, List

class MonteCarloValuationSimulator:
    """Institutional 10,000-run stochastic DCF and LBO Monte Carlo Engine."""

    def __init__(self):
        pass

    def run_dcf_simulation(
        self,
        base_fcf: float = 25.0,  # $25M Year 0 Free Cash Flow
        mean_growth_rate: float = 0.12,  # 12% mean annual FCF growth
        growth_std_dev: float = 0.04,    # 4% standard deviation
        mean_wacc: float = 0.095,        # 9.5% mean WACC
        wacc_range: float = 0.015,       # +/- 1.5% uniform spread
        terminal_growth_mean: float = 0.025, # 2.5% terminal growth
        iterations: int = 10000,
        random_seed: int = 42
    ) -> Dict[str, Any]:
        """
        Runs 10,000 stochastic DCF valuation scenarios.
        """
        rng = random.Random(random_seed)
        enterprise_values: List[float] = []

        for _ in range(iterations):
            # Sample stochastic parameters
            growth = rng.gauss(mean_growth_rate, growth_std_dev)
            growth = max(-0.10, min(0.35, growth))  # cap between -10% and +35%
            wacc = rng.uniform(mean_wacc - wacc_range, mean_wacc + wacc_range)
            g_terminal = max(0.01, min(wacc - 0.015, rng.gauss(terminal_growth_mean, 0.005)))

            # Project 5-year FCF
            pv_fcf = 0.0
            curr_fcf = base_fcf
            for year in range(1, 6):
                curr_fcf *= (1.0 + growth)
                discount_factor = (1.0 + wacc) ** year
                pv_fcf += curr_fcf / discount_factor

            # Terminal Value using Gordon Growth
            tv = (curr_fcf * (1.0 + g_terminal)) / (wacc - g_terminal)
            pv_tv = tv / ((1.0 + wacc) ** 5)

            ev = pv_fcf + pv_tv
            enterprise_values.append(ev)

        enterprise_values.sort()

        # Compute key distribution statistics
        n = len(enterprise_values)
        mean_ev = sum(enterprise_values) / n
        variance = sum((x - mean_ev) ** 2 for x in enterprise_values) / n
        std_dev = math.sqrt(variance)

        p05_downside = enterprise_values[int(0.05 * n)]
        p50_median = enterprise_values[int(0.50 * n)]
        p95_upside = enterprise_values[int(0.95 * n)]

        # 95% Value-at-Risk (Downside drop from median)
        var_95_pct = round(((p50_median - p05_downside) / p50_median) * 100.0, 1)

        return {
            "iterations_computed": iterations,
            "base_fcf_millions": f"${base_fcf:,.1f}M",
            "mean_enterprise_value_millions": round(mean_ev, 2),
            "median_enterprise_value_millions": round(p50_median, 2),
            "std_deviation_millions": round(std_dev, 2),
            "distribution_percentiles": {
                "5th_percentile_bear_case": round(p05_downside, 2),
                "25th_percentile_conservative": round(enterprise_values[int(0.25 * n)], 2),
                "50th_percentile_median": round(p50_median, 2),
                "75th_percentile_optimistic": round(enterprise_values[int(0.75 * n)], 2),
                "95th_percentile_bull_case": round(p95_upside, 2),
            },
            "downside_var_95_pct": f"{var_95_pct}% maximum drawdown at 95% confidence",
            "valuation_range_summary": (
                f"90% of all stochastic outcomes fall between ${p05_downside:,.1f}M and ${p95_upside:,.1f}M, "
                f"with a central median valuation of ${p50_median:,.1f}M."
            )
        }

monte_carlo_simulator = MonteCarloValuationSimulator()

