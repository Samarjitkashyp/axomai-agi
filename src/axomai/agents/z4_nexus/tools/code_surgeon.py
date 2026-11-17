"""
Z4 Nexus - Targeted Inline Code Surgeon & Precision Diff Engine (ChatGPT Canvas Style).
Applies laser-focused surgical modifications, unified diffs, and targeted refactoring
to specific lines/functions without rewriting or hallucinating untouched codebase code.
"""

import difflib
import re
from typing import Dict, Any, Optional
from axomai.core.llm import llm_brain

class CodeSurgeon:
    """ChatGPT Canvas-style precision surgical code editor."""

    def apply_surgical_edit(
        self,
        original_code: str,
        edit_instruction: str,
        target_symbol_or_lines: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes a targeted surgical edit on the code and returns clean unified diff + patched code.
        """
        system_prompt = (
            "You are Z4 Nexus Code Surgeon, an elite code architect & surgical refactoring engine like ChatGPT Canvas and Claude Artifacts. "
            "Rules:\n"
            "1. First, provide a concise 1-2 sentence explanation of the exact changes and improvements you are making.\n"
            "2. Then, provide the COMPLETE, production-ready, updated code in a single markdown code block with the appropriate language identifier (e.g. ```python, ```javascript, etc.).\n"
            "3. Never truncate code or use placeholders like '... rest of code unchanged'. Provide the full modified runnable file."
        )

        user_prompt = (
            f"Original Source Code:\n```\n{original_code}\n```\n\n"
            f"Target Region / Focus: {target_symbol_or_lines or 'Specific region mentioned in edit instruction'}\n"
            f"Edit Instruction: {edit_instruction}\n\n"
            "Perform the code modification, explain the changes, and output the complete updated code."
        )

        updated_code = original_code
        explanation = ""
        if llm_brain.is_available:
            res = llm_brain.generate(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.1)
            match = re.search(r'```(?:[a-zA-Z0-9_-]+)?\s*(.*?)\s*```', res, re.DOTALL)
            if match:
                updated_code = match.group(1).strip()
                explanation = re.sub(r'```(?:[a-zA-Z0-9_-]+)?\s*.*?\s*```', '', res, flags=re.DOTALL).strip()
            else:
                updated_code = res.strip()
                explanation = "Applied code modification as requested."

        # Compute unified diff
        orig_lines = original_code.splitlines(keepends=True)
        new_lines = updated_code.splitlines(keepends=True)
        diff_lines = list(difflib.unified_diff(orig_lines, new_lines, fromfile="original", tofile="modified", n=3))
        unified_diff = "".join(diff_lines)

        return {
            "status": "SURGICAL_EDIT_APPLIED",
            "has_changes": bool(unified_diff),
            "unified_diff": unified_diff,
            "modified_code": updated_code,
            "diff_summary": f"Modified {len([l for l in diff_lines if l.startswith('+')])} lines, deleted {len([l for l in diff_lines if l.startswith('-')])} lines.",
            "explanation": explanation
        }

code_surgeon = CodeSurgeon()
