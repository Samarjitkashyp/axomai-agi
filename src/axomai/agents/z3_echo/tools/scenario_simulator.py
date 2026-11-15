"""
Z3 Echo "What-If" Sensitivity & Scenario Modeling Engine.
Simulates parameter adjustments (pricing, marketing budget, COGS, volume elasticity)
and evaluates financial impact (Revenue, Margin, Net Profit) with comparison matrices and charts.
"""

import re
import json
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from rich.console import Console

from axomai.core.llm import llm_brain

console = Console()

class ScenarioSimulator:
    def __init__(self):
        pass

    def extract_simulation_parameters(self, query: str, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Uses LLM or rule-based regex to extract simulation parameters and percentage shifts.
        """
        defaults = {
            "price_delta_pct": 0.0,
            "marketing_delta_pct": 0.0,
            "cost_delta_pct": 0.0,
            "elasticity": -1.2,  # Default price elasticity of demand
            "description": "Simulated Adjustment"
        }

        if llm_brain.is_available:
            try:
                sys_prompt = (
                    "You are a Senior Financial Modeling Analyst. Extract simulation parameter changes from the user prompt.\n"
                    "Output JSON only with keys:\n"
                    "{\n"
                    '  "price_delta_pct": float (e.g. -5.0 for 5% drop, 10.0 for 10% hike),\n'
                    '  "marketing_delta_pct": float (e.g. 15.0 for 15% increase),\n'
                    '  "cost_delta_pct": float (e.g. -2.0 for 2% savings),\n'
                    '  "volume_delta_pct": float or null,\n'
                    '  "description": "Short description of scenario"\n'
                    "}"
                )
                raw = llm_brain.generate(sys_prompt, f"User Query: {query}", temperature=0.0)
                clean = raw.strip()
                if "```json" in clean:
                    clean = clean.split("```json")[1].split("```")[0].strip()
                elif "```" in clean:
                    clean = clean.split("```")[1].split("```")[0].strip()
                parsed = json.loads(clean)
                for k in ["price_delta_pct", "marketing_delta_pct", "cost_delta_pct", "volume_delta_pct"]:
                    if k in parsed and parsed[k] is not None:
                        defaults[k] = float(parsed[k])
                if parsed.get("description"):
                    defaults["description"] = parsed["description"]
                return defaults
            except Exception as e:
                console.print(f"[dim yellow][Z3 Scenario LLM Param Skip][/dim yellow] {e}")

        # Regex fallback
        q = query.lower()
        m_mkt = re.search(r'(?:marketing|ad|spend|cost)\s*(?:by|of)?\s*([+-]?\d+)\s*%', q)
        if m_mkt:
            defaults["marketing_delta_pct"] = float(m_mkt.group(1))

        m_price = re.search(r'(?:price|pricing|rate)\s*(?:by|of)?\s*([+-]?\d+)\s*%', q)
        if m_price:
            defaults["price_delta_pct"] = float(m_price.group(1))

        return defaults

    def simulate(self, query: str, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Executes a complete financial What-If simulation comparing Base Case vs Scenario.
        """
        params = self.extract_simulation_parameters(query, df)

        # 1. Calculate Base Metrics
        total_rev = float(df["revenue"].sum()) if "revenue" in df.columns else float(df.select_dtypes(include=[np.number]).iloc[:, 0].sum())
        total_mkt = float(df["marketing_cost"].sum()) if "marketing_cost" in df.columns else float(total_rev * 0.18)
        total_cogs = float(df["cogs"].sum()) if "cogs" in df.columns else float(total_rev * 0.40)
        total_profit = float(df["profit"].sum()) if "profit" in df.columns else float(total_rev - total_cogs - total_mkt)

        price_shift = params["price_delta_pct"] / 100.0
        mkt_shift = params["marketing_delta_pct"] / 100.0
        cost_shift = params.get("cost_delta_pct", 0.0) / 100.0

        # Demand elasticity: price reduction boosts volume, price hike lowers volume
        elasticity = params.get("elasticity", -1.2)
        if params.get("volume_delta_pct") is not None:
            volume_shift = params["volume_delta_pct"] / 100.0
        else:
            # Volume change from price elasticity + marketing boost (e.g., 0.25 elasticity on ad spend)
            mkt_volume_boost = (mkt_shift * 0.25) if mkt_shift > 0 else (mkt_shift * 0.15)
            price_volume_boost = price_shift * elasticity
            volume_shift = price_volume_boost + mkt_volume_boost

        # 2. Compute Simulated Case
        sim_volume_factor = 1.0 + volume_shift
        sim_price_factor = 1.0 + price_shift
        sim_rev = total_rev * sim_volume_factor * sim_price_factor
        sim_cogs = total_cogs * sim_volume_factor * (1.0 + cost_shift)
        sim_mkt = total_mkt * (1.0 + mkt_shift)
        sim_profit = sim_rev - sim_cogs - sim_mkt

        # 3. Calculate Deltas
        rev_delta = sim_rev - total_rev
        rev_pct = (rev_delta / total_rev * 100) if total_rev != 0 else 0.0

        cogs_delta = sim_cogs - total_cogs
        cogs_pct = (cogs_delta / total_cogs * 100) if total_cogs != 0 else 0.0

        mkt_delta = sim_mkt - total_mkt
        mkt_pct = (mkt_delta / total_mkt * 100) if total_mkt != 0 else 0.0

        profit_delta = sim_profit - total_profit
        profit_pct = (profit_delta / total_profit * 100) if total_profit != 0 else 0.0

        base_margin = (total_profit / total_rev * 100) if total_rev != 0 else 0.0
        sim_margin = (sim_profit / sim_rev * 100) if sim_rev != 0 else 0.0
        margin_delta = sim_margin - base_margin

        # 4. Format Matrix
        matrix = {
            "title": f"Scenario Simulation Matrix: {params.get('description', 'Parameter Adjustment')}",
            "headers": ["Metric", "Base Case", "Simulated Scenario", "Absolute Variance", "% Impact"],
            "rows": [
                ["Gross Revenue", f"{total_rev:,.2f}", f"{sim_rev:,.2f}", f"{rev_delta:+,.2f}", f"{rev_pct:+.1f}%"],
                ["Cost of Goods (COGS)", f"{total_cogs:,.2f}", f"{sim_cogs:,.2f}", f"{cogs_delta:+,.2f}", f"{cogs_pct:+.1f}%"],
                ["Marketing & Ad Spend", f"{total_mkt:,.2f}", f"{sim_mkt:,.2f}", f"{mkt_delta:+,.2f}", f"{mkt_pct:+.1f}%"],
                ["Net Profit", f"{total_profit:,.2f}", f"{sim_profit:,.2f}", f"{profit_delta:+,.2f}", f"{profit_pct:+.1f}%"],
                ["Net Profit Margin", f"{base_margin:.1f}%", f"{sim_margin:.1f}%", f"{margin_delta:+.1f}% pts", "—"]
            ],
            "raw_metrics": {
                "base_revenue": round(total_rev, 2),
                "base_cogs": round(total_cogs, 2),
                "base_marketing": round(total_mkt, 2),
                "base_profit": round(total_profit, 2),
                "elasticity": elasticity,
                "price_delta_pct": params["price_delta_pct"],
                "marketing_delta_pct": params["marketing_delta_pct"]
            }
        }

        # 5. Interactive Chart.js Bar Chart
        chart_config = {
            "type": "bar",
            "title": "Scenario Comparison: Base Case vs Simulated Case",
            "labels": ["Gross Revenue", "COGS", "Marketing", "Net Profit"],
            "datasets": [
                {
                    "label": "Base Case (Actual)",
                    "data": [round(total_rev, 2), round(total_cogs, 2), round(total_mkt, 2), round(total_profit, 2)],
                    "backgroundColor": "rgba(6, 182, 212, 0.7)",  # Cyan
                    "borderColor": "rgb(6, 182, 212)",
                    "borderWidth": 1.5
                },
                {
                    "label": "Simulated Scenario",
                    "data": [round(sim_rev, 2), round(sim_cogs, 2), round(sim_mkt, 2), round(sim_profit, 2)],
                    "backgroundColor": "rgba(16, 185, 129, 0.7)" if profit_delta >= 0 else "rgba(239, 68, 68, 0.7)",  # Emerald or Red
                    "borderColor": "rgb(16, 185, 129)" if profit_delta >= 0 else "rgb(239, 68, 68)",
                    "borderWidth": 1.5
                }
            ]
        }

        return {
            "success": True,
            "parameters": params,
            "matrix": matrix,
            "chart": chart_config,
            "summary": {
                "base_profit": round(total_profit, 2),
                "simulated_profit": round(sim_profit, 2),
                "profit_delta": round(profit_delta, 2),
                "profit_pct": round(profit_pct, 1),
                "base_margin": round(base_margin, 1),
                "simulated_margin": round(sim_margin, 1),
                "is_positive": profit_delta >= 0
            }
        }

scenario_simulator = ScenarioSimulator()
