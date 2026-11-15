"""
Z14 Horizon - EU Carbon Border Adjustment Mechanism (CBAM) Engine.
Calculates embedded direct and indirect GHG emissions and EU ETS carbon border tax liability.
"""

from typing import Dict, Any

class CBAMEngine:
    """Calculates EU CBAM embedded emissions and carbon tariff liability."""

    def __init__(self):
        # Default EU ETS carbon price in EUR per metric ton CO2e (2026 average)
        self.eu_ets_carbon_price_eur = 78.50  # €78.50 / tCO2e
        self.eur_inr_rate = 91.20

        # Standard embedded emissions factors (tCO2e per metric ton of finished product)
        self.emission_factors = {
            "iron_steel": {"direct": 1.85, "indirect": 0.45},
            "aluminum": {"direct": 2.10, "indirect": 6.80},
            "fertilizers": {"direct": 2.60, "indirect": 0.30},
            "cement": {"direct": 0.72, "indirect": 0.08},
            "hydrogen": {"direct": 9.30, "indirect": 1.20},
            "tea_agri": {"direct": 0.40, "indirect": 0.15},  # Scope 1 & 2 packaging/processing
        }

    def calculate_cbam_liability(
        self,
        sector: str,
        shipment_weight_metric_tons: float,
        domestic_carbon_price_paid_eur: float = 0.0,
        free_allowance_phase_out_pct: float = 0.975  # 2026 starts with 2.5% reduction (97.5% free allowance remaining)
    ) -> Dict[str, Any]:
        """
        Computes CBAM certificates required and total financial liability under EU Regulation 2023/956.
        """
        sector_key = sector.lower().replace(" ", "_")
        factors = self.emission_factors.get(sector_key, {"direct": 1.0, "indirect": 0.3})

        direct_emissions = round(shipment_weight_metric_tons * factors["direct"], 2)
        indirect_emissions = round(shipment_weight_metric_tons * factors["indirect"], 2)
        total_embedded_emissions = round(direct_emissions + indirect_emissions, 2)

        # Taxable emissions after applying EU ETS free allocation phase-out
        # During 2026 transition, taxable portion starts gradually phasing in
        taxable_emissions_factor = 1.0 - free_allowance_phase_out_pct
        taxable_emissions_tons = round(total_embedded_emissions * taxable_emissions_factor, 2)

        gross_cbam_liability_eur = round(taxable_emissions_tons * self.eu_ets_carbon_price_eur, 2)
        net_cbam_liability_eur = max(0.0, round(gross_cbam_liability_eur - (domestic_carbon_price_paid_eur * taxable_emissions_tons), 2))
        net_cbam_liability_inr = round(net_cbam_liability_eur * self.eur_inr_rate, 2)

        return {
            "sector": sector,
            "shipment_weight_metric_tons": shipment_weight_metric_tons,
            "direct_emissions_tco2e": direct_emissions,
            "indirect_emissions_tco2e": indirect_emissions,
            "total_embedded_emissions_tco2e": total_embedded_emissions,
            "eu_ets_benchmark_price_eur": self.eu_ets_carbon_price_eur,
            "free_allowance_phase_out_pct": round((1.0 - free_allowance_phase_out_pct) * 100, 2),
            "taxable_emissions_tco2e": taxable_emissions_tons,
            "net_cbam_liability_eur": net_cbam_liability_eur,
            "net_cbam_liability_inr": net_cbam_liability_inr,
            "effective_carbon_tax_per_ton_eur": round(net_cbam_liability_eur / max(shipment_weight_metric_tons, 1.0), 2),
            "compliance_requirement": (
                "Mandatory quarterly reporting to EU CBAM Registry with verified installation-specific emissions."
            )
        }

cbam_engine = CBAMEngine()

