"""
Z16 Omni - Parametric Crop, Flood & Seismic Insurance Payout Trigger Engine.
Evaluates satellite/hydrological/seismic thresholds to compute automated
parametric insurance payout percentages and relief trigger status.
"""

from typing import Dict, Any, List


class ParametricInsuranceTrigger:
    """Computes automated parametric disaster insurance payout triggers."""

    def evaluate_parametric_triggers(
        self,
        target_location: str,
        live_weather: Dict[str, Any],
        hydro_elev: Dict[str, Any],
        thermal_data: Dict[str, Any],
        disaster_feed: Dict[str, Any],
        energy_risk: Dict[str, Any],
    ) -> Dict[str, Any]:
        rain_7d = float(live_weather.get("precip_7d_total_mm", 0.0))
        surge_ratio = float(hydro_elev.get("discharge_surge_ratio", 1.0))
        esi = float(thermal_data.get("evaporative_stress_index", 0.2))
        max_mag = float(disaster_feed.get("max_magnitude_500km", 0.0))
        gust_kmh = float(energy_risk.get("wind_gusts_10m_kmh", 15.0))

        triggered: List[str] = []
        payout_pct = 0.0

        if rain_7d >= 150.0 or surge_ratio >= 1.6:
            triggered.append("FLOOD_INUNDATION_PAYOUT")
            payout_pct += 40.0
        if esi >= 0.60:
            triggered.append("DROUGHT_ESI_PAYOUT")
            payout_pct += 35.0
        if max_mag >= 5.5:
            triggered.append("SEISMIC_M5.5_PAYOUT")
            payout_pct += 50.0
        if gust_kmh >= 65.0:
            triggered.append("CYCLONE_GALE_PAYOUT")
            payout_pct += 30.0

        payout_pct = min(100.0, payout_pct)
        status = "PARAMETRIC_PAYOUT_TRIGGERED" if triggered else "NO_PAYOUT_THRESHOLD_NOT_BREACHED"

        return {
            "target_location": target_location,
            "trigger_status": status,
            "triggered_perils": triggered,
            "recommended_payout_pct": payout_pct,
        }


parametric_insurance_trigger = ParametricInsuranceTrigger()
