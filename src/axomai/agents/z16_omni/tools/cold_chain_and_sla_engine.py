"""
Z16 Omni - Geospatial Cold-Chain Thermal Spoilage & Logistics SLA Risk Engine.
Computes perishable/pharma spoilage risk, reefer cooling fuel penalty, and
corridor SLA delay buffers from live temperature, flood, and maritime delays.
"""

from typing import Dict, Any


class ColdChainAndSlaEngine:
    """Computes cold-chain spoilage risk and logistics SLA buffers."""

    def evaluate_cold_chain_and_sla(
        self,
        target_location: str,
        live_weather: Dict[str, Any],
        sar_flood: Dict[str, Any],
        impact_res: Dict[str, Any],
    ) -> Dict[str, Any]:
        temp_c = float(live_weather.get("temperature_c", 26.0))
        flood_tier = str(sar_flood.get("flood_severity_tier", "NORMAL_HYDROLOGY"))
        delay_days = float(impact_res.get("total_maritime_delay_days", 1.0))

        # Reefer thermal load increases above 25C
        thermal_load_pct = round(max(5.0, min(65.0, (temp_c - 18.0) * 1.8 + delay_days * 4.5)), 1)
        flood_delay_hrs = 18.0 if "CRITICAL" in flood_tier else (8.0 if "ELEVATED" in flood_tier else 2.0)
        sla_breach_prob = round(min(95.0, max(5.0, (delay_days * 15.0) + flood_delay_hrs * 1.5)), 1)
        recommended_buffer_hrs = int(round(flood_delay_hrs + (delay_days * 6.0)))

        return {
            "target_location": target_location,
            "cold_chain_spoilage_risk_pct": thermal_load_pct,
            "logistics_sla_breach_prob_pct": sla_breach_prob,
            "recommended_dispatch_buffer_hrs": recommended_buffer_hrs,
        }


cold_chain_sla_engine = ColdChainAndSlaEngine()
