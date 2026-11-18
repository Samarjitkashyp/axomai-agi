"""
Z11 Pragati - Global Public Policy, Statutory Compliance & Sovereign Incentives Engine.
Maps commercial enterprises, industrial scale-ups, and technology initiatives
to active National, Provincial/State, and Global industrial subsidies, tax holidays, and regulatory frameworks.
"""

from typing import Dict, Any, List

GLOBAL_POLICY_SCHEMES_DATABASE = [
    # 1. National & Federal Flagship Policies (Uniformly Applicable)
    {
        "scheme_name": "Prime Minister Employment Generation Programme (PMEGP)",
        "jurisdiction": "National / Federal (India)",
        "department": "Ministry of MSME / KVIC / State KVIB & DIC",
        "category": "Credit-Linked Capital Subsidy",
        "financial_benefit": "Direct capital subsidy of 15% to 35% on projects up to ₹50 Lakhs (Manufacturing) / ₹20 Lakhs (Service/Retail).",
        "eligibility": "Individuals 18+, self-help groups, registered MSMEs without commercial loan default.",
        "application_portal": "kviconline.gov.in",
        "keywords": ["msme", "pmegp", "self-employment", "retail", "manufacturing", "loan", "subsidy"],
        "relevance_score": 90
    },
    {
        "scheme_name": "Startup India Seed Fund Scheme (SISFS)",
        "jurisdiction": "National / Federal (India)",
        "department": "DPIIT, Ministry of Commerce and Industry",
        "category": "Technology Startup & Innovation Grant",
        "financial_benefit": "Up to ₹20 Lakhs as grant for proof-of-concept/prototype validation, and up to ₹50 Lakhs via convertible debentures or debt-linked investments.",
        "eligibility": "DPIIT-recognized startups incorporated within 2 years with viable technology-enabled product or business model.",
        "application_portal": "seedfund.startupindia.gov.in",
        "keywords": ["startup", "seed fund", "dpiit", "innovation", "technology", "grant"],
        "relevance_score": 92
    },
    {
        "scheme_name": "Production Linked Incentive (PLI) Scheme",
        "jurisdiction": "National / Global (India)",
        "department": "Ministry of Commerce & Industry / Line Ministries",
        "category": "Large-Scale Industrial & High-Tech Manufacturing",
        "financial_benefit": "4% to 6% cash incentive on incremental sales of manufactured goods over baseline year for 5 years.",
        "eligibility": "Enterprises meeting threshold minimum greenfield investment and incremental production targets in designated sectors.",
        "application_portal": "pli.gov.in",
        "keywords": ["pli", "manufacturing", "production", "electronics", "pharmaceuticals", "fab", "scale"],
        "relevance_score": 94
    },
    {
        "scheme_name": "CGTMSE Collateral-Free Credit Guarantee",
        "jurisdiction": "National / Federal (India)",
        "department": "Ministry of MSME & SIDBI",
        "category": "Credit Guarantee & Debt Financing",
        "financial_benefit": "Credit guarantee coverage up to 85% for collateral-free credit facilities up to ₹500 Lakhs (₹5 Crore).",
        "eligibility": "New and existing Micro and Small Enterprises engaged in manufacturing or service/trading activities.",
        "application_portal": "cgtmse.in",
        "keywords": ["credit guarantee", "collateral free", "sidbi", "loan", "bank loan", "cgtmse"],
        "relevance_score": 88
    },
    # 2. Global Trade & Export Promotion Frameworks
    {
        "scheme_name": "Export Promotion Capital Goods (EPCG) & Advance Authorisation",
        "jurisdiction": "Global / International Trade",
        "department": "Directorate General of Foreign Trade (DGFT)",
        "category": "Global Export Incentives & Zero-Duty Import",
        "financial_benefit": "Zero customs duty import of capital goods and raw materials against export obligation of 6x duty saved over 6 years.",
        "eligibility": "Manufacturer exporters and merchant exporters with valid Importer-Exporter Code (IEC).",
        "application_portal": "dgft.gov.in",
        "keywords": ["export", "import", "customs", "epcg", "dgft", "cross-border", "global trade"],
        "relevance_score": 91
    },
    {
        "scheme_name": "Special Economic Zone (SEZ) / FTWZ Tax Holiday",
        "jurisdiction": "Global / Sovereign Free Zone",
        "department": "Ministry of Commerce / SEZ Authorities",
        "category": "Export Hub & Duty-Free Zone",
        "financial_benefit": "100% income tax exemption on export income for 5 years, 50% for next 5 years; zero basic customs duty on all input imports.",
        "eligibility": "Commercial entities established in notified SEZs or Free Trade Warehousing Zones with positive net foreign exchange.",
        "application_portal": "sezindia.nic.in",
        "keywords": ["sez", "free trade zone", "ftwz", "tax holiday", "duty exemption", "tariff"],
        "relevance_score": 89
    },
    # 3. Dynamic State / Provincial Policies (Resolved on demand)
    {
        "scheme_name": "State Single Window Clearance & Industrial Investment Policy",
        "jurisdiction": "Provincial / State Single Window Systems",
        "department": "State Industrial Development Corporations (AIDC, MIDC, GIDC, KSIIDC, etc.)",
        "category": "Industrial Land, Electricity Exemption & Stamp Duty Rebate",
        "financial_benefit": "Capital investment subsidies (15% to 35%), 100% stamp duty waiver, and electricity duty exemption for 5 to 7 years.",
        "eligibility": "Registered commercial and manufacturing units setting up facilities in designated state industrial parks or commercial zones.",
        "application_portal": "national-single-window.gov.in / nsws.gov.in",
        "keywords": ["single window", "industrial policy", "stamp duty", "state subsidy", "patta", "land", "midc", "gidc", "aidc", "cmaaa", "basundhara"],
        "relevance_score": 93
    }
]

class SchemeMatcher:
    """Matches business goals to actionable National, State, and Global policy subsidies."""

    def match_schemes(self, query: str) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        matched = []

        # Detect jurisdiction preference from query
        is_global = any(k in q_lower for k in ["global", "international", "cross-border", "export", "import", "foreign", "trade"])
        is_startup = any(k in q_lower for k in ["startup", "seed", "tech", "software", "ai", "app", "innovation"])
        is_manufacturing = any(k in q_lower for k in ["manufactur", "factory", "plant", "industrial", "production", "pli"])
        is_credit = any(k in q_lower for k in ["loan", "collateral", "funding", "bank", "credit", "finance"])

        for s in GLOBAL_POLICY_SCHEMES_DATABASE:
            score = s["relevance_score"]

            # Query keyword resonance
            matched_keywords = sum(1 for kw in s["keywords"] if kw in q_lower)
            score += matched_keywords * 4

            if is_global and "Global" in s["jurisdiction"]:
                score += 15
            if is_startup and "Startup" in s["category"]:
                score += 15
            if is_manufacturing and "Manufacturing" in s["category"]:
                score += 12
            if is_credit and ("Credit" in s["category"] or "Capital" in s["category"]):
                score += 10

            matched.append({**s, "adjusted_score": score})

        matched.sort(key=lambda x: x["adjusted_score"], reverse=True)
        return matched[:4]

scheme_matcher = SchemeMatcher()
