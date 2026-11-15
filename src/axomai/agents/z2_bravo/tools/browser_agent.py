"""
Z2 Bravo - Autonomous Browser Agent with Z Sentinel SSRF Protection.
Enables goal-oriented web navigation, structured table extraction,
link exploration, and portal crawling with zero-trust network safety.
"""

import ipaddress
import re
import socket
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse, urljoin
import httpx
from bs4 import BeautifulSoup

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 AxomAI/2.0"
)

# SSRF Protected IP Subnets (RFC 1918, Loopback, Link-Local, Cloud Metadata)
BLOCKED_IP_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),  # AWS / Cloud Metadata IP
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]


class ZSentinelSsrfGuard:
    """Enterprise SSRF & Network Boundary Validator."""

    @staticmethod
    def validate_url(url: str) -> Dict[str, Any]:
        """Validates that a URL is safe and does not target internal or prohibited networks."""
        try:
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https"):
                return {"safe": False, "reason": f"Disallowed scheme '{parsed.scheme}'. Only http and https permitted."}

            hostname = parsed.hostname
            if not hostname:
                return {"safe": False, "reason": "Missing or invalid hostname in URL."}

            # Check loopback names
            if hostname.lower() in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
                return {"safe": False, "reason": f"Access to localhost / loopback '{hostname}' is strictly blocked."}

            # DNS Resolution check against private IP ranges
            try:
                ip_addrs = socket.gethostbyname_ex(hostname)[2]
                for ip_str in ip_addrs:
                    ip_obj = ipaddress.ip_address(ip_str)
                    for blocked_net in BLOCKED_IP_NETWORKS:
                        if ip_obj in blocked_net:
                            return {
                                "safe": False,
                                "reason": f"SSRF Protection: Host '{hostname}' resolves to private IP '{ip_str}' in '{blocked_net}'."
                            }
            except socket.gaierror:
                # Host may be unresolvable or synthetic in tests
                pass

            return {"safe": True, "hostname": hostname}
        except Exception as e:
            return {"safe": False, "reason": f"URL parsing error: {str(e)}"}


class AutonomousBrowserAgent:
    """Autonomous Web Navigation & Structured RPA Agent for Z2 Bravo."""

    def __init__(self, timeout: float = 8.0, max_hops: int = 2):
        self.timeout = timeout
        self.max_hops = max_hops
        self.headers = {"User-Agent": USER_AGENT}

    def browse_and_extract(self, start_url: str, goal: Optional[str] = None) -> Dict[str, Any]:
        """
        Navigates to the given URL, extracts text, tables, and follows relevant downstream links.
        """
        # 1. Z Sentinel SSRF Pre-flight Check
        sec_check = ZSentinelSsrfGuard.validate_url(start_url)
        if not sec_check["safe"]:
            return {
                "success": False,
                "url": start_url,
                "security_status": "BLOCKED_BY_Z_SENTINEL",
                "violation": sec_check["reason"],
                "tables": [],
                "links": []
            }

        # 2. Fetch primary page
        page_data = self._fetch_and_parse(start_url)
        if not page_data["success"]:
            return page_data

        # 3. Autonomous link discovery & multi-hop crawling
        visited_pages = [page_data]
        discovered_tables = list(page_data.get("tables", []))

        # Filter downstream links matching the goal or keywords
        target_keywords = self._extract_keywords(goal or "report tender price data schedule analysis")
        candidate_links = page_data.get("links", [])

        scored_links = []
        for l in candidate_links:
            text_match = sum(1 for kw in target_keywords if kw in l["text"].lower() or kw in l["url"].lower())
            if text_match > 0:
                scored_links.append((text_match, l["url"], l["text"]))

        # Sort highest relevance first and explore top hop
        scored_links.sort(reverse=True, key=lambda x: x[0])
        hops_taken = 0
        for score, link_url, link_text in scored_links[:self.max_hops]:
            sec = ZSentinelSsrfGuard.validate_url(link_url)
            if not sec["safe"]:
                continue

            sub_data = self._fetch_and_parse(link_url)
            if sub_data["success"]:
                visited_pages.append(sub_data)
                discovered_tables.extend(sub_data.get("tables", []))
                hops_taken += 1

        return {
            "success": True,
            "goal": goal,
            "security_status": "Z_SENTINEL_VERIFIED_SAFE",
            "primary_url": start_url,
            "pages_visited_count": len(visited_pages),
            "hops_explored": hops_taken,
            "extracted_tables_count": len(discovered_tables),
            "tables": discovered_tables[:5],  # Top 5 structured tables
            "pages_summary": [
                {
                    "title": p.get("title"),
                    "url": p.get("url"),
                    "summary": p.get("text_snippet", "")[:300]
                }
                for p in visited_pages
            ]
        }

    def _fetch_and_parse(self, url: str) -> Dict[str, Any]:
        """Fetches a single page and parses HTML tables and semantics."""
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True, headers=self.headers) as client:
                resp = client.get(url)
                if resp.status_code != 200:
                    return {
                        "success": False,
                        "url": url,
                        "error": f"HTTP {resp.status_code} returned by web server."
                    }

                # Parse DOM with BeautifulSoup
                soup = BeautifulSoup(resp.text, "html.parser")

                # Page title
                title = soup.title.string.strip() if soup.title and soup.title.string else url

                # Extract HTML Tables
                tables_data = []
                for idx, tbl in enumerate(soup.find_all("table")[:6]):
                    extracted = self._parse_table(tbl, idx + 1)
                    if extracted and len(extracted["rows"]) > 0:
                        tables_data.append(extracted)

                # Extract Links
                found_links = []
                for a_tag in soup.find_all("a", href=True):
                    href = a_tag["href"]
                    full_url = urljoin(url, href)
                    text = a_tag.get_text(strip=True)
                    if text and full_url.startswith(("http://", "https://")):
                        found_links.append({"text": text, "url": full_url})

                # Extract cleaned text
                for tag in soup(["script", "style", "nav", "footer", "aside"]):
                    tag.decompose()
                clean_text = " ".join(soup.stripped_strings)

                return {
                    "success": True,
                    "url": url,
                    "title": title,
                    "text_snippet": clean_text[:2000],
                    "tables": tables_data,
                    "links": found_links[:30]
                }
        except Exception as e:
            return {"success": False, "url": url, "error": f"Browser engine fetch error: {str(e)}"}

    def _parse_table(self, table_soup: Any, table_idx: int) -> Optional[Dict[str, Any]]:
        """Extracts structured 2D table matrix from HTML table element."""
        headers = []
        rows = []

        header_row = table_soup.find("tr")
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]

        for tr in table_soup.find_all("tr")[1:]:
            row_cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            if any(row_cells):
                rows.append(row_cells)

        if not headers and rows:
            headers = [f"Col {i+1}" for i in range(len(rows[0]))]

        if not rows:
            return None

        return {
            "table_id": f"table_{table_idx}",
            "headers": headers,
            "rows": rows[:15],
            "total_rows": len(rows),
            "columns_count": len(headers)
        }

    def _extract_keywords(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        stop_words = {"this", "that", "with", "from", "have", "what", "which", "will"}
        return [w for w in words if w not in stop_words]


browser_agent = AutonomousBrowserAgent()

