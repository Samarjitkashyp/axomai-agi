"""
AxomAI Continuous Learning Engine - Autonomous Prediction Engine.
Transforms passive knowledge ingestion into empirical scientific learning:
1. Emits falsifiable predictions with explicit confidence calibration and verification deadlines.
2. Evaluates observed real-world outcomes against prior predictions.
3. Calculates empirical prediction error (Brier score / regression delta).
4. Dynamically recalibrates Self-Model confidence and updates Belief Engine weights.
"""

import time
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from pathlib import Path

from axomai.config import settings
from axomai.cognition.self_model import self_model
from axomai.cognition.belief_manager import belief_manager

@dataclass
class FalsifiablePrediction:
    prediction_id: str
    domain: str
    target_entity: str
    hypothesis: str
    predicted_outcome: str
    confidence: float  # Epistemic confidence between 0.0 and 1.0
    deadline: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "PENDING_VERIFICATION"  # PENDING_VERIFICATION, CONFIRMED, REFUTED
    actual_outcome: Optional[str] = None
    prediction_error: Optional[float] = None
    calibration_adjustment: Optional[float] = None

class PredictionEngine:
    """Scientific hypothesis formulation and empirical prediction error learner."""

    def __init__(self):
        self.storage_path = settings.STORAGE_DIR / "prediction_records.jsonl"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.active_predictions: Dict[str, FalsifiablePrediction] = {}
        self.prediction_counter: int = 0
        self._load_active_predictions()

    def _load_active_predictions(self):
        """Loads prior pending predictions from persistent storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line.strip())
                            pred = FalsifiablePrediction(**data)
                            if pred.status == "PENDING_VERIFICATION":
                                self.active_predictions[pred.prediction_id] = pred
                                self.prediction_counter = max(self.prediction_counter, int(pred.prediction_id.split("_")[-1]) if "_" in pred.prediction_id else 0)
            except Exception:
                pass

    def emit_prediction(
        self,
        domain: str,
        target_entity: str,
        hypothesis: str,
        predicted_outcome: str,
        confidence: float,
        deadline: Optional[str] = None
    ) -> FalsifiablePrediction:
        """
        Registers an empirical, testable prediction with an explicit confidence score.
        """
        self.prediction_counter += 1
        pid = f"pred_{self.prediction_counter:04d}"
        deadline_str = deadline or datetime.now(timezone.utc).isoformat()

        pred = FalsifiablePrediction(
            prediction_id=pid,
            domain=domain,
            target_entity=target_entity,
            hypothesis=hypothesis,
            predicted_outcome=predicted_outcome,
            confidence=max(0.1, min(0.99, float(confidence))),
            deadline=deadline_str
        )
        self.active_predictions[pid] = pred

        # Persist to JSONL storage
        try:
            with open(self.storage_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(pred)) + "\n")
        except Exception:
            pass

        return pred

    def evaluate_prediction(
        self,
        prediction_id: str,
        actual_outcome: str,
        is_correct: bool
    ) -> Dict[str, Any]:
        """
        Compares reality against prior prediction, computes error, and updates epistemic weights.
        """
        pred = self.active_predictions.get(prediction_id)
        if not pred:
            return {"status": "PREDICTION_NOT_FOUND", "prediction_id": prediction_id}

        # Calculate empirical Brier score error: (confidence - outcome_binary)^2
        outcome_binary = 1.0 if is_correct else 0.0
        error = round(abs(pred.confidence - outcome_binary), 3)
        brier_score = round((pred.confidence - outcome_binary) ** 2, 4)

        pred.status = "CONFIRMED" if is_correct else "REFUTED"
        pred.actual_outcome = actual_outcome
        pred.prediction_error = error

        # Metacognitive Calibration Update in Self-Model
        new_calibration = self_model.calibrate_domain(
            domain=pred.domain,
            predicted_confidence=pred.confidence,
            actual_success=is_correct
        )
        pred.calibration_adjustment = new_calibration

        # Update Belief Engine weights (strengthen corroborated beliefs, weaken refuted ones)
        try:
            belief_weight_delta = 0.10 if is_correct else -0.20
            belief_manager.update_belief(
                claim_id=f"belief_{pred.target_entity}",
                evidence_confidence=pred.confidence,
                weight_delta=belief_weight_delta
            )
        except Exception:
            pass

        # Update persistent storage
        try:
            with open(self.storage_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(pred)) + "\n")
        except Exception:
            pass

        return {
            "prediction_id": prediction_id,
            "status": pred.status,
            "domain": pred.domain,
            "hypothesis": pred.hypothesis,
            "predicted_outcome": pred.predicted_outcome,
            "actual_outcome": actual_outcome,
            "is_correct": is_correct,
            "prediction_error": error,
            "brier_score": brier_score,
            "new_calibration": new_calibration
        }

    def get_empirical_performance(self) -> Dict[str, Any]:
        """Returns accuracy, calibration error, and Brier score across predictions."""
        total = len(self.active_predictions)
        evaluated = [p for p in self.active_predictions.values() if p.status in ["CONFIRMED", "REFUTED"]]
        correct = [p for p in evaluated if p.status == "CONFIRMED"]

        acc = round((len(correct) / len(evaluated)) * 100, 2) if evaluated else 0.0
        avg_brier = round(sum((p.confidence - (1.0 if p.status == "CONFIRMED" else 0.0))**2 for p in evaluated) / len(evaluated), 4) if evaluated else 0.0

        return {
            "total_predictions": total,
            "evaluated_count": len(evaluated),
            "pending_count": total - len(evaluated),
            "empirical_accuracy_pct": acc,
            "average_brier_score": avg_brier
        }

prediction_engine = PredictionEngine()
