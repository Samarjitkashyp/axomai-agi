"""
Z11 Pragati - Assam Governance & MSME Policy Intelligence Tool.
Maps commercial enterprises, youth startups, and retail projects
to active Assam state subsidies, industrial incentives, and digital land rules.
"""

from typing import Dict, Any, List

ASSAM_SCHEMES_DATABASE = [
    {
        "scheme_name": "Chief Minister Atmanirbhar Asom Abhijan (CMAAA)",
        "department": "Department of Industries & Commerce, Assam",
        "category": "Youth & MSME Self-Employment",
        "financial_benefit": "₹2 Lakhs (Tier 1) to ₹5 Lakhs (Tier 2) financial grant (50% direct subsidy + 50% zero-interest government loan).",
        "eligibility": "Age 18-40, resident of Assam, Class 10/12/ITI/Diploma, no commercial bank loan default.",
        "application_portal": "cmaaa.assam.gov.in",
        "relevance_score": 95
    },
    {
        "scheme_name": "Assam Industrial & Investment Policy 2023",
        "department": "AIDC / Industries & Commerce",
        "category": "Industrial & Retail Expansion Capital Incentives",
        "financial_benefit": "30% Capital Investment Subsidy (up to ₹5 Crore), 100% Stamp Duty reimbursement, 100% Electricity Duty exemption for 5 years, State GST reimbursement up to 150% of fixed capital.",
        "eligibility": "Registered commercial establishment in designated Assam industrial growth centers or private retail networks with local workforce quota (> 70%).",
        "application_portal": "easeofdoingbusiness.assam.gov.in",
        "relevance_score": 92
    },
    {
        "scheme_name": "Biponi Scheme (ASIDC)",
        "department": "Assam Small Industries Development Corporation",
        "category": "Market Exposure & Indigenous Product Retail Support",
        "financial_benefit": "Financial assistance of ₹2 Lakh to ₹5 Lakh for establishing regional display counters and marketing ethnic Assam products.",
        "eligibility": "Enterprises retailing Assam silk (Muga/Eri), Assam tea, bell metal, handloom, or localized processed food products.",
        "application_portal": "asidc.assam.gov.in",
        "relevance_score": 88
    },
    {
        "scheme_name": "Mission Basundhara 3.0 (Land Governance)",
        "department": "Revenue & Disaster Management Department, Assam",
        "category": "Land Rights, Patta Conversion & Mutation",
        "financial_benefit": "Instant online mutation, conversion of Annual Patta to Periodic Patta, and fast-track NOC for commercial industrial lease setup.",
        "eligibility": "Registered landholders and registered commercial tenants holding valid land revenue documents.",
        "application_portal": "basundhara.assam.gov.in",
        "relevance_score": 85
    },
    {
        "scheme_name": "Prime Minister Employment Generation Programme (PMEGP)",
        "department": "KVIC / State KVIB & District Industries Centers (DIC)",
        "category": "Credit-Linked Subsidy Scheme",
        "financial_benefit": "Subsidy of 25% (Urban) to 35% (Rural/Special Category) on project costs up to ₹50 Lakhs (Manufacturing) / ₹20 Lakhs (Service/Retail).",
        "eligibility": "Any individual above 18 years; 8th pass for projects above ₹10 Lakhs in manufacturing.",
        "application_portal": "kviconline.gov.in",
        "relevance_score": 90
    }
]

class SchemeMatcher:
    """Matches business goals to actionable Assam state & central subsidies."""

    def match_schemes(self, query: str) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        matched = []
        for s in ASSAM_SCHEMES_DATABASE:
            score = s["relevance_score"]
            if any(k in q_lower for k in ["retail", "store", "shop", "expansion"]) and "Retail" in s["category"]:
                score += 5
            if any(k in q_lower for k in ["land", "patta", "lease", "basundhara"]) and "Land" in s["category"]:
                score += 15
            if any(k in q_lower for k in ["subsidy", "loan", "grant", "funding"]) and "Financial" in s["financial_benefit"]:
                score += 5
            matched.append({**s, "adjusted_score": score})
        
        matched.sort(key=lambda x: x["adjusted_score"], reverse=True)
        return matched[:4]

scheme_matcher = SchemeMatcher()

