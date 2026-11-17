"""
Z2 Bravo Web Search Engine - Multi-Provider Live Intelligence.
Aggregates live results from Google Search / Google News, Bing News / Web,
and DuckDuckGo with domain deduplication and real-time freshness ranking.
"""

import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
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
    if len(words) > 6:
        stop_words = {
            "the", "a", "an", "and", "or", "for", "with", "in", "on", "at", "to", "from", "of",
            "pehle", "ka", "ke", "me", "nayi", "banao", "perform", "deep", "top", "conduct",
            "model", "assess", "presence", "spending", "density"
        }
        meaningful = [w for w in words if w.lower() not in stop_words]
        cleaned = " ".join(meaningful[:6]) if meaningful else " ".join(words[:6])

    return cleaned or q

class WebSearchEngine:
    """Multi-provider live web search engine supporting Google, Bing, and DuckDuckGo."""

    def __init__(self, default_max_results: int = 6):
        self.default_max_results = default_max_results
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 AxomAI/4.0"

    def search_google_news(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        """Queries Google News RSS index for up-to-the-minute real-world reporting."""
        results = []
        try:
            encoded_q = urllib.parse.quote(query)
            url = f"https://news.google.com/rss/search?q={encoded_q}&hl=en-IN&gl=IN&ceid=IN:en"
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=5) as resp:
                tree = ET.fromstring(resp.read())
                for item in tree.findall(".//item")[:limit]:
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    pub_elem = item.find("pubDate")
                    source_elem = item.find("source")
                    desc_elem = item.find("description")

                    title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                    link = link_elem.text.strip() if link_elem is not None and link_elem.text else ""
                    pub_date = pub_elem.text.strip() if pub_elem is not None and pub_elem.text else ""
                    source = source_elem.text.strip() if source_elem is not None and source_elem.text else "Google News"
                    raw_desc = desc_elem.text if desc_elem is not None and desc_elem.text else ""
                    clean_desc = re.sub(r'<[^>]+>', ' ', raw_desc).strip()

                    if title:
                        parsed = urlparse(link)
                        domain = parsed.netloc.replace("www.", "").strip() or source
                        results.append({
                            "title": title,
                            "url": link,
                            "snippet": f"[{pub_date[:16]}] {clean_desc[:300]}" if pub_date else clean_desc[:300],
                            "domain": domain,
                            "provider": "google_news"
                        })
        except Exception:
            pass
        return results

    def search_bing_news(self, query: str, limit: int = 4) -> List[Dict[str, str]]:
        """Queries Bing News RSS index for cross-engine corroboration."""
        results = []
        try:
            encoded_q = urllib.parse.quote(query)
            url = f"https://www.bing.com/news/search?q={encoded_q}&format=rss"
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=5) as resp:
                tree = ET.fromstring(resp.read())
                for item in tree.findall(".//item")[:limit]:
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    desc_elem = item.find("description")
                    pub_elem = item.find("pubDate")

                    title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                    link = link_elem.text.strip() if link_elem is not None and link_elem.text else ""
                    raw_desc = desc_elem.text if desc_elem is not None and desc_elem.text else ""
                    clean_desc = re.sub(r'<[^>]+>', ' ', raw_desc).strip()
                    pub_date = pub_elem.text.strip() if pub_elem is not None and pub_elem.text else ""

                    if title:
                        parsed = urlparse(link)
                        domain = parsed.netloc.replace("www.", "").strip() or "Bing News"
                        results.append({
                            "title": title,
                            "url": link,
                            "snippet": f"[{pub_date[:16]}] {clean_desc[:300]}" if pub_date else clean_desc[:300],
                            "domain": domain,
                            "provider": "bing_news"
                        })
        except Exception:
            pass
        return results

    def search_ddg(self, query: str, limit: int = 4) -> List[Dict[str, str]]:
        """Queries DuckDuckGo text index as supplementary provider."""
        results = []
        try:
            from ddgs import DDGS
            with DDGS() as ddgs:
                text_items = list(ddgs.text(query, max_results=limit))
                for item in text_items:
                    url = item.get("href", "").strip()
                    title = item.get("title", "").strip()
                    body = item.get("body", "").strip()
                    if url and title:
                        parsed = urlparse(url)
                        domain = parsed.netloc.replace("www.", "").strip()
                        results.append({
                            "title": title,
                            "url": url,
                            "snippet": body[:300],
                            "domain": domain,
                            "provider": "duckduckgo"
                        })
        except Exception:
            pass
        return results

    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Executes unified multi-provider search across Google, Bing, and DuckDuckGo.
        Deduplicates by URL and aggregates diverse source perspectives.
        """
        limit = max_results or self.default_max_results
        cleaned_query = clean_conversational_query(query)
        aggregated: List[Dict[str, str]] = []
        seen_urls = set()

        # 1. Fetch live Google intelligence
        g_results = self.search_google_news(cleaned_query, limit=max(3, limit // 2))
        for res in g_results:
            if res["url"] not in seen_urls:
                seen_urls.add(res["url"])
                aggregated.append(res)

        # 2. Fetch live Bing intelligence
        b_results = self.search_bing_news(cleaned_query, limit=max(2, limit // 2))
        for res in b_results:
            if res["url"] not in seen_urls:
                seen_urls.add(res["url"])
                aggregated.append(res)

        # 3. Supplementary DuckDuckGo search if needed
        if len(aggregated) < limit:
            ddg_results = self.search_ddg(cleaned_query, limit=limit - len(aggregated))
            for res in ddg_results:
                if res["url"] not in seen_urls:
                    seen_urls.add(res["url"])
                    aggregated.append(res)

        # Fallback if specific cleaned query returned zero results
        if not aggregated and cleaned_query != query:
            fallback_g = self.search_google_news(query[:50], limit=limit)
            for res in fallback_g:
                if res["url"] not in seen_urls:
                    seen_urls.add(res["url"])
                    aggregated.append(res)

        return aggregated[:limit]

    def multi_query_search(self, queries: List[str], max_per_query: int = 3) -> List[Dict[str, str]]:
        """Executes multiple targeted queries across different sub-angles."""
        aggregated: List[Dict[str, str]] = []
        seen_urls = set()

        for q in queries:
            sub_results = self.search(q, max_results=max_per_query)
            for item in sub_results:
                if item["url"] not in seen_urls:
                    seen_urls.add(item["url"])
                    aggregated.append(item)

        return aggregated

web_search_engine = WebSearchEngine()
