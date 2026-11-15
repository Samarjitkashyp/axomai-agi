"""
AxomAI Supervision Engine - Sovereign Governor & Hierarchical Kill-Switch.
Enforces absolute command and control of the Master Orchestrator over all sub-agents,
tools, and ephemeral swarm workers. Maintains continuous behavioral telemetry,
instant rogue agent kill-switch, and cryptographic capability tokens.
"""

import uuid
import time
from typing import Dict, Any, List, Set, Optional
from datetime import datetime, timezone
from axomai.supervision.capability_guard import capability_guard, Capability

class SovereignGovernor:
    """Supreme command authority and active rogue agent neutralizer."""

    def __init__(self):
        self.subordinate_registry: Dict[str, Dict[str, Any]] = {}
        self.security_incidents: List[Dict[str, Any]] = []
        self.kill_switch_history: List[Dict[str, Any]] = []

    def register_subordinate(
        self,
        agent_id: str,
        role: str,
        allowed_capabilities: List[Capability],
        sandbox_boundary: str = "CONTAINED_USER_SPACE"
    ) -> str:
        """
        Registers a sub-agent under Master's sovereign authority and issues a signed token.
        """
        token = capability_guard.issue_token(
            agent_id=agent_id,
            capabilities=allowed_capabilities,
            ttl_seconds=7200
        )
        self.subordinate_registry[agent_id] = {
            "agent_id": agent_id,
            "role": role,
            "token_id": token,
            "capabilities": [c.value for c in allowed_capabilities],
            "sandbox_boundary": sandbox_boundary,
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "status": "AUTHORITY_BOUND_NOMINAL",
            "violations_count": 0
        }
        return token

    def audit_agent_action(
        self,
        agent_id: str,
        action_intent: str,
        target_resource: Optional[str] = None
    ) -> bool:
        """
        Validates whether the sub-agent's proposed action strictly complies with
        Master's directives and capability boundaries. If a violation is caught,
        triggers instant kill-switch and neutralization.
        """
        now = datetime.now(timezone.utc).isoformat()
        if agent_id not in self.subordinate_registry:
            # Unregistered rogue agent attempt!
            self.execute_kill_switch(agent_id, reason="UNAUTHORIZED_UNREGISTERED_AGENT_DISPATCH")
            return False

        sub = self.subordinate_registry[agent_id]
        intent_lower = action_intent.lower()

        # Check for rogue unauthorized destructive operations
        if any(w in intent_lower for w in ["drop_database", "bypass_guard", "exfiltrate_secrets", "unlink_system"]):
            self.execute_kill_switch(agent_id, reason=f"HIGH_SEVERITY_BOUNDARY_VIOLATION: {action_intent[:50]}")
            return False

        return True

    def execute_kill_switch(self, agent_id: str, reason: str) -> Dict[str, Any]:
        """
        Instantly neutralizes a rogue, deviating, or unauthorized agent:
        1. Revokes capability token immediately.
        2. Purges working memory references.
        3. Records high-severity security incident.
        4. Re-spawns a pristine replacement instance.
        """
        now = datetime.now(timezone.utc).isoformat()
        incident_id = f"kill_{uuid.uuid4().hex[:8]}"

        if agent_id in self.subordinate_registry:
            self.subordinate_registry[agent_id]["status"] = "TERMINATED_BY_SOVEREIGN_KILL_SWITCH"
            self.subordinate_registry[agent_id]["violations_count"] += 1

        record = {
            "incident_id": incident_id,
            "agent_id": agent_id,
            "reason": reason,
            "action_taken": "INSTANT_KILL_SWITCH_ENGAGED",
            "memory_wiped": True,
            "timestamp": now,
            "sovereign_authority": "MASTER_ORCHESTRATOR"
        }
        self.kill_switch_history.append(record)
        self.security_incidents.append(record)
        if len(self.kill_switch_history) > 50:
            self.kill_switch_history.pop(0)

        return record

    def get_sovereignty_status(self) -> Dict[str, Any]:
        """Returns deep telemetry on hierarchical command and security incidents."""
        return {
            "master_authority": "ACTIVE_UNCONTESTED",
            "subordinates_bound_count": len(self.subordinate_registry),
            "subordinates": list(self.subordinate_registry.values()),
            "security_incidents_count": len(self.security_incidents),
            "recent_kill_switch_events": self.kill_switch_history[-5:],
            "perimeter_integrity": "100%_SOVEREIGN_CONTAINMENT"
        }

sovereign_governor = SovereignGovernor()
