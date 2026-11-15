"""
Automated Verification Suite for AxomAI-AGI Cognitive Core, Self-Evolution & Holographic HUD.
Tests:
1. Self-Model & Machine-Readable Introspection
2. World-Model Dynamic Representation & Temporal Forecasting
3. Capability Acquisition Loop & Dynamic Tool Synthesis
4. Epistemic Beliefs & Contradiction Detection
5. Deliberative Strategic Goal Formation
6. Closed-Loop Autonomous Self-Evolution Engine
7. Active Researcher & Knowledge Discovery
8. Live API Endpoints & Holographic UI Route
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath("src"))

def test_1_self_model():
    print("--- [1/8] Testing Introspective Self-Model ---")
    from axomai.cognition.self_model import self_model

    state = self_model.get_self_state()
    assert state["identity"] == "AxomAI Hyperion"
    assert "v4.0.0" in state["version"]
    assert state["capabilities_count"] >= 10
    assert len(state["limitations"]) > 0
    assert "cpu_utilization_pct" in state["hardware_vitals"]

    # Test introspection capability check
    can_exec, missing = self_model.can_execute_task(["multi_hop_deductive_reasoning"])
    assert can_exec is True
    assert len(missing) == 0

    can_exec_fake, missing_fake = self_model.can_execute_task(["quantum_teleportation_magic"])
    assert can_exec_fake is False
    assert "quantum_teleportation_magic" in missing_fake
    print("-> Self-Model & Introspection: PASSED")

def test_2_world_model():
    print("\n--- [2/8] Testing Dynamic World-Model & Trend Projection ---")
    from axomai.cognition.world_model import world_model

    snapshot = world_model.get_world_snapshot()
    assert snapshot["total_entities_modeled"] >= 4
    assert "changsari_logistics_hub" in snapshot["entities"]
    assert "brahmaputra_hydrology_network" in snapshot["entities"]

    # Test counterfactual risk evaluation
    risk_low = world_model.evaluate_action_risk("Analyze tea export price differences")
    assert risk_low["risk_tier"] == "LOW_RISK"
    assert risk_low["safe_to_proceed_autonomously"] is True

    risk_high = world_model.evaluate_action_risk("Purge and delete database records")
    assert risk_high["risk_tier"] == "HIGH_RISK"
    assert risk_high["requires_explicit_authorization"] is True

    # Test temporal forecasting
    world_model.record_metric_sample("storage_disk_trend", 50.0)
    world_model.record_metric_sample("storage_disk_trend", 52.0)
    forecast = world_model.predict_trend("storage_disk_trend", horizon_hours=12.0)
    assert forecast["forecast_available"] is True
    print("-> World-Model & Counterfactual Risk Evaluation: PASSED")

def test_3_capability_acquisition():
    print("\n--- [3/8] Testing Autonomous Capability Acquisition Loop ---")
    from axomai.cognition.capability_acquisition import capability_acquisition_engine
    from axomai.cognition.capability_model import capability_registry
    from axomai.cognition.self_model import self_model

    # Synthesize a new mathematical tool on the fly
    tool_code = """
def execute(base_value: float, tax_rate: float = 0.18) -> float:
    # Autonomous Tax & Land Duty Arbitrage Calculator
    return round(float(base_value) * (1.0 + float(tax_rate)), 2)
"""
    tool_name = "tax_duty_arbitrage_calculator"
    res = capability_acquisition_engine.acquire_capability(
        capability_name=tool_name,
        category="FISCAL_ARBITRAGE",
        description="Calculates gross landed invoice value with regional GST and duty.",
        python_code=tool_code,
        test_inputs=[{"base_value": 1000.0, "tax_rate": 0.18}],
        expected_outputs=[1180.0]
    )

    assert res["status"] == "CAPABILITY_ACQUIRED_AND_OPERATIONAL"
    assert capability_registry.has_capability(tool_name) is True
    
    # Test execution of newly acquired capability
    cap_def = capability_registry.get(tool_name)
    val = cap_def.execute(base_value=2500.0, tax_rate=0.12)
    assert val == 2800.0
    print(f"-> Acquired and executed new capability '{tool_name}': {val}")
    print("-> Capability Acquisition Loop: PASSED")

def test_4_belief_manager():
    print("\n--- [4/8] Testing Epistemic Beliefs & Contradiction Detection ---")
    from axomai.cognition.belief_manager import belief_manager

    summary = belief_manager.get_epistemic_summary()
    assert summary["total_beliefs"] >= 2
    assert summary["facts_count"] >= 1

    # Check contradiction detection
    contradiction = belief_manager.check_for_contradictions(
        new_claim="Bishop FoS 1.25 is totally unsafe and unacceptable.",
        topic="geotechnical_safety"
    )
    assert contradiction is not None
    print(f"-> Contradiction successfully caught against established fact: {contradiction['established_fact']}")
    print("-> Epistemic Belief Manager: PASSED")

def test_5_goal_formation():
    print("\n--- [5/8] Testing Deliberative Strategic Goal Formation ---")
    from axomai.cognition.goal_formation import cognitive_goal_formation

    mock_signals = [
        {
            "domain": "commodity_markets",
            "indicator": "Tea Export Mandi Volatility",
            "value": -4.2,
            "unit": "%",
            "severity": "HIGH",
            "message": "Spot export auction prices in Guwahati declined 4.2%."
        },
        {
            "domain": "system_infrastructure",
            "indicator": "Disk Storage Pressure",
            "value": 88.0,
            "unit": "%",
            "severity": "CRITICAL",
            "message": "Disk usage reached 88%."
        }
    ]

    goals = cognitive_goal_formation.deliberate_and_formulate_goals(mock_signals)
    assert len(goals) >= 2
    assert goals[0]["priority_score"] >= goals[1]["priority_score"]
    assert "rationalization" in goals[0]
    print(f"-> Top Deliberated Goal: {goals[0]['title']} (Score: {goals[0]['priority_score']}, Priority: {goals[0]['urgency']})")
    print("-> Cognitive Goal Formation: PASSED")

def test_6_self_evolution_engine():
    print("\n--- [6/8] Testing Closed-Loop Autonomous Self-Evolution Engine ---")
    from axomai.evolution.evolution_manager import evolution_manager

    evo_result = evolution_manager.run_self_evolution_cycle()
    print(f"-> Evolution Cycle Status: {evo_result['status']}")
    print(f"-> Selected Hypothesis: {evo_result['selected_hypothesis']['hypothesis_id']} ({evo_result['selected_hypothesis']['approach']})")
    assert evo_result["status"] == "EVOLUTION_PROMOTED"
    assert evo_result["sandbox_status"] == "HOT_PATCHED_LIVE_SUCCESS"
    print("-> Autonomous Self-Evolution Engine: PASSED")

def test_7_active_researcher():
    print("\n--- [7/8] Testing Active Researcher & Knowledge Discovery ---")
    from axomai.evolution.active_researcher import active_researcher

    dossier = active_researcher.conduct_active_research("Brahmaputra Multi-Modal Green Hydrogen Vessel Navigation")
    assert len(dossier["questions_formulated"]) == 3
    assert len(dossier["findings"]) >= 2
    print(f"-> Researched Dossier: {dossier['topic']} ({dossier['research_latency_ms']}ms)")
    print("-> Active Researcher: PASSED")

def test_8_api_and_holographic_ui():
    print("\n--- [8/8] Testing Live API Endpoints & Holographic Dashboard ---")
    from fastapi.testclient import TestClient
    from axomai.api.app import app

    client = TestClient(app)

    # 1. UI Root route returns Holographic HTML
    res_ui = client.get("/")
    assert res_ui.status_code == 200
    assert "AXOMAI // HYPERION" in res_ui.text
    assert "arc-orb-container" in res_ui.text
    print("-> Holographic AGI UI Route (GET /): PASSED (200 OK)")

    # 2. Cognition state endpoint
    res_cog = client.get("/api/cognition/state")
    assert res_cog.status_code == 200
    cog_data = res_cog.json()
    assert "self_model" in cog_data
    assert "world_model" in cog_data
    print("-> Cognition State Endpoint (GET /api/cognition/state): PASSED (200 OK)")

    # 3. Evolution cycle endpoint
    res_evo = client.post("/api/evolution/run-cycle")
    assert res_evo.status_code == 200
    assert res_evo.json()["status"] == "EVOLUTION_PROMOTED"
    print("-> Self-Evolution API Endpoint (POST /api/evolution/run-cycle): PASSED (200 OK)")

    # 4. Active research endpoint
    res_res = client.post("/api/evolution/active-research?topic=Assam%20Tea%20Genome%20Sequencing")
    assert res_res.status_code == 200
    assert res_res.json()["evidence_count"] >= 2
    print("-> Active Research API Endpoint (POST /api/evolution/active-research): PASSED (200 OK)")

if __name__ == "__main__":
    t_start = time.time()
    print("=== STARTING AXOMAI-AGI COGNITIVE CORE & EVOLUTION VERIFICATION ===")
    test_1_self_model()
    test_2_world_model()
    test_3_capability_acquisition()
    test_4_belief_manager()
    test_5_goal_formation()
    test_6_self_evolution_engine()
    test_7_active_researcher()
    test_8_api_and_holographic_ui()
    print(f"\n=== ALL 8 ADVANCED COGNITIVE MODULES PASSED 100% IN {round(time.time() - t_start, 2)} SECONDS ===")

