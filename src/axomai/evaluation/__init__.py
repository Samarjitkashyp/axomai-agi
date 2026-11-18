"""
AxomAI Evaluation Engine package.
Provides standardized benchmark suite, automated evaluation harness, regression detector,
and the AXOMIQ General Intelligence Benchmark v1 (Visible vs Hidden splits).
"""

from axomai.evaluation.benchmark_suite import BenchmarkSuite, benchmark_suite
from axomai.evaluation.evaluation_harness import EvaluationHarness
from axomai.evaluation.regression_detector import RegressionDetector
from axomai.evaluation.axomiq_benchmark import AXOMIQBenchmark, axomiq_benchmark

__all__ = [
    "BenchmarkSuite",
    "benchmark_suite",
    "EvaluationHarness",
    "RegressionDetector",
    "AXOMIQBenchmark",
    "axomiq_benchmark"
]
