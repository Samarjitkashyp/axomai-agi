"""
Z16 Omni - Executive HTML5 Geospatial Command Dashboard (.html) Builder.
Produces a standalone Tailwind + Chart.js interactive dashboard visualizing
7-Day Precipitation vs ET0, Multi-Hazard Risk Breakdown, and Live Telemetry KPIs.
"""

import json
import uuid
from typing import Dict, Any
from axomai.config import settings


class GeospatialHtml5Dashboard:
    """Produces standalone interactive HTML5 Geospatial Command Dashboards."""

    def __init__(self):
        self.output_dir = settings.STORAGE_DIR / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_command_dashboard_html(
        self,
        target_location: str,
        geo: Dict[str, Any],
        live_weather: Dict[str, Any],
        sar_flood: Dict[str, Any],
        thermal_data: Dict[str, Any],
        hydro_elev: Dict[str, Any],
        energy_risk: Dict[str, Any],
        disaster_feed: Dict[str, Any],
        marine_state: Dict[str, Any],
        leaflet_url: str,
    ) -> Dict[str, Any]:
        dates = live_weather.get("dates_7d") or ["D1", "D2", "D3", "D4", "D5", "D6", "D7"]
        precip = live_weather.get("precip_7d_mm") or [0.0] * 7
        et0 = live_weather.get("et0_7d_mm") or [4.0] * 7

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Z16 Omni Command Center — {target_location}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen p-6 font-sans">
  <div class="max-w-6xl mx-auto space-y-6">
    <div class="flex flex-wrap items-center justify-between border-b border-slate-800 pb-4">
      <div>
        <h1 class="text-2xl font-bold text-cyan-400">🛰️ Z16 Omni Geospatial Command Dashboard</h1>
        <p class="text-sm text-slate-400">{target_location} ({geo['region_label']}) • {geo['lat']:.4f}, {geo['lng']:.4f}</p>
      </div>
      <a href="{leaflet_url}" class="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-xs font-semibold text-white">Open Interactive Satellite Map</a>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
        <div class="text-xs text-slate-400">Composite Geo-Risk</div>
        <div class="text-2xl font-bold text-amber-400">{energy_risk['composite_geo_risk_score']}/100</div>
        <div class="text-xs text-slate-400">{energy_risk['composite_risk_grade']}</div>
      </div>
      <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
        <div class="text-xs text-slate-400">SAR Flood & Elevation</div>
        <div class="text-lg font-bold text-cyan-300">{sar_flood['flood_severity_tier']}</div>
        <div class="text-xs text-slate-400">{hydro_elev['elevation_meters_asl']} m ASL | {hydro_elev['river_discharge_today_m3s']} m³/s</div>
      </div>
      <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
        <div class="text-xs text-slate-400">Thermal ESI & Solar PV</div>
        <div class="text-lg font-bold text-emerald-400">ESI {thermal_data['evaporative_stress_index']}</div>
        <div class="text-xs text-slate-400">{energy_risk['solar_pv_yield_kwh_kwp_day']} kWh/kWp/day</div>
      </div>
      <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
        <div class="text-xs text-slate-400">Seismic / AQI / Marine</div>
        <div class="text-lg font-bold text-indigo-300">M{disaster_feed['max_magnitude_500km']} | PM2.5 {disaster_feed['atmospheric_aqi']['pm2_5']}</div>
        <div class="text-xs text-slate-400">Wave {marine_state['wave_height_m']}m ({marine_state['berthing_safety_tier']})</div>
      </div>
    </div>

    <div class="p-5 rounded-xl bg-slate-900 border border-slate-800">
      <h2 class="text-sm font-semibold text-cyan-300 mb-3">7-Day Live Precipitation vs Evapotranspiration (ET0)</h2>
      <canvas id="hydroChart" height="100"></canvas>
    </div>
  </div>

  <script>
    new Chart(document.getElementById('hydroChart'), {{
      type: 'bar',
      data: {{
        labels: {json.dumps(dates[:7])},
        datasets: [
          {{ label: 'Precipitation (mm)', data: {json.dumps(precip[:7])}, backgroundColor: 'rgba(56, 189, 248, 0.75)' }},
          {{ label: 'ET0 Evapotranspiration (mm)', data: {json.dumps(et0[:7])}, type: 'line', borderColor: '#f59e0b', tension: 0.3 }}
        ]
      }},
      options: {{ responsive: true, scales: {{ y: {{ beginAtZero: true }} }} }}
    }});
  </script>
</body>
</html>"""

        fname = f"omni_dashboard_{uuid.uuid4().hex[:8]}.html"
        fpath = self.output_dir / fname
        fpath.write_text(html, encoding="utf-8")
        return {"filename": fname, "file_path": str(fpath), "download_url": f"/api/download/generated/{fname}"}


geospatial_html5_dashboard = GeospatialHtml5Dashboard()
