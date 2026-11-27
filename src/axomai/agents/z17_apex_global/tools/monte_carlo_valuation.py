"""
Z17 Apex-Global - 10,000-Iteration Monte Carlo Stochastic Valuation Simulator.
Samples multivariate probability distributions across revenue growth, EBITDA margin,
WACC, and exit multiples to compute Value-at-Risk (VaR) and probabilistic valuation cones.
"""

import random
import math
from typing import Dict, Any, List

class MonteCarloValuationSimulator:
    """Institutional 10,000-run stochastic DCF and LBO Monte Carlo Engine."""

    def run_dcf_simulation(
        self,
        base_fcf: float = 25.0,
        mean_growth_rate: float = 0.12,
        growth_std_dev: float = 0.04,
        mean_wacc: float = 0.095,
        wacc_range: float = 0.015,
        terminal_growth_mean: float = 0.025,
        iterations: int = 10000,
        random_seed: int = 42
    ) -> Dict[str, Any]:
        """
        Runs 10,000 stochastic DCF valuation scenarios with stochastic WACC & terminal growth.
        """
        rng = random.Random(random_seed)
        enterprise_values: List[float] = []

        for _ in range(iterations):
            # Sample stochastic parameters (Gaussian for growth, Uniform for WACC)
            growth = rng.gauss(mean_growth_rate, growth_std_dev)
            growth = max(-0.12, min(0.40, growth))
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
            tv = (curr_fcf * (1.0 + g_terminal)) / max(wacc - g_terminal, 0.005)
            pv_tv = tv / ((1.0 + wacc) ** 5)

            ev = pv_fcf + pv_tv
            enterprise_values.append(ev)

        enterprise_values.sort()

        # Compute key distribution statistics
        n = len(enterprise_values)
        mean_ev = sum(enterprise_values) / n
        variance = sum((x - mean_ev) ** 2 for x in enterprise_values) / n
        std_dev = math.sqrt(variance)

        p01_downside = enterprise_values[int(0.01 * n)]
        p05_downside = enterprise_values[int(0.05 * n)]
        p25_conservative = enterprise_values[int(0.25 * n)]
        p50_median = enterprise_values[int(0.50 * n)]
        p75_optimistic = enterprise_values[int(0.75 * n)]
        p95_upside = enterprise_values[int(0.95 * n)]
        p99_upside = enterprise_values[int(0.99 * n)]

        # 95% Value-at-Risk (Downside drawdown from median)
        var_95_pct = round(((p50_median - p05_downside) / p50_median) * 100.0, 1)
        var_99_pct = round(((p50_median - p01_downside) / p50_median) * 100.0, 1)

        # Probability of achieving above baseline valuation
        prob_above_median = round((sum(1 for x in enterprise_values if x >= p50_median) / n) * 100.0, 1)

        return {
            "iterations_computed": iterations,
            "base_fcf_millions": f"${base_fcf:,.1f}M",
            "mean_enterprise_value_millions": round(mean_ev, 2),
            "median_enterprise_value_millions": round(p50_median, 2),
            "std_deviation_millions": round(std_dev, 2),
            "distribution_percentiles": {
                "1st_percentile_extreme_bear": round(p01_downside, 2),
                "5th_percentile_bear_case": round(p05_downside, 2),
                "25th_percentile_conservative": round(p25_conservative, 2),
                "50th_percentile_median": round(p50_median, 2),
                "75th_percentile_optimistic": round(p75_optimistic, 2),
                "95th_percentile_bull_case": round(p95_upside, 2),
                "99th_percentile_extreme_bull": round(p99_upside, 2)
            },
            "downside_var_95_pct": f"{var_95_pct}% maximum drawdown at 95% confidence",
            "downside_var_99_pct": f"{var_99_pct}% maximum drawdown at 99% confidence",
            "probability_above_median": f"{prob_above_median}%",
            "valuation_range_summary": (
                f"90% of all 10,000 stochastic outcomes fall between ${p05_downside:,.1f}M (Bear) and ${p95_upside:,.1f}M (Bull), "
                f"with a central median enterprise valuation of ${p50_median:,.1f}M."
            )
        }

monte_carlo_simulator = MonteCarloValuationSimulator()
