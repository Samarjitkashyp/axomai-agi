"""
Z17 Apex-Global - Universal Financial & Indian Forensic Parameter Extractor.
Extracts target company names, public tickers, Revenue, EBITDA, Growth, WACC, Debt,
plus Indian statutory parameters: Promoter Holding %, Pledge %, Bank Charges (INR Cr),
GSTR-1/3B/2B & ITC figures, Section 188 RPT amounts, SEBI SAST Stake % & Offer Price,
and Rule 11UA Issue Price vs DCF Fair Value.
"""

import re
from typing import Dict, Any, Optional, List


class FinancialExtractor:
    """Extracts financial modeling & Indian forensic parameters from unstructured user prompts."""

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
        "tata motors": "TMCV.NS",
        "tata steel": "TATASTEEL.NS",
        "hdfc": "HDFCBANK.NS", "hdfc bank": "HDFCBANK.NS",
        "icici": "ICICIBANK.NS",
        "sbi": "SBIN.NS", "state bank of india": "SBIN.NS",
        "itc": "ITC.NS",
        "maruti": "MARUTI.NS", "maruti suzuki": "MARUTI.NS",
        "wipro": "WIPRO.NS"
    }

    def parse_financial_query(self, query: str) -> Dict[str, Any]:
        q_lower = query.lower()

        # 1. Identify Ticker or Target Entity
        detected_ticker = None
        target_name = "Target Corporation"

        for name, ticker in self.KNOWN_TICKERS.items():
            if name == "itc" and any(k in q_lower for k in ["eligible itc", "claimed itc", "input tax credit", "gstr-2b", "gstr-3b"]):
                continue
            if re.search(r'\b' + re.escape(name) + r'\b', q_lower):
                detected_ticker = ticker
                target_name = name.title()
                break

        ns_match = re.search(r'\b([A-Za-z0-9_\-]{2,15}\.(?:NS|BO))\b', query, re.IGNORECASE)
        if ns_match:
            detected_ticker = ns_match.group(1).upper()
            target_name = detected_ticker
        elif not detected_ticker:
            ticker_match = re.search(r'\b([A-Z]{2,6})\b', query)
            if ticker_match:
                cand = ticker_match.group(1).upper()
                excluded = {
                    "FOR", "AND", "WITH", "THE", "PE", "DCF", "WACC", "CAGR", "EBITDA", "FCF",
                    "ROIC", "LBO", "INR", "USD", "EUR", "GBP", "SEBI", "NCLT", "GST", "GSTN",
                    "MCA", "ROC", "RPT", "IBC", "AIF", "DIN", "CHG", "NBFC", "SAST", "NAV",
                    "PAT", "CIRP", "GSTR", "ITC", "ICD", "LTD", "PVT", "RULE", "ACT", "TAX"
                }
                if cand not in excluded:
                    detected_ticker = cand
                    target_name = detected_ticker

        quoted_name = re.search(r"['\"]([A-Za-z0-9\s&\.\-]+?)['\"]", query)
        if quoted_name and not detected_ticker:
            target_name = quoted_name.group(1).strip()
        elif not detected_ticker:
            acq_match = re.search(
                r'(?:acquisition of|buyout of|valuation of|analyze|audit|evaluate|for|target[:\s]+)\s+([A-Za-z0-9\s&\.]+?)(?:\s+with|\s+having|\s+at|\s+for|\.|\,|$)',
                query, re.IGNORECASE
            )
            if acq_match:
                candidate = acq_match.group(1).strip()
                if len(candidate) > 2 and candidate.lower() not in ["the", "a", "an", "this", "target"]:
                    target_name = candidate

        # 2. Extract Core Financial Metrics (in USD Millions, converting INR Cr at 1 Cr = $0.12M)
        revenue_m, revenue_cr_explicit = self._extract_amount_with_cr(query, [r'revenue', r'sales', r'turnover'], default_m=120.0)
        ebitda_m, ebitda_cr_explicit = self._extract_amount_with_cr(query, [r'stated ebitda', r'ebitda', r'operating profit'], default_m=None)

        if ebitda_m is None:
            ebitda_m = round(revenue_m * 0.22, 2)
            ebitda_margin_pct = 22.0
        else:
            ebitda_margin_pct = round((ebitda_m / max(revenue_m, 1.0)) * 100.0, 1)

        fcf_m, _ = self._extract_amount_with_cr(query, [r'fcf', r'free cash flow'], default_m=None)
        if fcf_m is None:
            fcf_m = round(ebitda_m * 0.68, 2)

        growth_pct = self._extract_percentage(query, [r'growth', r'cagr', r'revenue growth'], default=14.0)
        wacc_pct = self._extract_percentage(query, [r'wacc', r'discount rate', r'cost of capital'], default=9.5)
        net_debt_m, debt_cr_explicit = self._extract_amount_with_cr(query, [r'net debt', r'debt', r'leverage'], default_m=round(ebitda_m * 1.5, 2))
        cash_m, cash_cr_explicit = self._extract_amount_with_cr(query, [r'cash'], default_m=round(ebitda_m * 0.25, 2))

        entry_multiple = self._extract_multiple(query, [r'multiple', r'ev/ebitda', r'ev multiple', r'valuation multiple'], default=11.5)
        entry_ev_m = round(ebitda_m * entry_multiple, 2)

        # 3. Extract Indian Sovereign & Forensic Parameters (None / 0.0 if not provided -> NO fake alarms)
        bank_charges_cr = self._extract_inr_cr(query, [r'bank charges?', r'charges?', r'liens?', r'chg-1'])
        gstr1_cr = self._extract_inr_cr(query, [r'gstr-1(?:\s+turnover)?(?:\s+reported)?'])
        gstr3b_tax_cr = self._extract_inr_cr(query, [r'gstr-3b\s+tax(?:\s+paid)?'])
        gstr2b_itc_cr = self._extract_inr_cr(query, [r'gstr-2b\s+(?:eligible\s+)?itc'])
        gstr3b_claimed_itc_cr = self._extract_inr_cr(query, [r'gstr-3b\s+(?:claimed\s+)?itc(?:\s+is)?', r'claimed\s+itc'])

        promoter_holding_pct = self._extract_percentage_optional(query, [r'promoter\s+holding', r'total\s+promoter\s+holding'])
        pledged_pct = self._extract_percentage_optional(query, [r'pledged(?:\s+to\s+nbfcs)?', r'of\s+promoter\s+shares\s+pledged', r'promoter\s+pledge'])
        # Also handle "62% of promoter shares pledged"
        if pledged_pct is None:
            pm = re.search(r'(\d+(?:\.\d+)?)\s*%\s*(?:of\s+promoter\s+shares\s+)?pledged', q_lower)
            if pm:
                pledged_pct = float(pm.group(1))

        stock_price_inr = self._extract_inr_per_share(query, [r'current\s+stock\s+price', r'share\s+price', r'market\s+price', r'cmp'])
        acq_stake_pct = self._extract_percentage_optional(query, [r'acquire\s+(?:a\s+)?', r'controlling\s+stake', r'stake\s+of'])
        if acq_stake_pct is None:
            sm = re.search(r'acquire\s+(?:a\s+)?(\d+(?:\.\d+)?)\s*%', q_lower)
            if sm:
                acq_stake_pct = float(sm.group(1))
        offer_price_inr = self._extract_inr_per_share(query, [r'stake\s+at', r'offer\s+price', r'acquire.*?at'])

        # RPT Siphoning items
        rpt_consulting_cr = self._extract_inr_cr(query, [r'consulting\s+fees?', r'spouse\s+firm'])
        rpt_icd_cr = self._extract_inr_cr(query, [r'inter-corporate\s+deposit', r'icd'])
        rpt_total_cr = (rpt_consulting_cr or 0.0) + (rpt_icd_cr or 0.0)

        # Rule 11UA Angel Tax
        issue_price_inr = self._extract_inr_per_share(query, [r'issu(?:ing|ed)\s+(?:fresh\s+)?shares.*?at', r'issue\s+price'])
        dcf_fair_value_inr = self._extract_inr_per_share(query, [r'dcf\s+fair\s+value(?:\s+is)?', r'fair\s+value(?:\s+is)?'])

        # NCLT / AIF flags
        mentions_nclt = any(k in q_lower for k in ["nclt", "ibc", "cirp", "insolvency", "bankrupt", "distressed", "29a", "haircut"])
        mentions_aif = any(k in q_lower for k in ["aif", "waterfall", "carried interest", "hurdle", "lp ", "gp "])
        aif_fund_cr = self._extract_inr_cr(query, [r'fund\s+size', r'committed\s+capital', r'aif\s+of'])

        is_accretion_dilution = any(k in q_lower for k in ["accretion", "dilution", "eps impact", "merger model", "all-cash", "all-stock", "share swap"])
        is_lbo_focus = any(k in q_lower for k in ["lbo", "leveraged buyout", "irr", "moic", "debt waterfall", "sponsor", "private equity"])
        is_transcript_audit = any(k in q_lower for k in ["earnings call", "transcript", "deception", "management tone", "q&a", "ceo commentary"])

        return {
            "target_name": target_name,
            "detected_ticker": detected_ticker,
            "revenue_m": revenue_m,
            "revenue_cr_explicit": revenue_cr_explicit,
            "ebitda_m": ebitda_m,
            "ebitda_cr_explicit": ebitda_cr_explicit,
            "ebitda_margin_pct": ebitda_margin_pct,
            "fcf_m": fcf_m,
            "growth_pct": growth_pct,
            "wacc_pct": wacc_pct,
            "net_debt_m": net_debt_m,
            "debt_cr_explicit": debt_cr_explicit,
            "cash_m": cash_m,
            "cash_cr_explicit": cash_cr_explicit,
            "entry_multiple": entry_multiple,
            "entry_ev_m": entry_ev_m,
            # Indian Sovereign Extracted Parameters
            "bank_charges_cr": bank_charges_cr,
            "gstr1_cr": gstr1_cr,
            "gstr3b_tax_cr": gstr3b_tax_cr,
            "gstr2b_itc_cr": gstr2b_itc_cr,
            "gstr3b_claimed_itc_cr": gstr3b_claimed_itc_cr,
            "promoter_holding_pct": promoter_holding_pct,
            "pledged_pct": pledged_pct,
            "stock_price_inr": stock_price_inr,
            "acq_stake_pct": acq_stake_pct,
            "offer_price_inr": offer_price_inr,
            "rpt_consulting_cr": rpt_consulting_cr or 0.0,
            "rpt_icd_cr": rpt_icd_cr or 0.0,
            "rpt_total_cr": rpt_total_cr,
            "issue_price_inr": issue_price_inr,
            "dcf_fair_value_inr": dcf_fair_value_inr,
            "mentions_nclt": mentions_nclt,
            "mentions_aif": mentions_aif,
            "aif_fund_cr": aif_fund_cr,
            "is_accretion_dilution": is_accretion_dilution,
            "is_lbo_focus": is_lbo_focus,
            "is_transcript_audit": is_transcript_audit,
            "raw_query": query
        }

    def _extract_amount_with_cr(self, text: str, keywords: List[str], default_m: Optional[float]) -> tuple:
        kw_pattern = "|".join(keywords)
        # Check INR Cr first (e.g. "Revenue INR 1,200 Cr" or "1,200 Cr revenue")
        m_cr = re.search(rf'(?:{kw_pattern})[:\s]*(?:is|of)?\s*(?:inr|rs\.?|₹)\s*(\d[\d,]*(?:\.\d+)?)\s*(?:cr|crore|crores)\b', text, re.IGNORECASE)
        if m_cr:
            cr_val = float(m_cr.group(1).replace(",", ""))
            return round(cr_val * 0.12, 2), cr_val

        # USD / generic M or B
        m = re.search(rf'(?:{kw_pattern})[:\s]*(?:is|of)?\s*\$?\s*(\d[\d,]*(?:\.\d+)?)\s*(m|million|b|billion|cr|crore)?\b', text, re.IGNORECASE)
        if m:
            val = float(m.group(1).replace(",", ""))
            unit = (m.group(2) or "").lower()
            if unit in ["cr", "crore"]:
                return round(val * 0.12, 2), val
            if unit in ["b", "billion"]:
                val *= 1000.0
            return val, None

        m2 = re.search(rf'\$\s*(\d[\d,]*(?:\.\d+)?)\s*(m|million|b|billion)?\s+(?:in\s+|of\s+)?(?:{kw_pattern})\b', text, re.IGNORECASE)
        if m2:
            val = float(m2.group(1).replace(",", ""))
            unit = (m2.group(2) or "").lower()
            if unit in ["b", "billion"]:
                val *= 1000.0
            return val, None

        return default_m, None

    def _extract_inr_cr(self, text: str, keywords: List[str]) -> Optional[float]:
        kw_pattern = "|".join(keywords)
        m1 = re.search(rf'(?:{kw_pattern})[^.\n]{{0,35}}?(?:inr|rs\.?|₹)\s*(\d[\d,]*(?:\.\d+)?)\s*(?:cr|crore|crores)?\b', text, re.IGNORECASE)
        if m1:
            return float(m1.group(1).replace(",", ""))
        m2 = re.search(rf'(?:inr|rs\.?|₹)\s*(\d[\d,]*(?:\.\d+)?)\s*(?:cr|crore|crores)?\s+(?:of\s+)?(?:{kw_pattern})\b', text, re.IGNORECASE)
        if m2:
            return float(m2.group(1).replace(",", ""))
        return None

    def _extract_inr_per_share(self, text: str, keywords: List[str]) -> Optional[float]:
        kw_pattern = "|".join(keywords)
        m = re.search(rf'(?:{kw_pattern})[:\s]*(?:is|of)?\s*(?:inr|rs\.?|₹)\s*(\d[\d,]*(?:\.\d+)?)', text, re.IGNORECASE)
        if m:
            return float(m.group(1).replace(",", ""))
        return None

    def _extract_percentage(self, text: str, keywords: List[str], default: float) -> float:
        val = self._extract_percentage_optional(text, keywords)
        return val if val is not None else default

    def _extract_percentage_optional(self, text: str, keywords: List[str]) -> Optional[float]:
        kw_pattern = "|".join(keywords)
        m = re.search(rf'(?:{kw_pattern})[:\s]*(?:is|of)?\s*(\d+(?:\.\d+)?)\s*%', text, re.IGNORECASE)
        if m:
            return float(m.group(1))
        m2 = re.search(rf'(\d+(?:\.\d+)?)\s*%\s+(?:{kw_pattern})', text, re.IGNORECASE)
        if m2:
            return float(m2.group(1))
        return None

    def _extract_multiple(self, text: str, keywords: List[str], default: float) -> float:
        kw_pattern = "|".join(keywords)
        m = re.search(rf'(?:{kw_pattern})[:\s]*(?:is|of)?\s*(\d+(?:\.\d+)?)\s*x?', text, re.IGNORECASE)
        if m:
            return float(m.group(1))
        return default


financial_extractor = FinancialExtractor()
