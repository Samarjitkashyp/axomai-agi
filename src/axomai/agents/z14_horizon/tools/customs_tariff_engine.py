"""
Z14 Horizon - Global Customs, HS Tariff & Trade Corridors Tool.
Maps Harmonized System (HS) Codes, Free Trade Agreements (FTA), and customs duty structures.
"""

from typing import Dict, Any, List

HS_CODE_DIRECTORY = {
    "0902": {
        "description": "Tea, whether or not flavored (Assam Black Tea, CTC, Green Tea)",
        "basic_customs_duty_pct": 100.0,
        "export_duty_pct": 0.0,
        "fta_preferences": {
            "UAE_CEPA": "Zero duty under bilateral quotas",
            "ASEAN_AIFTA": "Concessional 5% tariff",
            "AUSTRALIA_ECTA": "Duty-free quota access"
        },
        "sanitary_phytosanitary_reqs": "FSSAI Export Certificate, Maximum Residue Limit (MRL) Lab Clearance, Tea Board RCMC Registration"
    },
    "8471": {
        "description": "Automatic data processing machines, servers, and computing units",
        "basic_customs_duty_pct": 0.0, # ITA-1 Agreement
        "integrated_gst_pct": 18.0,
        "fta_preferences": {
            "GLOBAL_ITA": "Duty-Free under WTO ITA-1 Agreement"
        },
        "sanitary_phytosanitary_reqs": "BIS (Bureau of Indian Standards) Registration, EPR E-Waste Authorization"
    },
    "6204": {
        "description": "Women's or girls' suits, ensembles, jackets, dresses, skirts (Handloom & Silk)",
        "basic_customs_duty_pct": 20.0,
        "export_duty_pct": 0.0,
        "fta_preferences": {
            "UAE_CEPA": "Zero duty preferential access",
            "JAPAN_CEPA": "Zero duty with Certificate of Origin"
        },
        "sanitary_phytosanitary_reqs": "Textiles Committee Certificate of Origin, Silk Mark Certification"
    }
}

class CustomsTariffEngine:
    """Computes global landed costs, customs duty, and Free Trade Agreement benefits."""

    def calculate_landed_import_cost(
        self,
        cif_value_inr: float,
        hs_code: str = "8471",
        trade_partner: str = "United States"
    ) -> Dict[str, Any]:
        tariff = HS_CODE_DIRECTORY.get(hs_code, {
            "description": "General Commercial Merchandise",
            "basic_customs_duty_pct": 10.0,
            "integrated_gst_pct": 18.0,
            "sanitary_phytosanitary_reqs": "Standard Import Export Code (IEC) & Bill of Entry Filing"
        })

        bcd_rate = tariff.get("basic_customs_duty_pct", 10.0) / 100.0
        bcd_amount = round(cif_value_inr * bcd_rate, 2)

        # Social Welfare Surcharge (SWS): 10% of BCD
        sws_amount = round(bcd_amount * 0.10, 2)

        # Assessable value for IGST = CIF + BCD + SWS
        assessable_igst = cif_value_inr + bcd_amount + sws_amount
        igst_rate = tariff.get("integrated_gst_pct", 18.0) / 100.0
        igst_amount = round(assessable_igst * igst_rate, 2)

        total_customs_duty = round(bcd_amount + sws_amount + igst_amount, 2)
        total_landed_cost = round(cif_value_inr + total_customs_duty, 2)

        return {
            "hs_code": hs_code,
            "product_description": tariff["description"],
            "trade_partner": trade_partner.title(),
            "cif_value_inr": cif_value_inr,
            "basic_customs_duty_inr": bcd_amount,
            "social_welfare_surcharge_inr": sws_amount,
            "integrated_gst_inr": igst_amount,
            "total_customs_duty_inr": total_customs_duty,
            "effective_tariff_rate_pct": round((total_customs_duty / cif_value_inr) * 100, 2),
            "total_landed_cost_inr": total_landed_cost,
            "regulatory_filings": tariff.get("sanitary_phytosanitary_reqs", "Standard Clearance")
        }

customs_tariff_engine = CustomsTariffEngine()

