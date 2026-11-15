"""
Z3 Echo Analytics Router.
Classifies inquiries across Text-to-SQL, Auto-Joins, Predictive Forecasting,
Root-Cause Diagnostics, What-If Simulation, Anomaly Watchdog, and Executive PDF Export.
"""

import re
from enum import Enum
from typing import Dict, Any, List

class AnalyticsTaskType(str, Enum):
    TEXT_TO_SQL = "TEXT_TO_SQL"
    MULTI_TABLE_JOIN = "MULTI_TABLE_JOIN"
    PREDICTIVE_FORECAST = "PREDICTIVE_FORECAST"
    ROOT_CAUSE_ANALYSIS = "ROOT_CAUSE_ANALYSIS"
    WHAT_IF_SIMULATION = "WHAT_IF_SIMULATION"
    ANOMALY_AUDIT = "ANOMALY_AUDIT"
    ANALYTICS_EXPORT = "ANALYTICS_EXPORT"

class AnalyticsRouter:
    def route_query(self, query: str) -> Dict[str, Any]:
        q = query.lower().strip()

        # 1. Executive Analytics Dossier Export
        if any(w in q for w in ["pdf", "dossier", "export report", "download report", "board deck", "briefing pdf", "analytics dossier", "pdf bana"]):
            return {
                "task_type": AnalyticsTaskType.ANALYTICS_EXPORT,
                "confidence": 0.98
            }

        # 2. Root-Cause Diagnostic Analysis ("Why did it happen?")
        if any(w in q for w in [
            "why did", "kyu gira", "kyu badha", "root cause", "karan kya tha",
            "reason behind", "drop kyu", "spike kyu", "driver attribution",
            "variance explanation", "what caused", "why profit fell", "why sales dropped"
        ]):
            return {
                "task_type": AnalyticsTaskType.ROOT_CAUSE_ANALYSIS,
                "confidence": 0.96
            }

        # 3. Anomaly & Outlier Watchdog Audit
        if any(w in q for w in [
            "anomaly", "outlier", "audit data", "data integrity", "red flag",
            "health score", "duplicate rows", "missing values", "cleanliness", "data quality"
        ]):
            return {
                "task_type": AnalyticsTaskType.ANOMALY_AUDIT,
                "confidence": 0.95
            }

        # 4. What-If Simulation
        if any(w in q for w in [
            "what if", "what-if", "agar hum", "agar mai", "simulate", "simulation",
            "badha de", "kam kare", "ghata de", "sensitivity", "price change",
            "margin impact", "profit par kya", "marketing badha", "price kam"
        ]):
            return {
                "task_type": AnalyticsTaskType.WHAT_IF_SIMULATION,
                "confidence": 0.95
            }

        # 5. Predictive Forecasting
        if any(w in q for w in [
            "forecast", "predict", "prediction", "projection", "projected", "future",
            "next 3 months", "next quarter", "next year", "trajectory", "trend line",
            "aage ka", "bhavishya", "outlook", "estimate next", "seasonality"
        ]):
            periods = 3
            m_periods = re.search(r'next\s*(\d+)\s*(?:month|quarter|period|year)', q)
            if m_periods:
                periods = max(1, min(12, int(m_periods.group(1))))
            return {
                "task_type": AnalyticsTaskType.PREDICTIVE_FORECAST,
                "periods_ahead": periods,
                "confidence": 0.95
            }

        # 6. Multi-Table Auto-Join
        if any(w in q for w in ["join", "customers and orders", "customer spend", "orders by customer", "vip customers", "cross table", "relational"]):
            return {
                "task_type": AnalyticsTaskType.MULTI_TABLE_JOIN,
                "confidence": 0.92
            }

        # 7. Standard Text-to-SQL
        return {
            "task_type": AnalyticsTaskType.TEXT_TO_SQL,
            "confidence": 0.90
        }

analytics_router = AnalyticsRouter()
