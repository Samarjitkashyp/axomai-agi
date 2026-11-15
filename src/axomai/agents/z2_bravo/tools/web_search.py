"""
Z2 Bravo Web Search Engine.
High-speed, multi-provider web search engine with deduplication,
domain extraction, and strategic query expansion.
"""

import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from ddgs import DDGS
from rich.console import Console

console = Console()

def clean_conversational_query(q: str) -> str:
    """Strips conversational noise and extracts concise high-intent search keywords."""
    if ":" in q:
        parts = q.split(":")
        q = parts[0] if len(parts[0].split()) >= 3 else parts[1]

    cleaned = re.sub(
        r'^(can you tell me|can you please tell me|tell me|please tell me|what is|what are|batao|kya hai|kuch batao|perform deep market research on|analyze|assess|conduct|model|audit)\s*',
        '',
        q.strip(),
        flags=re.IGNORECASE
    )
    cleaned = re.sub(r'[,;:\"\'\(\)\[\]{}]+', ' ', cleaned).strip()

    words = cleaned.split()
    if len(words) > 5:
        stop_words = {
            "the", "a", "an", "and", "or", "for", "with", "in", "on", "at", "to", "from", "of",
            "pehle", "ka", "ke", "me", "nayi", "banao", "perform", "deep", "top", "conduct",
            "model", "assess", "district", "districts", "presence", "pricing", "spending", "density"
        }
        meaningful = [w for w in words if w.lower() not in stop_words]
        cleaned = " ".join(meaningful[:5]) if meaningful else " ".join(words[:5])

    return cleaned or q

class WebSearchEngine:
    def __init__(self, default_max_results: int = 6):
        self.default_max_results = default_max_results

    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Executes search on live web index and returns cleaned result cards.
        Intelligently routes time-sensitive queries to live news indexes.
        """
        limit = max_results or self.default_max_results
        cleaned_query = clean_conversational_query(query)
        results: List[Dict[str, str]] = []
        seen_urls = set()

        is_time_sensitive = any(w in cleaned_query.lower() for w in [
            "today", "aaj", "current", "latest", "now", "live", "news",
            "breaking", "up and down", "market today", "share market", "stock market",
            "sensex", "nifty", "yesterday", "this week"
        ])

        try:
            with DDGS() as ddgs:
                # 1. If time-sensitive, fetch fresh breaking news first
                if is_time_sensitive:
                    try:
                        # Clean query for news index
                        news_q = cleaned_query
                        if "up and down" in news_q.lower():
                            news_q = re.sub(r'up and down', 'indices', news_q, flags=re.IGNORECASE).strip()
                        if "market" in news_q.lower() and not any(w in news_q.lower() for w in ["stock", "share"]):
                            news_q = news_q.replace("market", "stock market")

                        raw_news = list(ddgs.news(news_q, max_results=min(limit, 4)))
                        for item in raw_news:
                            url = item.get("url", "").strip()
                            if not url or url in seen_urls:
                                continue
                            seen_urls.add(url)
                            parsed = urlparse(url)
                            domain = item.get("source") or parsed.netloc.replace("www.", "").strip()
                            date_str = item.get("date", "")[:10]
                            body = item.get("body", "").strip()
                            snippet = f"[{date_str}] {body}" if date_str else body

                            results.append({
                                "title": item.get("title", "").strip(),
                                "url": url,
                                "snippet": snippet,
                                "domain": domain
                            })
                    except Exception as ne:
                        console.print(f"[dim yellow][Z2 News Index Skip][/dim yellow] {ne}")

                # 2. General web text search
                text_items = []
                if is_time_sensitive:
                    try:
                        text_items = list(ddgs.text(cleaned_query, timelimit='w', max_results=limit))
                    except Exception:
                        text_items = []

                if not text_items:
                    text_items = list(ddgs.text(cleaned_query, max_results=limit))

                for item in text_items:
                    url = item.get("href", "").strip()
                    if not url or url in seen_urls:
                        continue
                    seen_urls.add(url)

                    parsed = urlparse(url)
                    domain = parsed.netloc.replace("www.", "").strip()

                    results.append({
                        "title": item.get("title", "").strip(),
                        "url": url,
                        "snippet": item.get("body", "").strip(),
                        "domain": domain
                    })
        except Exception as e:
            console.print(f"[dim red][Z2 Search Error][/dim red] {e}")

        return results

    def multi_query_search(self, queries: List[str], max_per_query: int = 3) -> List[Dict[str, str]]:
        """
        Executes multiple targeted queries across different sub-angles,
        deduplicating by domain/URL for broad coverage.
        """
        aggregated: List[Dict[str, str]] = []
        seen_domains = set()
        seen_urls = set()

        for q in queries:
            sub_results = self.search(q, max_results=max_per_query)
            for item in sub_results:
                url = item["url"]
                domain = item["domain"]

                # Prioritize diversity of domains
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                seen_domains.add(domain)
                aggregated.append(item)

        return aggregated


web_search_engine = WebSearchEngine()

