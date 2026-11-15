"""
AxomAI Metamorphosis Engine - Code Profiler & Complexity Analyzer.
Analyzes agent tool source code, identifies latency bottlenecks,
computes cyclomatic/AST metrics, and highlights optimization candidates.
"""

import ast
import time
from typing import Dict, Any, List, Optional

class CodeProfiler:
    """Profiles code complexity and identifies self-optimization targets."""

    def __init__(self):
        self.profiled_targets: List[Dict[str, Any]] = []

    def analyze_source_code(self, source_code: str, module_name: str = "dynamic_module") -> Dict[str, Any]:
        """
        Parses Python code AST, calculates complexity, and assesses optimization potential.
        """
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return {"status": "SYNTAX_ERROR", "error": str(e), "optimizable": False}

        function_defs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        loops = [node for node in ast.walk(tree) if isinstance(node, (ast.For, ast.While))]
        branches = [node for node in ast.walk(tree) if isinstance(node, (ast.If, ast.IfExp))]
        
        # Approximate Cyclomatic Complexity (1 + branches + loops)
        complexity = 1 + len(branches) + len(loops)
        line_count = len(source_code.strip().splitlines())

        # Determine optimization recommendation
        if complexity > 8 or len(loops) > 2:
            recommendation = "HIGH_PRIORITY_VECTORIZE_OR_MEMOIZE"
            potential_speedup = "2.5x - 4.0x"
        elif complexity > 4:
            recommendation = "MODERATE_INLINE_CACHING"
            potential_speedup = "1.5x - 2.0x"
        else:
            recommendation = "OPTIMAL_LIGHTWEIGHT"
            potential_speedup = "1.1x"

        result = {
            "module_name": module_name,
            "line_count": line_count,
            "functions_count": len(function_defs),
            "cyclomatic_complexity": complexity,
            "loop_count": len(loops),
            "branch_count": len(branches),
            "recommendation": recommendation,
            "estimated_speedup": potential_speedup,
            "optimizable": complexity >= 3
        }
        self.profiled_targets.append(result)
        return result

    def get_profiler_telemetry(self) -> Dict[str, Any]:
        return {
            "total_profiled": len(self.profiled_targets),
            "recent_targets": self.profiled_targets[-5:],
            "status": "PROFILER_ACTIVE"
        }

code_profiler = CodeProfiler()

