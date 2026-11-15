"""
Z14 Horizon - Global Freight Rate & Container Demurrage Predictor.
Benchmarks ocean container vs air cargo rates and models port congestion demurrage risks.
"""

from typing import Dict, Any

class FreightDemurrageEngine:
    """Calculates multimodal freight rates, Drewry container indices, and demurrage risks."""

    def __init__(self):
        # Benchmark container rates per 40ft High Cube (FEU) in USD
        self.container_benchmarks = {
            "kolkata_to_rotterdam": 3150.0,
            "nhava_sheva_to_rotterdam": 2850.0,
            "kolkata_to_jebel_ali": 1450.0,
            "kolkata_to_singapore": 850.0,
            "kolkata_to_los_angeles": 4200.0,
        }
        # Air cargo rates per kg in USD
        self.air_cargo_rates_per_kg = {
            "guwahati_to_frankfurt": 3.40,
            "kolkata_to_london": 3.10,
            "guwahati_to_dubai": 1.95,
        }
        self.usd_inr_rate = 86.40

    def calculate_multimodal_shipping(
        self,
        route: str,
        cargo_weight_kg: float,
        cargo_volume_cbm: float,
        container_count_40ft: int = 1
    ) -> Dict[str, Any]:
        """
        Compares Ocean Freight vs Air Cargo economics and transit duration.
        """
        route_key = route.lower().replace(" ", "_").replace("-", "_")
        ocean_base_usd = self.container_benchmarks.get(route_key, 2900.0) * container_count_40ft
        # Ocean bunker adjustment factor (BAF) + terminal handling (THC)
        ocean_surcharges_usd = (ocean_base_usd * 0.12) + (350.0 * container_count_40ft)
        total_ocean_usd = ocean_base_usd + ocean_surcharges_usd

        # Air cargo chargeable weight (1 CBM = 167 kg volumetric weight)
        volumetric_weight_kg = cargo_volume_cbm * 167.0
        chargeable_weight_kg = max(cargo_weight_kg, volumetric_weight_kg)
        air_rate_per_kg = 3.20  # average standard air cargo
        total_air_usd = round(chargeable_weight_kg * air_rate_per_kg, 2)

        return {
            "route": route,
            "cargo_weight_kg": cargo_weight_kg,
            "cargo_volume_cbm": cargo_volume_cbm,
            "ocean_freight": {
                "containers": f"{container_count_40ft} x 40ft HC",
                "base_rate_usd": ocean_base_usd,
                "surcharges_usd": round(ocean_surcharges_usd, 2),
                "total_cost_usd": round(total_ocean_usd, 2),
                "total_cost_inr": round(total_ocean_usd * self.usd_inr_rate, 2),
                "transit_time_days": "22 - 28 Days",
            },
            "air_cargo": {
                "chargeable_weight_kg": round(chargeable_weight_kg, 2),
                "rate_per_kg_usd": air_rate_per_kg,
                "total_cost_usd": total_air_usd,
                "total_cost_inr": round(total_air_usd * self.usd_inr_rate, 2),
                "transit_time_days": "3 - 5 Days",
            },
            "cost_premium_air_vs_ocean_multiple": round(total_air_usd / max(total_ocean_usd, 1.0), 2),
            "recommendation": (
                "Utilize Ocean Freight for high-volume commercial batch; allocate 5% urgent sample cargo to Air Freight."
            )
        }

    def predict_port_demurrage_risk(
        self,
        port_name: str,
        free_days_allowed: int = 7,
        expected_clearance_days: int = 11,
        containers_count: int = 2,
        daily_demurrage_fee_usd: float = 120.0
    ) -> Dict[str, Any]:
        """
        Calculates demurrage and detention liabilities due to customs clearance or port congestion delays.
        """
        excess_days = max(0, expected_clearance_days - free_days_allowed)
        total_demurrage_usd = excess_days * containers_count * daily_demurrage_fee_usd
        total_demurrage_inr = round(total_demurrage_usd * self.usd_inr_rate, 2)

        return {
            "port_name": port_name,
            "containers_count": containers_count,
            "contractual_free_days": free_days_allowed,
            "expected_dwell_days": expected_clearance_days,
            "demurrage_days_incurred": excess_days,
            "daily_rate_per_container_usd": daily_demurrage_fee_usd,
            "total_demurrage_liability_usd": round(total_demurrage_usd, 2),
            "total_demurrage_liability_inr": total_demurrage_inr,
            "risk_tier": "HIGH" if excess_days > 5 else ("MODERATE" if excess_days > 0 else "ZERO_RISK"),
            "mitigation_protocol": (
                "Request shipping line extended free-time amendment (14 days) and pre-clear via ICEGATE prior to vessel berthing."
            )
        }

freight_demurrage_engine = FreightDemurrageEngine()

