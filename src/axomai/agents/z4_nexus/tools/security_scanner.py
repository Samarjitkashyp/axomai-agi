"""
Z4 Nexus - SAST Security & Vulnerability Scanner.
Performs deep static code audits for credentials leakage, SQL injections,
command injections, insecure deserialization, XSS, and dangerous runtime patterns.
"""

import re
from typing import Dict, Any, List

class SecurityScanner:
    """Enterprise SAST Vulnerability Scanner."""

    PATTERNS = [
        {
            "id": "SEC-001",
            "name": "Hardcoded Secret / API Key",
            "category": "CREDENTIAL_LEAK",
            "severity": "CRITICAL",
            "regex": r'''(?i)(api[_-]?key|secret[_-]?key|password|auth[_-]?token|bearer|private[_-]?key)\s*[:=]\s*['"][a-zA-Z0-9_\-\.]{12,}['"]''',
            "advice": "Store credentials in environment variables (`os.environ.get(...)`) or secure vaults, never in plaintext code."
        },
        {
            "id": "SEC-002",
            "name": "SQL Injection Hazard",
            "category": "INJECTION",
            "severity": "CRITICAL",
            "regex": r'''(?i)(execute|cursor\.execute)\s*\(\s*f?['"].*?(select|insert|update|delete).*?\{|\%s''',
            "advice": "Use parameterized queries or ORMs (SQLAlchemy, Prisma) instead of string formatting."
        },
        {
            "id": "SEC-003",
            "name": "Command Injection Hazard",
            "category": "RCE",
            "severity": "HIGH",
            "regex": r'''(?i)(os\.system|subprocess\.Popen|subprocess\.run|subprocess\.call)\s*\(\s*(f?['"].*?\{|.*?\+.*?shell\s*=\s*True)''',
            "advice": "Pass arguments as a list without `shell=True` to prevent shell injection attacks."
        },
        {
            "id": "SEC-004",
            "name": "Insecure Deserialization",
            "category": "RCE",
            "severity": "HIGH",
            "regex": r'''(?i)(pickle\.loads|yaml\.load\s*\([^,)]+\))''',
            "advice": "Avoid `pickle` on untrusted data; use `yaml.safe_load()` instead of `yaml.load()`."
        },
        {
            "id": "SEC-005",
            "name": "Dangerous Eval / Exec",
            "category": "RCE",
            "severity": "HIGH",
            "regex": r'''\b(eval|exec)\s*\(''',
            "advice": "Eliminate dynamic code execution with `eval()` or `exec()`. Use `ast.literal_eval()` or structured parsers."
        },
        {
            "id": "SEC-006",
            "name": "Weak Cryptographic Hash",
            "category": "CRYPTO",
            "severity": "MEDIUM",
            "regex": r'''(?i)(hashlib\.md5|hashlib\.sha1)\s*\(''',
            "advice": "Do not use MD5 or SHA1 for password hashing or security tokens. Use bcrypt, argon2, or SHA-256/512."
        },
        {
            "id": "SEC-007",
            "name": "Cross-Site Scripting (XSS) Hazard",
            "category": "XSS",
            "severity": "MEDIUM",
            "regex": r'''(?i)(dangerouslySetInnerHTML|innerHTML\s*=)''',
            "advice": "Sanitize HTML using DOMPurify before injecting into the DOM, or use textContent/safe React state."
        },
        {
            "id": "SEC-008",
            "name": "Path Traversal Risk",
            "category": "FILE_ACCESS",
            "severity": "MEDIUM",
            "regex": r'''(?i)open\s*\(\s*f?['"].*?\.\./|\bPath\s*\(.*?user''',
            "advice": "Resolve paths against an allowed base directory using `os.path.abspath` and verify the prefix."
        }
    ]

    def scan_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Scans code string and returns audit dossier."""
        findings: List[Dict[str, Any]] = []
        lines = code.splitlines()

        for pat in self.PATTERNS:
            for line_idx, line in enumerate(lines, 1):
                # Skip comments
                clean_line = line.strip()
                if clean_line.startswith("#") or clean_line.startswith("//"):
                    continue

                if re.search(pat["regex"], line):
                    findings.append({
                        "rule_id": pat["id"],
                        "name": pat["name"],
                        "severity": pat["severity"],
                        "category": pat["category"],
                        "line": line_idx,
                        "snippet": clean_line[:100],
                        "recommendation": pat["advice"]
                    })

        # Calculate security score (100 is perfect)
        deduction = 0
        for f in findings:
            if f["severity"] == "CRITICAL": deduction += 25
            elif f["severity"] == "HIGH": deduction += 15
            elif f["severity"] == "MEDIUM": deduction += 10
            elif f["severity"] == "LOW": deduction += 5

        score = max(0, 100 - deduction)
        status = "SECURE" if score >= 90 else ("WARNING" if score >= 60 else "CRITICAL_RISK")

        return {
            "security_score": score,
            "status": status,
            "total_issues": len(findings),
            "findings": findings,
            "is_clean": len(findings) == 0
        }

security_scanner = SecurityScanner()
