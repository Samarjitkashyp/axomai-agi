"""
Z2 Bravo Web Content Scraper & Extractor.
Fetches, cleans, and structures main article body text from web pages
with concurrent execution and timeout resilience.
"""

from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import httpx
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

class WebScraperEngine:
    def __init__(self, timeout: float = 3.0, max_workers: int = 6):
        self.timeout = timeout
        self.max_workers = max_workers
        self.headers = {"User-Agent": USER_AGENT}

    def scrape_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Fetches a single URL and extracts clean readable text.
        """
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True, headers=self.headers) as client:
                resp = client.get(url)
                if resp.status_code != 200:
                    return None

                soup = BeautifulSoup(resp.text, "html.parser")

                # Remove non-content elements
                for tag in soup(["script", "style", "nav", "footer", "header", "aside", "svg", "iframe", "form", "button"]):
                    tag.decompose()

                # Extract title
                title = soup.title.string.strip() if soup.title and soup.title.string else ""
                
                # Extract meta description if available
                meta_desc = ""
                desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
                if desc_tag and desc_tag.get("content"):
                    meta_desc = desc_tag["content"].strip()

                # Clean text
                body_text = " ".join(soup.stripped_strings)

                # Trim excessive whitespace
                clean_body = " ".join(body_text.split())

                if len(clean_body) < 100:
                    return None

                parsed = urlparse(url)
                domain = parsed.netloc.replace("www.", "")

                return {
                    "url": url,
                    "domain": domain,
                    "title": title or domain,
                    "description": meta_desc,
                    "text": clean_body[:3500]  # First 3500 chars of substantive content
                }
        except Exception:
            return None

    def scrape_batch(self, urls: List[str], max_pages: int = 5) -> List[Dict[str, Any]]:
        """
        Scrapes multiple URLs in parallel using thread pool.
        """
        targets = urls[:max_pages]
        results = []

        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(targets) or 1)) as executor:
            scraped = list(executor.map(self.scrape_url, targets))

        for item in scraped:
            if item and item.get("text"):
                results.append(item)

        return results


web_scraper_engine = WebScraperEngine()

