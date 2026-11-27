"""
Z16 Omni - Executive Geospatial & Multi-Hazard Intelligence Briefing (.docx) Builder.
Generates a boardroom-ready Word report embedding live telemetry tables,
Tactical SAR/ESI Radar PNG, and 30-Day Change Detection Trendline PNG.
"""

import uuid
from pathlib import Path
from typing import Dict, Any
from docx import Document
from docx.shared import Inches
from axomai.config import settings


class GeospatialDocxBriefing:
    """Produces downloadable Word (.docx) Geospatial Intelligence Briefings."""

    def __init__(self):
        self.output_dir = settings.STORAGE_DIR / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_briefing_docx(
        self,
        target_location: str,
        geo: Dict[str, Any],
        sar_flood: Dict[str, Any],
        thermal_data: Dict[str, Any],
        hydro_elev: Dict[str, Any],
        energy_risk: Dict[str, Any],
        disaster_feed: Dict[str, Any],
        marine_state: Dict[str, Any],
        impact_res: Dict[str, Any],
        tactical_png_path: str,
        trend_png_path: str,
    ) -> Dict[str, Any]:
        doc = Document()
        doc.add_heading(f"Z16 Omni: Geospatial & Satellite Intelligence Briefing — {target_location}", level=0)
        doc.add_paragraph(
            f"Coordinates: {geo['lat']:.4f}, {geo['lng']:.4f} ({geo['region_label']}) | "
            f"Composite Geo-Risk Score: {energy_risk['composite_geo_risk_score']}/100 ({energy_risk['composite_risk_grade']})"
        )

        # 1. Live Multi-Sensor Matrix
        doc.add_heading("1. Live Earth, Hydrological & Marine Telemetry", level=1)
        rows = [
            ("Elevation & GloFAS River Discharge", f"{hydro_elev['elevation_meters_asl']} m ASL | {hydro_elev['river_discharge_today_m3s']} m3/s ({hydro_elev['hydro_flood_tier']})"),
            ("Sentinel-1 SAR Flood Expansion", f"{sar_flood['flood_severity_tier']} ({sar_flood['inundation_expansion_pct']}, {sar_flood['net_submerged_land_sqkm']} sq km)"),
            ("Thermal ESI (Pre-Drought)", f"ESI {thermal_data['evaporative_stress_index']} | LST {thermal_data['derived_land_surface_temp']} ({thermal_data['stress_tier']})"),
            ("Seismic (500km USGS)", f"{disaster_feed['earthquake_count_500km']} events | Max M{disaster_feed['max_magnitude_500km']} ({disaster_feed['seismic_tier']})"),
            ("Atmospheric Aerosol / Smoke", f"PM2.5 {disaster_feed['atmospheric_aqi']['pm2_5']} ug/m3 ({disaster_feed['atmospheric_aqi']['smoke_haze_tier']})"),
            ("Solar PV & Wind Gusts", f"{energy_risk['solar_pv_yield_kwh_kwp_day']} kWh/kWp/day | Gusts {energy_risk['wind_gusts_10m_kmh']} km/h ({energy_risk['wind_safety_tier']})"),
            ("Marine Sea-State", f"{marine_state['port_monitored']}: Wave {marine_state['wave_height_m']}m, Swell {marine_state['swell_height_m']}m ({marine_state['berthing_safety_tier']})"),
        ]
        table = doc.add_table(rows=1, cols=2)
        table.style = "Table Grid"
        hdr = table.rows[0].cells
        hdr[0].text = "Telemetry Domain"
        hdr[1].text = "Observed Live Metric & Tier"
        for k, v in rows:
            c = table.add_row().cells
            c[0].text = k
            c[1].text = v

        # 2. Operational & Financial Impact
        doc.add_heading("2. Supply Chain Rerouting & Financial Impact", level=1)
        doc.add_paragraph(f"Primary Corridor: {impact_res['primary_corridor']}")
        doc.add_paragraph(f"Recommended Alternate Route: {impact_res['recommended_alternate_route']}")
        doc.add_paragraph(
            f"Crop Yield Loss Risk: {impact_res['crop_yield_loss_risk_pct']}% | "
            f"Maritime Demurrage Exposure: INR {impact_res['estimated_demurrage_inr_lakhs']} Lakhs (${int(impact_res['estimated_demurrage_usd']):,})"
        )

        # 3. Visual GIS Maps & Trendline
        doc.add_heading("3. Tactical GIS Radar & 30-Day Change Detection", level=1)
        if tactical_png_path and Path(tactical_png_path).exists():
            doc.add_picture(tactical_png_path, width=Inches(6.0))
        if trend_png_path and Path(trend_png_path).exists():
            doc.add_picture(trend_png_path, width=Inches(6.0))

        fname = f"omni_briefing_{uuid.uuid4().hex[:8]}.docx"
        fpath = self.output_dir / fname
        doc.save(str(fpath))
        return {"filename": fname, "file_path": str(fpath), "download_url": f"/api/download/generated/{fname}"}


geospatial_docx_briefing = GeospatialDocxBriefing()
