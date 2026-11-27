"""
Z17 Apex-Global - Forensic Accounting & Balance Sheet Fraud Radar.
Calculates the 8-ratio Beneish M-Score (earnings manipulation fraud detection)
and the 5-ratio Altman Z-Score (credit distress and corporate bankruptcy prediction).
"""

from typing import Dict, Any

class ForensicAccountingRadar:
    """Forensic accounting analyzer applying Beneish M-Score and Altman Z-Score models."""

    def compute_beneish_m_score(
        self,
        dsri: float = 1.05,
        gmi: float = 1.02,
        aqi: float = 1.01,
        sgi: float = 1.14,
        depi: float = 1.00,
        sgai: float = 0.98,
        lvgi: float = 1.04,
        tata: float = 0.025
    ) -> Dict[str, Any]:
        """
        Computes the 8-variable Beneish M-Score.
        A score greater than -1.78 indicates high probability of accounting manipulation.
        """
        m_score = (
            -4.84
            + (0.920 * dsri)
            + (0.528 * gmi)
            + (0.404 * aqi)
            + (0.892 * sgi)
            + (0.115 * depi)
            - (0.172 * sgai)
            + (4.037 * tata)
            + (0.0327 * lvgi)
        )
        m_score = round(m_score, 2)

        # Standard academic threshold: -1.78
        is_manipulator = m_score > -1.78

        return {
            "beneish_m_score": m_score,
            "manipulation_threshold": -1.78,
            "verdict": "HIGH_MANIPULATION_RISK (Earnings Obfuscation Suspected)" if is_manipulator else "CLEAN_AUDIT (Low Manipulation Probability)",
            "risk_grade": "RED_FLAG_AUDIT" if is_manipulator else "LOW_RISK_PASSED",
            "ratio_breakdown": {
                "DSRI_days_sales_receivables": dsri,
                "GMI_gross_margin_index": gmi,
                "AQI_asset_quality_index": aqi,
                "SGI_sales_growth_index": sgi,
                "DEPI_depreciation_index": depi,
                "SGAI_sga_expense_index": sgai,
                "LVGI_leverage_index": lvgi,
                "TATA_total_accruals_to_assets": tata
            },
            "analyst_notes": (
                "Earnings quality shows elevated accruals or aggressive revenue recognition; recommend forensic working capital audit."
                if is_manipulator else
                "Reported earnings demonstrate high cash conversion and standard accrual ratios consistent with GAAP/IFRS standards."
            )
        }

    def compute_altman_z_score(
        self,
        working_capital_m: float = 25.0,
        retained_earnings_m: float = 65.0,
        ebit_m: float = 38.0,
        market_val_equity_m: float = 400.0,
        total_liabilities_m: float = 150.0,
        total_assets_m: float = 320.0,
        revenue_m: float = 240.0
    ) -> Dict[str, Any]:
        """
        Computes Altman Z-Score for corporate solvency:
        Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
        - Z > 2.99: Safe Zone (Solvent)
        - 1.81 <= Z <= 2.99: Grey Zone (Caution)
        - Z < 1.81: Distress Zone (Insolvency Probability)
        """
        x1 = working_capital_m / max(total_assets_m, 1.0)
        x2 = retained_earnings_m / max(total_assets_m, 1.0)
        x3 = ebit_m / max(total_assets_m, 1.0)
        x4 = market_val_equity_m / max(total_liabilities_m, 1.0)
        x5 = revenue_m / max(total_assets_m, 1.0)

        z_score = round((1.2 * x1) + (1.4 * x2) + (3.3 * x3) + (0.6 * x4) + (1.0 * x5), 2)

        if z_score >= 2.99:
            zone = "SAFE_ZONE"
            credit_health = "Pristine Balance Sheet (Near-Zero 2-Year Bankruptcy Probability)"
        elif z_score >= 1.81:
            zone = "GREY_ZONE"
            credit_health = "Moderate Vulnerability (Refinancing Risk Under Macro Headwinds)"
        else:
            zone = "DISTRESS_ZONE"
            credit_health = "Severe Liquidity Strain (High Default Risk Within 24 Months)"

        return {
            "altman_z_score": z_score,
            "solvency_zone": zone,
            "credit_health_summary": credit_health,
            "sub_factors": {
                "X1_working_capital_to_assets": round(x1, 3),
                "X2_retained_earnings_to_assets": round(x2, 3),
                "X3_ebit_to_assets": round(x3, 3),
                "X4_equity_to_liabilities": round(x4, 3),
                "X5_asset_turnover": round(x5, 3)
            }
        }

forensic_radar = ForensicAccountingRadar()
