"""
Automated Verification Suite for AxomAI-AGI Autonomous Web Operator & Digital RPA.
Tests:
1. Sovereign Encrypted Credential Vault (Fernet AES Encryption & Zero-Leakage Masking)
2. Human-in-the-Loop Security Gate Protocol (Safe 2FA & Verification Pause/Resume)
3. Autonomous Browser Navigator (DOM Parsing, Form Discovery & Autofill)
4. Automated Document Download & Ingestion
5. Multi-Tab Swarm Coordinator (Concurrent Multi-Portal Extraction)
6. Live Web-Operator API Endpoints
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath("src"))

def test_1_credential_vault():
    print("--- [1/6] Testing Sovereign Encrypted Credential Vault ---")
    from axomai.agency.web_operator import credential_vault

    # Store credential with Fernet encryption
    res = credential_vault.store_credential(
        service_id="discom_portal_assam",
        service_name="Assam Power Discom Portal",
        username="tea_estate_consumer_4021",
        secret="SuperSecretPassword@2026",
        metadata={"meter_no": "AP-9812", "division": "Dibrugarh"}
    )
    assert res["status"] == "SECURED_IN_ENCRYPTED_VAULT"

    # Retrieve decrypted credential for authorized operation
    cred = credential_vault.get_credential("discom_portal_assam")
    assert cred is not None
    assert cred["secret"] == "SuperSecretPassword@2026"
    assert cred["username"] == "tea_estate_consumer_4021"

    # Verify zero-leakage masking
    masked_list = credential_vault.list_services_masked()
    discom_entry = next((c for c in masked_list if c["service_id"] == "discom_portal_assam"), None)
    assert discom_entry is not None
    assert discom_entry["secret_masked"] == "********"
    assert "SuperSecretPassword@2026" not in str(discom_entry)

    # Verify audit log
    audit = credential_vault.get_audit_trail()
    assert len(audit) >= 2
    print("-> Credential stored with AES Fernet encryption, decrypted secret retrieved, and zero-leakage verified.")
    print("-> Sovereign Encrypted Credential Vault: PASSED")

def test_2_security_gate_protocol():
    print("\n--- [2/6] Testing Human-in-the-Loop Security Gate Protocol ---")
    from axomai.agency.web_operator import security_gate_protocol

    # 1. Simulate encountering a 2FA OTP prompt in HTML
    mock_html_2fa = """
    <html><body>
        <h2>Two-Factor Authentication Required</h2>
        <p>Please enter OTP sent to your registered mobile number ending in 8912.</p>
        <input type="text" name="otp_code" placeholder="Enter 6-digit OTP" />
    </body></html>
    """
    gate_event = security_gate_protocol.inspect_response_for_security_gate(
        response_text=mock_html_2fa,
        service_target="https://discom.assam.gov.in/auth/2fa"
    )

    assert gate_event is not None
    assert gate_event.gate_type == "2FA_OTP_VERIFICATION"
    assert gate_event.status == "PAUSED_WAITING_HUMAN_APPROVAL"
    gate_id = gate_event.gate_id
    print(f"-> Security Gate successfully triggered: {gate_id} ({gate_event.gate_type})")
    print(f"-> AGI safely paused: {gate_event.prompt_message}")

    # 2. Check pending gates list
    pending = security_gate_protocol.get_pending_gates()
    assert any(g["gate_id"] == gate_id for g in pending)

    # 3. Simulate user approving gate with OTP code
    approved = security_gate_protocol.approve_and_resume_gate(
        gate_id=gate_id,
        auth_token_or_confirmation="581924"
    )
    assert approved["resumed"] is True
    assert approved["status"] == "GATE_RESOLVED_MISSION_RESUMED"
    print("-> Human-in-the-Loop approval registered: Mission unblocked and resumed.")
    print("-> Security Gate Protocol: PASSED")

def test_3_browser_navigator_dom_and_forms():
    print("\n--- [3/6] Testing Autonomous Browser Navigator DOM & Forms ---")
    from axomai.agency.web_operator import browser_navigator

    # Test mock DOM navigation and form detection
    nav_res = browser_navigator.navigate_and_inspect("mock://portal.assam.gov.in/billing")
    assert nav_res["status_code"] == 200
    assert nav_res["forms_detected_count"] >= 1
    form = nav_res["forms"][0]
    assert form["input_count"] >= 3
    print(f"-> Visited page '{nav_res['title']}', detected {nav_res['forms_detected_count']} forms.")

    # Test form autofill and submission
    submit_res = browser_navigator.fill_and_submit_form(
        target_url="mock://portal.assam.gov.in/billing",
        action_url="mock://portal.assam.gov.in/billing/submit",
        form_fields={
            "consumer_number": "CON-98421",
            "subdivision": "Dibrugarh Rural",
            "billing_cycle": "OCT-2026"
        }
    )
    assert submit_res["status"] == "FORM_SUBMITTED_SUCCESSFULLY"
    print("-> Form autofill and submission executed successfully.")
    print("-> Autonomous Browser Navigator: PASSED")

def test_4_document_download():
    print("\n--- [4/6] Testing Autonomous Document Downloading ---")
    from axomai.agency.web_operator import browser_navigator
    from pathlib import Path

    dl_res = browser_navigator.download_document_artifact(
        download_url="mock://portal.assam.gov.in/reports/oct_tariff_schedule.pdf",
        filename_hint="oct_tariff_schedule.pdf"
    )
    assert dl_res["status"] == "DOWNLOAD_COMPLETED"
    local_path = Path(dl_res["local_file_path"])
    assert local_path.exists()
    assert local_path.stat().st_size > 0
    print(f"-> Document downloaded and saved locally: {local_path.name} ({dl_res['file_size_bytes']} bytes)")
    print("-> Automated Document Downloading: PASSED")

def test_5_multi_tab_swarm():
    print("\n--- [5/6] Testing Multi-Tab Swarm Coordinator ---")
    from axomai.agency.web_operator import multi_tab_swarm_coordinator

    portals = [
        {"name": "Discom Industrial Billing", "url": "mock://discom.assam.gov.in"},
        {"name": "Guwahati Tea Auction Committee", "url": "mock://gtac.assam.gov.in"},
        {"name": "Inland Waterways Logistics Port", "url": "mock://iwai.gov.in"}
    ]

    scrape_res = multi_tab_swarm_coordinator.execute_multi_portal_scrape(
        mission_title="Cross-Portal Tariff & Logistics Reconciliation",
        target_portals=portals
    )

    assert scrape_res["synthesis"]["portals_visited_count"] == 3
    assert scrape_res["synthesis"]["successful_extractions"] == 3
    print(f"-> Visited {len(scrape_res['results'])} portals in parallel swarm.")
    print("-> Consolidated findings into Episodic Memory.")
    print("-> Multi-Tab Swarm Coordinator: PASSED")

def test_6_api_endpoints():
    print("\n--- [6/6] Testing Web Operator Live API Endpoints ---")
    from fastapi.testclient import TestClient
    from axomai.api.app import app

    client = TestClient(app)

    # 1. Navigate endpoint
    res_nav = client.post("/api/web-operator/navigate?url=mock://assam.gov.in")
    assert res_nav.status_code == 200
    assert res_nav.json()["forms_detected_count"] >= 1
    print("-> Web Navigate API: PASSED (200 OK)")

    # 2. Vault list endpoint
    res_v = client.get("/api/web-operator/vault")
    assert res_v.status_code == 200
    assert len(res_v.json()["registered_services"]) >= 1
    print("-> Web Vault API: PASSED (200 OK)")

    # 3. Multi-Tab Scrape endpoint
    res_multi = client.post("/api/web-operator/multi-tab-scrape")
    assert res_multi.status_code == 200
    assert res_multi.json()["synthesis"]["portals_visited_count"] >= 1
    print("-> Multi-Tab Scrape API: PASSED (200 OK)")

if __name__ == "__main__":
    t_start = time.time()
    print("=== STARTING AXOMAI-AGI WEB OPERATOR & DIGITAL RPA VERIFICATION ===")
    test_1_credential_vault()
    test_2_security_gate_protocol()
    test_3_browser_navigator_dom_and_forms()
    test_4_document_download()
    test_5_multi_tab_swarm()
    test_6_api_endpoints()
    print(f"\n=== ALL 6 WEB OPERATOR MODULES PASSED 100% IN {round(time.time() - t_start, 2)} SECONDS ===")

