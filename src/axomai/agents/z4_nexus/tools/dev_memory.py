"""
Z4 Nexus - Long-Term Developer Memory & Personalized Coding Style Engine.
Persists developer preferences, preferred architectural paradigms, naming conventions,
and personal style constraints to deliver hyper-tailored software engineering.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

PROFILE_FILE = Path("e:/axomai_agi/.axomai_dev_profile.json")

DEFAULT_PROFILE = {
    "preferred_languages": [],
    "backend_framework": None,
    "frontend_framework": None,
    "styling": None,
    "architecture_pattern": "Clean Modular Architecture",
    "naming_convention": "Standard language idiomatic conventions",
    "test_runner": "Standard test runner",
    "indentation": "Standard",
    "strict_typing": True,
    "docstrings": "Standard docstrings",
    "custom_instructions": [
        "Never use placeholder TODOs.",
        "Always write clean, complete, reliable code with proper error handling."
    ]
}

class DevMemory:
    """Persistent developer personalization memory."""

    def __init__(self, profile_path: Path = PROFILE_FILE):
        self.profile_path = profile_path
        self._ensure_profile()

    def _ensure_profile(self):
        if not self.profile_path.exists():
            try:
                self.profile_path.write_text(json.dumps(DEFAULT_PROFILE, indent=2), encoding="utf-8")
            except Exception:
                pass

    def get_profile(self) -> Dict[str, Any]:
        """Loads active developer preferences."""
        if self.profile_path.exists():
            try:
                return json.loads(self.profile_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return DEFAULT_PROFILE

    def update_profile(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Updates and persists new developer style preferences."""
        current = self.get_profile()
        current.update(updates)
        try:
            self.profile_path.write_text(json.dumps(current, indent=2), encoding="utf-8")
        except Exception:
            pass
        return current

    def format_style_prompt(self) -> str:
        """Formats developer profile into system prompt injection string."""
        p = self.get_profile()
        stack_parts = []
        if p.get("backend_framework"):
            stack_parts.append(p.get("backend_framework"))
        if p.get("frontend_framework"):
            stack_parts.append(p.get("frontend_framework"))
        if p.get("styling"):
            stack_parts.append(f"({p.get('styling')})")

        stack_line = f"- Preferred Stack: {' + '.join(stack_parts)}\n" if stack_parts else ""
        if not stack_line and not p.get("preferred_languages"):
            return ""

        return (
            "--- User Personalized Developer Profile ---\n"
            f"{stack_line}"
            f"- Architecture: {p.get('architecture_pattern', 'Clean Architecture')}\n"
            "-------------------------------------------"
        )

dev_memory = DevMemory()
