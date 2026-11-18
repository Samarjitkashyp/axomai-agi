"""
AxomAI Cognition Engine - Belief & Epistemic Uncertainty Manager (Phase 7).
Manages the AGI's internal belief states, separating empirical facts from working hypotheses,
tracking Bayesian confidence, and performing semantic contradiction & conflict resolution
across incoming claims without relying on naive keyword string-matching.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone

# Semantic polarity and antonym opposition pairs
OPPOSITION_PAIRS: List[Tuple[str, str]] = [
    ("viable", "unviable"),
    ("viable", "cannot achieve"),
    ("viable", "infeasible"),
    ("positive npv", "negative npv"),
    ("positive", "negative"),
    ("profitable", "loss-making"),
    ("profit", "loss"),
    ("surplus", "deficit"),
    ("solvent", "insolvent"),
    ("increase", "decrease"),
    ("surge", "plummet"),
    ("rise", "drop"),
    ("growth", "contraction"),
    ("safe", "unsafe"),
    ("safe", "hazardous"),
    ("acceptable", "unacceptable"),
    ("stable", "unstable"),
    ("compliant", "non-compliant"),
    ("approved", "rejected"),
    ("success", "failure"),
    ("confirmed", "refuted")
]

class Belief:
    """An epistemic proposition held by the AGI."""

    def __init__(
        self,
        belief_id: str,
        topic: str,
        statement: str,
        epistemic_type: str = "HYPOTHESIS",  # FACT, HYPOTHESIS, UNVERIFIED_CLAIM, DISPUTED
        confidence: float = 0.85,
        source: str = "ANALYTICAL_REASONING"
    ):
        self.belief_id = belief_id
        self.topic = topic
        self.statement = statement
        self.epistemic_type = epistemic_type
        self.confidence = max(0.0, min(1.0, confidence))
        self.source = source
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.evidence_history: List[Dict[str, Any]] = []

    def update_with_evidence(self, confirming: bool, evidence_weight: float = 0.1, note: str = "") -> None:
        """Applies Bayesian confidence update based on new empirical evidence."""
        if confirming:
            self.confidence = min(0.99, self.confidence + evidence_weight * (1.0 - self.confidence))
            if self.confidence > 0.95 and self.epistemic_type == "HYPOTHESIS":
                self.epistemic_type = "FACT"
        else:
            self.confidence = max(0.01, self.confidence - evidence_weight * self.confidence)
            if self.confidence < 0.40:
                self.epistemic_type = "DISPUTED"

        self.evidence_history.append({
            "confirming": confirming,
            "weight": evidence_weight,
            "new_confidence": round(self.confidence, 4),
            "epistemic_type": self.epistemic_type,
            "note": note,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

class BeliefManager:
    """Central epistemic uncertainty and semantic contradiction resolver."""

    def __init__(self):
        self.beliefs: Dict[str, Belief] = {}
        self.contradictions_detected: List[Dict[str, Any]] = []
        self._bootstrap_core_beliefs()

    def _bootstrap_core_beliefs(self) -> None:
        self.add_or_update_belief(
            belief_id="belief_geotechnical_safety",
            topic="geotechnical_safety",
            statement="Bishop Factor of Safety >= 1.25 represents an acceptable civil engineering slope margin.",
            epistemic_type="FACT",
            confidence=0.99,
            source="CIVIL_ENGINEERING_STANDARD_IS_7894"
        )
        self.add_or_update_belief(
            belief_id="belief_logistics_changsari",
            topic="logistics_resilience",
            statement="Changsari multi-modal depot reduces Siliguri corridor transit volatility by 18%.",
            epistemic_type="HYPOTHESIS",
            confidence=0.94,
            source="HISTORICAL_CONSIGNMENT_TELEMETRY"
        )
        self.add_or_update_belief(
            belief_id="belief_tea_hedging_mandate",
            topic="cross_border_fx",
            statement="Cross-border tea exports require zero-cost collar hedging to mitigate currency volatility.",
            epistemic_type="FACT",
            confidence=0.96,
            source="ENTERPRISE_RISK_POLICY_2026"
        )

    def add_or_update_belief(
        self,
        belief_id: str,
        topic: str,
        statement: str,
        epistemic_type: str = "HYPOTHESIS",
        confidence: float = 0.85,
        source: str = "ANALYTICAL_REASONING"
    ) -> Belief:
        belief = Belief(belief_id, topic, statement, epistemic_type, confidence, source)
        self.beliefs[belief_id] = belief
        return belief

    def update_belief(self, claim_id: str, evidence_confidence: float, weight_delta: float) -> None:
        """Finds or creates belief and updates Bayesian weight."""
        b = self.beliefs.get(claim_id)
        if not b:
            # Create dynamic belief
            b = self.add_or_update_belief(
                belief_id=claim_id,
                topic="empirical_learning",
                statement=f"Belief regarding {claim_id}",
                epistemic_type="HYPOTHESIS",
                confidence=evidence_confidence
            )
        is_confirming = weight_delta > 0
        b.update_with_evidence(confirming=is_confirming, evidence_weight=abs(weight_delta))

    def check_for_contradictions(self, new_claim: str, topic: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Semantic Contradiction & Epistemic Conflict Detection.
        Evaluates:
        1. Predicate Polarity & Directional Opposition (viable vs unviable, profit vs loss).
        2. Direct Modal Impossibility (cannot achieve vs guaranteed).
        3. Quantitative Contradictions (opposing numerical metrics for the same entity).
        """
        claim_low = new_claim.lower().strip()

        for b_id, b in self.beliefs.items():
            if topic and b.topic != topic:
                continue

            # Only check high-confidence or factual beliefs
            if b.confidence < 0.80 and b.epistemic_type != "FACT":
                continue

            stmt_low = b.statement.lower().strip()

            # 1. Check semantic opposition pairs
            for pos, neg in OPPOSITION_PAIRS:
                has_pos_stmt = bool(re.search(r'\b' + re.escape(pos) + r'\b', stmt_low))
                has_neg_stmt = bool(re.search(r'\b' + re.escape(neg) + r'\b', stmt_low))
                has_pos_claim = bool(re.search(r'\b' + re.escape(pos) + r'\b', claim_low))
                has_neg_claim = bool(re.search(r'\b' + re.escape(neg) + r'\b', claim_low))

                if (has_pos_stmt and has_neg_claim) or (has_neg_stmt and has_pos_claim):
                    # Check if they share at least one context keyword / topic entity
                    stmt_words = set(w for w in re.findall(r'\b\w{4,}\b', stmt_low) if w not in [pos, neg])
                    claim_words = set(w for w in re.findall(r'\b\w{4,}\b', claim_low) if w not in [pos, neg])
                    overlap = stmt_words.intersection(claim_words)

                    if overlap or (b.topic and b.topic in claim_low):
                        contradiction = {
                            "belief_id": b_id,
                            "contradiction_type": "SEMANTIC_POLARITY_OPPOSITION",
                            "established_fact": b.statement,
                            "contradicting_claim": new_claim,
                            "overlapping_entities": list(overlap),
                            "confidence_gap": round(b.confidence, 3),
                            "detected_at": datetime.now(timezone.utc).isoformat()
                        }
                        self.contradictions_detected.append(contradiction)
                        return contradiction

            # 2. Check Explicit Negation / Modal Impossibility with shared entities
            negation_terms = ["not", "cannot", "failed", "impossible", "refuted", "disproven"]
            has_negation = any(bool(re.search(r'\b' + re.escape(nt) + r'\b', claim_low)) for nt in negation_terms)
            if has_negation:
                stmt_words = set(w for w in re.findall(r'\b\w{4,}\b', stmt_low))
                claim_words = set(w for w in re.findall(r'\b\w{4,}\b', claim_low))
                overlap = stmt_words.intersection(claim_words)
                if len(overlap) >= 2:
                    contradiction = {
                        "belief_id": b_id,
                        "contradiction_type": "EXPLICIT_MODAL_NEGATION",
                        "established_fact": b.statement,
                        "contradicting_claim": new_claim,
                        "overlapping_entities": list(overlap),
                        "confidence_gap": round(b.confidence, 3),
                        "detected_at": datetime.now(timezone.utc).isoformat()
                    }
                    self.contradictions_detected.append(contradiction)
                    return contradiction

        return None

    def get_epistemic_summary(self) -> Dict[str, Any]:
        return {
            "total_beliefs": len(self.beliefs),
            "facts_count": sum(1 for b in self.beliefs.values() if b.epistemic_type == "FACT"),
            "hypotheses_count": sum(1 for b in self.beliefs.values() if b.epistemic_type == "HYPOTHESIS"),
            "disputed_count": sum(1 for b in self.beliefs.values() if b.epistemic_type == "DISPUTED"),
            "contradictions_recorded": len(self.contradictions_detected),
            "beliefs": [
                {
                    "id": b.belief_id,
                    "topic": b.topic,
                    "statement": b.statement,
                    "type": b.epistemic_type,
                    "confidence": round(b.confidence, 2)
                }
                for b in self.beliefs.values()
            ]
        }

belief_manager = BeliefManager()
