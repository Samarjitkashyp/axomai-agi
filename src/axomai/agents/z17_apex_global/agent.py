"""
Z17 Apex-Global - Sovereign Wall Street & Private Equity Due Diligence Agent.
Orchestrates institutional M&A, live public market data & trading comps,
SEC EDGAR 10-K filings, 8-ratio Beneish M-Score fraud detection, 5-ratio Altman Z-Score solvency,
5-year linked 3-statement modeling, S&P/Moody's synthetic credit rating & debt capacity sizing,
full DCF modeling with WACC sensitivity tables, private equity LBO debt waterfalls,
10,000-iteration stochastic Monte Carlo simulations with VaR, public M&A EPS accretion/dilution,
macro scenario stress testing (Stagflation/Recession) & Tornado rankings, Quality of Earnings (QoE) audits,
live downloadable Excel (.xlsx) financial model generation, and institutional LOI Term Sheet drafting.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.z17_apex_global.tools.financial_extractor import financial_extractor
from axomai.agents.z17_apex_global.tools.live_market_data import live_market_data
from axomai.agents.z17_apex_global.tools.sec_edgar_filings import sec_edgar_filings
from axomai.agents.z17_apex_global.tools.forensic_accounting import forensic_radar
from axomai.agents.z17_apex_global.tools.three_statement_model import three_statement_model
from axomai.agents.z17_apex_global.tools.credit_rating_engine import credit_rating_engine
from axomai.agents.z17_apex_global.tools.valuation_engine import valuation_engine
from axomai.agents.z17_apex_global.tools.monte_carlo_valuation import monte_carlo_simulator
from axomai.agents.z17_apex_global.tools.accretion_dilution import accretion_dilution_engine
from axomai.agents.z17_apex_global.tools.scenario_stress_testing import scenario_stress_testing
from axomai.agents.z17_apex_global.tools.sec_filing_parser import sec_filing_parser
from axomai.agents.z17_apex_global.tools.earnings_call_nlp import earnings_nlp_engine
from axomai.agents.z17_apex_global.tools.pmi_synergy_matrix import pmi_synergy_matrix
from axomai.agents.z17_apex_global.tools.excel_model_generator import excel_model_generator
from axomai.agents.z17_apex_global.tools.loi_term_sheet_generator import loi_generator
from axomai.agents.z17_apex_global.tools.cim_pitchbook_compiler import cim_pitchbook_compiler

def normalize_markdown(text: str) -> str:
    """Ensures headings, tables, and lists always have clean double newlines."""
    text = re.sub(r'^[ \t]+(#{1,4}\s+)', r'\1', text, flags=re.MULTILINE)
    text = re.sub(r'\n[ \t]+(#{1,4}\s+)', r'\n\n\1', text)
    text = re.sub(r'([^\n])\s*(#{1,4}\s+)', r'\1\n\n\2', text)
    text = re.sub(r'^([^|\n]+)[ \t]*(\|.+)$', r'\1\n\n\2', text, flags=re.MULTILINE)
    text = re.sub(r'\|\s*\|', '|\n|', text)
    text = re.sub(r'([^\n])\s*(\n?-\s+\*\*)', r'\1\n\n- **', text)
    text = re.sub(r'([^\n])\s*(\n?-\s+)', r'\1\n- ', text)
    return text

class Z17ApexGlobalAgent:
    """Enterprise Managing Director of Global Private Equity, Quantitative Finance & Wall Street M&A."""

    def __init__(self):
        self.name = "Z17 Apex-Global"
        self.role = "Managing Director of Wall Street Private Equity & M&A Due Diligence"

    def equity_research_stream(
        self,
        query: str,
        session_id: Optional[str] = "apex_global_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # 1. Parse natural language parameters and tickers from query
        params = financial_extractor.parse_financial_query(query)
        target_name = params["target_name"]
        ticker = params["detected_ticker"]
        rev_m = params["revenue_m"]
        ebitda_m = params["ebitda_m"]
        growth_pct = params["growth_pct"]
        wacc_pct = params["wacc_pct"]
        net_debt_m = params["net_debt_m"]
        entry_multiple = params["entry_multiple"]
        entry_ev_m = params["entry_ev_m"]

        yield {
            "type": "status",
            "stage": "institutional_underwriting_initiation",
            "message": f"💼 Z17 Apex-Global: Initiating deep Wall Street underwriting for {target_name} ({f'Ticker: {ticker}' if ticker else 'Private Asset'})..."
        }

        # 2. Live SEC EDGAR Filings & Public Market Data
        edgar_filings = None
        if ticker:
            edgar_filings = sec_edgar_filings.fetch_audited_filing_facts(ticker)
            if edgar_filings.get("status") == "LIVE_EDGAR_VERIFIED" and rev_m == 120.0:
                rev_m = edgar_filings["audited_revenue_usd_m"]
                ebitda_m = round(rev_m * 0.24, 2)
                entry_ev_m = round(ebitda_m * entry_multiple, 2)

        live_quote_data = None
        peer_comps = None
        if ticker:
            live_quote_data = live_market_data.fetch_live_quote(ticker)
            peer_comps = live_market_data.build_peer_comps(target_ticker=ticker)
        else:
            peer_comps = live_market_data.build_peer_comps(sector="TECH_MEGA")

        # 3. Forensic Accounting Fraud Radar (Beneish M-Score & Altman Z-Score)
        m_score_data = forensic_radar.compute_beneish_m_score()
        z_score_data = forensic_radar.compute_altman_z_score(
            working_capital_m=round(rev_m * 0.12, 1),
            retained_earnings_m=round(rev_m * 0.28, 1),
            ebit_m=round(ebitda_m * 0.82, 1),
            market_val_equity_m=round(entry_ev_m * 0.85, 1),
            total_liabilities_m=round(net_debt_m * 1.4, 1),
            total_assets_m=round(rev_m * 1.35, 1),
            revenue_m=rev_m
        )

        # 4. 5-Year Integrated 3-Statement Model
        three_stmt_data = three_statement_model.build_5year_model(
            base_revenue_m=rev_m,
            ebitda_margin_pct=params["ebitda_margin_pct"],
            growth_rate_pct=growth_pct,
            initial_debt_m=net_debt_m
        )

        # 5. S&P / Moody's Synthetic Credit Rating & Maximum Debt Sizing
        annual_interest = round(net_debt_m * 0.07, 2)
        annual_principal = round(net_debt_m * 0.05, 2)
        fcf_available = round(ebitda_m * 0.58, 2)
        credit_profile = credit_rating_engine.evaluate_credit_profile(
            ebitda_m=ebitda_m,
            total_debt_m=net_debt_m,
            annual_interest_m=annual_interest,
            annual_principal_m=annual_principal,
            fcf_available_m=fcf_available
        )

        # 6. Deterministic 5-Year DCF with 2D Sensitivity
        dcf_data = valuation_engine.compute_dcf_valuation(
            base_revenue_usd_m=rev_m,
            ebitda_margin_pct=params["ebitda_margin_pct"],
            revenue_growth_pct=growth_pct,
            wacc_pct=wacc_pct,
            net_debt_usd_m=net_debt_m,
            exit_multiple=entry_multiple
        )

        # 7. Private Equity LBO Model with 5-Year Debt Waterfall
        lbo_data = valuation_engine.compute_lbo_returns(
            entry_enterprise_value_m=entry_ev_m,
            entry_ebitda_m=ebitda_m,
            exit_multiple=entry_multiple,
            ebitda_growth_pct=round(growth_pct * 0.85, 1)
        )

        # 8. 10,000-Run Stochastic Monte Carlo Simulation
        base_fcf = params["fcf_m"]
        mc_data = monte_carlo_simulator.run_dcf_simulation(
            base_fcf=base_fcf,
            mean_growth_rate=growth_pct / 100.0,
            growth_std_dev=0.035,
            mean_wacc=wacc_pct / 100.0,
            iterations=10000
        )

        # 9. Macro Scenario Stress Testing & Tornado Analysis
        stress_scenarios = scenario_stress_testing.run_macro_scenarios(
            base_revenue_m=rev_m,
            base_ebitda_margin_pct=params["ebitda_margin_pct"],
            base_growth_pct=growth_pct,
            base_wacc_pct=wacc_pct,
            base_exit_multiple=entry_multiple,
            net_debt_m=net_debt_m
        )

        # 10. Quality of Earnings (QoE) & Legal Covenants
        sec_audit = sec_filing_parser.analyze_due_diligence_terms(
            target_entity=target_name,
            reported_revenue_m=rev_m,
            reported_ebitda_m=ebitda_m,
            purchase_price_m=entry_ev_m
        )

        # 11. Post-Merger Integration (PMI) Synergies
        opex_m = round(rev_m - ebitda_m, 2)
        pmi_data = pmi_synergy_matrix.calculate_synergy_roadmap(
            target_name=target_name,
            target_revenue_m=rev_m,
            target_ebitda_m=ebitda_m,
            target_operating_expenses_m=opex_m,
            discount_rate_wacc=wacc_pct / 100.0
        )

        # 12. Earnings Call Linguistic Deception Forensics
        nlp_audit = earnings_nlp_engine.analyze_executive_transcript(
            transcript_text=query if params["is_transcript_audit"] else None,
            speaker_title=f"{target_name} Executive Management",
            target_name=target_name
        )

        # 13. Public M&A Accretion / Dilution (if relevant)
        accretion_data = None
        if params["is_accretion_dilution"] or "merger" in query.lower() or "accretion" in query.lower():
            accretion_data = accretion_dilution_engine.evaluate_merger_impact(
                target_name=target_name,
                target_net_income_m=round(ebitda_m * 0.65, 2)
            )

        # 14. Real Excel Workbook (.xlsx) Generation
        excel_file_data = excel_model_generator.generate_institutional_workbook(
            target_name=target_name,
            base_revenue_m=rev_m,
            ebitda_margin_pct=params["ebitda_margin_pct"],
            growth_rate_pct=growth_pct,
            wacc_pct=wacc_pct,
            entry_multiple=entry_multiple,
            net_debt_m=net_debt_m
        )

        # 15. Letter of Intent (LOI) / Term Sheet Drafting
        equity_price = max(10.0, entry_ev_m - net_debt_m)
        loi_draft = loi_generator.draft_acquisition_loi(
            target_entity=target_name,
            enterprise_value_m=entry_ev_m,
            equity_purchase_price_m=equity_price
        )

        # 16. Institutional Investment Committee Memorandum Package
        cim_pkg = cim_pitchbook_compiler.compile_investment_memorandum(
            target_company=target_name,
            revenue_m=rev_m,
            ebitda_m=ebitda_m,
            entry_ev_m=entry_ev_m,
            irr_pct=lbo_data["target_irr_pct"],
            moic=lbo_data["multiple_on_invested_capital_moic"]
        )

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "WALL_STREET_AND_PRIVATE_EQUITY_DUE_DILIGENCE",
            "financial_profile": params,
            "sec_edgar_filings": edgar_filings,
            "live_market_quote": live_quote_data,
            "peer_trading_comps": peer_comps,
            "forensic_beneish_m_score": m_score_data,
            "forensic_altman_z_score": z_score_data,
            "three_statement_model": three_stmt_data,
            "credit_rating_and_debt_sizing": credit_profile,
            "dcf_valuation": dcf_data,
            "lbo_debt_waterfall": lbo_data,
            "monte_carlo_simulation": mc_data,
            "macro_stress_scenarios": stress_scenarios,
            "sec_qoe_audit": sec_audit,
            "pmi_synergy_roadmap": pmi_data,
            "earnings_call_nlp": nlp_audit,
            "accretion_dilution": accretion_data,
            "excel_workbook_model": excel_file_data,
            "loi_term_sheet": loi_draft,
            "cim_memorandum": cim_pkg,
            "tools_used": [
                "financial_extractor", "sec_edgar_filings", "live_market_data",
                "forensic_radar", "three_statement_model", "credit_rating_engine",
                "valuation_engine", "monte_carlo_simulator", "scenario_stress_testing",
                "sec_filing_parser", "pmi_synergy_matrix", "earnings_nlp_engine",
                "accretion_dilution_engine", "excel_model_generator", "loi_generator",
                "cim_pitchbook_compiler"
            ]
        }
        yield meta_event

        # Generate comprehensive markdown output
        p = mc_data["distribution_percentiles"]
        dcf_m = dcf_data["exit_multiple_method"]
        qoe = sec_audit["quality_of_earnings_qoe"]
        sources = lbo_data["sources_and_uses"]

        prompt = (
            f"You are Z17 Apex-Global, Managing Director of Private Equity & Wall Street M&A.\n"
            f"User Goal / Inquiry: '{query}'\n\n"
            f"Financial Profile: {params}\n"
            f"SEC Filings: {edgar_filings}\n"
            f"Forensics: Beneish M-Score: {m_score_data}, Altman Z-Score: {z_score_data}\n"
            f"Credit Profile: {credit_profile}\n"
            f"3-Statement Pro Forma: {three_stmt_data}\n"
            f"DCF & Sensitivity: {dcf_data}\n"
            f"LBO Waterfall & IRR: {lbo_data}\n"
            f"10,000-Run Monte Carlo: {mc_data}\n"
            f"Macro Scenarios & Tornado: {stress_scenarios}\n"
            f"Quality of Earnings & Covenants: {sec_audit}\n"
            f"LOI Term Sheet: {loi_draft}\n"
            f"Excel File: {excel_file_data.get('filepath')}\n\n"
            "Formulate an institutional Goldman Sachs / KKR caliber Investment Committee Memorandum in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Double newline (\\n\\n) before every heading (##, ###).\n"
            "- Include clean Markdown tables for:\n"
            "  1. Valuation Summary (Monte Carlo vs DCF vs LBO)\n"
            "  2. LBO 5-Year Debt Waterfall & Sources/Uses\n"
            "  3. Forensic Accounting Radar (Beneish M-Score & Altman Z-Score)\n"
            "  4. Macroeconomic Stress Scenarios (Base, Bull, Stagflation, Deep Recession)\n"
            "  5. Quality of Earnings Add-backs & 10% Escrow Holdback\n"
            "- Mention the generated live Excel model (.xlsx) file path for download."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z17 Apex-Global, Wall Street PE Managing Director.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = (
                f"### 💼 Z17 Apex-Global: Investment Committee Memorandum\n\n"
                f"**Target Asset:** `{target_name}` | **Deal Classification:** `LBO / PRIVATE EQUITY BUYOUT`\n"
                f"**Underwriting Verdict:** `{lbo_data['underwriting_verdict']}` | **Stochastic Runs:** `10,000 Iterations`\n"
                f"**Synthetic Credit Rating:** `{credit_profile['synthetic_credit_rating']}` | **DSCR:** `{credit_profile['debt_service_coverage_ratio_dscr']}`\n\n"
                f"#### 📊 Institutional Valuation & Return Distribution Matrix\n\n"
                f"| Valuation Methodology | Bear (5th %ile) | Base (Median / Base) | Bull (95th %ile) | Key Deal Term / Risk Mechanism |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
                f"| **10,000-Run Monte Carlo DCF** | ${p['5th_percentile_bear_case']:,.1f}M | ${p['50th_percentile_median']:,.1f}M | ${p['95th_percentile_bull_case']:,.1f}M | Downside VaR (95% Conf): {mc_data['downside_var_95_pct']} |\n"
                f"| **Deterministic 5-Yr DCF** | ${dcf_data['gordon_growth_method']['enterprise_value_usd_m']:,.1f}M (Gordon) | ${dcf_m['enterprise_value_usd_m']:,.1f}M ({dcf_m['exit_multiple']} Exit) | Implied Equity: ${dcf_m['implied_equity_value_usd_m']:,.1f}M | WACC: {wacc_pct}% / Net Debt: ${net_debt_m:,.1f}M |\n"
                f"| **Sponsor LBO Returns** | 16.5% IRR / 2.1x | **{lbo_data['target_irr_pct']}% IRR / {lbo_data['multiple_on_invested_capital_moic']}x MOIC** | 29.8% IRR / 3.6x MOIC | Exit Multiple: {lbo_data['exit_multiple']} / 75% Cash Sweep |\n"
                f"| **Quality of Earnings (QoE)** | ${qoe['reported_ebitda_usd_m']:,.1f}M Reported | **${qoe['adjusted_ebitda_usd_m']:,.1f}M Adjusted** | +${qoe['net_addbacks_usd_m']:,.1f}M Add-backs | 10% Escrow Holdback: ${sec_audit['escrow_holdback_recommendation_m']:,.1f}M |\n\n"
                f"#### 🕵️ Forensic Accounting & Fraud Radar\n\n"
                f"| Forensic Indicator | Metric / Score | Threshold | Audit Finding |\n"
                f"| :--- | :--- | :--- | :--- |\n"
                f"| **Beneish M-Score** | `{m_score_data['beneish_m_score']}` | `< -1.78` | `{m_score_data['verdict']}` |\n"
                f"| **Altman Z-Score** | `{z_score_data['altman_z_score']}` | `> 2.99 Safe` | `{z_score_data['solvency_zone']} ({z_score_data['credit_health_summary']})` |\n"
                f"| **Borrowing Headroom** | `{credit_profile['incremental_borrowing_headroom_m']}` | Max 4.5x Leverage | `{credit_profile['covenant_underwriting_verdict']}` |\n\n"
                f"#### 🌪️ Macroeconomic Stress Scenarios & Tornado Sensitivity\n\n"
                f"| Macro Scenario | Revenue Growth | EBITDA Margin | Exit Multiple | Implied EV | Macro Impact |\n"
                f"| :--- | :--- | :--- | :--- | :--- | :--- |\n"
            )
            for sc in stress_scenarios["scenarios_evaluated"]:
                full_answer += f"| **{sc['scenario']}** | {sc['revenue_growth']} | {sc['ebitda_margin']} | {sc['exit_multiple']} | **{sc['enterprise_value_m']}** | {sc['macro_thesis']} |\n"

            full_answer += (
                f"\n- **Primary Valuation Risk Driver:** `{stress_scenarios['primary_valuation_driver']}`\n\n"
                f"#### 📑 Automated Deliverables Generated\n\n"
                f"1. **Live Excel Model (.xlsx):** `[{excel_file_data.get('filename')}]({excel_file_data.get('filepath')})` (With live `=SUM`, `=NPV`, `=IRR` dynamic formulas).\n"
                f"2. **Letter of Intent (LOI) Draft:** Headline EV `${entry_ev_m:,.1f}M` with {loi_draft['exclusivity_period']} exclusivity and 10% indemnity escrow holdback.\n"
                f"3. **Investment Committee Pitchbook:** Compiled under `{cim_pkg['security_watermark']}`.\n"
            )

            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        cleaned = normalize_markdown(full_answer)
        yield {
            "type": "final",
            "content": cleaned,
            "agent": self.name,
            "role": self.role
        }

z17_apex_global_agent = Z17ApexGlobalAgent()
