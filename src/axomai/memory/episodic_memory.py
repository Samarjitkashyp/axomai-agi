"""
AxomAI Cognitive Memory Engine - Tier 2: Episodic Memory (Experiences & Mistakes).
Stores past missions, execution outcomes, reward feedback (0.0 to 1.0),
and self-critique lessons learned so the AGI never repeats past mistakes.
"""

import sqlite3
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from axomai.config import settings

class EpisodicMemory:
    """Persistent experience and mistake-avoidance memory."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or (settings.STORAGE_DIR / "cognitive_memory.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS episodic_episodes (
                    episode_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    query TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    outcome_status TEXT NOT NULL,
                    reward_score REAL NOT NULL,
                    reflection TEXT,
                    lesson_learned TEXT,
                    vector_tokens TEXT,
                    metadata_json TEXT
                )
            """)
            conn.commit()
            # Seed default high-value baseline lessons if empty
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM episodic_episodes")
            if cursor.fetchone()[0] == 0:
                self._seed_default_episodes(conn)

    def _seed_default_episodes(self, conn):
        defaults = [
            (
                "ep_seed_01",
                "2026-10-01T08:00:00",
                "Export Orthodox tea from Dibrugarh to Hamburg without currency hedge",
                "y1",
                "SUBOPTIMAL",
                0.45,
                "Exposed tea exporter to 3.8% EUR/INR exchange rate depreciation during 45-day transit.",
                "Always execute Garman-Kohlhagen zero-cost FX collar via Z14 Horizon on cross-border shipments.",
                "export orthodox tea dibrugarh hamburg currency hedge fx collar",
                json.dumps({"domain": "agri_export"})
            ),
            (
                "ep_seed_02",
                "2026-10-15T14:30:00",
                "EPC Bridge pier excavation in Brahmaputra seismic Zone V with standard reinforcement",
                "y4",
                "HIGH_RISK",
                0.50,
                "Seismic Factor of Safety fell to 1.06 under PGA 0.36g peak ground acceleration.",
                "Mandate high-tenacity multi-tier geogrid and geotextile tube reinforcement to achieve FoS >= 1.25.",
                "epc bridge excavation brahmaputra seismic zone v geogrid safety",
                json.dumps({"domain": "civil_infra"})
            ),
            (
                "ep_seed_03",
                "2026-11-01T11:00:00",
                "Deploy PE buyout underwriting for Northeast food processing asset with Monte Carlo DCF",
                "z17",
                "OPTIMAL",
                0.98,
                "Accurately predicted median enterprise valuation and mapped EBITDA synergies with 95% confidence.",
                "Incorporate both terminal multiple method and Gordon Growth model for resilient cross-border valuations.",
                "pe buyout underwriting northeast food processing monte carlo dcf valuation",
                json.dumps({"domain": "institutional_pe"})
            )
        ]
        conn.executemany("""
            INSERT INTO episodic_episodes 
            (episode_id, timestamp, query, agent_id, outcome_status, reward_score, reflection, lesson_learned, vector_tokens, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, defaults)
        conn.commit()

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z0-9_\-]{3,}\b', text.lower())
        stopwords = {"the", "and", "for", "with", "from", "that", "this", "our", "are", "was", "were", "into"}
        return [w for w in words if w not in stopwords]

    def _compute_similarity(self, tokens_q: List[str], tokens_target: List[str]) -> float:
        if not tokens_q or not tokens_target:
            return 0.0
        set_q = set(tokens_q)
        set_t = set(tokens_target)
        intersection = len(set_q.intersection(set_t))
        union = len(set_q.union(set_t))
        return intersection / union if union > 0 else 0.0

    def record_episode(
        self,
        query: str,
        agent_id: str,
        outcome_status: str,
        reward_score: float,
        reflection: str,
        lesson_learned: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Records an execution experience with its self-critique lesson."""
        episode_id = f"ep_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:17]}"
        timestamp = datetime.utcnow().isoformat()
        tokens = " ".join(self._tokenize(f"{query} {reflection} {lesson_learned}"))
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO episodic_episodes 
                (episode_id, timestamp, query, agent_id, outcome_status, reward_score, reflection, lesson_learned, vector_tokens, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                episode_id,
                timestamp,
                query,
                agent_id,
                outcome_status,
                float(reward_score),
                reflection,
                lesson_learned,
                tokens,
                json.dumps(metadata or {})
            ))
            conn.commit()

        return {
            "episode_id": episode_id,
            "status": "RECORDED",
            "reward_score": reward_score,
            "lesson_learned": lesson_learned
        }

    def recall_relevant_lessons(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Recalls the most relevant past experiences and lessons for a given query."""
        q_tokens = self._tokenize(query)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM episodic_episodes")
            rows = cursor.fetchall()

        scored = []
        for row in rows:
            target_tokens = (row["vector_tokens"] or "").split()
            sim = self._compute_similarity(q_tokens, target_tokens)
            # Boost matches that contain exact words
            scored.append({
                "episode_id": row["episode_id"],
                "similarity": round(sim, 3),
                "query": row["query"],
                "agent_id": row["agent_id"],
                "outcome_status": row["outcome_status"],
                "reward_score": row["reward_score"],
                "reflection": row["reflection"],
                "lesson_learned": row["lesson_learned"],
                "timestamp": row["timestamp"]
            })

        # Sort by similarity descending, then reward_score
        scored.sort(key=lambda x: (x["similarity"], x["reward_score"]), reverse=True)
        return [s for s in scored if s["similarity"] > 0.05][:top_k]

    def get_stats(self) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), AVG(reward_score) FROM episodic_episodes")
            count, avg_reward = cursor.fetchone()
            cursor.execute("SELECT agent_id, COUNT(*) FROM episodic_episodes GROUP BY agent_id")
            by_agent = {row[0]: row[1] for row in cursor.fetchall()}

        return {
            "total_episodes": count or 0,
            "average_reward_score": round(avg_reward or 0.0, 3),
            "episodes_by_agent": by_agent
        }

episodic_memory = EpisodicMemory()

