"""
Z10 Matrix - Act East Policy Cross-Border & ICP Land Customs Engine.
Models India-Bangladesh Protocol Routes (NW-2/NW-16, Dawki, Sutarkandi, Petrapole)
and India-Myanmar-Thailand Trilateral Highway (Moreh-Tamu ICP), predicting customs
dwell times, RFID e-Seal compliance, and Jogighopa MMLP transit staging.
"""

from typing import Dict, Any, Optional


ICP_BORDER_STATIONS = {
    "petrapole": {"border": "India-Bangladesh (West Bengal)", "avg_customs_dwell_hrs": 18.0, "protocol": "ICEGATE + BBIN Motor Vehicles"},
    "dawki": {"border": "India-Bangladesh (Meghalaya)", "avg_customs_dwell_hrs": 8.5, "protocol": "LCS Limestone & Stone Export Corridor"},
    "sutarkandi": {"border": "India-Bangladesh (Karimganj, Assam)", "avg_customs_dwell_hrs": 10.0, "protocol": "Barak Valley Trade & Cement/Agri Corridor"},
    "moreh": {"border": "India-Myanmar-Thailand (Manipur)", "avg_customs_dwell_hrs": 22.0, "protocol": "Act East Trilateral Highway ICP"},
    "jogighopa": {"border": "Assam Multi-Modal Logistics Park (MMLP)", "avg_customs_dwell_hrs": 3.5, "protocol": "Road-Rail-NW2 Riverway Customs Bonded Hub"}
}


class ActEastCustomsEngine:
    """Evaluates Northeast Cross-Border ICP Customs Clearance & e-Seal Compliance."""

    def evaluate_cross_border_corridor(
        self,
        origin: str,
        destination: str,
        consignment_value_inr: float = 250000.0
    ) -> Dict[str, Any]:
        dest_l = destination.lower()
        orig_l = origin.lower()

        if "silchar" in dest_l or "agartala" in dest_l or "bangladesh" in dest_l:
            icp_key = "sutarkandi"
        elif "shillong" in dest_l or "dawki" in dest_l:
            icp_key = "dawki"
        elif "imphal" in dest_l or "myanmar" in dest_l or "moreh" in dest_l:
            icp_key = "moreh"
        elif "kolkata" in dest_l or "kolkata" in orig_l:
            icp_key = "petrapole"
        else:
            icp_key = "jogighopa"

        icp = ICP_BORDER_STATIONS[icp_key]
        rfid_eseal_required = consignment_value_inr >= 100000.0

        return {
            "act_east_corridor_hub": icp_key.title(),
            "border_jurisdiction": icp["border"],
            "predicted_customs_dwell_hrs": icp["avg_customs_dwell_hrs"],
            "customs_protocol": icp["protocol"],
            "icegate_rfid_eseal_mandated": rfid_eseal_required,
            "jogighopa_mmlp_integration": "Available for NW-2 Brahmaputra barge transshipment & bonded warehousing"
        }


act_east_customs = ActEastCustomsEngine()
