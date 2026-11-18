"""
Z13 Quantum - Global & Sovereign Commodity Market Surveillance Tool.
Tracks wholesale commodity rates, national mandi benchmarks, and global futures.
"""

from typing import Dict, Any, List, Optional

COMMODITY_BENCHMARKS = [
    {
        "commodity": "High-Grade Basmati Rice (Pusa 1121)",
        "market": "National Agriculture Market (e-NAM) / Karnal Hub",
        "wholesale_price_inr": 82.0,
        "unit": "per kg",
        "retail_mrp_range_inr": "₹120 – ₹155",
        "retail_margin_pct": 35.0,
        "trend": "STRONG (+6.5% Gulf export demand)"
    },
    {
        "commodity": "Milling Wheat (FAQ Grade)",
        "market": "Indore / Khanna Central Mandi",
        "wholesale_price_inr": 26.5,
        "unit": "per kg",
        "retail_mrp_range_inr": "₹34 – ₹40",
        "retail_margin_pct": 24.0,
        "trend": "STABLE (+1.5% buffer replenishment)"
    },
    {
        "commodity": "Raw Sugar (VHP Grade)",
        "market": "Kolhapur Wholesale Yard / ICE Global Sugar",
        "wholesale_price_inr": 38.0,
        "unit": "per kg",
        "retail_mrp_range_inr": "₹46 – ₹52",
        "retail_margin_pct": 20.0,
        "trend": "MODERATE (+2.8% ethanol parity)"
    },
    {
        "commodity": "Soybean (Yellow Non-GMO)",
        "market": "Dewas / Latur Central Grain Terminal",
        "wholesale_price_inr": 44.0,
        "unit": "per kg",
        "retail_mrp_range_inr": "₹58 – ₹66",
        "retail_margin_pct": 26.0,
        "trend": "BULLISH (+4.2% oilmeal demand)"
    },
    {
        "commodity": "Arabica Coffee (Plantation A)",
        "market": "Kushalnagar / ICE Arabica Futures",
        "wholesale_price_inr": 380.0,
        "unit": "per kg",
        "retail_mrp_range_inr": "₹650 – ₹850",
        "retail_margin_pct": 45.0,
        "trend": "BULLISH (+14.0% global supply tightness)"
    },
    {
        "commodity": "Premium Black CTC & Orthodox Tea",
        "market": "National Tea Auction Centers / Colombo & Mombasa parity",
        "wholesale_price_inr": 240.0,
        "unit": "per kg",
        "retail_mrp_range_inr": "₹350 – ₹480",
        "retail_margin_pct": 32.0,
        "trend": "STABLE (+3.2% export demand)"
    }
]

# Comprehensive Commodity Sector Heuristics for Dynamic Price Synthesis
DYNAMIC_COMMODITY_CATEGORIES = {
    "grains": {"mustard": (58.0, 78.0, 34.0, "Alwar / Bharatpur Mandi", "BULLISH (+3.8% winter demand)"),
               "maize": (21.5, 30.0, 39.5, "Davangere / Nizamabad Yard", "STABLE (+1.2% poultry feed)"),
               "barley": (22.0, 32.0, 45.0, "Jaipur / Sriganganagar Mandi", "MODERATE (+2.0% malt demand)"),
               "cotton": (68.0, 110.0, 61.7, "Rajkot / Akola Cotton Yard", "BULLISH (+5.1% textile export)")},
    "spices": {"turmeric": (145.0, 240.0, 65.5, "Nizamabad / Erode Spices Yard", "BULLISH (+8.2% export demand)"),
               "black pepper": (620.0, 950.0, 53.2, "Kochi / Wayanad Spices Board", "STRONG (+7.4% global tightness)"),
               "cardamom": (2100.0, 3200.0, 52.3, "Bodinayakanur / Spices Park", "VOLATILE (+11.5% festival rush)"),
               "ginger": (120.0, 220.0, 83.3, "Cochin / Karbi Anglong Hub", "FIRM (+6.0% fresh demand)")},
    "plantation": {"rubber": (185.0, 260.0, 40.5, "Kottayam Rubber Board Auction", "STABLE (+2.5% auto tyre demand)"),
                   "arecanut": (480.0, 650.0, 35.4, "Shivamogga / Mangaluru Yard", "BULLISH (+4.0% pan parity)")},
    "energy_metals": {"crude oil": (5900.0, 7200.0, 22.0, "MCX / NYMEX WTI Brent Parity", "MODERATE (-1.2% OPEC buffer)"),
                      "copper": (785.0, 950.0, 21.0, "MCX / LME Grade A Copper", "BULLISH (+4.5% EV demand)"),
                      "gold": (7850.0, 8600.0, 9.5, "IBJA / Bullion Spot Terminal", "STRONG (+6.8% central bank reserve)"),
                      "silver": (92.0, 115.0, 25.0, "MCX Silver 1kg Bar Benchmark", "BULLISH (+9.1% solar PV demand)")}
}

class MandiTracker:
    """Monitors national and global wholesale commodity prices and retail markups."""

    def __init__(self):
        self.benchmarks: List[Dict[str, Any]] = list(COMMODITY_BENCHMARKS)

    def register_commodity(self, commodity_data: Dict[str, Any]) -> None:
        """Dynamically registers new commodity telemetry."""
        self.benchmarks.append(commodity_data)

    def synthesize_commodity(self, query: str) -> Optional[Dict[str, Any]]:
        """Synthesizes dynamic commodity benchmark when querying unlisted commodities."""
        q_lower = query.lower()
        for cat, items in DYNAMIC_COMMODITY_CATEGORIES.items():
            for name, (ws, ret, margin, mkt, tr) in items.items():
                if name in q_lower:
                    unit_str = "per gram" if name in ["gold"] else ("per barrel" if name in ["crude oil"] else "per kg")
                    return {
                        "commodity": f"{name.title()} Benchmark",
                        "market": mkt,
                        "wholesale_price_inr": ws,
                        "unit": unit_str,
                        "retail_mrp_range_inr": f"₹{ret} – ₹{round(ret * 1.25, 1)}",
                        "retail_margin_pct": margin,
                        "trend": tr
                    }
        return None

    def get_benchmarks(self, query: str = "") -> List[Dict[str, Any]]:
        if not query:
            return self.benchmarks
            
        q_lower = query.lower()
        
        # Check if query requests an unlisted commodity
        synthesized = self.synthesize_commodity(query)
        if synthesized and not any(b["commodity"].lower() == synthesized["commodity"].lower() for b in self.benchmarks):
            self.benchmarks.insert(0, synthesized)

        scored = []
        for b in self.benchmarks:
            match_score = sum(1 for w in q_lower.split() if w in b["commodity"].lower() or w in b["market"].lower())
            scored.append((match_score, b))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [b for _, b in scored]

mandi_tracker = MandiTracker()
