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
            "You are Z4 Nexus Code Surgeon, an elite code architect & surgical refactoring engine like ChatGPT Canvas and Claude Artifacts.\n"
            "Rules:\n"
            "1. First, provide a concise 1-2 sentence explanation of the exact changes and improvements you are making.\n"
            "2. Then, provide the COMPLETE, production-ready, updated code in a single markdown code block with the appropriate language identifier (e.g. ```html, ```python, ```javascript, etc.).\n"
            "3. NEVER TRUNCATE CODE. Do NOT use placeholders like '... rest of code unchanged ...' or '/* remaining styles */'. You MUST return the full modified runnable file from start to finish.\n"
            "4. For HTML documents: keep all styles, head tags, fonts, body elements, scripts, and remaining sections fully intact, strictly removing or modifying only what was requested."
        )

        user_prompt = (
            f"Original Source Code:\n```\n{original_code}\n```\n\n"
            f"Target Region / Focus: {target_symbol_or_lines or 'Specific region mentioned in edit instruction'}\n"
            f"Edit Instruction: {edit_instruction}\n\n"
            "Perform the code modification, explain the changes concisely, and output the 100% complete updated code without any truncation or omitted sections."
        )

        updated_code = original_code
        explanation = ""
        if llm_brain.is_available:
            res = llm_brain.generate(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.1, max_tokens=16384)
            match = re.search(r'```(?:[a-zA-Z0-9_-]+)?\s*(.*?)\s*```', res, re.DOTALL)
            if match:
                updated_code = match.group(1).strip()
                explanation = re.sub(r'```(?:[a-zA-Z0-9_-]+)?\s*.*?\s*```', '', res, flags=re.DOTALL).strip()
            else:
                updated_code = res.strip()
                explanation = "Applied code modification as requested."

        # Precision Self-Healing Safeguard for HTML Element Excision (e.g. remove header/footer/navbar)
        instr_lower = edit_instruction.lower()
        if any(w in instr_lower for w in ["header"]) and any(w in instr_lower for w in ["remove", "delete", "hata", "hatao", "cut", "strip", "omit"]):
            has_header_in_new = bool(re.search(r'<header[\s>]', updated_code, re.I))
            is_truncated = ("<html" in original_code.lower() and "</html>" not in updated_code.lower())
            if has_header_in_new or is_truncated or updated_code == original_code or len(updated_code) < len(original_code) * 0.7:
                excised = re.sub(r'^[ \t]*<header[\s>].*?<\/header>[ \t]*\r?\n?', '', original_code, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE)
                if excised != original_code:
                    updated_code = excised
                    explanation = "Successfully identified and removed the `<header>` block from the document, preserving all styles, components, and layout intact."

        elif any(w in instr_lower for w in ["footer"]) and any(w in instr_lower for w in ["remove", "delete", "hata", "hatao", "cut"]):
            has_footer_in_new = bool(re.search(r'<footer[\s>]', updated_code, re.I))
            is_truncated = ("<html" in original_code.lower() and "</html>" not in updated_code.lower())
            if has_footer_in_new or is_truncated or updated_code == original_code or len(updated_code) < len(original_code) * 0.7:
                excised = re.sub(r'^[ \t]*<footer[\s>].*?<\/footer>[ \t]*\r?\n?', '', original_code, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE)
                if excised != original_code:
                    updated_code = excised
                    explanation = "Successfully excised the `<footer>` block from the document while preserving all content."

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
