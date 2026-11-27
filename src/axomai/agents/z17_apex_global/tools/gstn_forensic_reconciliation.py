"""
Z17 Apex-Global - GSTN e-Invoicing & Forensic Tax Reconciliation Radar.
Reconciles GSTR-1 vs GSTR-3B vs GSTR-2B government returns, detects circular trading,
ghost invoicing, and quantifies Section 16(2)(c) Input Tax Credit (ITC) clawback liabilities.
"""

from typing import Dict, Any, List

class GSTNForensicReconciler:
    """Forensic tax analyzer for Indian GST returns and circular turnover verification."""

    def reconcile_tax_returns(
        self,
        reported_turnover_inr_cr: float = 150.0,
        gstr1_outward_turnover_inr_cr: float = 148.5,
        gstr3b_taxable_turnover_inr_cr: float = 142.0,
        gstr2b_eligible_itc_inr_cr: float = 18.2,
        gstr3b_claimed_itc_inr_cr: float = 21.8
    ) -> Dict[str, Any]:
        """
        Cross-reconciles GSTR-1, GSTR-3B, and GSTR-2B to flag artificial turnover and fake ITC.
        """
        # Turnover Variance (GSTR-1 vs GSTR-3B)
        turnover_diff_cr = round(abs(gstr1_outward_turnover_inr_cr - gstr3b_taxable_turnover_inr_cr), 2)
        turnover_mismatch_pct = round((turnover_diff_cr / max(gstr1_outward_turnover_inr_cr, 1.0)) * 100.0, 2)

        # ITC Mismatch (Claimed in 3B vs Auto-drafted in 2B from genuine suppliers)
        excess_itc_claimed_cr = round(max(0.0, gstr3b_claimed_itc_inr_cr - gstr2b_eligible_itc_inr_cr), 2)
        itc_mismatch_pct = round((excess_itc_claimed_cr / max(gstr2b_eligible_itc_inr_cr, 1.0)) * 100.0, 2)

        # Potential Department Demand under Section 73 / 74:
        # Excess ITC + 18% Mandatory Interest + 100% Penalty
        tax_demand_cr = excess_itc_claimed_cr
        interest_demand_cr = round(tax_demand_cr * 0.18, 2)
        penalty_demand_cr = tax_demand_cr  # 100% penalty under Section 122/74
        total_gst_clawback_exposure_cr = round(tax_demand_cr + interest_demand_cr + penalty_demand_cr, 2)
        total_gst_exposure_usd_m = round(total_gst_clawback_exposure_cr * 0.12, 2)

        # Circular Trading / Ghost Invoicing Risk
        is_circular_trading = turnover_mismatch_pct > 4.0 or itc_mismatch_pct > 10.0
        risk_grade = "CRITICAL_CIRCULAR_TRADING_SUSPECTED" if is_circular_trading else "CLEAN_GST_RECONCILIATION"

        # Forensic Audit Findings
        findings = [
            {
                "checkpoint": "Turnover Reconciliation (GSTR-1 vs GSTR-3B)",
                "gstr1_sales": f"₹{gstr1_outward_turnover_inr_cr} Cr",
                "gstr3b_sales": f"₹{gstr3b_taxable_turnover_inr_cr} Cr",
                "variance": f"₹{turnover_diff_cr} Cr ({turnover_mismatch_pct}%)",
                "status": "FLAGGED_MISMATCH" if turnover_mismatch_pct > 3.0 else "PASSED"
            },
            {
                "checkpoint": "Input Tax Credit Validity (GSTR-2B vs GSTR-3B)",
                "gstr2b_supplier_itc": f"₹{gstr2b_eligible_itc_inr_cr} Cr",
                "gstr3b_availed_itc": f"₹{gstr3b_claimed_itc_inr_cr} Cr",
                "unmatched_itc": f"₹{excess_itc_claimed_cr} Cr ({itc_mismatch_pct}%)",
                "status": "SECTION_16_CLAWBACK_RISK" if excess_itc_claimed_cr > 0.5 else "PASSED"
            }
        ]

        return {
            "gstin_audit_status": risk_grade,
            "reported_turnover_inr_cr": f"₹{reported_turnover_inr_cr} Cr",
            "turnover_variance_cr": f"₹{turnover_diff_cr} Cr",
            "turnover_mismatch_pct": f"{turnover_mismatch_pct}%",
            "excess_itc_claimed_cr": f"₹{excess_itc_claimed_cr} Cr",
            "statutory_gst_clawback_exposure_cr": f"₹{total_gst_clawback_exposure_cr} Cr",
            "statutory_gst_clawback_exposure_usd_m": f"${total_gst_exposure_usd_m}M",
            "reconciliation_findings": findings,
            "indemnity_escrow_deduction_recommendation": (
                f"Deduct ₹{total_gst_clawback_exposure_cr} Cr (${total_gst_exposure_usd_m}M) directly from Purchase Price into a Special GST Tax Indemnity Escrow "
                f"to protect buyer against pending DGGI / State GST audit summons under Section 74."
            )
        }

gstn_reconciler = GSTNForensicReconciler()
