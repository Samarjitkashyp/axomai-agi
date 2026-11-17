"""
Z4 Nexus - 1-Click Cloud Deployment & Live Preview Engine.
Synthesizes container configs (Docker, Docker Compose), platform manifests
(Vercel, Railway, Render, Fly.io), and prepares live preview deployment pipelines.
"""

import re
import json
import hashlib
from typing import Dict, Any, List, Optional
from axomai.core.llm import llm_brain

class CloudDeployer:
    """Multi-cloud deployment architect."""

    PLATFORMS = ["vercel", "railway", "render", "docker", "fly_io", "aws_ecs"]

    def prepare_deployment(
        self,
        project_name: str,
        stack_description: str,
        target_platform: str = "vercel"
    ) -> Dict[str, Any]:
        """
        Synthesizes container manifests, environment variables template,
        health check specifications, and simulated live preview URL.
        """
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '-', project_name).lower()
        app_hash = hashlib.md5(clean_name.encode()).hexdigest()[:8]
        preview_url = f"https://{clean_name}-{app_hash}.up.railway.app" if target_platform == "railway" else f"https://{clean_name}-{app_hash}.vercel.app"

        system_prompt = (
            "You are Z4 Nexus Chief DevOps & Cloud Infrastructure Engineer. "
            "Generate production-ready deployment configurations for the requested cloud platform. "
            "Include:\n"
            "1. Core Config File (Dockerfile / vercel.json / railway.json)\n"
            "2. Environment Variables (.env.production with placeholders)\n"
            "3. Healthcheck Endpoint Spec (/health)\n"
            "4. CLI Deploy Command (e.g. `vercel --prod` or `railway up`)\n"
            "5. Zero-Downtime Rollout Strategy."
        )

        user_prompt = (
            f"Project: {clean_name}\n"
            f"Stack: {stack_description}\n"
            f"Target Platform: {target_platform}\n"
            f"Preview URL: {preview_url}\n\n"
            "Provide complete manifests and step-by-step deployment instructions."
        )

        if not llm_brain.is_available:
            dossier = (
                f"### 🚀 Cloud Deployment Plan: `{clean_name}`\n\n"
                f"**Target:** `{target_platform.upper()}` | **Live Preview:** [{preview_url}]({preview_url})\n\n"
                f"```dockerfile\nFROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nRUN pip install -r requirements.txt\nCMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n```"
            )
        else:
            dossier = llm_brain.generate(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.1)

        return {
            "status": "DEPLOYMENT_MANIFESTS_READY",
            "project_name": clean_name,
            "platform": target_platform,
            "preview_url": preview_url,
            "health_endpoint": "/api/health",
            "deployment_dossier": dossier
        }

cloud_deployer = CloudDeployer()
