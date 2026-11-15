"""
Z3 Echo Diagnostic AI & Root-Cause Variance Decomposition Engine.
Analyzes why key business metrics (profit, revenue, margin) dropped or surged between periods.
Performs multi-dimensional attribution across dimensions (regions, products, cost drivers).
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from rich.console import Console

from axomai.core.llm import llm_brain

console = Console()

class RootCauseEngine:
    def __init__(self):
        pass

    def identify_dimensions(self, df: pd.DataFrame) -> List[str]:
        """Finds categorical dimensions (e.g. region, category, product, month)."""
        dims = []
        for col in df.columns:
            if df[col].dtype == object or "str" in str(df[col].dtype) or col.lower() in ["region", "category", "product", "channel", "month", "quarter"]:
                if df[col].nunique() <= 30:  # Sensible cardinality
                    dims.append(col)
        return dims

    def analyze_root_cause(
        self,
        query: str,
        df: pd.DataFrame,
        metric: Optional[str] = "profit"
    ) -> Dict[str, Any]:
        """
        Executes multi-dimensional variance decomposition.
        Identifies exact contributors to positive or negative variance.
        """
        # Determine metric to analyze
        q_lower = query.lower()
        if "revenue" in q_lower or "sales" in q_lower:
            target_metric = "revenue" if "revenue" in df.columns else "sales"
        elif "margin" in q_lower:
            target_metric = "profit"
        elif "unit" in q_lower or "volume" in q_lower:
            target_metric = "units" if "units" in df.columns else "profit"
        else:
            target_metric = "profit" if "profit" in df.columns else "revenue"

        if target_metric not in df.columns:
            # Fallback to first numeric column
            num_cols = df.select_dtypes(include=[np.number]).columns
            if len(num_cols) > 0:
                target_metric = num_cols[0]
            else:
                return {"success": False, "error": "No numeric metric found for root cause analysis."}

        # Determine time/period column
        time_cols = [c for c in df.columns if c.lower() in ["period", "month", "quarter", "date", "year"]]
        time_col = time_cols[0] if time_cols else None

        # Compare latest period vs previous period (or second half vs first half)
        if time_col and df[time_col].nunique() >= 2:
            unique_periods = list(df[time_col].unique())
            period_b = unique_periods[-1]  # Current
            period_a = unique_periods[-2]  # Baseline
            df_a = df[df[time_col] == period_a]
            df_b = df[df[time_col] == period_b]
            period_label = f"{period_b} vs {period_a}"
        else:
            # Split dataset into half
            mid = len(df) // 2
            df_a = df.iloc[:mid]
            df_b = df.iloc[mid:]
            period_label = "Recent Period vs Prior Period"

        base_val = float(df_a[target_metric].sum())
        curr_val = float(df_b[target_metric].sum())
        total_delta = curr_val - base_val
        total_pct = (total_delta / abs(base_val) * 100) if base_val != 0 else 0.0

        # Multi-dimensional attribution breakdown
        dimensions = self.identify_dimensions(df)
        driver_breakdowns: List[Dict[str, Any]] = []

        for dim in dimensions:
            if dim == time_col:
                continue
            grouped_a = df_a.groupby(dim)[target_metric].sum()
            grouped_b = df_b.groupby(dim)[target_metric].sum()
            all_keys = set(grouped_a.index).union(set(grouped_b.index))

            dim_drivers = []
            for k in all_keys:
                val_a = float(grouped_a.get(k, 0.0))
                val_b = float(grouped_b.get(k, 0.0))
                delta = val_b - val_a
                share_of_delta = (delta / abs(total_delta) * 100) if total_delta != 0 else 0.0
                dim_drivers.append({
                    "entity": str(k),
                    "dimension": dim,
                    "baseline": round(val_a, 2),
                    "current": round(val_b, 2),
                    "delta": round(delta, 2),
                    "share_of_delta_pct": round(share_of_delta, 1)
                })

            # Sort by absolute impact
            dim_drivers.sort(key=lambda x: abs(x["delta"]), reverse=True)
            if dim_drivers:
                driver_breakdowns.append({
                    "dimension": dim,
                    "top_drivers": dim_drivers
                })

        # Find primary drivers across all categories
        all_drivers = []
        for group in driver_breakdowns:
            for item in group["top_drivers"]:
                all_drivers.append(item)
        all_drivers.sort(key=lambda x: abs(x["delta"]), reverse=True)

        primary_negative = [d for d in all_drivers if d["delta"] < 0][:3]
        primary_positive = [d for d in all_drivers if d["delta"] > 0][:3]

        # Cost driver analysis (if cogs and marketing_cost exist)
        cost_impacts = {}
        for cost_col in ["cogs", "marketing_cost"]:
            if cost_col in df.columns:
                c_a = float(df_a[cost_col].sum())
                c_b = float(df_b[cost_col].sum())
                c_delta = c_b - c_a
                cost_impacts[cost_col] = {
                    "base": round(c_a, 2),
                    "current": round(c_b, 2),
                    "delta": round(c_delta, 2),
                    "impact_on_profit": round(-c_delta, 2)  # Higher cost decreases profit
                }

        # Build Waterfall / Variance Attribution Chart
        chart_labels = ["Baseline Value"]
        chart_data = [round(base_val, 2)]
        chart_colors = ["rgba(6, 182, 212, 0.7)"]  # Cyan

        for d in all_drivers[:4]:
            chart_labels.append(f"{d['entity']} ({d['dimension']})")
            chart_data.append(round(d["delta"], 2))
            chart_colors.append("rgba(16, 185, 129, 0.7)" if d["delta"] >= 0 else "rgba(239, 68, 68, 0.7)")

        chart_labels.append("Final Net Value")
        chart_data.append(round(curr_val, 2))
        chart_colors.append("rgba(139, 92, 246, 0.7)")  # Violet

        attribution_chart = {
            "type": "bar",
            "title": f"Root-Cause Attribution Waterfall: {target_metric.title()} ({period_label})",
            "labels": chart_labels,
            "datasets": [
                {
                    "label": "Variance Contribution",
                    "data": chart_data,
                    "backgroundColor": chart_colors,
                    "borderColor": [c.replace("0.7", "1.0") for c in chart_colors],
                    "borderWidth": 1.5
                }
            ]
        }

        # Build Diagnostic Matrix
        matrix_rows = []
        for d in all_drivers[:6]:
            matrix_rows.append([
                d["dimension"].title(),
                d["entity"],
                f"{d['baseline']:,}",
                f"{d['current']:,}",
                f"{d['delta']:+,}",
                f"{d['share_of_delta_pct']:+.1f}%"
            ])

        diagnostic_matrix = {
            "title": f"Driver Attribution Matrix: {target_metric.title()} Variance ({total_delta:+,.2f} / {total_pct:+.1f}%)",
            "headers": ["Dimension", "Driver / Segment", "Baseline", "Current", "Variance Impact", "% of Total Shift"],
            "rows": matrix_rows
        }

        return {
            "success": True,
            "metric": target_metric,
            "period_label": period_label,
            "baseline_value": round(base_val, 2),
            "current_value": round(curr_val, 2),
            "total_variance": round(total_delta, 2),
            "total_variance_pct": round(total_pct, 1),
            "primary_negative": primary_negative,
            "primary_positive": primary_positive,
            "cost_impacts": cost_impacts,
            "diagnostic_matrix": diagnostic_matrix,
            "chart": attribution_chart
        }

root_cause_engine = RootCauseEngine()

