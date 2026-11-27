"""
Z10 Matrix - Cold-Chain Spoilage Kinetics & Reefer Telemetry Guard.
Models Q10 thermal degradation, ambient temperature delta across transit hours,
reefer diesel compressor surcharge, and pharma/dairy/tea shelf-life risk.
"""

from typing import Dict, Any, Optional


class ColdChainReeferGuard:
    """Evaluates cold-chain spoilage risk and reefer operating economics."""

    def evaluate_cold_chain_risk(
        self,
        transit_hours: float = 10.0,
        ambient_temp_c: float = 31.0,
        target_temp_c: float = 4.0,
        cargo_value_inr: float = 500000.0
    ) -> Dict[str, Any]:
        temp_delta = max(0.0, round(ambient_temp_c - target_temp_c, 1))
        # Reefer compressor fuel burn ~1.8L/hr scaled by thermal delta
        reefer_fuel_l = round(transit_hours * (1.2 + temp_delta * 0.04), 1)
        reefer_surcharge_inr = round(reefer_fuel_l * 91.5, 2)

        # Q10 kinetic spoilage risk index if active cooling fails or door opens
        thermal_stress_index = round((temp_delta / 10.0) * (transit_hours / 12.0), 2)
        spoilage_risk = (
            "HIGH_THERMAL_EXCURSION_RISK" if thermal_stress_index >= 3.5 else
            "MODERATE_REEFER_MONITORING" if thermal_stress_index >= 1.5 else
            "LOW_STABLE_COLD_CHAIN"
        )

        return {
            "target_setpoint_c": target_temp_c,
            "live_ambient_temp_c": ambient_temp_c,
            "thermal_gradient_c": temp_delta,
            "transit_hours": transit_hours,
            "reefer_diesel_burn_liters": reefer_fuel_l,
            "reefer_cooling_surcharge_inr": reefer_surcharge_inr,
            "spoilage_risk_grade": spoilage_risk,
            "value_at_risk_inr": cargo_value_inr if spoilage_risk.startswith("HIGH") else 0.0,
            "iot_protocol": "Dual-probe BLE thermal logger + 15-min SMS excursion alert"
        }


cold_chain_guard = ColdChainReeferGuard()
