"""
Mission Control - Autonomous Goal Decomposition & Strategic Planner.
Analyzes broad executive goals and decomposes them into an optimal
multi-agent execution graph across specialized AxomAI agents.
"""

import json
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from axomai.core.llm import llm_brain

class MissionMilestone(BaseModel):
    step_id: int
    title: str
    target_agent: str # "z1", "z2", "z3", "z4", "z5", "z6", "z7", "z8", "z9"
    agent_name: str
    objective: str
    prompt: str
    deliverable_type: str

class MissionPlan(BaseModel):
    mission_id: str
    title: str
    strategic_objective: str
    total_steps: int
    milestones: List[MissionMilestone]

AGENT_NAME_MAP = {
    "z1": "Z1 Alpha (File & Vision Intelligence)",
    "z2": "Z2 Bravo (Live Web & Market Research)",
    "z3": "Z3 Echo (SQL Analytics & Financial Forecasting)",
    "z4": "Z4 Nexus (Secure Code Sandbox & API Engine)",
    "z5": "Z5 Chronos (Task Scheduler & Autonomous Briefings)",
    "z6": "Z6 Hermes (Omnichannel & Executive Communications)",
    "z7": "Z7 Visionary (PowerPoint & Generative UI Architecture)",
    "z8": "Z8 Apex (Legal Contracts & Statutory Compliance)",
    "z9": "Z9 Cortex (Knowledge Graph & Episodic Memory)",
    "z10": "Z10 Matrix (Logistics & Fleet Optimization)",
    "z11": "Z11 Pragati (Public Policy, Statutory Incentives & Sovereign Governance)",
    "z12": "Z12 Athena (Talent & Workforce Strategy)",
    "z13": "Z13 Quantum (Market Surveillance & Dynamic Pricing)",
    "z14": "Z14 Horizon (Global Cross-Border Trade & FX)",
    "z15": "Z15 Sovereign (Global Cyber Defense & Threat Intel)",
    "z16": "Z16 Omni (Global Geospatial & Satellite Vision)",
    "z17": "Z17 Apex-Global (Wall Street & Private Equity Valuation)",
    "y1": "Y1 Annapurna (Agri-Science & Commodity Futures)",
    "y2": "Y2 Urja (Green Energy & Carbon Credits)",
    "y3": "Y3 Sanjeevani (Sovereign Healthcare & Cold-Chain)",
    "y4": "Y4 Vishwakarma (Mega Infrastructure & EPC Civil)",
    "y5": "Y5 Chanakya (Sovereign Geopolitics & OSINT)",
}

class MissionPlanner:
    """Decomposes complex, high-level business goals into structured multi-agent workflows."""

    def plan_mission(self, user_goal: str, doc_id: Optional[str] = None) -> MissionPlan:
        mission_id = str(uuid.uuid4())[:8]
        g_lower = user_goal.lower()

        # FAST PATH: High-Speed Instant Domain Recognition (<5ms) for Commercial Expansion & Business Strategy
        if any(k in g_lower for k in ["retail", "branch", "outlet", "store", "district", "expansion", "market entry"]) and any(k in g_lower for k in ["plan", "top 3", "strategy", "open", "kholne", "launch"]):
            return MissionPlan(
                mission_id=mission_id,
                title="Global Commercial Branch & Market Expansion Master Plan",
                strategic_objective="Formulate an end-to-end 360-degree commercial expansion strategy across target markets with market teardown, predictive unit economics, statutory compliance, and executive boardroom deck.",
                total_steps=4,
                milestones=[
                    MissionMilestone(
                        step_id=1,
                        title="Target Market Demographics, Footfall & Competitor Teardown",
                        target_agent="z2",
                        agent_name=AGENT_NAME_MAP["z2"],
                        objective="Identify and benchmark high-yield commercial hubs in target markets covering purchasing power, footfall density, and competitor presence.",
                        prompt=f"Perform deep market research on target commercial districts and markets for commercial expansion: analyze consumer demographics, retail density, purchasing power parity, and key commercial competitor dynamics: {user_goal}",
                        deliverable_type="MARKET_INTELLIGENCE"
                    ),
                    MissionMilestone(
                        step_id=2,
                        title="Financial Modeling, Capex & 12-Month Trajectory",
                        target_agent="z3",
                        agent_name=AGENT_NAME_MAP["z3"],
                        objective="Compute initial capex, recurring opex, monthly revenue trajectory, and break-even horizon per branch.",
                        prompt=f"Model the financial viability and forecasting for commercial branch expansion: estimate unit capex, monthly sales trajectory with R² confidence score, and projected break-even timeline: {user_goal}",
                        deliverable_type="FINANCIAL_PROJECTIONS"
                    ),
                    MissionMilestone(
                        step_id=3,
                        title="Statutory Licensing, Lease Safeguards & Regulatory Audit",
                        target_agent="z8",
                        agent_name=AGENT_NAME_MAP["z8"],
                        objective="Audit applicable commercial licensing, municipal trade authorizations, fire safety NOC, commercial lease lock-in clauses, and data protection compliance.",
                        prompt=f"Conduct comprehensive statutory legal and compliance audit for commercial branches in target jurisdictions: review applicable commercial licensing, municipal trade registration, tax registration, commercial lease indemnity clauses, and statutory privacy/data protection compliance. Output clean Markdown with well-formatted tables: {user_goal}",
                        deliverable_type="LEGAL_COMPLIANCE_AUDIT"
                    ),
                    MissionMilestone(
                        step_id=4,
                        title="Executive Boardroom Presentation Deck (.pptx)",
                        target_agent="z7",
                        agent_name=AGENT_NAME_MAP["z7"],
                        objective="Synthesize master strategic brief and generate downloadable 16:9 widescreen PowerPoint deck.",
                        prompt=f"Generate an executive presentation deck (.pptx) titled 'Commercial Branch Expansion Plan' summarizing the selected commercial markets, financial projections, statutory checklist, and roadmap: {user_goal}",
                        deliverable_type="EXECUTIVE_PRESENTATION_DECK"
                    )
                ]
            )

        # Check if LLM is available for intelligent dynamic decomposition
        if llm_brain.is_available:
            try:
                system_prompt = (
                    "You are the AxomAI AGI Mission Control Chief Architect.\n"
                    "Your objective is to decompose an ambitious enterprise business goal into a 3 to 4 step "
                    "multi-agent execution roadmap.\n\n"
                    "Available Agents:\n"
                    "- z1: File/Document extraction, contract reading, OCR, multi-doc analysis.\n"
                    "- z2: Live web research, competitor benchmarks, current 2024-2025 market trends.\n"
                    "- z3: Database SQL querying, sales analysis, financial modeling, trajectory forecasting.\n"
                    "- z4: Python data processing, custom sandbox calculations, API integrations.\n"
                    "- z7: PowerPoint deck generation, visual executive summaries, interactive widgets.\n"
                    "- z8: Legal contracts, DPDP statutory compliance, risk mitigation agreements.\n"
                    "- z9: Knowledge graph mapping, organizational episodic memory.\n\n"
                    "Return ONLY valid JSON matching this exact structure:\n"
                    "{\n"
                    '  "title": "Short Project Title",\n'
                    '  "strategic_objective": "1-sentence executive objective",\n'
                    '  "milestones": [\n'
                    '    {\n'
                    '      "step_id": 1,\n'
                    '      "title": "Milestone title",\n'
                    '      "target_agent": "z2",\n'
                    '      "objective": "What this step achieves",\n'
                    '      "prompt": "Specific instruction for this agent",\n'
                    '      "deliverable_type": "MARKET_INTELLIGENCE"\n'
                    '    }\n'
                    '  ]\n'
                    "}"
                )
                
                resp = llm_brain.generate(system_prompt, f"User Goal: {user_goal}", temperature=0.2)
                clean_json = resp.strip()
                if "```json" in clean_json:
                    clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_json:
                    clean_json = clean_json.split("```")[1].split("```")[0].strip()

                data = json.loads(clean_json)
                milestones = []
                for idx, m in enumerate(data.get("milestones", []), start=1):
                    agent_key = m.get("target_agent", "z2").lower()
                    if agent_key not in AGENT_NAME_MAP:
                        agent_key = "z2"
                    milestones.append(MissionMilestone(
                        step_id=idx,
                        title=m.get("title", f"Phase {idx}"),
                        target_agent=agent_key,
                        agent_name=AGENT_NAME_MAP.get(agent_key, "Z2 Bravo"),
                        objective=m.get("objective", "Execute strategic step"),
                        prompt=m.get("prompt", user_goal),
                        deliverable_type=m.get("deliverable_type", "ANALYTICS_DOSSIER")
                    ))

                if milestones:
                    return MissionPlan(
                        mission_id=mission_id,
                        title=data.get("title", "Autonomous Enterprise Mission"),
                        strategic_objective=data.get("strategic_objective", user_goal),
                        total_steps=len(milestones),
                        milestones=milestones
                    )
            except Exception as e:
                pass

        # Robust Fallback Deterministic Decomposition based on keywords
        milestones = []
        if any(k in g_lower for k in ["ev", "market", "competitor", "expansion", "growth", "strategy"]):
            milestones = [
                MissionMilestone(
                    step_id=1,
                    title="Live Market & Competitor Teardown",
                    target_agent="z2",
                    agent_name=AGENT_NAME_MAP["z2"],
                    objective="Scrape live market trends, competitor market share, and regional demand dynamics",
                    prompt=f"Perform live market intelligence and competitor analysis for: {user_goal}",
                    deliverable_type="MARKET_INTELLIGENCE"
                ),
                MissionMilestone(
                    step_id=2,
                    title="Financial Feasibility & Revenue Modeling",
                    target_agent="z3",
                    agent_name=AGENT_NAME_MAP["z3"],
                    objective="Query internal database benchmarks and compute 6-month predictive revenue trajectory",
                    prompt=f"Calculate revenue forecasting, financial sensitivity, and unit economics for: {user_goal}",
                    deliverable_type="FINANCIAL_PROJECTIONS"
                ),
                MissionMilestone(
                    step_id=3,
                    title="Statutory Compliance & Legal Risk Audit",
                    target_agent="z8",
                    agent_name=AGENT_NAME_MAP["z8"],
                    objective="Verify DPDP Act, regional state licensing, and contractual liability frameworks",
                    prompt=f"Audit statutory compliance and regulatory requirements for: {user_goal}",
                    deliverable_type="LEGAL_COMPLIANCE_AUDIT"
                ),
                MissionMilestone(
                    step_id=4,
                    title="Executive Deck & Strategic Presentation",
                    target_agent="z7",
                    agent_name=AGENT_NAME_MAP["z7"],
                    objective="Render 16:9 widescreen PowerPoint deck (.pptx) and executive board summary",
                    prompt=f"Generate executive PowerPoint presentation deck (.pptx) for: {user_goal}",
                    deliverable_type="POWERPOINT_PRESENTATION"
                )
            ]
            title = "Global Commercial & Market Expansion Strategic Mission"
        else:
            # General Enterprise Project Roadmap
            milestones = [
                MissionMilestone(
                    step_id=1,
                    title="Discovery & Landscape Intelligence",
                    target_agent="z2",
                    agent_name=AGENT_NAME_MAP["z2"],
                    objective="Gather real-time industry data, best practices, and external benchmarks",
                    prompt=f"Research industry landscape and actionable insights for: {user_goal}",
                    deliverable_type="MARKET_INTELLIGENCE"
                ),
                MissionMilestone(
                    step_id=2,
                    title="Data Analysis & Quantitative Validation",
                    target_agent="z3",
                    agent_name=AGENT_NAME_MAP["z3"],
                    objective="Model baseline metrics and forecast operational outcomes",
                    prompt=f"Analyze data metrics and project trajectory for: {user_goal}",
                    deliverable_type="ANALYTICS_DOSSIER"
                ),
                MissionMilestone(
                    step_id=3,
                    title="Governance, Risk & Compliance Check",
                    target_agent="z8",
                    agent_name=AGENT_NAME_MAP["z8"],
                    objective="Evaluate statutory risks, data safety, and enterprise guidelines",
                    prompt=f"Audit legal frameworks, liabilities and compliance for: {user_goal}",
                    deliverable_type="LEGAL_COMPLIANCE_AUDIT"
                ),
                MissionMilestone(
                    step_id=4,
                    title="Final Deliverable & Executive Deck",
                    target_agent="z7",
                    agent_name=AGENT_NAME_MAP["z7"],
                    objective="Synthesize master strategic brief and PowerPoint presentation deck",
                    prompt=f"Create executive briefing and presentation deck for: {user_goal}",
                    deliverable_type="POWERPOINT_PRESENTATION"
                )
            ]
            title = "Autonomous 360° Enterprise Execution Mission"

        return MissionPlan(
            mission_id=mission_id,
            title=title,
            strategic_objective=user_goal,
            total_steps=len(milestones),
            milestones=milestones
        )

mission_planner = MissionPlanner()

