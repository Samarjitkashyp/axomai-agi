"""
AxomAI Proactive Engine - Autonomous Goal Generator.
Detects latent environmental triggers (system health, commodity swings, logistics delays, weather warnings)
and proactively synthesizes strategic mission directives through deliberative cognitive goal formation.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from axomai.proactive.perception_radar import perception_radar, PerceptionRadar
from axomai.cognition.goal_formation import cognitive_goal_formation

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
        and synthesizes prioritized autonomous mission goals via deliberative cognitive goal formation.
        """
        now = datetime.now(timezone.utc).isoformat()

        # If no explicit signals provided, activate perception radar to scan environment live!
        active_signals = signals if signals is not None else self.radar.scan_environment()

        # Fallback if radar returned clean environment with no alerts
        if not active_signals:
            active_signals = [
                {
                    "domain": "global_supply_chain",
                    "indicator": "Multimodal Freight Volatility",
                    "value": -3.5,
                    "unit": "%",
                    "severity": "ELEVATED",
                    "message": "Global container dwell times and freight rates rose across primary maritime corridors."
                }
            ]

        # Formulate goals through deliberative cognitive goal formation
        deliberated_goals = cognitive_goal_formation.deliberate_and_formulate_goals(active_signals)

        generated_goals = []
        for g in deliberated_goals:
            priority_label = "P0_CRITICAL" if g.get("priority_score", 0.0) >= 0.80 else (
                "P1_HIGH" if g.get("priority_score", 0.0) >= 0.65 else "P2_OPTIMIZATION"
            )
            goal_entry = {
                "goal_id": g.get("goal_id", f"goal_{len(self.proactive_goals_history) + 1:04d}"),
                "title": g.get("title", "Autonomous Strategic Directive"),
                "priority": priority_label,
                "priority_score": g.get("priority_score", 0.70),
                "trigger_indicator": g.get("rationalization", "")[:60],
                "target_agent": g.get("target_agent", "action_runner"),
                "autonomous_action": g.get("action_directive", ""),
                "rationalization": g.get("rationalization", ""),
                "risk_tier": g.get("risk_tier", "LOW_RISK"),
                "created_at": g.get("created_at", now),
                "status": "PROACTIVELY_DISPATCHED"
            }
            generated_goals.append(goal_entry)
            self.proactive_goals_history.append(goal_entry)

        return generated_goals

    def get_proactive_history(self) -> List[Dict[str, Any]]:
        return list(self.proactive_goals_history[-20:])

goal_generator = GoalGenerator()
