"""
AxomAI Unified Hyper-Memory Hub.
Central orchestrator for the Sovereign 5-Tier Cognitive Memory Architecture:
- Tier 1: Working Memory (Live Attention & Scratchpad)
- Tier 2: Session Context Memory (Up to 100k tokens per session with ChatGPT-style redirection)
- Tier 3: 4D Temporal Knowledge Graph (Entities, Functional Relations, Contradiction Resolution & Autonomous Ingestion)
- Tier 4: Autobiographical Episodic Memory (Experiences, Mistake Avoidance & Reflexion Lessons)
- Tier 5: Subconscious Sleep & Consolidation Engine (Cross-Session User Persona Twin & Epistemic Abstraction)
- Procedural Memory (Reusable Operational Skills & Action Vault)
"""

import threading
from typing import Dict, Any, List, Optional
from axomai.memory.working_memory import working_memory, WorkingMemory
from axomai.memory.session_memory import session_conversation_memory, SessionConversationMemory
from axomai.memory.semantic_graph_memory import semantic_graph_memory, SemanticGraphMemory
from axomai.memory.episodic_memory import episodic_memory, EpisodicMemory
from axomai.memory.procedural_memory import procedural_memory, ProceduralMemory
from axomai.memory.subconscious_consolidation import subconscious_consolidation, SubconsciousConsolidationDaemon

class UnifiedHyperMemoryHub:
    """The Sovereign Multi-Tier Cognitive Memory Brain of AxomAI AGI."""

    def __init__(self):
        self.working = working_memory
        self.session = session_conversation_memory
        self.semantic = semantic_graph_memory
        self.episodic = episodic_memory
        self.procedural = procedural_memory
        self.subconscious = subconscious_consolidation
        self._turn_counter: int = 0
        self._lock = threading.Lock()

    def synthesize_hyper_memory_context(self, query: str, session_id: str) -> Dict[str, Any]:
        """
        Synthesizes a full 5-tier cognitive memory briefing for the incoming query:
        1. Tier 1 & 2: Active session turns and topic dossier (up to 100k context).
        2. Tier 3: 4D Temporal Knowledge Graph matching entities & functional relations.
        3. Tier 4: Autobiographical episodic lessons and mistake warnings.
        4. Tier 5: Subconscious User Persona Twin with cross-session active projects.
        """
        # 1. Active Session Context (Tier 2)
        sess_ctx = self.session.get_conversation_context(session_id, query)
        session_prompt = sess_ctx.get("context_prompt", "")

        # 2. 4D Temporal Knowledge Graph (Tier 3)
        words = [w.strip(",.?!\"'") for w in query.split() if len(w) > 3]
        active_facts: List[Dict[str, Any]] = []
        for w in words[:6]:
            found_facts = self.semantic.search_knowledge(w, limit=2, active_only=True)
            for f in found_facts:
                if f not in active_facts:
                    active_facts.append(f)

        graph_block = ""
        if active_facts:
            graph_lines = [
                f"  - ({f['subject_name']}) ──[{f['predicate']}]──▶ ({f['object_name']}) [Status: {f.get('epistemic_status', 'ACTIVE')}]"
                for f in active_facts[:6]
            ]
            graph_block = (
                "=== 🌐 [4D TEMPORAL KNOWLEDGE GRAPH FACTS] ===\n" +
                "\n".join(graph_lines) + "\n"
            )

        # 3. Episodic Memory Lessons (Tier 4)
        lessons = self.episodic.recall_relevant_lessons(query=query, top_k=2)
        episodic_block = ""
        if lessons:
            lesson_lines = [
                f"  * [Caution/Guidance]: {l['lesson_learned']} (Prior Outcome: {l['outcome_status']})"
                for l in lessons
            ]
            episodic_block = (
                "=== 🛡️ [AUTOBIOGRAPHICAL LESSONS & MISTAKE AVOIDANCE] ===\n" +
                "\n".join(lesson_lines) + "\n"
            )

        # 4. Subconscious User Persona Twin (Tier 5)
        persona_block = self.subconscious.format_persona_prompt_block()

        # Integrate into a single coherent prompt section
        sections = [persona_block]
        if graph_block:
            sections.append(graph_block)
        if episodic_block:
            sections.append(episodic_block)
        if session_prompt:
            sections.append(session_prompt)

        combined_hyper_prompt = "\n".join(sections)

        return {
            "query": query,
            "session_id": session_id,
            "hyper_prompt": combined_hyper_prompt,
            "facts_retrieved_count": len(active_facts),
            "lessons_retrieved_count": len(lessons),
            "active_facts": active_facts,
            "lessons": lessons
        }

    def auto_ingest_turn(
        self,
        session_id: str,
        role: str,
        content: str,
        agent_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Real-time cognitive ingestion across all 5 tiers:
        1. Records turn in SessionConversationMemory (Tier 2).
        2. Updates Working Memory attention buffer (Tier 1).
        3. Extracts and ingests triples into 4D Temporal Knowledge Graph (Tier 3).
        4. Periodically triggers subconscious consolidation (Tier 5).
        """
        if not content:
            return {"status": "EMPTY"}

        # 1. Session Memory Record
        self.session.record_turn(
            session_id=session_id,
            role=role,
            content=content,
            agent_name=agent_name
        )

        # 2. Working Memory Turn
        try:
            self.working.push_turn(role=role, content=content, agent_id=agent_name)
        except Exception:
            pass

        # 3. 4D Temporal Knowledge Graph Extraction
        extracted_triples = []
        try:
            extracted_triples = self.semantic.extract_and_ingest_triples_from_text(
                text=content,
                session_id=session_id
            )
        except Exception:
            pass

        # 4. Periodic Subconscious Sleep Consolidation (every 12 turns)
        with self._lock:
            self._turn_counter += 1
            if self._turn_counter % 12 == 0:
                try:
                    threading.Thread(
                        target=self.subconscious.run_consolidation_cycle,
                        kwargs={"idle_mode": True},
                        daemon=True
                    ).start()
                except Exception:
                    pass

        return {
            "status": "INGESTED",
            "session_id": session_id,
            "role": role,
            "extracted_triples": len(extracted_triples)
        }

    def trigger_subconscious_sleep(self, idle_mode: bool = False) -> Dict[str, Any]:
        """Forces an immediate subconscious consolidation cycle."""
        return self.subconscious.run_consolidation_cycle(idle_mode=idle_mode)

    def synthesize_cognitive_brief(self, query: str) -> Dict[str, Any]:
        """Legacy-compatible 360 brief for memory telemetry tools."""
        lessons = self.episodic.recall_relevant_lessons(query=query, top_k=3)
        keywords = [w for w in query.split() if len(w) > 3][:4]
        semantic_facts = []
        for kw in keywords:
            facts = self.semantic.search_knowledge(kw, limit=2)
            for f in facts:
                if f not in semantic_facts:
                    semantic_facts.append(f)

        available_skills = self.procedural.list_skills()
        working_snapshot = self.working.get_context_snapshot()

        return {
            "query": query,
            "episodic_guidance": [
                {
                    "lesson": l["lesson_learned"],
                    "past_outcome": l["outcome_status"],
                    "reward": l["reward_score"],
                    "relevance": l["similarity"]
                }
                for l in lessons
            ],
            "semantic_grounding": semantic_facts[:5],
            "procedural_skills_available": len(available_skills),
            "cognitive_load": working_snapshot["cognitive_load_score"]
        }

    def consolidate_experience(
        self,
        query: str,
        agent_id: str,
        outcome_status: str,
        reward_score: float,
        reflection: str,
        lesson_learned: str,
        new_facts: Optional[List[tuple]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Legacy-compatible execution experience consolidation."""
        ep_res = self.episodic.record_episode(
            query=query,
            agent_id=agent_id,
            outcome_status=outcome_status,
            reward_score=reward_score,
            reflection=reflection,
            lesson_learned=lesson_learned,
            metadata=metadata
        )

        ingested_facts = 0
        if new_facts:
            for fact in new_facts:
                if len(fact) >= 3:
                    s, p, o = fact[0], fact[1], fact[2]
                    conf = fact[3] if len(fact) > 3 else 1.0
                    self.semantic.add_temporal_fact(
                        subject=s,
                        predicate=p,
                        obj=o,
                        confidence=conf,
                        source_ref=f"Agent {agent_id.upper()} Reflection"
                    )
                    ingested_facts += 1

        return {
            "status": "CONSOLIDATED",
            "episode_id": ep_res["episode_id"],
            "reward_score": reward_score,
            "facts_ingested": ingested_facts
        }

    def get_memory_telemetry(self) -> Dict[str, Any]:
        """Returns 5-tier sovereign cognitive memory metrics."""
        ep_stats = self.episodic.get_stats()
        sem_stats = self.semantic.get_stats()
        skills = self.procedural.list_skills()
        working_snap = self.working.get_context_snapshot()
        twin = self.subconscious.get_persona_twin()

        return {
            "status": "SOVEREIGN_5TIER_HYPER_MEMORY_ACTIVE",
            "tiers": {
                "tier_1_working_memory": {
                    "buffer_depth": working_snap["buffer_depth"],
                    "cognitive_load": working_snap["cognitive_load_score"]
                },
                "tier_2_session_conversations": {
                    "total_sessions_on_disk": twin.total_sessions_stitched,
                    "max_token_ceiling": 100_000
                },
                "tier_3_temporal_knowledge_graph": sem_stats,
                "tier_4_episodic_memory": ep_stats,
                "tier_5_subconscious_consolidation": {
                    "user_title": twin.user_title,
                    "active_projects": len(twin.active_projects),
                    "abstracted_axioms": len(twin.abstracted_axioms),
                    "last_consolidated": twin.last_consolidated_at
                },
                "procedural_memory": {
                    "total_registered_skills": len(skills),
                    "active_skills": [s["skill_name"] for s in skills]
                }
            }
        }

unified_memory_hub = UnifiedHyperMemoryHub()
UnifiedMemoryHub = UnifiedHyperMemoryHub
