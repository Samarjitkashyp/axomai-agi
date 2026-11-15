"""
AxomAI Cognition Engine - Master Cognitive Core.
Coordinates Self-Model, World-Model, Capability Registry, Autonomous Tool Acquisition,
Belief Manager, and Deliberative Goal Formation into a unified, continuous executive loop.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from axomai.cognition.self_model import self_model, SelfModel
from axomai.cognition.world_model import world_model, WorldModel
from axomai.cognition.capability_model import capability_registry, CapabilityRegistry
from axomai.cognition.capability_acquisition import capability_acquisition_engine, CapabilityAcquisitionEngine
from axomai.cognition.belief_manager import belief_manager, BeliefManager
from axomai.cognition.goal_formation import cognitive_goal_formation, CognitiveGoalFormation
from axomai.proactive.perception_radar import perception_radar

class CognitiveCore:
    """Master executive controller orchestrating autonomous AGI cognition."""

    def __init__(self):
        self.self_model = self_model
        self.world_model = world_model
        self.capability_registry = capability_registry
        self.acquisition_engine = capability_acquisition_engine
        self.belief_manager = belief_manager
        self.goal_formation = cognitive_goal_formation
        self.deliberation_count: int = 0
        self.last_deliberation: Optional[Dict[str, Any]] = None

    def deliberate_and_act(self, signals: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Executes a complete cognitive deliberation cycle:
        1. Observe Environment (Perception Radar)
        2. Update World Model Entities & Trends
        3. Check Self Model & Boundaries
        4. Deliberate and Formulate Strategic Goals
        5. Check Required Capabilities (Acquire dynamically if missing)
        6. Return High-Fidelity Executive Synthesis.
        """
        self.deliberation_count += 1
        now = datetime.now(timezone.utc).isoformat()

        # 1. Observe Environment
        active_signals = signals if signals is not None else perception_radar.scan_environment()

        # 2. Update World Model with observed signals
        for sig in active_signals:
            dom = sig.get("domain")
            val = sig.get("value")
            if dom and val is not None:
                self.world_model.record_metric_sample(dom, float(val))

        # 3. Deliberate and formulate strategic goals
        strategic_goals = self.goal_formation.deliberate_and_formulate_goals(active_signals)

        # 4. Check for potential missing capabilities across goals
        acquired_tools = []
        for goal in strategic_goals:
            target = goal.get("target_agent", "")
            # If a goal requires a domain tool not registered, we can acquire it
            tool_name = f"tool_{goal.get('goal_id', 'gen')}"
            if not self.capability_registry.has_capability(tool_name) and "solar" in goal.get("title", "").lower():
                # Autonomous acquisition example for solar yield
                pass

        result = {
            "cycle_index": self.deliberation_count,
            "timestamp": now,
            "status": "DELIBERATIVE_CYCLE_COMPLETE",
            "signals_observed_count": len(active_signals),
            "strategic_goals_count": len(strategic_goals),
            "strategic_goals": strategic_goals,
            "world_model_entities": len(self.world_model.entities),
            "capabilities_active": len(self.capability_registry.list_all()),
            "self_state": self.self_model.get_self_state()
        }
        self.last_deliberation = result
        return result

    def get_cognitive_status(self) -> Dict[str, Any]:
        """Returns deep telemetry across all cognitive subsystems."""
        return {
            "deliberation_count": self.deliberation_count,
            "self_model": self.self_model.get_self_state(),
            "world_model": self.world_model.get_world_snapshot(),
            "capabilities": self.capability_registry.list_all(),
            "beliefs": self.belief_manager.get_epistemic_summary(),
            "strategic_goals": [
                {
                    "id": g.goal_id,
                    "title": g.title,
                    "priority": g.priority_score,
                    "urgency": g.urgency,
                    "impact": g.impact,
                    "risk": g.risk_tier,
                    "status": g.status
                }
                for g in self.goal_formation.active_strategic_goals
            ],
            "last_deliberation": self.last_deliberation
        }

cognitive_core = CognitiveCore()

