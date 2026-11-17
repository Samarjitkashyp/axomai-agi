"""
Z4 Nexus - Interactive Artifacts & Split-Screen Live Canvas Engine (Claude Artifacts Style).
Detects, packages, and streams structured interactive Artifacts (React components,
HTML/Tailwind pages, SVG graphics, Mermaid diagrams, and runnable apps) for side-by-side rendering.
"""

import re
import uuid
from typing import Dict, Any, Optional

class ArtifactsCanvas:
    """Claude-style interactive Artifacts and Live Canvas packager."""

    def detect_artifact_kind(self, code: str, language: str = "") -> str:
        """Determines the appropriate rendering kind for the artifact."""
        c = code.strip().lower()
        if "import react" in c or "from 'react'" in c or "export default function" in c or "jsx" in language:
            return "react"
        if "<!doctype html>" in c or ("<html" in c and "<body" in c) or ("<div" in c and "class=" in c):
            return "html"
        if "<svg" in c and "</svg>" in c:
            return "svg"
        if "mermaid" in language or "flowchart" in c or "erdiagram" in c or "sequencediagram" in c:
            return "mermaid"
        if "fastapi" in c or "express" in c or "app.listen" in c or "uvicorn" in c:
            return "api_service"
        return "code"

    def create_artifact(
        self,
        title: str,
        content: str,
        language: str = "python",
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Creates a structured Artifact object that triggers the split-screen Live Canvas in UI.
        """
        kind = self.detect_artifact_kind(content, language)
        artifact_id = f"art_{uuid.uuid4().hex[:8]}"

        # Format markdown artifact wrapper
        markdown_block = (
            f"```artifact\n"
            f"id: {artifact_id}\n"
            f"title: {title}\n"
            f"kind: {kind}\n"
            f"language: {language}\n"
            f"---\n"
            f"{content}\n"
            f"```"
        )

        return {
            "artifact_id": artifact_id,
            "title": title,
            "kind": kind,
            "language": language,
            "content": content,
            "description": description or f"Interactive {kind.upper()} artifact ready in Live Canvas",
            "canvas_trigger": True,
            "markdown_block": markdown_block
        }

artifacts_canvas = ArtifactsCanvas()
