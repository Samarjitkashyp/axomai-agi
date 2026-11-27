"""
Z7 Visionary - Live Website URL Brand Kit Extractor & Document-to-Deck Ingestor.
1. Fetches any target website URL via HTTP GET, parses <title>, theme-color meta tag,
   and primary CSS hex colors to automatically theme PPTX & HTML5 decks.
2. Reads uploaded PDF/Excel/Doc chunks from PostgreSQL (via doc_id) so presentations
   are grounded in the user's actual uploaded enterprise documents.
"""

import re
import uuid
import requests
from typing import Dict, Any, Optional, Tuple


class BrandKitAndDocIngestor:
    """Extracts live brand identity from URLs and ingests uploaded documents into slide context."""

    def _hex_to_rgb(self, hex_str: str) -> Tuple[int, int, int]:
        h = hex_str.lstrip("#")
        if len(h) == 6:
            return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return (0, 229, 255)

    def extract_brand_kit_from_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrapes live website metadata & CSS hex palette for instant white-label branding."""
        try:
            resp = requests.get(url, headers={"User-Agent": "AxomAI-Z7BrandKit/1.0"}, timeout=5)
            if resp.status_code == 200:
                html = resp.text[:120000]
                title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
                brand_title = re.sub(r'\s+', ' ', title_m.group(1)).strip()[:45] if title_m else url

                theme_m = re.search(r'<meta[^>]+name=["\']theme-color["\'][^>]+content=["\'](#[0-9a-fA-F]{6})["\']', html, re.IGNORECASE)
                hex_candidates = re.findall(r'#[0-9a-fA-F]{6}\b', html)
                # Filter out pure white/black/near-gray
                vivid = [
                    h for h in hex_candidates
                    if h.lower() not in ("#ffffff", "#000000", "#f8fafc", "#f1f5f9", "#111111", "#222222", "#333333")
                ]
                accent_hex = theme_m.group(1) if theme_m else (vivid[0] if vivid else "#00e5ff")
                return {
                    "source_url": url,
                    "brand_name": brand_title,
                    "accent_hex": accent_hex,
                    "accent_rgb": self._hex_to_rgb(accent_hex),
                    "extraction_status": "LIVE_URL_BRAND_EXTRACTED"
                }
        except Exception:
            pass
        return None

    def ingest_uploaded_document(self, doc_id: Optional[str]) -> Optional[str]:
        """Reads extracted document chunks from PostgreSQL if doc_id is provided."""
        if not doc_id:
            return None
        try:
            from axomai.db.session import SyncSessionLocal
            from axomai.db.models import DocumentChunk
            doc_uuid = uuid.UUID(doc_id)
            with SyncSessionLocal() as db:
                chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc_uuid).limit(6).all()
                if chunks:
                    return "\n".join(c.content[:500] for c in chunks)
        except Exception:
            pass
        return None


brand_doc_ingestor = BrandKitAndDocIngestor()
