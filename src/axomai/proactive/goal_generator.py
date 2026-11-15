"""
AxomAI Proactive Engine - Autonomous Goal Generator.
Detects latent environmental triggers (commodity swings, logistics delays, weather warnings)
and proactively synthesizes strategic mission directives without human prompts.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import random

class GoalGenerator:
    """Proactive mission generator formulating goals from autonomous environmental signals."""

    def __init__(self):
        self.proactive_goals_history: List[Dict[str, Any]] = []

    def evaluate_signals_and_generate_goals(
        self,
        signals: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Analyzes active real-world signals and synthesizes autonomous mission goals.
        """
        now = datetime.utcnow().isoformat()
        
        # Default real-world domain signals if none provided
        active_signals = signals or [
            {
                "domain": "commodity_markets",
                "indicator": "Tea Export Mandi Volatility",
                "value": -4.2,
                "unit": "%",
                "severity": "HIGH",
                "message": "Spot export auction prices in Guwahati declined 4.2% while Hamburg freight rates rose."
            },
            {
                "domain": "infrastructure_geotechnical",
                "indicator": "Brahmaputra Flood Embankment Pore Pressure",
                "value": 1.18,
                "unit": "FoS",
                "severity": "ELEVATED",
                "message": "Water table elevation in Dibrugarh pier sector reduced factor of safety below 1.25."
            },
            {
                "domain": "energy_arbitrage",
                "indicator": "Discom HT Tariff Differential",
                "value": 3.40,
                "unit": "INR/kWh",
                "severity": "OPPORTUNITY",
                "message": "Grid tariff differential widened to ₹3.40/kWh favoring instant captive solar PPA expansion."
            }
        ]

        generated_goals = []
        for sig in active_signals:
            dom = sig.get("domain")
            severity = sig.get("severity")
            indicator = sig.get("indicator")

            if dom == "commodity_markets" and severity in ["HIGH", "CRITICAL"]:
                goal = {
                    "goal_id": f"goal_{len(self.proactive_goals_history) + 1:04d}",
                    "title": "Autonomous Cross-Border FX Collar & Export Mandi Re-hedging",
                    "priority": "P0_CRITICAL",
                    "trigger_indicator": indicator,
                    "target_agent": "revenue_syndicate",
                    "autonomous_action": "Execute Garman-Kohlhagen zero-cost option collar and rebalance tea lot allocations to Hamburg.",
                    "created_at": now,
                    "status": "PROACTIVELY_DISPATCHED"
                }
                generated_goals.append(goal)
                self.proactive_goals_history.append(goal)

            elif dom == "infrastructure_geotechnical" and severity in ["ELEVATED", "HIGH"]:
                goal = {
                    "goal_id": f"goal_{len(self.proactive_goals_history) + 1:04d}",
                    "title": "Autonomous Seismic Slope Stabilization & FIDIC Extension of Time Protocol",
                    "priority": "P1_HIGH",
                    "trigger_indicator": indicator,
                    "target_agent": "infra_shield",
                    "autonomous_action": "Simulate Bishop slope reinforcement with geotextile tubes and draft FIDIC Clause 20.1 time-extension claim.",
                    "created_at": now,
                    "status": "PROACTIVELY_DISPATCHED"
                }
                generated_goals.append(goal)
                self.proactive_goals_history.append(goal)

            elif dom == "energy_arbitrage" and severity == "OPPORTUNITY":
                goal = {
                    "goal_id": f"goal_{len(self.proactive_goals_history) + 1:04d}",
                    "title": "Industrial Clean Energy Transition & Carbon Credit Arbitrage",
                    "priority": "P2_OPTIMIZATION",
                    "trigger_indicator": indicator,
                    "target_agent": "y2",
                    "autonomous_action": "Optimize 250kWp rooftop solar sizing and compute Verra VCS carbon monetization revenue.",
                    "created_at": now,
                    "status": "PROACTIVELY_DISPATCHED"
                }
                generated_goals.append(goal)
                self.proactive_goals_history.append(goal)

        return generated_goals

    def get_proactive_history(self) -> List[Dict[str, Any]]:
        return list(self.proactive_goals_history[-10:])

goal_generator = GoalGenerator()
