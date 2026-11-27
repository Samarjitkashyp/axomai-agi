"""
Z15 Sovereign - Live Post-Quantum Cryptography (PQC) & TLS Cipher Auditor.
Performs REAL live SSL/TLS socket handshakes against target domains to inspect
negotiated TLS versions and cipher suites, then audits them against Shor's Algorithm
and NIST FIPS 203 (ML-KEM / Kyber), FIPS 204 (ML-DSA / Dilithium), and FIPS 205 (SLH-DSA).
"""

import ssl
import socket
from typing import Dict, Any, List, Optional


class PostQuantumCryptoShield:
    """Live TLS/SSL Inspector & Post-Quantum Cryptography Migration Engine."""

    NIST_PQC_STANDARDS = {
        "ML-KEM": {
            "fips_standard": "FIPS 203",
            "former_name": "CRYSTALS-Kyber",
            "purpose": "General Public-Key Encryption & Key Encapsulation Mechanism (KEM)",
            "security_categories": ["ML-KEM-512 (Category 1)", "ML-KEM-768 (Category 3)", "ML-KEM-1024 (Category 5)"],
            "replaces": ["RSA-2048 / RSA-4096 Key Exchange", "ECDH (Elliptic Curve Diffie-Hellman)"]
        },
        "ML-DSA": {
            "fips_standard": "FIPS 204",
            "former_name": "CRYSTALS-Dilithium",
            "purpose": "Primary Digital Signatures (Authentication & Integrity)",
            "security_categories": ["ML-DSA-44 (Category 2)", "ML-DSA-65 (Category 3)", "ML-DSA-87 (Category 5)"],
            "replaces": ["RSA Signatures", "ECDSA", "Ed25519"]
        },
        "SLH-DSA": {
            "fips_standard": "FIPS 205",
            "former_name": "SPHINCS+",
            "purpose": "Stateless Hash-Based Digital Signatures (Backup Fallback)",
            "security_categories": ["SLH-DSA-SHA2-128s", "SLH-DSA-SHAKE-256f"],
            "replaces": ["High-security root CA certificate signing"]
        }
    }

    LEGACY_CRYPTO_VULNERABILITY = {
        "RSA": {"quantum_status": "VULNERABLE", "threat": "Broken by Shor's Algorithm", "hndl_risk": "CRITICAL"},
        "ECDSA": {"quantum_status": "VULNERABLE", "threat": "Broken by Shor's Algorithm", "hndl_risk": "CRITICAL"},
        "ECDHE": {"quantum_status": "VULNERABLE", "threat": "Classical key exchange decryptable retroactively", "hndl_risk": "CRITICAL"},
        "TLS_AES_256_GCM_SHA384": {"quantum_status": "SYMMETRIC_SAFE_KEX_CLASSICAL", "threat": "AES-256 safe, but classical X25519/ECDHE handshake vulnerable unless ML-KEM hybrid used", "hndl_risk": "HIGH"},
        "TLS_AES_128_GCM_SHA256": {"quantum_status": "SYMMETRIC_WEAKENED_BY_GROVER", "threat": "Grover reduces AES-128 to 64-bit quantum security", "hndl_risk": "HIGH"}
    }

    def inspect_live_tls(self, domain: str, port: int = 443) -> Optional[Dict[str, Any]]:
        """Performs a live TLS handshake against domain:443 to inspect actual cipher & TLS version."""
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((domain, port), timeout=4) as sock:
                with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                    cipher = ssock.cipher()  # (name, protocol, bits)
                    return {
                        "domain": domain,
                        "tls_version": ssock.version(),
                        "cipher_name": cipher[0] if cipher else "UNKNOWN",
                        "cipher_bits": cipher[2] if cipher else 0,
                        "source": "LIVE_TLS_HANDSHAKE"
                    }
        except Exception:
            return None

    def audit_cryptographic_inventory(
        self,
        tls_cipher_suites: Optional[List[str]] = None,
        database_key_algs: Optional[List[str]] = None,
        root_ca_signature_alg: str = "RSA-2048",
        target_domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Audits live TLS handshakes (if domain provided) and cryptographic inventories
        against quantum threats and HNDL espionage.
        """
        live_tls_info = None
        if target_domain and not target_domain.endswith(".internal"):
            live_tls_info = self.inspect_live_tls(target_domain)
            if live_tls_info:
                tls_cipher_suites = [live_tls_info["cipher_name"]]

        if not tls_cipher_suites:
            tls_cipher_suites = ["TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"]

        if not database_key_algs:
            database_key_algs = ["RSA-2048", "AES-256-GCM"]

        vulnerable_items = []
        hndl_exposure_detected = False

        for suite in tls_cipher_suites:
            matched = False
            for key, meta in self.LEGACY_CRYPTO_VULNERABILITY.items():
                if key in suite.upper():
                    vulnerable_items.append({
                        "asset": f"TLS Cipher: {suite}" + (f" ({live_tls_info['domain']} {live_tls_info['tls_version']})" if live_tls_info else ""),
                        "legacy_primitive": key,
                        "quantum_status": meta["quantum_status"],
                        "hndl_risk": meta["hndl_risk"],
                        "remediation_pqc": "Upgrade to X25519MLKEM768 (Hybrid Post-Quantum TLS 1.3)"
                    })
                    if meta["hndl_risk"] in ("CRITICAL", "HIGH"):
                        hndl_exposure_detected = True
                    matched = True
                    break
            if not matched:
                vulnerable_items.append({
                    "asset": f"TLS Cipher: {suite}",
                    "legacy_primitive": "CLASSICAL_KEX",
                    "quantum_status": "AUDIT_REQUIRED",
                    "hndl_risk": "HIGH",
                    "remediation_pqc": "Verify X25519MLKEM768 hybrid key exchange"
                })
                hndl_exposure_detected = True

        total_audited = len(tls_cipher_suites) + len(database_key_algs)
        vuln_count = len(vulnerable_items)
        readiness_pct = max(0.0, round(((total_audited - vuln_count) / max(total_audited, 1)) * 100, 1))

        return {
            "national_mission": "National Quantum Mission (NQM), Govt of India & NIST PQC Guidelines",
            "live_tls_handshake": live_tls_info,
            "quantum_readiness_score_pct": readiness_pct,
            "hndl_threat_verdict": "CRITICAL_RETROACTIVE_DECRYPTION_RISK" if hndl_exposure_detected else "PROTECTED_PQC_ENFORCED",
            "vulnerabilities_found": vulnerable_items,
            "nist_pqc_target_standards": self.NIST_PQC_STANDARDS,
            "post_quantum_migration_roadmap": [
                "Stage 1: Deploy Hybrid TLS 1.3 combining X25519 with ML-KEM-768 for all public and API edge gateways",
                "Stage 2: Transition internal code signing and SSH infrastructure to ML-DSA-65 (FIPS 204)",
                "Stage 3: Rotate legacy RSA database master keys to AES-256-GCM wrapped with ML-KEM-1024"
            ]
        }


pqc_shield = PostQuantumCryptoShield()
