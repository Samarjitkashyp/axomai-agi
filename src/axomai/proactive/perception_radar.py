"""
AxomAI Proactive Engine - Autonomous Real-World Perception Radar.
Observes the real local system, network telemetry, storage assets, and live external internet signals:
1. Real host hardware vitals (CPU, Memory, Disk, Storage health) via psutil.
2. Real-time network reachability, socket latency, and airgap detection.
3. Workspace & File System activity (incoming files, unindexed artifacts).
4. Real-world live external event signals harvested from verified RSS/news endpoints.
Zero synthetic modulo-minute formulas; 100% empirical grounding.
"""

import os
import psutil
import socket
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from axomai.config import settings

class PerceptionRadar:
    """Multi-domain real-world perception radar for autonomous AGI trigger detection."""

    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or settings.STORAGE_DIR
        self.last_observation: Dict[str, Any] = {}
        self.scan_count: int = 0

    def check_network_telemetry(self) -> Dict[str, Any]:
        """Measures empirical socket latency and internet connectivity."""
        t0 = time.time()
        try:
            sock = socket.create_connection(("1.1.1.1", 53), timeout=1.5)
            sock.close()
            latency_ms = round((time.time() - t0) * 1000, 2)
            return {"online": True, "latency_ms": latency_ms}
        except Exception:
            return {"online": False, "latency_ms": 0.0}

    def scan_environment(self) -> List[Dict[str, Any]]:
        """
        Scans system vitals, network reachability, storage assets, and live world indicators.
        Returns a list of high-significance empirical environmental signals.
        """
        self.scan_count += 1
        now = datetime.now(timezone.utc).isoformat()
        signals: List[Dict[str, Any]] = []

        # 1. Real System Hardware & Storage Telemetry
        try:
            cpu_pct = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage(str(self.storage_dir.parent if self.storage_dir.exists() else "."))

            if cpu_pct > 80.0:
                signals.append({
                    "domain": "system_infrastructure",
                    "indicator": "Compute Resource Saturation",
                    "value": cpu_pct,
                    "unit": "%",
                    "severity": "ELEVATED",
                    "source": "psutil_cpu",
                    "message": f"Host CPU utilization reached {cpu_pct}%. Dynamic throttling or task load-shedding recommended."
                })

            disk_free_gb = round(disk.free / (1024 ** 3), 2)
            if disk.percent > 88.0:
                signals.append({
                    "domain": "system_infrastructure",
                    "indicator": "Storage Disk Exhaustion Risk",
                    "value": disk.percent,
                    "unit": "%",
                    "severity": "CRITICAL",
                    "source": "psutil_disk",
                    "message": f"Disk utilization at {disk.percent}% with only {disk_free_gb} GB remaining. Ephemeral artifact purging required."
                })
        except Exception:
            pass

        # 2. Real Network & Gateway Telemetry
        net_info = self.check_network_telemetry()
        if not net_info["online"]:
            signals.append({
                "domain": "network_infrastructure",
                "indicator": "External Network Connectivity Severed",
                "value": 0.0,
                "unit": "ms",
                "severity": "HIGH",
                "source": "socket_gateway",
                "message": "Global internet gateway unreachable. System running in sovereign airgap mode."
            })
        elif net_info["latency_ms"] > 120.0:
            signals.append({
                "domain": "network_infrastructure",
                "indicator": "High Network Gateway Latency",
                "value": net_info["latency_ms"],
                "unit": "ms",
                "severity": "ELEVATED",
                "source": "socket_gateway",
                "message": f"External network latency spiked to {net_info['latency_ms']} ms. Expecting degraded remote API performance."
            })

        # 3. Real File System & Workspace Observation
        try:
            if self.storage_dir.exists():
                all_files = list(self.storage_dir.glob("*.*"))
                recent_files = [f for f in all_files if (time.time() - f.stat().st_mtime) < 3600]
                if recent_files:
                    signals.append({
                        "domain": "workspace_intelligence",
                        "indicator": "Unprocessed Workspace Documents Detected",
                        "value": len(recent_files),
                        "unit": "files",
                        "severity": "OPPORTUNITY",
                        "source": "filesystem_scanner",
                        "message": f"{len(recent_files)} newly modified data artifacts in storage require semantic indexing and ingestion."
                    })
        except Exception:
            pass

        # 4. Real External Market & Macro Event Sampling (Live RSS Radar)
        if net_info["online"]:
            try:
                from axomai.learning.web_harvester import web_harvester
                live_items = web_harvester.fetch_live_news_rss("Assam economic development infrastructure", max_results=1)
                if live_items:
                    item = live_items[0]
                    signals.append({
                        "domain": "external_world_radar",
                        "indicator": "Live Regional Infrastructure Pulse",
                        "value": 1.0,
                        "unit": "event",
                        "severity": "INFO",
                        "source": item.get("source", "Live RSS"),
                        "message": f"Live Dispatch [{item.get('source')}]: {item.get('title')}"
                    })
            except Exception:
                pass

        self.last_observation = {
            "timestamp": now,
            "scan_index": self.scan_count,
            "signals_detected": len(signals),
            "network_online": net_info["online"],
            "network_latency_ms": net_info["latency_ms"]
        }

        return signals

perception_radar = PerceptionRadar()
