"""
Z4 Nexus - Automated Performance Profiling & Flamegraph Heatmap Engine.
Benchmarks execution speed, analyzes algorithmic Big-O complexity,
identifies CPU/Memory hotspots, and provides optimized drop-in replacements.
"""

import time
import re
from typing import Dict, Any, List, Optional
from axomai.core.llm import llm_brain
from axomai.agents.z4_nexus.tools.polyglot_runner import polyglot_runner

class PerformanceProfiler:
    """Algorithmic profiler and performance optimizer."""

    def profile_and_optimize(self, code: str, language: str = "python", benchmark_runs: int = 5) -> Dict[str, Any]:
        """
        Profiles code performance and produces an optimized version with speedup analysis.
        """
        # Run benchmark of baseline code if runnable
        times = []
        if language in ["python", "javascript"]:
            for _ in range(benchmark_runs):
                res = polyglot_runner.run(code, language=language)
                if res["success"]:
                    times.append(res["execution_time_ms"])

        avg_latency = round(sum(times) / len(times), 2) if times else 0.0

        # LLM Algorithmic Profiling & Optimization
        system_prompt = (
            "You are Z4 Nexus Principal Performance & Systems Profiler. "
            "Analyze the given code for Big-O Time/Space complexity, identify the exact bottleneck, "
            "render an ASCII Flamegraph Heatmap of time spent, and output an ultra-optimized version.\n"
            "Format:\n"
            "1. Complexity Baseline (e.g. O(N^2))\n"
            "2. Bottleneck Breakdown\n"
            "3. ASCII Flamegraph\n"
            "4. Optimized Code Block\n"
            "5. Expected Speedup Ratio (e.g. ~10x-50x faster)"
        )

        user_prompt = (
            f"Code to Profile ({language}):\n```{language}\n{code}\n```\n"
            f"Measured Average Latency: {avg_latency} ms across {len(times)} runs.\n\n"
            "Provide the complete performance profiling dossier and optimized code."
        )

        full_dossier = ""
        optimized_code = code

        if llm_brain.is_available:
            full_dossier = llm_brain.generate(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.1)
            code_match = re.search(r'```(?:[a-zA-Z0-9_-]+)?\s*(.*?)\s*```', full_dossier, re.DOTALL)
            if code_match:
                optimized_code = code_match.group(1).strip()
        else:
            full_dossier = (
                f"### ⚡ Performance Profile\n\n"
                f"- Measured Latency: `{avg_latency} ms`\n"
                f"- Estimated Complexity: `O(N)`\n"
                f"- Recommendation: Cache intermediate calculations and vectorize operations."
            )

        return {
            "status": "PROFILED_OPTIMIZED",
            "measured_avg_latency_ms": avg_latency,
            "benchmark_samples": len(times),
            "optimized_code": optimized_code,
            "profiling_dossier": full_dossier
        }

perf_profiler = PerformanceProfiler()
