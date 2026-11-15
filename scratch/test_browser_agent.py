"""
Unit test for Z2 Bravo Autonomous Browser Agent & Z Sentinel SSRF Protection.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from axomai.agents.z2_bravo.tools.browser_agent import browser_agent, ZSentinelSsrfGuard

def test_ssrf_protection():
    print("Testing Z Sentinel SSRF security protection...")
    malicious_targets = [
        "http://localhost:8080/api/admin",
        "http://127.0.0.1:5432/db",
        "http://169.254.169.254/latest/meta-data/",
        "http://10.0.0.1/internal",
        "http://192.168.1.1/router",
        "file:///etc/passwd",
        "gopher://127.0.0.1:6379"
    ]

    for target in malicious_targets:
        res = browser_agent.browse_and_extract(target)
        assert res["success"] is False, f"Expected block for: {target}"
        assert res["security_status"] == "BLOCKED_BY_Z_SENTINEL"
        print(f"  [BLOCKED AS EXPECTED]: {target} -> {res['violation']}")

    print("PASS: SSRF Guard successfully blocked all prohibited internal/loopback targets!\n")

def test_table_parsing_and_extraction():
    print("Testing table parser on synthetic HTML DOM...")
    from bs4 import BeautifulSoup
    sample_html = """
    <html>
      <head><title>Assam Infrastructure Tenders 2024</title></head>
      <body>
        <h1>Active PWD Tenders</h1>
        <table id="tender_tbl">
          <tr><th>Tender ID</th><th>Project Title</th><th>Estimated Value (Cr)</th><th>Bid Deadline</th></tr>
          <tr><td>AS-PWD-001</td><td>Guwahati Ring Road Phase 2</td><td>₹450.0</td><td>2024-12-15</td></tr>
          <tr><td>AS-PWD-002</td><td>Brahmaputra Bridge Feeder</td><td>₹185.5</td><td>2024-12-20</td></tr>
          <tr><td>AS-PWD-003</td><td>Silchar Highway Expansion</td><td>₹92.0</td><td>2024-12-28</td></tr>
        </table>
        <a href="https://assam.gov.in/tenders/subpage">More Tenders</a>
      </body>
    </html>
    """
    soup = BeautifulSoup(sample_html, "html.parser")
    tbl = soup.find("table")
    extracted = browser_agent._parse_table(tbl, 1)

    assert extracted is not None
    assert len(extracted["headers"]) == 4
    assert len(extracted["rows"]) == 3
    print(f"Headers: {extracted['headers']}")
    print(f"Extracted {len(extracted['rows'])} rows cleanly:")
    for r in extracted["rows"]:
        print(f"  {r}")

    print("PASS: Autonomous Browser Agent table parsing passed 100%!")

if __name__ == "__main__":
    test_ssrf_protection()
    test_table_parsing_and_extraction()

