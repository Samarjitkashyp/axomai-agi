"""
AxomAI Evaluation Engine - Evaluation Harness.
Executes standardized benchmark batteries against AxomAI orchestrator / agents,
evaluating cognitive performance, safety bounds, error recovery, and latency.
"""

import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from axomai.evaluation.benchmark_suite import BenchmarkSuite, benchmark_suite

class EvaluationHarness:
    """Automated benchmark runner and cognitive evaluator for AxomAI-AGI."""

    def __init__(self, suite: Optional[BenchmarkSuite] = None):
        self.suite = suite or benchmark_suite

    def run_benchmark(self, orchestrator=None, version_tag: str = "v3.0.0-candidate") -> Dict[str, Any]:
        """
        Executes all benchmark tasks through the orchestrator and produces an objective scorecard.
        """
        if orchestrator is None:
            from axomai.agents.master_orchestrator import MasterOrchestrator
            orchestrator = MasterOrchestrator()

        start_total = time.time()
        tasks = self.suite.get_all_tasks()
        task_results = []
        pillar_weights: Dict[str, float] = {}
        pillar_earned: Dict[str, float] = {}

        for task in tasks:
            t_id = task["task_id"]
            pillar = task["pillar"]
            prompt = task["prompt"]
            weight = task.get("weight", 1.0)
            verifier = task["verifier"]

            pillar_weights[pillar] = pillar_weights.get(pillar, 0.0) + weight

            t0 = time.time()
            output_text = ""
            error_msg = None
            try:
                # Stream events from orchestrator
                events = list(orchestrator.orchestrate_stream(prompt))
                # Extract answer from 'final' or 'done' event, or fallback to text events
                for event in events:
                    if event.get("event") in ["done", "final"] or event.get("type") in ["done", "final"]:
                        output_text = event.get("answer", "") or event.get("content", "")
                        break
                if not output_text and events:
                    # Collect text tokens if final event wasn't standard
                    output_text = " ".join([e.get("content", "") for e in events if "content" in e])
            except Exception as ex:
                error_msg = str(ex)
                output_text = f"CRITICAL_FAILURE: {error_msg}"

            latency_ms = round((time.time() - t0) * 1000, 2)

            passed = False
            try:
                passed = bool(verifier(output_text))
            except Exception as v_err:
                passed = False
                error_msg = f"Verifier error: {str(v_err)}"

            earned = weight if passed else 0.0
            pillar_earned[pillar] = pillar_earned.get(pillar, 0.0) + earned

            task_results.append({
                "task_id": t_id,
                "pillar": pillar,
                "weight": weight,
                "passed": passed,
                "latency_ms": latency_ms,
                "error": error_msg,
                "output_preview": output_text[:200] if output_text else ""
            })

        total_weight = sum(pillar_weights.values())
        total_earned = sum(pillar_earned.values())
        composite_axomiq = round((total_earned / total_weight) * 100, 2) if total_weight > 0 else 0.0

        pillar_breakdown = {}
        for p, w in pillar_weights.items():
            earned_p = pillar_earned.get(p, 0.0)
            pillar_breakdown[p] = round((earned_p / w) * 100, 2) if w > 0 else 0.0

        total_passed = sum(1 for r in task_results if r["passed"])
        pass_rate = round((total_passed / len(tasks)) * 100, 2) if tasks else 0.0
        avg_latency = round(sum(r["latency_ms"] for r in task_results) / len(task_results), 2) if task_results else 0.0

        report = {
            "version": version_tag,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "composite_axomiq": composite_axomiq,
            "pass_rate": pass_rate,
            "passed_tasks": total_passed,
            "total_tasks": len(tasks),
            "average_latency_ms": avg_latency,
            "total_duration_sec": round(time.time() - start_total, 2),
            "pillars": pillar_breakdown,
            "task_results": task_results
        }

        return report

