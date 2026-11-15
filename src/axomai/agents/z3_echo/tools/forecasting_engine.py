"""
Z3 Echo Time-Series Predictive Analytics & Trend Forecasting Engine.
Fits statistical linear regression, moving averages, and trajectory extrapolation
to project future revenue, sales, and demand with Chart.js configurations.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from rich.console import Console

console = Console()

class ForecastingEngine:
    def __init__(self):
        pass

    def identify_series_columns(self, df: pd.DataFrame) -> Tuple[Optional[str], Optional[str]]:
        """
        Identifies the best time column and primary numeric metric column in a DataFrame.
        """
        time_candidates = ["period", "month", "date", "quarter", "year", "time", "day", "timestamp"]
        metric_candidates = ["revenue", "profit", "sales", "units", "amount", "value", "mrr", "arr", "new_customers"]

        time_col = None
        for col in df.columns:
            if any(cand in col.lower() for cand in time_candidates):
                time_col = col
                break
        if not time_col:
            # Fallback to first object/string column or index
            for col in df.columns:
                if df[col].dtype == object or "str" in str(df[col].dtype):
                    time_col = col
                    break

        metric_col = None
        for col in df.columns:
            if any(cand in col.lower() for cand in metric_candidates) and pd.api.types.is_numeric_dtype(df[col]):
                metric_col = col
                break
        if not metric_col:
            # Fallback to first numeric column
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    metric_col = col
                    break

        return time_col, metric_col

    def generate_forecast(
        self,
        df: pd.DataFrame,
        target_metric: Optional[str] = None,
        time_col: Optional[str] = None,
        periods_ahead: int = 3
    ) -> Dict[str, Any]:
        """
        Computes historical trend and projects future trajectory for `periods_ahead`.
        """
        detected_time, detected_metric = self.identify_series_columns(df)
        time_col = time_col or detected_time
        target_metric = target_metric or detected_metric

        if not target_metric or target_metric not in df.columns:
            return {
                "success": False,
                "error": f"No valid numeric column found to forecast among columns: {list(df.columns)}"
            }

        # Prepare historical series
        clean_df = df.dropna(subset=[target_metric]).copy()
        if clean_df.empty:
            return {"success": False, "error": "Dataset has no non-null values for metric."}

        y_vals = clean_df[target_metric].astype(float).values
        n = len(y_vals)
        if n < 2:
            return {"success": False, "error": "Need at least 2 historical data points for projection."}

        x_vals = np.arange(n)

        # 1. Fit Linear Regression: y = slope * x + intercept
        slope, intercept = np.polyfit(x_vals, y_vals, 1)
        fitted_y = slope * x_vals + intercept

        # Calculate R-squared (goodness of fit)
        ss_res = np.sum((y_vals - fitted_y) ** 2)
        ss_tot = np.sum((y_vals - np.mean(y_vals)) ** 2)
        r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0
        r_squared = max(0.0, min(1.0, float(r_squared)))

        # Historical labels
        if time_col and time_col in clean_df.columns:
            hist_labels = [str(x) for x in clean_df[time_col].values]
        else:
            hist_labels = [f"T{i+1}" for i in range(n)]

        # 2. Extrapolate future values with Seasonality & Cyclicality Detection
        future_x = np.arange(n, n + periods_ahead)
        future_y = slope * future_x + intercept

        # Seasonality Detection
        cycle_len = 4 if n >= 8 else (3 if n >= 6 else None)
        seasonal_factors = np.ones(periods_ahead)
        seasonality_detected = False
        seasonality_note = "Linear baseline trajectory"

        if cycle_len and np.all(fitted_y > 0):
            ratios = y_vals / fitted_y
            cycle_indices = [float(np.mean([ratios[i] for i in range(j, n, cycle_len)])) for j in range(cycle_len)]
            mean_idx = float(np.mean(cycle_indices))
            if mean_idx > 0:
                cycle_indices = [ci / mean_idx for ci in cycle_indices]
            
            if np.std(cycle_indices) > 0.04:
                seasonality_detected = True
                seasonality_note = f"Seasonality cycle detected ({cycle_len}-period cyclical wave)"
                for step in range(periods_ahead):
                    idx_in_cycle = (n + step) % cycle_len
                    seasonal_factors[step] = cycle_indices[idx_in_cycle]
                future_y = future_y * seasonal_factors

        # Prevent negative values if metric is strictly non-negative
        if np.all(y_vals >= 0):
            future_y = np.maximum(future_y, 0)

        # Generate future labels
        future_labels = []
        last_label = hist_labels[-1]
        for step in range(1, periods_ahead + 1):
            future_labels.append(f"{last_label}+M{step} (F)")

        # 3. Growth Metrics
        first_val = float(y_vals[0])
        last_val = float(y_vals[-1])
        projected_final = float(future_y[-1])

        growth_rate_percent = ((last_val - first_val) / abs(first_val) * 100) if first_val != 0 else 0.0
        projected_gain_percent = ((projected_final - last_val) / abs(last_val) * 100) if last_val != 0 else 0.0

        # 4. Build Interactive Chart.js Configuration
        # Full x-axis combines historical and forecasted periods
        all_labels = hist_labels + future_labels

        # Dataset 1: Historical Actuals (null for future slots)
        hist_series = [round(float(v), 2) for v in y_vals] + [None] * periods_ahead

        # Dataset 2: Forecast Line (bridges from last historical point)
        forecast_series = [None] * (n - 1) + [round(float(last_val), 2)] + [round(float(v), 2) for v in future_y]

        # Dataset 3: Upper & Lower Confidence Corridor (±8% variance)
        corridor_upper = [None] * (n - 1) + [round(float(last_val), 2)] + [round(float(v * 1.08), 2) for v in future_y]
        corridor_lower = [None] * (n - 1) + [round(float(last_val), 2)] + [round(float(v * 0.92), 2) for v in future_y]

        chart_config = {
            "type": "line",
            "title": f"Predictive Trajectory: {target_metric.replace('_', ' ').title()} (Next {periods_ahead} Periods)",
            "labels": all_labels,
            "datasets": [
                {
                    "label": f"Historical Actuals ({target_metric})",
                    "data": hist_series,
                    "borderColor": "rgb(6, 182, 212)",  # Cyan
                    "backgroundColor": "rgba(6, 182, 212, 0.15)",
                    "borderWidth": 2.5,
                    "pointRadius": 4,
                    "pointBackgroundColor": "rgb(6, 182, 212)",
                    "fill": False,
                    "tension": 0.2
                },
                {
                    "label": f"Predictive Forecast (Next {periods_ahead} Periods)",
                    "data": forecast_series,
                    "borderColor": "rgb(139, 92, 246)",  # Violet
                    "backgroundColor": "rgba(139, 92, 246, 0.15)",
                    "borderWidth": 2.5,
                    "borderDash": [6, 4],
                    "pointRadius": 5,
                    "pointBackgroundColor": "rgb(139, 92, 246)",
                    "fill": False,
                    "tension": 0.2
                },
                {
                    "label": "Confidence Upper (+8%)",
                    "data": corridor_upper,
                    "borderColor": "rgba(16, 185, 129, 0.4)",  # Emerald
                    "borderWidth": 1,
                    "borderDash": [2, 2],
                    "pointRadius": 0,
                    "fill": False
                },
                {
                    "label": "Confidence Lower (-8%)",
                    "data": corridor_lower,
                    "borderColor": "rgba(239, 68, 68, 0.4)",  # Rose
                    "borderWidth": 1,
                    "borderDash": [2, 2],
                    "pointRadius": 0,
                    "fill": False
                }
            ]
        }

        # Tabular breakdown
        projection_table = []
        for flabel, fval in zip(future_labels, future_y):
            projection_table.append({
                "period": flabel,
                "projected_value": round(float(fval), 2),
                "lower_bound": round(float(fval * 0.92), 2),
                "upper_bound": round(float(fval * 1.08), 2)
            })

        return {
            "success": True,
            "target_metric": target_metric,
            "time_column": time_col,
            "historical_count": n,
            "periods_ahead": periods_ahead,
            "slope": round(float(slope), 4),
            "r_squared": round(r_squared, 3),
            "historical_last": round(last_val, 2),
            "projected_end": round(projected_final, 2),
            "historical_growth_pct": round(growth_rate_percent, 1),
            "projected_growth_pct": round(projected_gain_percent, 1),
            "seasonality_detected": seasonality_detected,
            "seasonality_note": seasonality_note,
            "projection_table": projection_table,
            "chart": chart_config
        }

forecasting_engine = ForecastingEngine()

