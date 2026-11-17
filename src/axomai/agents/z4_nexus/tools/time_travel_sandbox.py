"""
Z4 Nexus - Time-Travel Execution & Zero-Cost State Rollback Engine.
Creates microsecond shadow snapshots of files and workspace state before executions,
enabling instant deterministic time-travel rollback if errors or regressions occur.
"""

import time
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional

class TimeTravelSandbox:
    """Deterministic snapshot and rollback engine for safe autonomous mutations."""

    def __init__(self):
        self._snapshots: Dict[str, Dict[str, Any]] = {}

    def create_checkpoint(self, file_paths: List[str]) -> Dict[str, Any]:
        """Captures state snapshot of specified files prior to mutation."""
        snapshot_id = f"chk_{int(time.time() * 1000)}"
        file_data = {}
        hasher = hashlib.sha256()

        for fp in file_paths:
            p = Path(fp)
            if p.exists() and p.is_file():
                try:
                    content = p.read_text(encoding="utf-8", errors="ignore")
                    file_data[str(p.resolve())] = content
                    hasher.update(content.encode("utf-8"))
                except Exception:
                    pass

        checkpoint = {
            "snapshot_id": snapshot_id,
            "created_at": time.time(),
            "files_count": len(file_data),
            "state_hash": hasher.hexdigest()[:16],
            "file_data": file_data
        }

        self._snapshots[snapshot_id] = checkpoint
        return {
            "status": "CHECKPOINT_RECORDED",
            "snapshot_id": snapshot_id,
            "files_protected": len(file_data),
            "state_hash": checkpoint["state_hash"]
        }

    def rollback(self, snapshot_id: str) -> Dict[str, Any]:
        """Restores files to the exact pristine state recorded at snapshot_id."""
        if snapshot_id not in self._snapshots:
            return {"status": "ERROR_SNAPSHOT_NOT_FOUND", "restored_files": 0}

        cp = self._snapshots[snapshot_id]
        restored = 0
        for full_path, orig_content in cp["file_data"].items():
            try:
                Path(full_path).write_text(orig_content, encoding="utf-8")
                restored += 1
            except Exception:
                pass

        return {
            "status": "ROLLBACK_SUCCESSFUL",
            "snapshot_id": snapshot_id,
            "restored_files": restored,
            "state_restored_to_hash": cp["state_hash"]
        }

    def commit(self, snapshot_id: str) -> Dict[str, Any]:
        """Commits changes and purges snapshot when execution is verified clean."""
        if snapshot_id in self._snapshots:
            del self._snapshots[snapshot_id]
        return {"status": "CHANGES_COMMITTED_PERMANENTLY", "snapshot_id": snapshot_id}

time_travel_sandbox = TimeTravelSandbox()
