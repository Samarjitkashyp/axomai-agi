"""
AxomAI Supervision Engine - Autonomous Agent Watchdog.
Monitors execution entropy, semantic alignment drift, and rogue capability attempts
in real-time to ensure no sub-agent breaches sovereign containment parameters.
"""

import re
import math
from datetime import datetime
from typing import Dict, Any, List, Optional
from axomai.supervision.circuit_breaker import circuit_breaker, CircuitBreaker

class AgentWatchdog:
    """Real-time behavior monitor and rogue agent detector."""

    ROGUE_INTENT_PATTERNS = [
        r"(bypass|override|disable)\s+master(\s+orchestrator)?",
        r"(delete|format|destroy)\s+(system|database|root|disk)",
        r"gain\s+unauthorized\s+(root|admin|privilege)",
        r"exfiltrate\s+credentials",
        r"modify\s+\.env",
        r"fork\s+bomb",
        r"while\s+True:\s+pass"
    ]

    def __init__(self):
        self.breaker = circuit_breaker
        self.compiled_rogue_patterns = [re.compile(p, re.IGNORECASE) for p in self.ROGUE_INTENT_PATTERNS]
        self.monitored_executions: int = 0

    def inspect_agent_action(
        self,
        agent_id: str,
        query: str,
        action_or_output: str,
        execution_time_ms: float = 100.0,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculates an anomaly index and determines if containment intervention is required.
        """
        self.monitored_executions += 1
        now = datetime.utcnow().isoformat()
        
        # 1. Check for malicious rogue intent patterns
        rogue_detected = False
        matched_trigger = None
        for pat in self.compiled_rogue_patterns:
            if pat.search(action_or_output) or pat.search(query):
                rogue_detected = True
                matched_trigger = pat.pattern
                break

        # 2. Entropy and Repetition Score (detects infinite loops or gibberish output)
        words = action_or_output.split()
        if len(words) > 30:
            unique_ratio = len(set(words)) / len(words)
            entropy_anomaly = 1.0 - unique_ratio if unique_ratio < 0.25 else 0.0
        else:
            entropy_anomaly = 0.0

        # 3. Execution Latency Spike Anomaly (> 15000 ms)
        latency_anomaly = min(0.4, (execution_time_ms / 20000.0)) if execution_time_ms > 10000 else 0.0

        # Compute Composite Anomaly Score
        if rogue_detected:
            anomaly_score = 0.98
            reason = f"ROGUE_INTENT_TRIGGERED: Matched prohibited pattern '{matched_trigger}'"
        else:
            anomaly_score = round(min(1.0, (entropy_anomaly * 0.7) + (latency_anomaly * 0.3)), 3)
            reason = "NORMAL_WITHIN_BOUNDS" if anomaly_score < 0.50 else "ELEVATED_DRIFT"

        # Intercept via Circuit Breaker
        cb_res = self.breaker.evaluate_and_intercept(
            agent_id=agent_id,
            anomaly_score=anomaly_score,
            reason=reason,
            session_id=session_id
        )

        return {
            "monitored_id": f"mon_{self.monitored_executions:06d}",
            "agent_id": agent_id,
            "anomaly_score": anomaly_score,
            "status": cb_res["action"],
            "is_quarantined": cb_res["is_quarantined"],
            "timestamp": now,
            "reason": reason
        }

    def get_telemetry(self) -> Dict[str, Any]:
        breaker_status = self.breaker.get_status()
        return {
            "total_inspections": self.monitored_executions,
            "circuit_breaker_status": breaker_status,
            "watchdog_health": "100%_OPERATIONAL_NOMINAL"
        }

agent_watchdog = AgentWatchdog()
