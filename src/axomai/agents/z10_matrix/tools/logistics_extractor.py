"""
Z10 Matrix - Dynamic Logistics & Supply Chain Query Extractor.
Extracts origin/destination cities (any Indian or global city), cargo weight (tons/kg),
invoice value (INR), monthly sales units, cold-chain flags, EV fleet preferences,
and ODC (Over-Dimensional Cargo) flags from natural language prompts.
"""

import re
from typing import Dict, Any, List, Optional


class LogisticsQueryExtractor:
    """Extracts structured freight, routing, and inventory parameters from user prompts."""

    KNOWN_CITIES = [
        "mumbai", "delhi", "new delhi", "bengaluru", "bangalore", "chennai", "kolkata",
        "hyderabad", "ahmedabad", "pune", "jaipur", "lucknow", "patna", "surat", "nagpur",
        "indore", "bhopal", "visakhapatnam", "kochi", "chandigarh", "bhubaneswar",
        "guwahati", "changsari", "nagaon", "dibrugarh", "jorhat", "silchar", "tezpur",
        "tinsukia", "golaghat", "sivasagar", "lakhimpur", "bongaigaon", "dhubri", "barpeta",
        "shillong", "imphal", "agartala", "aizawl", "dimapur", "kohima", "itanagar", "gangtok",
        "dubai", "singapore", "london", "rotterdam", "new york"
    ]

    def parse_logistics_query(self, query: str) -> Dict[str, Any]:
        q_lower = query.lower()

        # 1. Extract explicit "from X to Y, Z" pattern first
        origin = None
        destinations: List[str] = []

        from_to = re.search(r'\bfrom\s+([A-Za-z\s]+?)\s+to\s+([A-Za-z0-9,\s&]+?)(?:\s+with|\s+carrying|\s+for|\s+in|\.|$)', query, re.IGNORECASE)
        if from_to:
            orig_cand = from_to.group(1).strip().title()
            if len(orig_cand) >= 3:
                origin = orig_cand
            dest_raw = re.split(r',|\band\b|&', from_to.group(2))
            for d in dest_raw:
                dc = d.strip().title()
                if len(dc) >= 3 and dc.lower() != (origin or "").lower():
                    destinations.append(dc)

        # 2. Fallback / Supplement with Known Cities scan in order of appearance
        found_cities = []
        for city in self.KNOWN_CITIES:
            m = re.search(r'\b' + re.escape(city) + r'\b', q_lower)
            if m:
                found_cities.append((m.start(), city.title()))
        found_cities.sort(key=lambda x: x[0])

        if not origin and found_cities:
            origin = found_cities[0][1]
            for _, c in found_cities[1:]:
                if c not in destinations and c != origin:
                    destinations.append(c)
        elif origin and not destinations:
            for _, c in found_cities:
                if c != origin and c not in destinations:
                    destinations.append(c)

        if not origin:
            origin = "Guwahati"
        if not destinations:
            destinations = ["Dibrugarh", "Silchar"] if origin == "Guwahati" else ["Delhi", "Bengaluru"]

        # 3. Extract Cargo Weight (Tons or Kg)
        cargo_tons = 12.0
        m_tons = re.search(r'(\d+(?:\.\d+)?)\s*(?:ton|tons|tonne|tonnes|mt)\b', q_lower)
        if m_tons:
            cargo_tons = float(m_tons.group(1))
        else:
            m_kg = re.search(r'(\d+(?:\.\d+)?)\s*kg\b', q_lower)
            if m_kg:
                cargo_tons = round(float(m_kg.group(1)) / 1000.0, 2)

        # 4. Extract Invoice / Consignment Value (INR) for GST E-Way Bill
        invoice_value_inr = 250000.0
        m_cr = re.search(r'(?:value|worth|invoice|cargo|consignment)[^.\n]{0,25}?(?:inr|rs\.?|₹)\s*([\d,]+(?:\.\d+)?)\s*(?:cr|crore)\b', q_lower)
        m_lakh = re.search(r'(?:value|worth|invoice|cargo|consignment)[^.\n]{0,25}?(?:inr|rs\.?|₹)\s*([\d,]+(?:\.\d+)?)\s*(?:lakh|lac|l)\b', q_lower)
        m_inr = re.search(r'(?:value|worth|invoice|cargo|consignment)[^.\n]{0,25}?(?:inr|rs\.?|₹)\s*([\d,]+(?:\.\d+)?)', q_lower)
        if m_cr:
            invoice_value_inr = float(m_cr.group(1).replace(",", "")) * 10_000_000.0
        elif m_lakh:
            invoice_value_inr = float(m_lakh.group(1).replace(",", "")) * 100_000.0
        elif m_inr:
            invoice_value_inr = float(m_inr.group(1).replace(",", ""))

        # 5. Extract Monthly Sales Units
        m_units = re.search(r'(\d[\d,]*)\s*(?:units|boxes|cartons|cases)(?:/month|\s+per\s+month|\s+monthly)?', q_lower)
        monthly_sales_units = int(m_units.group(1).replace(",", "")) if m_units else 1500

        # 6. Extract Flags (Cold Chain, EV, ODC, Riverway/Rail)
        is_cold_chain = any(k in q_lower for k in ["cold chain", "cold-chain", "reefer", "pharma", "vaccine", "dairy", "frozen", "perishable", "temperature"])
        temp_m = re.search(r'(-?\d+(?:\.\d+)?)\s*°?\s*c\b', q_lower)
        target_temp_c = float(temp_m.group(1)) if temp_m else (4.0 if is_cold_chain else None)

        is_odc = any(k in q_lower for k in ["odc", "over-dimensional", "over dimensional", "heavy machinery", "turbine", "transformer"])
        prefer_ev = any(k in q_lower for k in ["ev ", "electric truck", "carbon", "scope 3", "green freight", "net zero"])
        is_multimodal = any(k in q_lower for k in ["rail", "concor", "river", "waterway", "nw-2", "brahmaputra", "barge", "multimodal", "air cargo"])

        return {
            "origin": origin,
            "destinations": destinations,
            "cargo_tons": cargo_tons,
            "invoice_value_inr": invoice_value_inr,
            "monthly_sales_units": monthly_sales_units,
            "is_cold_chain": is_cold_chain,
            "target_temp_c": target_temp_c,
            "is_odc": is_odc,
            "prefer_ev": prefer_ev,
            "is_multimodal": is_multimodal,
            "raw_query": query
        }


logistics_extractor = LogisticsQueryExtractor()
