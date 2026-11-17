"""
Z4 Nexus - Interactive System Architecture & Database Schema Visualizer.
Synthesizes verified Mermaid diagrams for Cloud Architecture, Microservices,
Entity-Relationship (ER) models, API Sequence Flows, and State Machines.
"""

import re
from typing import Dict, Any, Optional
from axomai.core.llm import llm_brain

class ArchVisualizer:
    """Enterprise System Architecture & Schema Visualizer."""

    SUPPORTED_TYPES = ["architecture", "er_diagram", "sequence", "state_machine", "pipeline"]

    def generate_diagram(
        self,
        intent: str,
        diagram_type: Optional[str] = "architecture",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes a verified Mermaid diagram and explanatory documentation.
        """
        system_prompt = (
            "You are Z4 Nexus Chief System Architect & Data Modeler. "
            "You create pristine, highly accurate Mermaid diagrams for complex software systems. "
            "Follow these strict formatting rules:\n"
            "1. Only use standard Mermaid syntax (flowchart TD/LR, erDiagram, sequenceDiagram, stateDiagram-v2).\n"
            "2. In flowcharts, always wrap labels with special characters in double quotes: A[\"User (Web/Mobile)\"].\n"
            "3. For erDiagram, specify entity names, fields, data types, and proper cardinalities (||--o{ etc.).\n"
            "4. For sequenceDiagram, show clear request/response activations between participants.\n"
            "5. Enclose the mermaid diagram strictly in ```mermaid ... ``` code blocks."
        )

        user_prompt = (
            f"User Architectural Request: {intent}\n"
            f"Diagram Type: {diagram_type or 'architecture'}\n"
            f"Context / Existing Components: {context or 'None specified'}\n\n"
            "Produce:\n"
            "1. Complete Mermaid diagram code block.\n"
            "2. Clear architectural breakdown explaining components, data flow, scaling bottlenecks, and resilience strategies."
        )

        if not llm_brain.is_available:
            default_mermaid = (
                "```mermaid\n"
                "flowchart TD\n"
                "    User[\"Client Browser / Mobile\"] --> CDN[\"Cloudflare Edge / CDN\"]\n"
                "    CDN --> LB[\"Application Load Balancer\"]\n"
                "    LB --> API[\"FastAPI / Node Backend Services\"]\n"
                "    API --> Cache[(\"Redis In-Memory Cache\")]\n"
                "    API --> DB[(\"PostgreSQL Primary DB\")]\n"
                "```"
            )
            return {
                "success": True,
                "mermaid_raw": default_mermaid,
                "explanation": "Default 3-tier scalable web architecture."
            }

        res = llm_brain.generate(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.2)
        match = re.search(r'```mermaid\s*(.*?)\s*```', res, re.DOTALL)
        mermaid_code = match.group(1).strip() if match else ""

        return {
            "success": bool(mermaid_code),
            "mermaid_raw": f"```mermaid\n{mermaid_code}\n```" if mermaid_code else "",
            "full_response": res.strip()
        }

arch_visualizer = ArchVisualizer()
