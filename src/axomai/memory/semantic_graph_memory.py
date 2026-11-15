"""
AxomAI Cognitive Memory Engine - Tier 3: Semantic Knowledge Graph Memory.
Maintains persistent entity-relation knowledge graph, ontological triples (Subject-Predicate-Object),
and multi-hop relational pathfinding across corporate, economic, and geopolitical domains.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from axomai.config import settings

class SemanticGraphMemory:
    """Persistent entity-relation graph and universal semantic memory."""

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
                    UNIQUE(subject_name, predicate, object_name)
                )
            """)
            conn.commit()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM semantic_entities")
            if cursor.fetchone()[0] == 0:
                self._seed_default_graph(conn)

    def _seed_default_graph(self, conn):
        now = datetime.utcnow().isoformat()
        entities = [
            ("ent_assam_tea", "Orthodox Tea", "COMMODITY", json.dumps({"origin": "Upper Assam", "hscode": "090210", "grade": "FTGFOP1"})),
            ("ent_hamburg", "Port of Hamburg", "LOCATION", json.dumps({"country": "Germany", "type": "Maritime Terminal", "eu_entry": True})),
            ("ent_siliguri", "Siliguri Corridor", "CHOKEPOINT", json.dumps({"width_km": 22, "strategic_significance": "Northeast Lifeline"})),
            ("ent_changsari", "Changsari Logistics Hub", "INFRASTRUCTURE", json.dumps({"storage_sqft": 150000, "buffer_role": "High-velocity Railhead"})),
            ("ent_solar_ppa", "Solar Rooftop PPA", "ENERGY_CONTRACT", json.dumps({"fixed_tariff": 4.45, "discom": "APDCL", "vcs_verified": True})),
            ("ent_fidic_20", "FIDIC Clause 20.1", "LEGAL_PROTOCOL", json.dumps({"notice_window_days": 28, "jurisdiction": "International EPC"}))
        ]
        conn.executemany("""
            INSERT OR IGNORE INTO semantic_entities (entity_id, entity_name, entity_type, attributes_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [(e[0], e[1], e[2], e[3], now, now) for e in entities])

        triples = [
            ("Orthodox Tea", "EXPORTS_TO", "Port of Hamburg", 0.99, "Commerce Ministry Data"),
            ("Orthodox Tea", "TRANSITS_THROUGH", "Changsari Logistics Hub", 0.98, "Multimodal Freight Radar"),
            ("Changsari Logistics Hub", "BYPASSES_CHOKEPOINT", "Siliguri Corridor", 0.95, "Z10 Contingency Route"),
            ("Solar Rooftop PPA", "OFFSETS_GRID_COST_FROM", "Changsari Logistics Hub", 0.96, "Y2 Energy Audit"),
            ("FIDIC Clause 20.1", "PROTECTS_DISPUTES_FOR", "Changsari Logistics Hub", 0.99, "Y4 Civil Audit")
        ]
        conn.executemany("""
            INSERT OR IGNORE INTO semantic_triples (subject_name, predicate, object_name, confidence, source_ref, verified, created_at)
            VALUES (?, ?, ?, ?, ?, 1, ?)
        """, [(t[0], t[1], t[2], t[3], t[4], now) for t in triples])
        conn.commit()

    def add_entity(self, name: str, entity_type: str, attributes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        entity_id = f"ent_{abs(hash(name.lower())) % 1000000:06d}"
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO semantic_entities (entity_id, entity_name, entity_type, attributes_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(entity_name) DO UPDATE SET
                    entity_type = excluded.entity_type,
                    attributes_json = excluded.attributes_json,
                    updated_at = excluded.updated_at
            """, (entity_id, name, entity_type, json.dumps(attributes or {}), now, now))
            conn.commit()
        return {"entity_id": entity_id, "name": name, "type": entity_type}

    def add_fact(
        self,
        subject: str,
        predicate: str,
        obj: str,
        confidence: float = 1.0,
        source_ref: str = "Autonomous Ingestion"
    ) -> Dict[str, Any]:
        """Inserts an ontological fact triple."""
        now = datetime.utcnow().isoformat()
        # Ensure entities exist
        self.add_entity(subject, "UNKNOWN_CONCEPT")
        self.add_entity(obj, "UNKNOWN_CONCEPT")

        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO semantic_triples 
                (subject_name, predicate, object_name, confidence, source_ref, verified, created_at)
                VALUES (?, ?, ?, ?, ?, 1, ?)
            """, (subject, predicate.upper().replace(" ", "_"), obj, float(confidence), source_ref, now))
            conn.commit()

        return {
            "subject": subject,
            "predicate": predicate,
            "object": obj,
            "confidence": confidence,
            "status": "STORED"
        }

    def query_entity_subgraph(self, entity_name: str) -> Dict[str, Any]:
        """Retrieves an entity and all its direct 1-hop inbound and outbound relations."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM semantic_entities WHERE LOWER(entity_name) = LOWER(?)", (entity_name,))
            ent_row = cursor.fetchone()
            
            # Outbound relations
            cursor.execute("SELECT * FROM semantic_triples WHERE LOWER(subject_name) = LOWER(?)", (entity_name,))
            outbound = [dict(r) for r in cursor.fetchall()]

            # Inbound relations
            cursor.execute("SELECT * FROM semantic_triples WHERE LOWER(object_name) = LOWER(?)", (entity_name,))
            inbound = [dict(r) for r in cursor.fetchall()]

        if not ent_row and not outbound and not inbound:
            return {"entity": entity_name, "found": False}

        return {
            "entity": entity_name,
            "found": True,
            "type": ent_row["entity_type"] if ent_row else "DYNAMIC",
            "attributes": json.loads(ent_row["attributes_json"]) if ent_row and ent_row["attributes_json"] else {},
            "outbound_relations": outbound,
            "inbound_relations": inbound
        }

    def find_multi_hop_path(self, start_entity: str, target_entity: str, max_depth: int = 3) -> Optional[List[Dict[str, Any]]]:
        """Discovers relational reasoning paths connecting two concepts."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT subject_name, predicate, object_name FROM semantic_triples")
            edges = cursor.fetchall()

        # Build adjacency graph
        adj: Dict[str, List[tuple]] = {}
        for edge in edges:
            s, p, o = edge["subject_name"].lower(), edge["predicate"], edge["object_name"].lower()
            if s not in adj: adj[s] = []
            adj[s].append((p, edge["object_name"], o))

        # BFS for shortest path
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

    def search_knowledge(self, keyword: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Searches across entities and facts matching the keyword."""
        kw = f"%{keyword.lower()}%"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT subject_name, predicate, object_name, confidence, source_ref 
                FROM semantic_triples 
                WHERE LOWER(subject_name) LIKE ? OR LOWER(predicate) LIKE ? OR LOWER(object_name) LIKE ?
                LIMIT ?
            """, (kw, kw, kw, limit))
            return [dict(r) for r in cursor.fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM semantic_entities")
            total_entities = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM semantic_triples")
            total_triples = cursor.fetchone()[0]

        return {
            "total_entities": total_entities,
            "total_triples": total_triples,
            "graph_density": round(total_triples / max(1, total_entities), 2)
        }

semantic_graph_memory = SemanticGraphMemory()
