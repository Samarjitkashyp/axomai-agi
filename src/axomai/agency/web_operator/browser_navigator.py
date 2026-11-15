"""
AxomAI Agency - Autonomous Web Browser Navigator & Form Filler.
Executes autonomous web navigation, DOM parsing, intelligent form discovery,
field autofill submission, and automated document downloading/ingestion
within strict sovereign and human-in-the-loop security protocols.
"""

import time
import httpx
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from urllib.parse import urljoin

from axomai.config import settings
from axomai.agency.web_operator.security_gate_protocol import security_gate_protocol

DOWNLOADS_DIR = settings.STORAGE_DIR / "downloads"
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

class AutonomousBrowserNavigator:
    """Autonomous DOM parser, web form autofiller, and document downloader."""

    def __init__(self):
        self.session_headers = {
            "User-Agent": "AxomAI-Hyperion/4.0.0 (Sovereign Autonomous Agent; Authorized Digital Operator)"
        }
        self.navigation_history: List[Dict[str, Any]] = []

    def navigate_and_inspect(self, url: str) -> Dict[str, Any]:
        """
        Navigates to a target URL, inspects DOM elements, forms, tables,
        and checks for human-in-the-loop security gates.
        """
        t0 = time.time()
        now = datetime.now(timezone.utc).isoformat()

        # Handle local or test URLs gracefully
        if url.startswith("http://test.local") or url.startswith("mock://"):
            return self._mock_navigation(url)

        try:
            with httpx.Client(timeout=10.0, follow_redirects=True, headers=self.session_headers) as client:
                res = client.get(url)
                duration_ms = round((time.time() - t0) * 1000, 2)

                # Step 1: Check for Security Gates (2FA, CAPTCHA, Verification)
                gate_event = security_gate_protocol.inspect_response_for_security_gate(res.text, service_target=url)
                if gate_event:
                    return {
                        "url": url,
                        "status_code": res.status_code,
                        "gate_triggered": True,
                        "gate_id": gate_event.gate_id,
                        "gate_message": gate_event.prompt_message,
                        "status": "PAUSED_WAITING_HUMAN_APPROVAL",
                        "duration_ms": duration_ms
                    }

                # Step 2: Parse DOM
                soup = BeautifulSoup(res.text, "html.parser")
                title = soup.title.string.strip() if soup.title else "Untitled Page"

                # Extract forms
                forms_found = []
                for i, f in enumerate(soup.find_all("form")):
                    action = f.get("action", "")
                    method = f.get("method", "get").upper()
                    inputs = []
                    for inp in f.find_all(["input", "textarea", "select"]):
                        inputs.append({
                            "name": inp.get("name", ""),
                            "type": inp.get("type", "text"),
                            "value": inp.get("value", "")
                        })
                    forms_found.append({
                        "form_index": i,
                        "action": urljoin(url, action),
                        "method": method,
                        "input_count": len(inputs),
                        "inputs": inputs
                    })

                # Extract tables summary
                tables_count = len(soup.find_all("table"))

                record = {
                    "url": url,
                    "title": title,
                    "status_code": res.status_code,
                    "forms_detected_count": len(forms_found),
                    "forms": forms_found,
                    "tables_detected": tables_count,
                    "gate_triggered": False,
                    "duration_ms": duration_ms,
                    "timestamp": now
                }
                self.navigation_history.append(record)
                return record

        except Exception as ex:
            return {
                "url": url,
                "error": str(ex),
                "status": "NAVIGATION_EXCEPTION",
                "timestamp": now
            }

    def fill_and_submit_form(
        self,
        target_url: str,
        action_url: str,
        form_fields: Dict[str, Any],
        method: str = "POST"
    ) -> Dict[str, Any]:
        """
        Autonomously populates and submits form fields to a verified action URL.
        """
        t0 = time.time()
        now = datetime.now(timezone.utc).isoformat()

        # Handle mock/test environments
        if target_url.startswith("http://test.local") or target_url.startswith("mock://"):
            return {
                "target_url": target_url,
                "action_url": action_url,
                "fields_submitted": list(form_fields.keys()),
                "status": "FORM_SUBMITTED_SUCCESSFULLY",
                "simulated_confirmation": "Application / Data Entry #9842 confirmed.",
                "duration_ms": 12.5,
                "timestamp": now
            }

        try:
            with httpx.Client(timeout=15.0, follow_redirects=True, headers=self.session_headers) as client:
                if method.upper() == "POST":
                    res = client.post(action_url, data=form_fields)
                else:
                    res = client.get(action_url, params=form_fields)

                duration_ms = round((time.time() - t0) * 1000, 2)
                
                # Check for 2FA gate post-submission
                gate = security_gate_protocol.inspect_response_for_security_gate(res.text, service_target=action_url)
                if gate:
                    return {
                        "action_url": action_url,
                        "status": "PAUSED_WAITING_HUMAN_APPROVAL",
                        "gate_id": gate.gate_id,
                        "gate_message": gate.prompt_message
                    }

                return {
                    "action_url": action_url,
                    "status_code": res.status_code,
                    "status": "FORM_SUBMITTED_SUCCESSFULLY" if res.status_code < 400 else "SUBMISSION_FAILED",
                    "fields_submitted_count": len(form_fields),
                    "duration_ms": duration_ms,
                    "timestamp": now
                }

        except Exception as ex:
            return {
                "action_url": action_url,
                "status": "SUBMISSION_EXCEPTION",
                "error": str(ex),
                "timestamp": now
            }

    def download_document_artifact(
        self,
        download_url: str,
        filename_hint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Autonomously downloads a document or data file from the web into storage/downloads/.
        """
        now = datetime.now(timezone.utc).isoformat()
        clean_name = filename_hint or download_url.split("/")[-1].split("?")[0] or f"doc_{int(time.time())}.dat"
        dest_path = DOWNLOADS_DIR / clean_name

        # Mock download handler
        if download_url.startswith("http://test.local") or download_url.startswith("mock://"):
            dest_path.write_text("Mock downloaded tariff / invoice report content", encoding="utf-8")
            return {
                "download_url": download_url,
                "local_file_path": str(dest_path),
                "file_size_bytes": dest_path.stat().st_size,
                "status": "DOWNLOAD_COMPLETED",
                "timestamp": now
            }

        try:
            with httpx.Client(timeout=20.0, follow_redirects=True, headers=self.session_headers) as client:
                res = client.get(download_url)
                if res.status_code == 200:
                    dest_path.write_bytes(res.content)
                    return {
                        "download_url": download_url,
                        "local_file_path": str(dest_path),
                        "file_size_bytes": len(res.content),
                        "status": "DOWNLOAD_COMPLETED",
                        "timestamp": now
                    }
                else:
                    return {
                        "download_url": download_url,
                        "status_code": res.status_code,
                        "status": "DOWNLOAD_FAILED",
                        "timestamp": now
                    }
        except Exception as ex:
            return {
                "download_url": download_url,
                "status": "DOWNLOAD_EXCEPTION",
                "error": str(ex),
                "timestamp": now
            }

    def _mock_navigation(self, url: str) -> Dict[str, Any]:
        """Returns mock DOM inspection for testing."""
        return {
            "url": url,
            "title": "Assam State Electricity Discom Portal",
            "status_code": 200,
            "forms_detected_count": 1,
            "forms": [{
                "form_index": 0,
                "action": urljoin(url, "/api/v1/bills/query"),
                "method": "POST",
                "input_count": 3,
                "inputs": [
                    {"name": "consumer_number", "type": "text", "value": ""},
                    {"name": "subdivision", "type": "text", "value": ""},
                    {"name": "billing_cycle", "type": "text", "value": ""}
                ]
            }],
            "tables_detected": 2,
            "gate_triggered": False,
            "duration_ms": 15.0,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

browser_navigator = AutonomousBrowserNavigator()
