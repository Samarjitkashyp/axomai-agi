"""
Z10 Matrix - Port Congestion, Container Detention & Demurrage AI Shield.
Monitors Indian maritime gateways (Kolkata/Haldia, JNPT, Mundra, Chennai),
tracks statutory Free-Days countdown, computes daily container demurrage/detention
exposure in INR, and recommends inland ICD / empty-yard fast-track evacuation.
"""

from typing import Dict, Any


INDIAN_PORTS_BENCHMARK = {
    "kolkata": {"name": "Syama Prasad Mookerjee Port (Kolkata / Haldia)", "avg_dwell_days": 4.8, "free_days": 5, "daily_demurrage_inr": 4800.0},
    "mumbai": {"name": "JNPT / Nhava Sheva Port", "avg_dwell_days": 3.2, "free_days": 5, "daily_demurrage_inr": 5500.0},
    "chennai": {"name": "Chennai / Kamarajar Port", "avg_dwell_days": 3.5, "free_days": 5, "daily_demurrage_inr": 5000.0},
    "ahmedabad": {"name": "Mundra Port (APSEZ)", "avg_dwell_days": 2.4, "free_days": 5, "daily_demurrage_inr": 5200.0}
}


class PortDemurrageShieldEngine:
    """Calculates port dwell risk and protects against container detention penalties."""

    def evaluate_port_demurrage(
        self,
        origin: str,
        destination: str,
        containers_count: int = 2,
        days_elapsed_at_port: int = 3
    ) -> Dict[str, Any]:
        key = "kolkata"
        for k in INDIAN_PORTS_BENCHMARK:
            if k in origin.lower() or k in destination.lower():
                key = k
                break

        port = INDIAN_PORTS_BENCHMARK[key]
        free_days_left = max(0, port["free_days"] - days_elapsed_at_port)
        projected_excess_days = max(0.0, round((days_elapsed_at_port + port["avg_dwell_days"] * 0.5) - port["free_days"], 1))
        projected_penalty_inr = round(projected_excess_days * port["daily_demurrage_inr"] * containers_count, 2)

        return {
            "gateway_port": port["name"],
            "containers_count": containers_count,
            "free_days_allowance": port["free_days"],
            "free_days_remaining": free_days_left,
            "projected_demurrage_risk_inr": projected_penalty_inr,
            "evacuation_protocol": (
                "DIRECT_PORT_DELIVERY (DPD) + CONCOR Rail Evacuation triggered to prevent Free-Days breach."
                if free_days_left <= 2 else
                "ON_SCHEDULE: Clear customs within remaining Free-Days window."
            )
        }


port_demurrage_shield = PortDemurrageShieldEngine()
