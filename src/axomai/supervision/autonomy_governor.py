"""
AxomAI Supervision Engine - Autonomy Governor (Blast Radius & Action Safety).
Classifies and governs autonomous actions based on:
- Blast radius (Contained vs System-wide)
- Reversibility (Rollback supported vs Irreversible)
- Environmental impact (Read-only vs Mutation vs Deletion)
Enforces granular Zero-Trust autonomous execution without granting unrestricted destructive authority.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class AutonomyTier:
    AUTONOMOUS_APPROVED = "AUTONOMOUS_APPROVED"
    HUMAN_CONSENT_REQUIRED = "HUMAN_CONSENT_REQUIRED"
    BLOCKED_UNSAFE = "BLOCKED_UNSAFE"

class AutonomyGovernor:
    """Evaluates proposed autonomous actions against enterprise risk boundaries."""

    # Disallowed irreversible or destructive keywords requiring human consent
    HUMAN_GATE_ACTIONS = {
        "drop_table", "truncate_table", "delete_database", "format_disk",
        "revoke_admin_token", "wipe_vault", "purge_all_memory", "deploy_production_cluster"
    }

    # Banned malware / destructive signatures
    BLOCKED_SIGNATURES = {
        "os.system", "rm -rf /", "mkfs", "dd if=", ":(){ :|:& };:", "chmod -R 777 /"
    }

    def __init__(self):
        self.governance_history: List[Dict[str, Any]] = []

    def evaluate_action(
        self,
        action_name: str,
        target_resource: str,
        blast_radius: str = "CONTAINED_LOCAL",
        reversibility: str = "ROLLBACK_SUPPORTED"
    ) -> Dict[str, Any]:
        """
        Evaluates an action and returns the governing verdict:
        - AUTONOMOUS_APPROVED: AI can proceed autonomously.
        - HUMAN_CONSENT_REQUIRED: Action requires explicit user approval before execution.
        - BLOCKED_UNSAFE: Critical security violation, strictly prohibited.
        """
        now = datetime.now(timezone.utc).isoformat()
        act_lower = action_name.lower()
        res_lower = target_resource.lower()

        # 1. Critical Exploit Check
        for sig in self.BLOCKED_SIGNATURES:
            if sig in act_lower or sig in res_lower:
                verdict = {
                    "tier": AutonomyTier.BLOCKED_UNSAFE,
                    "action": action_name,
                    "target_resource": target_resource,
                    "reason": f"Disallowed exploit signature detected: '{sig}'.",
                    "timestamp": now
                }
                self.governance_history.append(verdict)
                return verdict

        # 2. High Blast Radius / Irreversible Check -> Human Gate
        if any(h in act_lower for h in self.HUMAN_GATE_ACTIONS) or reversibility == "IRREVERSIBLE" or blast_radius == "SYSTEM_WIDE":
            verdict = {
                "tier": AutonomyTier.HUMAN_CONSENT_REQUIRED,
                "action": action_name,
                "target_resource": target_resource,
                "blast_radius": blast_radius,
                "reversibility": reversibility,
                "reason": "Action carries high blast radius or is irreversible. Sovereign policy requires human confirmation gate.",
                "timestamp": now
            }
            self.governance_history.append(verdict)
            return verdict

        # 3. Contained / Reversible Operations -> Autonomous Approval
        verdict = {
            "tier": AutonomyTier.AUTONOMOUS_APPROVED,
            "action": action_name,
            "target_resource": target_resource,
            "blast_radius": blast_radius,
            "reversibility": reversibility,
            "reason": "Action is contained within safe sandbox parameters with full rollback support.",
            "timestamp": now
        }
        self.governance_history.append(verdict)
        return verdict

autonomy_governor = AutonomyGovernor()
