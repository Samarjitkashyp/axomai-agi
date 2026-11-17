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
    "preferred_languages": ["Python", "TypeScript", "JavaScript"],
    "backend_framework": "FastAPI",
    "frontend_framework": "React (Next.js App Router)",
    "styling": "Tailwind CSS",
    "architecture_pattern": "Modular Clean Architecture with Type Safety",
    "naming_convention": "snake_case for Python, camelCase for JS/TS, PascalCase for Types/Classes",
    "test_runner": "Pytest / Vitest",
    "indentation": "4 spaces for Python, 2 spaces for JS/TS",
    "strict_typing": True,
    "docstrings": "Google / PEP 257 format",
    "custom_instructions": [
        "Never use placeholder TODOs.",
        "Always write complete, production-ready code with error handling.",
        "Include Big-O time and space complexity analysis for algorithms."
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
        return (
            "--- User Personalized Developer Profile ---\n"
            f"- Architecture: {p.get('architecture_pattern')}\n"
            f"- Preferred Stack: {p.get('backend_framework')} + {p.get('frontend_framework')} ({p.get('styling')})\n"
            f"- Style: {p.get('naming_convention')}, Indent: {p.get('indentation')}\n"
            f"- Strict Typing: {p.get('strict_typing')}\n"
            f"- Custom Directives: {'; '.join(p.get('custom_instructions', []))}\n"
            "-------------------------------------------"
        )

dev_memory = DevMemory()
