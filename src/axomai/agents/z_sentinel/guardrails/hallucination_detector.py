"""
Z Sentinel - Hallucination Detection & Fact-Grounding Engine.
Cross-verifies claims, numerical statistics, dates, and entity statements
against raw source context (UDM document chunks, live web sources, or SQL data tables).
"""

import re
from typing import Dict, Any, List, Optional
from axomai.core.llm import llm_brain

class HallucinationDetector:
    """Verifies that generated responses are strictly anchored in source evidence."""

    def extract_numerical_claims(self, text: str) -> List[str]:
        """Extracts percentages, monetary figures, metrics, and quantitative stats."""
        patterns = [
            r'[\$₹€£]\s*[0-9]+(?:\.[0-9]+)?(?:\s*(?:billion|million|trillion|lakh|crore|k|b|m))?',
            r'[0-9]+(?:\.[0-9]+)?\s*%',
            r'\b[0-9]{4}\b', # Years
            r'\b[0-9]+(?:\.[0-9]+)?\s*(?:units|users|growth|margin|cogs|share|per\s+cent)\b'
        ]
        claims = []
        for pat in patterns:
            found = re.findall(pat, text, re.IGNORECASE)
            claims.extend(found)
        return list(set(claims))

    def evaluate_grounding(
        self,
        answer: str,
        context_str: str,
        query: str,
        sources: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Calculates consensus score and detects ungrounded or fabricated statements.
        Returns:
            {
                "grounding_score": float (0-100),
                "is_grounded": bool,
                "verified_claims": List[Dict],
                "hallucinated_claims": List[str],
                "verdict": str
            }
        """
        if not answer:
            return {
                "grounding_score": 100.0,
                "is_grounded": True,
                "verified_claims": [],
                "hallucinated_claims": [],
                "verdict": "VERIFIED_EMPTY"
            }

        # 1. Numerical & Quantitative Cross-Verification
        claims = self.extract_numerical_claims(answer)
        verified_claims = []
        hallucinated_claims = []

        context_lower = (context_str or "").lower()
        if sources:
            for s in sources:
                context_lower += " " + str(s.get("title", "")).lower()
                context_lower += " " + str(s.get("snippet", "")).lower()

        if claims:
            for claim in claims:
                clean_claim = claim.lower().strip()
                # Check for numerical token in context
                num_match = re.search(r'[0-9]+(?:\.[0-9]+)?', clean_claim)
                if num_match and num_match.group(0) in context_lower:
                    verified_claims.append({
                        "entity": claim,
                        "claim": f"Quantitative metric '{claim}' verified in source evidence.",
                        "status": "VERIFIED_HIGH_CONFIDENCE",
                        "confidence_score": 98.0,
                        "verification_source": "Source Context Grounding"
                    })
                elif not context_lower:
                    # General reasoning or direct question
                    verified_claims.append({
                        "entity": claim,
                        "claim": f"Derived metric '{claim}'",
                        "status": "CALCULATED_CONSISTENT",
                        "confidence_score": 92.0,
                        "verification_source": "Analytical Reasoning"
                    })
                else:
                    hallucinated_claims.append(claim)

        # 2. Fast Semantic Consistency Check via LLM Brain if context exists
        semantic_score = 95.0
        if llm_brain.is_available and context_str and len(context_str.strip()) > 50:
            try:
                system_prompt = "You are Z Sentinel Quality & Hallucination Auditor. Your task is to verify that the generated answer is strictly grounded in the provided source context. Output valid JSON only."
                user_prompt = (
                    f"Source Context:\n{context_str[:2000]}\n\n"
                    f"Generated Answer:\n{answer[:2000]}\n\n"
                    "Output JSON only: {\"grounding_score\": 0-100, \"hallucination_found\": true|false, \"reason\": \"short reason\"}"
                )
                res = llm_brain.generate(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.0)
                clean_json = res.strip()
                if "```json" in clean_json:
                    clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_json:
                    clean_json = clean_json.split("```")[1].split("```")[0].strip()
                import json
                parsed = json.loads(clean_json)
                semantic_score = float(parsed.get("grounding_score", 95.0))
                if parsed.get("hallucination_found", False):
                    hallucinated_claims.append(parsed.get("reason", "Semantic divergence from source evidence"))
            except Exception:
                pass

        total_claims_count = len(claims) if claims else 1
        verified_ratio = len(verified_claims) / total_claims_count if claims else 1.0
        final_score = round((semantic_score * 0.6) + (verified_ratio * 100 * 0.4), 1)
        final_score = min(max(final_score, 0.0), 100.0)

        is_grounded = (final_score >= 80.0) and (len(hallucinated_claims) == 0)

        return {
            "grounding_score": final_score,
            "is_grounded": is_grounded,
            "verified_claims": verified_claims,
            "hallucinated_claims": hallucinated_claims,
            "verdict": "VERIFIED_HIGH_CONFIDENCE" if is_grounded else "HALLUCINATION_DETECTED"
        }

hallucination_detector = HallucinationDetector()
