"""
AxomAI Supervision Engine package.
Provides active circuit breakers, agent watchdog anomaly detection, and capability token guard.
"""

from axomai.supervision.circuit_breaker import CircuitBreaker, circuit_breaker
from axomai.supervision.agent_watchdog import AgentWatchdog, agent_watchdog
from axomai.supervision.capability_guard import Capability, CapabilityToken, CapabilityGuard, capability_guard

__all__ = [
    "CircuitBreaker",
    "circuit_breaker",
    "AgentWatchdog",
    "agent_watchdog",
    "Capability",
    "CapabilityToken",
    "CapabilityGuard",
    "capability_guard"
]
