"""
Z16 Omni - Multi-Location Geospatial Risk Comparator.
Detects 2+ locations in a user query and ranks them by live rainfall, soil moisture,
flood risk, and thermal stress in a single unified comparison matrix.
"""

import re
from typing import Dict, Any, List
from axomai.agents.z16_omni.tools.geo_extractor_and_live_apis import KNOWN_COORDS, geo_extractor_and_live_apis


class MultiSiteComparator:
    """Compares multiple cities, river basins, or ports using live telemetry."""

    def extract_multiple_locations(self, query: str) -> List[str]:
        q_low = (query or "").lower()
        found: List[str] = []
        for place in sorted(KNOWN_COORDS.keys(), key=len, reverse=True):
            if re.search(r'\b' + re.escape(place) + r'\b', q_low):
                lat_c, lng_c, _ = KNOWN_COORDS[place]
                if not any(abs(KNOWN_COORDS[f][0] - lat_c) < 0.05 and abs(KNOWN_COORDS[f][1] - lng_c) < 0.05 for f in found):
                    found.append(place)
        return found[:4]

    def compare_sites(self, query: str) -> List[Dict[str, Any]]:
        places = self.extract_multiple_locations(query)
        if len(places) < 2:
            return []

        results: List[Dict[str, Any]] = []
        for p in places:
            lat, lng, region = KNOWN_COORDS[p]
            w = geo_extractor_and_live_apis.fetch_live_earth_telemetry(lat, lng)
            flood_score = min(100.0, round((w["precip_7d_total_mm"] * 0.6) + (w["soil_moisture_pct"] * 0.8), 1))
            results.append({
                "location": p.title(),
                "region": region,
                "lat": lat,
                "lng": lng,
                "temp_c": w["temperature_c"],
                "cloud_cover_pct": w["cloud_cover_pct"],
                "precip_7d_mm": w["precip_7d_total_mm"],
                "soil_moisture_pct": w["soil_moisture_pct"],
                "et0_mm": w["et0_today_mm"],
                "composite_risk_score": flood_score,
            })

        results.sort(key=lambda x: x["composite_risk_score"], reverse=True)
        return results


multi_site_comparator = MultiSiteComparator()
