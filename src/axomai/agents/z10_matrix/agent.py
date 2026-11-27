"""
Z10 Matrix - 17-Tool Live Multimodal Logistics, Sovereign ULIP/ONDC & Supply Chain Titan.
Combines live OSRM highway routing, OpenStreetMap Nominatim geocoding, Open-Meteo live weather/flood
telemetry, 2-Opt multi-stop VRP solver, 3D MoRTH axle-load optimizer, CGST Rule 138 E-Way Bill,
Brahmaputra NW-2 / Rail CONCOR multimodal arbitrage, Cold-Chain Q10 spoilage guard, EV Carbon TCO,
Govt ULIP/ONDC Beckn protocol bridge, Zero-Deadhead Backhaul AI, Dynamic Spot-Bidding Reverse Auction,
Act East Cross-Border ICP Customs Engine, 5,000-Run Digital Twin War-Gamer, Port Demurrage Shield,
Flood-Zone BVLOS Cargo Drone Planner, and Highway Blackspot / Driver Fatigue Guard.
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

# 8 Future-Proof Sovereign & Deep-Tech Engines
from axomai.agents.z10_matrix.tools.ulip_ondc_bridge import ulip_ondc_bridge
from axomai.agents.z10_matrix.tools.backhaul_matcher import backhaul_matcher
from axomai.agents.z10_matrix.tools.spot_bidding_auction import spot_bidding_engine
from axomai.agents.z10_matrix.tools.act_east_customs_engine import act_east_customs
from axomai.agents.z10_matrix.tools.digital_twin_wargamer import digital_twin_wargamer
from axomai.agents.z10_matrix.tools.port_demurrage_shield import port_demurrage_shield
from axomai.agents.z10_matrix.tools.bvlos_drone_planner import bvlos_drone_planner
from axomai.agents.z10_matrix.tools.highway_safety_fatigue_guard import highway_safety_guard


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
    """Enterprise Chief Logistics Officer & 17-Tool Live Sovereign Supply Chain Commander."""

    def __init__(self):
        self.name = "Z10 Matrix"
        self.role = "17-Tool Sovereign Freight, ULIP/ONDC, Digital Twin & Multimodal Supply Chain Titan"

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
            "message": f"🚛 Z10 Matrix: Launching 17-tool live OSRM routing, Open-Meteo flood radar, ULIP/ONDC & Digital Twin from {origin} to {', '.join(dests)} ({cargo_tons}T)..."
        }

        # 1. 3D Fleet & Axle-Load Optimization
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

        # 3. Live Open-Meteo Weather & Flood Radar
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

        primary_route = routes[0]
        primary_weather = weather_reports[0]
        primary_alloc = allocations[0]

        # 6. CGST Rule 138 E-Way Bill & Multimodal Arbitrage
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
        cold_chain_data = cold_chain_guard.evaluate_cold_chain_risk(
            transit_hours=primary_route["transit_time_hrs"],
            ambient_temp_c=primary_weather["current_temp_c"],
            target_temp_c=params["target_temp_c"] if params["target_temp_c"] is not None else 4.0,
            cargo_value_inr=params["invoice_value_inr"]
        )

        # 8. EV vs Diesel Fleet TCO & Scope 3 Carbon Credit Analysis
        ev_carbon_data = ev_carbon_optimizer.compare_ev_vs_diesel(
            total_distance_km=sum(r["distance_km"] for r in routes),
            cargo_tons=cargo_tons,
            diesel_cost_inr=sum(r["fuel_cost_inr"] for r in routes)
        )

        # 9. Govt ULIP & ONDC Beckn v1.2.0 Dispatch Bridge
        ulip_ondc_data = ulip_ondc_bridge.generate_ulip_ondc_dispatch(
            origin=origin,
            destination=dests[0],
            cargo_tons=cargo_tons,
            vehicle_model=load_plan["recommended_vehicle"],
            estimated_cost_inr=primary_route["total_logistics_cost_inr"]
        )

        # 10. Zero-Deadhead Backhaul (Return-Load) Matching AI
        backhaul_data = backhaul_matcher.match_return_load(
            origin=origin,
            destination=dests[0],
            distance_km=primary_route["distance_km"],
            cargo_tons=cargo_tons,
            outbound_cost_inr=primary_route["total_logistics_cost_inr"]
        )

        # 11. Game-Theoretic Freight Spot-Bidding Reverse Auction
        auction_data = spot_bidding_engine.run_reverse_auction(
            origin=origin,
            destination=dests[0],
            base_operating_cost_inr=primary_route["total_logistics_cost_inr"],
            backhaul_prob_pct=backhaul_data["backhaul_match_probability_pct"],
            weather_risk=primary_weather["disruption_risk"]
        )

        # 12. Act East Policy Cross-Border ICP Customs Engine
        act_east_data = act_east_customs.evaluate_cross_border_corridor(
            origin=origin,
            destination=dests[0],
            consignment_value_inr=params["invoice_value_inr"]
        )

        # 13. 5,000-Run Digital Twin Black-Swan War-Gamer
        digital_twin_data = digital_twin_wargamer.run_disruption_wargame(
            base_transit_hrs=primary_route["transit_time_hrs"],
            safety_buffer_days=primary_alloc["buffer_days"],
            monsoon_risk=primary_route["monsoon_flood_risk"]
        )

        # 14. Port Congestion & Container Demurrage AI Shield
        port_demurrage_data = port_demurrage_shield.evaluate_port_demurrage(
            origin=origin,
            destination=dests[0]
        )

        # 15. Flood-Zone BVLOS Cargo Drone Delivery Planner
        drone_data = bvlos_drone_planner.plan_emergency_drone_drop(
            destination=dests[0],
            wind_speed_kmh=primary_weather["wind_speed_kmh"]
        )

        # 16. Highway Blackspot, Driver Fatigue & Wildlife Corridor Guard
        safety_data = highway_safety_guard.evaluate_route_safety(
            origin=origin,
            destination=dests[0],
            transit_hours=primary_route["transit_time_hrs"],
            terrain=primary_route["terrain"]
        )

        yield {
            "type": "status",
            "stage": "live_telemetry_complete",
            "message": f"🛰️ 17-Tool Matrix Complete: {primary_route['routing_source']} ({primary_route['distance_km']} km) | VRP Saved: {vrp_plan['distance_saved_km']} km | Auction L1: ₹{auction_data['winning_l1_rate_inr']:,.0f} | TTS: {digital_twin_data['time_to_survive_tts_days']}d"
        }

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "SOVEREIGN_17_TOOL_LOGISTICS_COMMAND",
            "tools_count": 17,
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
            "ulip_ondc": ulip_ondc_data,
            "backhaul_match": backhaul_data,
            "reverse_auction": auction_data,
            "act_east_customs": act_east_data,
            "digital_twin": digital_twin_data,
            "port_demurrage": port_demurrage_data,
            "bvlos_drone": drone_data,
            "driver_safety_geofence": safety_data,
            "tools_used": [
                "logistics_extractor", "route_optimizer", "live_weather_radar",
                "vrp_solver", "cargo_load_optimizer", "warehouse_allocator",
                "eway_multimodal", "cold_chain_guard", "ev_carbon_optimizer",
                "ulip_ondc_bridge", "backhaul_matcher", "spot_bidding_engine",
                "act_east_customs", "digital_twin_wargamer", "port_demurrage_shield",
                "bvlos_drone_planner", "highway_safety_guard"
            ]
        }
        yield meta_event

        prompt = (
            f"You are Z10 Matrix, 17-Tool Sovereign Chief Logistics Officer.\n"
            f"User Inquiry: '{query}'\n\n"
            f"LIVE TELEMETRY & SOVEREIGN OUTPUTS:\n"
            f"- Optimal Fleet & MoRTH Axle Compliance: {load_plan}\n"
            f"- Live OSRM Highway Routes: {routes}\n"
            f"- Live Open-Meteo Weather & Flood Radar: {weather_reports}\n"
            f"- 2-Opt Multi-Stop VRP Sequence: {vrp_plan}\n"
            f"- Govt ULIP & ONDC Beckn v1.2.0 Bridge: {ulip_ondc_data['ulip_api_readiness']} | Txn {ulip_ondc_data['ondc_beckn_protocol']['transaction_id']}\n"
            f"- Zero-Deadhead Backhaul Match: {backhaul_data}\n"
            f"- Reverse Auction Winning Carrier: {auction_data['winning_l1_carrier']} @ ₹{auction_data['winning_l1_rate_inr']} (Saved ₹{auction_data['savings_vs_broker_inr']} / {auction_data['savings_pct']}%)\n"
            f"- Act East Cross-Border ICP Hub: {act_east_data}\n"
            f"- 5,000-Run Digital Twin War-Game: {digital_twin_data}\n"
            f"- Port Demurrage Shield: {port_demurrage_data}\n"
            f"- Flood-Zone BVLOS Cargo Drone: {drone_data}\n"
            f"- Driver Fatigue & Wildlife Geofence: {safety_data}\n"
            f"- GST E-Way Bill & NW-2 Multimodal Arbitrage: {eway_data} | {multimodal_data}\n"
            f"- Cold-Chain & EV Carbon Credits: {cold_chain_data} | {ev_carbon_data}\n\n"
            "Formulate an authoritative, crisp Sovereign Freight & Supply Chain Command Dossier in clean GitHub Markdown using ONLY the real observed figures above."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z10 Matrix, Sovereign Chief Logistics Officer.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = (
                f"### 🚛 Z10 Matrix: 17-Tool Sovereign Freight & Supply Chain Matrix\n\n"
                f"**Origin:** `{origin}` | **Fleet:** `{load_plan['recommended_vehicle']}` | **ULIP/ONDC:** `Beckn v1.2.0`\n\n"
                f"#### 🛣️ Live OSRM Corridors & Open-Meteo Weather\n\n"
                f"| Destination | Distance | Transit | Auction L1 (₹) | Live Weather & Rain |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
            )
            for r, w in zip(routes, weather_reports):
                full_answer += (
                    f"| {r['destination']} | {r['distance_km']} km | {r['transit_time_hrs']} hrs | "
                    f"₹{r['total_logistics_cost_inr']:,.2f} | {w['current_temp_c']}°C, 3D Rain `{w['forecast_3day_rain_mm']}mm` |\n"
                )
            full_answer += (
                f"\n#### 🏆 Sovereign Optimization Highlights\n\n"
                f"- **2-Opt VRP Sequence:** `{' -> '.join(vrp_plan['optimal_sequence'])}` (Saved `{vrp_plan['distance_saved_km']} km`)\n"
                f"- **Zero-Deadhead Backhaul:** `{backhaul_data['matched_commodity_cluster']}` (`-{backhaul_data['deadhead_cost_savings_pct']}%` cost)\n"
                f"- **Reverse Auction Winner:** `{auction_data['winning_l1_carrier']}` @ `₹{auction_data['winning_l1_rate_inr']}`\n"
                f"- **Digital Twin Resilience:** TTS `{digital_twin_data['time_to_survive_tts_days']}d` vs TTR `{digital_twin_data['time_to_recover_ttr_days']}d` (`{digital_twin_data['resilience_verdict']}`)\n"
            )
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": normalize_markdown(full_answer)}


z10_matrix_agent = Z10MatrixAgent()
