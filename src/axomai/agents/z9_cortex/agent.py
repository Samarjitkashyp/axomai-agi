"""
Z9 Cortex - Collective Long-Term Memory & Knowledge Graph Agent.
Manages persistent episodic memory, entity-relationship graphs (NetworkX),
and detects strategic contradictions with historical corporate policy.
"""

from typing import Dict, Any, Generator, Optional
from axomai.core.llm import llm_brain
from axomai.agents.z9_cortex.tools.knowledge_graph import knowledge_graph
from axomai.agents.z9_cortex.tools.memory_store import memory_store
from axomai.agents.z9_cortex.tools.contradiction_detector import contradiction_detector

class Z9CortexAgent:
    """Enterprise Knowledge Graph & Long-Term Memory Custodian."""

    def __init__(self):
        self.name = "Z9 Cortex"
        self.role = "Collective Long-Term Memory & Knowledge Graph Agent"

    def memory_stream(
        self,
        query: str,
        session_id: Optional[str] = "cortex_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        q_lower = query.lower()

        # Check if user is storing a new memory
        if any(k in q_lower for k in ["remember that", "store in memory", "remember this", "save note that"]):
            yield {
                "type": "status",
                "stage": "store_memory",
                "message": "🧠 Z9 Cortex: Committing directive to permanent enterprise memory store..."
            }
            cleaned_fact = query
            for prefix in ["remember that", "store in memory", "remember this", "save note that"]:
                cleaned_fact = cleaned_fact.replace(prefix, "").strip()

            new_mem = memory_store.store_memory(cleaned_fact, category="Executive Decision")
            meta_event = {
                "type": "meta",
                "agent": self.name,
                "task_type": "MEMORY_STORED",
                "new_memory": new_mem,
                "tools_used": ["memory_store"]
            }
            yield meta_event

            ans = (
                f"### 🧠 Z9 Cortex: Permanent Memory Stored\n\n"
                f"- **Memory ID:** `{new_mem['memory_id']}`\n"
                f"- **Category:** `{new_mem['category']}`\n"
                f"- **Recorded Fact:** \"{new_mem['content']}\"\n"
                f"- **Timestamp:** `{new_mem['recorded_at']}`\n\n"
                "> This fact is now indexed in AxomAI AGI's permanent knowledge base and will be used to guide future reasoning and conflict checks across all agents."
            )
            for tok in ans.split(" "):
                yield {"type": "token", "content": tok + " "}
            yield {"type": "done", "answer": ans}
            return

        # Query Knowledge Graph & Episodic Recall
        yield {
            "type": "status",
            "stage": "traverse_graph",
            "message": "🧠 Z9 Cortex: Traversing semantic graph & retrieving cross-session memories..."
        }

        subgraph = knowledge_graph.query_subgraph(query)
        memories = memory_store.recall(query)
        conflict_res = contradiction_detector.detect_conflicts(query)

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "KNOWLEDGE_GRAPH_RECALL",
            "subgraph": subgraph,
            "memories": memories,
            "conflict_analysis": conflict_res,
            "tools_used": ["knowledge_graph", "memory_store", "contradiction_detector", "networkx"]
        }
        yield meta_event

        prompt = (
            f"You are Z9 Cortex, Collective Long-Term Memory & Knowledge Graph Custodian.\n"
            f"User Query: '{query}'\n\n"
            f"Connected Knowledge Graph Triplets ({len(subgraph.get('relationships', []))}):\n"
            f"{str(subgraph.get('relationships'))}\n\n"
            f"Recalled Corporate Memories ({len(memories)}):\n"
            f"{str(memories)}\n\n"
            f"Policy Conflict Assessment:\n{str(conflict_res)}\n\n"
            "Produce an executive memory & knowledge briefing in GitHub Markdown:\n"
            "1. 🧠 Enterprise Knowledge Graph Network (Entity-Relationship connections)\n"
            "2. 📜 Recalled Historical Directives & Decisions\n"
            "3. ⚠️ Policy & Strategic Consistency Verdict (Flag any conflicts if present)"
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z9 Cortex.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = f"### 🧠 Z9 Cortex Knowledge Graph\n\n**Connected Entities:** {len(subgraph.get('relationships', []))}\n**Recalled Memories:** {len(memories)}"
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": full_answer}

z9_cortex_agent = Z9CortexAgent()

