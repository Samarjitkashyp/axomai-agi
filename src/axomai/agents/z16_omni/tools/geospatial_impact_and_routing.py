"""
Z16 Omni - Operational Impact, Highway Rerouting, Crop Yield & Maritime Demurrage Engine.
Translates satellite & AIS telemetry into concrete financial INR/USD impact and cascading alerts.
"""

from typing import Dict, Any, List


class GeospatialImpactAndRouting:
    """Computes supply-chain rerouting, crop yield risk, and vessel demurrage costs."""

    def evaluate_operational_impact(
        self,
        target_location: str,
        sar_flood: Dict[str, Any],
        sat_indices: Dict[str, Any],
        thermal_data: Dict[str, Any],
        port_cv: Dict[str, Any],
        ais_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        # 1. Flood Highway / Corridor Rerouting
        flood_tier = str(sar_flood.get("flood_severity_tier", "NORMAL_HYDROLOGY"))
        is_assam = any(k in target_location.lower() for k in ["assam", "guwahati", "kaziranga", "majuli", "dibrugarh", "nagaon", "brahmaputra", "silchar", "dhubri"])
        if is_assam:
            corridor = "NH-27 / NH-15 Brahmaputra Freight Corridor"
            alternate_route = "Changsari Logistics Hub -> North Bank NH-15 -> Bogibeel Bridge Bypass"
        else:
            corridor = f"{target_location} Primary Arterial & Port Rail Spur"
            alternate_route = f"Dedicated Freight Corridor (DFC) / Elevated Bypass around {target_location}"

        # 2. Crop Yield Risk (NDVI + ESI fusion)
        ndvi = float(sat_indices.get("indices", {}).get("ndvi_vegetation_health", {}).get("mean_index", 0.65))
        esi = float(thermal_data.get("evaporative_stress_index", 0.25))
        yield_risk_pct = round(min(45.0, max(2.0, (esi * 35.0) + max(0.0, (0.65 - ndvi) * 40.0))), 1)

        # 3. Maritime Demurrage & Bunker Financial Impact
        berth_wait_h = float(port_cv.get("estimated_berth_wait_hours", 14.0))
        eta_str = str(ais_data.get("eta_drift_delay_hours", "+0h")).replace("+", "").replace("h", "")
        try:
            eta_delay_h = float(eta_str) if eta_str != "ON_SCHEDULE" else 0.0
        except Exception:
            eta_delay_h = 6.0

        total_delay_days = round((berth_wait_h + eta_delay_h) / 24.0, 2)
        daily_charter_usd = 24000.0
        demurrage_usd = round(total_delay_days * daily_charter_usd, 0)
        demurrage_inr_lakhs = round((demurrage_usd * 84.5) / 100000.0, 2)

        # 4. Cascading Multi-Agent Alerts (for Master Orchestrator / Enterprise Ops)
        cascading_alerts: List[Dict[str, str]] = []
        if "CRITICAL" in flood_tier or "ELEVATED" in flood_tier:
            cascading_alerts.append({
                "target_agent": "Z10 Matrix",
                "trigger": flood_tier,
                "action": f"Reroute fleet from {corridor} to {alternate_route}",
            })
        if berth_wait_h > 20 or eta_delay_h > 12:
            cascading_alerts.append({
                "target_agent": "Z14 / Z13 Finance",
                "trigger": f"PORT_DELAY_{berth_wait_h}H",
                "action": f"Hedge INR {demurrage_inr_lakhs}L demurrage exposure (${int(demurrage_usd):,})",
            })
        if esi > 0.45:
            cascading_alerts.append({
                "target_agent": "Z8 Agri & Commodity",
                "trigger": f"ESI_STRESS_{esi}",
                "action": f"Mitigate {yield_risk_pct}% projected crop yield risk via drip irrigation",
            })

        return {
            "primary_corridor": corridor,
            "recommended_alternate_route": alternate_route,
            "crop_yield_loss_risk_pct": yield_risk_pct,
            "total_maritime_delay_days": total_delay_days,
            "estimated_demurrage_usd": demurrage_usd,
            "estimated_demurrage_inr_lakhs": demurrage_inr_lakhs,
            "cascading_alerts": cascading_alerts,
        }


geospatial_impact_routing = GeospatialImpactAndRouting()
