"""
AxomAI Cognitive Memory Engine - Tier 3: 4D Temporal Knowledge Graph Memory.
Maintains persistent entity-relation knowledge graph, ontological triples (Subject-Predicate-Object),
with full 4D temporal tracking (valid_from, valid_to, session_origin, epistemic_status),
autonomous triple extraction from raw dialogue, and multi-hop relational pathfinding.
"""

import sqlite3
import json
import re
from enum import Enum
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple
from axomai.config import settings

class EpistemicStatus(str, Enum):
    EXTRACTED = "EXTRACTED"
    SOURCE_REPORTED = "SOURCE_REPORTED"
    CORROBORATED = "CORROBORATED"
    VERIFIED = "VERIFIED"
    ACTIVE = "ACTIVE"
    DISPUTED = "DISPUTED"
    SUPERSEDED = "SUPERSEDED"
    REFUTED = "REFUTED"

# Predicates where an entity can have only one active state at a given time
FUNCTIONAL_EXCLUSIVE_PREDICATES: Set[str] = {
    "LOCATED_IN",
    "RELOCATED_TO",
    "HEADQUARTERS_IN",
    "BUDGET_IS",
    "PRICING_IS",
    "STATUS_IS",
    "CURRENT_TARGET",
    "PREFERRED_STRATEGY",
    "PRIMARY_GOAL",
    "CEO_OF",
    "OPERATING_STATE",
    "CURRENT_VOLUME"
}

class SemanticGraphMemory:
    """Persistent 4D Temporal Entity-Relation Graph and Universal Semantic Memory."""

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
                CREATE TABLE IF NOT EXISTS semantic_entities (
                    entity_id TEXT PRIMARY KEY,
                    entity_name TEXT NOT NULL UNIQUE,
                    entity_type TEXT NOT NULL,
                    attributes_json TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS semantic_triples (
                    triple_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_name TEXT NOT NULL,
                    predicate TEXT NOT NULL,
                    object_name TEXT NOT NULL,
                    confidence REAL NOT NULL DEFAULT 1.0,
                    source_ref TEXT,
                    verified INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    valid_from TEXT,
                    valid_to TEXT,
                    session_origin TEXT,
                    epistemic_status TEXT NOT NULL DEFAULT 'ACTIVE'
                )
            """)
            conn.commit()

            # Schema Migration for existing DBs
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(semantic_triples)")
            existing_cols = {row["name"] for row in cursor.fetchall()}

            if "valid_from" not in existing_cols:
                conn.execute("ALTER TABLE semantic_triples ADD COLUMN valid_from TEXT DEFAULT NULL")
            if "valid_to" not in existing_cols:
                conn.execute("ALTER TABLE semantic_triples ADD COLUMN valid_to TEXT DEFAULT NULL")
            if "session_origin" not in existing_cols:
                conn.execute("ALTER TABLE semantic_triples ADD COLUMN session_origin TEXT DEFAULT NULL")
            if "epistemic_status" not in existing_cols:
                conn.execute("ALTER TABLE semantic_triples ADD COLUMN epistemic_status TEXT DEFAULT 'ACTIVE'")

            # Backfill valid_from for legacy rows
            conn.execute("UPDATE semantic_triples SET valid_from = created_at WHERE valid_from IS NULL")
            conn.commit()

            # Seed default high-value graph if empty
            cursor.execute("SELECT COUNT(*) FROM semantic_entities")
            if cursor.fetchone()[0] == 0:
                self._seed_default_graph(conn)

    def _seed_default_graph(self, conn):
        now = datetime.now(timezone.utc).isoformat()
        entities = [
            ("ent_semiconductor", "Advanced Semiconductor Fab", "CRITICAL_TECHNOLOGY", json.dumps({"node_nm": 3, "supply_chokepoint": "EUV Lithography", "strategic_significance": "Sovereign Compute Anchor"})),
            ("ent_transpacific", "Trans-Pacific Maritime Corridor", "GLOBAL_INFRASTRUCTURE", json.dumps({"throughput_teu": 25000000, "status": "Active International Gateway"})),
            ("ent_suez", "Suez Canal Maritime Gateway", "MARITIME_CHOKEPOINT", json.dumps({"transit_share_pct": 12.0, "significance": "Global Energy & Freight Lifeline"})),
            ("ent_grid_storage", "Grid Scale Battery Storage", "CLEAN_ENERGY_ASSET", json.dumps({"capacity_mwh": 2000, "role": "Intermittent Renewable Firming"})),
            ("ent_clean_ppa", "Renewable Power Purchase Agreement", "ENERGY_CONTRACT", json.dumps({"tenor_years": 25, "carbon_neutral": True, "vcs_verified": True})),
            ("ent_fidic_epc", "FIDIC Silver Book EPC Framework", "LEGAL_PROTOCOL", json.dumps({"dispute_adjudication_window_days": 28, "jurisdiction": "International Chamber of Commerce"}))
        ]
        conn.executemany("""
            INSERT OR IGNORE INTO semantic_entities (entity_id, entity_name, entity_type, attributes_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [(e[0], e[1], e[2], e[3], now, now) for e in entities])

        triples = [
            ("Advanced Semiconductor Fab", "DEPENDS_ON", "Trans-Pacific Maritime Corridor", 0.99, "Sovereign High-Tech Supply Chain Audit"),
            ("Trans-Pacific Maritime Corridor", "CONNECTS_TO", "Suez Canal Maritime Gateway", 0.98, "International Maritime Organization"),
            ("Grid Scale Battery Storage", "STABILIZES_GRID_FOR", "Advanced Semiconductor Fab", 0.97, "Global Energy Intelligence"),
            ("Renewable Power Purchase Agreement", "OFFSETS_CARBON_FOR", "Advanced Semiconductor Fab", 0.96, "ESG Sovereign Framework"),
            ("FIDIC Silver Book EPC Framework", "PROTECTS_CAPEX_FOR", "Grid Scale Battery Storage", 0.99, "International Arbitration Precedent")
        ]
        conn.executemany("""
            INSERT INTO semantic_triples (subject_name, predicate, object_name, confidence, source_ref, verified, created_at, valid_from, epistemic_status)
            VALUES (?, ?, ?, ?, ?, 1, ?, ?, 'ACTIVE')
        """, [(t[0], t[1], t[2], t[3], t[4], now, now) for t in triples])
        conn.commit()

    def add_entity(self, name: str, entity_type: str = "UNKNOWN_CONCEPT", attributes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        clean_name = name.strip()
        entity_id = f"ent_{abs(hash(clean_name.lower())) % 1000000:06d}"
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO semantic_entities (entity_id, entity_name, entity_type, attributes_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(entity_name) DO UPDATE SET
                    entity_type = CASE WHEN excluded.entity_type != 'UNKNOWN_CONCEPT' THEN excluded.entity_type ELSE semantic_entities.entity_type END,
                    attributes_json = excluded.attributes_json,
                    updated_at = excluded.updated_at
            """, (entity_id, clean_name, entity_type, json.dumps(attributes or {}), now, now))
            conn.commit()
        return {"entity_id": entity_id, "name": clean_name, "type": entity_type}

    def add_temporal_fact(
        self,
        subject: str,
        predicate: str,
        obj: str,
        confidence: float = 1.0,
        source_ref: str = "Autonomous Ingestion",
        session_id: Optional[str] = None,
        valid_from: Optional[str] = None,
        epistemic_status: str = "ACTIVE",
        verified: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Inserts an ontological fact triple with 4D temporal tracking and explicit epistemic status.
        Epistemic States: EXTRACTED, SOURCE_REPORTED, CORROBORATED, VERIFIED, ACTIVE, DISPUTED, SUPERSEDED, REFUTED.
        Automatically resolves contradictions by superseding prior exclusive facts.
        """
        now = datetime.now(timezone.utc).isoformat()
        v_from = valid_from or now
        norm_subj = subject.strip()
        norm_pred = predicate.upper().strip().replace(" ", "_")
        norm_obj = obj.strip()
        is_verified = verified if verified is not None else (1 if epistemic_status in ["ACTIVE", "CORROBORATED", "VERIFIED"] else 0)

        # Ensure entities exist
        self.add_entity(norm_subj, "UNKNOWN_CONCEPT")
        self.add_entity(norm_obj, "UNKNOWN_CONCEPT")

        superseded_count = 0
        with self._get_connection() as conn:
            # Contradiction Resolution: If predicate is exclusive, supersede existing active triples with different object
            if norm_pred in FUNCTIONAL_EXCLUSIVE_PREDICATES:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT triple_id, object_name FROM semantic_triples 
                    WHERE LOWER(subject_name) = LOWER(?) 
                      AND predicate = ? 
                      AND epistemic_status IN ('ACTIVE', 'CORROBORATED', 'VERIFIED')
                      AND LOWER(object_name) != LOWER(?)
                """, (norm_subj, norm_pred, norm_obj))
                old_rows = cursor.fetchall()
                for old in old_rows:
                    conn.execute("""
                        UPDATE semantic_triples 
                        SET valid_to = ?, epistemic_status = 'SUPERSEDED'
                        WHERE triple_id = ?
                    """, (now, old["triple_id"]))
                    superseded_count += 1

            # Check if this exact triple already exists actively
            cursor = conn.cursor()
            cursor.execute("""
                SELECT triple_id, confidence, source_ref, epistemic_status FROM semantic_triples 
                WHERE LOWER(subject_name) = LOWER(?) 
                  AND predicate = ? 
                  AND LOWER(object_name) = LOWER(?)
                  AND epistemic_status NOT IN ('SUPERSEDED', 'REFUTED')
            """, (norm_subj, norm_pred, norm_obj))
            existing = cursor.fetchone()

            if existing:
                # Corroborate existing fact if a new independent source confirms it
                old_status = existing["epistemic_status"]
                new_status = old_status
                if old_status in ["EXTRACTED", "SOURCE_REPORTED"] and source_ref != existing["source_ref"]:
                    new_status = "CORROBORATED"
                    is_verified = 1

                conn.execute("""
                    UPDATE semantic_triples 
                    SET confidence = MIN(0.99, MAX(confidence, ?) + 0.05), 
                        source_ref = source_ref || ' | ' || ?, 
                        session_origin = COALESCE(session_origin, ?),
                        epistemic_status = ?,
                        verified = ?
                    WHERE triple_id = ?
                """, (float(confidence), source_ref, session_id, new_status, is_verified, existing["triple_id"]))
                triple_id = existing["triple_id"]
                epistemic_status = new_status
            else:
                cursor.execute("""
                    INSERT INTO semantic_triples 
                    (subject_name, predicate, object_name, confidence, source_ref, verified, created_at, valid_from, valid_to, session_origin, epistemic_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, ?)
                """, (norm_subj, norm_pred, norm_obj, float(confidence), source_ref, is_verified, now, v_from, session_id, epistemic_status))
                triple_id = cursor.lastrowid

            conn.commit()

        return {
            "triple_id": triple_id,
            "subject": norm_subj,
            "predicate": norm_pred,
            "object": norm_obj,
            "confidence": confidence,
            "epistemic_status": epistemic_status,
            "verified": bool(is_verified),
            "superseded_prior_facts": superseded_count,
            "valid_from": v_from
        }

    def corroborate_fact(self, subject: str, predicate: str, obj: str, source_ref: str = "Secondary Corroboration") -> Dict[str, Any]:
        """Upgrades an unverified or extracted fact to CORROBORATED/VERIFIED status upon secondary evidence."""
        return self.add_temporal_fact(
            subject=subject,
            predicate=predicate,
            obj=obj,
            confidence=0.95,
            source_ref=source_ref,
            epistemic_status="CORROBORATED",
            verified=1
        )

    def add_fact(
        self,
        subject: str,
        predicate: str,
        obj: str,
        confidence: float = 1.0,
        source_ref: str = "Autonomous Ingestion"
    ) -> Dict[str, Any]:
        """Backward-compatible wrapper for legacy callers."""
        return self.add_temporal_fact(subject, predicate, obj, confidence, source_ref, epistemic_status="ACTIVE")

    def extract_and_ingest_triples_from_text(self, text: str, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Autonomous linguistic extractor: Parses subject-predicate-object triples
        directly from conversational utterances and ingests them into the 4D graph.
        """
        extracted = []
        if not text or len(text.strip()) < 10:
            return extracted

        patterns = [
            # Relocated / Located
            (r'(?i)([A-Za-z0-9_\s]{2,30}?)\s+(?:has relocated to|moved to|transferred to)\s+([A-Za-z0-9_\s]{2,30})', "RELOCATED_TO"),
            (r'(?i)([A-Za-z0-9_\s]{2,30}?)\s+(?:is located in|situated in|based in)\s+([A-Za-z0-9_\s]{2,30})', "LOCATED_IN"),
            # Pricing / Cost / Budget
            (r'(?i)(?:price of|pricing of|cost of)\s+([A-Za-z0-9_\s]{2,30}?)\s+(?:is|has reached|jumped to|dropped to)\s+([\d,.]+\s*(?:INR|USD|EUR|₹|\$|per kg)?)', "PRICING_IS"),
            (r'(?i)(?:budget for|allocated budget for)\s+([A-Za-z0-9_\s]{2,30}?)\s+(?:is|set at)\s+([\d,.]+\s*(?:INR|USD|EUR|₹|\$|lakh|crore|million)?)', "BUDGET_IS"),
            # Export / Trade
            (r'(?i)([A-Za-z0-9_\s]{2,30}?)\s+(?:exports to|ships to|destined for)\s+([A-Za-z0-9_\s]{2,30})', "EXPORTS_TO"),
            (r'(?i)([A-Za-z0-9_\s]{2,30}?)\s+(?:transits through|routed via)\s+([A-Za-z0-9_\s]{2,30})', "TRANSITS_THROUGH"),
            # Strategy / Preference / Requirement
            (r'(?i)(?:our preferred strategy for|preference for)\s+([A-Za-z0-9_\s]{2,30}?)\s+is\s+([A-Za-z0-9_\s]{3,50})', "PREFERRED_STRATEGY"),
            (r'(?i)([A-Za-z0-9_\s]{2,30}?)\s+(?:mandates|requires|needs)\s+([A-Za-z0-9_\s]{3,50})', "REQUIRES"),
            # Ownership / Operation
            (r'(?i)([A-Za-z0-9_\s]{2,30}?)\s+(?:operates|manages|controls)\s+([A-Za-z0-9_\s]{2,30})', "OPERATES")
        ]

        cleaned_text = re.sub(r'[\r\n]+', '. ', text)
        sentences = [s.strip() for s in cleaned_text.split('.') if len(s.strip()) > 8]

        for sent in sentences:
            for pattern, pred in patterns:
                match = re.search(pattern, sent)
                if match:
                    subj = match.group(1).strip()
                    obj = match.group(2).strip()
                    # Filter out short or garbage words
                    if len(subj) > 2 and len(obj) > 2 and len(subj) < 40 and len(obj) < 60:
                        if not any(w in subj.lower() for w in ["what", "how", "when", "why", "where", "tell me"]):
                            try:
                                res = self.add_temporal_fact(
                                    subject=subj,
                                    predicate=pred,
                                    obj=obj,
                                    confidence=0.85,
                                    source_ref="Autonomous Dialogue Ingestion",
                                    session_id=session_id,
                                    epistemic_status="EXTRACTED",
                                    verified=0
                                )
                                extracted.append(res)
                            except Exception:
                                pass

        return extracted

    def get_temporal_history(self, subject_name: str, predicate: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns the full chronological evolution of facts for an entity."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if predicate:
                cursor.execute("""
                    SELECT * FROM semantic_triples 
                    WHERE LOWER(subject_name) = LOWER(?) AND predicate = ?
                    ORDER BY valid_from ASC
                """, (subject_name, predicate.upper()))
            else:
                cursor.execute("""
                    SELECT * FROM semantic_triples 
                    WHERE LOWER(subject_name) = LOWER(?)
                    ORDER BY valid_from ASC
                """, (subject_name,))
            return [dict(r) for r in cursor.fetchall()]

    def query_temporal_subgraph(self, entity_name: str, active_only: bool = True) -> Dict[str, Any]:
        """Retrieves active vs superseded facts for an entity."""
        status_filter = "AND epistemic_status NOT IN ('SUPERSEDED', 'REFUTED')" if active_only else ""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM semantic_entities WHERE LOWER(entity_name) = LOWER(?)", (entity_name,))
            ent_row = cursor.fetchone()

            cursor.execute(f"SELECT * FROM semantic_triples WHERE LOWER(subject_name) = LOWER(?) {status_filter}", (entity_name,))
            outbound = [dict(r) for r in cursor.fetchall()]

            cursor.execute(f"SELECT * FROM semantic_triples WHERE LOWER(object_name) = LOWER(?) {status_filter}", (entity_name,))
            inbound = [dict(r) for r in cursor.fetchall()]

        return {
            "entity": entity_name,
            "found": bool(ent_row or outbound or inbound),
            "type": ent_row["entity_type"] if ent_row else "DYNAMIC",
            "active_outbound": outbound,
            "active_inbound": inbound
        }

    def query_entity_subgraph(self, entity_name: str) -> Dict[str, Any]:
        """Backward-compatible query."""
        sub = self.query_temporal_subgraph(entity_name, active_only=True)
        return {
            "entity": entity_name,
            "found": sub["found"],
            "type": sub["type"],
            "attributes": {},
            "outbound_relations": sub["active_outbound"],
            "inbound_relations": sub["active_inbound"]
        }

    def find_multi_hop_path(self, start_entity: str, target_entity: str, max_depth: int = 3) -> Optional[List[Dict[str, Any]]]:
        """Discovers relational reasoning paths connecting two concepts across valid facts."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT subject_name, predicate, object_name 
                FROM semantic_triples 
                WHERE epistemic_status NOT IN ('SUPERSEDED', 'REFUTED')
            """)
            edges = cursor.fetchall()

        adj: Dict[str, List[tuple]] = {}
        for edge in edges:
            s, p, o = edge["subject_name"].lower(), edge["predicate"], edge["object_name"].lower()
            if s not in adj: adj[s] = []
            adj[s].append((p, edge["object_name"], o))

        start_low = start_entity.lower()
        target_low = target_entity.lower()
        queue = [[(None, "START", start_entity)]]
        visited = {start_low}

        while queue:
            path = queue.pop(0)
            current_ent = path[-1][2]
            current_low = current_ent.lower()
            if current_low == target_low and len(path) > 1:
                return [{"subject": step[0], "predicate": step[1], "object": step[2]} for step in path[1:]]

            if len(path) <= max_depth:
                for predicate, raw_next, next_ent in adj.get(current_low, []):
                    if next_ent not in visited:
                        visited.add(next_ent)
                        new_path = list(path)
                        new_path.append((current_ent, predicate, raw_next))
                        queue.append(new_path)

        return None

    def search_knowledge(self, keyword: str, limit: int = 5, active_only: bool = True) -> List[Dict[str, Any]]:
        """Searches across entities and facts matching the keyword."""
        kw = f"%{keyword.lower()}%"
        status_filter = "AND epistemic_status NOT IN ('SUPERSEDED', 'REFUTED')" if active_only else ""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT subject_name, predicate, object_name, confidence, source_ref, epistemic_status, valid_from, valid_to 
                FROM semantic_triples 
                WHERE (LOWER(subject_name) LIKE ? OR LOWER(predicate) LIKE ? OR LOWER(object_name) LIKE ?)
                  {status_filter}
                ORDER BY confidence DESC, created_at DESC
                LIMIT ?
            """, (kw, kw, kw, limit))
            return [dict(r) for r in cursor.fetchall()]
            return [dict(r) for r in cursor.fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM semantic_entities")
            total_entities = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM semantic_triples WHERE epistemic_status = 'ACTIVE'")
            active_triples = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM semantic_triples WHERE epistemic_status = 'SUPERSEDED'")
            superseded_triples = cursor.fetchone()[0]

        return {
            "total_entities": total_entities,
            "total_triples": active_triples + superseded_triples,
            "active_triples": active_triples,
            "superseded_triples": superseded_triples,
            "graph_density": round((active_triples + superseded_triples) / max(1, total_entities), 2)
        }

semantic_graph_memory = SemanticGraphMemory()
