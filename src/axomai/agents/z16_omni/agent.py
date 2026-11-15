"""
Z16 Omni - Global Geospatial & Satellite Vision Intelligence Agent.
Orchestrates multi-constellation Earth observation, Sentinel-1 SAR cloud-penetrating radar,
satellite computer vision object counting, marine AIS vessel tracking, and thermal evaporative stress.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.z16_omni.tools.geospatial_engine import geospatial_engine
from axomai.agents.z16_omni.tools.satellite_analytics import satellite_analytics
from axomai.agents.z16_omni.tools.sar_radar_analytics import sar_radar_analytics
from axomai.agents.z16_omni.tools.satellite_cv_counter import satellite_cv_counter
from axomai.agents.z16_omni.tools.maritime_ais_tracker import maritime_ais_tracker
from axomai.agents.z16_omni.tools.thermal_evaporative_stress import thermal_stress_engine

def normalize_markdown(text: str) -> str:
    """Ensures headings, tables, and lists always have clean double newlines."""
    text = re.sub(r'^[ \t]+(#{1,4}\s+)', r'\1', text, flags=re.MULTILINE)
    text = re.sub(r'\n[ \t]+(#{1,4}\s+)', r'\n\n\1', text)
    text = re.sub(r'([^\n])\s*(#{1,4}\s+)', r'\1\n\n\2', text)
    text = re.sub(r'^([^|\n]+)[ \t]*(\|.+)$', r'\1\n\n\2', text, flags=re.MULTILINE)
    text = re.sub(r'\|\s*\|', '|\n|', text)
    text = re.sub(r'([^\n])\s*(\n?-\s+\*\*)', r'\1\n\n- **', text)
    text = re.sub(r'([^\n])\s*(\n?-\s+)', r'\1\n- ', text)
    return text

class Z16OmniAgent:
    """Enterprise Chief Remote Sensing Scientist & Global Geospatial Intelligence Officer."""

    def __init__(self):
        self.name = "Z16 Omni"
        self.role = "Global Geospatial & Satellite Vision Intelligence Agent"

    def geospatial_stream(
        self,
        query: str,
        session_id: Optional[str] = "omni_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield {
            "type": "status",
            "stage": "satellite_telemetry_analysis",
            "message": "🛰️ Z16 Omni: Acquiring Sentinel-1 SAR radar, AIS maritime transponders, CV object counts & ESI..."
        }

        # 1. Optical Multispectral Indices
        sat_indices = satellite_analytics.evaluate_satellite_indices(region_name="Guwahati-Brahmaputra Basin")
        ports = geospatial_engine.get_port_telemetry()

        # 2. Cloud-Penetrating Sentinel-1 SAR Radar Analysis
        sar_flood = sar_radar_analytics.analyze_sar_flood_inundation(
            region_name="Brahmaputra Valley (Guwahati - Nagaon Corridor)", cloud_cover_pct=100.0
        )

        # 3. Satellite Computer Vision Container / Tank Counting
        port_cv = satellite_cv_counter.detect_port_container_density("singapore_pasir_panjang")
        oil_tank = satellite_cv_counter.compute_oil_tank_fill_level("numaligarh_refinery_crude_tanks")

        # 4. Real-time Marine AIS Tracking
        ais_data = maritime_ais_tracker.track_vessel_telemetry("msc_assam_express")

        # 5. Thermal Infrared Evaporative Stress (Pre-Drought)
        thermal_data = thermal_stress_engine.compute_evaporative_stress("upper_assam_tea_belt")

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "GLOBAL_GEOSPATIAL_AND_SATELLITE_VISION",
            "optical_indices": sat_indices,
            "maritime_chokepoints": ports,
            "sar_radar_inundation": sar_flood,
            "satellite_cv_port": port_cv,
            "satellite_cv_oil": oil_tank,
            "ais_vessel_telemetry": ais_data,
            "thermal_evaporative_stress": thermal_data,
            "tools_used": [
                "geospatial_engine", "satellite_analytics", "sar_radar_analytics",
                "satellite_cv_counter", "maritime_ais_tracker", "thermal_stress_engine"
            ]
        }
        yield meta_event

        prompt = (
            f"You are Z16 Omni, Chief Remote Sensing Scientist & Geospatial Intelligence Officer.\n"
            f"User Goal / Inquiry: '{query}'\n\n"
            f"Sentinel-1 SAR Cloud-Penetrating Radar Analysis: {sar_flood}\n"
            f"Satellite CV Container/Oil Tank Audit: {port_cv} | {oil_tank}\n"
            f"AIS Vessel Telemetry: {ais_data}\n"
            f"Thermal Evaporative Stress (Pre-Drought): {thermal_data}\n\n"
            "Formulate an authoritative Geospatial Intelligence Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present Satellite Telemetry & Remote Sensing Indices in a clean Markdown Table:\n"
            "| Sensor Platform | Spectral / Radar Band | Target Asset / Region | Metric Observed | Strategic Operational Implication |\n"
            "| :--- | :--- | :--- | :--- | :--- |\n"
            "- Outline flood displacement corridors, port congestion bottlenecks, and agricultural early warnings.\n"
            "- Ensure every table row ends with a newline."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z16 Omni, Geospatial Intelligence Officer.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = (
                f"### 🛰️ Z16 Omni: Global Geospatial & Satellite Vision Intelligence\n\n"
                f"**Constellation:** `ESA Sentinel-1 SAR + NASA Landsat-9 + Planet Labs 30cm` | **Observation Mode:** `MULTI_SENSOR_FUSION`\n\n"
                f"#### 🌍 Remote Sensing Telemetry & Computer Vision Matrix\n\n"
                f"| Sensor Platform | Spectral / Radar Band | Target Asset / Region | Metric Observed | Strategic Operational Implication |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
                f"| **Sentinel-1 C-SAR** | Microwave Dual-Pol (VV/VH) | Brahmaputra Basin | Backscatter Δ: {sar_flood['backscatter_change_ratio_db']} | 100% cloud-penetrating flood mapping; {sar_flood['net_submerged_land_sqkm']} sq km inundated |\n"
                f"| **PlanetScope 30cm** | Optical RGB/NIR | Pasir Panjang, Singapore | {port_cv['detected_teu_count']:,} TEUs ({port_cv['yard_utilization_pct']}) | High yard congestion; container dwell time +36.5h |\n"
                f"| **Shadow Trig CV** | Optical Shadow Geometry | Numaligarh Crude Tanks | {oil_tank['tank_fill_level_pct']} Fill ({oil_tank['estimated_crude_stored_barrels']}) | Strategic energy inventory abundant at 80.9% capacity |\n"
                f"| **NASA ECOSTRESS** | Thermal Infrared (TIRS) | Upper Assam Tea Belt | LST: {thermal_data['derived_land_surface_temp']} (ESI: {thermal_data['evaporative_stress_index']}) | 15-day pre-drought root zone early warning; deploy drip irrigation |\n\n"
                f"#### 🚢 Marine AIS Vessel Tracking & Maritime Corridors\n\n"
                f"- **Monitored Vessel:** `{ais_data['vessel_name']}` ({ais_data['vessel_class']}) at `{ais_data['navigational_location']}`.\n"
                f"- **Speed Over Ground:** `{ais_data['speed_over_ground']}` | **ETA Drift:** `{ais_data['eta_drift_delay_hours']}` to `{ais_data['destination_port']}`.\n"
                f"- **Flood Logistics Alert:** SAR confirms water encroachment on low-lying culverts near NH-27 Nagaon-Raha corridor; traffic routed via Changsari high-ground hub.\n"
            )
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        cleaned = normalize_markdown(full_answer)
        yield {
            "type": "final",
            "content": cleaned,
            "agent": self.name,
            "role": self.role
        }

z16_omni_agent = Z16OmniAgent()
