"""
Y4 Vishwakarma - Primavera 4D & Earned Value Management (EVM) Delay Engine.
Computes Schedule Performance Index (SPI), Cost Performance Index (CPI), critical path schedule slippage,
and contractual Liquidated Damages (LD) liability for major highway, bridge, and EPC projects.
"""

from typing import Dict, Any

class PrimaveraDelayEngine:
    """Calculates EVM metrics, schedule variance, and EPC liquidated damages."""

    def __init__(self):
        pass

    def evaluate_epc_schedule_evm(
        self,
        project_name: str = "Brahmaputra Multimodal Bridge & Highway Link",
        budget_at_completion_cr_inr: float = 850.0,  # ₹850 Crore contract
        planned_value_pv_cr_inr: float = 480.0,      # ₹480 Cr expected at month 18
        earned_value_ev_cr_inr: float = 408.0,       # ₹408 Cr actual physical progress achieved
        actual_cost_ac_cr_inr: float = 445.0,        # ₹445 Cr spent to date
        contractual_completion_months: int = 36,
        elapsed_months: int = 18,
        ld_daily_penalty_pct: float = 0.05,          # 0.05% of contract value per day of delay
        max_ld_cap_pct: float = 10.0                 # Max 10% LD liability cap
    ) -> Dict[str, Any]:
        """
        Computes SPI, CPI, Estimate at Completion (EAC), projected milestone delay, and financial LD exposure.
        """
        # Variances
        schedule_variance_sv = round(earned_value_ev_cr_inr - planned_value_pv_cr_inr, 2)
        cost_variance_cv = round(earned_value_ev_cr_inr - actual_cost_ac_cr_inr, 2)

        # Performance Indices
        spi = round(earned_value_ev_cr_inr / max(planned_value_pv_cr_inr, 1.0), 3)
        cpi = round(earned_value_ev_cr_inr / max(actual_cost_ac_cr_inr, 1.0), 3)

        # Estimate at Completion: EAC = BAC / CPI
        eac_cr_inr = round(budget_at_completion_cr_inr / max(cpi, 0.1), 2)
        cost_overrun_cr_inr = round(eac_cr_inr - budget_at_completion_cr_inr, 2)

        # Projected Completion Time = Contract Duration / SPI
        projected_total_months = round(contractual_completion_months / max(spi, 0.1), 1)
        schedule_delay_months = round(projected_total_months - contractual_completion_months, 1)
        schedule_delay_days = int(schedule_delay_months * 30.4)

        # Contractual Liquidated Damages (LD)
        daily_ld_amount_cr_inr = budget_at_completion_cr_inr * (ld_daily_penalty_pct / 100.0)
        uncapped_ld_cr_inr = round(daily_ld_amount_cr_inr * schedule_delay_days, 2)
        max_ld_cap_cr_inr = round(budget_at_completion_cr_inr * (max_ld_cap_pct / 100.0), 2)
        enforceable_ld_cr_inr = min(uncapped_ld_cr_inr, max_ld_cap_cr_inr)

        return {
            "project_name": project_name,
            "budget_at_completion_bac_cr": f"₹{budget_at_completion_cr_inr:,.1f} Cr",
            "schedule_performance_index_spi": spi,
            "cost_performance_index_cpi": cpi,
            "schedule_variance_sv_cr": f"₹{schedule_variance_sv} Cr (Behind schedule)" if schedule_variance_sv < 0 else "On schedule",
            "cost_variance_cv_cr": f"₹{cost_variance_cv} Cr (Cost overrun)" if cost_variance_cv < 0 else "Under budget",
            "estimate_at_completion_eac_cr": f"₹{eac_cr_inr:,.1f} Cr (Overrun: +₹{cost_overrun_cr_inr} Cr)",
            "projected_completion_duration_months": f"{projected_total_months} Months (Delay: +{schedule_delay_months} Months)",
            "projected_delay_days": schedule_delay_days,
            "liquidated_damages_exposure_cr": f"₹{enforceable_ld_cr_inr:,.2f} Cr (Capped at {max_ld_cap_pct}%)",
            "critical_path_action": (
                "Issue statutory Clause 8.4 Extension of Time (EoT) claim based on unseasonable monsoon river surges "
                "to mitigate enforceable liquidated damages."
            )
        }

primavera_delay_engine = PrimaveraDelayEngine()

