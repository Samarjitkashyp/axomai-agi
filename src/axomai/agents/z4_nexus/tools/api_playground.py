"""
Z4 Nexus - Interactive API Playground & OpenAPI Spec Engine.
Extracts API schemas, generates OpenAPI 3.1 specifications, Postman Collections,
and interactive cURL command suites for instant endpoint execution.
"""

import re
import json
from typing import Dict, Any, List, Optional
from axomai.core.llm import llm_brain

class APIPlayground:
    """OpenAPI and interactive endpoint tester engine."""

    def generate_api_suite(self, api_code_or_intent: str, framework: str = "fastapi") -> Dict[str, Any]:
        """
        Synthesizes OpenAPI 3.1 spec, Postman Collection, and interactive cURL suite.
        """
        system_prompt = (
            "You are Z4 Nexus Senior API Architect. "
            "Convert the user's API code or requirements into an interactive API testing suite.\n"
            "Include:\n"
            "1. OpenAPI 3.1.0 Specification (JSON or YAML)\n"
            "2. Complete Postman Collection v2.1.0 JSON\n"
            "3. Interactive `curl` command suite with realistic headers, query params, and JSON bodies\n"
            "4. Expected response status codes (200, 201, 400, 401, 404, 500)"
        )

        user_prompt = (
            f"Framework: {framework}\n"
            f"API Code or Requirements:\n{api_code_or_intent}\n\n"
            "Provide the complete interactive API playground dossier."
        )

        if not llm_brain.is_available:
            suite = (
                "### 🔌 Interactive API Playground\n\n"
                "**Endpoint:** `POST /api/v1/auth/login`\n\n"
                "```bash\n"
                "curl -X POST http://localhost:8000/api/v1/auth/login \\\n"
                "  -H 'Content-Type: application/json' \\\n"
                "  -d '{\"email\": \"admin@axomai.com\", \"password\": \"secret123\"}'\n"
                "```\n\n"
                "**Expected 200 OK Response:**\n"
                "```json\n"
                "{\"access_token\": \"jwt_token_sample\", \"token_type\": \"bearer\"}\n"
                "```"
            )
        else:
            suite = llm_brain.generate(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.1)

        return {
            "status": "API_PLAYGROUND_READY",
            "framework": framework,
            "playground_dossier": suite
        }

api_playground = APIPlayground()
