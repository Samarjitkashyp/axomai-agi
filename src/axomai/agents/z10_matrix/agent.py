"""
Z10 Matrix - Autonomous Logistics, Supply Chain & Fleet Route Optimization Agent.
Orchestrates regional multi-modal route planning, monsoon detour management,
warehouse inventory staging, and freight unit economics.
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
    """Enterprise Chief Logistics Officer & Supply Chain Route Optimization Agent."""

    def __init__(self):
        self.name = "Z10 Matrix"
        self.role = "Logistics, Supply Chain & Fleet Route Optimization Agent"

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
            "message": "🚛 Z10 Matrix: Computing corridor route matrices, toll/fuel rates & flood safety buffers..."
        }

        # Analyze target destinations
        dests = []
        if "nagaon" in q_lower:
            dests.append("Nagaon")
        if "dibrugarh" in q_lower:
            dests.append("Dibrugarh")
        if "silchar" in q_lower:
            dests.append("Silchar")
        if not dests:
            dests = ["Nagaon", "Dibrugarh"]

        routes = [route_optimizer.optimize_route("Guwahati", d) for d in dests]
        allocations = [
            warehouse_allocator.calculate_branch_inventory_allocation(d, monthly_sales_units=1200)
            for d in dests
        ]

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "LOGISTICS_SUPPLY_CHAIN_OPTIMIZATION",
            "central_hub": "Changsari Logistics Park (Guwahati)",
            "routes_calculated": len(routes),
            "destinations": dests,
            "routes_data": routes,
            "allocations_data": allocations,
            "tools_used": ["route_optimizer", "warehouse_allocator"]
        }
        yield meta_event

        prompt = (
            f"You are Z10 Matrix, Chief Logistics Officer & Fleet Strategist for Northeast India.\n"
            f"User Goal / Inquiry: '{query}'\n\n"
            f"Computed Highway Routes:\n{str(routes)}\n\n"
            f"Warehouse & Buffer Staging Allocations:\n{str(allocations)}\n\n"
            "Formulate an authoritative, operational Freight Logistics & Supply Chain Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present Corridor Comparison as a clean GitHub Markdown Table with blank lines before and after:\n"
            "| Destination | Highway Corridor | Distance (km) | Transit Time | Total Trip Cost (₹) | Monsoon Flood Risk |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
            "- Include exact warehouse staging rules (Changsari central hub to satellite stores) and Kaziranga speed camera protocols.\n"
            "- Ensure every table row ends with a newline."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z10 Matrix, Chief Logistics Officer.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = (
                f"### 🚛 Z10 Matrix: Northeast Logistics & Fleet Optimization\n\n"
                f"**Central Distribution Hub:** `Changsari Integrated Logistics Park (Kamrup Metro)`\n\n"
                f"#### 🛣️ Highway Corridor & Freight Economics Matrix\n\n"
                f"| Destination | Highway Corridor | Distance (km) | Transit Time | Total Trip Cost (₹) | Monsoon Flood Risk |\n"
                f"| :--- | :--- | :--- | :--- | :--- | :--- |\n"
            )
            for r in routes:
                full_answer += (
                    f"| {r['destination']} | {r['corridor']} | {r['distance_km']} km | "
                    f"{r['transit_time_hrs']} hrs | ₹{r['total_logistics_cost_inr']:,.2f} | {r['monsoon_risk']} |\n"
                )
            full_answer += (
                f"\n#### 📦 Warehouse Staging & Flood Resilience Model\n\n"
                f"- **Central Warehouse:** 20,000 sq.ft at Changsari holding 21-day buffer inventory during June–August monsoons.\n"
                f"- **Kaziranga Eco-Sensitive Corridor:** Speed strictly regulated at 40 km/h with sensor cameras on NH-715 to prevent wildlife hazards.\n"
                f"- **Replenishment Frequency:** Twice a week for Nagaon (via 4-lane NH-27); Weekly consolidated 16-Ton run for Dibrugarh.\n"
            )
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": normalize_markdown(full_answer)}

z10_matrix_agent = Z10MatrixAgent()

