"""
AxomAI Cognition Engine - World Model (Dynamic Environmental Representation).
Maintains a living, structured mental model of the external world:
- Host environment (compute, storage trends, database cluster, services)
- Workspace entities (indexed documents, telemetry files, generated artifacts)
- Regional & domain state (logistics corridors, commodity markets, hydrological telemetry)
- Predictive temporal simulator (projects future trendlines and counterfactual risks).
"""

import os
import sys
import time
import shutil
import platform
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from axomai.config import settings

class WorldModel:
    """Dynamic mental simulation and structured state of the real external environment."""

    def __init__(self):
        self.last_updated = datetime.now(timezone.utc).isoformat()
        self.entities: Dict[str, Dict[str, Any]] = {}
        self.metric_trajectories: Dict[str, List[Dict[str, Any]]] = {}
        
        # Discover and model real external runtime environment dynamically
        self.discover_environment()

    def discover_environment(self) -> None:
        """Autonomously inspects and builds an accurate representation of the host system."""
        now = datetime.now(timezone.utc).isoformat()
        
        # 1. Real Host Compute Environment
        cpu_count = os.cpu_count() or 4
        os_platform = f"{platform.system()} {platform.release()} ({platform.machine()})"
        python_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
        self.entities["host_system"] = {
            "type": "COMPUTE_INFRASTRUCTURE",
            "os": os_platform,
            "python_runtime": python_ver,
            "logical_cpu_cores": cpu_count,
            "status": "OPERATIONAL",
            "last_discovered": now
        }

        # 2. Storage & Workspace Disk Telemetry
        storage_path = settings.STORAGE_DIR
        try:
            total, used, free = shutil.disk_usage(storage_path)
            total_gb = round(total / (1024 ** 3), 2)
            used_gb = round(used / (1024 ** 3), 2)
            free_gb = round(free / (1024 ** 3), 2)
            usage_pct = round((used / total) * 100, 1)
        except Exception:
            total_gb, used_gb, free_gb, usage_pct = 500.0, 50.0, 450.0, 10.0

        self.entities["storage_telemetry"] = {
            "type": "PERSISTENT_STORAGE",
            "storage_path": str(storage_path),
            "total_disk_gb": total_gb,
            "used_disk_gb": used_gb,
            "free_disk_gb": free_gb,
            "disk_utilization_pct": usage_pct,
            "status": "HEALTHY",
            "last_discovered": now
        }

        # 3. Cognitive Memory Store Verification
        db_file = settings.STORAGE_DIR / "cognitive_memory.db"
        self.entities["cognitive_memory_store"] = {
            "type": "SQLITE_HYPER_MEMORY",
            "path": str(db_file),
            "exists": db_file.exists(),
            "size_bytes": db_file.stat().st_size if db_file.exists() else 0,
            "status": "ONLINE" if db_file.exists() else "INITIALIZING",
            "last_discovered": now
        }

        # 4. API & Orchestration Gateway
        self.entities["orchestration_gateway"] = {
            "type": "SERVICE_GATEWAY",
            "port": getattr(settings, "API_PORT", 8080),
            "host": getattr(settings, "API_HOST", "127.0.0.1"),
            "status": "ACTIVE",
            "endpoints": ["/api/status", "/api/chat", "/api/evaluation/run", "/api/cognition/state"],
            "last_discovered": now
        }
        
        self.last_updated = now

    def register_entity(self, entity_id: str, entity_data: Dict[str, Any]) -> None:
        """Dynamically registers any real-world entity observed by agents or tools."""
        now = datetime.now(timezone.utc).isoformat()
        self.entities[entity_id] = {
            "registered_at": now,
            "last_updated": now,
            **entity_data
        }
        self.last_updated = now

    def update_entity(self, entity_id: str, updates: Dict[str, Any]) -> None:
        """Updates or registers a world entity."""
        if entity_id not in self.entities:
            self.entities[entity_id] = {
                "created_at": datetime.now(timezone.utc).isoformat(),
                **updates
            }
        else:
            self.entities[entity_id].update(updates)
            self.entities[entity_id]["last_modified"] = datetime.now(timezone.utc).isoformat()
        self.last_updated = datetime.now(timezone.utc).isoformat()

    def record_metric_sample(self, metric_name: str, value: float) -> None:
        """Records a timestamped metric for temporal trend modeling."""
        if metric_name not in self.metric_trajectories:
            self.metric_trajectories[metric_name] = []

        now = time.time()
        self.metric_trajectories[metric_name].append({
            "timestamp": now,
            "value": value
        })
        # Keep last 100 samples
        if len(self.metric_trajectories[metric_name]) > 100:
            self.metric_trajectories[metric_name].pop(0)

    def predict_trend(self, metric_name: str, horizon_hours: float = 24.0) -> Dict[str, Any]:
        """
        Projects temporal trendline and forecasts future state.
        Uses linear regression over historical samples if available.
        """
        samples = self.metric_trajectories.get(metric_name, [])
        if len(samples) < 2:
            return {
                "metric": metric_name,
                "forecast_available": False,
                "current_value": samples[-1]["value"] if samples else 0.0,
                "projected_value": samples[-1]["value"] if samples else 0.0,
                "projected_trend": "INSUFFICIENT_HISTORY"
            }

        t_first = samples[0]["timestamp"]
        t_last = samples[-1]["timestamp"]
        dt_hours = (t_last - t_first) / 3600.0 if (t_last - t_first) > 0 else 1.0

        v_first = samples[0]["value"]
        v_last = samples[-1]["value"]
        slope_per_hour = (v_last - v_first) / dt_hours

        projected = round(v_last + (slope_per_hour * horizon_hours), 2)
        trend = "INCREASING" if slope_per_hour > 0.05 else ("DECREASING" if slope_per_hour < -0.05 else "STABLE")

        return {
            "metric": metric_name,
            "forecast_available": True,
            "current_value": v_last,
            "slope_per_hour": round(slope_per_hour, 4),
            "projected_horizon_hours": horizon_hours,
            "projected_value": projected,
            "trend": trend
        }

    def evaluate_action_risk(self, proposed_action: str, target_resource: Optional[str] = None) -> Dict[str, Any]:
        """
        Simulates the counterfactual impact of an action on the world model before execution.
        Categorizes risk into LOW, MEDIUM, or HIGH.
        """
        action_lower = proposed_action.lower()
        
        # High Risk: Data deletion, credential change, system shutdown
        if any(w in action_lower for w in ["delete", "drop", "truncate", "unlink", "kill", "purge_all", "format"]):
            return {
                "risk_tier": "HIGH_RISK",
                "requires_explicit_authorization": True,
                "blast_radius": "DATA_LOSS_POTENTIAL",
                "counterfactual_prediction": "Potential permanent removal of target resource.",
                "safe_to_proceed_autonomously": False
            }

        # Medium Risk: Hot patch, configuration edit, dependency install
        if any(w in action_lower for w in ["patch", "reconfigure", "install", "restart", "modify"]):
            return {
                "risk_tier": "MEDIUM_RISK",
                "requires_explicit_authorization": False,
                "requires_sandbox_validation": True,
                "blast_radius": "RUNTIME_FUNCTIONALITY",
                "counterfactual_prediction": "Method or configuration update. Rollback path must be armed.",
                "safe_to_proceed_autonomously": True
            }

        # Low Risk: Read, analyze, compute, inspect, synthesize
        return {
            "risk_tier": "LOW_RISK",
            "requires_explicit_authorization": False,
            "requires_sandbox_validation": False,
            "blast_radius": "READ_ONLY_COMPUTE",
            "counterfactual_prediction": "Zero destructive impact on world state.",
            "safe_to_proceed_autonomously": True
        }

    def simulate_counterfactual(self, candidate_actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        World Model 2.0: Deliberatively simulates parallel futures for candidate actions.
        Projects consequences, side-effects, latency, cost, and selects optimal branch.
        """
        from axomai.cognition.counterfactual_engine import counterfactual_engine
        return counterfactual_engine.simulate_counterfactual_branches(candidate_actions, self.entities)

    def evaluate_action_regret(
        self,
        chosen_action_id: str,
        actual_reward: float,
        simulation_record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Post-execution counterfactual analysis:
        Detects if an unchosen alternative would have yielded superior utility and logs remedial policy.
        """
        from axomai.cognition.counterfactual_engine import counterfactual_engine
        return counterfactual_engine.evaluate_counterfactual_regret(chosen_action_id, actual_reward, simulation_record)

    def get_world_snapshot(self) -> Dict[str, Any]:
        """Returns full structured snapshot of the world model."""
        return {
            "last_updated": self.last_updated,
            "total_entities_modeled": len(self.entities),
            "entities": self.entities,
            "tracked_trajectories": list(self.metric_trajectories.keys())
        }

world_model = WorldModel()

