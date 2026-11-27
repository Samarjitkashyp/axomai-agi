"""
Z16 Omni - Live GloFAS River Discharge & Terrain Elevation Engine.
Uses Open-Meteo Global Flood API (GloFAS) and Elevation API to fetch real-time
river discharge (m3/s) and altitude (meters ASL) for any coordinates.
"""

import requests
from typing import Dict, Any


class RiverDischargeAndElevation:
    """Fetches live GloFAS river discharge and terrain elevation."""

    def fetch_hydrology_and_elevation(self, lat: float, lng: float, target_location: str) -> Dict[str, Any]:
        elevation_m = 55.0
        elev_source = "ELEVATION_FALLBACK"
        try:
            r_el = requests.get(
                "https://api.open-meteo.com/v1/elevation",
                params={"latitude": lat, "longitude": lng},
                timeout=3.5,
            )
            if r_el.status_code == 200:
                elevs = r_el.json().get("elevation") or []
                if elevs:
                    elevation_m = round(float(elevs[0]), 1)
                    elev_source = "LIVE_OPEN_METEO_ELEVATION_API"
        except Exception:
            pass

        discharge_today = 0.0
        discharge_max_7d = 0.0
        discharge_mean = 0.0
        flood_source = "GLOFAS_CALIBRATED_FALLBACK"
        try:
            r_fl = requests.get(
                "https://flood-api.openmeteo.com/v1/flood",
                params={
                    "latitude": lat,
                    "longitude": lng,
                    "daily": "river_discharge,river_discharge_mean,river_discharge_max",
                    "forecast_days": 7,
                },
                timeout=4.5,
            )
            if r_fl.status_code == 200:
                daily = r_fl.json().get("daily", {})
                rd = [float(x) for x in (daily.get("river_discharge") or []) if x is not None]
                rd_mean = [float(x) for x in (daily.get("river_discharge_mean") or []) if x is not None]
                rd_max = [float(x) for x in (daily.get("river_discharge_max") or []) if x is not None]
                if rd:
                    discharge_today = round(rd[0], 2)
                    discharge_max_7d = round(max(rd_max or rd), 2)
                    discharge_mean = round(sum(rd_mean) / len(rd_mean), 2) if rd_mean else discharge_today
                    flood_source = "LIVE_GLOFAS_FLOOD_API"
        except Exception:
            pass

        ratio = round(discharge_max_7d / max(discharge_mean, 1.0), 2) if discharge_mean > 0 else 1.0
        if ratio >= 1.6 and elevation_m < 90:
            hydro_tier = "CRITICAL_RIVER_SURGE"
        elif ratio >= 1.25:
            hydro_tier = "ELEVATED_DISCHARGE"
        else:
            hydro_tier = "NORMAL_RIVER_FLOW"

        return {
            "target_location": target_location,
            "elevation_source": elev_source,
            "elevation_meters_asl": elevation_m,
            "flood_api_source": flood_source,
            "river_discharge_today_m3s": discharge_today,
            "river_discharge_7d_max_m3s": discharge_max_7d,
            "river_discharge_mean_m3s": discharge_mean,
            "discharge_surge_ratio": ratio,
            "hydro_flood_tier": hydro_tier,
        }


river_discharge_elevation = RiverDischargeAndElevation()
