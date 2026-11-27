"""
Z10 Matrix - 9-Tool Live Multimodal Logistics, Fleet Optimization & Supply Chain Commander.
Zero hardcoded dummy scenarios: uses live OSRM highway routing, OpenStreetMap Nominatim geocoding,
Open-Meteo live weather/flood telemetry, 2-Opt multi-stop VRP solver, 3D MoRTH axle-load optimizer,
CGST Rule 138 E-Way Bill calculator, Brahmaputra NW-2 / Rail CONCOR multimodal arbitrage,
Cold-Chain Q10 spoilage guard, and EV vs Diesel Scope 3 Carbon Credit TCO optimizer.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.z10_matrix.tools.logistics_extractor import logistics_extractor
from axomai.agents.z10_matrix.tools.route_optimizer import route_optimizer
from axomai.agents.z10_matrix.tools.warehouse_allocator import warehouse_allocator
from axomai.agents.z10_matrix.tools.live_weather_corridor import live_weather_radar
from axomai.agents.z10_matrix.tools.vrp_multi_stop_solver import vrp_solver
from axomai.agents.z10_matrix.tools.cargo_3d_load_optimizer import cargo_load_optimizer
from axomai.agents.z10_matrix.tools.eway_bill_and_multimodal import eway_multimodal
from axomai.agents.z10_matrix.tools.cold_chain_reefer_guard import cold_chain_guard
from axomai.agents.z10_matrix.tools.ev_fleet_carbon_optimizer import ev_carbon_optimizer


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


class Z10MatrixAgent:
    """Enterprise Chief Logistics Officer & Live Multimodal Supply Chain Commander."""

    def __init__(self):
        self.name = "Z10 Matrix"
        self.role = "9-Tool Live Fleet Logistics, VRP, E-Way Bill & Multimodal Supply Chain Commander"

    def logistics_stream(
        self,
        query: str,
        session_id: Optional[str] = "matrix_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # 0. Dynamically extract all parameters from user query
        params = logistics_extractor.parse_logistics_query(query)
        origin = params["origin"]
        dests = params["destinations"]
        cargo_tons = params["cargo_tons"]

        yield {
            "type": "status",
            "stage": "logistics_optimization",
            "message": f"🚛 Z10 Matrix: Querying live OSRM road routes & Open-Meteo weather from {origin} to {', '.join(dests)} ({cargo_tons}T cargo)..."
        }

        # 1. 3D Fleet & Axle-Load Optimization (sets optimal vehicle mileage!)
        load_plan = cargo_load_optimizer.optimize_fleet_load(cargo_weight_tons=cargo_tons)

        # 2. Live OSRM Highway Routing & Nominatim Geocoding
        routes = [
            route_optimizer.optimize_route(
                origin=origin,
                destination=d,
                mileage_km_per_l=load_plan["vehicle_mileage_kmpl"],
                cargo_tons=cargo_tons
            )
            for d in dests
        ]

        # 3. Live Open-Meteo Weather & Flood Radar for each destination
        weather_reports = [
            live_weather_radar.fetch_corridor_weather(d, coords=r.get("destination_coords"))
            for d, r in zip(dests, routes)
        ]

        # 4. Multi-Stop VRP (Nearest Neighbor + 2-Opt TSP) Sequence Optimization
        vrp_plan = vrp_solver.solve_multi_stop_sequence(
            origin=origin,
            destinations=dests,
            mileage_km_per_l=load_plan["vehicle_mileage_kmpl"]
        )

        # 5. Live Weather-Driven Warehouse Buffer & Safety Stock Allocation
        allocations = [
            warehouse_allocator.calculate_branch_inventory_allocation(
                district=d,
                monthly_sales_units=params["monthly_sales_units"],
                monsoon_mode=(w["recommended_safety_buffer_days"] >= 15),
                custom_buffer_days=w["recommended_safety_buffer_days"]
            )
            for d, w in zip(dests, weather_reports)
        ]

        # 6. CGST Rule 138 E-Way Bill & Multimodal Arbitrage (Road vs Rail vs Brahmaputra NW-2 vs Air)
        primary_route = routes[0]
        eway_data = eway_multimodal.evaluate_eway_bill(
            consignment_value_inr=params["invoice_value_inr"],
            distance_km=primary_route["distance_km"],
            is_odc=params["is_odc"]
        )
        multimodal_data = eway_multimodal.compare_multimodal_options(
            distance_km=primary_route["distance_km"],
            cargo_tons=cargo_tons,
            road_cost_inr=primary_route["total_logistics_cost_inr"],
            road_hrs=primary_route["transit_time_hrs"]
        )

        # 7. Cold-Chain Spoilage & Reefer Guard
        avg_ambient_c = weather_reports[0]["current_temp_c"] if weather_reports else 30.0
        cold_chain_data = cold_chain_guard.evaluate_cold_chain_risk(
            transit_hours=primary_route["transit_time_hrs"],
            ambient_temp_c=avg_ambient_c,
            target_temp_c=params["target_temp_c"] if params["target_temp_c"] is not None else 4.0,
            cargo_value_inr=params["invoice_value_inr"]
        )

        # 8. EV vs Diesel Fleet TCO & Scope 3 Carbon Credit Analysis
        ev_carbon_data = ev_carbon_optimizer.compare_ev_vs_diesel(
            total_distance_km=sum(r["distance_km"] for r in routes),
            cargo_tons=cargo_tons,
            diesel_cost_inr=sum(r["fuel_cost_inr"] for r in routes)
        )

        yield {
            "type": "status",
            "stage": "live_telemetry_complete",
            "message": f"🛰️ Live Telemetry Ready: {primary_route['routing_source']} ({primary_route['distance_km']} km) | Weather: {weather_reports[0]['disruption_risk']} | VRP Saved: {vrp_plan['distance_saved_km']} km"
        }

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "LIVE_MULTIMODAL_LOGISTICS_COMMAND",
            "tools_count": 9,
            "extracted_parameters": params,
            "central_hub": f"{origin} Multi-Modal Hub",
            "routes_calculated": len(routes),
            "destinations": dests,
            "routes_data": routes,
            "weather_data": weather_reports,
            "vrp_optimization": vrp_plan,
            "fleet_load_plan": load_plan,
            "allocations_data": allocations,
            "eway_bill": eway_data,
            "multimodal_arbitrage": multimodal_data,
            "cold_chain": cold_chain_data,
            "ev_carbon_tco": ev_carbon_data,
            "tools_used": [
                "logistics_extractor", "route_optimizer", "live_weather_radar",
                "vrp_solver", "cargo_load_optimizer", "warehouse_allocator",
                "eway_multimodal", "cold_chain_guard", "ev_carbon_optimizer"
            ]
        }
        yield meta_event

        prompt = (
            f"You are Z10 Matrix, Chief Logistics Officer & Live Supply Chain Strategist.\n"
            f"User Inquiry: '{query}'\n\n"
            f"LIVE TELEMETRY & ALGORITHMIC OUTPUTS:\n"
            f"- Optimal Fleet & MoRTH Axle Compliance: {load_plan}\n"
            f"- Live OSRM Highway Routes: {routes}\n"
            f"- Live Open-Meteo Weather & Flood Radar: {weather_reports}\n"
            f"- 2-Opt Multi-Stop VRP Sequence: {vrp_plan}\n"
            f"- Weather-Adjusted Warehouse Buffers: {allocations}\n"
            f"- GST E-Way Bill (CGST Rule 138): {eway_data}\n"
            f"- Multimodal Arbitrage (Road vs Rail CONCOR vs Brahmaputra NW-2 Waterway vs Air): {multimodal_data}\n"
            f"- Cold-Chain Spoilage & Reefer Guard: {cold_chain_data}\n"
            f"- EV vs Diesel TCO & Carbon Credits: {ev_carbon_data}\n\n"
            "Formulate an authoritative, crisp Freight Logistics & Multimodal Supply Chain Dossier in clean GitHub Markdown using ONLY the real observed figures above.\n"
            "Include clean Markdown tables for Highway Corridors, Multimodal Arbitrage, and Statutory Compliance."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z10 Matrix, Chief Logistics Officer.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = (
                f"### 🚛 Z10 Matrix: Live Multimodal Fleet & Supply Chain Dossier\n\n"
                f"**Origin:** `{origin}` | **Fleet:** `{load_plan['recommended_vehicle']}` (`{load_plan['payload_utilization_pct']}%` load) | **E-Way Bill:** `{eway_data['statutory_validity_days']} Days`\n\n"
                f"#### 🛣️ Live Road Corridors & Open-Meteo Weather\n\n"
                f"| Destination | Source | Distance | Transit | Cost (₹) | Live Weather & Rain |\n"
                f"| :--- | :--- | :--- | :--- | :--- | :--- |\n"
            )
            for r, w in zip(routes, weather_reports):
                full_answer += (
                    f"| {r['destination']} | `{r['routing_source']}` | {r['distance_km']} km | "
                    f"{r['transit_time_hrs']} hrs | ₹{r['total_logistics_cost_inr']:,.2f} | "
                    f"{w['current_temp_c']}°C, 3D Rain `{w['forecast_3day_rain_mm']}mm` ({w['disruption_risk']}) |\n"
                )
            full_answer += (
                f"\n#### 🚢 Multimodal Arbitrage & 2-Opt VRP\n\n"
                f"- **Optimal VRP Sequence:** `{' -> '.join(vrp_plan['optimal_sequence'])}` (Saved `{vrp_plan['distance_saved_km']} km` / `₹{vrp_plan['fuel_savings_inr']}`)\n"
                f"- **Lowest Cost Mode:** `{multimodal_data['lowest_cost_mode']}` | **CO₂ Saved via NW-2 Waterway:** `{multimodal_data['co2_savings_via_waterway_vs_road_kg']} kg`\n"
                f"- **EV vs Diesel Savings:** `₹{ev_carbon_data['direct_fuel_savings_inr']}` fuel savings + `₹{ev_carbon_data['carbon_credit_revenue_inr']}` Carbon Credits\n"
            )
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": normalize_markdown(full_answer)}


z10_matrix_agent = Z10MatrixAgent()
