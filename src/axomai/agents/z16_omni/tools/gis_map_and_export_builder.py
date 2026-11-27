"""
Z16 Omni - Interactive Leaflet Satellite Map, Tactical GIS PNG, GeoJSON & Excel Builder.
Generates real downloadable GIS artifacts in storage/generated/.
"""

import json
import uuid
from typing import Dict, Any, List
from PIL import Image, ImageDraw
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from axomai.config import settings


class GISMapAndExportBuilder:
    """Produces interactive Leaflet HTML maps, Pillow GIS PNGs, GeoJSON, and Excel telemetry."""

    def __init__(self):
        self.output_dir = settings.STORAGE_DIR / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_interactive_leaflet_map(
        self,
        target_location: str,
        lat: float,
        lng: float,
        sar_flood: Dict[str, Any],
        thermal_data: Dict[str, Any],
        ports: List[Dict[str, Any]],
        change_30d: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Generates a standalone interactive Leaflet.js satellite + street map HTML file with maritime corridor."""
        fname = f"omni_map_{uuid.uuid4().hex[:8]}.html"
        fpath = self.output_dir / fname

        port_markers_js = ""
        route_pts = []
        for p in ports[:10]:
            c = p.get("coordinates", {})
            plat, plng = c.get("lat"), c.get("lng")
            if plat is not None and plng is not None:
                route_pts.append([plat, plng])
                pname = str(p.get("port_name", "Port")).replace("'", "")
                cong = str(p.get("congestion_index", "")).replace("'", "")
                port_markers_js += (
                    f"L.circleMarker([{plat}, {plng}], {{radius: 7, color: '#f59e0b', fillColor: '#fbbf24', fillOpacity: 0.85}})"
                    f".addTo(map).bindPopup('<b>{pname}</b><br/>Congestion: {cong}');\n"
                )

        c30 = change_30d or {}
        surge_txt = f"{c30.get('precip_surge_pct', 0.0):+.1f}%" if c30 else "N/A"
        verdict_txt = c30.get("change_verdict", "STABLE")

        flood_color = "#ef4444" if "CRITICAL" in str(sar_flood.get("flood_severity_tier", "")) else "#06b6d4"
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Z16 Omni Satellite GIS — {target_location}</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    body {{ margin: 0; font-family: system-ui, sans-serif; background: #020617; color: #f8fafc; }}
    #map {{ height: 100vh; width: 100vw; }}
    .hud {{ position: fixed; top: 14px; right: 14px; z-index: 999; background: rgba(15, 23, 42, 0.92);
            border: 1px solid #0ea5e9; border-radius: 10px; padding: 12px 16px; max-width: 340px; font-size: 12px; }}
    .hud h3 {{ margin: 0 0 6px; color: #38bdf8; font-size: 14px; }}
  </style>
</head>
<body>
  <div class="hud">
    <h3>🛰️ Z16 Omni Live GIS Telemetry</h3>
    <div><b>Target:</b> {target_location} ({lat:.4f}, {lng:.4f})</div>
    <div><b>SAR Flood Tier:</b> {sar_flood.get('flood_severity_tier')} ({sar_flood.get('inundation_expansion_pct')})</div>
    <div><b>30D Rain Surge:</b> {surge_txt} ({verdict_txt})</div>
    <div><b>Thermal ESI:</b> {thermal_data.get('evaporative_stress_index')} ({thermal_data.get('stress_tier')})</div>
    <div><b>LST:</b> {thermal_data.get('derived_land_surface_temp')}</div>
  </div>
  <div id="map"></div>
  <script>
    const esriSat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{ attribution: 'Esri World Imagery' }});
    const osm = L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{ attribution: 'OpenStreetMap' }});
    const map = L.map('map', {{ center: [{lat}, {lng}], zoom: 8, layers: [esriSat] }});
    L.control.layers({{ 'Satellite Imagery': esriSat, 'Street Map': osm }}).addTo(map);
    L.marker([{lat}, {lng}]).addTo(map).bindPopup('<b>{target_location}</b><br/>SAR: {sar_flood.get("flood_severity_tier")}<br/>ESI: {thermal_data.get("evaporative_stress_index")}').openPopup();
    L.circle([{lat}, {lng}], {{ radius: 18000, color: '{flood_color}', fillColor: '{flood_color}', fillOpacity: 0.18 }}).addTo(map);
    L.polyline({json.dumps(route_pts[:4])}, {{ color: '#38bdf8', weight: 2, dashArray: '6, 6' }}).addTo(map);
    {port_markers_js}
  </script>
</body>
</html>"""
        fpath.write_text(html, encoding="utf-8")
        return {"filename": fname, "file_path": str(fpath), "download_url": f"/api/download/generated/{fname}"}

    def create_tactical_gis_png(
        self,
        target_location: str,
        lat: float,
        lng: float,
        live_weather: Dict[str, Any],
        sar_flood: Dict[str, Any],
        thermal_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generates a 1000x520 tactical radar & thermal GIS summary PNG."""
        w, h = 1000, 520
        img = Image.new("RGB", (w, h), (8, 16, 30))
        draw = ImageDraw.Draw(img)

        for x in range(60, w - 40, 80):
            draw.line([(x, 70), (x, h - 50)], fill=(22, 38, 62), width=1)
        for y in range(70, h - 40, 60):
            draw.line([(60, y), (w - 40, y)], fill=(22, 38, 62), width=1)

        cx, cy = 480, 270
        for r in [45, 95, 145, 195]:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(14, 116, 144), width=2)
        draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(34, 211, 238), outline=(255, 255, 255), width=2)

        draw.text((40, 22), f"Z16 OMNI TACTICAL GIS RADAR — {target_location.upper()} ({lat:.3f}, {lng:.3f})", fill=(56, 189, 248))
        draw.text((60, 85), f"SOURCE: {live_weather.get('source')}", fill=(16, 185, 129))
        draw.text((60, 110), f"CLOUD COVER: {live_weather.get('cloud_cover_pct')}% | RAIN 7D: {live_weather.get('precip_7d_total_mm')} mm", fill=(226, 232, 240))
        draw.text((60, 135), f"SOIL MOISTURE: {live_weather.get('soil_moisture_pct')}% | LST: {thermal_data.get('derived_land_surface_temp')}", fill=(251, 191, 36))
        draw.text((60, 160), f"SAR FLOOD TIER: {sar_flood.get('flood_severity_tier')} ({sar_flood.get('inundation_expansion_pct')})", fill=(248, 113, 113))
        draw.text((60, 185), f"ESI DROUGHT INDEX: {thermal_data.get('evaporative_stress_index')} ({thermal_data.get('stress_tier')})", fill=(167, 139, 250))

        fname = f"omni_gis_{uuid.uuid4().hex[:8]}.png"
        fpath = self.output_dir / fname
        img.save(str(fpath))
        return {"filename": fname, "file_path": str(fpath), "download_url": f"/api/download/generated/{fname}"}

    def create_geojson_export(
        self,
        target_location: str,
        lat: float,
        lng: float,
        sar_flood: Dict[str, Any],
        thermal_data: Dict[str, Any],
        ports: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Exports target AOI + port network as standard GeoJSON."""
        features = [{
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lng, lat]},
            "properties": {
                "name": target_location,
                "role": "TARGET_AOI",
                "sar_flood_tier": sar_flood.get("flood_severity_tier"),
                "esi": thermal_data.get("evaporative_stress_index"),
                "lst": thermal_data.get("derived_land_surface_temp"),
            }
        }]
        for p in ports[:10]:
            c = p.get("coordinates", {})
            if c.get("lat") is not None and c.get("lng") is not None:
                features.append({
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [c["lng"], c["lat"]]},
                    "properties": {"name": p.get("port_name"), "congestion": p.get("congestion_index")}
                })
        fname = f"omni_geo_{uuid.uuid4().hex[:8]}.geojson"
        fpath = self.output_dir / fname
        fpath.write_text(json.dumps({"type": "FeatureCollection", "features": features}, indent=2), encoding="utf-8")
        return {"filename": fname, "file_path": str(fpath), "download_url": f"/api/download/generated/{fname}"}

    def create_telemetry_excel(
        self,
        target_location: str,
        live_weather: Dict[str, Any],
        ports: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generates a multi-sheet Excel telemetry workbook with live 7-day precip/ET0 & port matrix."""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "7-Day Earth Telemetry"
        header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
        header_font = Font(color="38BDF8", bold=True)

        ws.append(["Target Location", target_location, "Data Source", live_weather.get("source")])
        ws.append([])
        ws.append(["Date", "Precipitation (mm)", "ET0 Evapotranspiration (mm)", "Water Balance (Precip - ET0)"])
        for cell in ws[3]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center")

        dates = live_weather.get("dates_7d") or []
        precips = live_weather.get("precip_7d_mm") or []
        et0s = live_weather.get("et0_7d_mm") or []
        for idx, d in enumerate(dates[:7]):
            r = idx + 4
            p_val = precips[idx] if idx < len(precips) else 0.0
            e_val = et0s[idx] if idx < len(et0s) else 4.0
            ws.append([d, p_val, e_val, f"=B{r}-C{r}"])

        ws2 = wb.create_sheet("Maritime Port Hubs")
        ws2.append(["Port Name", "Country", "Throughput", "Chokepoint", "Congestion Index"])
        for cell in ws2[1]:
            cell.fill = header_fill
            cell.font = header_font
        for p in ports:
            ws2.append([p.get("port_name"), p.get("country"), p.get("annual_throughput_teu"), p.get("key_chokepoint"), p.get("congestion_index")])

        fname = f"omni_telemetry_{uuid.uuid4().hex[:8]}.xlsx"
        fpath = self.output_dir / fname
        wb.save(str(fpath))
        return {"filename": fname, "file_path": str(fpath), "download_url": f"/api/download/generated/{fname}"}


gis_map_export_builder = GISMapAndExportBuilder()
