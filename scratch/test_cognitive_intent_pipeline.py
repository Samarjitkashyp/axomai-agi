"""
Verification Suite for 5-Layer Cognitive Intent & Language Resonance Pipeline:
1. Multi-Dimensional Query Profiler (Language, Archetype, Domain, Invariants)
2. Strategic CTO Consultation vs Implementation Gating
3. Progressive Disclosure & Real-World Domain Invariants (Shoe store variants & logistics)
4. End-to-End Orchestrator Streaming & Language Resonance
"""
import sys
import os

def test_intent_profiler():
    print("[1/3] Testing CognitiveIntentProfiler...")
    from axomai.cognition.cognitive_intent_profiler import cognitive_intent_profiler
    
    # Test Case A: User's exact query
    q_shoe = "muje ak shoes business ka website banana he jaha par mai mens aur womens aur kids ka shoes sell karunga toh muje batao muje kis technology ko use karke website banan chiye"
    p_shoe = cognitive_intent_profiler.profile_query(q_shoe)
    
    assert p_shoe.language == "hinglish", f"Expected 'hinglish', got '{p_shoe.language}'"
    assert p_shoe.intent_archetype == "ADVISORY_STRATEGY", f"Expected 'ADVISORY_STRATEGY', got '{p_shoe.intent_archetype}'"
    assert p_shoe.domain == "ecommerce", f"Expected 'ecommerce', got '{p_shoe.domain}'"
    assert p_shoe.prohibit_code_dump is True, "Must prohibit unsolicited code dumping for advice queries"
    assert len(p_shoe.domain_invariants) >= 3, "Must have real-world e-commerce invariants"
    print(f"  ✓ Query 1 Profiled: Language={p_shoe.language}, Archetype={p_shoe.intent_archetype}, Domain={p_shoe.domain}")

    # Test Case B: Explicit code request
    q_code = "python me binary search tree ka code likh kar do with unit tests"
    p_code = cognitive_intent_profiler.profile_query(q_code)
    assert p_code.language == "hinglish"
    assert p_code.intent_archetype == "IMPLEMENTATION_CODE"
    assert p_code.prohibit_code_dump is False
    print(f"  ✓ Query 2 Profiled: Language={p_code.language}, Archetype={p_code.intent_archetype}")

    # Test Case C: Pure English Concept
    q_concept = "What is the difference between event-driven architecture and microservices?"
    p_concept = cognitive_intent_profiler.profile_query(q_concept)
    assert p_concept.language == "english"
    assert p_concept.intent_archetype == "CONCEPTUAL_EXPLANATION"
    print(f"  ✓ Query 3 Profiled: Language={p_concept.language}, Archetype={p_concept.intent_archetype}")
    print("  [PASS] CognitiveIntentProfiler OK")

def test_z4_strategic_consultation():
    print("[2/3] Testing Z4 Nexus Strategic Consultation & Code Gate...")
    from axomai.agents.z4_nexus.agent import z4_nexus_agent
    
    q_shoe = "muje ak shoes business ka website banana he jaha par mai mens aur womens aur kids ka shoes sell karunga toh muje batao muje kis technology ko use karke website banan chiye"
    
    chunks = []
    meta = None
    for event in z4_nexus_agent.code_stream(query=q_shoe, session_id="test_consult_sess"):
        if event["type"] == "meta":
            meta = event
        elif event["type"] == "token":
            chunks.append(event["content"])
        elif event["type"] == "done":
            pass

    full_text = "".join(chunks)
    assert meta is not None, "Meta event must be emitted"
    assert meta.get("task_type") == "STRATEGIC_SOLUTION_DESIGN", f"Unexpected task_type: {meta.get('task_type')}"
    assert meta.get("language") == "hinglish", f"Unexpected language: {meta.get('language')}"
    
    # Verify no raw models.py / main.py toy code dump
    assert "from sqlalchemy import Column" not in full_text, "Should NOT dump raw database boilerplate"
    assert "class Shoe(Base):" not in full_text, "Should NOT dump toy shoe class"
    
    # Verify real-world domain content & progressive disclosure
    assert "Shopify" in full_text or "Option 1" in full_text
    assert "Next.js" in full_text or "Option 2" in full_text
    assert "Variant" in full_text or "variant" in full_text or "Sizes" in full_text
    print(f"  ✓ Z4 Nexus Output length: {len(full_text)} chars")
    print(f"  ✓ Preview: {full_text[:180]}...")
    print("  [PASS] Z4 Nexus Strategic Consultation OK")

def test_orchestrator_end_to_end():
    print("[3/3] Testing Master Orchestrator End-to-End Pipeline...")
    from axomai.agents.master_orchestrator import MasterOrchestrator
    orchestrator = MasterOrchestrator()
    
    q_shoe = "muje ak shoes business ka website banana he jaha par mai mens aur womens aur kids ka shoes sell karunga toh muje batao muje kis technology ko use karke website banan chiye"
    
    chunks = []
    meta = None
    for event in orchestrator.orchestrate_stream(query=q_shoe, session_id="test_orch_sess"):
        if event["type"] == "meta":
            meta = event
        elif event["type"] == "token":
            chunks.append(event["content"])
    
    full_output = "".join(chunks)
    assert len(full_output) > 200, "Output must be substantial"
    assert "class Shoe(Base):" not in full_output, "Orchestrator must NOT dump toy code"
    print(f"  ✓ Orchestrator Stream verified: {len(full_output)} characters generated")
    print("  [PASS] Master Orchestrator End-to-End OK")

if __name__ == "__main__":
    print("=" * 70)
    print("   RUNNING COGNITIVE INTENT & LANGUAGE RESONANCE VERIFICATION SUITE")
    print("=" * 70)
    test_intent_profiler()
    test_z4_strategic_consultation()
    test_orchestrator_end_to_end()
    print("=" * 70)
    print("   ALL COGNITIVE PIPELINE TESTS PASSED SUCCESSFULLY (100%)")
    print("=" * 70)
