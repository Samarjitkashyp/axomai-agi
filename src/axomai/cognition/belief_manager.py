"""
AxomAI Cognition Engine - Belief & Epistemic Uncertainty Manager.
Manages the AGI's internal belief states, separating empirical facts from working hypotheses,
tracking Bayesian confidence, and actively detecting contradictions across incoming data.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class Belief:
    """An epistemic proposition held by the AGI."""

    def __init__(
        self,
        belief_id: str,
        topic: str,
        statement: str,
        epistemic_type: str = "HYPOTHESIS",  # FACT, HYPOTHESIS, UNVERIFIED_CLAIM
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
        else:
            self.confidence = max(0.01, self.confidence - evidence_weight * self.confidence)
            
        self.evidence_history.append({
            "confirming": confirming,
            "weight": evidence_weight,
            "new_confidence": round(self.confidence, 4),
            "note": note,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

class BeliefManager:
    """Central epistemic uncertainty and contradiction detector."""

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

    def check_for_contradictions(self, new_claim: str, topic: str) -> Optional[Dict[str, Any]]:
        """Detects if an incoming claim fundamentally contradicts an established high-confidence FACT."""
        for b_id, b in self.beliefs.items():
            if b.topic == topic and b.confidence > 0.90:
                # Simple negation check
                claim_low = new_claim.lower()
                stmt_low = b.statement.lower()
                if ("not" in claim_low or "unsafe" in claim_low) and "acceptable" in stmt_low:
                    contradiction = {
                        "belief_id": b_id,
                        "established_fact": b.statement,
                        "contradicting_claim": new_claim,
                        "confidence_gap": b.confidence,
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

