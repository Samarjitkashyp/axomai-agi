"""
AxomAI Agency - Autonomous Web Operator package.
Provides autonomous browser navigation, form autofill, encrypted credential vault,
human-in-the-loop security gate protocol, and multi-tab web swarm coordinator.
"""

from axomai.agency.web_operator.credential_vault import SovereignCredentialVault, credential_vault
from axomai.agency.web_operator.security_gate_protocol import SecurityGateProtocol, security_gate_protocol, SecurityGateEvent
from axomai.agency.web_operator.browser_navigator import AutonomousBrowserNavigator, browser_navigator
from axomai.agency.web_operator.multi_tab_swarm import MultiTabSwarmCoordinator, multi_tab_swarm_coordinator

__all__ = [
    "SovereignCredentialVault",
    "credential_vault",
    "SecurityGateProtocol",
    "security_gate_protocol",
    "SecurityGateEvent",
    "AutonomousBrowserNavigator",
    "browser_navigator",
    "MultiTabSwarmCoordinator",
    "multi_tab_swarm_coordinator"
]

