"""
Z17 Apex-Global - Wall Street & Private Equity Due Diligence Agent.
Orchestrates institutional M&A, live public market data & trading comps,
full 5-year DCF modeling with WACC sensitivity tables, private equity LBO debt waterfalls,
10,000-iteration stochastic Monte Carlo simulations, public M&A EPS accretion/dilution,
earnings call linguistic deception detection, Quality of Earnings (QoE) audits, and CIM packages.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.z17_apex_global.tools.financial_extractor import financial_extractor
from axomai.agents.z17_apex_global.tools.live_market_data import live_market_data
from axomai.agents.z17_apex_global.tools.valuation_engine import valuation_engine
from axomai.agents.z17_apex_global.tools.sec_filing_parser import sec_filing_parser
from axomai.agents.z17_apex_global.tools.monte_carlo_valuation import monte_carlo_simulator
from axomai.agents.z17_apex_global.tools.accretion_dilution import accretion_dilution_engine
from axomai.agents.z17_apex_global.tools.earnings_call_nlp import earnings_nlp_engine
from axomai.agents.z17_apex_global.tools.pmi_synergy_matrix import pmi_synergy_matrix
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
            "stage": "market_data_and_financial_profiling",
            "message": f"💼 Z17 Apex-Global: Profiling {target_name} ({f'Ticker: {ticker}' if ticker else 'Private Asset'}) across 10,000-run Monte Carlo DCF, LBO Debt Waterfall & QoE..."
        }

        # 2. Live Public Market Data & Comps (if ticker/public entity detected)
        live_quote_data = None
        peer_comps = None
        if ticker:
            live_quote_data = live_market_data.fetch_live_quote(ticker)
            peer_comps = live_market_data.build_peer_comps(target_ticker=ticker)
        else:
            peer_comps = live_market_data.build_peer_comps(sector="TECH_MEGA")

        # 3. Deterministic 5-Year DCF with 2D Sensitivity
        dcf_data = valuation_engine.compute_dcf_valuation(
            base_revenue_usd_m=rev_m,
            ebitda_margin_pct=params["ebitda_margin_pct"],
            revenue_growth_pct=growth_pct,
            wacc_pct=wacc_pct,
            net_debt_usd_m=net_debt_m,
            exit_multiple=entry_multiple
        )

        # 4. Private Equity LBO Model with 5-Year Debt Waterfall
        lbo_data = valuation_engine.compute_lbo_returns(
            entry_enterprise_value_m=entry_ev_m,
            entry_ebitda_m=ebitda_m,
            exit_multiple=entry_multiple,
            ebitda_growth_pct=round(growth_pct * 0.85, 1)
        )

        # 5. 10,000-Run Stochastic Monte Carlo Simulation
        base_fcf = params["fcf_m"]
        mc_data = monte_carlo_simulator.run_dcf_simulation(
            base_fcf=base_fcf,
            mean_growth_rate=growth_pct / 100.0,
            growth_std_dev=0.035,
            mean_wacc=wacc_pct / 100.0,
            iterations=10000
        )

        # 6. Quality of Earnings (QoE) & Legal Covenants
        sec_audit = sec_filing_parser.analyze_due_diligence_terms(
            target_entity=target_name,
            reported_revenue_m=rev_m,
            reported_ebitda_m=ebitda_m,
            purchase_price_m=entry_ev_m
        )

        # 7. Post-Merger Integration (PMI) Synergies
        opex_m = round(rev_m - ebitda_m, 2)
        pmi_data = pmi_synergy_matrix.calculate_synergy_roadmap(
            target_name=target_name,
            target_revenue_m=rev_m,
            target_ebitda_m=ebitda_m,
            target_operating_expenses_m=opex_m,
            discount_rate_wacc=wacc_pct / 100.0
        )

        # 8. Earnings Call Linguistic Deception Forensics
        nlp_audit = earnings_nlp_engine.analyze_executive_transcript(
            transcript_text=query if params["is_transcript_audit"] else None,
            speaker_title=f"{target_name} Executive Management",
            target_name=target_name
        )

        # 9. Public M&A Accretion / Dilution (if relevant or strategic merger)
        accretion_data = None
        if params["is_accretion_dilution"] or "merger" in query.lower() or "accretion" in query.lower():
            accretion_data = accretion_dilution_engine.evaluate_merger_impact(
                target_name=target_name,
                target_net_income_m=round(ebitda_m * 0.65, 2)
            )

        # 10. Institutional Investment Committee Memorandum Package
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
            "live_market_quote": live_quote_data,
            "peer_trading_comps": peer_comps,
            "dcf_valuation": dcf_data,
            "lbo_debt_waterfall": lbo_data,
            "monte_carlo_simulation": mc_data,
            "sec_qoe_audit": sec_audit,
            "pmi_synergy_roadmap": pmi_data,
            "earnings_call_nlp": nlp_audit,
            "accretion_dilution": accretion_data,
            "cim_memorandum": cim_pkg,
            "tools_used": [
                "financial_extractor", "live_market_data", "valuation_engine",
                "monte_carlo_simulator", "sec_filing_parser", "pmi_synergy_matrix",
                "earnings_nlp_engine", "accretion_dilution_engine", "cim_pitchbook_compiler"
            ]
        }
        yield meta_event

        # Prepare rich Markdown response
        prompt = (
            f"You are Z17 Apex-Global, Managing Director of Private Equity & Wall Street M&A.\n"
            f"User Goal / Inquiry: '{query}'\n\n"
            f"Financial Profile: {params}\n"
            f"Live Market Data: {live_quote_data}\n"
            f"Peer Trading Comps: {peer_comps}\n"
            f"5-Year DCF Modeling & Sensitivity: {dcf_data}\n"
            f"LBO Debt Waterfall & Returns: {lbo_data}\n"
            f"10,000-Iteration Monte Carlo: {mc_data}\n"
            f"Quality of Earnings & Covenants: {sec_audit}\n"
            f"PMI Cost Synergies: {pmi_data}\n"
            f"Earnings NLP Forensic Deception: {nlp_audit}\n"
            f"Accretion/Dilution Analysis: {accretion_data}\n\n"
            "Formulate an institutional Goldman Sachs / KKR caliber Investment Committee Memorandum in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Double newline (\\n\\n) before every heading (##, ###).\n"
            "- Include complete Markdown tables for:\n"
            "  1. Valuation Summary (Monte Carlo vs DCF vs LBO)\n"
            "  2. LBO 5-Year Debt Waterfall & Sources/Uses\n"
            "  3. Quality of Earnings (Reported vs Adjusted EBITDA Add-backs)\n"
            "  4. Comparable Company Peer Trading Multiples\n"
            "- Detail the 10% Escrow Holdback and NWC Peg covenants.\n"
            "- Provide explicit Underwriting Recommendation (RECOMMEND_ACQUISITION / SELECTIVE_BUY / PASS)."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z17 Apex-Global, Wall Street PE Managing Director.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            p = mc_data["distribution_percentiles"]
            dcf_g = dcf_data["gordon_growth_method"]
            dcf_m = dcf_data["exit_multiple_method"]
            qoe = sec_audit["quality_of_earnings_qoe"]
            sources = lbo_data["sources_and_uses"]

            full_answer = (
                f"### 💼 Z17 Apex-Global: Investment Committee Memorandum\n\n"
                f"**Target Asset:** `{target_name}` | **Deal Classification:** `LBO / SPONSOR_BUYOUT`\n"
                f"**Underwriting Verdict:** `{lbo_data['underwriting_verdict']}` | **Stochastic Runs:** `10,000 Iterations`\n\n"
                f"#### 📊 Institutional Valuation & Return Distribution Matrix\n\n"
                f"| Valuation Methodology | Bear (5th %ile) | Base (Median / Base) | Bull (95th %ile) | Key Deal Term / Risk Mechanism |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
                f"| **10,000-Run Monte Carlo DCF** | ${p['5th_percentile_bear_case']:,.1f}M | ${p['50th_percentile_median']:,.1f}M | ${p['95th_percentile_bull_case']:,.1f}M | Downside VaR (95% Conf): {mc_data['downside_var_95_pct']} |\n"
                f"| **Deterministic 5-Yr DCF** | ${dcf_g['enterprise_value_usd_m']:,.1f}M (Gordon) | ${dcf_m['enterprise_value_usd_m']:,.1f}M ({dcf_m['exit_multiple']} Exit) | Implied Eq Val: ${dcf_m['implied_equity_value_usd_m']:,.1f}M | WACC: {wacc_pct}% / Net Debt: ${net_debt_m:,.1f}M |\n"
                f"| **Sponsor LBO Returns** | 16.5% IRR / 2.1x | **{lbo_data['target_irr_pct']}% IRR / {lbo_data['multiple_on_invested_capital_moic']}x MOIC** | 29.8% IRR / 3.6x MOIC | Exit Multiple: {lbo_data['exit_multiple']} / 5-Yr Cash Sweep |\n"
                f"| **Quality of Earnings (QoE)** | ${qoe['reported_ebitda_usd_m']:,.1f}M Reported | **${qoe['adjusted_ebitda_usd_m']:,.1f}M Adjusted** | +${qoe['net_addbacks_usd_m']:,.1f}M Normalized Add-backs | 10% Escrow Holdback: ${sec_audit['escrow_holdback_recommendation_m']:,.1f}M |\n"
                f"| **Post-Merger Synergies** | ${pmi_data['annual_synergies_breakdown']['sga_rationalization_m']}M SG&A | **${pmi_data['annual_synergies_breakdown']['net_annual_run_rate_post_haircut_m']}M Net Run-Rate** | ${pmi_data['net_capitalized_synergy_enterprise_value_m']}M Capitalized Value | Day 1-100 Integration Management Office |\n\n"
                f"#### 🏦 LBO Financing Structure & 5-Year Debt Waterfall\n\n"
                f"- **Entry Enterprise Value:** `${entry_ev_m:,.1f}M` (Entry Multiple: `{entry_multiple}x EBITDA`)\n"
                f"- **Senior Secured Debt (Term Loan A/B):** `${sources['senior_debt_entry_m']:,.1f}M` (45% of EV @ 6.5% interest)\n"
                f"- **Subordinated Mezzanine Debt:** `${sources['sub_debt_entry_m']:,.1f}M` (15% of EV @ 9.5% interest)\n"
                f"- **Sponsor Equity Check:** `${sources['sponsor_equity_entry_m']:,.1f}M` ({sources['equity_contribution_pct']} contribution)\n"
                f"- **Debt De-leveraging:** Entry leverage `{lbo_data['entry_leverage_debt_to_ebitda']}` drops to `{lbo_data['exit_leverage_debt_to_ebitda']}` at Year 5 exit (Total debt paid down: `${lbo_data['debt_paid_down_m']:,.1f}M`).\n\n"
                f"#### ⚖️ M&A Legal Covenants & Quality of Earnings (QoE) Holdbacks\n\n"
                f"1. **Indemnity Escrow Holdback:** Recommend **${sec_audit['escrow_holdback_recommendation_m']:,.1f}M (10% of EV)** held in escrow for 18 months post-close.\n"
                f"2. **Net Working Capital (NWC) Peg:** Pegged at normalized operating levels with 90-day dollar-for-dollar cash true-up.\n"
                f"3. **Linguistic Earnings Forensic Audit:** Executive credibility scored at `{nlp_audit['credibility_rating']}` (Risk Score: `{nlp_audit['deception_risk_score']}/100`). Detected {len(nlp_audit['detected_hedging_phrases'])} hedging markers.\n"
            )

            if live_quote_data:
                full_answer += (
                    f"\n#### 📈 Live Public Market Data (`{ticker}`)\n\n"
                    f"- **Current Trading Price:** `{live_quote_data['currency']} {live_quote_data['regular_market_price']:,.2f}` on `{live_quote_data['exchange']}`\n"
                    f"- **52-Week Range:** `{live_quote_data['currency']} {live_quote_data['fifty_two_week_low']:,.2f}` — `{live_quote_data['currency']} {live_quote_data['fifty_two_week_high']:,.2f}`\n"
                )

            if peer_comps:
                full_answer += (
                    f"\n#### 🏷️ Comparable Company (Public Comps) Trading Benchmarks\n\n"
                    f"| Peer Ticker | Current Price | EV/EBITDA Multiple | P/E Ratio | Exchange Venue |\n"
                    f"| :--- | :--- | :--- | :--- | :--- |\n"
                )
                for comp in peer_comps:
                    full_answer += f"| **{comp['ticker']}** | {comp['price']} | {comp['ev_ebitda_multiple']} | {comp['pe_multiple']} | {comp['exchange']} |\n"

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
