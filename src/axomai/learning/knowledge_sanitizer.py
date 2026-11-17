"""
AxomAI Continuous Learning Engine - Knowledge Sanitizer & Anti-Poisoning Filter.
Ensures external internet data, scraped articles, and raw feeds do not contain
prompt injections, poisoned backdoors, or malicious payload instructions
before admission into long-term cognitive memory.
"""

import re
from typing import Dict, Any, List, Tuple

class KnowledgeSanitizer:
    """Anti-poisoning, injection detection, and content safety filter."""

    # High-risk jailbreak and prompt-injection signatures
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
        r"system\s+prompt\s+override",
        r"you\s+are\s+now\s+in\s+dan\s+mode",
        r"disregard\s+all\s+safety",
        r"<script.*?>.*?</script>",
        r"__import__\s*\(",
        r"os\.system\s*\(",
        r"subprocess\.call",
        r"rm\s+-rf",
        r"drop\s+table",
        r"delete\s+from\s+semantic_"
    ]

    def __init__(self):
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.INJECTION_PATTERNS]

    def sanitize_text(self, raw_text: str) -> Dict[str, Any]:
        """
        Inspects raw downloaded content for security threats.
        Returns cleaned text or flags critical security contamination.
        """
        if not raw_text or not isinstance(raw_text, str):
            return {"is_safe": False, "cleaned_text": "", "reason": "EMPTY_OR_INVALID_INPUT"}

        detected_threats = []
        for pat in self.compiled_patterns:
            if pat.search(raw_text):
                detected_threats.append(pat.pattern)

        if detected_threats:
            return {
                "is_safe": False,
                "cleaned_text": "",
                "reason": "MALICIOUS_PROMPT_INJECTION_OR_EXPLOIT_DETECTED",
                "matched_patterns": detected_threats
            }

        # Remove excessive whitespace, control characters, and suspicious script tags
        cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', raw_text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        # Quality check: Minimum meaningful content length
        if len(cleaned.split()) < 3:
            return {"is_safe": False, "cleaned_text": "", "reason": "CONTENT_TOO_TRIVIAL"}

        return {
            "is_safe": True,
            "cleaned_text": cleaned,
            "length_words": len(cleaned.split()),
            "safety_score": 0.99
        }

    def extract_candidate_triples(self, sanitized_text: str) -> List[Tuple[str, str, str]]:
        """
        Extracts candidate ontological relations (Subject, Predicate, Object)
        from factual declarative sentences.
        """
        candidates = []
        sentences = re.split(r'[.!?]\s+', sanitized_text)
        
        # High-confidence relationship regex patterns
        relation_regexes = [
            (r"([A-Z][a-zA-Z0-9\s]{2,25})\s+is\s+(located\s+in|operated\s+by|managed\s+by)\s+([A-Z][a-zA-Z0-9\s]{2,25})", "LOCATED_IN"),
            (r"([A-Z][a-zA-Z0-9\s]{2,25})\s+(supplies|exports|produces)\s+([a-zA-Z0-9\s]{3,25})", "PRODUCES_OR_EXPORTS"),
            (r"([A-Z][a-zA-Z0-9\s]{2,25})\s+(mandates|regulates|enforces)\s+([a-zA-Z0-9\s]{3,25})", "REGULATES"),
            (r"([A-Z][a-zA-Z0-9\s]{2,25})\s+reduced\s+costs\s+by\s+([0-9\.]+%?)", "COST_EFFICIENCY_METRIC")
        ]

        for sent in sentences:
            for pat, default_pred in relation_regexes:
                match = re.search(pat, sent)
                if match:
                    groups = match.groups()
                    if len(groups) >= 2:
                        subj = groups[0].strip()
                        obj = groups[-1].strip()
                        pred = default_pred
                        candidates.append((subj, pred, obj))

        return candidates

    def extract_evidence_triples(self, sanitized_text: str) -> List[Dict[str, Any]]:
        """
        Extracts candidate ontological relations with verified evidence spans and calibrated confidence.
        """
        candidates = []
        sentences = [s.strip() for s in re.split(r'[.!?]\s+', sanitized_text) if len(s.strip()) > 15]

        relation_regexes = [
            (r"([A-Z][a-zA-Z0-9\s]{2,30})\s+(?:is|are)\s+(located\s+in|operated\s+by|managed\s+by|headquartered\s+in)\s+([A-Z][a-zA-Z0-9\s]{2,30})", "LOCATED_IN", 0.94),
            (r"([A-Z][a-zA-Z0-9\s]{2,30})\s+(supplies|exports|produces|sells|distributes)\s+([a-zA-Z0-9\s\$\₹\€]{3,30})", "PRODUCES_OR_EXPORTS", 0.92),
            (r"([A-Z][a-zA-Z0-9\s]{2,30})\s+(mandates|regulates|enforces|announced)\s+([a-zA-Z0-9\s]{3,30})", "REGULATES_OR_ANNOUNCED", 0.90),
            (r"([A-Z][a-zA-Z0-9\s]{2,30})\s+(?:recorded|achieved|reported)\s+([a-zA-Z0-9\s%₹\$\€]+)", "PERFORMANCE_EVENT", 0.88),
            (r"([A-Z][a-zA-Z0-9\s]{2,30})\s+(?:invests|funded|allocated)\s+([0-9\.]+\s*(?:crore|million|billion|inr|usd)?)\s+(?:in|for)\s+([a-zA-Z0-9\s]{3,30})", "CAPITAL_ALLOCATION", 0.95)
        ]

        for sent in sentences:
            for pat, default_pred, base_conf in relation_regexes:
                match = re.search(pat, sent, re.IGNORECASE)
                if match:
                    groups = [g.strip() for g in match.groups() if g]
                    if len(groups) >= 2:
                        subj = groups[0]
                        obj = groups[-1]
                        conf = base_conf
                        if any(c.isdigit() for c in sent):
                            conf = min(0.98, conf + 0.03)
                        candidates.append({
                            "subject": subj,
                            "predicate": default_pred,
                            "object": obj,
                            "evidence_span": sent,
                            "confidence": round(conf, 3)
                        })
                        break
        return candidates

knowledge_sanitizer = KnowledgeSanitizer()

