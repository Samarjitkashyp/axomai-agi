"""
AxomAI Agency - Human-in-the-Loop Security Gate Protocol.
Safely detects and handles human verification gates (2FA OTP, SMS challenge, anti-bot challenge):
When a security barrier is detected, the AGI halts autonomous progress, engages a sovereign pause,
dispatches an interactive alert to the user on the Holographic HUD, and awaits authorized human verification.
"""

import uuid
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class SecurityGateEvent:
    """An event representing an encounter with an authentication gate requiring human authorization."""

    def __init__(
        self,
        gate_id: str,
        service_target: str,
        gate_type: str,  # 2FA_OTP, AUTH_CHALLENGE, SMS_VERIFICATION, HUMAN_CONFIRMATION
        prompt_message: str
    ):
        self.gate_id = gate_id
        self.service_target = service_target
        self.gate_type = gate_type
        self.prompt_message = prompt_message
        self.status = "PAUSED_WAITING_HUMAN_APPROVAL"
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.resolved_at: Optional[str] = None
        self.resolution_data: Optional[Dict[str, Any]] = None

    def resolve(self, auth_token_or_confirmation: Optional[str] = None) -> None:
        self.status = "APPROVED_BY_USER_RESUMED"
        self.resolved_at = datetime.now(timezone.utc).isoformat()
        self.resolution_data = {
            "token_provided": bool(auth_token_or_confirmation),
            "resolved_at": self.resolved_at
        }

class SecurityGateProtocol:
    """Manages safe, compliant Human-in-the-Loop authentication pause and resume workflows."""

    def __init__(self):
        self.active_gates: Dict[str, SecurityGateEvent] = {}
        self.gate_history: List[Dict[str, Any]] = []

    def inspect_response_for_security_gate(
        self,
        response_text: str,
        service_target: str
    ) -> Optional[SecurityGateEvent]:
        """
        Inspects web response HTML/headers for 2FA or security verification barriers.
        If found, immediately creates a gate and puts execution in safe pause.
        """
        text_lower = response_text.lower()
        gate_type = None

        if any(w in text_lower for w in ["enter otp", "two-factor", "2fa code", "authenticator app", "sms verification"]):
            gate_type = "2FA_OTP_VERIFICATION"
        elif any(w in text_lower for w in ["captcha", "verify you are human", "cf-turnstile", "recaptcha"]):
            gate_type = "HUMAN_VERIFICATION_GATE"

        if gate_type:
            gate_id = f"gate_{uuid.uuid4().hex[:8]}"
            event = SecurityGateEvent(
                gate_id=gate_id,
                service_target=service_target,
                gate_type=gate_type,
                prompt_message=(
                    f"Human Authorization Required on '{service_target}'. "
                    f"Please confirm verification or provide OTP code to authorize AGI progression."
                )
            )
            self.active_gates[gate_id] = event
            self._log_history(event)
            return event

        return None

    def approve_and_resume_gate(
        self,
        gate_id: str,
        auth_token_or_confirmation: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes human approval and signals AGI task resumption.
        """
        if gate_id not in self.active_gates:
            return {
                "gate_id": gate_id,
                "status": "NOT_FOUND_OR_ALREADY_RESOLVED",
                "resumed": False
            }

        event = self.active_gates.pop(gate_id)
        event.resolve(auth_token_or_confirmation)
        self._log_history(event)

        return {
            "gate_id": gate_id,
            "status": "GATE_RESOLVED_MISSION_RESUMED",
            "service_target": event.service_target,
            "resumed": True,
            "timestamp": event.resolved_at
        }

    def _log_history(self, event: SecurityGateEvent) -> None:
        record = {
            "gate_id": event.gate_id,
            "service_target": event.service_target,
            "gate_type": event.gate_type,
            "status": event.status,
            "prompt_message": event.prompt_message,
            "created_at": event.created_at,
            "resolved_at": event.resolved_at
        }
        self.gate_history.append(record)
        if len(self.gate_history) > 30:
            self.gate_history.pop(0)

    def get_pending_gates(self) -> List[Dict[str, Any]]:
        return [
            {
                "gate_id": e.gate_id,
                "service": e.service_target,
                "type": e.gate_type,
                "message": e.prompt_message,
                "status": e.status,
                "created_at": e.created_at
            }
            for e in self.active_gates.values()
        ]

security_gate_protocol = SecurityGateProtocol()
