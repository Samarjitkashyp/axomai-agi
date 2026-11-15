"""
Z3 Echo - Advanced Enterprise Database & Predictive Analytics Agent.
Orchestrates:
1. Multi-Table Auto-Joins (customers, products, orders)
2. Diagnostic Root-Cause Variance Decomposition
3. Seasonality-Aware Time-Series Forecasting
4. Autonomous Anomaly, Outlier & Integrity Watchdog
5. Live Database / Relational Connector
6. Publication-Grade Executive Analytics Dossier (PDF Export)
"""

import os
import uuid
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Generator, Tuple
from datetime import datetime

import pandas as pd
import numpy as np
from rich.console import Console

from axomai.db.session import SyncSessionLocal
from axomai.db.models import Document, AgentSession, AgentTaskLog
from axomai.core.llm import llm_brain
from axomai.agents.z3_echo.router import analytics_router, AnalyticsTaskType
from axomai.agents.z3_echo.tools.sql_engine import sql_engine, generate_default_enterprise_dataset
from axomai.agents.z3_echo.tools.forecasting_engine import forecasting_engine
from axomai.agents.z3_echo.tools.scenario_simulator import scenario_simulator
from axomai.agents.z3_echo.tools.root_cause_engine import root_cause_engine
from axomai.agents.z3_echo.tools.anomaly_engine import anomaly_watchdog
from axomai.agents.z3_echo.tools.db_connector import db_connector
from axomai.agents.z3_echo.tools.report_exporter import report_exporter

console = Console()

class Z3EchoAgent:
    def __init__(self):
        self.name = "Z3 Echo"
        self.role = "Enterprise Database & Predictive Analytics Agent"
        self.router = analytics_router

    def _resolve_dataset(self, query: str, doc_id: Optional[str]) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame], str]:
        """
        Loads DataFrame and relational multi-tables dictionary.
        """
        q_lower = query.lower()
        is_relational_intent = any(w in q_lower for w in ["customer", "order", "product", "join", "tier", "spent", "vip"])

        if is_relational_intent:
            rel_tables = db_connector.get_relational_tables()
            primary_df = rel_tables.get("orders", generate_default_enterprise_dataset())
            return primary_df, rel_tables, "Enterprise Relational Database (Orders, Customers, Products)"

        if doc_id and doc_id != "database_analytics":
            try:
                doc_uuid = uuid.UUID(doc_id)
                with SyncSessionLocal() as db:
                    doc = db.query(Document).filter(Document.id == doc_uuid).first()
                    if doc and doc.file_path and Path(doc.file_path).exists():
                        fp = Path(doc.file_path)
                        if fp.suffix.lower() in [".xlsx", ".xls"]:
                            xl = pd.ExcelFile(fp)
                            tables = {sname.lower().replace(" ", "_"): xl.parse(sname) for sname in xl.sheet_names}
                            primary_df = list(tables.values())[0]
                            return primary_df, tables, f"Uploaded Workbook: {doc.filename} ({len(tables)} sheets)"
                        elif fp.suffix.lower() in [".csv", ".tsv"]:
                            df = pd.read_csv(fp)
                            return df, {"analytics_data": df}, f"Uploaded CSV: {doc.filename}"
                    elif doc and doc.udm_data:
                        tables = doc.udm_data.get("tables", [])
                        if tables and tables[0].get("headers") and tables[0].get("rows"):
                            t = tables[0]
                            df = pd.DataFrame(t["rows"], columns=t["headers"])
                            return df, {"analytics_data": df}, f"Extracted Table: {doc.filename}"
            except Exception as e:
                console.print(f"[dim yellow][Z3 Doc Resolve Skip][/dim yellow] {e}")

        # Default enterprise performance dataset + relational tables
        default_df = generate_default_enterprise_dataset()
        rel_tables = db_connector.get_relational_tables()
        rel_tables["analytics_data"] = default_df
        return default_df, rel_tables, "Enterprise Sales & Financial Dataset (2025-2026)"

    def analytics(
        self,
        query: str,
        session_id: Optional[str] = None,
        doc_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Synchronous analytics pipeline."""
        gen = self.analytics_stream(query, session_id=session_id, doc_id=doc_id)
        meta_data = {}
        full_answer = ""
        for event in gen:
            if event.get("type") == "meta":
                meta_data = event
            elif event.get("type") == "token":
                full_answer += event.get("content", "")
            elif event.get("type") == "done":
                full_answer = event.get("answer", full_answer)

        return {
            "agent": self.name,
            "query": query,
            "task_type": meta_data.get("task_type"),
            "dataset_name": meta_data.get("dataset_name"),
            "sql_query": meta_data.get("sql_query"),
            "data_table": meta_data.get("data_table"),
            "chart": meta_data.get("chart"),
            "scenario_matrix": meta_data.get("scenario_matrix"),
            "generated_file": meta_data.get("generated_file"),
            "tools_used": meta_data.get("tools_used", []),
            "answer": full_answer
        }

    def analytics_stream(
        self,
        query: str,
        session_id: Optional[str] = None,
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """Real-time SSE streaming analytics pipeline covering all 6 phases."""
        session_id = session_id or str(uuid.uuid4())[:8]
        tools_used = []

        # 1. Resolve Active Dataset & Multi-Table Schema
        df, rel_tables, dataset_name = self._resolve_dataset(query, doc_id)
        tools_used.append("relational_schema_connector")

        # Safe Natural Language Action Gate Check
        action_proposal = db_connector.analyze_mutation_request(query)
        if action_proposal:
            tools_used.append("safe_action_approval_gate")
            yield {
                "type": "status",
                "stage": "action_gate",
                "message": f"Safe Action Gate: Detected database modification intent on '{action_proposal['table']}'. Generating diff preview for approval..."
            }
            meta_event = {
                "type": "meta",
                "agent": self.name,
                "task_type": "ACTION_APPROVAL_REQUIRED",
                "dataset_name": dataset_name,
                "action_proposal": action_proposal,
                "sql_query": action_proposal.get("sql"),
                "tools_used": tools_used
            }
            yield meta_event

            prompt = (
                f"You are Z3 Echo, Enterprise Database & Analytics Agent. The user requested: '{query}'.\n"
                f"A Safe Action Proposal was generated to modify table '{action_proposal['table']}':\n"
                f"- Description: {action_proposal['description']}\n"
                f"- SQL Command: {action_proposal['sql']}\n"
                f"- Affected Records: {action_proposal['affected_rows_count']}\n\n"
                f"Explain concisely what this update modifies, and inform the user that changes are paused until approved in the Action Approval Card below."
            )
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate("You are Z3 Echo, Enterprise Database & Analytics Agent.", prompt):
                    yield {"type": "token", "content": chunk}
            else:
                yield {"type": "token", "content": prompt}
            yield {"type": "done", "answer": ""}
            return

        # 2. Route Query Intent
        plan = self.router.route_query(query)
        task_type = plan["task_type"]

        yield {
            "type": "status",
            "stage": "planning",
            "message": f"Identified task: {task_type} on {dataset_name}..."
        }

        sql_query = None
        data_table = None
        chart_config = None
        scenario_matrix = None
        generated_file = None
        execution_summary = ""

        # 3. Task Execution
        if task_type == AnalyticsTaskType.ROOT_CAUSE_ANALYSIS:
            yield {
                "type": "status",
                "stage": "root_cause_diagnostics",
                "message": "Performing multi-dimensional variance attribution and cost driver decomposition..."
            }
            rc_res = root_cause_engine.analyze_root_cause(query, df)
            if rc_res.get("success"):
                scenario_matrix = rc_res.get("diagnostic_matrix")
                chart_config = rc_res.get("chart")
                tools_used.append("root_cause_engine")
                top_neg = ", ".join([f"{d['entity']} ({d['delta']:+,})" for d in rc_res.get("primary_negative", [])])
                top_pos = ", ".join([f"{d['entity']} ({d['delta']:+,})" for d in rc_res.get("primary_positive", [])])
                execution_summary = (
                    f"Analyzed: {rc_res.get('metric')} ({rc_res.get('period_label')})\n"
                    f"Total Variance: {rc_res.get('total_variance'):+,} ({rc_res.get('total_variance_pct'):+}%)\n"
                    f"Top Negative Drag Drivers: {top_neg or 'None'}\n"
                    f"Top Positive Momentum Drivers: {top_pos or 'None'}"
                )

        elif task_type == AnalyticsTaskType.ANOMALY_AUDIT:
            yield {
                "type": "status",
                "stage": "anomaly_watchdog",
                "message": "Scanning dataset for statistical outliers (Z-scores/IQR) and integrity flaws..."
            }
            an_res = anomaly_watchdog.scan_dataset(df)
            if an_res.get("success"):
                scenario_matrix = an_res.get("anomaly_matrix")
                tools_used.append("anomaly_watchdog")
                execution_summary = (
                    f"Audit Health Score: {an_res.get('health_score')}% / 100%\n"
                    f"Scanned: {an_res.get('total_records')} records across {an_res.get('total_columns')} columns\n"
                    f"Identified Issues: {an_res.get('issues_count')} anomalies ({an_res.get('critical_count')} critical)"
                )

        elif task_type == AnalyticsTaskType.PREDICTIVE_FORECAST:
            yield {
                "type": "status",
                "stage": "forecasting",
                "message": "Fitting time-series regression with seasonality cycle detection..."
            }
            periods = plan.get("periods_ahead", 3)
            f_res = forecasting_engine.generate_forecast(df, periods_ahead=periods)
            if f_res.get("success"):
                chart_config = f_res.get("chart")
                tools_used.append("seasonality_forecasting_engine")
                if f_res.get("projection_table"):
                    data_table = {
                        "title": f"Forecast Projection Table ({f_res['target_metric']} • {f_res.get('seasonality_note', '')})",
                        "headers": ["Projected Period", "Forecasted Value", "Lower Bound (-8%)", "Upper Bound (+8%)"],
                        "rows": [[p["period"], f"{p['projected_value']:,}", f"{p['lower_bound']:,}", f"{p['upper_bound']:,}"] for p in f_res["projection_table"]]
                    }
                execution_summary = (
                    f"Target Metric: {f_res.get('target_metric')}\n"
                    f"Historical Baseline: {f_res.get('historical_last'):,}\n"
                    f"Projected End Value: {f_res.get('projected_end'):,} ({f_res.get('projected_growth_pct'):+}%)\n"
                    f"Seasonality: {f_res.get('seasonality_note')}\n"
                    f"Model R² Confidence Score: {f_res.get('r_squared')}"
                )

        elif task_type == AnalyticsTaskType.WHAT_IF_SIMULATION:
            yield {
                "type": "status",
                "stage": "simulating",
                "message": "Modeling financial elasticity and evaluating parameter variances..."
            }
            sim_res = scenario_simulator.simulate(query, df)
            if sim_res.get("success"):
                scenario_matrix = sim_res.get("matrix")
                chart_config = sim_res.get("chart")
                tools_used.append("scenario_simulator")
                s = sim_res.get("summary", {})
                execution_summary = (
                    f"Base Profit: {s.get('base_profit'):,}\n"
                    f"Simulated Profit: {s.get('simulated_profit'):,}\n"
                    f"Variance: {s.get('profit_delta'):+,} ({s.get('profit_pct'):+}%)\n"
                    f"Margin Shift: {s.get('base_margin')}% -> {s.get('simulated_margin')}%"
                )

        else:
            # TEXT_TO_SQL or MULTI_TABLE_JOIN or ANALYTICS_EXPORT
            yield {
                "type": "status",
                "stage": "executing_sql",
                "message": "Compiling safe multi-table DuckDB SQL query..."
            }
            # If multi-table is available, use primary table or full relational context
            sql_res = sql_engine.run_text_to_sql(query, df)
            tools_used.append("duckdb_sql_engine")
            sql_query = sql_res.get("sql")

            if sql_res.get("success"):
                data_table = {
                    "title": f"SQL Query Results ({sql_res.get('row_count', 0)} rows returned in {sql_res.get('execution_time_ms', 0)}ms)",
                    "headers": sql_res.get("headers", []),
                    "rows": sql_res.get("rows", [])
                }
                execution_summary = f"Query executed successfully in {sql_res.get('execution_time_ms')}ms. Returned {sql_res.get('row_count')} records."
            else:
                execution_summary = f"SQL Execution Note: {sql_res.get('error')}"

        # 4. Synthesize Executive Analytics Intelligence
        system_prompt = (
            "You are Z3 Echo, the Advanced Enterprise Database & Predictive Analytics Agent developed by AxomAI AGI.\n"
            "Your specialty: Transforming raw enterprise data, SQL outputs, root-cause diagnostics, and forecasting projections into "
            "clear, decisive executive briefings.\n\n"
            "CRITICAL PROTOCOLS:\n"
            "1. Deliver precise, grounded numbers with bold formatting.\n"
            "2. Structure:\n"
            "   - ## 📊 Executive Summary (High-level findings in 2 concise paragraphs)\n"
            "   - ## 🔍 Key Metrics & Analytical Breakdown (Bullet points with exact percentages, drivers, and figures)\n"
            "   - ## 💡 Strategic Recommendations & Action Plan (Clear, actionable takeaways for leadership)\n"
            "3. Match the user's language (English, Hindi, or Hinglish) naturally.\n"
            "4. Do not output raw SQL code blocks in prose, as the SQL query is already rendered in the UI badge."
        )

        user_prompt = (
            f"USER QUERY: {query}\n"
            f"ANALYTICS TASK: {task_type}\n"
            f"DATASET: {dataset_name}\n"
            f"EXECUTION SUMMARY:\n{execution_summary}\n\n"
        )
        if data_table and data_table.get("rows"):
            preview_rows = [f"| {' | '.join(data_table['headers'])} |"]
            for r in data_table["rows"][:5]:
                preview_rows.append(f"| {' | '.join(str(c) for c in r)} |")
            user_prompt += "DATA RESULTS PREVIEW:\n" + "\n".join(preview_rows) + "\n\n"

        full_answer = ""
        if llm_brain.is_available:
            try:
                full_answer = llm_brain.generate(system_prompt, user_prompt, temperature=0.1)
            except Exception as e:
                full_answer = f"Analytics synthesis note: {execution_summary}\n\n{e}"
        else:
            full_answer = f"### Analytics Summary ({task_type})\n\n{execution_summary}"

        # 5. Check if user requested an Executive PDF Report Export
        is_export_requested = (
            task_type == AnalyticsTaskType.ANALYTICS_EXPORT
            or any(w in query.lower() for w in ["pdf", "dossier", "export report", "download report", "board deck", "briefing pdf", "analytics dossier", "pdf bana"])
        )

        if is_export_requested and full_answer:
            summary_snippet = full_answer[:600]
            rep_res = report_exporter.generate_analytics_report(
                topic=query,
                summary=summary_snippet,
                detailed_findings=full_answer,
                sql_query=sql_query,
                data_table=data_table,
                scenario_matrix=scenario_matrix,
                task_type=task_type
            )
            if rep_res.get("success"):
                generated_file = rep_res
                tools_used.append("report_exporter")

        # 6. Yield Metadata event
        yield {
            "type": "meta",
            "agent": self.name,
            "task_type": task_type,
            "dataset_name": dataset_name,
            "sql_query": sql_query,
            "data_table": data_table,
            "chart": chart_config,
            "scenario_matrix": scenario_matrix,
            "generated_file": generated_file,
            "tools_used": tools_used
        }

        # 7. Stream tokens
        words = full_answer.split(" ")
        for i in range(0, len(words), 4):
            chunk = " ".join(words[i:i+4]) + " "
            yield {
                "type": "token",
                "content": chunk
            }

        yield {
            "type": "done",
            "answer": full_answer
        }

        # 8. Log to PostgreSQL
        try:
            with SyncSessionLocal() as db:
                task_log = AgentTaskLog(
                    session_id=session_id,
                    document_id=uuid.UUID(doc_id) if doc_id and doc_id != "database_analytics" else None,
                    task_type=task_type,
                    user_query=query,
                    tools_used=tools_used,
                    evidence=[{"dataset": dataset_name, "records": len(df)}],
                    response=full_answer[:2000]
                )
                db.add(task_log)
                db.commit()
        except Exception:
            pass

z3_echo_agent = Z3EchoAgent()
