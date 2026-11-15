"""
Z9 Cortex - Long-Term Episodic Memory Store Tool.
Persists long-term conversational memory, executive decisions,
and historical milestones across sessions.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from axomai.config import settings

class MemoryStore:
    """Persistent episodic and semantic corporate memory."""

    def __init__(self):
        self.memory_file = settings.STORAGE_DIR / "cortex_memory.json"
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.memory_file.exists():
            self._init_default_memories()

    def _init_default_memories(self):
        default_memories = [
            {
                "memory_id": "mem_01",
                "category": "Corporate Policy",
                "content": "All marketing discounts above 15% require CFO sign-off.",
                "recorded_at": "2024-03-15T10:00:00Z"
            },
            {
                "memory_id": "mem_02",
                "category": "Strategic Roadmap",
                "content": "Priority 2024 focus: EV two-wheeler ecosystem expansion across Northeast India.",
                "recorded_at": "2024-06-20T14:30:00Z"
            },
            {
                "memory_id": "mem_03",
                "category": "Security Protocol",
                "content": "Z Sentinel must inspect all outgoing documents for PII and hallucination consensus before external release.",
                "recorded_at": "2024-09-01T09:15:00Z"
            }
        ]
        self._save(default_memories)

    def _load(self) -> List[Dict[str, Any]]:
        try:
            if self.memory_file.exists():
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return []

    def _save(self, memories: List[Dict[str, Any]]):
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(memories, f, indent=2)
        except Exception:
            pass

    def recall(self, query: str) -> List[Dict[str, Any]]:
        memories = self._load()
        q_words = set(query.lower().split())
        matched = []
        for m in memories:
            c_words = set(m["content"].lower().split())
            if q_words.intersection(c_words):
                matched.append(m)
        return matched if matched else memories[:3]

    def store_memory(self, content: str, category: str = "General Directive") -> Dict[str, Any]:
        memories = self._load()
        new_mem = {
            "memory_id": f"mem_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "category": category,
            "content": content,
            "recorded_at": datetime.utcnow().isoformat()
        }
        memories.append(new_mem)
        self._save(memories)
        return new_mem

memory_store = MemoryStore()

