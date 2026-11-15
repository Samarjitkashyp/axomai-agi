"""
AxomAI Cognition Engine - World Model (Dynamic Environmental Representation).
Maintains a living, structured mental model of the external world:
- Host environment (compute, storage trends, database cluster, services)
- Workspace entities (indexed documents, telemetry files, generated artifacts)
- Regional & domain state (logistics corridors, commodity markets, hydrological telemetry)
- Predictive temporal simulator (projects future trendlines and counterfactual risks).
"""

import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from axomai.config import settings

class WorldModel:
    """Dynamic mental simulation and structured state of the external environment."""

    def __init__(self):
        self.last_updated = datetime.now(timezone.utc).isoformat()
        
        # Structured representation of external entities
        self.entities: Dict[str, Dict[str, Any]] = {
            "server_host": {
                "type": "INFRASTRUCTURE",
                "status": "HEALTHY",
                "port": 8080,
                "endpoints_active": ["/api/status", "/api/chat", "/api/evaluation/run", "/api/cognition/state"],
                "disk_trend_mb_per_hour": 1.2
            },
            "database_cluster": {
                "type": "POSTGRESQL",
                "name": settings.DB_NAME,
                "host": settings.DB_HOST,
                "port": settings.DB_PORT,
                "status": "ONLINE",
                "replication_mode": "PRIMARY"
            },
            "changsari_logistics_hub": {
                "type": "CORRIDOR_NODE",
                "location": "Kamrup Assam",
                "railhead_status": "OPERATIONAL",
                "buffer_stock_capacity_pct": 94.2,
                "throughput_teu_daily": 850
            },
            "brahmaputra_hydrology_network": {
                "type": "GEOTECHNICAL_SENSOR",
                "embankment_sector": "Dibrugarh - Majuli",
                "pore_pressure_fos": 1.26,
                "water_elevation_trend": "STABLE",
                "flood_risk_level": "LOW_SEASONAL"
            },
            "guwahati_tea_auction_mandi": {
                "type": "COMMODITY_EXCHANGE",
                "spot_index_inr_kg": 248.50,
                "export_differential_pct": -3.2,
                "hedged_currency_pair": "EUR/INR",
                "volatility_index": "MODERATE"
            }
        }

        # Temporal metric history for forecasting
        self.metric_trajectories: Dict[str, List[Dict[str, Any]]] = {}

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

    def get_world_snapshot(self) -> Dict[str, Any]:
        """Returns full structured snapshot of the world model."""
        return {
            "last_updated": self.last_updated,
            "total_entities_modeled": len(self.entities),
            "entities": self.entities,
            "tracked_trajectories": list(self.metric_trajectories.keys())
        }

world_model = WorldModel()

