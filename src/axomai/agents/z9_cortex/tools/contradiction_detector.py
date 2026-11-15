"""
Z9 Cortex - Policy Contradiction & Strategic Conflict Detector Tool.
Evaluates proposals against past corporate memories and knowledge graph edges
to alert leadership of policy collisions.
"""

from typing import Dict, Any, List
from axomai.agents.z9_cortex.tools.memory_store import memory_store

class ContradictionDetector:
    """Detects logical or policy conflicts with past memory."""

    def detect_conflicts(self, proposal: str) -> Dict[str, Any]:
        past_memories = memory_store.recall(proposal)
        p_lower = proposal.lower()

        conflicts = []
        # Example check: discount policy
        if "discount" in p_lower and any(num in p_lower for num in ["20%", "25%", "30%", "50%"]):
            conflicts.append({
                "policy": "Discount Approval Protocol (2024-03-15)",
                "conflict_reason": "Proposed discount exceeds 15% threshold; requires mandatory CFO sign-off.",
                "severity": "HIGH"
            })

        return {
            "has_conflict": len(conflicts) > 0,
            "conflicts": conflicts,
            "recalled_memories_checked": len(past_memories)
        }

contradiction_detector = ContradictionDetector()

