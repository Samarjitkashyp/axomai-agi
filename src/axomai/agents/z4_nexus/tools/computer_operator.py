"""
Z4 Nexus - Autonomous Computer Use & Workspace Operator (Claude 3.5 Sonnet Style).
Inspects workspace environment, audits listening ports, runs package management,
executes builds and test suites, and operates local developer tools autonomously.
"""

import sys
import os
import shutil
import subprocess
import time
from typing import Dict, Any, List, Optional

class ComputerOperator:
    """Autonomous workspace and host developer operator."""

    def __init__(self, workspace_root: str = "e:/axomai_agi"):
        self.workspace_root = workspace_root

    def get_workspace_vitals(self) -> Dict[str, Any]:
        """Audits host runtime environment, disk space, and open dev ports."""
        vitals = {
            "python_executable": sys.executable,
            "node_available": bool(shutil.which("node")),
            "npm_available": bool(shutil.which("npm")),
            "git_available": bool(shutil.which("git")),
            "operating_system": os.name,
            "timestamp": time.time()
        }

        # Check listening developer ports on localhost
        open_ports = []
        for port in [8080, 8000, 3000, 5173, 5000]:
            try:
                import socket
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.15)
                    if s.connect_ex(("127.0.0.1", port)) == 0:
                        open_ports.append(port)
            except Exception:
                pass

        vitals["active_dev_ports"] = open_ports
        return vitals

    def run_workspace_command(self, command: str, timeout_seconds: int = 25) -> Dict[str, Any]:
        """
        Executes a safe developer command in workspace (build, test, package install).
        """
        cmd_lower = command.lower()
        # Security Guardrail: prevent destructive OS commands
        destructive = ["rmdir /s", "del /f /s /q c:\\", "format ", "drop database", ":(){ :|:& };:"]
        if any(d in cmd_lower for d in destructive):
            return {
                "success": False,
                "stdout": "",
                "stderr": "Security Guardrail: Destructive OS command blocked by Z Sentinel.",
                "exit_code": 403
            }

        start_t = time.perf_counter()
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            elapsed = round((time.perf_counter() - start_t) * 1000, 2)
            return {
                "success": res.returncode == 0,
                "stdout": res.stdout.strip(),
                "stderr": res.stderr.strip(),
                "exit_code": res.returncode,
                "runtime_ms": elapsed
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Command timed out after {timeout_seconds}s",
                "exit_code": -1,
                "runtime_ms": timeout_seconds * 1000
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "exit_code": 1,
                "runtime_ms": 0.0
            }

computer_operator = ComputerOperator()
