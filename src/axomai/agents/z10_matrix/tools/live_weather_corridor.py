"""
Z10 Matrix - Live Weather, Flood & Monsoon Corridor Radar.
Queries Open-Meteo Live Weather API for exact route/destination coordinates
to measure real-time temperature, rainfall (mm), wind speed, and 3-day cumulative
precipitation, dynamically adjusting flood/landslide risk and warehouse safety buffers.
"""

import requests
from typing import Dict, Any, Optional, Tuple


class LiveWeatherCorridorRadar:
    """Fetches real-time meteorological & flood disruption telemetry for freight corridors."""

    def fetch_corridor_weather(
        self,
        city_name: str,
        coords: Optional[Tuple[float, float]] = None
    ) -> Dict[str, Any]:
        """Queries Open-Meteo API for live current weather and 3-day precipitation forecast."""
        if not coords:
            coords = (26.1445, 91.7362)  # Guwahati fallback

        lat, lon = coords
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,precipitation,wind_speed_10m"
            f"&daily=precipitation_sum&forecast_days=3&timezone=Asia/Kolkata"
        )

        source = "LIVE_OPEN_METEO_API"
        temp_c = 28.0
        curr_rain_mm = 0.0
        wind_kmh = 8.0
        rain_3day_mm = 0.0

        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                curr = data.get("current", {})
                temp_c = float(curr.get("temperature_2m", 28.0))
                curr_rain_mm = float(curr.get("precipitation", 0.0))
                wind_kmh = float(curr.get("wind_speed_10m", 8.0))
                daily_rain = data.get("daily", {}).get("precipitation_sum", [0.0])
                rain_3day_mm = round(sum(float(x or 0.0) for x in daily_rain), 1)
            else:
                source = f"OPEN_METEO_HTTP_{resp.status_code}"
        except Exception:
            source = "WEATHER_OFFLINE_BASELINE"

        # Classify disruption risk & dynamic buffer days
        if rain_3day_mm >= 80.0 or curr_rain_mm >= 15.0:
            risk = "SEVERE_MONSOON_FLOOD_ALERT"
            recommended_buffer_days = 21
            speed_penalty_pct = 30.0
        elif rain_3day_mm >= 25.0 or curr_rain_mm >= 3.0:
            risk = "MODERATE_RAIN_CAUTION"
            recommended_buffer_days = 15
            speed_penalty_pct = 12.0
        else:
            risk = "CLEAR_ALL_WEATHER"
            recommended_buffer_days = 10
            speed_penalty_pct = 0.0

        return {
            "city": city_name.title(),
            "coordinates": coords,
            "weather_source": source,
            "current_temp_c": temp_c,
            "current_precipitation_mm": curr_rain_mm,
            "wind_speed_kmh": wind_kmh,
            "forecast_3day_rain_mm": rain_3day_mm,
            "disruption_risk": risk,
            "recommended_safety_buffer_days": recommended_buffer_days,
            "transit_speed_penalty_pct": speed_penalty_pct
        }


live_weather_radar = LiveWeatherCorridorRadar()
