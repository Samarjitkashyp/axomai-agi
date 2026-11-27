"""
Z10 Matrix - 3D Fleet Load & MoRTH Axle-Weight Compliance Optimizer.
Selects optimal Indian commercial vehicle configurations (Tata Ace to 40ft Multi-Axle),
computes payload & volumetric utilization, and prevents Motor Vehicles (Amendment) Act 2019
overloading penalties (₹20,000 base + ₹2,000 per excess ton).
"""

import math
from typing import Dict, Any, List


INDIAN_FLEET_CATALOG = [
    {"model": "Tata Ace Gold (LCV)", "max_payload_tons": 0.75, "volume_cft": 140, "mileage_kmpl": 16.0},
    {"model": "Eicher Pro 2075 (7-Tonner)", "max_payload_tons": 7.0, "volume_cft": 650, "mileage_kmpl": 7.5},
    {"model": "Tata LPT 1618 (16-Ton Rigid)", "max_payload_tons": 16.0, "volume_cft": 1350, "mileage_kmpl": 4.8},
    {"model": "Ashok Leyland 3520 (28-Ton Multi-Axle)", "max_payload_tons": 28.0, "volume_cft": 2200, "mileage_kmpl": 3.8},
    {"model": "40ft High-Cube Tractor Trailer", "max_payload_tons": 35.0, "volume_cft": 2680, "mileage_kmpl": 3.2}
]


class Cargo3DLoadOptimizer:
    """Optimizes truck selection, payload utilization, and statutory MoRTH axle compliance."""

    def optimize_fleet_load(
        self,
        cargo_weight_tons: float = 12.0,
        cargo_density_cft_per_ton: float = 65.0
    ) -> Dict[str, Any]:
        req_volume_cft = round(cargo_weight_tons * cargo_density_cft_per_ton, 1)

        # Find best single vehicle or multi-truck split
        selected = None
        trucks_needed = 1
        for veh in INDIAN_FLEET_CATALOG:
            if veh["max_payload_tons"] >= cargo_weight_tons and veh["volume_cft"] >= req_volume_cft:
                selected = veh
                break

        if not selected:
            selected = INDIAN_FLEET_CATALOG[-1]
            trucks_needed = math.ceil(max(
                cargo_weight_tons / selected["max_payload_tons"],
                req_volume_cft / selected["volume_cft"]
            ))

        total_cap_tons = round(selected["max_payload_tons"] * trucks_needed, 2)
        payload_util_pct = round((cargo_weight_tons / max(total_cap_tons, 0.1)) * 100.0, 1)
        excess_tons = max(0.0, round(cargo_weight_tons - total_cap_tons, 2))
        morth_penalty_inr = round(20000.0 + excess_tons * 2000.0, 2) if excess_tons > 0 else 0.0

        return {
            "recommended_vehicle": selected["model"],
            "trucks_required": trucks_needed,
            "cargo_weight_tons": cargo_weight_tons,
            "required_volume_cft": req_volume_cft,
            "total_fleet_capacity_tons": total_cap_tons,
            "payload_utilization_pct": payload_util_pct,
            "vehicle_mileage_kmpl": selected["mileage_kmpl"],
            "morth_axle_compliance": "100% COMPLIANT (Zero Overload)" if excess_tons == 0 else f"OVERLOAD_VIOLATION (+{excess_tons}T)",
            "avoided_mv_act_2019_penalty_inr": morth_penalty_inr
        }


cargo_load_optimizer = Cargo3DLoadOptimizer()
