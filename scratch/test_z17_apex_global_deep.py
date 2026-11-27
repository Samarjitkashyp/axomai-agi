"""
Deep verification test suite for Z17 Apex-Global - Institutional Wall Street & Private Equity Engine.
"""

import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from axomai.agents.z17_apex_global.tools.financial_extractor import financial_extractor
from axomai.agents.z17_apex_global.tools.live_market_data import live_market_data
from axomai.agents.z17_apex_global.tools.valuation_engine import valuation_engine
from axomai.agents.z17_apex_global.tools.monte_carlo_valuation import monte_carlo_simulator
from axomai.agents.z17_apex_global.tools.accretion_dilution import accretion_dilution_engine
from axomai.agents.z17_apex_global.tools.sec_filing_parser import sec_filing_parser
from axomai.agents.z17_apex_global.tools.earnings_call_nlp import earnings_nlp_engine
from axomai.agents.z17_apex_global.tools.pmi_synergy_matrix import pmi_synergy_matrix
from axomai.agents.z17_apex_global.agent import z17_apex_global_agent

def test_financial_extractor():
    print("\n--- 1. Testing Financial Extractor ---")
    q = "Evaluate LBO buyout of Apex Logistics with $250M revenue, $55M EBITDA, 16% growth, looking for 11x multiple and 10% WACC"
    params = financial_extractor.parse_financial_query(q)
    print(f"Target: {params['target_name']}")
    print(f"Revenue: ${params['revenue_m']}M | EBITDA: ${params['ebitda_m']}M ({params['ebitda_margin_pct']}%)")
    print(f"Growth: {params['growth_pct']}% | WACC: {params['wacc_pct']}% | Entry Multiple: {params['entry_multiple']}x")
    assert params["revenue_m"] == 250.0
    assert params["ebitda_m"] == 55.0
    assert params["growth_pct"] == 16.0
    assert params["entry_multiple"] == 11.0
    print("✅ Financial Extractor: PASSED")

def test_live_market_data():
    print("\n--- 2. Testing Live Market Data & Comps ---")
    quote = live_market_data.fetch_live_quote("AAPL")
    print(f"AAPL Quote: {quote['currency']} {quote['regular_market_price']} | Exchange: {quote['exchange']}")
    comps = live_market_data.build_peer_comps(target_ticker="AAPL")
    print(f"Built {len(comps)} peer comps:")
    for c in comps:
        print(f"  {c['ticker']}: {c['price']} | EV/EBITDA: {c['ev_ebitda_multiple']} | P/E: {c['pe_multiple']}")
    assert len(comps) >= 3
    print("✅ Live Market Data & Comps: PASSED")

def test_dcf_and_lbo_engine():
    print("\n--- 3. Testing DCF & LBO Debt Waterfall Engine ---")
    dcf = valuation_engine.compute_dcf_valuation(
        base_revenue_usd_m=200.0,
        ebitda_margin_pct=25.0,
        revenue_growth_pct=15.0,
        wacc_pct=9.5,
        exit_multiple=12.0
    )
    print(f"DCF Enterprise Value (Exit Multiple): ${dcf['exit_multiple_method']['enterprise_value_usd_m']}M")
    print(f"DCF Enterprise Value (Gordon Growth): ${dcf['gordon_growth_method']['enterprise_value_usd_m']}M")
    print(f"Sensitivity Matrix (WACC vs g): {list(dcf['sensitivity_matrix_wacc_vs_g'].keys())}")
    
    lbo = valuation_engine.compute_lbo_returns(
        entry_enterprise_value_m=500.0,
        entry_ebitda_m=50.0,
        exit_multiple=12.0
    )
    print(f"LBO Sponsor Initial Equity: ${lbo['sources_and_uses']['sponsor_equity_entry_m']}M")
    print(f"LBO Exit Equity: ${lbo['sponsor_exit_equity_m']}M")
    print(f"LBO MOIC: {lbo['multiple_on_invested_capital_moic']}x | IRR: {lbo['target_irr_pct']}%")
    print(f"LBO Underwriting Verdict: {lbo['underwriting_verdict']}")
    assert lbo["multiple_on_invested_capital_moic"] > 1.5
    assert lbo["target_irr_pct"] > 10.0
    print("✅ DCF & LBO Waterfall Engine: PASSED")

def test_monte_carlo():
    print("\n--- 4. Testing 10,000-Iteration Monte Carlo Engine ---")
    mc = monte_carlo_simulator.run_dcf_simulation(base_fcf=35.0, iterations=10000)
    p = mc["distribution_percentiles"]
    print(f"Monte Carlo 10,000 Iterations Computed.")
    print(f"Bear (5th %ile): ${p['5th_percentile_bear_case']}M | Median (50th %ile): ${p['50th_percentile_median']}M | Bull (95th %ile): ${p['95th_percentile_bull_case']}M")
    print(f"Downside VaR: {mc['downside_var_95_pct']}")
    assert p["5th_percentile_bear_case"] < p["50th_percentile_median"] < p["95th_percentile_bull_case"]
    print("✅ 10,000 Monte Carlo Stochastic Engine: PASSED")

def test_accretion_dilution():
    print("\n--- 5. Testing Public M&A Accretion / Dilution Engine ---")
    acc = accretion_dilution_engine.evaluate_merger_impact(
        acquirer_name="TechTitan Inc",
        target_name="CloudTarget Corp",
        offer_premium_pct=25.0,
        pre_tax_synergies_m=35.0
    )
    print(f"Transaction Equity Value: {acc['transaction_equity_value_m']}")
    print(f"Standalone Acquirer EPS: {acc['acquirer_standalone_eps']} -> Pro Forma EPS: {acc['pro_forma_eps']}")
    print(f"Accretion/Dilution: {acc['accretion_dilution_pct']} ({acc['accretion_dilution_dollars']})")
    print(f"Verdict: {acc['deal_verdict']}")
    assert "deal_verdict" in acc
    print("✅ Accretion / Dilution Engine: PASSED")

def test_sec_and_qoe():
    print("\n--- 6. Testing Quality of Earnings (QoE) & Deal Covenants ---")
    qoe = sec_filing_parser.analyze_due_diligence_terms(
        target_entity="CloudTarget Corp",
        reported_revenue_m=180.0,
        reported_ebitda_m=38.0
    )
    rep = qoe["quality_of_earnings_qoe"]
    print(f"Reported EBITDA: ${rep['reported_ebitda_usd_m']}M -> Adjusted EBITDA: ${rep['adjusted_ebitda_usd_m']}M (Net Addbacks: +${rep['net_addbacks_usd_m']}M)")
    print(f"Escrow Holdback (10%): ${qoe['escrow_holdback_recommendation_m']}M")
    assert rep["adjusted_ebitda_usd_m"] > rep["reported_ebitda_usd_m"]
    print("✅ Quality of Earnings (QoE) & Covenants: PASSED")

def test_earnings_nlp():
    print("\n--- 7. Testing Earnings Call Linguistic Deception Engine ---")
    nlp = earnings_nlp_engine.analyze_executive_transcript(
        transcript_text="To the best of our knowledge we believe that headwinds are temporary. Frankly speaking, mistakes were made, but we couldn't be more excited.",
        speaker_title="CEO"
    )
    print(f"Deception Risk Score: {nlp['deception_risk_score']}/100 | Rating: {nlp['credibility_rating']}")
    print(f"Hedging Phrases: {nlp['detected_hedging_phrases']}")
    print(f"Distancing Phrases: {nlp['passive_voice_distancing']}")
    print(f"Defensive Superlatives: {nlp['defensive_superlatives']}")
    assert nlp["deception_risk_score"] > 20
    print("✅ Earnings NLP Deception Forensics: PASSED")

def test_end_to_end_agent_stream():
    print("\n--- 8. Testing End-to-End Z17 Apex-Global Agent Stream ---")
    query = "Evaluate LBO acquisition of Apex Industrial Tech with $180M revenue, $42M EBITDA, 14% growth rate, looking for 12x multiple"
    events = list(z17_apex_global_agent.equity_research_stream(query))
    print(f"Total Stream Events Emitted: {len(events)}")
    
    meta_event = [e for e in events if e.get("type") == "meta"][0]
    final_event = [e for e in events if e.get("type") == "final"][0]
    
    print(f"Meta Event Tools Used: {meta_event['tools_used']}")
    print(f"Final Content Preview (First 350 chars):\n{final_event['content'][:350]}...\n")
    
    assert len(meta_event["tools_used"]) == 9
    assert "Investment Committee" in final_event["content"] or "Memorandum" in final_event["content"]
    assert "Valuation" in final_event["content"] or "LBO" in final_event["content"]
    assert "Debt" in final_event["content"] or "EBITDA" in final_event["content"]
    print("✅ End-to-End Z17 Apex-Global Agent Stream: 100% PASSED")

if __name__ == "__main__":
    print("================================================================================")
    print("🚀 RUNNING INSTITUTIONAL WALL STREET TEST SUITE: Z17 APEX-GLOBAL")
    print("================================================================================")
    test_financial_extractor()
    test_live_market_data()
    test_dcf_and_lbo_engine()
    test_monte_carlo()
    test_accretion_dilution()
    test_sec_and_qoe()
    test_earnings_nlp()
    test_end_to_end_agent_stream()
    print("================================================================================")
    print("🏆 ALL 8 INSTITUTIONAL TEST SUITES PASSED WITH 100% SUCCESS!")
    print("================================================================================")
