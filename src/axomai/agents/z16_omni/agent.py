"""
Z16 Omni - Global Geospatial & Satellite Vision Intelligence Agent.
Orchestrates multi-constellation Earth observation, Sentinel-1 SAR cloud-penetrating radar,
satellite computer vision object counting, marine AIS vessel tracking, and thermal evaporative stress.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from pathlib import Path
from axomai.core.llm import llm_brain
from axomai.agents.z16_omni.tools.geo_extractor_and_live_apis import geo_extractor_and_live_apis
from axomai.agents.z16_omni.tools.gis_map_and_export_builder import gis_map_export_builder
from axomai.agents.z16_omni.tools.change_detection_engine import change_detection_engine
from axomai.agents.z16_omni.tools.geospatial_impact_and_routing import geospatial_impact_routing
from axomai.agents.z16_omni.tools.disaster_telemetry_feed import disaster_telemetry_feed
from axomai.agents.z16_omni.tools.multi_site_comparator import multi_site_comparator
from axomai.agents.z16_omni.tools.river_discharge_and_elevation import river_discharge_elevation
from axomai.agents.z16_omni.tools.solar_wind_and_energy_grid import solar_wind_energy_grid
from axomai.agents.z16_omni.tools.satellite_orbit_and_pass import satellite_orbit_pass
from axomai.agents.z16_omni.tools.marine_ocean_state import marine_ocean_state
from axomai.agents.z16_omni.tools.geospatial_docx_briefing import geospatial_docx_briefing
from axomai.agents.z16_omni.tools.geospatial_html5_dashboard import geospatial_html5_dashboard
from axomai.agents.z16_omni.tools.geofence_and_kml_exporter import geofence_kml_exporter
from axomai.agents.z16_omni.tools.carbon_and_agronomy_engine import carbon_agronomy_engine
from axomai.agents.z16_omni.tools.aviation_drone_corridor import aviation_drone_corridor
from axomai.agents.z16_omni.tools.urban_heat_and_site_suitability import urban_heat_site_suitability
from axomai.agents.z16_omni.tools.parametric_insurance_trigger import parametric_insurance_trigger
from axomai.agents.z16_omni.tools.cold_chain_and_sla_engine import cold_chain_sla_engine
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
        geo = geo_extractor_and_live_apis.extract_geo_intent(query)
        target_loc = geo["target_location"]
        lat, lng = geo["lat"], geo["lng"]
        live_weather = geo["live_weather"]
        stac_scene = geo["stac_scene"]

        yield {
            "type": "status",
            "stage": "satellite_telemetry_analysis",
            "message": f"🛰️ Z16 Omni: Fetching live Open-Meteo + STAC satellite pass for {target_loc} ({lat:.3f}, {lng:.3f})..."
        }

        # 1. Live-Calibrated Optical Multispectral Indices & Port Hubs
        sat_indices = satellite_analytics.evaluate_satellite_indices(
            region_name=target_loc,
            cloud_cover_pct=live_weather["cloud_cover_pct"],
            soil_moisture_pct=live_weather["soil_moisture_pct"],
            precip_7d_mm=live_weather["precip_7d_total_mm"],
            stac_scene=stac_scene,
        )
        ports = geospatial_engine.get_port_telemetry(query)

        # 2. Cloud-Penetrating Sentinel-1 SAR Radar Analysis (Live Rain + Soil Moisture)
        sar_flood = sar_radar_analytics.analyze_sar_flood_inundation(
            region_name=target_loc,
            cloud_cover_pct=live_weather["cloud_cover_pct"],
            precip_7d_mm=live_weather["precip_7d_total_mm"],
            soil_moisture_pct=live_weather["soil_moisture_pct"],
            stac_scene=stac_scene,
        )

        # 3. Dynamic Port Container & Refinery Tank Shadow Trigonometry (using real astronomical solar angle)
        orbit_pass = satellite_orbit_pass.compute_orbital_pass_and_solar_angle(lat, lng, target_loc)
        port_cv = satellite_cv_counter.detect_port_container_density(geo["port_key"])
        oil_tank = satellite_cv_counter.compute_oil_tank_fill_level(
            geo["tank_key"], solar_elevation_deg=orbit_pass["solar_elevation_deg"]
        )

        # 4. Dynamic Marine AIS Tracking & Live Ocean Sea-State
        ais_data = maritime_ais_tracker.track_vessel_telemetry(geo["vessel_key"])
        marine_state = marine_ocean_state.fetch_marine_sea_state(ports, target_loc)

        # 5. True Planck + Live ET0 Thermal Evaporative Stress (Pre-Drought)
        thermal_data = thermal_stress_engine.compute_evaporative_stress(
            biome_id=geo["biome_key"],
            live_temp_c=live_weather["temperature_c"],
            live_et0_mm=live_weather["et0_today_mm"],
            soil_moisture_pct=live_weather["soil_moisture_pct"],
        )

        # 6. 30-Day Historical Anomaly & Change Detection + Operational/Financial Impact
        change_30d = change_detection_engine.analyze_30d_anomaly(target_loc, lat, lng)
        impact_res = geospatial_impact_routing.evaluate_operational_impact(
            target_location=target_loc, sar_flood=sar_flood, sat_indices=sat_indices,
            thermal_data=thermal_data, port_cv=port_cv, ais_data=ais_data
        )
        disaster_feed = disaster_telemetry_feed.fetch_seismic_and_aqi(lat, lng, target_loc)
        hydro_elev = river_discharge_elevation.fetch_hydrology_and_elevation(lat, lng, target_loc)
        energy_risk = solar_wind_energy_grid.evaluate_energy_and_composite_risk(
            lat=lat, lng=lng, target_location=target_loc,
            sar_flood=sar_flood, thermal_data=thermal_data, disaster_feed=disaster_feed
        )
        multi_site = multi_site_comparator.compare_sites(query)

        # 7. Optional Uploaded Aerial/Satellite Image CV Analysis
        uploaded_cv = None
        img_m = re.search(r'([A-Za-z0-9_\\/:.\-]+\.(?:png|jpg|jpeg|webp))', query or "", re.IGNORECASE)
        if img_m and Path(img_m.group(1)).exists():
            uploaded_cv = satellite_cv_counter.analyze_uploaded_image(img_m.group(1))

        # 8. Generate Downloadable Interactive Leaflet Map, Tactical GIS PNG, GeoJSON & Excel
        leaflet_map = gis_map_export_builder.create_interactive_leaflet_map(
            target_location=target_loc, lat=lat, lng=lng,
            sar_flood=sar_flood, thermal_data=thermal_data, ports=ports, change_30d=change_30d
        )
        tactical_png = gis_map_export_builder.create_tactical_gis_png(
            target_location=target_loc, lat=lat, lng=lng,
            live_weather=live_weather, sar_flood=sar_flood, thermal_data=thermal_data
        )
        geojson_res = gis_map_export_builder.create_geojson_export(
            target_location=target_loc, lat=lat, lng=lng,
            sar_flood=sar_flood, thermal_data=thermal_data, ports=ports
        )
        excel_res = gis_map_export_builder.create_telemetry_excel(
            target_location=target_loc, live_weather=live_weather, ports=ports
        )
        docx_res = geospatial_docx_briefing.create_briefing_docx(
            target_location=target_loc, geo=geo, sar_flood=sar_flood, thermal_data=thermal_data,
            hydro_elev=hydro_elev, energy_risk=energy_risk, disaster_feed=disaster_feed,
            marine_state=marine_state, impact_res=impact_res,
            tactical_png_path=tactical_png["file_path"],
            trend_png_path=change_30d["trend_chart"]["file_path"],
        )
        dashboard_res = geospatial_html5_dashboard.create_command_dashboard_html(
            target_location=target_loc, geo=geo, live_weather=live_weather, sar_flood=sar_flood,
            thermal_data=thermal_data, hydro_elev=hydro_elev, energy_risk=energy_risk,
            disaster_feed=disaster_feed, marine_state=marine_state, leaflet_url=leaflet_map["download_url"],
        )
        geofence_res = geofence_kml_exporter.evaluate_breaches_and_export_kml(
            target_location=target_loc, lat=lat, lng=lng, sar_flood=sar_flood,
            thermal_data=thermal_data, hydro_elev=hydro_elev, energy_risk=energy_risk,
            disaster_feed=disaster_feed, ports=ports,
        )
        carbon_agro = carbon_agronomy_engine.evaluate_carbon_and_agronomy(
            target_location=target_loc, sat_indices=sat_indices,
            live_weather=live_weather, thermal_data=thermal_data,
        )
        drone_corridor = aviation_drone_corridor.evaluate_drone_flight_window(
            target_location=target_loc, live_weather=live_weather,
            energy_risk=energy_risk, hydro_elev=hydro_elev,
        )
        site_suit = urban_heat_site_suitability.evaluate_site_suitability(
            target_location=target_loc, live_weather=live_weather,
            thermal_data=thermal_data, hydro_elev=hydro_elev, energy_risk=energy_risk,
        )
        insurance_trig = parametric_insurance_trigger.evaluate_parametric_triggers(
            target_location=target_loc, live_weather=live_weather,
            hydro_elev=hydro_elev, thermal_data=thermal_data,
            disaster_feed=disaster_feed, energy_risk=energy_risk,
        )
        cold_sla = cold_chain_sla_engine.evaluate_cold_chain_and_sla(
            target_location=target_loc, live_weather=live_weather,
            sar_flood=sar_flood, impact_res=impact_res,
        )

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "GLOBAL_GEOSPATIAL_AND_SATELLITE_VISION",
            "geo_target": {"location": target_loc, "region": geo["region_label"], "lat": lat, "lng": lng},
            "live_weather": live_weather,
            "stac_scene": stac_scene,
            "change_detection_30d": change_30d,
            "operational_impact": impact_res,
            "seismic_and_aqi": disaster_feed,
            "river_discharge_and_elevation": hydro_elev,
            "solar_wind_and_composite_risk": energy_risk,
            "orbital_telemetry": orbit_pass,
            "multi_site_comparison": multi_site,
            "uploaded_image_cv": uploaded_cv,
            "optical_indices": sat_indices,
            "maritime_chokepoints": ports,
            "sar_radar_inundation": sar_flood,
            "satellite_cv_port": port_cv,
            "satellite_cv_oil": oil_tank,
            "ais_vessel_telemetry": ais_data,
            "marine_sea_state": marine_state,
            "thermal_evaporative_stress": thermal_data,
            "interactive_map": leaflet_map,
            "tactical_gis_png": tactical_png,
            "change_trend_png": change_30d["trend_chart"],
            "geojson_export": geojson_res,
            "excel_telemetry": excel_res,
            "docx_briefing": docx_res,
            "html5_dashboard": dashboard_res,
            "geofence_and_kml": geofence_res,
            "carbon_and_agronomy": carbon_agro,
            "aviation_drone_corridor": drone_corridor,
            "urban_heat_and_site_suitability": site_suit,
            "parametric_insurance_trigger": insurance_trig,
            "cold_chain_and_sla": cold_sla,
            "tools_used": [
                "geo_extractor_and_live_apis", "gis_map_export_builder",
                "change_detection_engine", "geospatial_impact_routing",
                "disaster_telemetry_feed", "multi_site_comparator", "river_discharge_elevation",
                "solar_wind_energy_grid", "satellite_orbit_pass", "marine_ocean_state",
                "geospatial_docx_briefing", "geospatial_html5_dashboard", "geofence_kml_exporter",
                "carbon_agronomy_engine", "aviation_drone_corridor", "urban_heat_site_suitability",
                "parametric_insurance_trigger", "cold_chain_sla_engine",
                "geospatial_engine", "satellite_analytics", "sar_radar_analytics",
                "satellite_cv_counter", "maritime_ais_tracker", "thermal_evaporative_stress"
            ]
        }
        yield meta_event

        multi_site_md = ""
        if multi_site:
            rows = "\n".join(
                f"| **{s['location']}** ({s['region']}) | {s['temp_c']}°C | {s['precip_7d_mm']} mm | {s['soil_moisture_pct']}% | **{s['composite_risk_score']}** |"
                for s in multi_site
            )
            multi_site_md = (
                f"\n#### 📍 Multi-Site Live Risk Ranking\n\n"
                f"| Location | Temp | 7D Rain | Soil Moisture | Composite Risk Score |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
                f"{rows}\n"
            )

        aqi = disaster_feed["atmospheric_aqi"]
        eonet_str = ", ".join(e.get("title", "") for e in (disaster_feed.get("nasa_eonet_active_events") or [])[:2]) or "None active"
        download_banner = (
            f"\n\n### 🗺️ Downloadable GIS & Satellite Artifacts ({target_loc})\n\n"
            f"- 🌐 **[Open Interactive Satellite & Port Map (.html)]({leaflet_map['download_url']})**\n"
            f"- 🎛️ **[Open Executive GIS Command Dashboard (.html)]({dashboard_res['download_url']})**\n"
            f"- 📡 **[Download Tactical SAR/ESI GIS Radar (.png)]({tactical_png['download_url']})**\n"
            f"- 📈 **[Download 30-Day Change Detection Chart (.png)]({change_30d['trend_chart']['download_url']})**\n"
            f"- 📊 **[Download 7-Day Telemetry & Port Workbook (.xlsx)]({excel_res['download_url']})**\n"
            f"- 📄 **[Download Executive GIS Intelligence Briefing (.docx)]({docx_res['download_url']})**\n"
            f"- 🧭 **[Download QGIS / ArcGIS Vector Layer (.geojson)]({geojson_res['download_url']})**\n"
            f"- 🌍 **[Download Google Earth 3D Package (.kml)]({geofence_res['kml_file']['download_url']})**\n\n"
            f"#### ⚡ Operational, Hydrological, Seismic & Atmospheric Telemetry\n"
            f"- **Composite Geo-Risk Score:** `{energy_risk['composite_geo_risk_score']}/100` (`{energy_risk['composite_risk_grade']}`) | **Solar PV Yield:** `{energy_risk['solar_pv_yield_kwh_kwp_day']} kWh/kWp/day` | **Wind Gusts:** `{energy_risk['wind_gusts_10m_kmh']} km/h` (`{energy_risk['wind_safety_tier']}`)\n"
            f"- **Live LEO Orbit & Solar Angle:** `{orbit_pass['leo_platform']}` @ `{orbit_pass['live_footprint_coords']}` (`{orbit_pass['ground_track_distance_km']} km` away, `{orbit_pass['source']}`) | Solar Elevation `{orbit_pass['solar_elevation_deg']}°`\n"
            f"- **Marine Sea-State ({marine_state['port_monitored']}):** Wave `{marine_state['wave_height_m']} m` | Swell `{marine_state['swell_height_m']} m` (`{marine_state['berthing_safety_tier']}` — `{marine_state['source']}`)\n"
            f"- **Terrain & River Discharge (GloFAS):** Elevation `{hydro_elev['elevation_meters_asl']} m ASL` | Discharge `{hydro_elev['river_discharge_today_m3s']} m³/s` (7D Max `{hydro_elev['river_discharge_7d_max_m3s']} m³/s` — `{hydro_elev['hydro_flood_tier']}`)\n"
            f"- **30D Rain Surge:** `{change_30d['precip_surge_pct']:+.1f}%` ({change_30d['change_verdict']})\n"
            f"- **Seismic (500km USGS):** `{disaster_feed['earthquake_count_500km']} events` (Max M`{disaster_feed['max_magnitude_500km']}` — `{disaster_feed['seismic_tier']}`)\n"
            f"- **NASA EONET Global Watch:** `{eonet_str}` (`{disaster_feed.get('eonet_source')}`)\n"
            f"- **Atmospheric Aerosol / Smoke:** `PM2.5 {aqi['pm2_5']} µg/m³` | `Dust {aqi['dust']}` (`{aqi['smoke_haze_tier']}` — `{aqi['source']}`)\n"
            f"- **Alternate Freight Route:** `{impact_res['recommended_alternate_route']}`\n"
            f"- **Crop Yield Risk:** `{impact_res['crop_yield_loss_risk_pct']}%` | **Carbon Credits:** `{carbon_agro['estimated_carbon_stock_tco2e_ha']} tCO2e/ha` (`INR {int(carbon_agro['carbon_credit_value_inr_ha']):,}/ha`) | **Agronomy Window:** `{carbon_agro['precision_agronomy_window']}`\n"
            f"- **UAV Drone Sortie:** `{drone_corridor['flight_status']}` (Max `{drone_corridor['recommended_altitude_agl_m']} m AGL`) | **Site Suitability:** `{site_suit['site_suitability_score']}/100` (`{site_suit['site_suitability_grade']}`) | **Parametric Insurance:** `{insurance_trig['trigger_status']}` (`{insurance_trig['recommended_payout_pct']}%`)\n"
            f"- **Cold-Chain Spoilage Risk:** `{cold_sla['cold_chain_spoilage_risk_pct']}%` | **SLA Buffer:** `+{cold_sla['recommended_dispatch_buffer_hrs']}h` | **Demurrage Exposure:** `INR {impact_res['estimated_demurrage_inr_lakhs']} Lakhs` (`${int(impact_res['estimated_demurrage_usd']):,}`)\n"
            f"{multi_site_md}"
        )

        prompt = (
            f"You are Z16 Omni, Chief Remote Sensing Scientist & Geospatial Intelligence Officer.\n"
            f"User Goal / Inquiry: '{query}'\n"
            f"Target Coordinates: {target_loc} ({geo['region_label']}) @ {lat:.4f}, {lng:.4f}\n"
            f"Live Earth Telemetry ({live_weather['source']}): Temp {live_weather['temperature_c']}°C, Cloud {live_weather['cloud_cover_pct']}%, 7D Rain {live_weather['precip_7d_total_mm']}mm, Soil Moisture {live_weather['soil_moisture_pct']}%, ET0 {live_weather['et0_today_mm']}mm\n"
            f"Latest Satellite Scene ({stac_scene['source']}): {stac_scene['scene_id']} ({stac_scene['datetime']})\n"
            f"Sentinel-1 SAR Flood Analysis: {sar_flood}\n"
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
            full_answer += download_banner
            for tok in download_banner.split(" "):
                yield {"type": "token", "content": tok + " "}
        else:
            full_answer = (
                f"### 🛰️ Z16 Omni: Live Geospatial & Satellite Vision Intelligence ({target_loc})\n\n"
                f"**Coordinates:** `{lat:.4f}, {lng:.4f}` ({geo['region_label']}) | **Telemetry:** `{live_weather['source']}` | **STAC Pass:** `{stac_scene['scene_id']}`\n\n"
                f"#### 🌍 Remote Sensing Telemetry & Computer Vision Matrix\n\n"
                f"| Sensor Platform | Spectral / Radar Band | Target Asset / Region | Metric Observed | Strategic Operational Implication |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
                f"| **Sentinel-1 C-SAR** | Microwave Dual-Pol (VV/VH) | {target_loc} | Backscatter Δ: {sar_flood['backscatter_change_ratio_db']} | {sar_flood['flood_severity_tier']}; {sar_flood['net_submerged_land_sqkm']} sq km expansion |\n"
                f"| **Optical CV 30cm** | Optical RGB/NIR | {port_cv['facility_id']} | {port_cv['detected_teu_count']:,} TEUs ({port_cv['yard_utilization_pct']}) | {port_cv['congestion_status']}; berth wait {port_cv['estimated_berth_wait_hours']}h |\n"
                f"| **Shadow Trig CV** | Optical Shadow Geometry | {oil_tank['facility']} | {oil_tank['tank_fill_level_pct']} Fill ({oil_tank['estimated_crude_stored_barrels']}) | {oil_tank['strategic_reserves_status']} |\n"
                f"| **Thermal + Open-Meteo** | TIRS + Live ET0 | {geo['biome_key']} | LST: {thermal_data['derived_land_surface_temp']} (ESI: {thermal_data['evaporative_stress_index']}) | {thermal_data['stress_tier']}; {thermal_data['agronomic_intervention']} |\n\n"
                f"#### 🚢 Marine AIS Vessel Tracking & Maritime Corridors\n\n"
                f"- **Monitored Vessel:** `{ais_data['vessel_name']}` ({ais_data['vessel_class']}) at `{ais_data['navigational_location']}`.\n"
                f"- **Speed Over Ground:** `{ais_data['speed_over_ground']}` | **ETA Drift:** `{ais_data['eta_drift_delay_hours']}` to `{ais_data['destination_port']}`.\n"
                f"{download_banner}"
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
