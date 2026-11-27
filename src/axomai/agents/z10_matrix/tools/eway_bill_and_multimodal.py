"""
Z10 Matrix - GST E-Way Bill (CGST Rule 138) & Multimodal Freight Arbitrage Engine.
Calculates statutory E-Way Bill mandates & validity windows (1 day per 200 km normal,
1 day per 20 km ODC) and compares Road Truck vs Indian Railways CONCOR vs
Brahmaputra Inland Waterway (NW-2 Pandu-Dhubri-Dibrugarh) vs Air Cargo.
"""

import math
from typing import Dict, Any, List


class EwayBillAndMultimodalEngine:
    """Statutory CGST Rule 138 Compliance & Multimodal Cost/CO2 Arbitrage Engine."""

    def evaluate_eway_bill(
        self,
        consignment_value_inr: float = 250000.0,
        distance_km: float = 350.0,
        is_odc: bool = False
    ) -> Dict[str, Any]:
        """Evaluates CGST Rule 138 mandatory E-Way Bill threshold and validity days."""
        mandatory = consignment_value_inr > 50000.0
        km_per_day = 20.0 if is_odc else 200.0
        validity_days = math.ceil(max(distance_km, 1.0) / km_per_day) if mandatory else 0

        return {
            "statutory_rule": "CGST Rule 138 (Central Goods and Services Tax Rules, 2017)",
            "consignment_value_inr": consignment_value_inr,
            "eway_bill_mandatory": mandatory,
            "cargo_category": "Over-Dimensional Cargo (ODC)" if is_odc else "Regular Commercial Freight",
            "distance_km": distance_km,
            "statutory_validity_days": validity_days,
            "rule_basis": f"1 day per {int(km_per_day)} km" if mandatory else "Exempt (Value <= ₹50,000)"
        }

    def compare_multimodal_options(
        self,
        distance_km: float = 450.0,
        cargo_tons: float = 12.0,
        road_cost_inr: float = 12500.0,
        road_hrs: float = 10.5
    ) -> Dict[str, Any]:
        """Compares Road vs Rail (CONCOR) vs NW-2 Brahmaputra River Barge vs Air Freight."""
        # Emission factors: kg CO2 per ton-km
        road_co2_kg = round(distance_km * cargo_tons * 0.096, 1)

        rail_cost_inr = round(distance_km * cargo_tons * 1.45 + 3200.0, 2)
        rail_hrs = round((distance_km / 28.0) + 6.0, 1)  # Includes terminal handling
        rail_co2_kg = round(distance_km * cargo_tons * 0.028, 1)

        waterway_cost_inr = round(distance_km * cargo_tons * 0.95 + 2800.0, 2)
        waterway_hrs = round((distance_km / 14.0) + 8.0, 1)
        waterway_co2_kg = round(distance_km * cargo_tons * 0.019, 1)

        air_cost_inr = round(distance_km * cargo_tons * 24.0 + 18000.0, 2)
        air_hrs = round((distance_km / 650.0) + 4.5, 1)
        air_co2_kg = round(distance_km * cargo_tons * 0.602, 1)

        modes = [
            {"mode": "Highway Diesel Truck", "cost_inr": road_cost_inr, "transit_hrs": road_hrs, "co2_kg": road_co2_kg},
            {"mode": "Indian Railways (CONCOR)", "cost_inr": rail_cost_inr, "transit_hrs": rail_hrs, "co2_kg": rail_co2_kg},
            {"mode": "Inland Waterway (NW-2 Brahmaputra Barge)", "cost_inr": waterway_cost_inr, "transit_hrs": waterway_hrs, "co2_kg": waterway_co2_kg},
            {"mode": "Air Freight Express", "cost_inr": air_cost_inr, "transit_hrs": air_hrs, "co2_kg": air_co2_kg}
        ]
        cheapest = min(modes, key=lambda m: m["cost_inr"])
        fastest = min(modes, key=lambda m: m["transit_hrs"])

        return {
            "modes_compared": modes,
            "lowest_cost_mode": cheapest["mode"],
            "fastest_mode": fastest["mode"],
            "co2_savings_via_waterway_vs_road_kg": round(road_co2_kg - waterway_co2_kg, 1)
        }


eway_multimodal = EwayBillAndMultimodalEngine()
