"""
Verification Test Suite for the 4 Newly Implemented Agents:
1. Z10 Matrix (Logistics & Fleet Optimization)
2. Z11 Pragati (Assam Governance & MSME Policy)
3. Z12 Athena (Talent & Workforce Strategy)
4. Z13 Quantum (Market Surveillance & Dynamic Pricing)
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from axomai.agents.master_orchestrator import master_orchestrator
from axomai.agents.z10_matrix import z10_matrix_agent
from axomai.agents.z11_pragati import z11_pragati_agent
from axomai.agents.z12_athena import z12_athena_agent
from axomai.agents.z13_quantum import z13_quantum_agent

def test_z10_matrix():
    print("\n[TEST] 1. Z10 Matrix (Logistics & Fleet Optimization)...")
    q = "optimize fleet logistics corridor from Changsari to Nagaon and Dibrugarh with warehouse staging"
    route = master_orchestrator.classify_and_route(q)
    assert route["agent"] == "z10", f"Expected z10 routing, got {route['agent']}"
    print(f"  ✓ Master Orchestrator correctly routed to {route['name']}")

    events = list(z10_matrix_agent.logistics_stream(q))
    meta = next((e for e in events if e.get("type") == "meta"), None)
    done = next((e for e in events if e.get("type") == "done"), None)
    assert meta is not None, "Meta event missing in Z10"
    assert done is not None, "Done event missing in Z10"
    assert meta["routes_calculated"] >= 2, "Routes calculated count < 2"
    print(f"  ✓ Z10 Matrix calculated {meta['routes_calculated']} corridor routes with Changsari staging")
    print(f"  ✓ Output preview: {done['answer'][:120]}...")
    print("  ✓ Z10 MATRIX PASSED 100%")

def test_z11_pragati():
    print("\n[TEST] 2. Z11 Pragati (Assam Governance & MSME Policy)...")
    q = "what are the Assam government CMAAA subsidy and Mission Basundhara land rules for opening a business?"
    route = master_orchestrator.classify_and_route(q)
    assert route["agent"] == "z11", f"Expected z11 routing, got {route['agent']}"
    print(f"  ✓ Master Orchestrator correctly routed to {route['name']}")

    events = list(z11_pragati_agent.policy_stream(q))
    meta = next((e for e in events if e.get("type") == "meta"), None)
    done = next((e for e in events if e.get("type") == "done"), None)
    assert meta is not None, "Meta event missing in Z11"
    assert done is not None, "Done event missing in Z11"
    assert meta["matched_schemes_count"] >= 3, "Matched schemes count < 3"
    print(f"  ✓ Z11 Pragati matched {meta['matched_schemes_count']} state schemes (Top: {meta['top_scheme']})")
    print(f"  ✓ Output preview: {done['answer'][:120]}...")
    print("  ✓ Z11 PRAGATI PASSED 100%")

def test_z12_athena():
    print("\n[TEST] 3. Z12 Athena (Talent & Workforce Strategy)...")
    q = "what is the headcount staffing and salary benchmark with EPF and ESIC payroll for 3 branches in Assam?"
    route = master_orchestrator.classify_and_route(q)
    assert route["agent"] == "z12", f"Expected z12 routing, got {route['agent']}"
    print(f"  ✓ Master Orchestrator correctly routed to {route['name']}")

    events = list(z12_athena_agent.hr_stream(q))
    meta = next((e for e in events if e.get("type") == "meta"), None)
    done = next((e for e in events if e.get("type") == "done"), None)
    assert meta is not None, "Meta event missing in Z12"
    assert done is not None, "Done event missing in Z12"
    assert meta["total_headcount"] > 10, "Total headcount <= 10"
    print(f"  ✓ Z12 Athena modeled {meta['total_headcount']} staff headcount across network (Monthly Wage: ₹{meta['total_monthly_payroll_inr']:,.2f})")
    print(f"  ✓ Statutory breakdown: Take-Home ₹{meta['sample_payroll_breakdown']['net_in_hand_salary']}")
    print(f"  ✓ Output preview: {done['answer'][:120]}...")
    print("  ✓ Z12 ATHENA PASSED 100%")

def test_z13_quantum():
    print("\n[TEST] 4. Z13 Quantum (Market Surveillance & Dynamic Pricing)...")
    q = "check wholesale mandi commodity prices and GTAC tea auction rates with dynamic pricing elasticity"
    route = master_orchestrator.classify_and_route(q)
    assert route["agent"] == "z13", f"Expected z13 routing, got {route['agent']}"
    print(f"  ✓ Master Orchestrator correctly routed to {route['name']}")

    events = list(z13_quantum_agent.market_surveillance_stream(q))
    meta = next((e for e in events if e.get("type") == "meta"), None)
    done = next((e for e in events if e.get("type") == "done"), None)
    assert meta is not None, "Meta event missing in Z13"
    assert done is not None, "Done event missing in Z13"
    assert meta["benchmarks_monitored"] >= 4, "Benchmarks monitored < 4"
    print(f"  ✓ Z13 Quantum monitored {meta['benchmarks_monitored']} commodity benchmarks & modeled dynamic price elasticity")
    print(f"  ✓ Output preview: {done['answer'][:120]}...")
    print("  ✓ Z13 QUANTUM PASSED 100%")

if __name__ == "__main__":
    print("=" * 65)
    print("AXOMAI AGI - 4 NEW SPECIALIZED AGENTS VERIFICATION SUITE")
    print("=" * 65)
    test_z10_matrix()
    test_z11_pragati()
    test_z12_athena()
    test_z13_quantum()
    print("=" * 65)
    print("ALL 4 NEW AGENTS VERIFIED 100% OPERATIONAL & READY!")
    print("=" * 65)

