"""
Z17 Apex-Global - Private Equity Letter of Intent (LOI) & Term Sheet Drafting Engine.
Drafts institutional, legally-vetted non-binding Letters of Intent (LOIs) and Term Sheets
with transaction consideration, escrow holdbacks, working capital collars, and exclusivity covenants.
"""

import datetime
from typing import Dict, Any, Optional

class LOITermSheetGenerator:
    """Generates institutional Private Equity acquisition Letters of Intent (LOIs)."""

    def draft_acquisition_loi(
        self,
        buyer_entity: str = "AxomAI Sovereign Capital Partners LP",
        target_entity: str = "Target Corporation",
        enterprise_value_m: float = 300.0,
        equity_purchase_price_m: float = 265.0,
        escrow_holdback_pct: float = 10.0,
        exclusivity_days: int = 45,
        target_nwc_m: float = 18.5
    ) -> Dict[str, Any]:
        """
        Drafts a comprehensive M&A Letter of Intent (LOI) with deal terms.
        """
        today_str = datetime.date.today().strftime("%B %d, %Y")
        escrow_amount_m = round(enterprise_value_m * (escrow_holdback_pct / 100.0), 2)
        cash_at_closing_m = round(equity_purchase_price_m - escrow_amount_m, 2)

        loi_sections = [
            {
                "article": "1. Transaction Structure & Consideration",
                "clause": (
                    f"Buyer proposes to acquire 100% of the fully-diluted equity interests of {target_entity} "
                    f"based on an agreed headline Enterprise Value of ${enterprise_value_m:,.1f}M (cash-free, debt-free). "
                    f"Net Equity Purchase Price payable to shareholders is estimated at ${equity_purchase_price_m:,.1f}M."
                )
            },
            {
                "article": "2. Consideration Breakdown & Escrow Holdback",
                "clause": (
                    f"At Closing, Buyer shall wire ${cash_at_closing_m:,.1f}M in cash directly to selling shareholders. "
                    f"An amount of ${escrow_amount_m:,.1f}M ({escrow_holdback_pct}% of Enterprise Value) will be deposited "
                    f"with a mutually agreed third-party escrow agent for an 18-month survival period to secure general indemnification claims."
                )
            },
            {
                "article": "3. Net Working Capital (NWC) Peg & Cash True-Up",
                "clause": (
                    f"The Purchase Price assumes a Normalized Target Net Working Capital of ${target_nwc_m:,.1f}M at Closing. "
                    f"A dollar-for-dollar upward or downward post-closing true-up will be conducted within 90 days following closing."
                )
            },
            {
                "article": "4. Exclusivity & Non-Solicitation Period",
                "clause": (
                    f"In consideration of Buyer committing substantial legal, accounting, and operational resources, "
                    f"Seller agrees to grant Buyer an exclusive negotiating period of {exclusivity_days} calendar days "
                    f"during which Seller shall not solicit, initiate, or engage in discussions with any third party."
                )
            },
            {
                "article": "5. Rep & Warranty Insurance (RWI) & Conditions to Closing",
                "clause": (
                    "Consummation of the Transaction is conditioned upon customary conditions precedent, including "
                    "completion of confirmatory due diligence, procurement of a buy-side Representation & Warranty Insurance (RWI) policy, "
                    "and receipt of required antitrust, regulatory, and corporate consents."
                )
            },
            {
                "article": "6. Governing Law & Jurisdiction",
                "clause": "This Letter of Intent and the Definitive Purchase Agreement shall be governed by Delaware General Corporation Law (DGCL) / English Commercial Arbitration."
            }
        ]

        formatted_loi_text = (
            f"**CONFIDENTIAL NON-BINDING LETTER OF INTENT (LOI)**\n\n"
            f"**Date:** {today_str}\n"
            f"**Buyer:** {buyer_entity}\n"
            f"**Target Company:** {target_entity}\n"
            f"**Headline Enterprise Valuation:** ${enterprise_value_m:,.1f}M\n\n"
            f"---\n\n"
        )
        for s in loi_sections:
            formatted_loi_text += f"### {s['article']}\n{s['clause']}\n\n"

        return {
            "title": f"ACQUISITION LETTER OF INTENT: {target_entity.upper()}",
            "date": today_str,
            "buyer": buyer_entity,
            "target": target_entity,
            "headline_enterprise_value_m": f"${enterprise_value_m:,.1f}M",
            "cash_at_closing_m": f"${cash_at_closing_m:,.1f}M",
            "escrow_holdback_m": f"${escrow_amount_m:,.1f}M ({escrow_holdback_pct}%)",
            "exclusivity_period": f"{exclusivity_days} Days",
            "sections": loi_sections,
            "formatted_loi_markdown": formatted_loi_text
        }

loi_generator = LOITermSheetGenerator()
