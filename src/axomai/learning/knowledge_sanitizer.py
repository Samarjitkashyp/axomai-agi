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

knowledge_sanitizer = KnowledgeSanitizer()
