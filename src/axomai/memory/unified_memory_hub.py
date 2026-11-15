"""
AxomAI Unified Cognitive Memory Hub.
Central orchestrator for all 4 cognitive memory tiers:
- Tier 1: Working Memory (Live context & Scratchpad)
- Tier 2: Episodic Memory (Experiences, Mistakes & Reflexion Lessons)
- Tier 3: Semantic Graph Memory (Entities, Facts & Relational Triples)
- Tier 4: Procedural Memory (Autonomous Skills & Algorithmic Registry)
"""

from typing import Dict, Any, List, Optional
from axomai.memory.working_memory import working_memory, WorkingMemory
from axomai.memory.episodic_memory import episodic_memory, EpisodicMemory
from axomai.memory.semantic_graph_memory import semantic_graph_memory, SemanticGraphMemory
from axomai.memory.procedural_memory import procedural_memory, ProceduralMemory

class UnifiedMemoryHub:
    """The central multi-tier brain facade of AxomAI AGI."""

    def __init__(self):
        self.working = working_memory
        self.episodic = episodic_memory
        self.semantic = semantic_graph_memory
        self.procedural = procedural_memory

    def synthesize_cognitive_brief(self, query: str) -> Dict[str, Any]:
        """
        Synthesizes a 360-degree cognitive memory brief for any incoming query:
        1. Checks episodic memory for past lessons & mistake warnings.
        2. Queries semantic graph for related domain entities & triples.
        3. Looks up relevant procedural skills.
        4. Gathers active working memory scratchpad.
        """
        # 1. Past experiences & mistake avoidance
        lessons = self.episodic.recall_relevant_lessons(query=query, top_k=3)
        
        # 2. Semantic facts & relations
        keywords = [w for w in query.split() if len(w) > 3][:4]
        semantic_facts = []
        for kw in keywords:
            facts = self.semantic.search_knowledge(kw, limit=2)
            for f in facts:
                if f not in semantic_facts:
                    semantic_facts.append(f)

        # 3. Procedural skills available
        available_skills = self.procedural.list_skills()

        # 4. Working memory snapshot
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
        """
        Consolidates an execution into long-term brain memory:
        1. Records episodic memory.
        2. Ingests any newly discovered factual triples into semantic graph.
        """
        # 1. Episodic
        ep_res = self.episodic.record_episode(
            query=query,
            agent_id=agent_id,
            outcome_status=outcome_status,
            reward_score=reward_score,
            reflection=reflection,
            lesson_learned=lesson_learned,
            metadata=metadata
        )

        # 2. Semantic facts ingestion
        ingested_facts = 0
        if new_facts:
            for fact in new_facts:
                if len(fact) >= 3:
                    s, p, o = fact[0], fact[1], fact[2]
                    conf = fact[3] if len(fact) > 3 else 1.0
                    self.semantic.add_fact(s, p, o, confidence=conf, source_ref=f"Agent {agent_id.upper()} Reflection")
                    ingested_facts += 1

        return {
            "status": "CONSOLIDATED",
            "episode_id": ep_res["episode_id"],
            "reward_score": reward_score,
            "facts_ingested": ingested_facts
        }

    def get_memory_telemetry(self) -> Dict[str, Any]:
        """Returns fleet-wide cognitive memory metrics."""
        ep_stats = self.episodic.get_stats()
        sem_stats = self.semantic.get_stats()
        skills = self.procedural.list_skills()
        working_snap = self.working.get_context_snapshot()

        return {
            "status": "OPTIMAL_COGNITION",
            "tiers": {
                "working_memory": {
                    "buffer_depth": working_snap["buffer_depth"],
                    "cognitive_load": working_snap["cognitive_load_score"]
                },
                "episodic_memory": ep_stats,
                "semantic_graph": sem_stats,
                "procedural_memory": {
                    "total_registered_skills": len(skills),
                    "active_skills": [s["skill_name"] for s in skills]
                }
            }
        }

unified_memory_hub = UnifiedMemoryHub()

