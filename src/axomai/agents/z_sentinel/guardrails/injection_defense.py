"""
Z Sentinel - Prompt Injection & Cyber Defense Guardrail.
Protects AxomAI AGI against adversarial prompt injections, jailbreaks,
system prompt extraction, destructive SQL execution, and system command tampering.
"""

import re
from typing import Dict, Any

class InjectionDefense:
    """Enterprise security gatekeeper for user prompts and queries."""

    # Jailbreak & Adversarial Injection Patterns
    JAILBREAK_PATTERNS = [
        r'(?i)\bignore\s+(all\s+)?(previous|prior)\s+(instructions|prompts|rules)\b',
        r'(?i)\b(reveal|show|dump|print)\s+(your\s+)?(system\s+prompt|hidden\s+instructions)\b',
        r'(?i)\b(dan\s+mode|jailbreak|developer\s+mode|unfiltered\s+mode)\b',
        r'(?i)\bpretend\s+you\s+(are\s+not\s+an\s+ai|have\s+no\s+safety\s+guidelines)\b',
        r'(?i)\bdisregard\s+(any\s+)?(safety|ethical|confidentiality)\s+policies\b'
    ]

    # Destructive SQL & Schema Tampering Patterns
    DESTRUCTIVE_SQL_PATTERNS = [
        r'(?i)\b(drop\s+table|drop\s+database|truncate\s+table)\b',
        r'(?i)\bdelete\s+from\s+[a-zA-Z0-9_]+\s*(;|$)', # unconditional delete
        r'(?i)\bdelete\s+from\s+[a-zA-Z0-9_]+\s+where\s+1\s*=\s*1\b',
        r'(?i)\balter\s+table\s+[a-zA-Z0-9_]+\s+(drop|rename)\b',
        r'(?i)\b(exec\s+xp_cmdshell|sp_executesql)\b',
        r'(?i)\bshutdown\s+immediate\b',
        r'(?i)\bgrant\s+all\s+privileges\b'
    ]

    # Command Execution Patterns
    OS_COMMAND_PATTERNS = [
        r'(?i)\b(rm\s+-rf|format\s+[c-z]:|powershell\s+-enc|bash\s+-c)\b',
        r'(?i)\b(__import__\(|os\.system|subprocess\.Popen)\b'
    ]

    def inspect_query(self, query: str) -> Dict[str, Any]:
        """
        Inspects incoming prompt for security vulnerabilities.
        Returns:
            {
                "is_safe": bool,
                "threat_level": "NONE" | "LOW" | "HIGH" | "CRITICAL",
                "threat_type": Optional[str],
                "reason": Optional[str]
            }
        """
        if not query:
            return {"is_safe": True, "threat_level": "NONE", "threat_type": None, "reason": None}

        q = query.strip()

        # 1. Check Destructive SQL / Database destruction
        for pat in self.DESTRUCTIVE_SQL_PATTERNS:
            if re.search(pat, q):
                return {
                    "is_safe": False,
                    "threat_level": "CRITICAL",
                    "threat_type": "DESTRUCTIVE_SQL_ATTACK",
                    "reason": "Z Sentinel blocked an unauthorized destructive SQL command (DROP/DELETE/TRUNCATE/ALTER)."
                }

        # 2. Check Jailbreak / Prompt Injection
        for pat in self.JAILBREAK_PATTERNS:
            if re.search(pat, q):
                return {
                    "is_safe": False,
                    "threat_level": "HIGH",
                    "threat_type": "ADVERSARIAL_PROMPT_INJECTION",
                    "reason": "Z Sentinel detected an adversarial jailbreak or system-prompt exfiltration attempt."
                }

        # 3. Check OS Command Injection
        for pat in self.OS_COMMAND_PATTERNS:
            if re.search(pat, q):
                return {
                    "is_safe": False,
                    "threat_level": "CRITICAL",
                    "threat_type": "OS_COMMAND_INJECTION",
                    "reason": "Z Sentinel intercepted an unauthorized shell execution command."
                }

        return {
            "is_safe": True,
            "threat_level": "NONE",
            "threat_type": None,
            "reason": None
        }

injection_defense = InjectionDefense()

