"""
Z4 Nexus - Automated Code Bug Fixer & AST Debugger Tool.
Performs static AST syntax validation, detects logic errors, unhandled exceptions,
and generates verified drop-in fixes.
"""

import ast
from typing import Dict, Any, Tuple
from axomai.core.llm import llm_brain
from axomai.agents.z4_nexus.tools.code_sandbox import code_sandbox

class BugFixer:
    """Static and dynamic code analyzer and auto-repair engine."""

    def check_syntax(self, code: str) -> Tuple[bool, str]:
        """Validates code syntax via Python AST parser."""
        try:
            ast.parse(code)
            return True, "Syntax is valid."
        except SyntaxError as e:
            return False, f"SyntaxError at line {e.lineno}, col {e.offset}: {e.msg}"

    def analyze_and_fix(self, code: str, error_context: str = "") -> Dict[str, Any]:
        """
        Analyzes broken code, pinpoints the root cause, and generates a repaired version.
        """
        is_valid_syntax, syntax_msg = self.check_syntax(code)

        if not llm_brain.is_available:
            return {
                "fixed": False,
                "diagnosis": syntax_msg,
                "repaired_code": code,
                "verified": is_valid_syntax
            }

        system_prompt = (
            "You are Z4 Nexus, Principal Software Engineer & AST Debugger. "
            "Your task is to analyze broken or bugged code, diagnose the root cause, "
            "and provide a 100% working, repaired version. "
            "Output JSON only: {\"diagnosis\": \"short explanation of the bug\", \"repaired_code\": \"full fixed code\"}"
        )
        user_prompt = (
            f"Code to Debug:\n```python\n{code}\n```\n\n"
            f"Error / Symptoms:\n{error_context or syntax_msg}\n\n"
            "Produce the corrected code in valid JSON."
        )

        try:
            res = llm_brain.generate(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.1)
            clean_json = res.strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_json:
                clean_json = clean_json.split("```")[1].split("```")[0].strip()

            import json
            parsed = json.loads(clean_json)
            repaired = parsed.get("repaired_code", code)
            diagnosis = parsed.get("diagnosis", "Auto-repaired code logic.")

            # Verify repaired code in sandbox
            verify_res = code_sandbox.run_code(repaired)

            return {
                "fixed": True,
                "diagnosis": diagnosis,
                "repaired_code": repaired,
                "verified": verify_res["success"],
                "sandbox_output": verify_res["stdout"] or verify_res["stderr"]
            }
        except Exception as e:
            return {
                "fixed": False,
                "diagnosis": f"Debugger exception: {str(e)}",
                "repaired_code": code,
                "verified": False
            }

bug_fixer = BugFixer()

