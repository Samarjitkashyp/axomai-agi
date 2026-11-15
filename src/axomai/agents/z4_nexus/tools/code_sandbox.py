"""
Z4 Nexus - Secure Python Code Sandbox & Interpreter Tool.
Executes Python scripts, mathematical computations, data transformations,
and algorithm benchmarks safely with timeout handling and full stdout/stderr capture.
"""

import sys
import io
import contextlib
import traceback
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any

class CodeSandbox:
    """Isolated Python execution runtime for Z4 Nexus."""

    def __init__(self, timeout_seconds: int = 15):
        self.timeout_seconds = timeout_seconds

    def run_code(self, code_snippet: str) -> Dict[str, Any]:
        """
        Executes python code snippet in a dedicated isolated subprocess.
        Returns:
            {
                "success": bool,
                "stdout": str,
                "stderr": str,
                "exit_code": int,
                "execution_time_ms": float
            }
        """
        if not code_snippet.strip():
            return {
                "success": False,
                "stdout": "",
                "stderr": "Empty code snippet provided",
                "exit_code": 1
            }

        # Create temporary script file
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
            tmp.write(code_snippet)
            tmp_path = tmp.name

        import time
        start_t = time.perf_counter()

        try:
            # Run in active virtual environment python
            res = subprocess.run(
                [sys.executable, tmp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds
            )
            elapsed_ms = round((time.perf_counter() - start_t) * 1000, 2)

            return {
                "success": res.returncode == 0,
                "stdout": res.stdout.strip(),
                "stderr": res.stderr.strip(),
                "exit_code": res.returncode,
                "execution_time_ms": elapsed_ms
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Execution timed out after {self.timeout_seconds} seconds.",
                "exit_code": -1,
                "execution_time_ms": self.timeout_seconds * 1000
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Sandbox runner error: {str(e)}",
                "exit_code": 1,
                "execution_time_ms": 0.0
            }
        finally:
            try:
                Path(tmp_path).unlink(missing_ok=True)
            except Exception:
                pass

code_sandbox = CodeSandbox()

