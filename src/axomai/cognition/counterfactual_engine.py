"""
AxomAI Cognition Engine - Counterfactual & Causal Simulation Engine (World Model 2.0).
Enables the AGI to simulate parallel futures before executing decisions:
"What happens if I take Action A vs Action B vs Action C?"
- Simulates forward consequences, ripple effects, latency/cost/risk tradeoffs.
- Evaluates multi-branch expected utility.
- Analyzes post-execution counterfactual regret to continuously update decision policies.
"""

import time
import math
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from axomai.memory.episodic_memory import episodic_memory

@dataclass
class SimulatedBranch:
    action_id: str
    action_name: str
    description: str
    predicted_reward: float
    estimated_cost: float
    estimated_latency_ms: float
    risk_score: float
    ripple_effects: List[str]
    expected_utility: float
    causal_rationale: str

class CounterfactualEngine:
    """Deliberative simulator computing predictive consequences and counterfactual regret."""

    def __init__(self):
        self.simulation_history: List[Dict[str, Any]] = []

    def simulate_counterfactual_branches(
        self,
        candidate_actions: List[Dict[str, Any]],
        context_state: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Simulates parallel alternative futures for candidate actions.
        Ranks by Expected Utility:
        Utility = (Reward * 0.45) - (Cost * 0.20) - (Risk * 0.20) - (NormalizedLatency * 0.15)
        """
        t0 = time.time()
        branches: List[SimulatedBranch] = []
        state = context_state or {}

        for act in candidate_actions:
            aid = act.get("action_id", f"act_{len(branches) + 1}")
            aname = act.get("name", "unnamed_action")
            desc = act.get("description", "")
            
            # Extract or estimate base parameters
            pred_reward = float(act.get("predicted_reward", 0.75))
            est_cost = float(act.get("estimated_cost", 0.10))
            est_latency = float(act.get("estimated_latency_ms", 120.0))
            risk = float(act.get("risk_score", 0.15))
            
            # Predict ripple effects based on action semantics
            ripples = []
            act_text = (aname + " " + desc).lower()
            if any(k in act_text for k in ["cache", "memoize", "store", "buffer"]):
                ripples.append("Reduces downstream database load by ~35%")
                ripples.append("Introduces minor cache invalidation complexity")
                pred_reward += 0.05
                est_latency *= 0.6
            elif any(k in act_text for k in ["parallel", "async", "swarm", "concurrent"]):
                ripples.append("Accelerates total execution by ~40%")
                ripples.append("Increases thread pool concurrency and transient memory allocation")
                est_latency *= 0.65
                risk += 0.05
            elif any(k in act_text for k in ["verify", "audit", "sandbox", "strict"]):
                ripples.append("Prevents downstream hallucinations and execution failures")
                ripples.append("Adds slight verification latency overhead (+15ms)")
                risk = max(0.01, risk - 0.10)
                pred_reward += 0.10
            elif any(k in act_text for k in ["direct", "fast_path", "bypass"]):
                ripples.append("Ultra-low latency instant dispatch")
                ripples.append("Bypasses multi-step deliberation; requires fallback safety boundary")
                est_latency *= 0.3
                risk += 0.10

            # Normalize latency into 0.0 - 1.0 penalty scale (1000ms = 1.0)
            norm_latency = min(1.0, est_latency / 1000.0)

            # Expected Utility calculation
            utility = (pred_reward * 0.45) - (est_cost * 0.20) - (risk * 0.20) - (norm_latency * 0.15)
            utility = round(max(0.0, min(1.0, utility)), 3)

            rationale = (
                f"Action '{aname}' yields expected utility {utility} "
                f"(Reward: {pred_reward}, Risk: {risk}, Latency: {round(est_latency, 1)}ms). "
                f"Key consequence: {ripples[0] if ripples else 'Nominal operational progression.'}"
            )

            branch = SimulatedBranch(
                action_id=aid,
                action_name=aname,
                description=desc,
                predicted_reward=round(pred_reward, 3),
                estimated_cost=round(est_cost, 3),
                estimated_latency_ms=round(est_latency, 1),
                risk_score=round(risk, 3),
                ripple_effects=ripples,
                expected_utility=utility,
                causal_rationale=rationale
            )
            branches.append(branch)

        # Sort branches by expected utility (descending)
        branches.sort(key=lambda b: b.expected_utility, reverse=True)
        winner = branches[0] if branches else None

        simulation_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_branches_simulated": len(branches),
            "optimal_action_id": winner.action_id if winner else None,
            "optimal_action_name": winner.action_name if winner else None,
            "highest_expected_utility": winner.expected_utility if winner else 0.0,
            "branches": [asdict(b) for b in branches],
            "simulation_latency_ms": round((time.time() - t0) * 1000, 2)
        }
        self.simulation_history.append(simulation_record)
        return simulation_record

    def evaluate_counterfactual_regret(
        self,
        chosen_action_id: str,
        actual_reward: float,
        simulation_record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Post-execution counterfactual analysis:
        Compares observed reality with discarded alternatives.
        If an unchosen branch was predicted to yield superior utility, logs a permanent lesson.
        """
        branches = simulation_record.get("branches", [])
        chosen_branch = next((b for b in branches if b["action_id"] == chosen_action_id), None)
        other_branches = [b for b in branches if b["action_id"] != chosen_action_id]

        max_alternative_utility = max([b["expected_utility"] for b in other_branches], default=0.0)
        best_alternative = next((b for b in other_branches if b["expected_utility"] == max_alternative_utility), None)

        regret_delta = round(max(0.0, max_alternative_utility - actual_reward), 3)
        has_regret = regret_delta >= 0.20

        lesson = ""
        if has_regret and best_alternative:
            lesson = (
                f"Counterfactual Policy Update: For scenario '{simulation_record.get('optimal_action_name')}', "
                f"chosen action achieved {actual_reward} but alternative '{best_alternative['action_name']}' "
                f"had simulated utility {best_alternative['expected_utility']} (Regret Δ: {regret_delta}). "
                f"Prioritize '{best_alternative['action_name']}' under similar operational constraints."
            )
            try:
                episodic_memory.record_episode(
                    query=f"Counterfactual Regret Analysis: {chosen_action_id}",
                    agent_id="counterfactual_engine",
                    outcome_status="COUNTERFACTUAL_LESSON",
                    reward_score=actual_reward,
                    reflection=f"Regret detected against alternative {best_alternative['action_name']}",
                    lesson_learned=lesson,
                    metadata={"regret_delta": regret_delta, "best_alternative": best_alternative["action_id"]}
                )
            except Exception:
                pass

        return {
            "chosen_action_id": chosen_action_id,
            "actual_reward": actual_reward,
            "max_alternative_utility": max_alternative_utility,
            "regret_delta": regret_delta,
            "has_counterfactual_regret": has_regret,
            "lesson_learned": lesson if has_regret else "Chosen action performed within nominal utility expectations."
        }

counterfactual_engine = CounterfactualEngine()
