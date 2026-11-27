"""
Z18 Vanguard - Answer Engine Optimization (AEO) Analyzer.
Evaluates readiness for AI conversational answer engines (Perplexity AI, ChatGPT Search, Claude, Google Gemini).
Checks Schema.org JSON-LD structured data, FAQ formatting, direct-answer snippet density,
question-framed headings, and extractable tables/bullet lists.
"""

import re
import json
from typing import Dict, Any, List
from bs4 import BeautifulSoup

QUESTION_WORDS = [
    "what", "how", "why", "when", "where", "who", "which",
    "can", "does", "is", "are", "should", "will", "best", "guide", "difference"
]

class AEOAnalyzer:
    """Evaluates readiness for conversational answer engines and featured snippets."""

    def analyze(self, html: str, target_url: str) -> Dict[str, Any]:
        """Audits page against modern Answer Engine Optimization (AEO) protocols."""
        issues: List[Dict[str, Any]] = []
        deductions = 0

        soup = BeautifulSoup(html, "html.parser")

        # 1. Schema.org JSON-LD Detection & Type Validation
        script_schemas = soup.find_all("script", attrs={"type": re.compile(r"application/ld\+json", re.I)})
        parsed_schemas: List[Dict[str, Any]] = []
        schema_types: List[str] = []

        for s in script_schemas:
            try:
                content = s.string or s.text or ""
                data = json.loads(content.strip())
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "@type" in item:
                            schema_types.append(str(item["@type"]))
                            parsed_schemas.append(item)
                elif isinstance(data, dict):
                    if "@graph" in data and isinstance(data["@graph"], list):
                        for item in data["@graph"]:
                            if isinstance(item, dict) and "@type" in item:
                                schema_types.append(str(item["@type"]))
                                parsed_schemas.append(item)
                    elif "@type" in data:
                        schema_types.append(str(data["@type"]))
                        parsed_schemas.append(data)
            except Exception:
                issues.append({
                    "severity": "CRITICAL",
                    "category": "AEO",
                    "element": '<script type="application/ld+json">',
                    "issue": "Malformed JSON-LD Schema syntax",
                    "impact": "Search and answer engines will discard the entire structured data block due to JSON parsing failure.",
                    "fix": "Fix JSON syntax errors in your application/ld+json script tag."
                })
                deductions += 20

        if not schema_types:
            issues.append({
                "severity": "CRITICAL",
                "category": "AEO",
                "element": "Schema.org JSON-LD",
                "issue": "Zero Structured Data (Schema JSON-LD) detected",
                "impact": "AI answer engines (Perplexity, ChatGPT Search) cannot easily map entities, authors, FAQs, or organizations into their knowledge graphs.",
                "fix": "Inject comprehensive JSON-LD schemas (Organization, WebPage, and FAQPage or Article)."
            })
            deductions += 30
        else:
            # Check high-value AEO schemas
            has_faq = any("FAQPage" in t for t in schema_types)
            has_org = any(t in ["Organization", "Corporation", "LocalBusiness"] for t in schema_types)
            has_content_type = any(t in ["Article", "BlogPosting", "Product", "Service", "HowTo", "WebPage"] for t in schema_types)

            if not has_faq:
                issues.append({
                    "severity": "OPPORTUNITY",
                    "category": "AEO",
                    "element": "FAQPage Schema",
                    "issue": "No FAQPage Schema markup found",
                    "impact": "Missed opportunity for high-visibility Q&A rich snippets in Perplexity and Google SERPs.",
                    "fix": "Add FAQPage JSON-LD schema wrapping key user questions and authoritative answers."
                })
                deductions += 10

            if not has_org:
                issues.append({
                    "severity": "WARNING",
                    "category": "AEO",
                    "element": "Organization Schema",
                    "issue": "Missing Organization / Brand Schema markup",
                    "impact": "Answer engines cannot confidently anchor your brand entity into the Knowledge Graph.",
                    "fix": "Add Organization schema detailing legal name, logo, official website, and sameAs social profiles."
                })
                deductions += 8

        # 2. Question-Framed Headings Analysis
        all_headings = soup.find_all(["h2", "h3"])
        heading_texts = [h.get_text(strip=True) for h in all_headings if h.get_text(strip=True)]
        question_headings = []
        for ht in heading_texts:
            ht_lower = ht.lower()
            if any(ht_lower.startswith(q) or f" {q} " in ht_lower or ht.endswith("?") for q in QUESTION_WORDS):
                question_headings.append(ht)

        if not question_headings and len(all_headings) > 0:
            issues.append({
                "severity": "WARNING",
                "category": "AEO",
                "element": "Headings (H2/H3)",
                "issue": "No question-formatted headings detected",
                "impact": "AI answer engines query matching algorithms heavily favor headings formulated as natural questions.",
                "fix": "Refactor sub-headings into conversational user queries (e.g., 'What is...', 'How to...', 'Why choose...')."
            })
            deductions += 12

        # 3. Direct Answer Snippet Density (35 to 65 word answer blocks)
        paragraphs = soup.find_all("p")
        ideal_snippets = 0
        for p in paragraphs:
            text = p.get_text(strip=True)
            word_count = len(text.split())
            if 35 <= word_count <= 65:
                # Check if it has factual indicators (e.g. is, provides, means, includes, because)
                if any(ind in text.lower() for ind in ["is", "are", "refers to", "provides", "works by", "because", "includes"]):
                    ideal_snippets += 1

        if ideal_snippets == 0 and len(paragraphs) > 2:
            issues.append({
                "severity": "WARNING",
                "category": "AEO",
                "element": "<p> Content Blocks",
                "issue": "Absence of concise 35–65 word direct-answer summary paragraphs",
                "impact": "Answer engines struggle to extract crisp, self-contained summary quotes without editing.",
                "fix": "Place a crisp 40–50 word direct definition or answer immediately following each major H2 question."
            })
            deductions += 14

        # 4. Extractable Structured Elements (Lists & Tables)
        tables = soup.find_all("table")
        lists = soup.find_all(["ul", "ol", "dl"])
        total_structured_containers = len(tables) + len(lists)

        if total_structured_containers == 0:
            issues.append({
                "severity": "WARNING",
                "category": "AEO",
                "element": "Lists & Tables",
                "issue": "Zero bullet lists (<ol>/<ul>) or comparison tables (<table>) detected",
                "impact": "Answer engines prioritize bulleted steps and tabular comparisons for direct LLM response generation.",
                "fix": "Format key takeaways, feature comparisons, and multi-step processes into clean HTML lists or tables."
            })
            deductions += 12

        aeo_score = max(10, 100 - deductions)

        return {
            "aeo_score": aeo_score,
            "detected_schemas": schema_types,
            "schema_count": len(parsed_schemas),
            "question_headings_count": len(question_headings),
            "question_headings_samples": question_headings[:4],
            "direct_answer_snippets_detected": ideal_snippets,
            "structured_lists_count": len(lists),
            "structured_tables_count": len(tables),
            "issues": issues
        }

aeo_analyzer = AEOAnalyzer()
