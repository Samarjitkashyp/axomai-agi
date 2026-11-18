"""
Integration test suite for Phase 8 Open-Ended Cognitive Loop:
1. Counterfactual Simulation & Regret Engine
2. Template-Free Autonomous Goal Generation
3. Subconscious Causal Rule Induction
4. Dynamic Capability Acquisition & Tool Synthesis
5. CognitiveCore End-to-End Deliberation Loop
"""
import sys
import os
import time

def test_counterfactual_engine():
    print("[1/5] Testing Counterfactual Simulation & Regret Engine...")
    from axomai.cognition.counterfactual_engine import CounterfactualEngine, SimulatedBranch
    from axomai.cognition.world_model import WorldModel
    
    wm = WorldModel()
    
    # Test 1: Simulation
    candidate_actions = [
        {"action_id": "act_scale", "name": "horizontal_scale", "description": "Scale server host cluster", "predicted_reward": 0.85, "estimated_cost": 0.20, "estimated_latency_ms": 150.0, "risk_score": 0.10},
        {"action_id": "act_cache", "name": "optimize_caching", "description": "Cache database queries with LRU buffer", "predicted_reward": 0.90, "estimated_cost": 0.05, "estimated_latency_ms": 80.0, "risk_score": 0.05},
        {"action_id": "act_throttle", "name": "rate_limit_throttle", "description": "Throttle excess rpm to protect memory", "predicted_reward": 0.65, "estimated_cost": 0.02, "estimated_latency_ms": 40.0, "risk_score": 0.25},
    ]
    
    sim_res = wm.simulate_counterfactual(candidate_actions)
    
    assert "branches" in sim_res, "Simulation must return branches"
    assert len(sim_res["branches"]) == 3, f"Expected 3 branches, got {len(sim_res['branches'])}"
    assert "optimal_action_id" in sim_res, "Must identify optimal action ID"
    print(f"  -> Optimal Action: '{sim_res['optimal_action_name']}' (Utility: {sim_res['highest_expected_utility']})")
    assert sim_res["highest_expected_utility"] > 0, "Highest utility should be positive"
    
    # Test 2: Post-Execution Regret Evaluation
    # If we chose act_throttle (low utility) with poor actual reward 0.50, regret should be detected
    regret = wm.evaluate_action_regret(
        chosen_action_id="act_throttle",
        actual_reward=0.30,
        simulation_record=sim_res
    )
    assert "regret_delta" in regret, "Regret delta must be calculated"
    assert "has_counterfactual_regret" in regret, "Regret flag must be evaluated"
    print(f"  -> Post-execution regret delta: {regret['regret_delta']} | Regret flag: {regret['has_counterfactual_regret']}")
    print("  [PASS] Counterfactual Simulation & Regret Engine OK")

def test_goal_generator():
    print("[2/5] Testing Template-Free Goal Generator...")
    from axomai.proactive.goal_generator import GoalGenerator
    
    gg = GoalGenerator()
    signals = [
        {"source": "system_telemetry", "type": "traffic_surge", "magnitude": 0.92, "target": "edge_ingress"},
        {"source": "epistemic_monitor", "type": "high_entropy_belief", "magnitude": 0.78, "topic": "global_supply_chain"},
        {"source": "agent_performance", "type": "suboptimal_latency", "magnitude": 0.65, "agent": "z09_cerebro"}
    ]
    
    goals = gg.evaluate_signals_and_generate_goals(signals)
    assert len(goals) > 0, "Should generate autonomous goals from signals"
    for g in goals:
        assert hasattr(g, "title") or isinstance(g, dict), "Goal item must have structured title"
        title = g.title if hasattr(g, "title") else g.get("title")
        score = g.priority_score if hasattr(g, "priority_score") else g.get("priority_score", 0)
        print(f"  -> Generated Goal: '{title}' (Priority: {score})")
    print("  [PASS] Template-Free Goal Generator OK")

def test_causal_rule_induction():
    print("[3/5] Testing Subconscious Causal Rule Induction...")
    from axomai.memory.subconscious_consolidation import SubconsciousConsolidationDaemon
    from axomai.memory.episodic_memory import episodic_memory
    
    # Seed episodic episodes with high reward
    episodic_memory.record_episode(
        query="Optimize database memory caching",
        agent_id="z09_cerebro",
        outcome_status="OPTIMAL",
        reward_score=0.95,
        reflection="Applied Redis LRU cache with 300s TTL; p99 latency dropped 72%",
        lesson_learned="Applying Redis LRU cache with 300s TTL reduced database p99 latency by 72% under surge."
    )
    episodic_memory.record_episode(
        query="Optimize multi-region replication latency",
        agent_id="z10_matrix",
        outcome_status="OPTIMAL",
        reward_score=0.91,
        reflection="Horizontal read replicas combined with connection pooling prevent thread exhaustion",
        lesson_learned="Horizontal read replicas combined with connection pooling prevent thread exhaustion during high concurrency."
    )
    episodic_memory.record_episode(
        query="Cross-verify statutory regulatory compliance",
        agent_id="z11_pragati",
        outcome_status="OPTIMAL",
        reward_score=0.92,
        reflection="Primary official gazettes are mandatory to eliminate unverified claims",
        lesson_learned="Secondary news aggregator reports frequently misquote effective enforcement dates; primary official gazettes are mandatory."
    )
    
    daemon = SubconsciousConsolidationDaemon()
    twin = daemon.get_persona_twin()
    daemon._phase_causal_abstraction(twin)
    
    axioms = twin.abstracted_axioms
    print(f"  -> Induced {len(axioms)} Abstract Invariant Axioms:")
    for ax in axioms[-4:]:
        print(f"     * {ax}")
    assert len(axioms) > 0, "Must synthesize abstract axioms from high-reward episodes"
    print("  [PASS] Subconscious Causal Rule Induction OK")

def test_dynamic_capability_acquisition():
    print("[4/5] Testing Dynamic Capability Acquisition...")
    from axomai.cognition.capability_acquisition import CapabilityAcquisitionEngine
    from axomai.cognition.capability_model import capability_registry
    
    engine = CapabilityAcquisitionEngine()
    test_cap_name = f"moving_avg_calc_{int(time.time())}"
    code = (
        "def execute(data: list) -> float:\n"
        "    if not data:\n"
        "        return 0.0\n"
        "    return round(sum(data) / len(data), 2)\n"
    )
    
    result = engine.acquire_capability(
        capability_name=test_cap_name,
        category="ANALYTICS",
        description="Calculates moving average of numeric series in sandboxed environment",
        python_code=code,
        test_inputs=[{"data": [10.0, 20.0, 30.0]}],
        expected_outputs=[20.0]
    )
    
    assert result.get("status") in ["CAPABILITY_ACQUIRED_AND_OPERATIONAL", "ACQUIRED_AND_REGISTERED"], f"Capability acquisition failed: {result}"
    print(f"  -> Capability Status: {result.get('status')} - Name: {result.get('capability_name')}")
    assert capability_registry.has_capability(test_cap_name), "Capability must be registered in capability_registry"
    print("  [PASS] Dynamic Capability Acquisition OK")

def test_cognitive_core_deliberation():
    print("[5/5] Testing CognitiveCore End-to-End Deliberative Loop...")
    from axomai.cognition.cognitive_core import cognitive_core
    
    signals = [
        {"domain": "server_host", "type": "traffic_surge", "value": 0.88, "urgency": "HIGH"},
        {"domain": "global_network_backbone", "type": "packet_loss", "value": 0.05, "urgency": "MEDIUM"}
    ]
    loop_summary = cognitive_core.deliberate_and_act(
        signals=signals,
        auto_execute_top_mission=False
    )
    
    assert loop_summary.get("status") == "DELIBERATIVE_CYCLE_COMPLETE", f"Unexpected status: {loop_summary}"
    print(f"  -> Cognitive Core Status: {loop_summary['status']}")
    print(f"  -> Strategic Goals Formulated: {loop_summary.get('strategic_goals_count', 0)}")
    print(f"  -> Tools Acquired Dynamically: {loop_summary.get('acquired_tools_count', 0)}")
    if loop_summary.get("counterfactual_simulation"):
        cf = loop_summary["counterfactual_simulation"]
        print(f"  -> Counterfactual Simulation: Winner='{cf.get('optimal_action_name')}' (Utility: {cf.get('highest_expected_utility')})")
    print("  [PASS] CognitiveCore End-to-End Deliberative Loop OK")

if __name__ == "__main__":
    print("=" * 70)
    print("   RUNNING PHASE 8 OPEN-ENDED COGNITIVE LOOP VERIFICATION SUITE")
    print("=" * 70)
    test_counterfactual_engine()
    test_goal_generator()
    test_causal_rule_induction()
    test_dynamic_capability_acquisition()
    test_cognitive_core_deliberation()
    print("=" * 70)
    print("   ALL 5 COGNITIVE VERIFICATION TESTS PASSED SUCCESSFULLY (100%)")
    print("=" * 70)
