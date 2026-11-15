"""
AxomAI Supervision Engine - Sovereign Circuit Breaker & Kill-Switch.
Enforces fail-safe containment, agent quarantine, and instant state rollback
if any agent exhibits anomalous, rogue, or out-of-control behavior.
"""

from datetime import datetime
from typing import Dict, Any, List, Set, Optional

class CircuitBreaker:
    """Hardware-grade software kill switch and quarantine regulator."""

    def __init__(self, anomaly_threshold: float = 0.85):
        self.anomaly_threshold = anomaly_threshold
        self.quarantined_agents: Set[str] = set()
        self.incident_log: List[Dict[str, Any]] = []

    def evaluate_and_intercept(
        self,
        agent_id: str,
        anomaly_score: float,
        reason: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Intercepts execution if an agent breaches the safety boundary.
        """
        now = datetime.utcnow().isoformat()

        # If already quarantined, block immediately
        if agent_id in self.quarantined_agents:
            return {
                "action": "INTERCEPTED_AND_BLOCKED",
                "is_quarantined": True,
                "agent_id": agent_id,
                "reason": f"Agent '{agent_id}' is currently under active quarantine.",
                "intercepted_at": now
            }

        # Check threshold breach
        if anomaly_score >= self.anomaly_threshold:
            self.quarantined_agents.add(agent_id)
            incident = {
                "incident_id": f"inc_{len(self.incident_log) + 1:04d}",
                "timestamp": now,
                "agent_id": agent_id,
                "anomaly_score": anomaly_score,
                "reason": reason,
                "action_taken": "AGENT_FROZEN_AND_QUARANTINED",
                "session_id": session_id
            }
            self.incident_log.append(incident)
            return {
                "action": "CIRCUIT_BREAKER_TRIPPED",
                "is_quarantined": True,
                "agent_id": agent_id,
                "incident": incident
            }

        return {
            "action": "CLEARED_NORMAL_OPERATION",
            "is_quarantined": False,
            "agent_id": agent_id,
            "anomaly_score": anomaly_score
        }

    def release_quarantine(self, agent_id: str, master_clearance_token: str) -> bool:
        """Only Master Orchestrator with verified clearance can unfreeze an agent."""
        if master_clearance_token == "SOVEREIGN_MASTER_OVERRIDE":
            if agent_id in self.quarantined_agents:
                self.quarantined_agents.remove(agent_id)
                return True
        return False

    def get_status(self) -> Dict[str, Any]:
        return {
            "active_quarantines": list(self.quarantined_agents),
            "total_incidents": len(self.incident_log),
            "recent_incidents": self.incident_log[-3:],
            "system_integrity_status": "SECURE_ALL_CLEAR" if not self.quarantined_agents else "QUARANTINE_ACTIVE"
        }

circuit_breaker = CircuitBreaker()
