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

    def deliberate_and_act(self, signals: Optional[List[Dict[str, Any]]] = None, auto_execute_top_mission: bool = True) -> Dict[str, Any]:
        """
        Executes a complete cognitive deliberation cycle:
        1. Observe Environment (Perception Radar)
        2. Update World Model Entities & Trends
        3. Check Self Model & Boundaries
        4. Deliberate and Formulate Strategic Goals
        5. Check Required Capabilities (Acquire dynamically if missing via Tool Forge)
        6. Dispatch Top Strategic Goal to Autonomous Mission Manager
        7. Return High-Fidelity Executive Synthesis.
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

        # 4. Closed-Loop Autonomous Capability Acquisition Across Strategic Goals
        import re
        acquired_tools = []
        for goal in strategic_goals:
            goal_id = goal.get("goal_id", "gen")
            goal_title = goal.get("title", "")
            clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', goal_title.lower()[:24]).strip('_')
            tool_name = f"tool_{clean_name}" if clean_name else f"tool_{goal_id}"

            # If the required domain capability is not in the active registry, autonomously synthesize it
            if not self.capability_registry.has_capability(tool_name):
                acq_res = self.acquisition_engine.synthesize_and_acquire_for_goal({
                    "goal_id": goal_id,
                    "title": goal_title,
                    "tool_name": tool_name,
                    "target_agent": goal.get("target_agent", "z4"),
                    "action_directive": goal.get("action_directive", goal_title)
                })
                if acq_res.get("status") == "CAPABILITY_ACQUIRED_AND_OPERATIONAL":
                    acquired_tools.append(acq_res)

        # 5. Autonomous Mission Dispatch & Execution Loop
        executed_mission = None
        if strategic_goals and auto_execute_top_mission:
            top_goal = strategic_goals[0]
            try:
                from axomai.agents.mission_control.planner import mission_planner
                from axomai.memory.episodic_memory import episodic_memory
                mission_title = top_goal.get("title", "Autonomous Strategic Objective")
                directive = top_goal.get("action_directive", mission_title)
                plan = mission_planner.plan_mission(directive)
                executed_mission = {
                    "mission_id": plan.mission_id,
                    "title": plan.title,
                    "strategic_objective": plan.strategic_objective,
                    "total_steps": plan.total_steps,
                    "milestones": [m.model_dump() for m in plan.milestones],
                    "status": "DISPATCHED_AND_PLANNED"
                }
                # Update World Model with newly dispatched mission
                self.world_model.update_entity("active_mission", {
                    "mission_id": plan.mission_id,
                    "title": plan.title,
                    "status": "IN_PROGRESS",
                    "total_steps": plan.total_steps
                })
                # Record mission activation in episodic memory
                episodic_memory.record_episode(
                    query=f"Autonomous Strategic Mission: {plan.title}",
                    agent_id="mission_controller",
                    outcome_status="IN_PROGRESS",
                    reward_score=0.9,
                    reflection=f"Planned {plan.total_steps}-milestone autonomous roadmap for strategic goal '{top_goal.get('goal_id')}'.",
                    lesson_learned=f"Decomposed objective into multi-agent milestones across specialized agents.",
                    metadata={"mission_id": plan.mission_id, "goal_id": top_goal.get("goal_id")}
                )
            except Exception as m_err:
                executed_mission = {"status": "DISPATCH_ERROR", "error": str(m_err)}

        result = {
            "cycle_index": self.deliberation_count,
            "timestamp": now,
            "status": "DELIBERATIVE_CYCLE_COMPLETE",
            "signals_observed_count": len(active_signals),
            "strategic_goals_count": len(strategic_goals),
            "strategic_goals": strategic_goals,
            "acquired_tools_count": len(acquired_tools),
            "acquired_tools": acquired_tools,
            "active_mission": executed_mission,
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

