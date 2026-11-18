"""
Z10 Matrix - Global Logistics, Multimodal Fleet Optimization & Supply Chain Agent.
Computes highway transit times, fuel economics, warehouse buffer allocation,
and route resilience across regional, national, and international logistics corridors.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.z10_matrix.tools.route_optimizer import route_optimizer
from axomai.agents.z10_matrix.tools.warehouse_allocator import warehouse_allocator

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
    """Enterprise Chief Logistics Officer & Multimodal Supply Chain Specialist."""

    def __init__(self):
        self.name = "Z10 Matrix"
        self.role = "Global Fleet Logistics, Highway Corridor & Warehouse Staging Specialist"

    def logistics_stream(
        self,
        query: str,
        session_id: Optional[str] = "matrix_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        q_lower = query.lower()

        yield {
            "type": "status",
            "stage": "logistics_optimization",
            "message": "🚛 Z10 Matrix: Computing multimodal corridor routes, fuel economics & inventory safety buffers..."
        }

        # Dynamically determine origin and destinations from query
        origin = "Central Distribution Hub"
        for city in ["mumbai", "delhi", "bengaluru", "kolkata", "chennai", "hyderabad", "ahmedabad", "guwahati"]:
            if city in q_lower:
                origin = city.title()
                break

        dests = []
        for city in ["delhi", "mumbai", "chennai", "kolkata", "bengaluru", "pune", "dibrugarh", "nagaon", "silchar"]:
            if city in q_lower and city.title() != origin:
                dests.append(city.title())

        if not dests:
            dests = ["Regional Distribution Terminal A", "Regional Distribution Terminal B"]

        routes = [route_optimizer.optimize_route(origin, d) for d in dests]
        allocations = [
            warehouse_allocator.calculate_branch_inventory_allocation(d, monthly_sales_units=1500)
            for d in dests
        ]

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "LOGISTICS_SUPPLY_CHAIN_OPTIMIZATION",
            "central_hub": f"{origin} Logistics Park",
            "routes_calculated": len(routes),
            "destinations": dests,
            "routes_data": routes,
            "allocations_data": allocations,
            "tools_used": ["route_optimizer", "warehouse_allocator"]
        }
        yield meta_event

        prompt = (
            f"You are Z10 Matrix, Chief Logistics Officer & Multimodal Fleet Strategist.\n"
            f"User Goal / Inquiry: '{query}'\n\n"
            f"Computed Highway & Freight Routes:\n{str(routes)}\n\n"
            f"Warehouse & Buffer Staging Allocations:\n{str(allocations)}\n\n"
            "Formulate an authoritative, operational Freight Logistics & Supply Chain Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present Corridor Comparison as a clean GitHub Markdown Table with blank lines before and after:\n"
            "| Destination | Highway Corridor | Distance (km) | Transit Time | Total Trip Cost (₹) | Terrain & Weather Risk |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
            "- Include exact warehouse staging rules (central hub to satellite terminals) and fleet speed/safety protocols.\n"
            "- Ensure every table row ends with a newline."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z10 Matrix, Chief Logistics Officer.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = (
                f"### 🚛 Z10 Matrix: Multimodal Freight Logistics & Corridor Optimization\n\n"
                f"**Central Distribution Gateway:** `{origin} Central Logistics Hub`\n\n"
                f"#### 🛣️ Highway Corridor & Freight Economics Matrix\n\n"
                f"| Destination | Highway Corridor | Distance (km) | Transit Time | Total Trip Cost (₹) | Terrain & Weather Risk |\n"
                f"| :--- | :--- | :--- | :--- | :--- | :--- |\n"
            )
            for r in routes:
                full_answer += (
                    f"| {r['destination']} | {r['corridor']} | {r['distance_km']} km | "
                    f"{r['transit_time_hrs']} hrs | ₹{r.get('total_logistics_cost_inr', r.get('total_trip_cost_inr', 0)):,.2f} | {r.get('monsoon_risk', r.get('monsoon_flood_risk', 'MODERATE'))} |\n"
                )
            full_answer += (
                f"\n#### 📦 Warehouse Staging & Supply Chain Resilience Model\n\n"
                f"- **Central Warehouse:** Scaled storage buffer holding safety stock to absorb seasonal weather and transport variations.\n"
                f"- **Fleet Safety Protocol:** Vehicle telematics, GPS speed governors, and driver fatigue rotation enforced across all long-haul corridors.\n"
                f"- **Replenishment Frequency:** High-velocity branch terminals receive bi-weekly dispatches; outlying regional hubs on weekly consolidated runs.\n"
            )
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": normalize_markdown(full_answer)}

z10_matrix_agent = Z10MatrixAgent()
