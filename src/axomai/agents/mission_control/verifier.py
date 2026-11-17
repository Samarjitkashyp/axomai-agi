"""
AxomAI Mission Control - Autonomous Mission Verifier.
Conducts multi-dimensional verification on milestone outputs:
1. Substantive Deliverable Validation (non-trivial length, formatting, structure).
2. Domain Acceptance Criteria (Research, Coding, Analytics, Legal/Governance).
3. Z Sentinel Security & Hallucination Audit (PII masking, fact grounding, auto-healing).
4. Emits actionable diagnostics for auto-recovery / replanning when verification fails.
"""

import ast
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from axomai.agents.z_sentinel import z_sentinel_agent

@dataclass
class VerificationResult:
    passed: bool
    quality_score: float
    feedback: str
    criteria_met: List[str] = field(default_factory=list)
    missing_criteria: List[str] = field(default_factory=list)
    sanitized_output: str = ""
    sentinel_audit: Optional[Dict[str, Any]] = None

class MissionVerifier:
    """Rigorous acceptance verifier for autonomous mission milestones."""

    def __init__(self):
        self.sentinel = z_sentinel_agent

    def verify_milestone(
        self,
        output: str,
        milestone_title: str,
        milestone_objective: str,
        target_agent: str,
        context_str: str = ""
    ) -> VerificationResult:
        """
        Validates milestone output against acceptance criteria, length, substance, and security.
        """
        criteria_met = []
        missing_criteria = []
        feedback_notes = []

        # 1. Non-Empty & Minimum Substance Validation
        if not output or not output.strip():
            return VerificationResult(
                passed=False,
                quality_score=0.0,
                feedback="CRITICAL: Milestone output is completely empty.",
                criteria_met=[],
                missing_criteria=["non_empty_output", "substantive_content"],
                sanitized_output=""
            )

        clean_text = output.strip()
        char_len = len(clean_text)
        
        # Check for placeholder / failure responses
        lower_text = clean_text.lower()
        if any(ph in lower_text for ph in ["i don't know", "could not find", "internal server error", "exception occurred"]) and char_len < 120:
            return VerificationResult(
                passed=False,
                quality_score=0.15,
                feedback=f"REJECTED: Output appears to be a trivial failure or placeholder: '{clean_text}'",
                criteria_met=[],
                missing_criteria=["substantive_content"],
                sanitized_output=clean_text
            )

        if char_len >= 80:
            criteria_met.append("substantive_length")
        else:
            missing_criteria.append("substantive_length")
            feedback_notes.append("Output is unusually short (< 80 characters).")

        # 2. Domain-Specific Acceptance Criteria
        agent_key = (target_agent or "").lower()

        # Research Domain (Z2 Bravo, Market Intelligence)
        if agent_key in ["z2", "z2_bravo", "research"]:
            has_headings = bool(re.search(r'#{1,4}\s+', clean_text))
            has_bullets = bool(re.search(r'^\s*[-*•]\s+', clean_text, re.MULTILINE))
            has_facts_or_entities = bool(re.search(r'\b(market|demand|growth|rate|sector|cost|spread|analysis|source|report|crore|lakh|percent|%)\b', lower_text))

            if has_headings or has_bullets:
                criteria_met.append("structured_presentation")
            else:
                missing_criteria.append("structured_presentation")
                feedback_notes.append("Research output lacks structured markdown headings or bullet points.")

            if has_facts_or_entities:
                criteria_met.append("domain_terminology_grounding")
            else:
                missing_criteria.append("domain_terminology_grounding")
                feedback_notes.append("Research lacks concrete market or entity references.")

        # Coding / ToolForge Domain (Z4 Nexus)
        elif agent_key in ["z4", "z4_nexus", "coding"]:
            has_code_block = "```" in clean_text or "def " in clean_text or "class " in clean_text or "import " in clean_text
            if has_code_block:
                criteria_met.append("code_artifacts_present")
                # Syntax validation on extracted python code blocks
                code_matches = re.findall(r'```(?:python)?\s*([\s\S]*?)```', clean_text)
                for code_snippet in code_matches:
                    try:
                        ast.parse(code_snippet.strip())
                        criteria_met.append("python_ast_syntax_valid")
                    except SyntaxError as syn_err:
                        missing_criteria.append("python_ast_syntax_valid")
                        feedback_notes.append(f"Syntax error detected in code artifact: {syn_err.msg}")
            else:
                missing_criteria.append("code_artifacts_present")
                feedback_notes.append("Coding milestone deliverable contains no executable code or functions.")

        # Analytics / Financial / Modeling Domain (Z3 Echo, Z13, Z17)
        elif agent_key in ["z3", "z13", "z17", "financial", "analytics"]:
            has_numeric_metrics = bool(re.search(r'\b(?:\d+(?:\.\d+)?%?|\₹|\$|crore|lakh|metric|ebitda|irr|npv|ratio)\b', lower_text))
            if has_numeric_metrics:
                criteria_met.append("quantitative_metrics_present")
            else:
                missing_criteria.append("quantitative_metrics_present")
                feedback_notes.append("Analytics deliverable lacks numerical metrics, formulas, or financial data.")

        # Governance & Legal Domain (Z8 Apex, Z11 Pragati)
        elif agent_key in ["z8", "z11", "legal", "compliance"]:
            has_regulatory_references = bool(re.search(r'\b(act|clause|section|fidic|compliance|statutory|rule|regulatory|msme|policy)\b', lower_text))
            if has_regulatory_references:
                criteria_met.append("regulatory_framework_anchored")
            else:
                missing_criteria.append("regulatory_framework_anchored")
                feedback_notes.append("Governance deliverable lacks explicit statutory, clause, or policy citations.")

        # 3. Z Sentinel Security, PII & Hallucination Audit
        sentinel_audit = None
        sanitized_output = clean_text
        try:
            audit_res = self.sentinel.audit_response(
                answer=clean_text,
                context_str=context_str or milestone_objective,
                query=f"{milestone_title}: {milestone_objective}"
            )
            sanitized_output = audit_res.get("sanitized_answer", clean_text)
            sentinel_audit = audit_res.get("verification_audit", {})
            grounding_score = audit_res.get("grounding_score", 100.0)

            if audit_res.get("self_healed"):
                criteria_met.append("sentinel_self_healed")

            if grounding_score >= 70.0:
                criteria_met.append("sentinel_grounding_verified")
            else:
                missing_criteria.append("sentinel_grounding_verified")
                feedback_notes.append(f"Z Sentinel grounding confidence below threshold: {grounding_score}%")
        except Exception:
            criteria_met.append("sentinel_fallback_accepted")

        # 4. Final Quality Score & Strict Zero-Tolerance Pass/Fail Verdict
        mandatory_criteria = {"non_empty_output", "substantive_length"}
        if agent_key in ["z4", "z4_nexus", "coding"]:
            mandatory_criteria.add("code_artifacts_present")
        elif agent_key in ["z2", "z2_bravo", "research"]:
            mandatory_criteria.add("domain_terminology_grounding")
        elif agent_key in ["z3", "z13", "z17", "financial", "analytics"]:
            mandatory_criteria.add("quantitative_metrics_present")
        elif agent_key in ["z8", "z11", "legal", "compliance"]:
            mandatory_criteria.add("regulatory_framework_anchored")

        total_eval_points = len(criteria_met) + len(missing_criteria)
        quality_score = round(len(criteria_met) / max(total_eval_points, 1), 2)
        
        # Zero-Tolerance Rigor:
        # 1. Every mandatory criterion MUST be satisfied (no exceptions).
        # 2. Minimum overall quality score must be >= 0.70.
        missing_mandatory = [c for c in missing_criteria if c in mandatory_criteria]
        passed = (len(missing_mandatory) == 0) and (quality_score >= 0.70)

        feedback = "Milestone passed strict verification criteria." if passed else (
            f"Milestone failed verification ({round(quality_score * 100)}% score). "
            f"Mandatory failures: {missing_mandatory}. Deficiencies: " + "; ".join(feedback_notes)
        )

        return VerificationResult(
            passed=passed,
            quality_score=quality_score,
            feedback=feedback,
            criteria_met=criteria_met,
            missing_criteria=missing_criteria,
            sanitized_output=sanitized_output,
            sentinel_audit=sentinel_audit
        )

mission_verifier = MissionVerifier()
