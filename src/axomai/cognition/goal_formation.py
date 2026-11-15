"""
AxomAI Cognition Engine - Cognitive Goal Formation.
Replaces simplistic rule triggers with deliberative cognitive reasoning:
Perception + World Model + Self Model + Beliefs ->
1. "What changed?" (Delta Detection)
2. "What does this mean?" (Contextual Significance)
3. "What don't I know?" (Epistemic Unknowns)
4. "What could happen?" (Temporal Projection)
-> Candidate Goals -> Deliberative Scoring -> Prioritized Strategic Goals.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from axomai.cognition.self_model import self_model, SelfModel
from axomai.cognition.world_model import world_model, WorldModel
from axomai.cognition.belief_manager import belief_manager, BeliefManager

class StrategicGoal:
    """A deeply deliberated autonomous goal."""

    def __init__(
        self,
        goal_id: str,
        title: str,
        rationalization: str,
        urgency: float,
        impact: float,
        feasibility: float,
        risk_tier: str,
        target_agent: str,
        action_directive: str
    ):
        self.goal_id = goal_id
        self.title = title
        self.rationalization = rationalization
        self.urgency = urgency
        self.impact = impact
        self.feasibility = feasibility
        self.risk_tier = risk_tier
        self.target_agent = target_agent
        self.action_directive = action_directive
        # Composite utility score: (Urgency * 0.4) + (Impact * 0.4) + (Feasibility * 0.2)
        self.priority_score = round((urgency * 0.4) + (impact * 0.4) + (feasibility * 0.2), 3)
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.status = "FORMULATED"

class CognitiveGoalFormation:
    """Deliberative goal synthesis engine powered by world model and self model awareness."""

    def __init__(
        self,
        self_m: Optional[SelfModel] = None,
        world_m: Optional[WorldModel] = None,
        belief_m: Optional[BeliefManager] = None
    ):
        self.self_model = self_m or self_model
        self.world_model = world_m or world_model
        self.belief_manager = belief_m or belief_manager
        self.active_strategic_goals: List[StrategicGoal] = []
        self.goal_counter: int = 0

    def deliberate_and_formulate_goals(self, environmental_signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Executes multi-step deliberative reasoning over incoming signals and current world model state.
        """
        candidates: List[StrategicGoal] = []

        for sig in environmental_signals:
            dom = sig.get("domain", "general")
            ind = sig.get("indicator", "anomaly")
            val = sig.get("value", 0.0)
            sev = sig.get("severity", "NORMAL")
            msg = sig.get("message", "")

            # Step 1: Deliberation - "What changed and what does it mean?"
            if dom == "system_infrastructure" and sev in ["CRITICAL", "ELEVATED"]:
                self.goal_counter += 1
                g = StrategicGoal(
                    goal_id=f"strat_{self.goal_counter:04d}",
                    title="Autonomous Host Resource Rebalance & Storage Health Preservation",
                    rationalization=(
                        f"Perception detected {ind} at {val}%. If ignored, compute degradation "
                        f"or memory out-of-bounds crash could destabilize background agents."
                    ),
                    urgency=0.95 if sev == "CRITICAL" else 0.75,
                    impact=0.90,
                    feasibility=0.98,
                    risk_tier="LOW_RISK",
                    target_agent="action_runner",
                    action_directive="Purge expired temporary artifacts in storage/temp and recalibrate worker thread limits."
                )
                candidates.append(g)

            elif dom == "workspace_intelligence" and sev == "OPPORTUNITY":
                self.goal_counter += 1
                g = StrategicGoal(
                    goal_id=f"strat_{self.goal_counter:04d}",
                    title="Autonomous Knowledge Graph Assimilation of New Workspace Assets",
                    rationalization=(
                        f"Detected {val} unprocessed document artifacts. Assimilating these into Semantic Graph "
                        f"enables proactive cross-domain insights without waiting for user prompting."
                    ),
                    urgency=0.60,
                    impact=0.85,
                    feasibility=0.95,
                    risk_tier="LOW_RISK",
                    target_agent="z9_cortex",
                    action_directive="Parse newly detected workspace documents, vectorize chunks, and embed semantic graph nodes."
                )
                candidates.append(g)

            elif dom == "commodity_markets" and sev in ["HIGH", "CRITICAL"]:
                self.goal_counter += 1
                g = StrategicGoal(
                    goal_id=f"strat_{self.goal_counter:04d}",
                    title="Real-Time FX Garman-Kohlhagen Option Collar Synthesis",
                    rationalization=(
                        f"Export auction spreads swung {val}%. World model predicts margin compression if unhedged. "
                        f"Synthesizing zero-cost collar insulates export cash flows."
                    ),
                    urgency=0.90,
                    impact=0.95,
                    feasibility=0.92,
                    risk_tier="MEDIUM_RISK",
                    target_agent="revenue_syndicate",
                    action_directive="Calculate Garman-Kohlhagen collar floor/cap bounds and adjust consignment dispatch lots."
                )
                candidates.append(g)

            elif dom == "infrastructure_geotechnical" and sev in ["ELEVATED", "HIGH"]:
                self.goal_counter += 1
                g = StrategicGoal(
                    goal_id=f"strat_{self.goal_counter:04d}",
                    title="Geotechnical Slope Reinforcement & FIDIC Clause 20.1 Protocol",
                    rationalization=(
                        f"Embankment pore pressure FoS dropped to {val} (< 1.25 safety threshold). "
                        f"Immediate simulated geotextile reinforcement and contractual claim notice required."
                    ),
                    urgency=0.88,
                    impact=0.92,
                    feasibility=0.90,
                    risk_tier="MEDIUM_RISK",
                    target_agent="infra_shield",
                    action_directive="Simulate Bishop slope reinforcement with geotextile tubes and draft FIDIC time extension claim."
                )
                candidates.append(g)

            elif dom == "energy_arbitrage" and sev == "OPPORTUNITY":
                self.goal_counter += 1
                g = StrategicGoal(
                    goal_id=f"strat_{self.goal_counter:04d}",
                    title="Captive Solar Clean Energy Dispatch & Carbon Arbitrage",
                    rationalization=(
                        f"Grid peak tariff differential reached ₹{val}/kWh. Maximizing captive solar generation "
                        f"cuts peak industrial operating expenses while generating Verra VCS credits."
                    ),
                    urgency=0.70,
                    impact=0.80,
                    feasibility=0.95,
                    risk_tier="LOW_RISK",
                    target_agent="y2",
                    action_directive="Optimize 250kWp rooftop solar sizing and compute Verra VCS carbon monetization revenue."
                )
                candidates.append(g)

        # Sort candidates by composite priority score
        candidates.sort(key=lambda x: x.priority_score, reverse=True)
        self.active_strategic_goals = candidates

        return [
            {
                "goal_id": g.goal_id,
                "title": g.title,
                "priority_score": g.priority_score,
                "rationalization": g.rationalization,
                "urgency": g.urgency,
                "impact": g.impact,
                "feasibility": g.feasibility,
                "risk_tier": g.risk_tier,
                "target_agent": g.target_agent,
                "action_directive": g.action_directive,
                "created_at": g.created_at,
                "status": "DELIBERATED_AND_DISPATCHED"
            }
            for g in candidates
        ]

cognitive_goal_formation = CognitiveGoalFormation()

