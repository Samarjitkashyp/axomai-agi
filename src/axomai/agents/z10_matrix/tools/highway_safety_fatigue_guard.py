"""
Z10 Matrix - Highway Blackspot, Driver Fatigue & Wildlife Geofence AI Guard.
Enforces Motor Transport Workers Act continuous driving limits (mandatory 45-min rest
every 4.5 hrs, max 8-10 hrs driving/shift), flags MoRTH accident blackspots,
and enforces Assam Kaziranga / Elephant Corridor speed-camera geofences (40 km/h).
"""

import math
from typing import Dict, Any, List


class HighwaySafetyFatigueGuard:
    """Enforces driver HOS safety, MoRTH blackspot alerts, and wildlife corridor geofences."""

    def evaluate_route_safety(
        self,
        origin: str,
        destination: str,
        transit_hours: float,
        terrain: str = ""
    ) -> Dict[str, Any]:
        # Motor Transport Workers Act: max 4.5 hrs continuous driving before mandatory break
        mandatory_rest_stops = max(0, math.floor(transit_hours / 4.5))
        requires_dual_driver = transit_hours > 9.0
        rest_delay_hrs = round(mandatory_rest_stops * 0.75, 2)
        safe_total_eta_hrs = round(transit_hours + rest_delay_hrs, 1)

        geofence_alerts: List[str] = []
        route_str = f"{origin} {destination} {terrain}".lower()
        if any(k in route_str for k in ["dibrugarh", "jorhat", "kaziranga", "tezpur", "golaghat"]):
            geofence_alerts.append("KAZIRANGA_WILDLIFE_CORRIDOR: Strict 40 km/h ANPR camera geofence active (₹2,000-₹5,000 automated fine).")
        if any(k in route_str for k in ["silchar", "shillong", "sonapur", "jowai", "ghat"]):
            geofence_alerts.append("MORTH_GHAT_BLACKSPOT: Sonapur/Meghalaya steep gradient — engine braking & daytime convoy advised.")
        if not geofence_alerts:
            geofence_alerts.append("NHAI_STANDARD_BLACKSPOT_RADAR: Automated night-fatigue dashcam & 80 km/h speed governor active.")

        return {
            "statutory_act": "Motor Transport Workers Act & MoRTH Highway Safety Directive",
            "driving_hours_raw": transit_hours,
            "mandatory_rest_stops": mandatory_rest_stops,
            "dual_driver_relay_required": requires_dual_driver,
            "safe_adjusted_eta_hrs": safe_total_eta_hrs,
            "geofence_and_blackspot_alerts": geofence_alerts,
            "safety_compliance_status": "DUAL_DRIVER_MANDATED" if requires_dual_driver else "SINGLE_DRIVER_COMPLIANT"
        }


highway_safety_guard = HighwaySafetyFatigueGuard()
