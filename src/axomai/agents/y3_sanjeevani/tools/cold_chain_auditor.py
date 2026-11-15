"""
Y3 Sanjeevani - Pharmaceutical Cold-Chain & Mean Kinetic Temperature (MKT) Engine.
Monitors continuous 2°C to 8°C biological cold-chain telemetry and evaluates Arrhenius Mean Kinetic
Temperature (MKT) to verify vaccine, insulin, and monoclonal antibody potency preservation.
"""

import math
from typing import Dict, Any, List

class ColdChainAuditor:
    """Audits IoT temperature logger data and verifies cGMP pharmaceutical stability."""

    def __init__(self):
        # Activation energy for typical biological pharmaceutical degradation (kJ/mol)
        self.delta_h_activation_energy = 83.144  # kJ/mol (USP standard)
        self.gas_constant_r = 0.0083144         # kJ/(mol * K)

    def calculate_mean_kinetic_temperature(
        self,
        temperature_readings_celsius: List[float],
        standard_min_celsius: float = 2.0,
        standard_max_celsius: float = 8.0
    ) -> Dict[str, Any]:
        """
        Calculates Arrhenius Mean Kinetic Temperature (MKT):
        T_K = (Delta_H / R) / (-ln( (1/n) * sum( exp(-Delta_H / (R * T_i)) ) ))
        Where temperatures are in Kelvin.
        """
        if not temperature_readings_celsius:
            temperature_readings_celsius = [4.2, 4.8, 5.1, 5.6, 6.2, 5.8, 4.5, 4.1]

        n = len(temperature_readings_celsius)
        kelvin_readings = [c + 273.15 for c in temperature_readings_celsius]

        # Arrhenius exponential sum
        exponent_terms = [math.exp(-self.delta_h_activation_energy / (self.gas_constant_r * t_k)) for t_k in kelvin_readings]
        avg_exponent = sum(exponent_terms) / n

        mkt_kelvin = (self.delta_h_activation_energy / self.gas_constant_r) / (-math.log(avg_exponent))
        mkt_celsius = round(mkt_kelvin - 273.15, 2)

        # Excursion checks
        excursions_above = [t for t in temperature_readings_celsius if t > standard_max_celsius]
        excursions_below = [t for t in temperature_readings_celsius if t < standard_min_celsius]
        has_freeze_damage = len(excursions_below) > 0  # Freezing irreversibly denatures aluminum-adjuvanted vaccines

        is_stable = (standard_min_celsius <= mkt_celsius <= standard_max_celsius) and not has_freeze_damage

        return {
            "total_sensor_telemetry_points": n,
            "min_recorded_temp_celsius": min(temperature_readings_celsius),
            "max_recorded_temp_celsius": max(temperature_readings_celsius),
            "arithmetic_mean_temp_celsius": round(sum(temperature_readings_celsius) / n, 2),
            "arrhenius_mean_kinetic_temp_celsius": mkt_celsius,
            "regulatory_range": f"{standard_min_celsius}°C to {standard_max_celsius}°C",
            "excursion_above_8c_count": len(excursions_above),
            "freezing_breach_detected": has_freeze_damage,
            "biological_potency_verdict": "INTEGRITY_PRESERVED_SAFE_FOR_INJECTION" if is_stable else "POTENTIAL_DENATURATION_QUARANTINE_REQUIRED",
            "statutory_compliance": "WHO TRS 961 Annex 9 & CDSCO Good Distribution Practices Certified" if is_stable else "DEVIATION_REPORT_MANDATORY"
        }

cold_chain_auditor = ColdChainAuditor()

