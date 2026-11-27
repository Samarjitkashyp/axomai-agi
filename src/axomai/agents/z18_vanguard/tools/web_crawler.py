"""
Z18 Vanguard - Universal Web Crawler & Live DOM Ingestion Tool.
Fetches live website HTML, HTTP response headers, robots.txt, and sitemap.xml
with timeout protection, redirect tracking, and browser user-agent emulation.
"""

import time
import re
from typing import Dict, Any, Optional
from urllib.parse import urlparse, urljoin
import httpx

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 (AxomAI-SearchAuditor/1.0)"
)

class WebCrawler:
    """High-speed asynchronous and synchronous DOM crawler for SEO/AEO/GEO inspection."""

    def __init__(self, timeout_sec: float = 12.0):
        self.timeout = timeout_sec

    def extract_url_from_query(self, query: str) -> Optional[str]:
        """Extracts the first HTTP/HTTPS or domain URL from natural language query."""
        match = re.search(r'https?://[^\s\'"<>]+', query)
        if match:
            return match.group(0).rstrip(".,;)")
        
        # Check domain pattern without protocol (e.g. 'example.com' or 'www.example.com')
        domain_match = re.search(r'\b(?:www\.)?[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+(?:/[^\s\'"<>]*)?', query)
        if domain_match:
            candidate = domain_match.group(0).rstrip(".,;)")
            if not candidate.startswith("http"):
                return f"https://{candidate}"
            return candidate
        return None

    def crawl_url(self, target_url: str) -> Dict[str, Any]:
        """
        Fetches the primary page, extracts HTTP response headers, latency,
        and verifies robots.txt and sitemap.xml presence.
        """
        # Ensure scheme
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = f"https://{target_url}"

        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

        parsed = urlparse(target_url)
        base_origin = f"{parsed.scheme}://{parsed.netloc}"

        start_time = time.time()
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True, verify=False) as client:
                resp = client.get(target_url, headers=headers)
                latency_ms = round((time.time() - start_time) * 1000, 1)

                html_content = resp.text
                status_code = resp.status_code
                response_headers = dict(resp.headers)
                final_url = str(resp.url)
                is_https = final_url.startswith("https://")

                # Check robots.txt
                robots_url = urljoin(base_origin, "/robots.txt")
                robots_txt_found = False
                try:
                    robots_resp = client.get(robots_url, headers=headers, timeout=5.0)
                    robots_txt_found = (robots_resp.status_code == 200 and "user-agent" in robots_resp.text.lower())
                except Exception:
                    pass

                # Check sitemap.xml
                sitemap_url = urljoin(base_origin, "/sitemap.xml")
                sitemap_found = False
                try:
                    sitemap_resp = client.get(sitemap_url, headers=headers, timeout=5.0)
                    sitemap_found = (sitemap_resp.status_code == 200 and ("<urlset" in sitemap_resp.text or "<sitemapindex" in sitemap_resp.text))
                except Exception:
                    pass

                return {
                    "success": True,
                    "target_url": target_url,
                    "final_url": final_url,
                    "status_code": status_code,
                    "latency_ms": latency_ms,
                    "is_https": is_https,
                    "content_length_bytes": len(html_content.encode("utf-8")),
                    "headers": {
                        "server": response_headers.get("server", "Hidden / Cloudflare"),
                        "content_type": response_headers.get("content-type", "text/html"),
                        "x_frame_options": response_headers.get("x-frame-options", "Missing"),
                        "strict_transport_security": "hsts" in response_headers.get("strict-transport-security", "").lower()
                    },
                    "robots_txt": {
                        "url": robots_url,
                        "found": robots_txt_found
                    },
                    "sitemap_xml": {
                        "url": sitemap_url,
                        "found": sitemap_found
                    },
                    "html": html_content
                }

        except Exception as e:
            # Fallback for synthetic / offline analysis or connectivity failure
            return {
                "success": False,
                "target_url": target_url,
                "error": str(e),
                "status_code": 0,
                "latency_ms": 0,
                "is_https": target_url.startswith("https://"),
                "content_length_bytes": 0,
                "headers": {},
                "robots_txt": {"url": f"{base_origin}/robots.txt", "found": False},
                "sitemap_xml": {"url": f"{base_origin}/sitemap.xml", "found": False},
                "html": ""
            }

web_crawler = WebCrawler()
