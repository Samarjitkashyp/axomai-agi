"""
Z4 Nexus - Dynamic API Connector & Integration Engine.
Generates robust Python client wrappers for REST / GraphQL APIs,
webhook listeners, and third-party SaaS services (Stripe, Razorpay, Shopify, Salesforce, Twilio).
"""

from typing import Dict, Any
from axomai.core.llm import llm_brain

class APIConnector:
    """Automated API integration client generator."""

    def generate_client(self, api_description_or_spec: str) -> Dict[str, Any]:
        """
        Produces a complete, production-ready Python client for the specified API.
        """
        if not llm_brain.is_available:
            return {
                "service_name": "Generic API",
                "client_code": "# LLM Brain offline - API generator requires active model.",
                "endpoints": []
            }

        system_prompt = (
            "You are Z4 Nexus, Senior API Architect. Generate a clean, production-ready Python "
            "integration client using `requests` or `urllib` with authentication headers, "
            "type hints, docstrings, and robust error handling. "
            "Output JSON only: {\"service_name\": \"Name\", \"endpoints\": [\"method path\"], \"client_code\": \"full python code\"}"
        )
        user_prompt = (
            f"API Requirements / Specification:\n{api_description_or_spec}\n\n"
            "Generate the complete Python client wrapper in JSON format."
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
            return parsed
        except Exception as e:
            return {
                "service_name": "Custom Integration",
                "client_code": f"# Error generating client: {str(e)}",
                "endpoints": []
            }

api_connector = APIConnector()

