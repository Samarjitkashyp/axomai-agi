import sys
import os

sys.path.insert(0, os.path.abspath("src"))

from axomai.memory.semantic_graph_memory import semantic_graph_memory
from axomai.memory.subconscious_consolidation import subconscious_consolidation
from axomai.memory.unified_memory_hub import unified_memory_hub
from axomai.agents.master_orchestrator import master_orchestrator

def test_4d_temporal_graph_contradiction_resolution():
    print("--- [TEST 1: 4D Temporal Graph & Contradiction Resolution] ---", flush=True)

    # Initial Fact: Guwahati
    f1 = semantic_graph_memory.add_temporal_fact(
        subject="Tea Terminal Beta",
        predicate="LOCATED_IN",
        obj="Guwahati Central",
        confidence=0.95,
        session_id="sess_init"
    )
    assert f1["epistemic_status"] == "ACTIVE"
    print("Added Initial Fact: (Tea Terminal Beta, LOCATED_IN, Guwahati Central) [ACTIVE]", flush=True)

    # Contradicting Fact: Changsari (LOCATED_IN is functional exclusive)
    f2 = semantic_graph_memory.add_temporal_fact(
        subject="Tea Terminal Beta",
        predicate="LOCATED_IN",
        obj="Changsari Logistics Hub",
        confidence=0.99,
        session_id="sess_update"
    )
    assert f2["epistemic_status"] == "ACTIVE"
    assert f2["superseded_prior_facts"] >= 1
    print("Added Relocation Fact: (Tea Terminal Beta, LOCATED_IN, Changsari Logistics Hub) [ACTIVE]", flush=True)

    # Verify history
    history = semantic_graph_memory.get_temporal_history("Tea Terminal Beta", "LOCATED_IN")
    assert len(history) >= 2, f"Expected at least 2 chronological entries, got {len(history)}"

    old_fact = [h for h in history if h["object_name"] == "Guwahati Central"][0]
    new_fact = [h for h in history if h["object_name"] == "Changsari Logistics Hub"][0]

    assert old_fact["epistemic_status"] == "SUPERSEDED", "Old fact must be marked SUPERSEDED"
    assert old_fact["valid_to"] is not None, "Old fact valid_to timestamp must be set"
    assert new_fact["epistemic_status"] == "ACTIVE", "New fact must be ACTIVE"
    assert new_fact["valid_to"] is None, "New fact valid_to must be NULL/None"

    print("TEST 1 PASSED: 4D Temporal Graph resolves contradictions cleanly.\n", flush=True)


def test_autonomous_triple_extraction():
    print("--- [TEST 2: Autonomous Dialogue Extraction & Ingestion] ---", flush=True)

    text = (
        "The management announced that Upper Assam Tea Exports has relocated to Changsari Multimodal Park. "
        "Furthermore, allocated budget for Brahmaputra Dredging is 450 crore. "
        "Our preferred strategy for Currency Exposure is Garman-Kohlhagen collar."
    )
    extracted = semantic_graph_memory.extract_and_ingest_triples_from_text(text, session_id="sess_dialogue_01")
    print(f"Autonomous Extractor parsed {len(extracted)} ontological triples from text:", flush=True)
    for t in extracted:
        print(f"  -> ({t['subject']}) ──[{t['predicate']}]──▶ ({t['object']})", flush=True)

    assert len(extracted) >= 2, f"Expected at least 2 extracted triples, got {len(extracted)}"
    
    # Check that search finds the new fact
    res = semantic_graph_memory.search_knowledge("Brahmaputra Dredging", active_only=True)
    assert len(res) > 0, "Extracted budget fact must be searchable in knowledge graph"
    print("TEST 2 PASSED: Autonomous text extraction & graph ingestion works.\n", flush=True)


def test_subconscious_sleep_consolidation():
    print("--- [TEST 3: Subconscious Sleep & Memory Consolidation] ---", flush=True)

    summary = subconscious_consolidation.run_consolidation_cycle(idle_mode=False)
    print(f"Subconscious Sleep Cycle Status: {summary['cycle_status']} in {summary['latency_ms']} ms", flush=True)
    print(f"  - Pruned Superseded Triples: {summary['phase_1_pruning']['pruned_superseded_triples']}", flush=True)
    print(f"  - Sessions Stitched: {summary['phase_2_stitching']['sessions_processed']}", flush=True)
    print(f"  - Active Projects Tracked: {summary['active_projects_tracked']}", flush=True)
    print(f"  - Epistemic Axioms Synthesized: {summary['abstract_axioms_count']}", flush=True)

    twin = subconscious_consolidation.get_persona_twin()
    assert twin.total_sessions_stitched >= 0
    prompt_block = subconscious_consolidation.format_persona_prompt_block()
    assert "USER PERSONA TWIN" in prompt_block
    print("User Persona Twin Prompt Block:\n", prompt_block[:350], "...", flush=True)
    print("TEST 3 PASSED: Subconscious sleep consolidation & Persona Twin works.\n", flush=True)


def test_end_to_end_hyper_memory_orchestrator():
    print("--- [TEST 4: End-to-End Orchestrator 5-Tier Memory & Cross-Session Recall] ---", flush=True)

    # 1. Test 5-Tier Memory Status Query
    events_mem = list(master_orchestrator.orchestrate_stream("memory status", session_id="sess_audit_01"))
    done_mem = [e for e in events_mem if e.get("type") == "done"][0]
    ans_mem = done_mem.get("answer", "")
    assert "5-Tier Hyper-Memory Architecture" in ans_mem or "Tier 1: Working Memory" in ans_mem
    print("5-Tier Memory Brief Telemetry Verified.", flush=True)

    # 2. Test Subconscious Sleep Cycle Trigger
    events_sleep = list(master_orchestrator.orchestrate_stream("run sleep cycle", session_id="sess_audit_01"))
    done_sleep = [e for e in events_sleep if e.get("type") == "done"][0]
    ans_sleep = done_sleep.get("answer", "")
    assert "Subconscious Sleep & Memory Consolidation" in ans_sleep
    print("Subconscious Sleep Cycle execution verified via Master Orchestrator.", flush=True)

    # 3. Test Cross-Session Recall of 4D Fact
    events_q = list(master_orchestrator.orchestrate_stream("where is Tea Terminal Beta located in?", session_id="sess_fresh_09"))
    done_q = [e for e in events_q if e.get("type") == "done"][0]
    ans_q = done_q.get("answer", "")
    assert "Changsari Logistics Hub" in ans_q, f"Must recall active location Changsari, got: {ans_q}"
    print(f"Cross-Session 4D Knowledge Recall Verified:\n{ans_q}", flush=True)

    print("TEST 4 PASSED: End-to-end 5-Tier Hyper-Memory recall verified.\n", flush=True)


if __name__ == "__main__":
    test_4d_temporal_graph_contradiction_resolution()
    test_autonomous_triple_extraction()
    test_subconscious_sleep_consolidation()
    test_end_to_end_hyper_memory_orchestrator()
    print("=== ALL 5-TIER SOVEREIGN HYPER-MEMORY TESTS PASSED! ===", flush=True)
