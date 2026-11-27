"""
Unit & Integration Verification Suite for Z18 Vanguard:
Autonomous SEO, AEO (Answer Engine) & GEO (Generative AI) Intelligence Agent.
"""

import sys
from pathlib import Path

# Add src to PYTHONPATH
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

SAMPLE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AxomAI Platform - Sovereign General Intelligence for Enterprise</title>
    <meta name="description" content="AxomAI delivers sovereign general intelligence, enterprise multi-agent workflows, and verifiable cognitive architectures for modern organizations worldwide.">
    <link rel="canonical" href="https://axomai.org">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="AxomAI Platform">
    <meta property="og:description" content="Sovereign general intelligence and cognitive architectures.">
    <meta property="og:image" content="https://axomai.org/og.png">
    <meta name="author" content="Dr. Samarjit Kashyap">
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "AxomAI",
        "url": "https://axomai.org"
    }
    </script>
</head>
<body>
    <h1>AxomAI Sovereign Enterprise Intelligence</h1>
    <h2>What is AxomAI and how does it optimize enterprise operations?</h2>
    <p>AxomAI is an autonomous cognitive operating system engineered to streamline complex organizational workflows and provide verifiable intelligence across diverse business domains. By integrating real-time telemetry, specialized agent swarms, and mathematical verification, it accelerates enterprise throughput with measured consistency.</p>

    <h2>Why choose AxomAI for institutional scale-ups?</h2>
    <p>Our benchmarks demonstrate a 45.8% reduction in latency and over ₹12.5 Lakhs saved in compute costs across 12,000 automated runs in 2026.</p>
    <ul>
        <li>100% Deterministic Mathematical Verification</li>
        <li>Sub-second multi-agent swarm synthesis</li>
        <li>Zero hallucination tolerance for compliance</li>
    </ul>

    <img src="/logo.png" alt="AxomAI Logo">
    <img src="/banner.png">
    <a href="https://github.com/Samarjitkashyp/axomai-agi">Official Source Code</a>
</body>
</html>
"""

def test_z18_vanguard_suite():
    print("======================================================================")
    print("   RUNNING Z18 VANGUARD (SEO, AEO, GEO) FULL VERIFICATION SUITE       ")
    print("======================================================================")

    # 1. Test Web Crawler URL Extraction
    print("\n[1/6] Testing WebCrawler...")
    from axomai.agents.z18_vanguard.tools.web_crawler import web_crawler
    url1 = web_crawler.extract_url_from_query("Audit https://techcrunch.com for SEO")
    url2 = web_crawler.extract_url_from_query("Check seo of google.com please")
    assert url1 == "https://techcrunch.com", f"Expected 'https://techcrunch.com', got {url1}"
    assert url2 == "https://google.com", f"Expected 'https://google.com', got {url2}"
    print(f"  ✓ URL Extraction Verified: '{url1}' & '{url2}'")

    # 2. Test SEO Analyzer
    print("\n[2/6] Testing SEOAnalyzer...")
    from axomai.agents.z18_vanguard.tools.seo_analyzer import seo_analyzer
    mock_crawl = {
        "status_code": 200,
        "robots_txt": {"found": True},
        "sitemap_xml": {"found": True}
    }
    seo_res = seo_analyzer.analyze(SAMPLE_HTML, "https://axomai.org", mock_crawl)
    print(f"  ✓ SEO Score: {seo_res['seo_score']}/100")
    print(f"  ✓ Title: '{seo_res['title']}' ({seo_res['title_length']} chars)")
    print(f"  ✓ Meta Description Length: {seo_res['meta_description_length']}")
    print(f"  ✓ Headings: H1={seo_res['headings_summary']['h1_count']}, H2={seo_res['headings_summary']['h2_count']}")
    assert seo_res["seo_score"] >= 80, f"Expected SEO score >= 80, got {seo_res['seo_score']}"
    assert seo_res["headings_summary"]["h1_count"] == 1
    assert seo_res["images_summary"]["missing_alt_count"] == 1  # 1 image has alt, 1 missing alt
    print("  [PASS] SEOAnalyzer Verified!")

    # 3. Test AEO Analyzer
    print("\n[3/6] Testing AEOAnalyzer...")
    from axomai.agents.z18_vanguard.tools.aeo_analyzer import aeo_analyzer
    aeo_res = aeo_analyzer.analyze(SAMPLE_HTML, "https://axomai.org")
    print(f"  ✓ AEO Score: {aeo_res['aeo_score']}/100")
    print(f"  ✓ Detected Schemas: {aeo_res['detected_schemas']}")
    print(f"  ✓ Question Headings: {aeo_res['question_headings_count']}")
    print(f"  ✓ Direct Answer Snippets: {aeo_res['direct_answer_snippets_detected']}")
    assert "Organization" in aeo_res["detected_schemas"]
    assert aeo_res["question_headings_count"] >= 2
    assert aeo_res["direct_answer_snippets_detected"] >= 1
    print("  [PASS] AEOAnalyzer Verified!")

    # 4. Test GEO Analyzer
    print("\n[4/6] Testing GEOAnalyzer...")
    from axomai.agents.z18_vanguard.tools.geo_analyzer import geo_analyzer
    geo_res = geo_analyzer.analyze(SAMPLE_HTML, "https://axomai.org")
    print(f"  ✓ GEO Score: {geo_res['geo_score']}/100")
    print(f"  ✓ Empirical Quotability Data Points: {geo_res['quotability_metrics_count']} ({geo_res['sample_data_points']})")
    print(f"  ✓ Author Byline Present: {geo_res['has_author_byline']}")
    assert geo_res["quotability_metrics_count"] >= 3  # 45.8%, ₹12.5, 2026, 12,000
    assert geo_res["has_author_byline"] is True
    print("  [PASS] GEOAnalyzer Verified!")

    # 5. Test Remediation Engine
    print("\n[5/6] Testing RemediationEngine...")
    from axomai.agents.z18_vanguard.tools.remediation_engine import remediation_engine
    fixes = remediation_engine.generate_fixes("https://axomai.org", seo_res, aeo_res, geo_res)
    assert "<title>" in fixes["drop_in_head_html"]
    assert "application/ld+json" in fixes["drop_in_json_ld"]
    assert "FAQPage" in fixes["drop_in_json_ld"]
    print("  ✓ Drop-in HTML & Schema JSON-LD successfully synthesized!")
    print("  [PASS] RemediationEngine Verified!")

    # 6. Test Master Orchestrator Routing & Live Stream
    print("\n[6/6] Testing Master Orchestrator Routing & Z18 Execution...")
    from axomai.agents.master_orchestrator import MasterOrchestrator
    orchestrator = MasterOrchestrator()

    # Routing checks
    q1 = "audit https://example.com for seo aeo and geo"
    q2 = "kisi website ka seo check karke batao kya issue he aur kaise fix kare"
    q3 = "perform a comprehensive technical seo and schema audit for https://startup.io"

    r1 = orchestrator.classify_and_route(q1)
    r2 = orchestrator.classify_and_route(q2)
    r3 = orchestrator.classify_and_route(q3)

    print(f"  ✓ Routed '{q1}' -> {r1['agent']} ({r1['name']})")
    print(f"  ✓ Routed '{q2}' -> {r2['agent']} ({r2['name']})")
    print(f"  ✓ Routed '{q3}' -> {r3['agent']} ({r3['name']})")

    assert r1["agent"] == "z18", f"Expected 'z18', got {r1['agent']}"
    assert r2["agent"] == "z18", f"Expected 'z18', got {r2['agent']}"
    assert r3["agent"] == "z18", f"Expected 'z18', got {r3['agent']}"

    # Stream execution check
    print("  ✓ Executing live audit stream...")
    events = list(orchestrator.orchestrate_stream(query="audit https://axomai.org for seo aeo geo"))
    assert len(events) > 5
    has_meta = any(e.get("type") == "meta" and e.get("agent") == "Z18 Vanguard" for e in events)
    has_done = any(e.get("type") == "done" for e in events)
    assert has_meta, "Expected Z18 Vanguard meta event"
    assert has_done, "Expected done event"
    print(f"  ✓ Live Audit Stream Verified ({len(events)} events emitted)!")
    print("  [PASS] Master Orchestrator Z18 Integration 100% Operational!")

    print("\n======================================================================")
    print(">>> 🎉 Z18 VANGUARD (SEO, AEO, GEO) PASSED ALL TESTS WITH 100% SUCCESS <<<")
    print("======================================================================")

if __name__ == "__main__":
    test_z18_vanguard_suite()
