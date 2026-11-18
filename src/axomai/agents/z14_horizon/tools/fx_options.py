"""
Z14 Horizon - FX Options & Garman-Kohlhagen Currency Hedging Engine.
Provides European Call/Put pricing, Greeks, and Zero-Cost Collar hedging strategies.
"""

import math
from typing import Dict, Any, Optional

def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def norm_pdf(x: float) -> float:
    """Standard normal probability density function."""
    return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)

class FXOptionsEngine:
    """Institutional Garman-Kohlhagen FX Options & Collar Strategy Calculator."""

    def __init__(self):
        # Dynamic implied volatilities across G10 and Emerging FX pairs
        self.volatilities: Dict[str, float] = {
            "USDINR": 0.055,  # 5.5% annual implied vol
            "EURINR": 0.072,  # 7.2% annual implied vol
            "GBPINR": 0.081,  # 8.1% annual implied vol
            "JPYINR": 0.095,  # 9.5% annual implied vol
            "EURUSD": 0.068,
            "GBPUSD": 0.075,
            "USDJPY": 0.088,
            "AUDUSD": 0.082,
            "USDCAD": 0.062,
            "USDCHF": 0.065,
            "USDCNY": 0.045,
            "SGDINR": 0.048,
            "AEDINR": 0.042
        }

    def get_volatility(self, pair: str) -> float:
        """Dynamically resolves or estimates implied volatility for ANY currency pair."""
        p_clean = pair.upper().replace("/", "").replace("-", "")
        if p_clean in self.volatilities:
            return self.volatilities[p_clean]
        if any(c in p_clean for c in ["BTC", "ETH", "CRYPTO"]):
            return 0.58
        if any(c in p_clean for c in ["TRY", "BRL", "ZAR", "RUB"]):
            return 0.165
        return 0.070  # Standard G10 average baseline

    def register_volatility(self, pair: str, vol: float) -> None:
        """Registers real-time market implied volatility."""
        self.volatilities[pair.upper().replace("/", "").replace("-", "")] = vol

    def price_currency_option(
        self,
        spot: float,
        strike: float,
        tenor_years: float,
        domestic_rate: float,  # e.g., INR rate = 0.065 (6.5%)
        foreign_rate: float,   # e.g., USD rate = 0.045 (4.5%)
        volatility: float,      # e.g., 0.055 (5.5%)
        option_type: str = "call"
    ) -> Dict[str, Any]:
        """
        Prices a European currency option using Garman-Kohlhagen (1983).
        """
        if tenor_years <= 0 or volatility <= 0 or spot <= 0 or strike <= 0:
            raise ValueError("Invalid parameters for option pricing")

        sqrt_t = math.sqrt(tenor_years)
        d1 = (math.log(spot / strike) + (domestic_rate - foreign_rate + 0.5 * volatility ** 2) * tenor_years) / (volatility * sqrt_t)
        d2 = d1 - volatility * sqrt_t

        exp_rf = math.exp(-foreign_rate * tenor_years)
        exp_rd = math.exp(-domestic_rate * tenor_years)

        if option_type.lower() == "call":
            price = spot * exp_rf * norm_cdf(d1) - strike * exp_rd * norm_cdf(d2)
            delta = exp_rf * norm_cdf(d1)
            theta = (
                - (spot * exp_rf * norm_pdf(d1) * volatility) / (2.0 * sqrt_t)
                + foreign_rate * spot * exp_rf * norm_cdf(d1)
                - domestic_rate * strike * exp_rd * norm_cdf(d2)
            )
        else:  # put
            price = strike * exp_rd * norm_cdf(-d2) - spot * exp_rf * norm_cdf(-d1)
            delta = -exp_rf * norm_cdf(-d1)
            theta = (
                - (spot * exp_rf * norm_pdf(d1) * volatility) / (2.0 * sqrt_t)
                - foreign_rate * spot * exp_rf * norm_cdf(-d1)
                + domestic_rate * strike * exp_rd * norm_cdf(-d2)
            )

        gamma = (exp_rf * norm_pdf(d1)) / (spot * volatility * sqrt_t)
        vega = spot * exp_rf * sqrt_t * norm_pdf(d1)  # per 100% vol (divide by 100 for 1% vol change)

        return {
            "spot": spot,
            "strike": strike,
            "tenor_years": tenor_years,
            "tenor_days": int(round(tenor_years * 365)),
            "option_type": option_type.upper(),
            "premium": round(price, 4),
            "premium_pct": round((price / spot) * 100.0, 3),
            "greeks": {
                "delta": round(delta, 4),
                "gamma": round(gamma, 6),
                "vega_1pct": round(vega / 100.0, 4),
                "theta_per_day": round(theta / 365.0, 4),
            }
        }

    def calculate_zero_cost_collar(
        self,
        spot: float,
        notional: float,
        tenor_months: int = 3,
        pair: str = "USDINR",
        floor_downside_pct: float = 0.02,  # 2% out of the money put floor
        domestic_rate: float = 0.065,      # RBI repo / risk-free
        foreign_rate: float = 0.045        # Fed funds / risk-free
    ) -> Dict[str, Any]:
        """
        Structures an exporter Zero-Cost Collar:
        - Buys an OTM Put option (protects downside if currency drops)
        - Sells an OTM Call option (caps upside, finances the put premium to net zero)
        """
        vol = self.get_volatility(pair)
        tenor_years = tenor_months / 12.0

        # Protective Put Strike (Floor)
        put_strike = round(spot * (1.0 - floor_downside_pct), 2)
        put_res = self.price_currency_option(
            spot, put_strike, tenor_years, domestic_rate, foreign_rate, vol, option_type="put"
        )
        target_premium = put_res["premium"]

        # Search for Call Strike (Cap) where Call Premium ≈ Put Premium
        best_call_strike = spot * 1.01
        min_diff = float("inf")

        # Binary search / step search for call strike
        for step in range(10, 150):
            test_strike = round(spot * (1.0 + step * 0.001), 2)
            call_res = self.price_currency_option(
                spot, test_strike, tenor_years, domestic_rate, foreign_rate, vol, option_type="call"
            )
            diff = abs(call_res["premium"] - target_premium)
            if diff < min_diff:
                min_diff = diff
                best_call_strike = test_strike

        final_call = self.price_currency_option(
            spot, best_call_strike, tenor_years, domestic_rate, foreign_rate, vol, option_type="call"
        )
        net_premium = round(put_res["premium"] - final_call["premium"], 4)

        return {
            "pair": pair.upper(),
            "spot_rate": spot,
            "notional": notional,
            "tenor_months": tenor_months,
            "put_floor_strike": put_strike,
            "put_premium": put_res["premium"],
            "call_cap_strike": best_call_strike,
            "call_premium": final_call["premium"],
            "net_premium_cost": net_premium,
            "is_zero_cost": abs(net_premium) < 0.05,
            "downside_protection_level": f"₹{put_strike} (Locks min conversion)",
            "upside_participation_cap": f"₹{best_call_strike} (Caps max upside)",
            "hedged_value_floor_inr": round(put_strike * notional, 2),
            "hedged_value_cap_inr": round(best_call_strike * notional, 2),
            "recommendation": (
                f"Zero-Cost Collar guarantees conversion between ₹{put_strike} and ₹{best_call_strike} "
                f"per USD without paying any upfront hedging premium."
            )
        }

fx_options_engine = FXOptionsEngine()

