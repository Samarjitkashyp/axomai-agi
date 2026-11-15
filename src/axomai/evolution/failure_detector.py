"""
AxomAI Evolution Engine - Autonomous Failure & Bottleneck Detector.
Scans execution telemetry, agent error logs, and latency metrics to autonomously detect
cognitive weaknesses, edge-case crashes, and optimization opportunities without user prompting.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class FailureDetector:
    """Introspective monitor for system errors, latency regressions, and cognitive anomalies."""

    def __init__(self):
        self.detected_anomalies: List[Dict[str, Any]] = []

    def inspect_execution_history(self, task_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyzes historical execution logs and flags systematic failures.
        """
        new_anomalies = []
        for record in task_records:
            had_error = record.get("had_error", False) or bool(record.get("error"))
            latency_ms = record.get("latency_ms", 0.0)
            agent_id = record.get("agent_id", "orchestrator")
            query = record.get("query", "generic_query")

            if had_error:
                anomaly = {
                    "anomaly_id": f"anom_{len(self.detected_anomalies) + 1:04d}",
                    "type": "EXECUTION_EXCEPTION",
                    "severity": "HIGH",
                    "agent_id": agent_id,
                    "target_query_pattern": query[:60],
                    "root_cause_context": record.get("error") or "Unhandled runtime exception",
                    "detected_at": datetime.now(timezone.utc).isoformat()
                }
                new_anomalies.append(anomaly)
                self.detected_anomalies.append(anomaly)

            elif latency_ms > 4000.0:  # Latency bottleneck (> 4.0s)
                anomaly = {
                    "anomaly_id": f"anom_{len(self.detected_anomalies) + 1:04d}",
                    "type": "LATENCY_BOTTLENECK",
                    "severity": "MEDIUM",
                    "agent_id": agent_id,
                    "target_query_pattern": query[:60],
                    "root_cause_context": f"Execution latency reached {latency_ms}ms (threshold 4000ms)",
                    "detected_at": datetime.now(timezone.utc).isoformat()
                }
                new_anomalies.append(anomaly)
                self.detected_anomalies.append(anomaly)

        if len(self.detected_anomalies) > 50:
            self.detected_anomalies = self.detected_anomalies[-50:]

        return new_anomalies

    def get_unresolved_weaknesses(self) -> List[Dict[str, Any]]:
        return list(self.detected_anomalies[-10:])

failure_detector = FailureDetector()

