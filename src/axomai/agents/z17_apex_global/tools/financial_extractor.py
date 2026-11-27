"""
Z17 Apex-Global - Financial Extractor & Natural Language Parameter Parser.
Extracts target company names, public tickers, revenue, EBITDA, growth rates,
WACC, net debt, and acquisition multiples from natural language user queries.
Supports both prefix and suffix syntax (e.g. '$250M revenue' and 'revenue of $250M').
"""

import re
from typing import Dict, Any, Optional

class FinancialExtractor:
    """Extracts financial modeling parameters and market tickers from unstructured user prompts."""

    KNOWN_TICKERS = {
        "apple": "AAPL", "aapl": "AAPL",
        "microsoft": "MSFT", "msft": "MSFT",
        "google": "GOOGL", "alphabet": "GOOGL", "googl": "GOOGL",
        "amazon": "AMZN", "amzn": "AMZN",
        "nvidia": "NVDA", "nvda": "NVDA",
        "tesla": "TSLA", "tsla": "TSLA",
        "meta": "META",
        "tcs": "TCS.NS", "tata consultancy": "TCS.NS",
        "reliance": "RELIANCE.NS", "ril": "RELIANCE.NS",
        "infosys": "INFY.NS", "infy": "INFY.NS",
        "zomato": "ZOMATO.NS",
        "tata motors": "TATAMOTORS.NS",
        "hdfc": "HDFCBANK.NS", "hdfc bank": "HDFCBANK.NS",
        "icici": "ICICIBANK.NS",
        "wipro": "WIPRO.NS"
    }

    def parse_financial_query(self, query: str) -> Dict[str, Any]:
        """
        Parses user query into structured financial inputs with sensible,
        defensible Wall Street default baselines.
        """
        q_lower = query.lower()

        # 1. Identify Ticker or Target Entity
        detected_ticker = None
        target_name = "Target Corporation"

        for name, ticker in self.KNOWN_TICKERS.items():
            if re.search(r'\b' + re.escape(name) + r'\b', q_lower):
                detected_ticker = ticker
                target_name = name.title()
                break

        # 1. Identify Explicit Tickers (e.g. SBIN.NS, ITC.NS, AAPL, NVDA)
        ns_match = re.search(r'\b([A-Za-z0-9_\-]{2,15}\.(?:NS|BO))\b', query, re.IGNORECASE)
        if ns_match:
            detected_ticker = ns_match.group(1).upper()
            target_name = detected_ticker
        else:
            ticker_match = re.search(r'\b([A-Z]{2,6})\b', query)
            if ticker_match:
                cand = ticker_match.group(1).upper()
                if cand not in ["FOR", "AND", "WITH", "THE", "PE", "DCF", "WACC", "CAGR", "EBITDA", "FCF", "ROIC", "LBO", "INR", "USD", "EUR", "GBP", "SEBI", "NCLT", "GST", "MCA", "ROC", "RPT", "IBC", "AIF", "DIN"]:
                    detected_ticker = cand
                    target_name = detected_ticker

        acq_match = re.search(r'(?:acquisition of|buyout of|valuation of|analyze|audit|evaluate|tell me about|target[:\s]+)\s+([A-Za-z0-9\s&]+?)(?:\s+with|\s+having|\s+at|\s+for|\.|\,|$)', query, re.IGNORECASE)
        if acq_match and not detected_ticker:
            candidate = acq_match.group(1).strip()
            if len(candidate) > 2 and candidate.lower() not in ["the", "a", "an", "this", "target"]:
                target_name = candidate

        # 2. Extract Numerical Metrics (Supports prefix & suffix syntax)
        revenue_m = self._extract_amount(query, [r'revenue', r'sales', r'turnover'], default=120.0)
        ebitda_m = self._extract_amount(query, [r'ebitda', r'operating profit'], default=None)
        
        if ebitda_m is None:
            ebitda_m = round(revenue_m * 0.22, 2)
            ebitda_margin_pct = 22.0
        else:
            ebitda_margin_pct = round((ebitda_m / max(revenue_m, 1.0)) * 100.0, 1)

        fcf_m = self._extract_amount(query, [r'fcf', r'free cash flow'], default=None)
        if fcf_m is None:
            fcf_m = round(ebitda_m * 0.68, 2)

        growth_pct = self._extract_percentage(query, [r'growth', r'cagr', r'revenue growth'], default=14.0)
        wacc_pct = self._extract_percentage(query, [r'wacc', r'discount rate', r'cost of capital'], default=9.5)
        net_debt_m = self._extract_amount(query, [r'net debt', r'debt', r'leverage'], default=round(ebitda_m * 1.5, 2))
        
        entry_multiple = self._extract_multiple(query, [r'multiple', r'ev/ebitda', r'ev multiple', r'valuation multiple'], default=11.5)
        entry_ev_m = round(ebitda_m * entry_multiple, 2)

        is_accretion_dilution = any(k in q_lower for k in ["accretion", "dilution", "eps impact", "merger model", "all-cash", "all-stock", "share swap"])
        is_lbo_focus = any(k in q_lower for k in ["lbo", "leveraged buyout", "irr", "moic", "debt waterfall", "sponsor", "private equity"])
        is_transcript_audit = any(k in q_lower for k in ["earnings call", "transcript", "deception", "management tone", "q&a", "ceo commentary"])

        return {
            "target_name": target_name,
            "detected_ticker": detected_ticker,
            "revenue_m": revenue_m,
            "ebitda_m": ebitda_m,
            "ebitda_margin_pct": ebitda_margin_pct,
            "fcf_m": fcf_m,
            "growth_pct": growth_pct,
            "wacc_pct": wacc_pct,
            "net_debt_m": net_debt_m,
            "entry_multiple": entry_multiple,
            "entry_ev_m": entry_ev_m,
            "is_accretion_dilution": is_accretion_dilution,
            "is_lbo_focus": is_lbo_focus,
            "is_transcript_audit": is_transcript_audit,
            "raw_query": query
        }

    def _extract_amount(self, text: str, patterns: list, default: Optional[float] = None) -> Optional[float]:
        """Extracts dollar/rupee amounts in millions or raw figures matching both prefix & suffix syntax."""
        for pat in patterns:
            # 1. Prefix: "revenue of $250M" or "revenue: 250 million"
            prefix_match = re.search(r'(?:' + pat + r')\s*(?:of|is|at|[:=])?\s*[\$₹]?\s*([0-9]+(?:\.[0-9]+)?)\s*(m|b|cr|crore|million|billion)?\b', text, re.IGNORECASE)
            if prefix_match:
                val = float(prefix_match.group(1))
                unit = (prefix_match.group(2) or '').lower()
                return self._scale_val(val, unit)

            # 2. Suffix: "$250M revenue" or "250 million sales"
            suffix_match = re.search(r'[\$₹]?\s*([0-9]+(?:\.[0-9]+)?)\s*(m|b|cr|crore|million|billion)?\s*(?:of)?\s*(?:' + pat + r')\b', text, re.IGNORECASE)
            if suffix_match:
                val = float(suffix_match.group(1))
                unit = (suffix_match.group(2) or '').lower()
                return self._scale_val(val, unit)

        return default

    def _scale_val(self, val: float, unit: str) -> float:
        if unit in ['b', 'billion']:
            return val * 1000.0
        elif unit in ['cr', 'crore']:
            return round(val * 0.12, 2)
        return val

    def _extract_percentage(self, text: str, patterns: list, default: float) -> float:
        """Extracts percentages e.g. 15%, 12.5% supporting prefix & suffix."""
        for pat in patterns:
            # 1. Suffix: "16% growth"
            suffix_match = re.search(r'([0-9]+(?:\.[0-9]+)?)\s*%\s*(?:annual)?\s*(?:' + pat + r')\b', text, re.IGNORECASE)
            if suffix_match:
                return float(suffix_match.group(1))
            # 2. Prefix: "growth of 16%" or "growth: 16%"
            prefix_match = re.search(r'(?:' + pat + r')\s*(?:of|is|at|[:=])?\s*([0-9]+(?:\.[0-9]+)?)\s*%', text, re.IGNORECASE)
            if prefix_match:
                return float(prefix_match.group(1))
        return default

    def _extract_multiple(self, text: str, patterns: list, default: float) -> float:
        """Extracts valuation multiples e.g. 11x multiple, 12x, 10.5x."""
        for pat in patterns:
            match = re.search(r'(?:' + pat + r')\s*(?:of|is|at|[:=])?\s*([0-9]+(?:\.[0-9]+)?)\s*x?', text, re.IGNORECASE)
            if match:
                return float(match.group(1))
        direct_x = re.search(r'\b([0-9]+(?:\.[0-9]+)?)\s*x\b', text, re.IGNORECASE)
        if direct_x:
            return float(direct_x.group(1))
        return default

financial_extractor = FinancialExtractor()
