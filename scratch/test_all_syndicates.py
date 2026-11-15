"""
Verification test for AxomAI Mega-Syndicates:
1. Commercial Revenue Syndicate (Y1 + Z13 + Z14)
2. Sovereign Infrastructure & Energy Shield (Y2 + Y4 + Z10)
3. Institutional Wall Street & Sovereign Geopolitics Syndicate (Z17 + Y5 + Z15)
"""
import sys
import os

sys.path.insert(0, os.path.abspath("src"))

from axomai.agents.master_orchestrator import MasterOrchestrator
from axomai.syndicates import (
    commercial_revenue_syndicate,
    infrastructure_energy_shield,
    institutional_syndicate
)

def test_syndicate_routing():
    print("--- 1. Testing Master Orchestrator Syndicate Routing ---")
    orchestrator = MasterOrchestrator()
    
    # 1. Revenue Syndicate
    r1 = orchestrator.classify_and_route("Run the revenue syndicate for our Upper Assam tea export pipeline")
    print(f"Revenue Syndicate routing: {r1['agent']} ({r1['confidence']})")
    assert r1["agent"] == "revenue_syndicate", f"Expected revenue_syndicate, got {r1['agent']}"
    
    # 2. Infra Shield
    r2 = orchestrator.classify_and_route("Activate the infrastructure shield for Dibrugarh industrial solar and FIDIC claims")
    print(f"Infra Shield routing: {r2['agent']} ({r2['confidence']})")
    assert r2["agent"] == "infra_shield", f"Expected infra_shield, got {r2['agent']}"
    
    # 3. Institutional Syndicate
    r3 = orchestrator.classify_and_route("Deploy institutional syndicate for PE buyout LBO underwriting and OFAC screening")
    print(f"Institutional Syndicate routing: {r3['agent']} ({r3['confidence']})")
    assert r3["agent"] == "institutional_syndicate", f"Expected institutional_syndicate, got {r3['agent']}"
    print("[PASS] Master Orchestrator Syndicate Routing Verified!")

def test_commercial_revenue_syndicate():
    print("\n--- 2. Testing Commercial Revenue Syndicate Execution ---")
    res = list(commercial_revenue_syndicate.syndicate_stream("Optimize Upper Assam orthodox tea export pipeline to Hamburg"))
    text_chunks = [e["content"] for e in res if e.get("type") in ["token", "text", "final"]]
    full_output = "".join(text_chunks)
    assert len(full_output) > 200, f"Commercial Revenue Syndicate output too short ({len(full_output)})"
    assert "Commodity Spot/Futures Cost-of-Carry" in full_output or "Garman-Kohlhagen" in full_output
    assert "Farm-to-Export" in full_output
    print(f"[PASS] Commercial Revenue Syndicate executed cleanly ({len(res)} stream events)!")

def test_infrastructure_energy_shield():
    print("\n--- 3. Testing Sovereign Infrastructure & Energy Shield Execution ---")
    res = list(infrastructure_energy_shield.shield_stream("Audit Dibrugarh logistics park solar rooftop PPA and flood embankment FIDIC claim"))
    text_chunks = [e["content"] for e in res if e.get("type") in ["token", "text", "final"]]
    full_output = "".join(text_chunks)
    assert len(full_output) > 200, f"Infrastructure Shield output too short ({len(full_output)})"
    assert "Solar" in full_output or "FIDIC" in full_output or "Changsari" in full_output
    print(f"[PASS] Sovereign Infrastructure & Energy Shield executed cleanly ({len(res)} stream events)!")

def test_institutional_syndicate():
    print("\n--- 4. Testing Institutional Wall Street & Sovereign Geopolitics Syndicate Execution ---")
    res = list(institutional_syndicate.institutional_stream("Underwrite $25M FCF tea agro-processing acquisition with OFAC check and zero-trust audit"))
    text_chunks = [e["content"] for e in res if e.get("type") in ["token", "text", "final"]]
    full_output = "".join(text_chunks)
    assert len(full_output) > 200, f"Institutional Syndicate output too short ({len(full_output)})"
    assert "LBO" in full_output or "OFAC" in full_output or "Zero-Trust" in full_output
    print(f"[PASS] Institutional Syndicate executed cleanly ({len(res)} stream events)!")

def test_orchestrator_end_to_end():
    print("\n--- 5. Testing Master Orchestrator End-to-End Syndicate Execution ---")
    orchestrator = MasterOrchestrator()
    events = list(orchestrator.orchestrate_stream("Deploy wall street syndicate to underwrite buyout target and screen counterparties"))
    text_chunks = [e["content"] for e in events if e.get("type") in ["token", "text", "final"]]
    full_output = "".join(text_chunks)
    assert len(full_output) > 200, f"Orchestrator syndicate execution failed ({len(full_output)})"
    print(f"[PASS] Orchestrator routed and executed syndicate cleanly ({len(events)} stream events)!")

if __name__ == "__main__":
    test_syndicate_routing()
    test_commercial_revenue_syndicate()
    test_infrastructure_energy_shield()
    test_institutional_syndicate()
    test_orchestrator_end_to_end()
    print("\n=======================================================")
    print(">>> ALL 3 SYNDICATES & ORCHESTRATOR 100% OPERATIONAL! <<<")
    print("=======================================================")
