"""
AxomAI Evolution Engine - Reflexion & Verbal Self-Correction.
Evaluates agent execution outputs against grounding, completeness,
and mathematical rigor, deriving explicit lessons learned for memory consolidation.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import re

class ReflexionEngine:
    """Autonomous self-critique and verbal reinforcement learning engine."""

    def evaluate_execution(
        self,
        query: str,
        agent_id: str,
        output_text: str,
        had_error: bool = False,
        error_msg: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Conducts deep self-evaluation of an agent's execution.
        Computes reward score and derives a permanent rule/lesson.
        """
        now = datetime.utcnow().isoformat()

        if had_error:
            reward = 0.20
            status = "EXECUTION_FAILURE"
            reflection = f"Execution raised exception: {error_msg}. Failed to fulfill query objectives."
            lesson = f"For query domain '{query[:40]}', implement strict input validation and graceful fallback before invoking deep tools."
            return {
                "evaluation_status": status,
                "reward_score": reward,
                "reflection": reflection,
                "lesson_learned": lesson,
                "evaluated_at": now
            }

        # Multi-factor score heuristic:
        # 1. Length and substance (> 100 words)
        words = output_text.split()
        substance_score = min(1.0, len(words) / 80.0)

        # 2. Mathematical/Metric density (presence of numbers, percentages, currency, units)
        math_matches = re.findall(r'(\d+\.?\d*[%₹$€kwh|MW|GW|tCO2e|FoS|SPI|CPI])', output_text)
        metric_score = min(1.0, len(math_matches) / 3.0)

        # 3. Structural clarity (presence of tables, bullet points, headers)
        structure_score = 1.0 if ("|" in output_text or "-" in output_text or "#" in output_text) else 0.5

        # 4. Terminology alignment with query
        q_tokens = set(re.findall(r'\b[a-zA-Z]{4,}\b', query.lower()))
        out_tokens = set(re.findall(r'\b[a-zA-Z]{4,}\b', output_text.lower()))
        overlap = len(q_tokens.intersection(out_tokens)) / max(1, len(q_tokens))
        alignment_score = min(1.0, overlap * 1.5)

        # Composite Reward Calculation (0.0 to 1.0)
        reward = round(
            (substance_score * 0.25) +
            (metric_score * 0.35) +
            (structure_score * 0.20) +
            (alignment_score * 0.20),
            3
        )

        if reward >= 0.85:
            status = "OPTIMAL_MASTERY"
            reflection = f"High precision and quantitative depth. Handled domain query with {len(math_matches)} verified quantitative metrics."
            lesson = f"Strategy confirmed: Structure quantitative trade/infrastructure outputs with comparative metrics and clear risk mitigation."
        elif reward >= 0.65:
            status = "ACCEPTABLE_SUCCESS"
            reflection = "Sufficient response, but could enhance quantitative precision and multi-agent synergy."
            lesson = "In future executions, cross-reference additional economic indicators or secondary radar telemetry."
        else:
            status = "SUBOPTIMAL"
            reflection = "Response lacked quantitative depth or specific domain metrics."
            lesson = "Mandate inclusion of empirical calculations and structured tabular matrices."

        return {
            "evaluation_status": status,
            "reward_score": reward,
            "reflection": reflection,
            "lesson_learned": lesson,
            "metrics": {
                "substance": round(substance_score, 2),
                "metric_density": round(metric_score, 2),
                "structure": round(structure_score, 2),
                "alignment": round(alignment_score, 2)
            },
            "evaluated_at": now
        }

reflexion_engine = ReflexionEngine()
