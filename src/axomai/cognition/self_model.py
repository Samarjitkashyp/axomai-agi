"""
AxomAI Cognition Engine - Self-Model (Introspective Self-Awareness).
Maintains a living, machine-readable model of the AGI's own identity, version,
operational boundaries, active capabilities, hardware resources, confidence calibration,
known failure modes, and current learning targets.
"""

import time
import platform
import psutil
from datetime import datetime, timezone
from typing import Dict, Any, List, Set, Optional, Tuple
from axomai.config import settings

class SelfModel:
    """Introspective self-awareness model for AxomAI-AGI."""

    def __init__(self):
        self.identity = "AxomAI Hyperion"
        self.version = "v4.0.0-AGI-CognitiveCore"
        self.architecture = "Hierarchical Cognitive Multi-Agent AGI with Autonomous Self-Evolution"
        self.boot_time = datetime.now(timezone.utc).isoformat()
        
        # Native capabilities registered in the system
        self._capabilities: Set[str] = {
            "multi_hop_deductive_reasoning",
            "quantitative_financial_engineering",
            "geotechnical_hydrology_modeling",
            "cross_domain_swarm_orchestration",
            "episodic_semantic_memory_recall",
            "ast_code_profiling_and_hot_patching",
            "proactive_environmental_perception",
            "capability_token_rbac_governance",
            "autonomous_benchmark_evaluation",
            "document_vision_ocr_multimodal",
            "vector_semantic_search",
            "zero_cost_collar_hedging",
            "sql_relational_synthesis"
        }

        # Explicitly declared operational boundaries and limitations
        self._limitations: List[str] = [
            "No direct physical actuation in kinetic real world without robotics interface",
            "No raw destructive filesystem operations without verified DELETE capability token",
            "Cannot bypass cryptographic Zero-Trust RBAC boundaries",
            "Sandboxed code execution enforces strict module whitelist (no arbitrary os.system)"
        ]

        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.known_failure_modes: List[Dict[str, Any]] = []
        self.learning_targets: List[Dict[str, Any]] = []
        self.confidence_calibration: Dict[str, float] = {
            "mathematical_computation": 0.99,
            "geotechnical_analysis": 0.96,
            "financial_fx_hedging": 0.97,
            "cross_modal_orchestration": 0.95,
            "code_hot_patching": 0.93,
            "unseen_domain_synthesis": 0.88
        }
        # Longitudinal performance telemetry across domains (updated dynamically at runtime)
        self.performance_stats: Dict[str, Dict[str, Any]] = {
            "python_coding": {"success": 0, "total": 0, "total_latency_sec": 0.0},
            "web_research": {"success": 0, "total": 0, "total_latency_sec": 0.0},
            "document_vision": {"success": 0, "total": 0, "total_latency_sec": 0.0},
            "tool_generation": {"success": 0, "total": 0, "total_latency_sec": 0.0},
            "quantitative_math": {"success": 0, "total": 0, "total_latency_sec": 0.0}
        }

    def can_execute_task(self, required_capabilities: List[str]) -> Tuple[bool, List[str]]:
        """
        Introspects whether the AI natively possesses the capabilities required for a task.
        Returns (has_all_capabilities, list_of_missing_capabilities).
        """
        missing = [cap for cap in required_capabilities if cap not in self._capabilities]
        return len(missing) == 0, missing

    def register_capability(self, capability_name: str, source: str = "AUTONOMOUS_ACQUISITION") -> None:
        """Dynamically registers a newly synthesized or acquired capability into the self-model."""
        self._capabilities.add(capability_name)
        now = datetime.now(timezone.utc).isoformat()
        self.learning_targets.append({
            "target": capability_name,
            "status": "ACQUIRED_AND_OPERATIONAL",
            "acquired_via": source,
            "timestamp": now
        })

    def record_execution(self, domain: str, success: bool, latency_sec: float) -> None:
        """Records an execution outcome into longitudinal performance stats."""
        if domain not in self.performance_stats:
            self.performance_stats[domain] = {"success": 0, "total": 0, "total_latency_sec": 0.0}
        st = self.performance_stats[domain]
        st["total"] += 1
        if success:
            st["success"] += 1
        st["total_latency_sec"] += latency_sec

    def get_performance_profile(self) -> Dict[str, Any]:
        """Calculates empirical accuracy, latency, and identifies weakest capability."""
        profile = {}
        weakest_domain = None
        lowest_acc = 101.0

        for dom, st in self.performance_stats.items():
            tot = st["total"]
            acc = round((st["success"] / tot) * 100, 2) if tot > 0 else 0.0
            avg_lat = round(st["total_latency_sec"] / tot, 2) if tot > 0 else 0.0
            profile[dom] = {
                "accuracy_pct": acc,
                "average_latency_sec": avg_lat,
                "total_runs": tot
            }
            if acc < lowest_acc:
                lowest_acc = acc
                weakest_domain = dom

        return {
            "domains": profile,
            "weakest_capability": weakest_domain,
            "lowest_accuracy_pct": lowest_acc
        }

    def record_failure_mode(self, domain: str, error_context: str, mitigation: str) -> None:
        """Records an introspective failure observation to avoid repeating mistakes."""
        self.known_failure_modes.append({
            "domain": domain,
            "context": error_context,
            "mitigation": mitigation,
            "detected_at": datetime.now(timezone.utc).isoformat()
        })
        if len(self.known_failure_modes) > 20:
            self.known_failure_modes.pop(0)

    def get_hardware_telemetry(self) -> Dict[str, Any]:
        """Reads real-time compute resources."""
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        return {
            "os": f"{platform.system()} {platform.release()}",
            "cpu_utilization_pct": cpu,
            "ram_used_gb": round(mem.used / (1024**3), 2),
            "ram_total_gb": round(mem.total / (1024**3), 2),
            "ram_percent": mem.percent
        }

    def get_self_state(self) -> Dict[str, Any]:
        """Provides full introspective state of the AGI core."""
        return {
            "identity": self.identity,
            "version": self.version,
            "architecture": self.architecture,
            "boot_time": self.boot_time,
            "capabilities_count": len(self._capabilities),
            "capabilities": sorted(list(self._capabilities)),
            "limitations": self._limitations,
            "active_tasks_count": len(self.active_tasks),
            "active_tasks": list(self.active_tasks.values()),
            "known_failures_count": len(self.known_failure_modes),
            "known_failures": self.known_failure_modes[-5:],
            "confidence_calibration": self.confidence_calibration,
            "performance_profile": self.get_performance_profile(),
            "learning_targets": self.learning_targets[-5:],
            "hardware_vitals": self.get_hardware_telemetry(),
            "status": "COGNITIVE_EQUILIBRIUM"
        }

self_model = SelfModel()

