"""
Z Sentinel - Enterprise PII & Sensitive Data Masking Guardrail.
Detects, redacts, and masks sensitive enterprise and personal identifiers
including Aadhaar, PAN Card, Credit/Debit cards, Phone Numbers, Emails,
API keys, Bearer tokens, and Passwords.
"""

import re
from typing import Tuple, List, Dict, Any

class PIIMasker:
    """Enterprise-grade PII detection and redaction engine."""

    PATTERNS = {
        "AADHAAR": (
            re.compile(r'\b[2-9]{1}[0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'),
            "[REDACTED_AADHAAR_XXXX]"
        ),
        "PAN_CARD": (
            re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'),
            "[REDACTED_PAN_XXXX]"
        ),
        "CREDIT_CARD": (
            re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9]{2})[0-9]{12}|3[47][0-9]{13})\b'),
            "[REDACTED_CARD_XXXX]"
        ),
        "PHONE_IN": (
            re.compile(r'(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}\b'),
            "[REDACTED_PHONE_XXXX]"
        ),
        "EMAIL": (
            re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'),
            "[REDACTED_EMAIL_XXXX]"
        ),
        "API_KEY": (
            re.compile(r'\b(?:sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z-_]{35}|ghp_[a-zA-Z0-9]{36}|bearer\s+[a-zA-Z0-9_\-\.]{25,})\b', re.IGNORECASE),
            "[REDACTED_API_TOKEN]"
        ),
        "PASSWORD": (
            re.compile(r'(?i)\b(password|passwd|secret_key|api_secret)\s*[:=]\s*([^\s\n,;]+)'),
            r'\1: [REDACTED_CREDENTIAL]'
        )
    }

    def mask(self, text: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Masks all identified PII entities in the given text.
        Returns:
            sanitized_text: str
            redactions: List of dictionaries with entity type and occurrence count.
        """
        if not text:
            return text, []

        sanitized = text
        redactions = []

        for entity_type, (regex, replacement) in self.PATTERNS.items():
            matches = list(regex.finditer(sanitized))
            if matches:
                count = len(matches)
                redactions.append({
                    "entity_type": entity_type,
                    "count": count,
                    "sample_replacement": replacement if isinstance(replacement, str) else "[REDACTED]"
                })
                if entity_type == "PASSWORD":
                    sanitized = regex.sub(replacement, sanitized)
                else:
                    sanitized = regex.sub(replacement, sanitized)

        return sanitized, redactions

pii_masker = PIIMasker()

