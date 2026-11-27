"""
Comprehensive Indian Sovereign Verification Test Suite for Z17 Apex-Global
Testing all 8 Indian Corporate, Regulatory & Forensic modules + 24-Tool Master Stream.
"""

import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from axomai.agents.z17_apex_global.tools.mca_roc_lien_scanner import mca_roc_scanner
from axomai.agents.z17_apex_global.tools.gstn_forensic_reconciliation import gstn_reconciler
from axomai.agents.z17_apex_global.tools.promoter_pledge_radar import promoter_pledge_radar
from axomai.agents.z17_apex_global.tools.rpt_siphoning_scanner import rpt_siphoning_scanner
from axomai.agents.z17_apex_global.tools.rule_11ua_valuation import rule_11ua_engine
from axomai.agents.z17_apex_global.tools.nclt_ibc_resolution import nclt_ibc_resolution
from axomai.agents.z17_apex_global.tools.sebi_sast_takeover import sebi_sast_engine
from axomai.agents.z17_apex_global.tools.aif_fund_waterfall import aif_fund_waterfall
from axomai.agents.z17_apex_global.agent import z17_apex_global_agent

def test_indian_sovereign_suite():
    print("================================================================================")
    print("🇮🇳 RUNNING INDIAN SOVEREIGN 8-PILLAR VERIFICATION SUITE: Z17 APEX-GLOBAL")
    print("================================================================================")

    # 1. MCA-21 RoC Bank Liens
    print("\n--- 1. Testing MCA-21 RoC Form CHG-1 Bank Liens & DIN Scanner ---")
    roc = mca_roc_scanner.scan_corporate_charges(company_name="Tata Consumer Logistics Ltd", reported_fixed_assets_m=100.0)
    print(f"Total Open Bank Charges: {roc['total_open_charges_count']} charges | Encumbered Debt: {roc['total_encumbered_debt_inr_cr']}")
    print(f"Asset Encumbrance: {roc['asset_encumbrance_ratio']} | Risk Grade: {roc['lien_risk_grade']}")
    assert roc["total_open_charges_count"] >= 2
    assert "₹" in roc["total_encumbered_debt_inr_cr"]
    print("✅ 1. MCA-21 RoC Bank Liens: PASSED")

    # 2. GSTN Forensic Reconciliation
    print("\n--- 2. Testing GSTN GSTR-1 vs 3B vs 2B Circular Trading Radar ---")
    gst = gstn_reconciler.reconcile_tax_returns(
        reported_turnover_inr_cr=200.0,
        gstr1_outward_turnover_inr_cr=198.0,
        gstr3b_taxable_turnover_inr_cr=185.0,
        gstr2b_eligible_itc_inr_cr=22.0,
        gstr3b_claimed_itc_inr_cr=28.5
    )
    print(f"GSTIN Audit Status: {gst['gstin_audit_status']}")
    print(f"Turnover Variance: {gst['turnover_variance_cr']} ({gst['turnover_mismatch_pct']})")
    print(f"Excess ITC Claimed: {gst['excess_itc_claimed_cr']} | Clawback Exposure: {gst['statutory_gst_clawback_exposure_cr']}")
    assert "CRITICAL_CIRCULAR_TRADING_SUSPECTED" in gst["gstin_audit_status"]
    print("✅ 2. GSTN Forensic Reconciliation: PASSED")

    # 3. Promoter Share Pledging Radar
    print("\n--- 3. Testing Promoter Share Pledge & Margin Call Crash Radar ---")
    pledge = promoter_pledge_radar.analyze_promoter_pledges(
        company_name="MidCap Enterprise Ltd",
        current_share_price_inr=520.0,
        promoter_holding_pct=60.0,
        pledged_shares_pct_of_promoter=52.0
    )
    print(f"Promoter Holding: {pledge['promoter_holding_pct']} | Pledged to NBFCs: {pledge['pledged_shares_as_pct_of_promoter']}")
    print(f"Estimated Debt Raised: {pledge['estimated_promoter_debt_secured_cr']}")
    print(f"Margin Call Trigger: {pledge['margin_call_trigger_price']} | Risk: {pledge['pledge_risk_classification']}")
    assert "CRITICAL_MARGIN_CALL_EXPOSURE" in pledge["pledge_risk_classification"]
    print("✅ 3. Promoter Pledge Radar: PASSED")

    # 4. Related Party Transactions (RPT) Siphoning Scanner
    print("\n--- 4. Testing Related Party Transactions (Section 188) Siphoning Audit ---")
    rpt = rpt_siphoning_scanner.scan_related_party_transactions(
        company_name="Family Promoted Venture Ltd",
        reported_pat_inr_cr=35.0,
        reported_ebitda_inr_cr=55.0
    )
    print(f"RPT Leakage Items: {rpt['rpt_leakage_items_count']} | Annual Operational Siphoned: {rpt['annual_operational_profit_siphoned_cr']}")
    print(f"Total Diverted Capital: {rpt['total_diverted_promoter_capital_cr']}")
    print(f"Reported EBITDA: {rpt['reported_ebitda_cr']} -> Normalized True EBITDA: {rpt['normalized_true_ebitda_cr']}")
    assert rpt["rpt_leakage_items_count"] == 4
    print("✅ 4. Related Party Siphoning Scanner: PASSED")

    # 5. Income Tax Rule 11UA Angel Tax Valuation
    print("\n--- 5. Testing Income Tax Rule 11UA & Angel Tax Valuation Defense ---")
    tax_val = rule_11ua_engine.compute_rule_11ua_valuation(
        company_name="GrowthTech Private Limited",
        book_value_assets_cr=180.0,
        book_value_liabilities_cr=60.0,
        paid_up_equity_shares_cr=3.0
    )
    print(f"Rule 11UA NAV FMV: {tax_val['nav_book_value_method']['nav_per_share']}")
    print(f"Rule 11UA Merchant Banker DCF FMV: {tax_val['merchant_banker_dcf_method']['dcf_fair_market_value_per_share']}")
    print(f"Safe Harbor Band: {tax_val['statutory_safe_harbor_band']}")
    assert "DCF" in tax_val["merchant_banker_dcf_method"]["dcf_fair_market_value_per_share"] or "₹" in tax_val["merchant_banker_dcf_method"]["dcf_fair_market_value_per_share"]
    print("✅ 5. Rule 11UA Angel Tax Valuation: PASSED")

    # 6. NCLT & IBC 2016 Distressed Asset Resolution
    print("\n--- 6. Testing NCLT & IBC 2016 CIRP Resolution & Section 29A Screener ---")
    ibc = nclt_ibc_resolution.evaluate_cirp_resolution_plan(
        corporate_debtor="Distressed Power Project Ltd",
        total_admitted_claims_inr_cr=1200.0,
        secured_financial_debt_inr_cr=900.0,
        proposed_resolution_offer_inr_cr=550.0
    )
    print(f"Total Admitted Claims: {ibc['total_admitted_claims_cr']}")
    print(f"Section 29A Eligibility: {ibc['section_29a_eligibility']}")
    print(f"Secured Bank Recovery: {ibc['coc_recovery_waterfall']['secured_financial_creditors']['recovery_pct']} (Haircut: {ibc['coc_recovery_waterfall']['secured_financial_creditors']['bank_haircut_pct']})")
    assert "100% COMPLIANT" in ibc["section_29a_eligibility"]
    print("✅ 6. NCLT IBC CIRP Resolution: PASSED")

    # 7. SEBI Takeover Code (SAST 26% Open Offer)
    print("\n--- 7. Testing SEBI Takeover Code (SAST Regulations 2011) Engine ---")
    sast = sebi_sast_engine.evaluate_takeover_compliance(
        target_name="Listed Industrial Components Ltd",
        shares_outstanding_cr=15.0,
        shares_to_acquire_cr=4.5,  # 30% acquisition
        negotiated_deal_price_inr=500.0
    )
    print(f"Acquisition Stake: {sast['acquisition_stake_pct']} | Open Offer Triggered: {sast['open_offer_triggered']}")
    print(f"Mandatory 26% Open Offer Size: {sast['statutory_open_offer_shares_cr']}")
    print(f"Total Open Offer Value: {sast['open_offer_consideration_inr_cr']} | Escrow Deposit: {sast['regulation_17_escrow_deposit_inr_cr']}")
    assert "YES" in sast["open_offer_triggered"]
    assert "₹" in sast["open_offer_consideration_inr_cr"]
    print("✅ 7. SEBI Takeover Code Engine: PASSED")

    # 8. SEBI AIF Category I/II Private Equity Fund Waterfall
    print("\n--- 8. Testing SEBI AIF Private Equity Fund Waterfall Engine ---")
    aif = aif_fund_waterfall.compute_distribution_waterfall(
        total_committed_capital_inr_cr=600.0,
        total_realized_proceeds_inr_cr=1650.0,
        investment_horizon_years=5.0
    )
    print(f"Fund: {aif['fund_name']} | Structure: {aif['waterfall_structure']}")
    print(f"LP Capital Returned: {aif['distribution_tiers_inr_cr']['tier1_lp_capital_return_cr']}")
    print(f"Total LP Distributions: {aif['net_fund_realizations']['total_lp_distributions_cr']}")
    print(f"GP Carried Interest Generated: {aif['net_fund_realizations']['total_gp_carried_interest_cr']}")
    assert "₹" in aif['net_fund_realizations']['total_gp_carried_interest_cr']
    print("✅ 8. SEBI AIF Fund Waterfall Engine: PASSED")

    # 9. Master 24-Tool Agent Stream Verification
    print("\n--- 9. Testing Master Z17 Apex-Global 24-Tool Stream Execution ---")
    query = (
        "Evaluate an institutional acquisition of Assam Agro-Logistics Ltd with ₹250 Cr revenue, "
        "₹55 Cr EBITDA, 15% growth. Check MCA-21 RoC bank charges, GSTN tax reconciliation, "
        "promoter share pledging, Section 188 RPT siphoning, Rule 11UA valuation, and compile full memo."
    )
    events = list(z17_apex_global_agent.equity_research_stream(query))
    print(f"Total Master Stream Events: {len(events)}")
    
    meta_event = [e for e in events if e.get("type") == "meta"][0]
    final_event = [e for e in events if e.get("type") == "final"][0]
    
    tools = meta_event["tools_used"]
    print(f"Total Tools Orchestrated: {len(tools)} tools")
    print(f"Tools List: {tools}")
    
    assert len(tools) == 24
    assert "mca_roc_charges" in meta_event
    assert "gstn_tax_audit" in meta_event
    assert "promoter_pledge_audit" in meta_event
    assert "rpt_siphoning_audit" in meta_event
    assert "rule_11ua_valuation" in meta_event
    assert "nclt_ibc_resolution" in meta_event
    assert "sebi_sast_takeover" in meta_event
    assert "aif_fund_waterfall" in meta_event
    assert len(final_event["content"]) > 500
    print("✅ 9. Master Z17 Apex-Global 24-Tool Execution: 100% PASSED")

    print("\n================================================================================")
    print("🏆 ALL 8 INDIAN SOVEREIGN MODULES + MASTER SUITE PASSED WITH 100% PERFECTION!")
    print("================================================================================")

if __name__ == "__main__":
    test_indian_sovereign_suite()
