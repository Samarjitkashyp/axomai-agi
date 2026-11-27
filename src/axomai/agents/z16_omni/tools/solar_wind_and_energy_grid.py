"""
Z16 Omni - Live Solar Irradiance, Cyclone/Wind Gusts & Composite Geo-Risk Index Engine.
Fetches real-time shortwave radiation and 10m wind gusts from Open-Meteo, computes
Solar PV yield potential (kWh/kWp/day), port crane wind safety, and a 0-100 Composite Geo-Risk Score.
"""

import requests
from typing import Dict, Any


class SolarWindAndEnergyGrid:
    """Computes live solar PV potential, wind/cyclone safety, and Composite Geo-Risk Score."""

    def evaluate_energy_and_composite_risk(
        self,
        lat: float,
        lng: float,
        target_location: str,
        sar_flood: Dict[str, Any],
        thermal_data: Dict[str, Any],
        disaster_feed: Dict[str, Any],
    ) -> Dict[str, Any]:
        wind_kmh = 12.0
        gust_kmh = 22.0
        solar_wm2 = 420.0
        source = "SOLAR_WIND_FALLBACK"

        try:
            resp = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lng,
                    "current": "wind_speed_10m,wind_gusts_10m,shortwave_radiation",
                    "daily": "shortwave_radiation_sum",
                    "forecast_days": 1,
                    "timezone": "auto",
                },
                timeout=4.0,
            )
            if resp.status_code == 200:
                data = resp.json()
                cur = data.get("current", {})
                daily = data.get("daily", {})
                wind_kmh = round(float(cur.get("wind_speed_10m") or 10.0), 1)
                gust_kmh = round(float(cur.get("wind_gusts_10m") or 18.0), 1)
                solar_wm2 = round(float(cur.get("shortwave_radiation") or 350.0), 1)
                rad_mj = float((daily.get("shortwave_radiation_sum") or [16.0])[0] or 16.0)
                pv_kwh_kwp = round((rad_mj / 3.6) * 0.78, 2)  # 78% PR solar PV yield
                source = "LIVE_OPEN_METEO_ENERGY_API"
            else:
                pv_kwh_kwp = 4.2
        except Exception:
            pv_kwh_kwp = 4.2

        wind_tier = "SEVERE_GALE_CRANE_HALT" if gust_kmh >= 65 else ("HIGH_WIND_WATCH" if gust_kmh >= 40 else "SAFE_OPERATIONS")

        # Composite Geo-Risk Score (0 - 100)
        flood_pts = 30.0 if "CRITICAL" in str(sar_flood.get("flood_severity_tier")) else (18.0 if "ELEVATED" in str(sar_flood.get("flood_severity_tier")) else 6.0)
        esi_pts = min(25.0, float(thermal_data.get("evaporative_stress_index", 0.2)) * 30.0)
        seismic_pts = min(25.0, float(disaster_feed.get("max_magnitude_500km", 0.0)) * 4.5)
        pm25 = float(disaster_feed.get("atmospheric_aqi", {}).get("pm2_5", 20.0))
        aqi_pts = min(10.0, pm25 / 15.0)
        wind_pts = 10.0 if gust_kmh >= 65 else (5.0 if gust_kmh >= 40 else 1.0)
        composite_score = round(min(100.0, flood_pts + esi_pts + seismic_pts + aqi_pts + wind_pts), 1)
        risk_grade = "CRITICAL" if composite_score >= 65 else ("ELEVATED" if composite_score >= 40 else "LOW_MODERATE")

        return {
            "target_location": target_location,
            "source": source,
            "wind_speed_10m_kmh": wind_kmh,
            "wind_gusts_10m_kmh": gust_kmh,
            "wind_safety_tier": wind_tier,
            "shortwave_radiation_wm2": solar_wm2,
            "solar_pv_yield_kwh_kwp_day": pv_kwh_kwp,
            "composite_geo_risk_score": composite_score,
            "composite_risk_grade": risk_grade,
        }


solar_wind_energy_grid = SolarWindAndEnergyGrid()
