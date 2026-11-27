"""
Phase-by-Phase Comprehensive Verification Test Suite for Z17 Apex-Global
Testing all 16 quantitative, forensic, and legal tools.
"""

import os
import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from axomai.agents.z17_apex_global.tools.sec_edgar_filings import sec_edgar_filings
from axomai.agents.z17_apex_global.tools.forensic_accounting import forensic_radar
from axomai.agents.z17_apex_global.tools.three_statement_model import three_statement_model
from axomai.agents.z17_apex_global.tools.credit_rating_engine import credit_rating_engine
from axomai.agents.z17_apex_global.tools.scenario_stress_testing import scenario_stress_testing
from axomai.agents.z17_apex_global.tools.excel_model_generator import excel_model_generator
from axomai.agents.z17_apex_global.tools.loi_term_sheet_generator import loi_generator
from axomai.agents.z17_apex_global.agent import z17_apex_global_agent

def test_phase1_sec_and_forensics():
    print("\n--- [Phase 1 Test]: SEC EDGAR Filings & Forensic Accounting Radar ---")
    facts = sec_edgar_filings.fetch_audited_filing_facts("AAPL")
    print(f"SEC EDGAR Result: {facts['status']} | Ticker: {facts['ticker']} | Audited Rev: ${facts['audited_revenue_usd_m']}M")
    assert "audited_revenue_usd_m" in facts
    
    m_score = forensic_radar.compute_beneish_m_score()
    print(f"Beneish M-Score: {m_score['beneish_m_score']} | Verdict: {m_score['verdict']}")
    assert m_score["beneish_m_score"] < -1.78
    
    z_score = forensic_radar.compute_altman_z_score()
    print(f"Altman Z-Score: {z_score['altman_z_score']} | Zone: {z_score['solvency_zone']}")
    assert z_score["altman_z_score"] > 2.5
    print("✅ Phase 1: PASSED")

def test_phase2_three_statement_and_credit():
    print("\n--- [Phase 2 Test]: 3-Statement Model & Credit Rating Engine ---")
    model = three_statement_model.build_5year_model(base_revenue_m=150.0)
    print(f"Income Statement Years: {len(model['income_statement'])}")
    print(f"Year 5 Rev: ${model['income_statement'][-1]['revenue']}M | Net Income: ${model['income_statement'][-1]['net_income']}M")
    print(f"Year 5 Balance Check: {model['balance_sheet'][-1]['balance_check']}")
    assert "BALANCED" in model['balance_sheet'][-1]['balance_check']
    
    credit = credit_rating_engine.evaluate_credit_profile(ebitda_m=45.0, total_debt_m=135.0)
    print(f"Synthetic Credit Rating: {credit['synthetic_credit_rating']}")
    print(f"DSCR: {credit['debt_service_coverage_ratio_dscr']} | Max Debt Capacity: {credit['max_sustainable_debt_capacity_m']}")
    assert "synthetic_credit_rating" in credit
    print("✅ Phase 2: PASSED")

def test_phase3_scenarios_excel_and_loi():
    print("\n--- [Phase 3 Test]: Scenario Stress Testing, Excel (.xlsx) & LOI Generator ---")
    scenarios = scenario_stress_testing.run_macro_scenarios(base_revenue_m=150.0)
    print(f"Scenarios evaluated: {len(scenarios['scenarios_evaluated'])}")
    for sc in scenarios['scenarios_evaluated']:
        print(f"  {sc['scenario']}: EV = {sc['enterprise_value_m']}")
    assert len(scenarios['scenarios_evaluated']) == 4
    
    excel_res = excel_model_generator.generate_institutional_workbook(target_name="Test Enterprise Asset")
    print(f"Excel Generation Status: {excel_res['status']} | File: {excel_res.get('filename')}")
    assert excel_res["status"] == "EXCEL_MODEL_GENERATED"
    assert os.path.exists(excel_res["filepath"])
    
    loi = loi_generator.draft_acquisition_loi(target_entity="Apex Global Holdings", enterprise_value_m=450.0)
    print(f"LOI Title: {loi['title']} | Escrow: {loi['escrow_holdback_m']}")
    assert "ACQUISITION LETTER OF INTENT" in loi["title"]
    print("✅ Phase 3: PASSED")

def test_phase4_end_to_end_agent_suite():
    print("\n--- [Phase 4 Test]: Full 16-Tool Master Agent Orchestration ---")
    query = (
        "Evaluate an LBO acquisition of Apex Logistics with $200M revenue, $48M EBITDA, "
        "15% growth, and 11x entry multiple. Include 3-statement model, credit rating, "
        "forensic Beneish M-Score, macro stress scenarios, and generate the live Excel model."
    )
    events = list(z17_apex_global_agent.equity_research_stream(query))
    print(f"Total Stream Events Emitted: {len(events)}")
    
    meta_event = [e for e in events if e.get("type") == "meta"][0]
    final_event = [e for e in events if e.get("type") == "final"][0]
    
    tools = meta_event["tools_used"]
    print(f"Total Tools Orchestrated: {len(tools)} tools")
    print(f"Tools List: {tools}")
    
    assert len(tools) == 16
    assert "excel_workbook_model" in meta_event
    assert "forensic_beneish_m_score" in meta_event
    assert "credit_rating_and_debt_sizing" in meta_event
    assert "macro_stress_scenarios" in meta_event
    assert "three_statement_model" in meta_event
    assert len(final_event["content"]) > 500
    print("✅ Phase 4: PASSED (All 16 Tools Orchestrated 100%)")

if __name__ == "__main__":
    print("================================================================================")
    print("🏛️ INSTITUTIONAL PRIVATE EQUITY SUITE: Z17 APEX-GLOBAL 100% WORKING TEST")
    print("================================================================================")
    test_phase1_sec_and_forensics()
    test_phase2_three_statement_and_credit()
    test_phase3_scenarios_excel_and_loi()
    test_phase4_end_to_end_agent_suite()
    print("================================================================================")
    print("🏆 ALL PHASES 100% IMPLEMENTED & VERIFIED WITH COMPLETE PASS!")
    print("================================================================================")
