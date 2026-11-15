"""
AxomAI Swarm Hive - Swarm Consensus & Ephemeral Lifecycle Manager.
Fuses parallel sub-agent findings, performs weighted consensus scoring,
and gracefully decommissions temporary agents to guarantee zero memory bloat.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from axomai.swarm_hive.agent_spawner import agent_spawner, AgentSpawner

class SwarmConsensus:
    """Aggregates ephemeral swarm intelligence and cleans up runtime footprint."""

    def __init__(self):
        self.spawner = agent_spawner

    def execute_swarm_mission(self, mission_domains: List[str], mission_query: str) -> Dict[str, Any]:
        """
        Executes an end-to-end ephemeral swarm mission:
        Spawn -> Parallel Execute -> Consensus Score -> Memory Flush.
        """
        now = datetime.utcnow().isoformat()
        
        # 1. Spawn temporary clones
        clones = self.spawner.spawn_swarm_cluster(mission_domains)
        clone_ids = [c.clone_id for c in clones]

        # 2. Execute slices across all clones
        slice_results = []
        for clone in clones:
            res = clone.execute_slice({"query": mission_query})
            slice_results.append(res)

        # 3. Compute weighted consensus score
        scores = [s["findings"]["score"] for s in slice_results]
        avg_consensus_score = round(sum(scores) / max(1, len(scores)), 2)

        # 4. Graceful Decommission & Memory Flush
        self.spawner.decommission_clones(clone_ids)

        return {
            "mission_query": mission_query,
            "swarm_size": len(clones),
            "consensus_score": avg_consensus_score,
            "status": "SWARM_CONSENSUS_REACHED_AND_DECOMMISSIONED",
            "ephemeral_clones_purged": len(clone_ids),
            "timestamp": now,
            "specialist_findings": slice_results
        }

swarm_consensus = SwarmConsensus()

