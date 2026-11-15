"""
Z13 Quantum - Dynamic Price Elasticity & Margin Optimization Engine.
Computes price elasticity of demand, competitor undercut defense, and optimal retail markups.
"""

from typing import Dict, Any, List

class PriceElasticityEngine:
    """Calculates price optimization curves and competitor defense strategies."""

    def compute_pricing_strategy(
        self,
        product_category: str,
        procurement_cost_inr: float,
        competitor_price_inr: float,
        elasticity_type: str = "moderate"
    ) -> Dict[str, Any]:
        elasticities = {
            "staples": -0.7, # inelastic, necessity goods
            "moderate": -1.3, # normal FMCG
            "lifestyle": -2.2 # highly elastic, luxury / premium
        }
        e = elasticities.get(elasticity_type.lower(), -1.3)

        # Target markup based on category
        markup_pct = 0.22 if elasticity_type == "staples" else (0.35 if elasticity_type == "moderate" else 0.55)
        optimal_price = round(procurement_cost_inr * (1 + markup_pct), 2)

        # Competitor delta
        comp_diff_pct = round(((optimal_price - competitor_price_inr) / competitor_price_inr) * 100, 1)

        recommendation = ""
        if comp_diff_pct > 5.0:
            recommendation = "Bundle with fast-moving commodity staple or introduce a 'Value-Pack' to preserve gross margin."
        elif comp_diff_pct < -5.0:
            recommendation = "Strong price advantage; highlight superior regional procurement quality on retail shelf."
        else:
            recommendation = "Competitive parity; deploy loyalty point multiplier and localized Assamese branding."

        return {
            "category": product_category.title(),
            "procurement_cost_inr": procurement_cost_inr,
            "competitor_price_inr": competitor_price_inr,
            "optimal_retail_price_inr": optimal_price,
            "gross_margin_pct": round(markup_pct * 100, 1),
            "competitor_delta_pct": comp_diff_pct,
            "elasticity_coefficient": e,
            "strategic_recommendation": recommendation
        }

price_elasticity_engine = PriceElasticityEngine()

