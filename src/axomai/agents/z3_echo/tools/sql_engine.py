"""
Z3 Echo Text-to-SQL & In-Memory Analytical SQL Engine.
Supports high-speed schema inspection, LLM SQL generation,
safety validation, self-correcting query execution, and DuckDB analytics.
"""

import re
import time
import duckdb
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from rich.console import Console

from axomai.core.llm import llm_brain

console = Console()

FORBIDDEN_SQL_PATTERNS = [
    r'\bdrop\b', r'\bdelete\b', r'\btruncate\b', r'\bupdate\b',
    r'\binsert\b', r'\balter\b', r'\battach\b', r'\bdetach\b',
    r'\bcopy\b', r'\binstall\b', r'\bload\b', r'\bcreate\s+table\b',
    r'\bimport\b', r'\bexport\b', r'\bexec\b', r'\bexecute\b'
]

def generate_default_enterprise_dataset() -> pd.DataFrame:
    """
    Provides a rich, realistic enterprise dataset for testing and immediate analytics
    when no custom document is uploaded.
    """
    records = [
        {"period": "2025-01", "month": "Jan", "quarter": "Q1", "region": "North", "category": "Enterprise AI", "units": 120, "unit_price": 50000, "revenue": 60.0, "marketing_cost": 12.0, "cogs": 24.0, "profit": 24.0, "new_customers": 45},
        {"period": "2025-02", "month": "Feb", "quarter": "Q1", "region": "West", "category": "Cloud Infra", "units": 140, "unit_price": 48000, "revenue": 67.2, "marketing_cost": 13.5, "cogs": 26.5, "profit": 27.2, "new_customers": 52},
        {"period": "2025-03", "month": "Mar", "quarter": "Q1", "region": "South", "category": "SaaS Platform", "units": 175, "unit_price": 52000, "revenue": 91.0, "marketing_cost": 17.0, "cogs": 34.0, "profit": 40.0, "new_customers": 68},
        {"period": "2025-04", "month": "Apr", "quarter": "Q2", "region": "North", "category": "Enterprise AI", "units": 160, "unit_price": 50000, "revenue": 80.0, "marketing_cost": 15.0, "cogs": 31.0, "profit": 34.0, "new_customers": 58},
        {"period": "2025-05", "month": "May", "quarter": "Q2", "region": "East", "category": "Analytics Suite", "units": 190, "unit_price": 45000, "revenue": 85.5, "marketing_cost": 16.5, "cogs": 33.0, "profit": 36.0, "new_customers": 64},
        {"period": "2025-06", "month": "Jun", "quarter": "Q2", "region": "West", "category": "Cloud Infra", "units": 210, "unit_price": 48000, "revenue": 100.8, "marketing_cost": 19.0, "cogs": 39.0, "profit": 42.8, "new_customers": 75},
        {"period": "2025-07", "month": "Jul", "quarter": "Q3", "region": "South", "category": "Enterprise AI", "units": 230, "unit_price": 51000, "revenue": 117.3, "marketing_cost": 21.0, "cogs": 44.5, "profit": 51.8, "new_customers": 82},
        {"period": "2025-08", "month": "Aug", "quarter": "Q3", "region": "North", "category": "SaaS Platform", "units": 250, "unit_price": 53000, "revenue": 132.5, "marketing_cost": 23.5, "cogs": 49.0, "profit": 60.0, "new_customers": 91},
        {"period": "2025-09", "month": "Sep", "quarter": "Q3", "region": "East", "category": "Analytics Suite", "units": 270, "unit_price": 46000, "revenue": 124.2, "marketing_cost": 22.0, "cogs": 47.0, "profit": 55.2, "new_customers": 88},
        {"period": "2025-10", "month": "Oct", "quarter": "Q4", "region": "West", "category": "Cloud Infra", "units": 290, "unit_price": 49000, "revenue": 142.1, "marketing_cost": 25.0, "cogs": 52.5, "profit": 64.6, "new_customers": 98},
        {"period": "2025-11", "month": "Nov", "quarter": "Q4", "region": "South", "category": "Enterprise AI", "units": 320, "unit_price": 52000, "revenue": 166.4, "marketing_cost": 28.0, "cogs": 59.0, "profit": 79.4, "new_customers": 112},
        {"period": "2025-12", "month": "Dec", "quarter": "Q4", "region": "North", "category": "Enterprise AI", "units": 350, "unit_price": 54000, "revenue": 189.0, "marketing_cost": 31.0, "cogs": 65.0, "profit": 93.0, "new_customers": 125}
    ]
    return pd.DataFrame(records)

class SQLEngine:
    def __init__(self):
        self.table_name = "analytics_data"

    def validate_sql_safety(self, sql: str) -> Tuple[bool, Optional[str]]:
        """Validates that query is strictly read-only and free from destructive patterns."""
        cleaned = sql.strip().lower()
        if not (cleaned.startswith("select") or cleaned.startswith("with") or cleaned.startswith("describe") or cleaned.startswith("explain")):
            return False, "Query must start with SELECT, WITH, or DESCRIBE."

        for pattern in FORBIDDEN_SQL_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                return False, f"Prohibited SQL keyword or operation detected: '{pattern}'"

        return True, None

    def generate_sql(self, user_query: str, df: pd.DataFrame, error_feedback: Optional[str] = None) -> str:
        """
        Uses LLM with schema context to synthesize valid DuckDB/PostgreSQL SQL.
        """
        schema_info = []
        for col, dtype in df.dtypes.items():
            sample_vals = [str(x) for x in df[col].dropna().unique()[:3]]
            schema_info.append(f"  - `{col}` ({dtype}): sample values {sample_vals}")
        schema_str = "\n".join(schema_info)

        system_prompt = (
            "You are an Elite Database Architect and SQL Generation Expert for AxomAI AGI Z3 Echo.\n"
            f"Table Name: `{self.table_name}`\n"
            f"Table Schema & Column Sample Values:\n{schema_str}\n\n"
            "CRITICAL RULES:\n"
            "1. Output ONLY the raw SQL query. No explanations, no markdown blocks, no quotes around the code.\n"
            "2. Strictly write read-only SELECT queries (DuckDB / standard SQL syntax).\n"
            "3. Handle NULLs gracefully with COALESCE or IS NOT NULL.\n"
            "4. Format currency, decimals, and roundings properly (e.g., ROUND(..., 2)).\n"
            "5. If calculating growth or rankings, use window functions like LAG, RANK, or OVER ().\n"
            "6. Always assign clear, readable column aliases (e.g. `AS total_revenue`)."
        )

        user_prompt = f"User Request: {user_query}"
        if error_feedback:
            user_prompt += f"\n\nPREVIOUS SQL FAILED WITH ERROR: {error_feedback}\nPlease fix the SQL query to resolve this error."

        if not llm_brain.is_available:
            return f"SELECT * FROM {self.table_name} LIMIT 10;"

        try:
            raw_sql = llm_brain.generate(system_prompt, user_prompt, temperature=0.0)
            clean_sql = raw_sql.strip()
            if "```sql" in clean_sql:
                clean_sql = clean_sql.split("```sql")[1].split("```")[0].strip()
            elif "```" in clean_sql:
                clean_sql = clean_sql.split("```")[1].split("```")[0].strip()
            
            clean_sql = clean_sql.rstrip(";")
            return clean_sql
        except Exception as e:
            console.print(f"[dim red][SQL Gen Error][/dim red] {e}")
            return f"SELECT * FROM {self.table_name} LIMIT 10"

    def execute_query(self, sql: str, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Executes safe SQL on the in-memory DataFrame using DuckDB.
        """
        is_safe, error_msg = self.validate_sql_safety(sql)
        if not is_safe:
            return {
                "success": False,
                "sql": sql,
                "error": error_msg,
                "headers": [],
                "rows": [],
                "row_count": 0,
                "execution_time_ms": 0.0
            }

        start_time = time.perf_counter()
        try:
            con = duckdb.connect(database=":memory:")
            # Register active dataframe
            con.register(self.table_name, df)
            
            result_df = con.execute(sql).df()
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

            headers = [str(c) for c in result_df.columns]
            rows = []
            for _, r in result_df.head(100).iterrows():
                row_vals = []
                for val in r:
                    if pd.isna(val):
                        row_vals.append("—")
                    elif isinstance(val, (int, np.integer)):
                        row_vals.append(f"{val:,}")
                    elif isinstance(val, (float, np.floating)):
                        row_vals.append(f"{val:,.2f}" if abs(val) >= 0.01 else f"{val:.4f}")
                    else:
                        row_vals.append(str(val))
                rows.append(row_vals)

            return {
                "success": True,
                "sql": sql,
                "headers": headers,
                "rows": rows,
                "row_count": len(result_df),
                "execution_time_ms": elapsed_ms,
                "df": result_df,
                "error": None
            }
        except Exception as e:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return {
                "success": False,
                "sql": sql,
                "error": str(e),
                "headers": [],
                "rows": [],
                "row_count": 0,
                "execution_time_ms": elapsed_ms
            }

    def run_text_to_sql(self, user_query: str, df: pd.DataFrame) -> Dict[str, Any]:
        """
        End-to-end Text-to-SQL execution with automatic self-healing retry on error.
        """
        sql = self.generate_sql(user_query, df)
        result = self.execute_query(sql, df)

        # Self-healing retry if first attempt failed
        if not result["success"] and result.get("error") and llm_brain.is_available:
            console.print(f"[dim yellow][Z3 Echo SQL Retry][/dim yellow] Fixing: {result['error']}")
            fixed_sql = self.generate_sql(user_query, df, error_feedback=result["error"])
            retry_res = self.execute_query(fixed_sql, df)
            if retry_res["success"]:
                return retry_res

        return result

sql_engine = SQLEngine()

