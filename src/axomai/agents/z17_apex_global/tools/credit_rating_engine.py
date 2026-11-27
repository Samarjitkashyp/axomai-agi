"""
Z17 Apex-Global - S&P / Moody's Synthetic Credit Rating & Debt Sizing Engine.
Evaluates corporate debt capacity, Debt Service Coverage Ratio (DSCR),
Fixed Charge Coverage Ratio (FCCR), and assigns synthetic credit ratings with bond yield spreads.
"""

from typing import Dict, Any

class CreditRatingEngine:
    """Evaluates debt capacity and synthetic credit ratings according to rating agency methodologies."""

    # S&P / Moody's Corporate Rating Matrix benchmarks
    RATING_BENCHMARKS = [
        {"rating": "AAA", "max_leverage": 1.0, "min_coverage": 15.0, "spread_bps": 50},
        {"rating": "AA",  "max_leverage": 1.75, "min_coverage": 10.0, "spread_bps": 85},
        {"rating": "A",   "max_leverage": 2.5, "min_coverage": 6.5,  "spread_bps": 125},
        {"rating": "BBB", "max_leverage": 3.5, "min_coverage": 4.5,  "spread_bps": 175},
        {"rating": "BB",  "max_leverage": 4.5, "min_coverage": 3.0,  "spread_bps": 275},
        {"rating": "B",   "max_leverage": 5.5, "min_coverage": 1.75, "spread_bps": 450},
        {"rating": "CCC", "max_leverage": 7.0, "min_coverage": 1.0,  "spread_bps": 850}
    ]

    def evaluate_credit_profile(
        self,
        ebitda_m: float = 35.0,
        total_debt_m: float = 120.0,
        annual_interest_m: float = 8.5,
        annual_principal_m: float = 6.0,
        fcf_available_m: float = 22.0
    ) -> Dict[str, Any]:
        """
        Calculates credit metrics, assigns synthetic credit rating, and computes debt sizing headroom.
        """
        leverage_ratio = round(total_debt_m / max(ebitda_m, 1.0), 2)
        interest_coverage = round(ebitda_m / max(annual_interest_m, 0.1), 2)
        
        # Debt Service Coverage Ratio (DSCR) = FCF Available / (Principal + Interest)
        total_debt_service = annual_principal_m + annual_interest_m
        dscr = round(fcf_available_m / max(total_debt_service, 0.1), 2)

        # Fixed Charge Coverage Ratio (FCCR)
        fccr = round((ebitda_m - (fcf_available_m * 0.25)) / max(total_debt_service, 0.1), 2)

        # Determine Synthetic Rating
        assigned_rating = "CCC (Distressed / High Yield)"
        spread_bps = 850
        classification = "SPECULATIVE_GRADE"

        for b in self.RATING_BENCHMARKS:
            if leverage_ratio <= b["max_leverage"] and interest_coverage >= b["min_coverage"]:
                assigned_rating = f"{b['rating']} ({'Investment Grade' if b['spread_bps'] <= 175 else 'High Yield'})"
                spread_bps = b["spread_bps"]
                classification = "INVESTMENT_GRADE" if b["spread_bps"] <= 175 else "HIGH_YIELD_SPECULATIVE"
                break

        # Maximum Debt Sizing Capacity at 1.35x DSCR & 4.5x Max Leverage
        max_sustainable_debt_m = round(min(ebitda_m * 4.5, (fcf_available_m / 1.35) * 10.0), 1)
        borrowing_headroom_m = round(max_sustainable_debt_m - total_debt_m, 1)

        return {
            "synthetic_credit_rating": assigned_rating,
            "credit_classification": classification,
            "indicative_spread_over_sofr": f"{spread_bps} bps (+{round(spread_bps / 100.0, 2)}%)",
            "leverage_debt_to_ebitda": f"{leverage_ratio}x",
            "interest_coverage_ratio": f"{interest_coverage}x",
            "debt_service_coverage_ratio_dscr": f"{dscr}x",
            "fixed_charge_coverage_ratio_fccr": f"{fccr}x",
            "dscr_status": "PRISTINE_COVERAGE" if dscr >= 1.5 else ("ACCEPTABLE_COVENANT" if dscr >= 1.25 else "TIGHT_REFINANCING_RISK"),
            "max_sustainable_debt_capacity_m": f"${max_sustainable_debt_m}M",
            "incremental_borrowing_headroom_m": f"${borrowing_headroom_m}M",
            "covenant_underwriting_verdict": (
                "Balance sheet leverage meets standard Tier-1 private debt underwriting criteria."
                if dscr >= 1.35 and leverage_ratio <= 4.5 else
                "Elevated leverage ratio requires equity cure mechanism or seller note subordination."
            )
        }

credit_rating_engine = CreditRatingEngine()
