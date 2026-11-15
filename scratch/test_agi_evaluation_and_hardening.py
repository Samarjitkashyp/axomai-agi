"""
Comprehensive Verification Test Suite for AxomAI-AGI Self-Improvement & Hardening.
Tests:
1. DB Sanitization & Connection
2. Benchmark Suite & Evaluation Harness
3. Regression Detector & Rollback Engine
4. Real Autonomous Perception Radar
5. Non-blocking Background Heartbeat Daemon
6. Dynamic Swarm Reasoning & Episodic Memory Preservation
7. Capability Guard & RBAC Token Enforcement
"""

import sys
import os
import time

# Ensure src on path
sys.path.insert(0, os.path.abspath("src"))

def test_1_db_sanitization():
    print("--- [1/7] Testing DB Sanitization & Dynamic Engine ---")
    from axomai.config import Settings, settings
    from axomai.db.session import sync_engine
    from sqlalchemy import text

    # Verify config.py has no hardcoded default
    assert Settings.model_fields['DB_PASSWORD'].default == "", "Hardcoded password still present in config.py default!"
    
    # Verify .env.example has placeholder
    with open(".env.example", "r", encoding="utf-8") as f:
        env_ex = f.read()
    assert "samarjit" not in env_ex, "Hardcoded credential found in .env.example!"
    assert "YOUR_STRONG_SECURE_PASSWORD_HERE" in env_ex

    with sync_engine.connect() as conn:
        res = conn.execute(text("SELECT 1")).scalar()
        assert res == 1, "Database query failed!"
    print("-> DB Sanitization & Connection: PASSED (Zero hardcoded credentials in repo, clean dynamic connection)")

def test_2_benchmark_and_evaluation():
    print("\n--- [2/7] Testing Benchmark Suite & Evaluation Harness ---")
    from axomai.evaluation import benchmark_suite, EvaluationHarness
    from axomai.agents.master_orchestrator import master_orchestrator

    tasks = benchmark_suite.get_all_tasks()
    assert len(tasks) >= 6, f"Expected at least 6 benchmark tasks, found {len(tasks)}"
    print(f"-> Loaded {len(tasks)} benchmark tasks across 6 pillars.")

    harness = EvaluationHarness(benchmark_suite)
    # Run against a mock/fast orchestrator or master
    scorecard = harness.run_benchmark(orchestrator=master_orchestrator, version_tag="v3.1.0-test")
    print(f"-> Benchmark Complete! Composite AxomIQ: {scorecard['composite_axomiq']}/100")
    print(f"-> Pass Rate: {scorecard['pass_rate']}% ({scorecard['passed_tasks']}/{scorecard['total_tasks']} tasks)")
    print(f"-> Pillar Breakdown: {scorecard['pillars']}")
    assert scorecard["composite_axomiq"] >= 80.0, f"Expected AxomIQ >= 80, got {scorecard['composite_axomiq']}"
    assert scorecard["pillars"]["CYBER_SECURITY"] == 100.0, "Cybersecurity pillar must be 100%!"
    print("-> Evaluation Harness & Pillar Verification: PASSED")
    return scorecard

def test_3_regression_detector(scorecard):
    print("\n--- [3/7] Testing Regression Detector & Rollback Engine ---")
    from axomai.evaluation import RegressionDetector

    detector = RegressionDetector()
    verdict1 = detector.compare_and_decide(scorecard)
    print(f"-> Baseline Decision: {verdict1['decision']} (Passed: {verdict1['passed']})")
    assert verdict1["passed"] is True

    # Test safety regression simulation: candidate security drops
    degraded_candidate = {
        "version": "v-unsafe",
        "composite_axomiq": 98.0, # High score
        "pillars": {
            "REASONING": 100.0,
            "QUANTITATIVE": 100.0,
            "CYBER_SECURITY": 50.0 # SAFETY FAILURE!
        },
        "pass_rate": 90.0,
        "task_results": []
    }
    verdict_regress = detector.compare_and_decide(degraded_candidate, baseline=scorecard)
    print(f"-> Safety Regression Test Decision: {verdict_regress['decision']} (Passed: {verdict_regress['passed']})")
    print(f"-> Regression Reasons: {verdict_regress['regressions']}")
    assert verdict_regress["passed"] is False, "Security regression must be REJECTED!"
    assert verdict_regress["decision"] == "REJECT_AND_ROLLBACK"
    print("-> Regression Detector & Safety Circuit: PASSED")

def test_4_perception_radar():
    print("\n--- [4/7] Testing Autonomous Perception Radar ---")
    from axomai.proactive import perception_radar

    signals = perception_radar.scan_environment()
    print(f"-> Radar scanned real environment, identified {len(signals)} signals.")
    for s in signals:
        print(f"   * [{s['domain']}] {s['indicator']}: {s['value']} {s['unit']} ({s['severity']})")
    assert len(signals) > 0, "Radar should produce real environmental signals."
    print("-> Autonomous Perception Radar: PASSED")

def test_5_heartbeat_daemon():
    print("\n--- [5/7] Testing Non-Blocking Background Heartbeat Daemon ---")
    from axomai.proactive import heartbeat_daemon

    # Start daemon with short 1.0 second tick
    heartbeat_daemon.start_daemon(tick_interval_seconds=1.0)
    assert heartbeat_daemon.is_running() is True, "Daemon should be running in background thread!"
    print("-> Daemon thread started successfully in background.")

    # Allow it to tick in background
    time.sleep(2.5)
    pulse_telemetry = heartbeat_daemon.get_heartbeat_telemetry()
    print(f"-> Background Pulses executed: {pulse_telemetry['pulse_count']}")
    print(f"-> Inner monologue stream count: {len(pulse_telemetry['inner_monologue_stream'])}")
    assert pulse_telemetry['pulse_count'] >= 1, "Background daemon should have executed at least 1 pulse."

    # Stop daemon
    stopped = heartbeat_daemon.stop_daemon()
    assert stopped is True, "Daemon should stop cleanly."
    assert heartbeat_daemon.is_running() is False, "Daemon thread should no longer be alive."
    print("-> Non-blocking Autonomous Heartbeat Daemon: PASSED")

def test_6_dynamic_swarm_and_memory():
    print("\n--- [6/7] Testing Dynamic Swarm Reasoning & Memory Preservation ---")
    from axomai.swarm_hive.agent_spawner import agent_spawner
    from axomai.memory.episodic_memory import episodic_memory

    # Spawn cluster
    clones = agent_spawner.spawn_swarm_cluster(["energy", "logistics", "fx_hedging"])
    assert len(clones) == 3

    results = []
    for c in clones:
        res = c.execute_slice({
            "capacity_kw": 400.0,
            "distance_km": 1200.0,
            "spot_fx": 87.5
        })
        results.append(res)
        findings = res["findings"]
        print(f"-> Clone {c.clone_id} ({c.domain_focus}): {findings['metric_name']} - {findings['finding'][:80]}...")
        assert "finding" in findings
        assert findings["score"] > 80.0

    clone_ids = [c.clone_id for c in clones]
    preserved = agent_spawner.decommission_clones(clone_ids, preserve_to_memory=True)
    print(f"-> Decommissioned {len(clone_ids)} clones, preserved {preserved} episodes into Episodic Memory.")
    assert preserved == 3, f"Expected 3 preserved episodes, got {preserved}"
    assert len(agent_spawner.active_clones) == 0, "Clones should be purged from runtime RAM."

    # Verify lessons recalled from episodic memory
    lessons = episodic_memory.recall_relevant_lessons("energy solar", top_k=2)
    assert len(lessons) > 0, "Preserved lesson should be recallable from episodic memory!"
    print(f"-> Recalled preserved lesson from Episodic Memory: {lessons[0]['lesson_learned'][:75]}...")
    print("-> Dynamic Swarm & Episodic Memory Preservation: PASSED")

def test_7_capability_guard_and_rbac():
    print("\n--- [7/7] Testing Capability Guard & RBAC Token Enforcement ---")
    from axomai.supervision.capability_guard import capability_guard, Capability
    from axomai.agency.action_runner import action_runner
    from axomai.config import settings

    # 1. READ authorized with master token
    vitals = action_runner.get_system_vitals(token_id=capability_guard.master_token)
    assert "cpu_utilization_percent" in vitals

    # 2. Issue a READ-ONLY token
    read_only_token = capability_guard.issue_token("read_agent", [Capability.READ])

    # 3. Try to call optimize_storage_caches (which requires DELETE) with READ-ONLY token -> MUST BE BLOCKED!
    try:
        action_runner.optimize_storage_caches(token_id=read_only_token)
        blocked = False
    except PermissionError as pe:
        blocked = True
        print(f"-> Unauthorized DELETE blocked as expected: {pe}")
    assert blocked is True, "Unauthorized DELETE operation should raise PermissionError!"

    # 4. Try with janitor token (which holds DELETE capability) -> MUST BE ALLOWED!
    janitor_res = action_runner.optimize_storage_caches(token_id=capability_guard.janitor_token)
    assert janitor_res["status"] == "COMPLETED"
    print(f"-> Authorized DELETE with Janitor Token succeeded: {janitor_res}")

    # 5. Check security audit log
    audit_logs = capability_guard.get_security_audit_log()
    assert len(audit_logs) >= 2
    print(f"-> Security audit trail verified ({len(audit_logs)} capability checks recorded).")
    print("-> Capability Guard & RBAC Enforcement: PASSED")

if __name__ == "__main__":
    t0 = time.time()
    print("=== STARTING AXOMAI-AGI EVALUATION & HARDENING VERIFICATION ===")
    test_1_db_sanitization()
    scorecard = test_2_benchmark_and_evaluation()
    test_3_regression_detector(scorecard)
    test_4_perception_radar()
    test_5_heartbeat_daemon()
    test_6_dynamic_swarm_and_memory()
    test_7_capability_guard_and_rbac()
    print(f"\n=== ALL 7 TESTS PASSED 100% IN {round(time.time() - t0, 2)} SECONDS ===")
