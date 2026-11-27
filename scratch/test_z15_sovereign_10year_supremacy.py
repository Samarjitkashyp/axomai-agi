"""
Automated Sovereign Verification Suite for Z15 Sovereign (14-Tool Arsenal).
Validates all 8 Indian Sovereign Cybersecurity Pillars + Existing Enterprise Suite with 100% rigor.
No mocks or shortcuts.
"""

import sys
from pathlib import Path

# Add src to pythonpath
src_dir = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(src_dir))

from axomai.agents.z15_sovereign.tools import (
    cve_scanner,
    compliance_framework,
    mitre_adversary_profiler,
    sbom_analyzer,
    llm_guardrail_shield,
    deception_grid,
    cert_in_reporter,
    dpdp_shield,
    nciipc_shield,
    rbi_npci_shield,
    pqc_shield,
    ebpf_hotpatcher,
    cart_auditor,
    sovereign_cti
)
from axomai.agents.z15_sovereign.agent import z15_sovereign_agent
from axomai.agents.master_orchestrator import master_orchestrator

def test_sovereign_suite():
    print("=" * 80)
    print("🇮🇳 RUNNING Z15 SOVEREIGN 10-YEAR SUPREMACY VERIFICATION SUITE")
    print("=" * 80)

    # 1. CERT-In 6-Hour Statutory Incident Reporter
    print("\n--- 1. Testing CERT-In 6-Hour Statutory Incident Reporter ---")
    cert_dossier = cert_in_reporter.generate_statutory_incident_dossier(
        incident_type="Ransomware attack attempting database encryption",
        affected_system_name="Core_Banking_PostgreSQL_Cluster_01",
        threat_vector="Compromised edge gateway credentials with privilege escalation"
    )
    assert cert_dossier["statutory_compliance_status"] == "COMPLIANT_WITHIN_6_HOURS"
    assert "CERTIN-IND-" in cert_dossier["incident_reference_id"]
    assert cert_dossier["statutory_deadline_hours_remaining"] > 0
    print(f"CERT-In Dossier Ref: {cert_dossier['incident_reference_id']}")
    print(f"Compliance Status: {cert_dossier['statutory_compliance_status']} ({cert_dossier['time_elapsed_since_detection_hours']} hrs elapsed)")
    print("✅ 1. CERT-In Incident Reporter: PASSED")

    # 2. DPDP Act 2023 Data Fiduciary & ₹250 Cr Penalty Shield
    print("\n--- 2. Testing DPDP Act 2023 Data Fiduciary & Penalty Shield ---")
    sample_payload = (
        "Customer Aadhaar: 4521 8890 1234, PAN Card: ABCDE9988K, UPI VPA: rohit@okhdfcbank. "
        "Storage secured with AES-256 and encrypted customer audit logs."
    )
    dpdp_audit = dpdp_shield.audit_data_fiduciary_compliance(sample_payload)
    assert dpdp_audit["total_pii_entities_detected"] >= 3
    assert dpdp_audit["compliance_score_pct"] >= 80.0
    assert dpdp_audit["potential_penalty_exposure_inr_cr"] == 0.0

    dpbi_notice = dpdp_shield.draft_dpbi_breach_intimation(
        incident_description="Unauthorized API scrape attempt mitigated by Z15 honeytokens",
        affected_data_principals_count=150,
        affected_pii_types=["Aadhaar", "PAN", "UPI_VPA"]
    )
    assert "Data Protection Board of India" in dpbi_notice["statutory_recipient"]
    print(f"DPDP Compliance Score: {dpdp_audit['compliance_score_pct']}% | Sovereign PII Detected: {dpdp_audit['total_pii_entities_detected']}")
    print(f"Statutory Shield: {dpdp_audit['statutory_shield_verdict']}")
    print("✅ 2. DPDP Act 2023 Shield: PASSED")

    # 3. NCIIPC Critical National Infrastructure SCADA/OT Grid Shield
    print("\n--- 3. Testing NCIIPC Critical National Infrastructure SCADA/OT Shield ---")
    grid_audit = nciipc_shield.audit_scada_telemetry(
        sector="Power & Energy (National Grid)",
        substation_name="Western_Grid_Substation_765KV",
        grid_frequency_hz=49.40,  # Critical desync
        unauthorized_coil_writes=3
    )
    assert "RED_CRITICAL" in grid_audit["threat_classification"]
    assert grid_audit["nciipc_sop_isolation_playbook"]["substation_isolated"] is True
    print(f"Grid Threat Classification: {grid_audit['threat_classification']}")
    print(f"Substation Air-Gap Engaged: {grid_audit['nciipc_sop_isolation_playbook']['substation_isolated']}")
    print("✅ 3. NCIIPC SCADA/OT Grid Shield: PASSED")

    # 4. RBI Cyber Resilience & NPCI UPI Fraud Interceptor
    print("\n--- 4. Testing RBI Cyber Resilience & NPCI UPI Fraud Interceptor ---")
    rbi_audit = rbi_npci_shield.audit_rbi_cyber_governance()
    assert rbi_audit["readiness_score_pct"] == 100.0

    upi_intercept = rbi_npci_shield.intercept_npci_upi_fraud(
        sender_vpa="victim@okhdfc",
        receiver_vpa="mule_syndicate@ybl",
        amount_inr=95000.0,
        transaction_count_last_10_mins=14,
        sim_swap_in_last_24_hours=True
    )
    assert upi_intercept["transaction_verdict"] == "BLOCKED_MULE_ACCOUNT_QUARANTINE"
    assert upi_intercept["fraud_probability_score"] >= 95.0
    print(f"RBI Cyber Readiness: {rbi_audit['readiness_score_pct']}%")
    print(f"UPI Interception Verdict: {upi_intercept['transaction_verdict']} (Score: {upi_intercept['fraud_probability_score']})")
    print("✅ 4. RBI & NPCI UPI Cyber Resilience: PASSED")

    # 5. Post-Quantum Cryptography (PQC) Shield
    print("\n--- 5. Testing Post-Quantum Cryptography (PQC) & NQM Shield ---")
    pqc_audit = pqc_shield.audit_cryptographic_inventory(
        tls_cipher_suites=["TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"],
        root_ca_signature_alg="RSA-2048"
    )
    assert pqc_audit["hndl_threat_verdict"] == "CRITICAL_RETROACTIVE_DECRYPTION_RISK"
    assert "ML-KEM" in pqc_audit["nist_pqc_target_standards"]
    print(f"PQC Threat Verdict: {pqc_audit['hndl_threat_verdict']}")
    print(f"PQC Target Standards: {list(pqc_audit['nist_pqc_target_standards'].keys())}")
    print("✅ 5. Post-Quantum Cryptography Shield: PASSED")

    # 6. eBPF Linux Kernel Autonomous Zero-Day Interceptor
    print("\n--- 6. Testing eBPF Linux Kernel Virtual Hot-Patcher ---")
    ebpf_patch = ebpf_hotpatcher.synthesize_ebpf_virtual_hotpatch(
        cve_id="CVE-2024-3094",
        vulnerable_binary_name="sshd"
    )
    assert "EBPF-PATCH-" in ebpf_patch["patch_reference_id"]
    assert ebpf_patch["server_restart_required"] is False
    assert "lsm/bprm_check_security" in ebpf_patch["compiled_ebpf_c_source"]
    print(f"eBPF Patch ID: {ebpf_patch['patch_reference_id']}")
    print(f"Kernel Hook Point: {ebpf_patch['kernel_hook_point']} | Reboot Required: {ebpf_patch['server_restart_required']}")
    print("✅ 6. eBPF Kernel Hot-Patcher: PASSED")

    # 7. Continuous Automated Red-Teaming (CART) Auditor
    print("\n--- 7. Testing CART Continuous Defensive Auditor ---")
    cart_res = cart_auditor.run_continuous_red_team_audit()
    assert cart_res["actionable_vulnerabilities_confirmed"] >= 1
    assert "Python FastAPI Defensive" in cart_res["findings"][0]["automated_patch_snippet"]
    print(f"CART Health Score: {cart_res['security_posture_health_pct']}% | Confirmed Zero-Days: {cart_res['actionable_vulnerabilities_confirmed']}")
    print(f"Patch Ready: {cart_res['remediation_status']}")
    print("✅ 7. CART Continuous Red-Teaming: PASSED")

    # 8. Sovereign Cyber Threat Intelligence (CTI) Fusion Engine
    print("\n--- 8. Testing Sovereign CTI Fusion Engine ---")
    cti_res = sovereign_cti.scan_sovereign_threat_feeds()
    assert cti_res["connected_threat_feeds_count"] == 5
    assert len(cti_res["active_threat_pulses"]) >= 2
    print(f"Active Sovereign Threat Feeds: {cti_res['connected_threat_feeds_count']}")
    print(f"Threat Exposure Index: {cti_res['threat_exposure_index']} ({cti_res['exposure_grade']})")
    print("✅ 8. Sovereign CTI Fusion Engine: PASSED")

    # 9. Master Z15 Sovereign 14-Tool Live Stream Execution
    print("\n--- 9. Testing Master Z15 Sovereign 14-Tool Live Execution ---")
    query = "Perform sovereign cyber defense audit for critical national infrastructure power grid with CERT-In and DPDP Act compliance"
    stream_events = list(z15_sovereign_agent.cyber_defense_stream(query))
    
    meta_events = [e for e in stream_events if e.get("type") == "meta"]
    final_events = [e for e in stream_events if e.get("type") == "final"]

    assert len(meta_events) == 1
    meta = meta_events[0]
    assert meta["tools_count"] == 14
    assert len(meta["tools_used"]) == 14
    assert len(final_events) == 1
    final_doc = final_events[0]["content"]

    assert "CERT-In Status" in final_doc
    assert "DPDP Act, 2023" in final_doc
    assert "NCIIPC" in final_doc
    assert "eBPF Virtual Hot-Patching" in final_doc

    print(f"Total Master Stream Events: {len(stream_events)}")
    print(f"Total Tools Orchestrated: {meta['tools_count']} tools")
    print(f"Tools List: {meta['tools_used']}")
    print("✅ 9. Master Z15 Sovereign 14-Tool Execution: 100% PASSED")

    # 10. Master Orchestrator Intent Routing
    print("\n--- 10. Testing Master Orchestrator Intent Routing to Z15 ---")
    routing_res = master_orchestrator.route_intent("Draft CERT-In 6-hour incident report for ransomware attack")
    assert routing_res["agent"] == "z15"
    assert routing_res["name"] == "Z15 Sovereign"
    print(f"Routing Intent Test: '{routing_res['name']}' selected with confidence {routing_res['confidence']}")
    print("✅ 10. Master Orchestrator Routing: PASSED")

    print("\n" + "=" * 80)
    print("🏆 ALL 8 SOVEREIGN DEFENSE MODULES + MASTER 14-TOOL SUITE PASSED 100%!")
    print("=" * 80)

if __name__ == "__main__":
    test_sovereign_suite()
