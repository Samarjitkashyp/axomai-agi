"""
Z16 Omni - Google Earth KML 3D Exporter & Multi-Hazard Geofence Breach Alert Engine.
Generates a Google Earth-compatible .kml file with target AOI pin, 18km hazard polygon ring,
and maritime corridor LineString, plus structured threshold breach alerts.
"""

import math
import uuid
from xml.sax.saxutils import escape
from typing import Dict, Any, List
from axomai.config import settings


class GeofenceAndKmlExporter:
    """Produces Google Earth .kml packages and evaluates multi-hazard threshold breaches."""

    def __init__(self):
        self.output_dir = settings.STORAGE_DIR / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def evaluate_breaches_and_export_kml(
        self,
        target_location: str,
        lat: float,
        lng: float,
        sar_flood: Dict[str, Any],
        thermal_data: Dict[str, Any],
        hydro_elev: Dict[str, Any],
        energy_risk: Dict[str, Any],
        disaster_feed: Dict[str, Any],
        ports: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        breaches: List[str] = []
        if "CRITICAL" in str(sar_flood.get("flood_severity_tier")) or "CRITICAL" in str(hydro_elev.get("hydro_flood_tier")):
            breaches.append("CRITICAL_FLOOD_GEOFENCE_BREACH")
        if float(thermal_data.get("evaporative_stress_index", 0.0)) > 0.45:
            breaches.append("PRE_DROUGHT_ESI_THRESHOLD_BREACH")
        if float(disaster_feed.get("max_magnitude_500km", 0.0)) >= 4.0:
            breaches.append(f"SEISMIC_ALERT_M{disaster_feed.get('max_magnitude_500km')}")
        if float(energy_risk.get("wind_gusts_10m_kmh", 0.0)) >= 45.0:
            breaches.append("HIGH_WIND_GUST_WARNING")
        if float(disaster_feed.get("atmospheric_aqi", {}).get("pm2_5", 0.0)) > 60.0:
            breaches.append("HIGH_AEROSOL_SMOKE_ALERT")

        # Build 18km radius circle polygon coordinates (lon,lat,0)
        ring_coords = []
        r_deg_lat = 18.0 / 111.0
        r_deg_lng = 18.0 / max(10.0, 111.0 * math.cos(math.radians(lat)))
        for deg in range(0, 361, 15):
            rad = math.radians(deg)
            ring_coords.append(f"{lng + r_deg_lng * math.cos(rad):.5f},{lat + r_deg_lat * math.sin(rad):.5f},0")
        ring_str = " ".join(ring_coords)

        port_placemarks = ""
        for p in ports[:6]:
            c = p.get("coordinates", {})
            if c.get("lat") is not None and c.get("lng") is not None:
                pname = escape(str(p.get("port_name", "Port")))
                cong = escape(str(p.get("congestion_index", "")))
                port_placemarks += (
                    f"<Placemark><name>{pname}</name><description>Congestion: {cong}</description>"
                    f"<Point><coordinates>{c['lng']},{c['lat']},0</coordinates></Point></Placemark>\n"
                )

        t_safe = escape(target_location)
        desc = escape(
            f"Geo-Risk: {energy_risk.get('composite_geo_risk_score')}/100 | "
            f"SAR: {sar_flood.get('flood_severity_tier')} | ESI: {thermal_data.get('evaporative_stress_index')}"
        )

        kml = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Z16 Omni — {t_safe}</name>
    <Placemark>
      <name>{t_safe} (Target AOI)</name>
      <description>{desc}</description>
      <Point><coordinates>{lng},{lat},0</coordinates></Point>
    </Placemark>
    <Placemark>
      <name>18km Hazard Geofence Ring</name>
      <Polygon><outerBoundaryIs><LinearRing><coordinates>{ring_str}</coordinates></LinearRing></outerBoundaryIs></Polygon>
    </Placemark>
    {port_placemarks}
  </Document>
</kml>"""

        fname = f"omni_earth_{uuid.uuid4().hex[:8]}.kml"
        fpath = self.output_dir / fname
        fpath.write_text(kml, encoding="utf-8")

        return {
            "active_breach_alerts": breaches,
            "breach_count": len(breaches),
            "kml_file": {"filename": fname, "file_path": str(fpath), "download_url": f"/api/download/generated/{fname}"},
        }


geofence_kml_exporter = GeofenceAndKmlExporter()
