"""
AxomAI Evaluation Engine package.
Provides standardized benchmark suite, automated evaluation harness, and regression detector.
"""

from axomai.evaluation.benchmark_suite import BenchmarkSuite, benchmark_suite
from axomai.evaluation.evaluation_harness import EvaluationHarness
from axomai.evaluation.regression_detector import RegressionDetector

__all__ = [
    "BenchmarkSuite",
    "benchmark_suite",
    "EvaluationHarness",
    "RegressionDetector"
]

