"""
Z14 Horizon - Global Foreign Exchange (FX) & Currency Hedging Engine.
Computes cross-currency conversions, forward hedge pricing, and FX volatility bands.
"""

from typing import Dict, Any, List

# Benchmark Institutional FX Rates against USD
FX_USD_RATES = {
    "USD": 1.0,
    "INR": 86.40,
    "EUR": 0.92,
    "GBP": 0.79,
    "AED": 3.6725,
    "SGD": 1.34,
    "JPY": 154.50,
    "CNY": 7.24
}

class FXEngine:
    """Manages cross-currency risk, conversion, and forward contract hedging."""

    def convert_currency(self, amount: float, from_curr: str, to_curr: str) -> Dict[str, Any]:
        f = from_curr.upper().strip()
        t = to_curr.upper().strip()
        
        rate_from = FX_USD_RATES.get(f, 1.0)
        rate_to = FX_USD_RATES.get(t, 1.0)

        # Convert to USD then to target
        amount_usd = amount / rate_from
        converted_amount = amount_usd * rate_to
        effective_rate = rate_to / rate_from

        return {
            "from_currency": f,
            "to_currency": t,
            "original_amount": amount,
            "converted_amount": round(converted_amount, 2),
            "effective_exchange_rate": round(effective_rate, 4),
            "rate_usd_basis": {"from_usd": rate_from, "to_usd": rate_to}
        }

    def compute_forward_hedge(
        self,
        notional_amount: float,
        base_currency: str = "USD",
        quote_currency: str = "INR",
        tenor_months: int = 6,
        domestic_rate_pct: float = 6.5, # RBI Repo
        foreign_rate_pct: float = 4.5    # US Fed Funds
    ) -> Dict[str, Any]:
        """
        Computes forward exchange rate using Covered Interest Rate Parity:
        F = S * (1 + r_d * t) / (1 + r_f * t)
        """
        spot_rate = FX_USD_RATES.get(quote_currency, 86.40) / FX_USD_RATES.get(base_currency, 1.0)
        t = tenor_months / 12.0

        r_d = domestic_rate_pct / 100.0
        r_f = foreign_rate_pct / 100.0

        forward_rate = spot_rate * ((1 + r_d * t) / (1 + r_f * t))
        forward_premium_pct = round(((forward_rate - spot_rate) / spot_rate) * 100, 2)
        hedged_value_quote = round(notional_amount * forward_rate, 2)
        unhedged_spot_value = round(notional_amount * spot_rate, 2)

        return {
            "notional_base_amount": notional_amount,
            "base_currency": base_currency,
            "quote_currency": quote_currency,
            "tenor_months": tenor_months,
            "spot_rate": round(spot_rate, 4),
            "forward_rate": round(forward_rate, 4),
            "forward_premium_pct": forward_premium_pct,
            "hedged_total_quote": hedged_value_quote,
            "unhedged_spot_total": unhedged_spot_value,
            "risk_mitigation": f"Locked-in forward hedge protects against currency depreciation beyond ₹{forward_rate:.2f}/{base_currency}."
        }

fx_engine = FXEngine()

