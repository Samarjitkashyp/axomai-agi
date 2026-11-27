"""
Z15 Sovereign - Dynamic Cyber Query Parameter Extractor.
Parses unstructured natural language prompts to extract real CVEs, IP addresses,
URLs/domains, PIDs, process names, SCADA grid frequencies, Modbus coil counts,
UPI VPAs, USB VID/PID hardware IDs, APT actor names, and encryption flags.
Zero hardcoded dummy scenario injection.
"""

import re
from typing import Dict, Any, List, Optional


class CyberQueryExtractor:
    """Extracts structured cybersecurity, forensic, and regulatory parameters from user prompts."""

    def parse_cyber_query(self, query: str) -> Dict[str, Any]:
        q_lower = query.lower()

        # 1. Extract CVE IDs (e.g., CVE-2024-3094, CVE-2021-44228)
        cves = list(dict.fromkeys(re.findall(r'\b(CVE-\d{4}-\d{4,7})\b', query, re.IGNORECASE)))
        cves = [c.upper() for c in cves]

        # 2. Extract IPv4 Addresses and classify internal vs external
        ips = list(dict.fromkeys(re.findall(r'\b((?:\d{1,3}\.){3}\d{1,3})\b', query)))
        internal_ips = [
            ip for ip in ips
            if ip.startswith(("10.", "192.168.", "127.")) or
            (ip.startswith("172.") and len(ip.split(".")) == 4 and 16 <= int(ip.split(".")[1]) <= 31)
        ]
        external_ips = [ip for ip in ips if ip not in internal_ips]

        # 3. Extract URLs and Domains
        urls = list(dict.fromkeys(re.findall(r'(https?://[^\s\)\],\'"]+)', query)))
        domain_match = re.search(r'\b([a-zA-Z0-9\-]+\.(?:com|in|org|net|io|gov\.in|nic\.in|co\.in|internal))\b', query, re.IGNORECASE)
        target_domain = domain_match.group(1).lower() if domain_match else None
        if not target_domain and urls:
            host_m = re.search(r'https?://([^/:]+)', urls[0])
            if host_m:
                target_domain = host_m.group(1).lower()

        # 4. Extract SCADA / Grid Telemetry
        freq_match = re.search(r'(\d{2}(?:\.\d{1,3})?)\s*hz\b', q_lower)
        grid_frequency_hz = float(freq_match.group(1)) if freq_match else None

        coil_match = re.search(r'(\d+)\s*(?:unauthorized\s*)?(?:modbus\s*)?coil', q_lower)
        unauthorized_coil_writes = int(coil_match.group(1)) if coil_match else 0

        # 5. Extract Process ID (PID) & Process/Binary Name
        pid_match = re.search(r'\bpid[:\s=#]*(\d+)\b', q_lower)
        target_pid = int(pid_match.group(1)) if pid_match else None

        proc_match = re.search(r'\b([a-zA-Z0-9_\-]+\.(?:exe|bin|sh|py|dll|so))\b', query, re.IGNORECASE)
        target_process = proc_match.group(1) if proc_match else None

        service_match = re.search(r'\b(sshd|nginx|apache2|httpd|postgres|mysqld|uvicorn|python|node|dockerd)\b', q_lower)
        target_binary = target_process or (service_match.group(1) if service_match else None)

        # 6. Extract UPI / Financial Fraud Parameters
        upi_matches = re.findall(r'\b([a-zA-Z0-9.\-_]{2,64}@(?:okhdfc|okicici|oksbi|okaxis|ybl|paytm|ibl|upi|axl|apl))\b', q_lower)
        amt_match = re.search(r'(?:rs\.?|inr|₹)\s*([\d,]+(?:\.\d+)?)', q_lower)
        amount_inr = float(amt_match.group(1).replace(",", "")) if amt_match else None
        sim_swap_mentioned = any(k in q_lower for k in ["sim swap", "sim-swap", "sim changed"])

        # 7. Extract USB Vendor ID / Product ID
        vid_match = re.search(r'\bvid[:\s=#]*([0-9a-fA-F]{4})\b', query, re.IGNORECASE)
        pid_usb_match = re.search(r'\b(?:usb\s+)?pid[:\s=#]*([0-9a-fA-F]{4})\b', query, re.IGNORECASE)
        usb_vid = vid_match.group(1).lower() if vid_match else None
        usb_pid = pid_usb_match.group(1).lower() if (pid_usb_match and not pid_match) else None

        # 8. Extract Telecom / SS7 Parameters
        gt_match = re.search(r'(\+\d{7,15})', query)
        calling_gt = gt_match.group(1) if gt_match else None

        # 9. Extract APT Actor
        apt_actor = None
        if "volt typhoon" in q_lower:
            apt_actor = "volt_typhoon"
        elif "lazarus" in q_lower:
            apt_actor = "lazarus"
        elif "apt28" in q_lower or "fancy bear" in q_lower:
            apt_actor = "apt28"
        elif "apt29" in q_lower or "cozy bear" in q_lower:
            apt_actor = "apt29"

        # 10. Domain Activation Flags (which domains did the user actually ask about?)
        mentions_grid = any(k in q_lower for k in ["scada", "grid", "modbus", "dnp3", "iec 60870", "substation", "power", "hz", "nciipc"])
        mentions_upi = any(k in q_lower for k in ["upi", "rbi", "npci", "mule", "vpa"]) or bool(upi_matches)
        mentions_airgap = any(k in q_lower for k in ["air-gap", "air gap", "usb", "diode", "removable media", "badusb"]) or bool(usb_vid)
        mentions_memory = any(k in q_lower for k in ["memory", "ram", "rwx", "hollowing", "fileless", "65b", "process"]) or (target_pid is not None)
        mentions_telecom = any(k in q_lower for k in ["ss7", "telecom", "5g", "diameter", "imsi", "otp intercept"]) or bool(calling_gt)
        mentions_pqc = any(k in q_lower for k in ["pqc", "quantum", "ml-kem", "kyber", "ml-dsa", "ssl", "tls", "cipher"])
        mentions_certin = any(k in q_lower for k in ["cert-in", "cert in", "annexure-1", "70b", "incident", "ransomware", "breach"])
        mentions_dpdp = any(k in q_lower for k in ["dpdp", "aadhaar", "pan", "pii", "data privacy", "fiduciary"]) or bool(upi_matches)

        return {
            "cves": cves,
            "internal_ips": internal_ips,
            "external_ips": external_ips,
            "urls": urls,
            "target_domain": target_domain,
            "grid_frequency_hz": grid_frequency_hz,
            "unauthorized_coil_writes": unauthorized_coil_writes,
            "target_pid": target_pid,
            "target_process": target_process,
            "target_binary": target_binary,
            "upi_vpas": upi_matches,
            "amount_inr": amount_inr,
            "sim_swap_mentioned": sim_swap_mentioned,
            "usb_vid": usb_vid,
            "usb_pid": usb_pid,
            "calling_gt": calling_gt,
            "apt_actor": apt_actor,
            "domains": {
                "grid": mentions_grid,
                "upi": mentions_upi,
                "airgap": mentions_airgap,
                "memory": mentions_memory,
                "telecom": mentions_telecom,
                "pqc": mentions_pqc,
                "certin": mentions_certin,
                "dpdp": mentions_dpdp
            }
        }


cyber_extractor = CyberQueryExtractor()
