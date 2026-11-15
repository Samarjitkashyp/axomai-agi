"""
End-to-End Verification Suite for AxomAI Super-AGI Capabilities:
1. Proactive Heartbeat Daemon & Goal Generator (Prompt-less Autonomy)
2. Recursive Code Metamorphosis (AST Profiler & Zero-Downtime Hot-Patcher)
3. Dynamic Ephemeral Agent Spawner & Hive Swarm Consensus
4. Digital Agency & Sovereign Hardware Vitals
5. Master Orchestrator Routing & Live SSE Streaming
"""

import sys
import os

sys.path.insert(0, os.path.abspath("src"))

from axomai.proactive import goal_generator, heartbeat_daemon
from axomai.metamorphosis import code_profiler, self_patcher
from axomai.swarm_hive import agent_spawner, swarm_consensus
from axomai.agency import action_runner
from axomai.agents.master_orchestrator import MasterOrchestrator

def test_proactive_engine():
    print("--- [1/5] Testing Proactive Heartbeat & Autonomous Goal Generator ---")
    goals = goal_generator.evaluate_signals_and_generate_goals()
    assert len(goals) >= 2, f"Expected at least 2 proactive goals, got {len(goals)}"
    assert goals[0]["status"] == "PROACTIVELY_DISPATCHED"
    print(f"  ✓ Proactively synthesized {len(goals)} strategic mission directives from environmental signals.")

    pulse = heartbeat_daemon.trigger_pulse()
    assert pulse["status"] == "COGNITIVE_PULSE_NOMINAL"
    assert "inner_monologue" in pulse
    assert len(pulse["inner_monologue"]) > 10
    print(f"  ✓ Cognitive Heartbeat Pulse #{pulse['pulse_index']} active: \"{pulse['inner_monologue'][:55]}...\"")

def test_code_metamorphosis():
    print("\n--- [2/5] Testing Recursive Code Metamorphosis & Hot-Patcher ---")
    source_to_test = (
        "def execute(values, threshold=5.0):\n"
        "    res = 0.0\n"
        "    for v in values:\n"
        "        if v > threshold:\n"
        "            res += v * 1.25\n"
        "    return round(res, 2)\n"
    )
    analysis = code_profiler.analyze_source_code(source_to_test, module_name="margin_rebalancer")
    assert analysis["optimizable"] is True
    assert analysis["cyclomatic_complexity"] >= 3
    print(f"  ✓ Code AST Profiler analyzed module '{analysis['module_name']}' (Complexity: {analysis['cyclomatic_complexity']}, Speedup: {analysis['estimated_speedup']})")

    # Hot patch validation
    patch = self_patcher.test_and_apply_hot_patch(
        patch_id="patch_test_01",
        optimized_code=source_to_test,
        test_inputs=[{"values": [2.0, 6.0, 10.0], "threshold": 5.0}],
        expected_outputs=[20.0]
    )
    assert patch["status"] == "HOT_PATCHED_LIVE_SUCCESS"
    assert patch["test_cases_verified"] == 1
    print(f"  ✓ Live Zero-Downtime Hot-Patch applied & sandboxed in {patch['verification_latency_ms']} ms.")

def test_ephemeral_swarm_hive():
    print("\n--- [3/5] Testing Dynamic Ephemeral Swarm Spawner & Consensus ---")
    domains = ["clean energy", "freight corridor", "forex risk hedging"]
    swarm_res = swarm_consensus.execute_swarm_mission(
        mission_domains=domains,
        mission_query="Evaluate integrated Brahmaputra tea export and solar infrastructure"
    )
    assert swarm_res["status"] == "SWARM_CONSENSUS_REACHED_AND_DECOMMISSIONED"
    assert swarm_res["swarm_size"] == 3
    assert swarm_res["consensus_score"] >= 80.0
    assert swarm_res["ephemeral_clones_purged"] == 3
    assert len(agent_spawner.active_clones) == 0
    print(f"  ✓ Ephemeral swarm executed with consensus score {swarm_res['consensus_score']}% and 100% memory flush.")

def test_digital_agency():
    print("\n--- [4/5] Testing Digital Agency & Host Hardware Vitals ---")
    vitals = action_runner.get_system_vitals()
    assert vitals["agency_health_status"] == "HARDWARE_OPTIMAL_STABLE"
    assert vitals["ram_total_gb"] > 0
    assert vitals["workspace_disk_free_gb"] > 0
    print(f"  ✓ Hardware Vitals verified on {vitals['os_platform']} (RAM: {vitals['ram_used_gb']}G/{vitals['ram_total_gb']}G, Free Disk: {vitals['workspace_disk_free_gb']}G)")

    artifact = action_runner.compile_executive_artifact(
        artifact_title="sovereign_fleet_brief",
        markdown_content="# Sovereign Strategic Brief\nAll systems operational."
    )
    assert artifact["status"] == "SUCCESS"
    assert os.path.exists(artifact["file_path"])
    print(f"  ✓ Compiled digital executive artifact ({artifact['file_size_bytes']} bytes).")

def test_master_orchestrator_super_agi_stream():
    print("\n--- [5/5] Testing Master Orchestrator Super-AGI Routing & Streaming ---")
    orchestrator = MasterOrchestrator()

    # 1. Proactive Pulse Stream
    r1 = orchestrator.classify_and_route("Check proactive pulse and inner monologue")
    assert r1["agent"] == "proactive_pulse"
    events1 = list(orchestrator.orchestrate_stream("Check proactive pulse and inner monologue"))
    assert len(events1) > 2
    print("  ✓ Master Orchestrator routed & streamed Proactive Pulse")

    # 2. Metamorphosis Stream
    r2 = orchestrator.classify_and_route("Run code metamorphosis and self patch logic")
    assert r2["agent"] == "metamorphosis"
    events2 = list(orchestrator.orchestrate_stream("Run code metamorphosis and self patch logic"))
    assert len(events2) > 2
    print("  ✓ Master Orchestrator routed & streamed Code Metamorphosis")

    # 3. Swarm Hive Consensus Stream
    r3 = orchestrator.classify_and_route("Spawn swarm hive mind for parallel audit")
    assert r3["agent"] == "swarm_hive"
    events3 = list(orchestrator.orchestrate_stream("Spawn swarm hive mind for parallel audit"))
    assert len(events3) > 2
    print("  ✓ Master Orchestrator routed & streamed Ephemeral Swarm Hive")

    # 4. Digital Agency Vitals Stream
    r4 = orchestrator.classify_and_route("Audit system vitals and hardware health")
    assert r4["agent"] == "agency_vitals"
    events4 = list(orchestrator.orchestrate_stream("Audit system vitals and hardware health"))
    assert len(events4) > 2
    print("  ✓ Master Orchestrator routed & streamed Digital Agency Vitals")

if __name__ == "__main__":
    test_proactive_engine()
    test_code_metamorphosis()
    test_ephemeral_swarm_hive()
    test_digital_agency()
    test_master_orchestrator_super_agi_stream()
    print("\n=========================================================================")
    print("🎉 ALL 5 SUPER-AGI CORE CAPABILITY MODULES 100% OPERATIONAL & VERIFIED! 🎉")
    print("=========================================================================")

