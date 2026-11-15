"""
Z2 Bravo - Autonomous Deep Web & Market Research Agent.
Orchestrates multi-query web crawling, concurrent page extraction,
real-time fact verification, market competitor matrix synthesis,
cross-document gap analysis, and executive research dossier generation.
"""

import os
import re
import json
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List, Generator
from datetime import datetime

from rich.console import Console
from sqlalchemy.orm import Session

from axomai.config import settings
from axomai.db.session import SyncSessionLocal
from axomai.db.models import Document, AgentSession, AgentTaskLog
from axomai.core.llm import llm_brain
from axomai.agents.z2_bravo.router import research_router, ResearchTaskType
from axomai.agents.z2_bravo.tools.web_search import web_search_engine
from axomai.agents.z2_bravo.tools.web_scraper import web_scraper_engine
from axomai.agents.z2_bravo.tools.dossier_generator import dossier_generator_engine
from axomai.agents.z2_bravo.tools.multi_hop_engine import multi_hop_engine
from axomai.agents.z2_bravo.tools.radar_engine import radar_engine
from axomai.agents.z2_bravo.tools.quadrant_engine import quadrant_engine
from axomai.agents.z2_bravo.tools.sentiment_engine import sentiment_engine
from axomai.agents.z2_bravo.tools.filings_engine import filings_engine
from axomai.agents.z2_bravo.tools.regional_crawler import regional_crawler
from axomai.agents.z2_bravo.tools.podcast_engine import podcast_engine
from axomai.agents.z2_bravo.tools.browser_agent import browser_agent

console = Console()

class Z2BravoAgent:
    """
    Z2 Bravo - Autonomous Deep Web & Market Research Agent.
    """
    def __init__(self):
        self.name = "Z2 Bravo"
        self.role = "Autonomous Deep Web & Market Research Agent"
        self.router = research_router

    def research(
        self,
        topic: str,
        session_id: Optional[str] = None,
        doc_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synchronous execution of Deep Web & Market Research.
        """
        generator = self.research_stream(topic, session_id=session_id, doc_id=doc_id)
        meta_data = {}
        full_answer = ""

        for event in generator:
            if event.get("type") == "meta":
                meta_data = event
            elif event.get("type") == "token":
                full_answer += event.get("content", "")
            elif event.get("type") == "done":
                full_answer = event.get("answer", full_answer)

        return {
            "agent": self.name,
            "topic": topic,
            "task_type": meta_data.get("task_type"),
            "tools_used": meta_data.get("tools_used", []),
            "sources": meta_data.get("sources", []),
            "market_matrix": meta_data.get("market_matrix"),
            "chart": meta_data.get("chart"),
            "generated_file": meta_data.get("generated_file"),
            "verification_audit": meta_data.get("verification_audit"),
            "radar_data": meta_data.get("radar_data"),
            "quadrant_data": meta_data.get("quadrant_data"),
            "sentiment_pulse": meta_data.get("sentiment_pulse"),
            "filings_data": meta_data.get("filings_data"),
            "regional_data": meta_data.get("regional_data"),
            "podcast_data": meta_data.get("podcast_data"),
            "answer": full_answer
        }

    def research_stream(
        self,
        topic: str,
        session_id: Optional[str] = None,
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Real-time SSE streaming execution of Z2 Bravo Deep Web Research.
        Yields status updates, meta data (sources, citations, dossier card),
        and token-by-token answer stream.
        """
        session_id = session_id or str(uuid.uuid4())[:8]
        tools_used = ["ddgs_web_search", "web_scraper"]

        # 1. Fetch Internal Document Context if provided (Z1 + Z2 Synergy)
        internal_doc_context = ""
        active_doc_name = None
        if doc_id:
            try:
                doc_uuid = uuid.UUID(doc_id)
                with SyncSessionLocal() as db:
                    doc = db.query(Document).filter(Document.id == doc_uuid).first()
                    if doc:
                        active_doc_name = doc.filename
                        udm = doc.udm_data or {}
                        pages = udm.get("pages", [])
                        snippets = [p.get("text", "")[:600] for p in pages[:4] if p.get("text")]
                        internal_doc_context = f"\n\n[INTERNAL DOCUMENT: {doc.filename} (Type: {doc.file_type})]:\n" + "\n---\n".join(snippets)
                        tools_used.append("z1_document_bridge")
            except Exception:
                pass

        # 1.5. Check for Direct Autonomous Browser Navigation / RPA Request (Phase 4)
        url_match = re.search(r'https?://[^\s]+', topic)
        is_direct_browser = bool(url_match) or any(k in topic.lower() for k in ["browse ", "navigate to ", "crawl ", "extract tables", "web rpa"])
        if url_match or (is_direct_browser and ("http" in topic or "portal" in topic or "gov.in" in topic)):
            target_url = url_match.group(0) if url_match else "https://assam.gov.in"
            yield {
                "type": "status",
                "stage": "browser_navigation",
                "message": f"🌐 Z2 Bravo: Autonomous Browser Agent exploring {target_url} with Z Sentinel SSRF guard..."
            }
            browser_res = browser_agent.browse_and_extract(target_url, goal=topic)
            if not browser_res.get("success"):
                meta_event = {
                    "type": "meta",
                    "agent": self.name,
                    "task_type": "AUTONOMOUS_BROWSER_EXTRACTION",
                    "security_status": browser_res.get("security_status", "BLOCKED"),
                    "violation": browser_res.get("violation", "Security check failed"),
                    "tools_used": ["browser_agent", "ssrf_sentinel_guard"]
                }
                yield meta_event
                yield {"type": "token", "content": f"### 🛡️ Z Sentinel Security Interception\n\n**Navigation Blocked:** `{browser_res.get('violation')}`\n\nAxomAI Autonomous Browser Agent strictly enforces zero-trust network boundaries and rejected prohibited network traversal."}
                yield {"type": "done", "answer": browser_res.get("violation", "Blocked")}
                return

            tables = browser_res.get("tables", [])
            market_matrix = None
            if tables:
                first_tbl = tables[0]
                market_matrix = {
                    "title": f"Extracted Web Matrix from {target_url}",
                    "headers": first_tbl.get("headers", []),
                    "rows": first_tbl.get("rows", [])[:8]
                }

            sources = [
                {"title": p.get("title", target_url), "url": p.get("url", target_url), "domain": urlparse(target_url).netloc, "snippet": p.get("summary", "")}
                for p in browser_res.get("pages_summary", [])
            ]

            meta_event = {
                "type": "meta",
                "agent": self.name,
                "task_type": "AUTONOMOUS_BROWSER_EXTRACTION",
                "security_status": "Z_SENTINEL_VERIFIED_SAFE",
                "pages_visited": browser_res.get("pages_visited_count", 1),
                "hops_explored": browser_res.get("hops_explored", 0),
                "sources": sources,
                "market_matrix": market_matrix,
                "tools_used": ["browser_agent", "ssrf_sentinel_guard", "html_dom_parser"]
            }
            yield meta_event

            prompt = (
                f"You are Z2 Bravo Autonomous Browser Agent. The user instructed: '{topic}'.\n"
                f"Target Portal: {target_url}\n"
                f"Pages Explored: {browser_res.get('pages_visited_count')} | Hops: {browser_res.get('hops_explored')}\n"
                f"Extracted Tables Count: {len(tables)}\n"
                f"Summaries:\n" + "\n".join([f"- {p['title']} ({p['url']}): {p['summary']}" for p in browser_res.get("pages_summary", [])]) + "\n\n"
                "Synthesize a crisp, highly structured executive briefing of what was found on the portal, including the extracted tables and relevant next steps."
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate("You are Z2 Bravo Autonomous Browser Agent.", prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = f"### 🌐 Z2 Bravo Browser Exploration: {target_url}\n\n**Pages Visited:** {browser_res.get('pages_visited_count')} | **Hops:** {browser_res.get('hops_explored')}\n\nExtracted {len(tables)} data table(s) successfully with Z Sentinel zero-trust validation."
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # 2. Plan Research & Formulate Queries
        plan = self.router.plan_research(topic, has_active_document=bool(internal_doc_context))
        task_type = plan["task_type"]
        search_queries = plan["params"].get("search_queries", [topic])

        yield {
            "type": "status",
            "stage": "search_planning",
            "message": f"Formulated {len(search_queries)} research queries: {', '.join(search_queries[:2])}..."
        }

        # 3. Multi-Query Web Search
        raw_sources = web_search_engine.multi_query_search(search_queries, max_per_query=3)
        if not raw_sources:
            # Fallback direct search
            raw_sources = web_search_engine.search(topic, max_results=5)

        yield {
            "type": "status",
            "stage": "web_crawling",
            "message": f"Harvested {len(raw_sources)} authoritative sources across search indexes."
        }

        # 4. Deep Content Scraping
        target_urls = [s["url"] for s in raw_sources[:5]]
        scraped_pages = web_scraper_engine.scrape_batch(target_urls, max_pages=4)

        # Merge scraped full-text with search snippets
        verified_sources: List[Dict[str, Any]] = []
        evidence_blocks: List[str] = []

        for idx, src in enumerate(raw_sources[:8]):
            # Check if we have deeper scraped content for this source
            deeper = next((p for p in scraped_pages if p["url"] == src["url"]), None)
            text_body = deeper["text"] if deeper else src["snippet"]
            
            verified_sources.append({
                "source_id": idx + 1,
                "title": src["title"],
                "url": src["url"],
                "domain": src["domain"],
                "snippet": src["snippet"],
                "has_deep_content": bool(deeper)
            })

            evidence_blocks.append(
                f"[Source {idx+1}: {src['domain']} — {src['title']} ({src['url']})]:\n{text_body[:1800]}"
            )

        evidence_str = "\n\n---\n\n".join(evidence_blocks)

        yield {
            "type": "status",
            "stage": "synthesizing",
            "message": f"Deep reading & cross-verifying evidence across {len(verified_sources)} live sources..."
        }

        # 5. Extract Structured Market Matrix (if comparison / market benchmark)
        market_matrix = None
        is_matrix_eligible = (
            task_type in [ResearchTaskType.COMPETITOR_BENCHMARK, ResearchTaskType.MARKET_ANALYSIS]
            or any(w in topic.lower() for w in ["vs", "compare", "competitor", "matrix", "pricing", "market share"])
        )

        if is_matrix_eligible and llm_brain.is_available:
            try:
                matrix_sys = (
                    "You are a Senior Market Research Analyst. Extract a clean comparison matrix from the provided web research.\n"
                    "Output JSON only with keys:\n"
                    "{\n"
                    '  "title": "Competitor & Market Benchmark Matrix",\n'
                    '  "headers": ["Entity / Product", "Market Share / Volume", "Key Strengths", "Price / Range", "Weaknesses / Risks"],\n'
                    '  "rows": [["Ola Electric", "35%", "...", "...", "..."], ...]\n'
                    "}\n"
                    "If no clear comparative entities exist, output {}."
                )
                matrix_user = f"Topic: {topic}\n\nEvidence:\n{evidence_str[:3000]}\n\nExtract JSON matrix:"
                raw_mat = llm_brain.generate(matrix_sys, matrix_user, temperature=0.1)
                clean_mat = raw_mat.strip()
                if "```json" in clean_mat:
                    clean_mat = clean_mat.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_mat:
                    clean_mat = clean_mat.split("```")[1].split("```")[0].strip()
                parsed_mat = json.loads(clean_mat)
                if parsed_mat.get("headers") and parsed_mat.get("rows"):
                    market_matrix = parsed_mat
                    tools_used.append("market_matrix_extractor")
            except Exception:
                pass

        # Phase 1: Multi-Hop Autonomous Recursive Search & Fact Verification
        yield {
            "type": "status",
            "stage": "multi_hop_verification",
            "message": "Phase 1: Multi-Hop Recursive Verification & Authority Consensus check..."
        }
        verification_audit = multi_hop_engine.verify_recursively(topic, verified_sources, evidence_str)
        tools_used.append("multi_hop_engine")

        # Phase 2: Autonomous Competitor Radar & Live Price/Feature Tracker
        radar_data = radar_engine.scan_for_radar_updates(topic, evidence_str)
        if radar_data:
            tools_used.append("radar_engine")

        # Phase 3: Interactive 2x2 Strategic Quadrant Matrix (Price vs Performance)
        quadrant_data = quadrant_engine.generate_quadrant_matrix(topic, market_matrix, evidence_str)
        quadrant_chart = None
        if quadrant_data:
            tools_used.append("quadrant_engine")
            quadrant_chart = quadrant_data.get("chart_config")

        # Phase 4: Consumer Sentiment & Social Pulse Decomposition
        sentiment_pulse = sentiment_engine.analyze_sentiment_pulse(topic, evidence_str)
        if sentiment_pulse:
            tools_used.append("sentiment_engine")

        # Phase 5: Corporate Filings & Audited Financials Extractor
        filings_data = filings_engine.extract_audited_financials(topic, evidence_str)
        if filings_data:
            tools_used.append("filings_engine")

        # Phase 6: Hyper-Local & Regional Language Crawling (Assam & North-East)
        regional_data = regional_crawler.crawl_regional_intelligence(topic)
        if regional_data:
            tools_used.append("regional_crawler")

        # 6. Synthesize Grounded Research Intelligence
        today_date = datetime.now().strftime("%B %d, %Y")
        system_prompt = (
            f"You are Z2 Bravo, the Autonomous Deep Web & Market Research Agent developed by AxomAI AGI.\n"
            f"Current Real-World Date: {today_date}.\n"
            "Your mission: Deliver authoritative, meticulously verified, and high-value research intelligence strictly based on the provided live web evidence.\n\n"
            "CRITICAL PROTOCOLS:\n"
            f"1. TEMPORAL ACCURACY: Today's real-world date is {today_date}. When the user asks about 'today' or current market movements (up/down, closing, indices), report the latest live figures from the search results with their dates. NEVER refer to past years (like 2024) as 'today'. If today's market is currently closed or it is a weekend, clarify the latest trading session figures.\n"
            "2. Grounding & Citations: Every key claim, number, statistic, or fact MUST cite the source using badges like `[Source: domain.com](URL)` or `[Source 1: domain.com]`.\n"
            "3. Structure:\n"
            "   - ## 🌐 Executive Market Briefing (High-level 2-3 paragraph synthesis)\n"
            "   - ## 📊 Key Strategic Insights & Findings (Bullet points with bold metrics)\n"
            "   - ## ⚖️ Market Comparison & Competitive Dynamics (Detailed breakdown)\n"
            "   - ## 💡 Strategic Implications & Takeaways (Actionable conclusions)\n"
            "4. If an internal document context is provided, actively cross-compare internal data against external market realities.\n"
            "5. Match the user's language (English, Hindi, or Hinglish) naturally."
        )

        user_prompt = (
            f"RESEARCH TOPIC: {topic}\n"
            f"DETECTED TASK: {task_type}\n"
            f"{f'ACTIVE INTERNAL DOCUMENT: {active_doc_name}' if active_doc_name else ''}\n"
            f"{internal_doc_context}\n\n"
            f"LIVE VERIFIED WEB EVIDENCE ({len(verified_sources)} Sources):\n"
            f"{evidence_str}\n\n"
            f"Provide your authoritative, grounded Deep Web Research Report:"
        )

        full_answer = ""
        tools_used.append(f"openai_{llm_brain.model_name}")

        # Check if user requested an Executive Dossier PDF/Word file
        generated_dossier = None
        is_dossier_requested = (
            task_type == ResearchTaskType.DOSSIER_EXPORT
            or any(w in topic.lower() for w in ["dossier", "pdf", "word", "download", "export report", "bana kar do"])
        )

        # 7. Generate reasoning text
        if llm_brain.is_available:
            try:
                full_answer = llm_brain.generate(system_prompt, user_prompt, temperature=0.2)
            except Exception as e:
                full_answer = f"Research synthesis error: {e}\n\nTop sources gathered:\n" + "\n".join([f"- [{s['title']}]({s['url']})" for s in verified_sources[:4]])
        else:
            full_answer = "### Top Verified Live Web Sources:\n\n" + "\n".join([f"- **{s['domain']}**: [{s['title']}]({s['url']})\n  {s['snippet']}" for s in verified_sources])

        # If dossier requested, generate the PDF
        if is_dossier_requested and full_answer:
            summary_snippet = full_answer[:600]
            dossier_res = dossier_generator_engine.generate_dossier_pdf(
                topic=topic,
                summary=summary_snippet,
                detailed_findings=full_answer,
                sources=verified_sources,
                market_matrix=market_matrix
            )
            if dossier_res.get("success"):
                generated_dossier = dossier_res
                tools_used.append("dossier_generator_engine")

        # Phase 7: Executive Audio Podcast & Briefing Engine
        podcast_data = podcast_engine.generate_podcast_briefing(topic, full_answer, evidence_str)
        if podcast_data:
            tools_used.append("podcast_engine")

        # 8. Yield Meta event
        yield {
            "type": "meta",
            "agent": self.name,
            "task_type": task_type,
            "tools_used": tools_used,
            "sources": verified_sources,
            "market_matrix": market_matrix,
            "chart": quadrant_chart,
            "generated_file": generated_dossier,
            "verification_audit": verification_audit,
            "radar_data": radar_data,
            "quadrant_data": quadrant_data,
            "sentiment_pulse": sentiment_pulse,
            "filings_data": filings_data,
            "regional_data": regional_data,
            "podcast_data": podcast_data
        }

        # 9. Stream answer tokens with typewriter effect
        words = full_answer.split(" ")
        for i in range(0, len(words), 3):
            chunk = " ".join(words[i:i+3]) + (" " if i+3 < len(words) else "")
            yield {
                "type": "token",
                "content": chunk
            }

        # 10. Yield Done event
        yield {
            "type": "done",
            "answer": full_answer
        }

        # 11. Log Interaction in PostgreSQL
        try:
            with SyncSessionLocal() as db:
                session = db.query(AgentSession).filter(AgentSession.id == session_id).first()
                if not session:
                    session = AgentSession(id=session_id, agent_name=self.name)
                    db.add(session)
                    db.flush()

                task_log = AgentTaskLog(
                    session_id=session.id,
                    document_id=uuid.UUID(doc_id) if doc_id else None,
                    user_query=topic,
                    task_type=str(task_type),
                    tools_used=tools_used,
                    evidence=[{"title": s["title"], "url": s["url"], "domain": s["domain"]} for s in verified_sources],
                    response=full_answer
                )
                db.add(task_log)
                db.commit()
        except Exception:
            pass


z2_bravo_agent = Z2BravoAgent()

