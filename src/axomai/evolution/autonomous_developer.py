"""
AxomAI Evolution Engine - Autonomous Developer & Code Synthesizer.
Empowers AxomAI to write its own Python code, execute sandboxed verification unit tests,
benchmark accuracy, and register verified tools into Procedural Memory without human intervention.
"""

import sys
import traceback
from datetime import datetime
from typing import Dict, Any, List, Optional
from axomai.memory.procedural_memory import procedural_memory, ProceduralMemory

class AutonomousDeveloper:
    """Self-coding and automated tool engineering engine."""

    def __init__(self):
        self.procedural = procedural_memory
        self.synthesis_log: List[Dict[str, Any]] = []

    def develop_and_deploy_skill(
        self,
        skill_name: str,
        category: str,
        description: str,
        code_body: str,
        unit_test_cases: List[Dict[str, Any]],
        input_schema: Optional[Dict[str, Any]] = None,
        output_schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes, sandboxes, unit-tests, and deploys a new Python tool.
        """
        now = datetime.utcnow().isoformat()
        
        # 1. Inspect code safety
        forbidden = ["os.system", "subprocess", "eval(", "shutil.rmtree", "__import__('os')", "socket", "open("]
        for f in forbidden:
            if f in code_body:
                return {
                    "status": "REJECTED_UNSAFE_OPERATION",
                    "reason": f"Forbidden instruction '{f}' detected in synthesized code.",
                    "skill_name": skill_name
                }

        # 2. Prepare Sandbox Environment
        def _safe_import(name, *args, **kwargs):
            allowed = {"math", "json", "re", "datetime", "typing"}
            if name in allowed:
                return __import__(name, *args, **kwargs)
            raise ImportError(f"Import of module '{name}' is restricted by sovereign sandbox policy.")

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
            "dict": dict,
            "isinstance": isinstance
        }
        scope = {}
        
        # 3. Compile and Run Unit Tests
        try:
            exec(code_body, {"__builtins__": safe_builtins}, scope)
            if "execute" not in scope or not callable(scope["execute"]):
                return {
                    "status": "COMPILATION_ERROR",
                    "reason": "Synthesized code must define a callable function 'execute(**kwargs)'",
                    "skill_name": skill_name
                }

            # Run test cases
            passed_tests = 0
            for i, tc in enumerate(unit_test_cases):
                inputs = tc.get("inputs", {})
                expected = tc.get("expected_output")
                result = scope["execute"](**inputs)
                
                # Numeric tolerance comparison if float
                if isinstance(expected, float) and isinstance(result, float):
                    if abs(result - expected) > 0.05:
                        raise AssertionError(f"Test #{i+1} failed: Expected {expected}, got {result}")
                elif expected is not None and result != expected:
                    raise AssertionError(f"Test #{i+1} failed: Expected {expected}, got {result}")
                
                passed_tests += 1

        except Exception as e:
            tb = traceback.format_exc()
            return {
                "status": "UNIT_TEST_FAILED",
                "error": str(e),
                "traceback": tb[-200:],
                "skill_name": skill_name
            }

        # 4. Deploy to Procedural Memory
        reg_res = self.procedural.register_skill(
            skill_name=skill_name,
            category=category,
            description=description,
            code_snippet=code_body,
            input_schema=input_schema or {"kwargs": "Any"},
            output_schema=output_schema or {"result": "Any"},
            is_verified=True
        )

        record = {
            "skill_name": skill_name,
            "skill_id": reg_res["skill_id"],
            "status": "DEPLOYED_TO_PROCEDURAL_MEMORY",
            "passed_tests": passed_tests,
            "deployed_at": now
        }
        self.synthesis_log.append(record)

        return record

    def autonomous_synthesize_algorithm(self, domain_challenge: str) -> Dict[str, Any]:
        """
        Autonomously synthesizes and deploys algorithms for common high-value domain challenges.
        """
        d_low = domain_challenge.lower()

        if "freight carbon" in d_low or "emission per ton km" in d_low:
            code = (
                "def execute(tonnage, distance_km, mode='rail'):\n"
                "    factors = {'rail': 0.028, 'road_truck': 0.096, 'inland_waterway': 0.031}\n"
                "    factor = factors.get(mode, 0.096)\n"
                "    total_kg = tonnage * distance_km * factor\n"
                "    return round(total_kg / 1000.0, 3)  # metric tons of CO2e\n"
            )
            return self.develop_and_deploy_skill(
                skill_name="Freight Ton-Km Carbon Auditor",
                category="LOGISTICS_EMISSIONS",
                description="Calculates GHG carbon emissions for freight consignments across rail, road, and inland waterway.",
                code_body=code,
                unit_test_cases=[
                    {"inputs": {"tonnage": 1000, "distance_km": 500, "mode": "rail"}, "expected_output": 14.0},
                    {"inputs": {"tonnage": 500, "distance_km": 200, "mode": "inland_waterway"}, "expected_output": 3.1}
                ],
                input_schema={"tonnage": "float", "distance_km": "float", "mode": "str"},
                output_schema={"tco2e": "float"}
            )

        elif "black scholes" in d_low or "delta" in d_low:
            code = (
                "def execute(spot, strike, rate, vol, time_years):\n"
                "    import math\n"
                "    d1 = (math.log(spot / strike) + (rate + 0.5 * vol ** 2) * time_years) / (vol * math.sqrt(time_years))\n"
                "    # Normal CDF approximation\n"
                "    delta = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))\n"
                "    return round(delta, 3)\n"
            )
            return self.develop_and_deploy_skill(
                skill_name="Black-Scholes Delta Calculator",
                category="QUANTITATIVE_FINANCE",
                description="Computes option call Delta sensitivity for commodity futures hedging.",
                code_body=code,
                unit_test_cases=[
                    {"inputs": {"spot": 100.0, "strike": 100.0, "rate": 0.05, "vol": 0.2, "time_years": 1.0}, "expected_output": 0.637}
                ],
                input_schema={"spot": "float", "strike": "float", "rate": "float", "vol": "float", "time_years": "float"},
                output_schema={"call_delta": "float"}
            )

        else:
            code = (
                "def execute(value, growth_rate, discount_rate):\n"
                "    if discount_rate <= growth_rate:\n"
                "        return 0.0\n"
                "    terminal_value = (value * (1.0 + growth_rate)) / (discount_rate - growth_rate)\n"
                "    return round(terminal_value, 2)\n"
            )
            return self.develop_and_deploy_skill(
                skill_name="Gordon Growth Terminal Valuator",
                category="FINANCIAL_ENGINEERING",
                description="Computes perpetual terminal enterprise value using Gordon Growth formula.",
                code_body=code,
                unit_test_cases=[
                    {"inputs": {"value": 1000.0, "growth_rate": 0.03, "discount_rate": 0.10}, "expected_output": 14714.29}
                ]
            )

autonomous_developer = AutonomousDeveloper()
