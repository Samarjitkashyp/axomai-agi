"""
AxomAI Supervision Engine - Capability-Based Access Control (RBAC) Guard.
Enforces fine-grained cryptographic and capability token verification:
- READ: Telemetry, logs, semantic memory
- WRITE: Compiling artifacts, updating memory
- EXECUTE: Spawning sub-agents, running benchmarks, sandboxed functions
- DELETE: Cache purging, ephemeral artifact unlinking
- NETWORK: Outbound API querying, external radar scans
Prevents unauthorized actions or destructive deletions across all agent operations.
"""

import uuid
import time
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any, List, Set, Optional

class Capability(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    EXECUTE = "EXECUTE"
    DELETE = "DELETE"
    NETWORK = "NETWORK"

class CapabilityToken:
    """Security token granting bounded operational capabilities to an agent."""

    def __init__(self, agent_id: str, capabilities: Set[Capability], ttl_seconds: int = 3600):
        self.token_id = f"cap_{uuid.uuid4().hex}"
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.issued_at = time.time()
        self.expires_at = self.issued_at + ttl_seconds

    def is_valid(self) -> bool:
        return time.time() < self.expires_at

    def has_capability(self, capability: Capability) -> bool:
        return self.is_valid() and capability in self.capabilities

class CapabilityGuard:
    """Fine-grained capability verification and authorization perimeter."""

    def __init__(self):
        self._tokens: Dict[str, CapabilityToken] = {}
        self.audit_log: List[Dict[str, Any]] = []

        # Bootstrap trusted system tokens
        self.master_token = self.issue_token(
            agent_id="master_orchestrator",
            capabilities=[Capability.READ, Capability.WRITE, Capability.EXECUTE, Capability.DELETE, Capability.NETWORK],
            ttl_seconds=86400 * 365
        )
        self.janitor_token = self.issue_token(
            agent_id="system_janitor",
            capabilities=[Capability.READ, Capability.DELETE],
            ttl_seconds=86400 * 365
        )

    def issue_token(self, agent_id: str, capabilities: List[Capability], ttl_seconds: int = 3600) -> str:
        """Issues a new capability token with specific access rights."""
        token = CapabilityToken(
            agent_id=agent_id,
            capabilities=set(capabilities),
            ttl_seconds=ttl_seconds
        )
        self._tokens[token.token_id] = token
        return token.token_id

    def verify_capability(
        self,
        token_id: Optional[str],
        required_cap: Capability,
        resource_target: Optional[str] = None
    ) -> bool:
        """
        Verifies if the provided token holds the required capability.
        Logs security audit trail for every verification attempt.
        """
        now = datetime.now(timezone.utc).isoformat()
        if not token_id or token_id not in self._tokens:
            self._log_audit(token_id, "ANONYMOUS", required_cap, resource_target, granted=False, reason="INVALID_OR_MISSING_TOKEN")
            return False

        token = self._tokens[token_id]
        if not token.is_valid():
            self._log_audit(token_id, token.agent_id, required_cap, resource_target, granted=False, reason="TOKEN_EXPIRED")
            return False

        granted = token.has_capability(required_cap)
        reason = "AUTHORIZED" if granted else "CAPABILITY_DENIED"
        self._log_audit(token_id, token.agent_id, required_cap, resource_target, granted=granted, reason=reason)
        return granted

    def enforce_capability(
        self,
        token_id: Optional[str],
        required_cap: Capability,
        resource_target: Optional[str] = None
    ) -> None:
        """
        Enforces capability check; raises PermissionError on violation.
        """
        if not self.verify_capability(token_id, required_cap, resource_target):
            raise PermissionError(
                f"Security Perimeter Violation: Operation requires capability '{required_cap.value}' "
                f"for resource '{resource_target or 'system'}', but token was unauthorized or missing."
            )

    def _log_audit(self, token_id: Optional[str], agent_id: str, cap: Capability, resource: Optional[str], granted: bool, reason: str):
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "token_id": token_id or "NONE",
            "agent_id": agent_id,
            "capability": cap.value,
            "resource": resource or "GLOBAL",
            "granted": granted,
            "reason": reason
        }
        self.audit_log.append(record)
        if len(self.audit_log) > 100:
            self.audit_log.pop(0)

    def get_security_audit_log(self) -> List[Dict[str, Any]]:
        return list(self.audit_log[-20:])

capability_guard = CapabilityGuard()

