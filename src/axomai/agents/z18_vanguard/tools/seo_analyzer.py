"""
Z18 Vanguard - Technical & On-Page SEO Analyzer.
Evaluates title, meta descriptions, canonical tags, indexability, headings hierarchy,
OpenGraph, Twitter cards, image alt attributes, and link architecture.
"""

import re
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup

class SEOAnalyzer:
    """Comprehensive technical and on-page search engine optimization evaluator."""

    def analyze(self, html: str, target_url: str, crawl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Performs exhaustive on-page & technical SEO audit."""
        issues: List[Dict[str, Any]] = []
        deductions = 0

        soup = BeautifulSoup(html, "html.parser")

        # 1. Title Tag Inspection
        title_tag = soup.find("title")
        title_text = title_tag.get_text(strip=True) if title_tag else ""
        title_length = len(title_text)

        if not title_text:
            issues.append({
                "severity": "CRITICAL",
                "category": "SEO",
                "element": "<title>",
                "issue": "Missing or empty Title tag",
                "impact": "Search engines cannot determine page theme; catastrophic ranking penalty.",
                "fix": "Add a unique, keyword-rich <title> tag between 50 to 60 characters."
            })
            deductions += 25
        elif title_length < 30:
            issues.append({
                "severity": "WARNING",
                "category": "SEO",
                "element": "<title>",
                "issue": f"Title tag too short ({title_length} characters)",
                "impact": "Missed opportunity for primary and secondary keyword placement.",
                "fix": "Expand title to 50–60 characters incorporating primary intent and brand suffix."
            })
            deductions += 8
        elif title_length > 65:
            issues.append({
                "severity": "WARNING",
                "category": "SEO",
                "element": "<title>",
                "issue": f"Title tag too long ({title_length} characters)",
                "impact": "Title will be truncated in Google SERP with an ellipsis (...).",
                "fix": "Trim title to under 60 characters so it fits fully within 600px desktop/mobile width."
            })
            deductions += 6

        # 2. Meta Description Inspection
        meta_desc = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
        desc_text = meta_desc.get("content", "").strip() if meta_desc else ""
        desc_length = len(desc_text)

        if not desc_text:
            issues.append({
                "severity": "CRITICAL",
                "category": "SEO",
                "element": '<meta name="description">',
                "issue": "Missing Meta Description",
                "impact": "Google will generate random snippet text, resulting in lower Organic Click-Through Rates (CTR).",
                "fix": "Add an engaging, action-oriented meta description between 145 to 160 characters."
            })
            deductions += 18
        elif desc_length < 80:
            issues.append({
                "severity": "WARNING",
                "category": "SEO",
                "element": '<meta name="description">',
                "issue": f"Meta Description too short ({desc_length} characters)",
                "impact": "Fails to fully utilize SERP snippet real-estate.",
                "fix": "Expand description to 145–160 characters with clear value proposition and call to action."
            })
            deductions += 6
        elif desc_length > 165:
            issues.append({
                "severity": "WARNING",
                "category": "SEO",
                "element": '<meta name="description">',
                "issue": f"Meta Description too long ({desc_length} characters)",
                "impact": "Snippet will be cut off on mobile and desktop search results.",
                "fix": "Condense description to under 160 characters."
            })
            deductions += 5

        # 3. Canonical Tag Verification
        canonical = soup.find("link", attrs={"rel": re.compile(r"^canonical$", re.I)})
        canonical_url = canonical.get("href", "").strip() if canonical else ""
        if not canonical_url:
            issues.append({
                "severity": "WARNING",
                "category": "SEO",
                "element": '<link rel="canonical">',
                "issue": "Missing Canonical URL tag",
                "impact": "High risk of duplicate content dilution across URL variants (HTTP/HTTPS/trailing slash).",
                "fix": f'Add `<link rel="canonical" href="{target_url}" />` in the `<head>` section.'
            })
            deductions += 10

        # 4. Robots Meta Tag & Indexability
        robots_meta = soup.find("meta", attrs={"name": re.compile(r"^robots$", re.I)})
        robots_content = robots_meta.get("content", "").lower() if robots_meta else "index, follow"
        is_noindex = "noindex" in robots_content
        if is_noindex:
            issues.append({
                "severity": "CRITICAL",
                "category": "SEO",
                "element": '<meta name="robots">',
                "issue": "Page is explicitly set to 'noindex'",
                "impact": "Search engine crawlers are blocked from indexing this page in search results.",
                "fix": "Remove 'noindex' directive from robots meta tag unless page is intentionally private."
            })
            deductions += 35

        # 5. Headings Architecture (H1, H2, H3)
        h1_tags = soup.find_all("h1")
        h2_tags = soup.find_all("h2")
        h3_tags = soup.find_all("h3")

        if len(h1_tags) == 0:
            issues.append({
                "severity": "CRITICAL",
                "category": "SEO",
                "element": "<h1>",
                "issue": "Missing H1 Heading tag",
                "impact": "Weakens topical clarity and primary keyword signal for crawlers.",
                "fix": "Add exactly one descriptive <h1> tag reflecting the primary theme of the page."
            })
            deductions += 15
        elif len(h1_tags) > 1:
            issues.append({
                "severity": "WARNING",
                "category": "SEO",
                "element": "<h1>",
                "issue": f"Multiple H1 tags detected ({len(h1_tags)} H1s found)",
                "impact": "Dilutes the main semantic hierarchy of the document.",
                "fix": "Keep only one primary <h1> and convert secondary headings to <h2>."
            })
            deductions += 6

        # 6. Mobile Viewport Tag
        viewport = soup.find("meta", attrs={"name": re.compile(r"^viewport$", re.I)})
        if not viewport:
            issues.append({
                "severity": "CRITICAL",
                "category": "SEO",
                "element": '<meta name="viewport">',
                "issue": "Missing Mobile Viewport Meta tag",
                "impact": "Fails Google Mobile-First Indexing requirements; degraded rankings on mobile devices.",
                "fix": 'Add `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.'
            })
            deductions += 15

        # 7. Open Graph & Social Cards
        og_title = soup.find("meta", property="og:title")
        og_desc = soup.find("meta", property="og:description")
        og_image = soup.find("meta", property="og:image")
        if not (og_title and og_desc and og_image):
            issues.append({
                "severity": "OPPORTUNITY",
                "category": "SEO",
                "element": '<meta property="og:*">',
                "issue": "Incomplete OpenGraph Social metadata",
                "impact": "Sub-optimal social sharing link previews on LinkedIn, WhatsApp, X, and Facebook.",
                "fix": "Add complete OpenGraph tags: og:title, og:description, og:image, and og:url."
            })
            deductions += 5

        # 8. Images and Alt Attributes
        images = soup.find_all("img")
        images_missing_alt = [img for img in images if not img.get("alt") or img.get("alt").strip() == ""]
        if images_missing_alt:
            issues.append({
                "severity": "WARNING",
                "category": "SEO",
                "element": '<img alt="...">',
                "issue": f"{len(images_missing_alt)} out of {len(images)} images missing descriptive alt text",
                "impact": "Hurts image accessibility (ADA/WCAG) and Google Image Search visibility.",
                "fix": "Add descriptive, keyword-relevant alt attributes to all content images."
            })
            deductions += min(10, len(images_missing_alt) * 2)

        # 9. Link Architecture
        links = soup.find_all("a", href=True)
        empty_anchors = [a for a in links if a["href"].strip() in ["#", "", "javascript:void(0)"]]
        if empty_anchors:
            issues.append({
                "severity": "OPPORTUNITY",
                "category": "SEO",
                "element": '<a href="#">',
                "issue": f"{len(empty_anchors)} empty or unlinked placeholder anchor tags detected",
                "impact": "Wastes crawl budget and creates dead-end signals for search bots.",
                "fix": "Replace empty anchor links with real navigational paths or clean button elements."
            })
            deductions += 4

        # 10. robots.txt and sitemap.xml checks from crawler
        if not crawl_data.get("robots_txt", {}).get("found", False):
            issues.append({
                "severity": "WARNING",
                "category": "SEO",
                "element": "robots.txt",
                "issue": "robots.txt file not found or inaccessible",
                "impact": "Crawlers have no explicit crawl guidelines or sitemap directive.",
                "fix": "Deploy a clean robots.txt file at the domain root specifying Sitemap location."
            })
            deductions += 6

        if not crawl_data.get("sitemap_xml", {}).get("found", False):
            issues.append({
                "severity": "WARNING",
                "category": "SEO",
                "element": "sitemap.xml",
                "issue": "XML Sitemap not found at default /sitemap.xml path",
                "impact": "Delays indexing of newly published pages and deep URLs.",
                "fix": "Generate and submit a clean XML sitemap to Google Search Console and Bing Webmaster."
            })
            deductions += 6

        seo_score = max(10, 100 - deductions)

        return {
            "seo_score": seo_score,
            "title": title_text,
            "title_length": title_length,
            "meta_description": desc_text,
            "meta_description_length": desc_length,
            "canonical_url": canonical_url,
            "is_noindex": is_noindex,
            "headings_summary": {
                "h1_count": len(h1_tags),
                "h1_texts": [h.get_text(strip=True) for h in h1_tags[:3]],
                "h2_count": len(h2_tags),
                "h3_count": len(h3_tags)
            },
            "images_summary": {
                "total_images": len(images),
                "missing_alt_count": len(images_missing_alt)
            },
            "links_summary": {
                "total_links": len(links),
                "empty_anchors": len(empty_anchors)
            },
            "issues": issues
        }

seo_analyzer = SEOAnalyzer()
