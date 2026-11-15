"""
Z13 Quantum - Competitive Market Surveillance & Dynamic Pricing Agent.
Monitors commodity auction rates, competitor pricing tactics, and computes
profit-maximizing pricing elasticity models.
"""

import re
from typing import Dict, Any, Generator, Optional, List

from axomai.core.llm import llm_brain
from axomai.agents.z13_quantum.tools.mandi_tracker import mandi_tracker
from axomai.agents.z13_quantum.tools.price_elasticity_engine import price_elasticity_engine

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

class Z13QuantumAgent:
    """Enterprise Chief Commercial Officer & Market Pricing Surveillance Specialist."""

    def __init__(self):
        self.name = "Z13 Quantum"
        self.role = "Competitive Market Surveillance & Dynamic Pricing Agent"

    def market_surveillance_stream(
        self,
        query: str,
        session_id: Optional[str] = "quantum_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield {
            "type": "status",
            "stage": "price_surveillance",
            "message": "📈 Z13 Quantum: Scanning GTAC auction rates, wholesale mandis & elasticity curves..."
        }

        benchmarks = mandi_tracker.get_benchmarks(query)

        # Compute sample pricing strategies for 2 core regional product lines
        tea_strategy = price_elasticity_engine.compute_pricing_strategy(
            "Assam CTC Tea (1kg Pack)", procurement_cost_inr=215.0, competitor_price_inr=295.0, elasticity_type="moderate"
        )
        rice_strategy = price_elasticity_engine.compute_pricing_strategy(
            "Joha Rice Premium (5kg)", procurement_cost_inr=390.0, competitor_price_inr=560.0, elasticity_type="staples"
        )

        strategies = [tea_strategy, rice_strategy]

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "MARKET_SURVEILLANCE_AND_DYNAMIC_PRICING",
            "benchmarks_monitored": len(benchmarks),
            "primary_market": "Guwahati Tea Auction Centre & Regional Mandis",
            "strategies": strategies,
            "tools_used": ["mandi_tracker", "price_elasticity_engine"]
        }
        yield meta_event

        prompt = (
            f"You are Z13 Quantum, Chief Commercial Officer & Market Surveillance Strategist.\n"
            f"User Goal / Inquiry: '{query}'\n\n"
            f"Regional Wholesale & GTAC Benchmarks:\n{str(benchmarks)}\n\n"
            f"Dynamic Pricing Elasticity Models:\n{str(strategies)}\n\n"
            "Formulate an authoritative, boardroom-ready Market Surveillance & Pricing Strategy Dossier in clean GitHub Markdown.\n\n"
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "- Always place a blank line (\\n\\n) before every heading (##, ###).\n"
            "- Present Commodity Price Benchmarks as a clean GitHub Markdown Table with blank lines before and after:\n"
            "| Commodity | Wholesale Market | Auction Rate (₹) | Retail MRP Range (₹) | Target Margin % | Trend Outlook |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
            "- Present Dynamic Pricing Strategies in a structured table or bold bullets with clear competitor defense tactics.\n"
            "- Ensure every table row ends with a newline."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z13 Quantum, Commercial Pricing Officer.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = (
                f"### 📈 Z13 Quantum: Market Surveillance & Dynamic Pricing Dossier\n\n"
                f"**Primary Benchmark Index:** `Guwahati Tea Auction Centre (GTAC) & Regional Wholesale Mandis`\n\n"
                f"#### 📊 Wholesale Mandi & Auction Benchmark Matrix\n\n"
                f"| Commodity | Wholesale Market | Auction Rate (₹) | Retail MRP Range (₹) | Target Margin % | Trend Outlook |\n"
                f"| :--- | :--- | :--- | :--- | :--- | :--- |\n"
            )
            for b in benchmarks:
                full_answer += (
                    f"| **{b['commodity']}** | {b['market']} | ₹{b['wholesale_price_inr']:.2f} {b['unit']} | "
                    f"{b['retail_mrp_range_inr']} | {b['retail_margin_pct']}% | {b['trend']} |\n"
                )
            full_answer += (
                f"\n#### 🎯 Dynamic Pricing Recommendations & Margin Defense:\n\n"
                f"1. **Assam CTC Tea (1kg Pack):** Optimal retail price **₹{tea_strategy['optimal_retail_price_inr']:.2f}** (Margin: `{tea_strategy['gross_margin_pct']}%`). *Recommendation:* {tea_strategy['strategic_recommendation']}\n"
                f"2. **Indigenous Joha Rice (5kg Bag):** Optimal retail price **₹{rice_strategy['optimal_retail_price_inr']:.2f}** (Margin: `{rice_strategy['gross_margin_pct']}%`). *Recommendation:* {rice_strategy['strategic_recommendation']}\n\n"
                f"#### 🛡️ Anti-Predatory Counter Strategy:\n"
                f"- If quick-commerce players discount staples below cost, counter by highlighting **GI-Tagged Authentic Regional Origin** and direct farmer procurement stamps on store shelves.\n"
            )
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": normalize_markdown(full_answer)}

z13_quantum_agent = Z13QuantumAgent()

