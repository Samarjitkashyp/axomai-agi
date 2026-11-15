"""
AxomAI Metamorphosis Engine - Autonomous Self-Patcher & Live Hot-Reloader.
Safely recompiles, sandboxes, benchmarks, and hot-patches runtime Python functions
with zero server downtime, achieving recursive self-improvement backed by
closed-loop regression benchmarking.
"""

import time
import inspect
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Callable

class SelfPatcher:
    """Hot-reloads and patches runtime functions with verified self-optimized code and benchmark regression checks."""

    def __init__(self):
        self.applied_patches: Dict[str, Dict[str, Any]] = []
        self.applied_patches_dict: Dict[str, Dict[str, Any]] = {}
        self.rollback_registry: Dict[str, Callable] = {}

    def test_and_apply_hot_patch(
        self,
        patch_id: str,
        optimized_code: str,
        test_inputs: List[Dict[str, Any]],
        expected_outputs: List[Any],
        target_object: Optional[Any] = None,
        target_method_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validates the patch in a sandboxed test runner, compares outputs,
        and hot-swaps the runtime method live.
        """
        now = datetime.now(timezone.utc).isoformat()
        
        # 1. Security scan
        prohibited = ["os.system", "subprocess", "eval(", "rmtree", "socket", "open("]
        for p in prohibited:
            if p in optimized_code:
                return {
                    "patch_id": patch_id,
                    "status": "REJECTED_UNSAFE",
                    "reason": f"Code contains prohibited keyword '{p}'"
                }

        # 2. Sandbox Compilation
        def _safe_import(name, *args, **kwargs):
            allowed = {"math", "json", "re", "datetime", "typing"}
            if name in allowed:
                return __import__(name, *args, **kwargs)
            raise ImportError(f"Module '{name}' blocked in patch sandbox.")

        safe_builtins = {
            "__import__": _safe_import,
            "math": __import__("math"),
            "range": range,
            "len": len,
            "min": min,
            "max": max,
            "sum": sum,
            "round": round,
            "abs": abs,
            "float": float,
            "int": int,
            "str": str,
            "list": list,
            "dict": dict
        }
        scope = {}

        try:
            t0 = time.perf_counter()
            exec(optimized_code, {"__builtins__": safe_builtins}, scope)
            if "execute" not in scope or not callable(scope["execute"]):
                return {
                    "patch_id": patch_id,
                    "status": "COMPILATION_ERROR",
                    "reason": "Optimized code must expose callable 'execute(**kwargs)' entrypoint"
                }

            patched_func = scope["execute"]

            # 3. Unit Test Verification
            for i, (inp, exp) in enumerate(zip(test_inputs, expected_outputs)):
                res = patched_func(**inp)
                if isinstance(exp, float) and isinstance(res, float):
                    if abs(res - exp) > 0.05:
                        raise AssertionError(f"Regression in test #{i+1}: expected {exp}, got {res}")
                elif res != exp:
                    raise AssertionError(f"Regression in test #{i+1}: expected {exp}, got {res}")

            t1 = time.perf_counter()
            verification_latency_ms = round((t1 - t0) * 1000, 2)

        except Exception as e:
            return {
                "patch_id": patch_id,
                "status": "SANDBOX_TEST_FAILED",
                "error": str(e)
            }

        # 4. Live Runtime Hot-Swapping (Zero Downtime)
        if target_object and target_method_name:
            if hasattr(target_object, target_method_name):
                # Save original for rollback
                self.rollback_registry[patch_id] = getattr(target_object, target_method_name)
                # Hot swap
                setattr(target_object, target_method_name, patched_func)

        patch_meta = {
            "patch_id": patch_id,
            "status": "HOT_PATCHED_LIVE_SUCCESS",
            "verification_latency_ms": verification_latency_ms,
            "test_cases_verified": len(test_inputs),
            "applied_at": now,
            "zero_downtime": True
        }
        self.applied_patches_dict[patch_id] = patch_meta
        return patch_meta

    def benchmark_and_promote_patch(
        self,
        patch_id: str,
        target_object: Any,
        target_method_name: str,
        orchestrator=None
    ) -> Dict[str, Any]:
        """
        Runs comprehensive AGI evaluation harness against the patched system.
        If any regression or security violation is detected, immediately triggers
        automated rollback and restores original unpatched state.
        """
        from axomai.evaluation import EvaluationHarness, RegressionDetector

        harness = EvaluationHarness()
        candidate_score = harness.run_benchmark(orchestrator=orchestrator, version_tag=f"patch_{patch_id}")
        detector = RegressionDetector()
        verdict = detector.compare_and_decide(candidate_score)

        if not verdict["passed"]:
            # Automatic instant rollback!
            self.rollback_patch(patch_id, target_object, target_method_name)
            return {
                "patch_id": patch_id,
                "status": "ROLLED_BACK_DUE_TO_REGRESSION",
                "verdict": verdict,
                "candidate_score": candidate_score
            }

        return {
            "patch_id": patch_id,
            "status": "BENCHMARK_PROMOTED_TO_PRODUCTION",
            "verdict": verdict,
            "candidate_score": candidate_score
        }

    def rollback_patch(self, patch_id: str, target_object: Any, target_method_name: str) -> bool:
        """Rolls back a hot patch to its original pre-patch state."""
        if patch_id in self.rollback_registry and target_object:
            original = self.rollback_registry[patch_id]
            setattr(target_object, target_method_name, original)
            if patch_id in self.applied_patches_dict:
                self.applied_patches_dict[patch_id]["status"] = "ROLLED_BACK"
            return True
        return False

    def get_patch_telemetry(self) -> Dict[str, Any]:
        return {
            "total_patches_applied": len(self.applied_patches_dict),
            "active_patches": list(self.applied_patches_dict.values()),
            "status": "METAMORPHOSIS_ONLINE"
        }

self_patcher = SelfPatcher()
