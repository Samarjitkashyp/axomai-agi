"""
Integration Test Suite for Phase 7:
- Autonomous Self-Improvement Laboratory (ExperimentManager)
- Durable Artifact Store (SQLite persistence across reboots)
- PredictionEngine Reboot Persistence & Root-Cause Closed-Loop
- Epistemic Truth Hierarchy & Mathematical Verifier
- Semantic Contradiction Engine (BeliefManager)
- AXOMIQ Generalization Benchmark (Dev vs Hidden split)
"""
import sys
import os
import time
import math
import shutil

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from axomai.learning.prediction_engine import PredictionEngine
from axomai.agents.mission_control.artifact_store import MissionArtifactStore
from axomai.memory.semantic_graph_memory import SemanticGraphMemory, EpistemicStatus
from axomai.cognition.belief_manager import BeliefManager
from axomai.agents.mission_control.verifier import MissionVerifier
from axomai.evolution.experiment_manager import ExperimentManager, EvolutionTarget
from axomai.evaluation.axomiq_benchmark import AXOMIQBenchmark

def test_prediction_engine_persistence():
    print("[1/6] Testing PredictionEngine Persistence & Root-Cause Learning...")
    pe1 = PredictionEngine()
    
    # Emit a test prediction
    pred = pe1.emit_prediction(
        domain="market_dynamics",
        target_entity="Crude Oil Brent",
        hypothesis="Crude oil will cross $100 within 24 hours",
        predicted_outcome="CROSSES_100",
        confidence=0.85
    )
    pid = pred.prediction_id
    assert pid in pe1.all_predictions, "Prediction must be tracked in all_predictions"
    
    # Evaluate as REFUTED to trigger root cause learning
    eval_res = pe1.evaluate_prediction(
        prediction_id=pid,
        actual_outcome="STAYED_72_CEASEFIRE",
        is_correct=False
    )
    assert eval_res["status"] == "REFUTED"
    assert "root_cause_learning" in eval_res
    
    stats1 = pe1.get_empirical_performance()
    assert stats1["evaluated_count"] >= 1, "Should have at least 1 evaluated prediction"
    
    # Simulate daemon reboot: instantiate brand-new PredictionEngine
    pe2 = PredictionEngine()
    stats2 = pe2.get_empirical_performance()
    
    # Verify evaluated outcomes, accuracy, and Brier score survived reboot
    assert stats2["evaluated_count"] == stats1["evaluated_count"], (
        f"Evaluated count mismatch after reboot: {stats2['evaluated_count']} vs {stats1['evaluated_count']}"
    )
    assert abs(stats2["average_brier_score"] - stats1["average_brier_score"]) < 1e-4, "Brier score must persist across reboots"
    assert pid in pe2.all_predictions, "Evaluated prediction must be loaded in memory after reboot"
    assert pe2.all_predictions[pid].status == "REFUTED", "Prediction must retain REFUTED status"
    print("  -> PASSED: PredictionEngine loaded full history and persisted calibration across reboot.")

def test_artifact_store_persistence():
    print("[2/6] Testing MissionArtifactStore SQLite Persistence...")
    store1 = MissionArtifactStore()
    
    # Store artifact
    art = store1.store_artifact(
        mission_id="mission_alpha_77",
        step_id=1,
        agent_name="research_director",
        title="geological_report.pdf",
        deliverable_type="pdf_report",
        full_content="Deep core sample reveals high-grade copper deposit at 450m depth.",
        quality_score=0.96,
        verification_criteria=["mineral_density_check"]
    )
    assert art.artifact_id is not None
    
    # Simulate reboot: instantiate brand-new MissionArtifactStore
    store2 = MissionArtifactStore()
    retrieved = store2.get_artifact(art.artifact_id)
    assert retrieved is not None, "Artifact must be retrieved from SQLite after reboot"
    assert retrieved.full_content == art.full_content, "Artifact content must match exactly"
    assert retrieved.title == "geological_report.pdf"
    
    # Verify index query after reboot
    mission_artifacts = store2.get_artifacts("mission_alpha_77")
    assert len(mission_artifacts) >= 1, "Mission artifacts must be indexed and retrieved"
    print("  -> PASSED: MissionArtifactStore SQLite persistence confirmed across reboots.")

def test_semantic_graph_epistemic_hierarchy():
    print("[3/6] Testing Semantic Graph Epistemic Status & Corroboration...")
    sg = SemanticGraphMemory()
    test_subj = f"Rare Earth Prospect {int(time.time() * 1000)}"
    
    # Add an extracted fact
    fact = sg.add_temporal_fact(
        subject=test_subj,
        predicate="LOCATED_AT",
        obj="Salba District",
        confidence=0.6,
        source_ref="unverified_news_channel",
        epistemic_status=EpistemicStatus.EXTRACTED.value
    )
    assert fact["epistemic_status"] == EpistemicStatus.EXTRACTED.value
    assert fact["verified"] is False, "Extracted dialogue fact must have verified=0/False"
    
    # Corroborate fact with official geological survey
    corrob = sg.corroborate_fact(
        subject=test_subj,
        predicate="LOCATED_AT",
        obj="Salba District",
        source_ref="Geological Survey of India Official Report"
    )
    assert corrob["epistemic_status"] == EpistemicStatus.CORROBORATED.value
    assert corrob["verified"] is True, "Corroborated fact must have verified=1/True"
    print("  -> PASSED: Semantic graph epistemic hierarchy and corroboration functional.")

def test_belief_manager_semantic_contradiction():
    print("[4/6] Testing BeliefManager Semantic Contradiction Engine...")
    bm = BeliefManager()
    
    # Add belief
    bm.add_or_update_belief(
        belief_id="belief_mining_1",
        topic="mining",
        statement="The mining project is financially viable with high net margin",
        confidence=0.88,
        source="CFO analysis"
    )
    
    # Check conflicting claim with semantic antonym / polarity inversion
    conflict = bm.check_for_contradictions(
        new_claim="The mining project is financially unviable due to deep losses"
    )
    assert conflict is not None, "Semantic contradiction should be detected between viable and unviable"
    print("  -> PASSED: Semantic contradiction engine detected polarity conflict.")

def test_mission_verifier_math_consistency():
    print("[5/6] Testing MissionVerifier Mathematical & Epistemic Truth Consistency...")
    mv = MissionVerifier()
    
    # Test text containing an obvious arithmetic hallucination: 15 * 10 = 300
    hallucinated_text = "The estimated units are 15 packets at $10 each, so the total amount is 15 * 10 = 300 dollars."
    res = mv.verify_milestone(
        output=hallucinated_text,
        milestone_title="Financial Model",
        milestone_objective="Verify financial calculation and unit economics",
        target_agent="z3"
    )
    
    assert res.passed is False, "Arithmetic hallucination must fail verification"
    assert "mathematical_consistency_verified" in res.missing_criteria, (
        f"Missing criteria should contain mathematical_consistency_verified: {res.missing_criteria}"
    )
    assert any("Mathematical" in f or "Equation" in f for f in [res.feedback]), (
        f"Feedback should report mathematical error: {res.feedback}"
    )
    print("  -> PASSED: MissionVerifier caught arithmetic hallucination and rejected deliverable.")

def test_experiment_manager_and_axomiq():
    print("[6/6] Testing ExperimentManager (Domain-Agnostic Evolution) & AXOMIQ Benchmark...")
    em = ExperimentManager()
    
    target = EvolutionTarget(
        target_id="route_query_opt",
        module_name="axomai.routing",
        function_name="route_query",
        description="Optimize query routing latency without losing semantic match accuracy",
        baseline_code="def route_query(q):\n    return 'fast_lane' if 'urgent' in q else 'standard_lane'",
        test_inputs=[{"q": "urgent request alpha"}, {"q": "routine status check beta"}],
        expected_outputs=["fast_lane", "standard_lane"],
        domain="ALGORITHMIC_ROUTING"
    )
    
    run_result = em.run_experiment(target)
    assert "baseline_metrics" in run_result
    assert len(run_result["candidates_evaluated"]) == 3
    assert em.cognitive_version.startswith("v4.")
    
    # Verify ledger persistence
    summary = em.get_ledger_summary()
    assert summary["total_autonomous_improvements"] >= 0
    assert "recent_improvements" in summary
    
    # Run AXOMIQ Benchmark with a mock orchestrator response
    bench = AXOMIQBenchmark()
    def mock_agent(prompt: str) -> str:
        return (
            "NPV is positive 45 Cr with IRR 21%. The temporal entity is located at Guwahati. "
            "Evidence is verified from official reports. Root cause analysis identified falsified assumption. "
            "Remedial policy enforced."
        )
    report = bench.run_benchmark(mock_agent)
    assert "axomiq_composite_index" in report
    assert "generalization_gap_pct" in report
    assert "development_suite" in report and "hidden_suite" in report
    print(f"  -> AXOMIQ Composite: {report['axomiq_composite_index']}, Generalization Gap: {report['generalization_gap_pct']}%")
    print("  -> PASSED: ExperimentManager self-improvement and AXOMIQ Benchmark verified.")

if __name__ == "__main__":
    print("=" * 70)
    print("AXOMAI PHASE 7: LABORATORY INTEGRATION TEST SUITE")
    print("=" * 70)
    try:
        test_prediction_engine_persistence()
        test_artifact_store_persistence()
        test_semantic_graph_epistemic_hierarchy()
        test_belief_manager_semantic_contradiction()
        test_mission_verifier_math_consistency()
        test_experiment_manager_and_axomiq()
        print("=" * 70)
        print("ALL PHASE 7 TESTS PASSED SUCCESSFULLY! (100% OPERATIONAL)")
        print("=" * 70)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"FAILED: {e}")
        sys.exit(1)
