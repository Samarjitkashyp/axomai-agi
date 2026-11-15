"""
AxomAI Supervision Engine package.
Provides active circuit breakers, agent watchdog, capability token guard,
Sovereign Governor with hierarchical kill-switch, and Sovereign Immunity Guard.
"""

from axomai.supervision.circuit_breaker import CircuitBreaker, circuit_breaker
from axomai.supervision.agent_watchdog import AgentWatchdog, agent_watchdog
from axomai.supervision.capability_guard import Capability, CapabilityToken, CapabilityGuard, capability_guard
from axomai.supervision.sovereign_governor import SovereignGovernor, sovereign_governor
from axomai.supervision.immunity_guard import ImmunityGuard, immunity_guard

__all__ = [
    "CircuitBreaker",
    "circuit_breaker",
    "AgentWatchdog",
    "agent_watchdog",
    "Capability",
    "CapabilityToken",
    "CapabilityGuard",
    "capability_guard",
    "SovereignGovernor",
    "sovereign_governor",
    "ImmunityGuard",
    "immunity_guard"
]
