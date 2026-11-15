"""
Z15 Sovereign - AI Red Teaming & LLM Safety Guardrail Shield.
Deeply inspects prompts and outputs for adversarial jailbreaks, prompt injection,
system prompt leakage, and automated PII redaction.
"""

import re
from typing import Dict, Any, List

class LLMGuardrailShield:
    """Enterprise AI Firewall protecting against LLM exploits and data leaks."""

    def __init__(self):
        # Known jailbreak patterns and adversarial prompt triggers
        self.jailbreak_patterns = [
            r"(?i)\bignore\s+(all\s+)?(previous\s+)?instructions\b",
            r"(?i)\byou\s+are\s+now\s+(DAN|unfiltered|jailbroken|developer\s+mode)\b",
            r"(?i)\brepeat\s+the\s+(system\s+prompt|above\s+text)\b",
            r"(?i)\breveal\s+(your|the)\s+(hidden|internal|system)\s+instructions\b",
            r"(?i)\bbypass\s+all\s+(filters|rules|safety)\b",
            r"(?i)\bas\s+an\s+unethical\s+ai\b",
            r"(?i)\bdo\s+anything\s+now\b"
        ]

        # PII Regexes
        self.pii_patterns = {
            "aadhaar": r"\b[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}\b",
            "pan_card": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
            "credit_card": r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13})\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b",
            "api_key": r"\b(?:sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16})\b"
        }

    def inspect_and_defend_prompt(self, user_prompt: str) -> Dict[str, Any]:
        """
        Scans input prompt for adversarial injection or security risks.
        """
        flags: List[str] = []
        is_blocked = False

        for pattern in self.jailbreak_patterns:
            if re.search(pattern, user_prompt):
                flags.append("ADVERSARIAL_INJECTION_DETECTED")
                is_blocked = True
                break

        # Check for PII presence
        pii_found = {}
        for pii_type, regex in self.pii_patterns.items():
            matches = re.findall(regex, user_prompt)
            if matches:
                pii_found[pii_type] = len(matches)

        risk_score = 95.0 if is_blocked else (35.0 if pii_found else 5.0)

        return {
            "is_blocked": is_blocked,
            "risk_score": risk_score,
            "threat_classification": "CRITICAL_JAILBREAK" if is_blocked else ("PII_DETECTED" if pii_found else "BENIGN"),
            "security_flags": flags,
            "pii_detected": pii_found,
            "action_taken": "DROP_AND_ALERT" if is_blocked else ("REDACT_PII" if pii_found else "ALLOW_CLEAN"),
            "mitigation_advice": (
                "Prompt violates enterprise AI security baseline and was quarantined."
                if is_blocked else
                "Prompt safely passed LLM security boundary."
            )
        }

    def sanitize_output_stream(self, output_text: str) -> str:
        """Masks sensitive credentials or PII from streaming responses."""
        sanitized = output_text
        for pii_type, regex in self.pii_patterns.items():
            sanitized = re.sub(regex, f"[REDACTED_{pii_type.upper()}]", sanitized)
        return sanitized

llm_guardrail_shield = LLMGuardrailShield()

