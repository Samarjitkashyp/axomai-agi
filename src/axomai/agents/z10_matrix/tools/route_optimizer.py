"""
Z10 Matrix - Regional Route & Fleet Optimization Tool.
Computes distance, transit time, toll/fuel estimation, terrain difficulty,
and monsoon weather risk across Assam and Northeast logistics corridors.
"""

from typing import Dict, Any, List, Optional

CORRIDOR_DATA = {
    ("guwahati", "nagaon"): {
        "corridor": "NH-27 (East-West Expressway)",
        "distance_km": 124,
        "transit_time_hrs": 2.8,
        "lane_profile": "4-Lane Divided Expressway",
        "toll_charges_inr": 210,
        "terrain": "Plain All-Weather Highway",
        "monsoon_flood_risk": "LOW (Elevated embankment)",
        "recommended_vehicle": "16-Ton Multi-Axle or 3.5T LCV",
        "speed_limit_kmh": 80
    },
    ("guwahati", "dibrugarh"): {
        "corridor": "NH-715 / NH-29 / NH-2",
        "distance_km": 445,
        "transit_time_hrs": 9.5,
        "lane_profile": "Mixed 4-Lane & 2-Lane Highway",
        "toll_charges_inr": 620,
        "terrain": "Plains with Kaziranga Eco-Sensitive Corridor (Strict 40 km/h camera checks)",
        "monsoon_flood_risk": "MODERATE (Kaziranga stretch requires convoy during heavy monsoons)",
        "recommended_vehicle": "16-Ton Heavy Truck with GPS Fleet Tracking",
        "speed_limit_kmh": 65
    },
    ("guwahati", "silchar"): {
        "corridor": "NH-6 (Meghalaya Plateau to Barak Valley)",
        "distance_km": 315,
        "transit_time_hrs": 10.5,
        "lane_profile": "Hilly 2-Lane Ghat Road",
        "toll_charges_inr": 340,
        "terrain": "Steep Hill Terrain (Sonapur / Jowai Ghats)",
        "monsoon_flood_risk": "HIGH (Landslide vulnerability during June-August)",
        "recommended_vehicle": "Heavy 6-Wheel Rugged Chassis LCV",
        "speed_limit_kmh": 40
    },
    ("guwahati", "jorhat"): {
        "corridor": "NH-715",
        "distance_km": 305,
        "transit_time_hrs": 6.8,
        "lane_profile": "4-Lane & 2-Lane Sections",
        "toll_charges_inr": 480,
        "terrain": "Central Valley Plain Highway",
        "monsoon_flood_risk": "LOW-MODERATE",
        "recommended_vehicle": "3.5T to 9T Medium Freight Vehicle",
        "speed_limit_kmh": 70
    },
    ("guwahati", "tezpur"): {
        "corridor": "NH-15 / Kolia Bhomora Setu",
        "distance_km": 178,
        "transit_time_hrs": 3.8,
        "lane_profile": "4-Lane Bridge Corridor",
        "toll_charges_inr": 280,
        "terrain": "Brahmaputra North-Bank Connector",
        "monsoon_flood_risk": "LOW (River bridge corridor)",
        "recommended_vehicle": "3.5T LCV",
        "speed_limit_kmh": 75
    }
}

class RouteOptimizer:
    """Computes real-world commercial freight routing and cost profiles across Northeast corridors."""

    def __init__(self, diesel_rate_per_liter: float = 91.50):
        self.diesel_rate = diesel_rate_per_liter

    def optimize_route(self, origin: str, destination: str, payload_tons: float = 5.0) -> Dict[str, Any]:
        orig = origin.lower().strip()
        dest = destination.lower().strip()

        # Lookup key
        key = None
        for (o, d) in CORRIDOR_DATA:
            if (o in orig and d in dest) or (d in orig and o in dest):
                key = (o, d)
                break

        if not key:
            # Fallback estimation based on generic distance
            dist_est = 250
            return {
                "origin": origin.title(),
                "destination": destination.title(),
                "corridor": "Regional National Highway Link",
                "distance_km": dist_est,
                "transit_time_hrs": round(dist_est / 45, 1),
                "toll_charges_inr": 350,
                "fuel_cost_inr": round((dist_est / 4.2) * self.diesel_rate, 2),
                "total_logistics_cost_inr": round(((dist_est / 4.2) * self.diesel_rate) + 350 + (payload_tons * 150), 2),
                "terrain": "Regional Mixed Corridor",
                "monsoon_risk": "MODERATE",
                "recommended_vehicle": "3.5T Commercial LCV"
            }

        data = CORRIDOR_DATA[key]
        dist = data["distance_km"]
        
        # Mileage estimate: ~4.5 km/L for 5-Ton, ~3.2 km/L for 16-Ton
        km_per_liter = 4.2 if payload_tons <= 7.5 else 3.4
        fuel_liters = round(dist / km_per_liter, 1)
        fuel_cost = round(fuel_liters * self.diesel_rate, 2)
        driver_allowance = round(data["transit_time_hrs"] * 120, 2)
        total_trip_cost = round(fuel_cost + data["toll_charges_inr"] + driver_allowance, 2)

        return {
            "origin": origin.title(),
            "destination": destination.title(),
            "corridor": data["corridor"],
            "distance_km": dist,
            "transit_time_hrs": data["transit_time_hrs"],
            "lane_profile": data["lane_profile"],
            "toll_charges_inr": data["toll_charges_inr"],
            "fuel_liters": fuel_liters,
            "fuel_cost_inr": fuel_cost,
            "driver_allowance_inr": driver_allowance,
            "total_logistics_cost_inr": total_trip_cost,
            "cost_per_ton_km": round(total_trip_cost / (dist * payload_tons), 2) if payload_tons > 0 else 0,
            "terrain": data["terrain"],
            "monsoon_risk": data["monsoon_flood_risk"],
            "recommended_vehicle": data["recommended_vehicle"],
            "speed_limit_kmh": data["speed_limit_kmh"]
        }

    def multi_district_network_plan(self, central_hub: str = "Changsari (Guwahati)", destinations: List[str] = None) -> List[Dict[str, Any]]:
        dests = destinations or ["Nagaon", "Dibrugarh"]
        network = []
        for d in dests:
            network.append(self.optimize_route(central_hub, d))
        return network

route_optimizer = RouteOptimizer()

