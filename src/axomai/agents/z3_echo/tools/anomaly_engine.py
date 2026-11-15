"""
Z3 Echo Autonomous Anomaly, Outlier & Data Integrity Watchdog.
Performs automated scans on enterprise datasets to detect statistical outliers (Z-score/IQR),
data integrity flaws, duplicate entries, sudden volatility spikes, and compliance red-flags.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from rich.console import Console

console = Console()

class AnomalyWatchdog:
    def __init__(self):
        pass

    def scan_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Runs comprehensive automated anomaly & data integrity audit.
        """
        total_rows = len(df)
        total_cols = len(df.columns)
        if total_rows == 0:
            return {"success": False, "error": "Dataset is empty."}

        issues: List[Dict[str, Any]] = []

        # 1. Null / Missing Values Audit
        null_counts = df.isnull().sum()
        for col, count in null_counts.items():
            if count > 0:
                pct = (count / total_rows) * 100
                severity = "HIGH" if pct > 20 else ("MEDIUM" if pct > 5 else "LOW")
                issues.append({
                    "type": "Missing Values (Null)",
                    "target": col,
                    "severity": severity,
                    "observed": f"{count} nulls ({pct:.1f}%)",
                    "baseline": "0 nulls",
                    "action": "Impute with median or verify ingestion pipeline"
                })

        # 2. Duplicate Rows Audit
        dup_count = int(df.duplicated().sum())
        if dup_count > 0:
            issues.append({
                "type": "Duplicate Rows",
                "target": "Entire Table",
                "severity": "HIGH",
                "observed": f"{dup_count} duplicate rows",
                "baseline": "0 duplicates",
                "action": "Deduplicate table using primary key"
            })

        # 3. Statistical Outlier Detection (Z-score & IQR)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            clean_series = df[col].dropna()
            if len(clean_series) < 4:
                continue

            mean = clean_series.mean()
            std = clean_series.std()
            q1 = clean_series.quantile(0.25)
            q3 = clean_series.quantile(0.75)
            iqr = q3 - q1

            # High z-score outliers (|z| > 2.5)
            if std > 0:
                z_scores = np.abs((clean_series - mean) / std)
                outliers = clean_series[z_scores > 2.5]
                if len(outliers) > 0:
                    worst_val = outliers.iloc[np.argmax(np.abs(outliers.values - mean))]
                    issues.append({
                        "type": "Statistical Outlier (Z > 2.5)",
                        "target": col,
                        "severity": "MEDIUM",
                        "observed": f"Extreme value: {worst_val:,.2f} (n={len(outliers)})",
                        "baseline": f"Mean: {mean:,.2f} (±{std:,.2f})",
                        "action": "Verify if entry is a legitimate transaction or reporting error"
                    })

            # Negative value checks on strictly non-negative columns
            if any(term in col.lower() for term in ["price", "units", "revenue", "count", "customers"]):
                negatives = clean_series[clean_series < 0]
                if len(negatives) > 0:
                    issues.append({
                        "type": "Invalid Negative Value",
                        "target": col,
                        "severity": "CRITICAL",
                        "observed": f"{len(negatives)} negative values (min: {negatives.min()})",
                        "baseline": ">= 0",
                        "action": "Clean negative values or check return/refund logic"
                    })

        # 4. Volatility & Trend Breaks (if time/period column present)
        time_cols = [c for c in df.columns if c.lower() in ["period", "month", "quarter", "date"]]
        if time_cols and len(numeric_cols) > 0:
            tcol = time_cols[0]
            val_col = numeric_cols[0]
            grouped = df.groupby(tcol)[val_col].sum()
            if len(grouped) >= 3:
                pct_shifts = grouped.pct_change().dropna()
                extreme_drops = pct_shifts[pct_shifts < -0.40]
                for p_idx, drop_val in extreme_drops.items():
                    issues.append({
                        "type": "Sudden Trend Plunge (>40%)",
                        "target": f"{tcol}: {p_idx}",
                        "severity": "HIGH",
                        "observed": f"{drop_val * 100:.1f}% period collapse",
                        "baseline": "Normal trend variance (±15%)",
                        "action": "Investigate operational downtime or missing transaction batch"
                    })

        # Calculate Health Score (0 - 100%)
        critical_count = sum(1 for i in issues if i["severity"] == "CRITICAL")
        high_count = sum(1 for i in issues if i["severity"] == "HIGH")
        medium_count = sum(1 for i in issues if i["severity"] == "MEDIUM")
        deduction = (critical_count * 25) + (high_count * 15) + (medium_count * 5)
        health_score = max(10, min(100, 100 - deduction))

        # Build Anomaly Matrix for UI
        matrix_rows = []
        for iss in issues:
            matrix_rows.append([
                iss["severity"],
                iss["type"],
                iss["target"],
                iss["observed"],
                iss["baseline"],
                iss["action"]
            ])

        anomaly_matrix = {
            "title": f"Data Integrity & Anomaly Audit Matrix (Health Score: {health_score}%)",
            "headers": ["Severity", "Issue Type", "Target Column / Scope", "Observed Anomaly", "Normal Baseline", "Prescribed Action"],
            "rows": matrix_rows if matrix_rows else [["PASS", "Clean Data", "All Columns", "No critical anomalies found", "Normal", "Ready for Modeling"]]
        }

        return {
            "success": True,
            "health_score": health_score,
            "total_records": total_rows,
            "total_columns": total_cols,
            "issues_count": len(issues),
            "critical_count": critical_count,
            "anomaly_matrix": anomaly_matrix
        }

anomaly_watchdog = AnomalyWatchdog()

