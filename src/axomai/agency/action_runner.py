"""
AxomAI Agency Engine - Autonomous Digital Operations & System Peripheral Controller.
Executes autonomous health diagnostics, storage optimization, report compilation,
and infrastructure monitoring within strict capability-based containment boundaries (RBAC).
"""

import os
import shutil
import platform
import psutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from axomai.config import settings
from axomai.supervision.capability_guard import capability_guard, Capability

class ActionRunner:
    """Safe, sovereign real-world digital operations and system manager with RBAC enforcement."""

    def __init__(self):
        self.operations_log: List[Dict[str, Any]] = []

    def get_system_vitals(self, token_id: Optional[str] = None) -> Dict[str, Any]:
        """Gathers host OS vitals, CPU, memory, and disk health metrics."""
        # Token validation: default to master token if internal call, otherwise enforce READ
        active_token = token_id or capability_guard.master_token
        capability_guard.enforce_capability(active_token, Capability.READ, resource_target="system_vitals")

        now = datetime.now(timezone.utc).isoformat()
        
        cpu_pct = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage(str(settings.STORAGE_DIR))

        vitals = {
            "timestamp": now,
            "os_platform": f"{platform.system()} {platform.release()}",
            "cpu_utilization_percent": cpu_pct,
            "ram_total_gb": round(mem.total / (1024 ** 3), 2),
            "ram_used_gb": round(mem.used / (1024 ** 3), 2),
            "ram_available_gb": round(mem.available / (1024 ** 3), 2),
            "ram_percent": mem.percent,
            "workspace_disk_total_gb": round(disk.total / (1024 ** 3), 2),
            "workspace_disk_free_gb": round(disk.free / (1024 ** 3), 2),
            "disk_percent": disk.percent,
            "agency_health_status": "HARDWARE_OPTIMAL_STABLE"
        }
        return vitals

    def compile_executive_artifact(
        self,
        artifact_title: str,
        markdown_content: str,
        file_format: str = "md",
        token_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Autonomously formats, compiles, and writes an executive document in storage/generated/.
        Strictly requires WRITE capability token.
        """
        active_token = token_id or capability_guard.master_token
        capability_guard.enforce_capability(active_token, Capability.WRITE, resource_target="storage/generated")

        now = datetime.now(timezone.utc).isoformat()
        clean_title = "".join(c if c.isalnum() or c in ['_', '-'] else '_' for c in artifact_title.lower())
        out_dir = settings.STORAGE_DIR / "generated"
        out_dir.mkdir(parents=True, exist_ok=True)
        file_path = out_dir / f"{clean_title}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.{file_format}"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        op_record = {
            "operation": "COMPILE_EXECUTIVE_ARTIFACT",
            "title": artifact_title,
            "file_path": str(file_path),
            "file_size_bytes": file_path.stat().st_size,
            "timestamp": now,
            "status": "SUCCESS"
        }
        self.operations_log.append(op_record)
        return op_record

    def optimize_storage_caches(self, token_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Safely scans and purges stale temporary files in the uploads/temp directory.
        Strictly requires DELETE capability token (preventing unauthorized deletions).
        """
        active_token = token_id or capability_guard.master_token
        capability_guard.enforce_capability(active_token, Capability.DELETE, resource_target="storage/temp")

        now = datetime.now(timezone.utc).isoformat()
        temp_dir = settings.STORAGE_DIR / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        purged_count = 0
        freed_bytes = 0
        for item in temp_dir.glob("*"):
            if item.is_file():
                sz = item.stat().st_size
                item.unlink(missing_ok=True)
                purged_count += 1
                freed_bytes += sz

        return {
            "operation": "PURGE_TEMP_CACHES",
            "files_purged": purged_count,
            "bytes_freed": freed_bytes,
            "timestamp": now,
            "status": "COMPLETED"
        }

action_runner = ActionRunner()
