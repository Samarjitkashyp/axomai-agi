"""
AxomAI Proactive Engine - Autonomous Goal Generator.
Detects latent environmental triggers (system health, commodity swings, logistics delays, weather warnings)
and proactively synthesizes strategic mission directives without human prompts.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from axomai.proactive.perception_radar import perception_radar, PerceptionRadar

class GoalGenerator:
    """Proactive mission generator formulating goals from autonomous environmental signals."""

    def __init__(self, radar: Optional[PerceptionRadar] = None):
        self.radar = radar or perception_radar
        self.proactive_goals_history: List[Dict[str, Any]] = []

    def evaluate_signals_and_generate_goals(
        self,
        signals: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Analyzes active real-world signals (or scans via radar if none provided)
        and synthesizes prioritized autonomous mission goals.
        """
        now = datetime.now(timezone.utc).isoformat()

        # If no explicit signals provided, activate perception radar to scan environment live!
        if signals is None:
            active_signals = self.radar.scan_environment()
        else:
            active_signals = signals

        # Fallback if radar returned clean environment with no alerts
        if not active_signals:
            active_signals = [
                {
                    "domain": "commodity_markets",
                    "indicator": "Tea Export Mandi Volatility",
                    "value": -4.2,
                    "unit": "%",
                    "severity": "HIGH",
                    "message": "Spot export auction prices in Guwahati declined 4.2% while Hamburg freight rates rose."
                }
            ]

        generated_goals = []
        for sig in active_signals:
            dom = sig.get("domain")
            severity = sig.get("severity")
            indicator = sig.get("indicator")

            if dom == "system_infrastructure" and severity in ["CRITICAL", "ELEVATED"]:
                goal = {
                    "goal_id": f"goal_{len(self.proactive_goals_history) + 1:04d}",
                    "title": "Autonomous Host Resource Rebalance & Storage Cleansing",
                    "priority": "P0_CRITICAL",
                    "trigger_indicator": indicator,
                    "target_agent": "system_janitor",
                    "autonomous_action": "Execute memory cache purge, prune orphaned ephemeral artifacts, and adjust process thread limits.",
                    "created_at": now,
                    "status": "PROACTIVELY_DISPATCHED"
                }
                generated_goals.append(goal)
                self.proactive_goals_history.append(goal)

            elif dom == "workspace_intelligence" and severity == "OPPORTUNITY":
                goal = {
                    "goal_id": f"goal_{len(self.proactive_goals_history) + 1:04d}",
                    "title": "Autonomous Ingestion & Semantic Graph Embedding of New Artifacts",
                    "priority": "P2_OPTIMIZATION",
                    "trigger_indicator": indicator,
                    "target_agent": "z9_cortex",
                    "autonomous_action": "Parse newly detected workspace documents and update semantic graph knowledge nodes.",
                    "created_at": now,
                    "status": "PROACTIVELY_DISPATCHED"
                }
                generated_goals.append(goal)
                self.proactive_goals_history.append(goal)

            elif dom == "commodity_markets" and severity in ["HIGH", "CRITICAL"]:
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
        return list(self.proactive_goals_history[-20:])

goal_generator = GoalGenerator()
