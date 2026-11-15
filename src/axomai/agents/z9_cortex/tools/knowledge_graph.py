"""
Z9 Cortex - Enterprise Knowledge Graph Engine Tool.
Builds, traverses, and queries entity-relationship networks using NetworkX.
Connects people, products, vendors, metrics, and past decisions into a unified graph.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import networkx as nx
from axomai.config import settings

class KnowledgeGraphEngine:
    """Enterprise semantic entity-relationship graph."""

    def __init__(self):
        self.graph = nx.DiGraph()
        self.graph_file = settings.STORAGE_DIR / "cortex_graph.json"
        self.graph_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_or_seed()

    def _load_or_seed(self):
        if self.graph_file.exists():
            try:
                with open(self.graph_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for n in data.get("nodes", []):
                        self.graph.add_node(n["id"], **n.get("attrs", {}))
                    for e in data.get("edges", []):
                        self.graph.add_edge(e["source"], e["target"], relation=e.get("relation", "RELATES_TO"))
                return
            except Exception:
                pass

        # Seed baseline enterprise knowledge graph
        triplets = [
            ("AxomAI AGI", "DEPLOYED_FOR", "Enterprise Intelligence"),
            ("AxomAI AGI", "PROTECTED_BY", "Z Sentinel"),
            ("Z1 Alpha", "SPECIALIZES_IN", "Multimodal Document Intelligence"),
            ("Z2 Bravo", "SPECIALIZES_IN", "Live Web & Competitor Radar"),
            ("Z3 Echo", "SPECIALIZES_IN", "Relational SQL & Predictive Analytics"),
            ("Z4 Nexus", "SPECIALIZES_IN", "Code Execution & API Integration"),
            ("Z5 Chronos", "SPECIALIZES_IN", "Autonomous Cron & Watchdog Alerts"),
            ("Z6 Hermes", "SPECIALIZES_IN", "Voice & Omnichannel Dispatch"),
            ("Z7 Visionary", "SPECIALIZES_IN", "PowerPoint Decks & Generative UI"),
            ("Z8 Apex", "SPECIALIZES_IN", "Contract Redlining & Compliance"),
            ("Z9 Cortex", "SPECIALIZES_IN", "Long-Term Memory & Knowledge Graph"),
            ("EV Scooter Campaign", "COMPETES_WITH", "Ola Electric"),
            ("EV Scooter Campaign", "COMPETES_WITH", "Ather Energy"),
            ("AI Chip Market", "DOMINATED_BY", "NVIDIA"),
            ("Enterprise SQL Warehouse", "GOVERNED_BY", "DPDP Act 2023")
        ]
        for src, rel, tgt in triplets:
            self.graph.add_edge(src, tgt, relation=rel)

        self._save_graph()

    def _save_graph(self):
        try:
            nodes = [{"id": n, "attrs": self.graph.nodes[n]} for n in self.graph.nodes]
            edges = [{"source": u, "target": v, "relation": self.graph.edges[u, v].get("relation", "")} for u, v in self.graph.edges]
            with open(self.graph_file, "w", encoding="utf-8") as f:
                json.dump({"nodes": nodes, "edges": edges}, f, indent=2)
        except Exception:
            pass

    def query_subgraph(self, entity_or_topic: str) -> Dict[str, Any]:
        """Finds related entities and paths connected to the given query."""
        matched_nodes = [n for n in self.graph.nodes if entity_or_topic.lower() in n.lower()]
        if not matched_nodes:
            matched_nodes = list(self.graph.nodes)[:6]

        sub_edges = []
        for n in matched_nodes:
            # Outgoing
            for succ in self.graph.successors(n):
                rel = self.graph.edges[n, succ].get("relation", "CONNECTED_TO")
                sub_edges.append({"source": n, "relation": rel, "target": succ})
            # Incoming
            for pred in self.graph.predecessors(n):
                rel = self.graph.edges[pred, n].get("relation", "CONNECTED_TO")
                sub_edges.append({"source": pred, "relation": rel, "target": n})

        return {
            "queried_entity": entity_or_topic,
            "matched_nodes": matched_nodes,
            "relationships": sub_edges[:15],
            "total_graph_nodes": self.graph.number_of_nodes(),
            "total_graph_edges": self.graph.number_of_edges()
        }

knowledge_graph = KnowledgeGraphEngine()

