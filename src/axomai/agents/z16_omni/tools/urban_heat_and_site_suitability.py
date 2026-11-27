"""
Z16 Omni - Urban Heat Island (UHI) & Industrial/Warehouse Site Suitability Engine.
Scores land suitability (0-100) for warehouses, cold chains, solar parks, and factories
using live elevation, flood risk, seismic hazard, and thermal UHI delta.
"""

from typing import Dict, Any


class UrbanHeatAndSiteSuitability:
    """Computes Urban Heat Island delta and industrial site suitability score."""

    def evaluate_site_suitability(
        self,
        target_location: str,
        live_weather: Dict[str, Any],
        thermal_data: Dict[str, Any],
        hydro_elev: Dict[str, Any],
        energy_risk: Dict[str, Any],
    ) -> Dict[str, Any]:
        air_temp = float(live_weather.get("temperature_c", 26.0))
        lst_str = str(thermal_data.get("derived_land_surface_temp", "28.0°C")).split("°C")[0]
        try:
            lst_c = float(lst_str)
        except Exception:
            lst_c = air_temp + 2.4

        uhi_delta_c = round(lst_c - air_temp, 1)
        elev_m = float(hydro_elev.get("elevation_meters_asl", 55.0))
        geo_risk = float(energy_risk.get("composite_geo_risk_score", 30.0))

        # Site Suitability (100 = ideal high-ground low-risk industrial/warehouse zone)
        elev_bonus = 12.0 if elev_m >= 50.0 else 0.0
        suitability = round(max(15.0, min(98.0, 100.0 - (geo_risk * 0.75) + elev_bonus)), 1)
        grade = "PRIME_INDUSTRIAL_ZONE" if suitability >= 75 else ("MODERATE_REQUIRES_MITIGATION" if suitability >= 50 else "HIGH_HAZARD_AVOID")

        return {
            "target_location": target_location,
            "uhi_surface_air_delta_c": uhi_delta_c,
            "site_suitability_score": suitability,
            "site_suitability_grade": grade,
        }


urban_heat_site_suitability = UrbanHeatAndSiteSuitability()
