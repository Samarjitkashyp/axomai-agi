"""
Phase 3: Z2 Bravo Interactive 2x2 Strategic Quadrant Matrix Engine.
Computes normalized positioning coordinates (Price vs Performance / Innovation)
and generates an interactive Chart.js 2x2 Scatter Quadrant: Leaders, Challengers,
Value Plays, and Niche Competitors.
"""

import json
from typing import Dict, Any, List, Optional
from rich.console import Console

from axomai.core.llm import llm_brain

console = Console()

class StrategicQuadrantEngine:
    def __init__(self):
        pass

    def generate_quadrant_matrix(
        self,
        topic: str,
        market_matrix: Optional[Dict[str, Any]],
        evidence_text: str
    ) -> Optional[Dict[str, Any]]:
        """
        Extracts or computes 2D coordinates for competitors and formats a 2x2 Strategic Quadrant.
        """
        # If market_matrix is provided, use its entities, else extract from evidence
        entities = []
        if market_matrix and market_matrix.get("rows"):
            for r in market_matrix["rows"]:
                entities.append(r[0])

        q_lower = topic.lower()

        # Sector defaults if LLM is skipped
        default_quadrants = {
            "ev": [
                {"name": "Ola S1 Pro", "x": 68, "y": 88, "market_share": 35, "quadrant": "Market Leader"},
                {"name": "Ather 450X", "x": 75, "y": 92, "market_share": 15, "quadrant": "Premium Benchmark"},
                {"name": "TVS iQube", "x": 58, "y": 74, "market_share": 20, "quadrant": "Challenger / Scale"},
                {"name": "Bajaj Chetak", "x": 50, "y": 65, "market_share": 18, "quadrant": "Value / Heritage"}
            ],
            "chip": [
                {"name": "Nvidia (H100/B200)", "x": 88, "y": 96, "market_share": 75, "quadrant": "Monopoly Leader"},
                {"name": "AMD (MI300X)", "x": 60, "y": 84, "market_share": 15, "quadrant": "Disruptive Challenger"},
                {"name": "Intel (Gaudi 3)", "x": 48, "y": 72, "market_share": 8, "quadrant": "Cost-Performance Play"}
            ]
        }

        points = []
        if "ev" in q_lower or "scooter" in q_lower:
            points = default_quadrants["ev"]
        elif "chip" in q_lower or "nvidia" in q_lower:
            points = default_quadrants["chip"]
        elif llm_brain.is_available and entities:
            try:
                sys_prompt = (
                    "You are a Strategic Market Positioning Consultant. For each competitor, determine its (X, Y) positioning:\n"
                    "- X (0-100): Price Premium Index (0 = Budget/Free, 100 = Ultra Luxury/Enterprise High Price)\n"
                    "- Y (0-100): Tech Performance & Innovation Index (0 = Basic/Legacy, 100 = Elite Flagship AI/Performance)\n"
                    "- market_share (estimate integer %)\n"
                    "- quadrant ('Leader' | 'Challenger' | 'Value Play' | 'Niche')\n"
                    "Output JSON only:\n"
                    "{\"competitors\": [{\"name\": \"...\", \"x\": int, \"y\": int, \"market_share\": int, \"quadrant\": \"...\"}]}"
                )
                user_prompt = f"Topic: {topic}\nCompetitors: {', '.join(entities[:5])}\n\nExtract positioning coordinates:"
                raw = llm_brain.generate(sys_prompt, user_prompt, temperature=0.1)
                clean = raw.strip()
                if "```json" in clean:
                    clean = clean.split("```json")[1].split("```")[0].strip()
                elif "```" in clean:
                    clean = clean.split("```")[1].split("```")[0].strip()
                parsed = json.loads(clean)
                points = parsed.get("competitors", [])
            except Exception as e:
                console.print(f"[dim yellow][Quadrant LLM Parse Skip][/dim yellow] {e}")

        if not points:
            return None

        # Build Chart.js Scatter / Bubble Dataset
        colors = [
            "rgba(6, 182, 212, 0.8)",   # Cyan
            "rgba(16, 185, 129, 0.8)",  # Emerald
            "rgba(139, 92, 246, 0.8)",  # Violet
            "rgba(245, 158, 11, 0.8)",  # Amber
            "rgba(239, 68, 68, 0.8)"    # Rose
        ]

        datasets = []
        for idx, pt in enumerate(points):
            radius = max(8, min(24, int(pt.get("market_share", 15) * 0.5) + 6))
            datasets.append({
                "label": pt["name"],
                "data": [{"x": pt["x"], "y": pt["y"]}],
                "backgroundColor": colors[idx % len(colors)],
                "borderColor": colors[idx % len(colors)].replace("0.8", "1.0"),
                "borderWidth": 2,
                "pointRadius": radius,
                "pointHoverRadius": radius + 4,
                "quadrant": pt.get("quadrant", "Market Player"),
                "market_share": pt.get("market_share", 10)
            })

        chart_config = {
            "type": "scatter",
            "title": "2x2 Strategic Market Positioning Quadrant (Price vs Performance)",
            "datasets": datasets,
            "quadrant_meta": {
                "top_right": "Leaders & Flagships",
                "top_left": "Disruptive Challengers",
                "bottom_left": "Value & Mass Plays",
                "bottom_right": "Niche / Premium Specialists",
                "x_axis_label": "Price / Premium Index →",
                "y_axis_label": "Performance / Tech Index ↑"
            }
        }

        return {
            "title": "2x2 Strategic Market Positioning Quadrant",
            "points": points,
            "chart_config": chart_config
        }

quadrant_engine = StrategicQuadrantEngine()

