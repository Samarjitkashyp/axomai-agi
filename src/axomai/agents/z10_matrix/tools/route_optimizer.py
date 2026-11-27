"""
Z10 Matrix - Live Road Route & Corridor Optimization Engine.
Connects to OpenStreetMap Nominatim Geocoding + Live OSRM Road Routing API
to fetch ACTUAL highway driving distances and transit durations between ANY two cities
in Assam, India, or the World. Enriches routes with Assam/Northeast terrain intelligence
(Kaziranga speed-camera zone, Sonapur/Jowai ghats) and falls back cleanly to Haversine math.
"""

import math
import requests
from typing import Dict, Any, List, Optional, Tuple

CITY_COORDINATES: Dict[str, Tuple[float, float]] = {
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.7041, 77.1025),
    "new delhi": (28.6139, 77.2090),
    "bengaluru": (12.9716, 77.5946),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "hyderabad": (17.3850, 78.4867),
    "ahmedabad": (23.0225, 72.5714),
    "pune": (18.5204, 73.8567),
    "jaipur": (26.9124, 75.7873),
    "lucknow": (26.8467, 80.9462),
    "patna": (25.5941, 85.1376),
    "surat": (21.1702, 72.8311),
    "nagpur": (21.1458, 79.0882),
    "guwahati": (26.1445, 91.7362),
    "changsari": (26.2405, 91.6882),
    "nagaon": (26.3470, 92.6840),
    "dibrugarh": (27.4728, 94.9120),
    "jorhat": (26.7509, 94.2037),
    "silchar": (24.8333, 92.7789),
    "tezpur": (26.6528, 92.7926),
    "tinsukia": (27.4922, 95.3468),
    "golaghat": (26.5167, 93.9667),
    "shillong": (25.5788, 91.8933),
    "imphal": (24.8170, 93.9368),
    "agartala": (23.8315, 91.2868),
    "aizawl": (23.7271, 92.7176),
    "dimapur": (25.9090, 93.7266),
    "kohima": (25.6751, 94.1086),
    "itanagar": (27.0844, 93.6053),
    "dhubri": (26.0207, 89.9743),
    "dubai": (25.2048, 55.2708),
    "singapore": (1.3521, 103.8198),
    "london": (51.5074, -0.1278),
    "rotterdam": (51.9244, 4.4777),
    "new york": (40.7128, -74.0060)
}

CORRIDOR_INTELLIGENCE = {
    ("guwahati", "dibrugarh"): {
        "corridor": "NH-715 / NH-29 / NH-2 (Upper Assam Spine)",
        "terrain": "Plains with Kaziranga Eco-Sensitive Zone (Strict 40 km/h speed-camera enforcement)",
        "monsoon_flood_risk": "MODERATE-HIGH (Kaziranga animal corridor & Brahmaputra floods)"
    },
    ("guwahati", "silchar"): {
        "corridor": "NH-6 (Meghalaya Plateau to Barak Valley)",
        "terrain": "Steep Hill Ghat Road (Sonapur / Jowai Tunnel & Ghats)",
        "monsoon_flood_risk": "HIGH (Landslide vulnerability during June-September)"
    },
    ("guwahati", "nagaon"): {
        "corridor": "NH-27 (East-West Expressway)",
        "terrain": "4-Lane Divided All-Weather Expressway",
        "monsoon_flood_risk": "LOW (Elevated embankment)"
    },
    ("mumbai", "delhi"): {
        "corridor": "NE-4 Delhi-Mumbai Expressway / Western Freight Corridor",
        "terrain": "8-Lane Access Controlled Commercial Plains",
        "monsoon_flood_risk": "VERY LOW"
    }
}


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * (math.sin(dlambda / 2.0) ** 2)
    return round(r * (2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))), 1)


class RouteOptimizer:
    """Computes live OSRM highway driving routes, coordinates, fuel/toll economics, and corridor risks."""

    def __init__(self):
        self.headers = {"User-Agent": "AxomAI-Z10Matrix/2.0"}
        self._coord_cache: Dict[str, Tuple[float, float]] = dict(CITY_COORDINATES)

    def geocode_city(self, city_name: str) -> Optional[Tuple[float, float]]:
        """Resolves any city name to (lat, lon) via cache or live OpenStreetMap Nominatim."""
        key = city_name.lower().strip()
        if key in self._coord_cache:
            return self._coord_cache[key]
        try:
            url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(city_name + ', India')}&format=json&limit=1"
            resp = requests.get(url, headers=self.headers, timeout=5)
            if resp.status_code == 200 and resp.json():
                item = resp.json()[0]
                coords = (float(item["lat"]), float(item["lon"]))
                self._coord_cache[key] = coords
                return coords
        except Exception:
            pass
        return None

    def fetch_live_osrm_route(self, c1: Tuple[float, float], c2: Tuple[float, float]) -> Optional[Tuple[float, float]]:
        """Queries live OSRM road routing API for actual driving distance (km) and duration (hrs)."""
        try:
            # OSRM expects lon,lat;lon,lat
            url = f"https://router.project-osrm.org/route/v1/driving/{c1[1]},{c1[0]};{c2[1]},{c2[0]}?overview=false"
            resp = requests.get(url, headers=self.headers, timeout=6)
            if resp.status_code == 200:
                data = resp.json()
                routes = data.get("routes", [])
                if routes:
                    dist_km = round(routes[0]["distance"] / 1000.0, 1)
                    # Commercial trucks average ~75% of car speed on Indian highways
                    hrs = round((routes[0]["duration"] / 3600.0) * 1.32, 1)
                    return dist_km, hrs
        except Exception:
            pass
        return None

    def optimize_route(
        self,
        origin: str,
        destination: str,
        diesel_price_inr: float = 91.5,
        mileage_km_per_l: float = 4.2,
        cargo_tons: float = 12.0
    ) -> Dict[str, Any]:
        """
        Optimizes route using live OSRM highway telemetry + Nominatim geocoding,
        calculating exact diesel, toll, driver allowance, and regional terrain risk.
        """
        o_key = origin.lower().strip()
        d_key = destination.lower().strip()

        c1 = self.geocode_city(origin)
        c2 = self.geocode_city(destination)

        routing_source = "FALLBACK_BASELINE"
        dist_km = 300.0
        transit_hrs = 7.5

        if c1 and c2:
            osrm_res = self.fetch_live_osrm_route(c1, c2)
            if osrm_res:
                dist_km, transit_hrs = osrm_res
                routing_source = "LIVE_OSRM_HIGHWAY_API"
            else:
                # Haversine * 1.28 road circuity factor
                dist_km = round(haversine_distance_km(c1[0], c1[1], c2[0], c2[1]) * 1.28, 1)
                transit_hrs = round(dist_km / 42.0, 1)
                routing_source = "HAVERSINE_CIRCUITY_MODEL"

        # Corridor Intelligence lookup (order independent)
        intel = CORRIDOR_INTELLIGENCE.get((o_key, d_key)) or CORRIDOR_INTELLIGENCE.get((d_key, o_key))
        corridor_name = intel["corridor"] if intel else f"National Highway Network ({origin.title()} ↔ {destination.title()})"
        terrain = intel["terrain"] if intel else "Mixed National Highway & Arterial Corridor"
        monsoon_risk = intel["monsoon_flood_risk"] if intel else "MODERATE"

        # Fuel, Toll & Driver Economics
        fuel_liters = round(dist_km / mileage_km_per_l, 1)
        fuel_cost_inr = round(fuel_liters * diesel_price_inr, 2)
        toll_inr = round(dist_km * 1.55, 2)  # Avg NHAI FASTag commercial axle toll ~₹1.55/km
        driver_ops_inr = round(transit_hrs * 180.0 + 600.0, 2)
        total_cost_inr = round(fuel_cost_inr + toll_inr + driver_ops_inr, 2)
        cost_per_ton_km = round(total_cost_inr / max(dist_km * cargo_tons, 1.0), 2)

        return {
            "origin": origin.title(),
            "destination": destination.title(),
            "origin_coords": c1,
            "destination_coords": c2,
            "routing_source": routing_source,
            "corridor": corridor_name,
            "distance_km": dist_km,
            "transit_time_hrs": transit_hrs,
            "terrain": terrain,
            "monsoon_flood_risk": monsoon_risk,
            "fuel_liters_required": fuel_liters,
            "fuel_cost_inr": fuel_cost_inr,
            "toll_charges_inr": toll_inr,
            "total_logistics_cost_inr": total_cost_inr,
            "cost_per_ton_km_inr": cost_per_ton_km
        }


route_optimizer = RouteOptimizer()
