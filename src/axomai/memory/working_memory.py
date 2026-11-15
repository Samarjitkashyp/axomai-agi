"""
AxomAI Cognitive Memory Engine - Tier 1: Working Memory (Short-Term & Scratchpad).
Maintains active conversation context, intermediate reasoning scratchpads,
cognitive load indexing, and rolling short-term synthesis.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import json

class WorkingMemory:
    """Active conversational and scratchpad working memory."""

    def __init__(self, max_context_items: int = 25):
        self.max_context_items = max_context_items
        self.scratchpad: Dict[str, Any] = {}
        self.conversation_buffer: List[Dict[str, Any]] = []
        self.active_session_id: Optional[str] = None
        self.cognitive_load: float = 0.0

    def start_session(self, session_id: str):
        self.active_session_id = session_id
        self.conversation_buffer = []
        self.scratchpad = {}
        self.cognitive_load = 0.1

    def push_turn(self, role: str, content: str, agent_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        turn = {
            "timestamp": datetime.utcnow().isoformat(),
            "role": role,
            "content": content,
            "agent_id": agent_id or "user",
            "metadata": metadata or {}
        }
        self.conversation_buffer.append(turn)
        if len(self.conversation_buffer) > self.max_context_items:
            self.conversation_buffer.pop(0)
        self._update_cognitive_load()

    def set_scratchpad(self, key: str, value: Any):
        self.scratchpad[key] = {
            "value": value,
            "updated_at": datetime.utcnow().isoformat()
        }
        self._update_cognitive_load()

    def get_scratchpad(self, key: str, default: Any = None) -> Any:
        entry = self.scratchpad.get(key)
        if entry:
            return entry.get("value", default)
        return default

    def get_context_snapshot(self) -> Dict[str, Any]:
        return {
            "session_id": self.active_session_id,
            "buffer_depth": len(self.conversation_buffer),
            "cognitive_load_score": round(self.cognitive_load, 3),
            "recent_turns": self.conversation_buffer[-5:],
            "active_scratchpad_keys": list(self.scratchpad.keys())
        }

    def _update_cognitive_load(self):
        # Cognitive load estimated by buffer size + scratchpad depth
        load = (len(self.conversation_buffer) / self.max_context_items) * 0.6 + (len(self.scratchpad) / 20.0) * 0.4
        self.cognitive_load = min(1.0, max(0.05, load))

    def clear(self):
        self.conversation_buffer.clear()
        self.scratchpad.clear()
        self.cognitive_load = 0.0

working_memory = WorkingMemory()

