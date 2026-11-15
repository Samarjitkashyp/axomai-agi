"""
Y4 Vishwakarma - FIDIC Engineering Contract Claims & Dispute Adjudication Engine.
Audits EPC claims under FIDIC Red, Yellow, and Silver Books (Clause 8.4 Extension of Time,
Clause 13 Variations, and Clause 20.1 28-Day Strict Notice Bar Rules).
"""

from typing import Dict, Any, List

class FIDICContractAuditor:
    """Audits contractual entitlement and dispute risk under international FIDIC conditions."""

    def __init__(self):
        self.standard_clauses = {
            "clause_8_4": "Extension of Time for Completion (Adverse climatic conditions / Employer delays)",
            "clause_13": "Variations and Adjustments (Right to vary, provisional sums, legislation changes)",
            "clause_17_3": "Employer's Risks (War, hostilities, exceptionally adverse physical conditions)",
            "clause_20_1": "Contractor's Claims (Mandatory 28-day notice period to prevent time-bar)"
        }

    def audit_contractor_claim(
        self,
        claim_type: str = "extension_of_time_eot",
        delay_event: str = "Brahmaputra high-flood water levels exceeding 100-year return period",
        notice_served_days_after_event: int = 18,
        quantified_eot_claim_days: int = 75,
        claimed_prolongation_cost_cr_inr: float = 14.50
    ) -> Dict[str, Any]:
        """
        Evaluates whether a contractor claim is legally admissible and calculates Dispute Adjudication Board (DAB) success probability.
        """
        # Strict FIDIC 28-day notice bar rule (Sub-Clause 20.1)
        is_time_barred = notice_served_days_after_event > 28

        entitlement_score = 0.0
        if not is_time_barred:
            entitlement_score = 85.0 if "flood" in delay_event.lower() or "climatic" in delay_event.lower() else 70.0
        else:
            entitlement_score = 15.0  # High likelihood of dismissal due to time bar

        # Probability of Dispute Adjudication Board (DAB) / Arbitration success
        dab_probability = round(entitlement_score / 100.0, 2)
        recommended_settlement_eot_days = int(quantified_eot_claim_days * 0.80) if not is_time_barred else 0
        recommended_prolongation_settlement_cr = round(claimed_prolongation_cost_cr_inr * 0.65, 2) if not is_time_barred else 0.0

        return {
            "claim_reference": "FIDIC Yellow Book (Plant & Design-Build) Claim",
            "evaluated_clause": "Clause 8.4 [Extension of Time] & Clause 20.1 [Contractor Claims]",
            "delay_event_description": delay_event,
            "notice_served_latency_days": f"{notice_served_days_after_event} Days post-event",
            "statutory_time_bar_status": "DISMISSED_TIME_BARRED (Exceeded 28-day window)" if is_time_barred else "ADMISSIBLE (Served within mandatory 28-day window)",
            "dab_adjudication_success_probability": dab_probability,
            "original_claimed_eot_days": quantified_eot_claim_days,
            "recommended_settlement_eot_days": recommended_settlement_eot_days,
            "claimed_prolongation_cost_cr": f"₹{claimed_prolongation_cost_cr_inr} Cr",
            "recommended_settlement_cost_cr": f"₹{recommended_prolongation_settlement_cr} Cr",
            "legal_engineering_verdict": (
                "Claim is legally robust under Clause 8.4(c) exceptionally adverse climatic conditions. "
                "Recommend executing an amicable commercial addendum granting 60 days EoT to waive liquidated damages."
                if not is_time_barred else
                "Claim is strictly time-barred under FIDIC Sub-Clause 20.1. Employer discharged from all liability."
            )
        }

fidic_contract_auditor = FIDICContractAuditor()

