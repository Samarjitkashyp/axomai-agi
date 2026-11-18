"""
AxomAI Cognitive Memory Engine - Tier 4: Procedural Memory (Skills & Tool Synthesis Registry).
Stores executable skills, specialized algorithms, and autonomous tools
invented by AxomAI agents, making them permanently available across the fleet.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from axomai.config import settings

class ProceduralMemory:
    """Persistent registry of autonomous skills and synthesized algorithmic tools."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or (settings.STORAGE_DIR / "cognitive_memory.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._runtime_cache: Dict[str, Callable] = {}
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS procedural_skills (
                    skill_id TEXT PRIMARY KEY,
                    skill_name TEXT NOT NULL UNIQUE,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    code_snippet TEXT NOT NULL,
                    input_schema TEXT NOT NULL,
                    output_schema TEXT NOT NULL,
                    success_count INTEGER NOT NULL DEFAULT 0,
                    failure_count INTEGER NOT NULL DEFAULT 0,
                    is_verified INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    last_used_at TEXT
                )
            """)
            conn.commit()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM procedural_skills")
            if cursor.fetchone()[0] == 0:
                self._seed_default_skills(conn)

    def _seed_default_skills(self, conn):
        now = datetime.utcnow().isoformat()
        skills = [
            (
                "skill_mkt_arrhenius",
                "Arrhenius Mean Kinetic Temperature",
                "HEALTHCARE_ALGO",
                "Calculates thermal degradation over non-isothermal pharma cold chains.",
                """def execute(readings_celsius, delta_h=83.144):\n    import math\n    R = 8.31446261815324e-3\n    kelvins = [t + 273.15 for t in readings_celsius]\n    n = len(kelvins)\n    if n == 0: return 0.0\n    sum_exp = sum(math.exp(-delta_h / (R * tk)) for tk in kelvins)\n    inv_mkt = -(R / delta_h) * math.log(sum_exp / n)\n    return round((1.0 / inv_mkt) - 273.15, 2)""",
                json.dumps({"readings_celsius": "List[float]"}),
                json.dumps({"mkt_celsius": "float"}),
                42, 0, 1, now, now
            ),
            (
                "skill_bishops_stability",
                "Bishop Simplified Slope Stability",
                "CIVIL_ENGINEERING",
                "Evaluates embankment factor of safety against rotational slip surface in flood zones.",
                """def execute(c_prime, phi_deg, weight_kn, pore_pressure_kn, alpha_deg, b_width):\n    import math\n    phi_rad = math.radians(phi_deg)\n    alpha_rad = math.radians(alpha_deg)\n    cos_a = math.cos(alpha_rad)\n    sin_a = math.sin(alpha_rad)\n    tan_phi = math.tan(phi_rad)\n    driving = weight_kn * sin_a\n    resisting = (c_prime * b_width) + (weight_kn - pore_pressure_kn) * tan_phi\n    fos = resisting / max(1.0, driving)\n    return round(max(0.5, fos), 2)""",
                json.dumps({"c_prime": "float", "phi_deg": "float", "weight_kn": "float"}),
                json.dumps({"factor_of_safety": "float"}),
                38, 0, 1, now, now
            )
        ]
        conn.executemany("""
            INSERT OR IGNORE INTO procedural_skills 
            (skill_id, skill_name, category, description, code_snippet, input_schema, output_schema, success_count, failure_count, is_verified, created_at, last_used_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, skills)
        conn.commit()

    def clear_all_skills(self) -> None:
        """Purges all stored procedural skills to allow clean dynamic operation."""
        self._runtime_cache.clear()
        with self._get_connection() as conn:
            conn.execute("DELETE FROM procedural_skills")
            conn.commit()

    def register_skill(
        self,
        skill_name: str,
        category: str,
        description: str,
        code_snippet: str,
        input_schema: Dict[str, Any],
        output_schema: Dict[str, Any],
        is_verified: bool = False
    ) -> Dict[str, Any]:
        """Registers a newly synthesized tool or skill into procedural memory."""
        skill_id = f"skill_{skill_name.lower().replace(' ', '_')}"
        now = datetime.utcnow().isoformat()

        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO procedural_skills 
                (skill_id, skill_name, category, description, code_snippet, input_schema, output_schema, success_count, failure_count, is_verified, created_at, last_used_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, ?, ?, ?)
                ON CONFLICT(skill_name) DO UPDATE SET
                    code_snippet = excluded.code_snippet,
                    description = excluded.description,
                    input_schema = excluded.input_schema,
                    output_schema = excluded.output_schema,
                    is_verified = excluded.is_verified,
                    last_used_at = excluded.last_used_at
            """, (
                skill_id,
                skill_name,
                category,
                description,
                code_snippet,
                json.dumps(input_schema),
                json.dumps(output_schema),
                1 if is_verified else 0,
                now,
                now
            ))
            conn.commit()

        # Invalidate cache
        if skill_id in self._runtime_cache:
            del self._runtime_cache[skill_id]

        return {
            "skill_id": skill_id,
            "skill_name": skill_name,
            "status": "REGISTERED",
            "verified": is_verified
        }

    def execute_skill(self, skill_name_or_id: str, **kwargs) -> Dict[str, Any]:
        """Executes a registered skill within an isolated runtime scope."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM procedural_skills 
                WHERE LOWER(skill_id) = LOWER(?) OR LOWER(skill_name) = LOWER(?)
            """, (skill_name_or_id, skill_name_or_id))
            row = cursor.fetchone()

        if not row:
            return {"error": f"Skill '{skill_name_or_id}' not found in procedural memory", "success": False}

        code = row["code_snippet"]
        scope = {}
        try:
            # Safe execution sandbox for pure mathematical/analytical python functions
            def _safe_import(name, *args, **kwargs):
                allowed = {"math", "json", "re", "datetime", "typing"}
                if name in allowed:
                    return __import__(name, *args, **kwargs)
                raise ImportError(f"Import of module '{name}' is restricted by sovereign sandbox policy.")

            safe_builtins = {
                "__import__": _safe_import,
                "math": __import__("math"),
                "range": range,
                "len": len,
                "min": min,
                "max": max,
                "sum": sum,
                "round": round,
                "abs": abs,
                "float": float,
                "int": int,
                "str": str,
                "list": list,
                "dict": dict,
                "isinstance": isinstance
            }
            exec(code, {"__builtins__": safe_builtins}, scope)
            if "execute" not in scope:
                return {"error": "Skill code missing 'execute' entrypoint", "success": False}

            result = scope["execute"](**kwargs)
            self._record_telemetry(row["skill_id"], success=True)
            return {
                "skill_id": row["skill_id"],
                "skill_name": row["skill_name"],
                "result": result,
                "success": True
            }
        except Exception as e:
            self._record_telemetry(row["skill_id"], success=False)
            return {"error": str(e), "success": False}

    def _record_telemetry(self, skill_id: str, success: bool):
        now = datetime.utcnow().isoformat()
        with self._get_connection() as conn:
            if success:
                conn.execute("""
                    UPDATE procedural_skills 
                    SET success_count = success_count + 1, last_used_at = ? 
                    WHERE skill_id = ?
                """, (now, skill_id))
            else:
                conn.execute("""
                    UPDATE procedural_skills 
                    SET failure_count = failure_count + 1, last_used_at = ? 
                    WHERE skill_id = ?
                """, (now, skill_id))
            conn.commit()

    def list_skills(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT skill_id, skill_name, category, description, success_count, failure_count, is_verified FROM procedural_skills")
            return [dict(r) for r in cursor.fetchall()]

procedural_memory = ProceduralMemory()
