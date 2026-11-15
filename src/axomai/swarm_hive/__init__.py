"""
AxomAI Swarm Hive package.
Provides ephemeral agent spawner, swarm consensus, and micro-swarm commander.
"""

from axomai.swarm_hive.agent_spawner import agent_spawner, AgentSpawner, EphemeralSubAgent
from axomai.swarm_hive.swarm_consensus import swarm_consensus, SwarmConsensus
from axomai.swarm_hive.micro_swarm_commander import micro_swarm_commander, MicroSwarmCommander

__all__ = [
    "agent_spawner",
    "AgentSpawner",
    "EphemeralSubAgent",
    "swarm_consensus",
    "SwarmConsensus",
    "micro_swarm_commander",
    "MicroSwarmCommander"
]
