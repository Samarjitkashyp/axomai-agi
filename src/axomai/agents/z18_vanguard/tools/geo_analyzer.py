"""
Z18 Vanguard - Generative Engine Optimization (GEO) Analyzer.
Evaluates readiness for Google AI Overviews, SearchGPT, and LLM Citation synthesis.
Audits Quotability score, statistical & empirical density, E-E-A-T signals,
author attribution, publication timestamps, and topical depth.
"""

import re
from typing import Dict, Any, List
from bs4 import BeautifulSoup

class GEOAnalyzer:
    """Evaluates suitability for generative AI synthesis, LLM citations, and AI Overviews."""

    def analyze(self, html: str, target_url: str) -> Dict[str, Any]:
        """Audits page against Generative Engine Optimization (GEO) criteria."""
        issues: List[Dict[str, Any]] = []
        deductions = 0

        soup = BeautifulSoup(html, "html.parser")

        # Strip scripts and styles for content evaluation
        for s in soup(["script", "style", "noscript", "svg"]):
            s.decompose()

        body_text = soup.get_text(separator=" ", strip=True)
        words = body_text.split()
        total_word_count = len(words)

        # 1. Topical Depth & Content Volume
        if total_word_count < 350:
            issues.append({
                "severity": "CRITICAL",
                "category": "GEO",
                "element": "Body Text",
                "issue": f"Thin content detected ({total_word_count} words)",
                "impact": "Generative models (Google Gemini, GPT-4) dismiss thin pages as low-information gain, skipping them for AI Overviews.",
                "fix": "Expand content to at least 800–1,200 words providing comprehensive topical depth and unique insights."
            })
            deductions += 25
        elif total_word_count < 700:
            issues.append({
                "severity": "WARNING",
                "category": "GEO",
                "element": "Body Text",
                "issue": f"Moderate content depth ({total_word_count} words)",
                "impact": "May lose citation share to more thorough, long-form industry guides.",
                "fix": "Add case studies, practical examples, and exhaustive sub-topic breakdowns."
            })
            deductions += 10

        # 2. Quotability & Statistical Density (Numbers, Percentages, Currencies, Benchmarks)
        stats_patterns = [
            r'\b\d+(?:\.\d+)?%',                                   # Percentages: 45%, 99.8%
            r'(?:₹|\$|€|£)\s*\d+(?:,\d+)*(?:\.\d+)?(?:\s*(?:k|m|b|lakh|crore))?', # Currency
            r'\b\d{4}\b',                                          # Years: 2024, 2025, 2026
            r'\b\d+(?:\.\d+)?\s*(?:ms|sec|kg|ton|km|mb|gb|tb|hz)\b'# Physical units
        ]
        
        found_data_points = []
        for pat in stats_patterns:
            matches = re.findall(pat, body_text, re.IGNORECASE)
            found_data_points.extend(matches)

        quotability_count = len(found_data_points)
        if quotability_count < 3:
            issues.append({
                "severity": "CRITICAL",
                "category": "GEO",
                "element": "Empirical Data",
                "issue": "Extremely low statistical and numerical density (Quotability Deficit)",
                "impact": "LLMs cite sources that provide specific numbers, benchmarks, and verifiable metrics. Vague prose is rarely cited in AI Overviews.",
                "fix": "Infuse content with concrete statistics, empirical survey results, benchmark comparisons, and verifiable metrics."
            })
            deductions += 24
        elif quotability_count < 8:
            issues.append({
                "severity": "WARNING",
                "category": "GEO",
                "element": "Empirical Data",
                "issue": f"Low statistical density ({quotability_count} data points detected)",
                "impact": "Limited quote-worthy anchor statements for AI synthesis.",
                "fix": "Incorporate at least 10–15 factual data points and benchmark comparisons."
            })
            deductions += 10

        # 3. E-E-A-T: Author Byline & Transparency
        has_author = bool(
            soup.find("meta", attrs={"name": re.compile(r"^author$", re.I)}) or
            soup.find(attrs={"rel": re.compile(r"author", re.I)}) or
            soup.find(class_=re.compile(r"author|byline|written-by|editor", re.I)) or
            "by " in body_text.lower()[:500]
        )
        if not has_author:
            issues.append({
                "severity": "WARNING",
                "category": "GEO",
                "element": "Author Byline / E-E-A-T",
                "issue": "Missing clear author byline or expert attribution",
                "impact": "Google AI and generative engines prioritize verified human expertise and reputable credentials.",
                "fix": "Include author byline with credentials, job title, and link to an author bio page."
            })
            deductions += 14

        # 4. Content Freshness: Publication & Update Timestamps
        has_date = bool(
            soup.find("meta", property=re.compile(r"published_time|modified_time|date", re.I)) or
            soup.find("time") or
            soup.find(class_=re.compile(r"date|published|updated|timestamp", re.I))
        )
        if not has_date:
            issues.append({
                "severity": "WARNING",
                "category": "GEO",
                "element": "Freshness Metadata",
                "issue": "Missing explicit publication date (<time> or dateModified tag)",
                "impact": "Generative engines down-weight undated content to avoid hallucinating stale information.",
                "fix": "Add semantic `<time datetime='...'>` tags and Schema `datePublished` / `dateModified` properties."
            })
            deductions += 12

        # 5. Authoritative External Citations
        external_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("http") and not any(d in href for d in ["facebook", "twitter", "linkedin", "instagram", "youtube"]):
                external_links.append(href)

        if len(external_links) == 0:
            issues.append({
                "severity": "OPPORTUNITY",
                "category": "GEO",
                "element": "Outbound References",
                "issue": "Zero outbound authoritative citations found",
                "impact": "Connecting your content to high-authority peer sources signals credibility and academic rigor to generative parsers.",
                "fix": "Link to credible industry benchmarks, research papers, or primary official sources."
            })
            deductions += 8

        geo_score = max(10, 100 - deductions)

        return {
            "geo_score": geo_score,
            "total_word_count": total_word_count,
            "quotability_metrics_count": quotability_count,
            "sample_data_points": found_data_points[:6],
            "has_author_byline": has_author,
            "has_freshness_timestamps": has_date,
            "external_citations_count": len(external_links),
            "issues": issues
        }

geo_analyzer = GEOAnalyzer()
