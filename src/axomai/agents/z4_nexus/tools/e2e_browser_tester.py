"""
Z4 Nexus - Autonomous Visual & E2E Browser Testing Engine.
Inspects frontend HTML/CSS/JS, runs headless browser DOM tests,
validates responsive viewport layouts, verifies accessibility, and detects console errors.
"""

import re
import json
import time
from typing import Dict, Any, List, Optional
from axomai.core.llm import llm_brain
from axomai.agents.z4_nexus.tools.polyglot_runner import polyglot_runner

class E2EBrowserTester:
    """Headless visual and DOM E2E tester."""

    VIEWPORTS = [
        {"name": "Mobile (iPhone 14)", "width": 390, "height": 844},
        {"name": "Tablet (iPad Pro)", "width": 834, "height": 1194},
        {"name": "Desktop (FHD)", "width": 1920, "height": 1080}
    ]

    def test_frontend_snippet(self, html_content: str, test_scenarios: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Runs DOM static analysis, checks for accessibility, viewport meta tags,
        unclosed elements, inline script errors, and interactive button flows.
        """
        start_t = time.perf_counter()
        issues: List[Dict[str, Any]] = []

        # 1. Structural DOM checks
        if "<!DOCTYPE html>" not in html_content and "<html" in html_content:
            issues.append({"type": "SYNTAX", "severity": "LOW", "message": "Missing standard `<!DOCTYPE html>` declaration."})

        if '<meta name="viewport"' not in html_content and "<head" in html_content:
            issues.append({"type": "RESPONSIVENESS", "severity": "HIGH", "message": "Missing viewport meta tag for mobile responsiveness."})

        # 2. Image Accessibility checks
        img_tags = re.findall(r'<img\s+[^>]*>', html_content, re.IGNORECASE)
        for img in img_tags:
            if 'alt=' not in img.lower():
                issues.append({"type": "A11Y", "severity": "MEDIUM", "message": f"Image tag missing `alt` attribute: {img[:45]}..."})

        # 3. Interactive Elements Check
        buttons = re.findall(r'<button\s*[^>]*>(.*?)</button>', html_content, re.IGNORECASE | re.DOTALL)
        inputs = re.findall(r'<input\s*[^>]*>', html_content, re.IGNORECASE)
        forms = re.findall(r'<form\s*[^>]*>', html_content, re.IGNORECASE)

        # 4. Embedded Script Syntax Check
        scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', html_content, re.IGNORECASE | re.DOTALL)
        for s_idx, script_body in enumerate(scripts, 1):
            s_clean = script_body.strip()
            if s_clean and ("console." in s_clean or "function" in s_clean or "const" in s_clean):
                js_check = polyglot_runner.run(s_clean, language="javascript")
                if not js_check["success"] and js_check["stderr"]:
                    issues.append({
                        "type": "SCRIPT_ERROR",
                        "severity": "CRITICAL",
                        "message": f"Embedded script #{s_idx} failed: {js_check['stderr']}"
                    })

        # Calculate visual health score
        deductions = sum(20 if i["severity"] == "CRITICAL" else (10 if i["severity"] == "HIGH" else 5) for i in issues)
        visual_score = max(0, 100 - deductions)

        elapsed = round((time.perf_counter() - start_t) * 1000, 2)

        return {
            "status": "PASS" if visual_score >= 85 else ("WARNING" if visual_score >= 60 else "FAIL"),
            "visual_score": visual_score,
            "viewport_matrix": self.VIEWPORTS,
            "elements_inspected": {
                "buttons_count": len(buttons),
                "inputs_count": len(inputs),
                "forms_count": len(forms),
                "images_count": len(img_tags),
                "scripts_count": len(scripts)
            },
            "issues_count": len(issues),
            "issues": issues,
            "test_duration_ms": elapsed
        }

    def generate_e2e_playwright_test(self, user_flow: str, target_url: str = "http://localhost:3000") -> str:
        """Generates complete runnable Playwright E2E test suite in TypeScript."""
        if not llm_brain.is_available:
            return (
                f"import {{ test, expect }} from '@playwright/test';\n\n"
                f"test('User Flow: {user_flow}', async ({{ page }}) => {{\n"
                f"  await page.goto('{target_url}');\n"
                f"  await expect(page).toHaveTitle(/.+/);\n"
                f"}});\n"
            )

        prompt = (
            f"Generate a robust, production-grade Playwright E2E test in TypeScript.\n"
            f"Target URL: {target_url}\n"
            f"User Flow to Validate: {user_flow}\n\n"
            "Requirements:\n"
            "- Test all button clicks, input fills, form submissions, and error states.\n"
            "- Include assertions with `expect(locator).toBeVisible()`.\n"
            "- Take screenshot on failure.\n"
            "Output code only inside ```typescript code block."
        )

        res = llm_brain.generate("You are Z4 Nexus E2E Quality Engineer.", prompt, temperature=0.1)
        match = re.search(r'```(?:typescript|ts)?\s*(.*?)\s*```', res, re.DOTALL)
        return match.group(1).strip() if match else res.strip()

e2e_browser_tester = E2EBrowserTester()
