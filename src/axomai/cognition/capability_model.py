"""
AxomAI Cognition Engine - Dynamic Capability Registry & Model.
Maintains the catalog of operational skills, tools, and algorithms available to the AGI.
Provides standardized invocation schemas, security classification, and dynamic registration.
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timezone

class CapabilityDefinition:
    """Specification of an executable capability."""

    def __init__(
        self,
        name: str,
        description: str,
        category: str,
        handler: Optional[Callable] = None,
        parameters: Optional[Dict[str, Any]] = None,
        security_level: str = "LOW",
        acquired_dynamically: bool = False
    ):
        self.name = name
        self.description = description
        self.category = category
        self.handler = handler
        self.parameters = parameters or {}
        self.security_level = security_level
        self.acquired_dynamically = acquired_dynamically
        self.registered_at = datetime.now(timezone.utc).isoformat()
        self.invocation_count: int = 0

    def execute(self, **kwargs) -> Any:
        if self.handler is None:
            raise NotImplementedError(f"Capability '{self.name}' has no registered handler.")
        self.invocation_count += 1
        return self.handler(**kwargs)

class CapabilityRegistry:
    """Central registry of all native and dynamically acquired AGI capabilities."""

    def __init__(self):
        self._capabilities: Dict[str, CapabilityDefinition] = {}
        self._bootstrap_default_capabilities()

    def _bootstrap_default_capabilities(self) -> None:
        """Initializes core default capabilities."""
        self.register(CapabilityDefinition(
            name="bishop_factor_of_safety",
            description="Computes geotechnical slope stability factor of safety using Bishop simplified method.",
            category="GEOTECHNICAL",
            handler=lambda resisting, driving: round(float(resisting) / float(driving), 3),
            parameters={"resisting": "float", "driving": "float"},
            security_level="LOW"
        ))
        self.register(CapabilityDefinition(
            name="zero_cost_collar_hedging",
            description="Calculates put floor and call cap bounds for FX risk neutralization.",
            category="FINANCIAL_ENGINEERING",
            handler=lambda spot, spread=0.04: {
                "floor_put": round(float(spot) * (1.0 - spread), 2),
                "cap_call": round(float(spot) * (1.0 + spread), 2),
                "neutralized_spot": float(spot)
            },
            parameters={"spot": "float", "spread": "float"},
            security_level="LOW"
        ))
        self.register(CapabilityDefinition(
            name="solar_clean_energy_yield",
            description="Computes annual generation MWh and carbon offset tCO2e for industrial captive solar.",
            category="ENERGY_ARBITRAGE",
            handler=lambda capacity_kw: {
                "annual_mwh": round((float(capacity_kw) * 4.2 * 365) / 1000.0, 2),
                "co2_offset_tons": round(((float(capacity_kw) * 4.2 * 365) / 1000.0) * 0.82, 2)
            },
            parameters={"capacity_kw": "float"},
            security_level="LOW"
        ))

    def register(self, cap: CapabilityDefinition) -> None:
        self._capabilities[cap.name] = cap

    def get(self, name: str) -> Optional[CapabilityDefinition]:
        return self._capabilities.get(name)

    def has_capability(self, name: str) -> bool:
        return name in self._capabilities

    def list_all(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": c.name,
                "description": c.description,
                "category": c.category,
                "security_level": c.security_level,
                "acquired_dynamically": c.acquired_dynamically,
                "invocation_count": c.invocation_count,
                "registered_at": c.registered_at
            }
            for c in self._capabilities.values()
        ]

capability_registry = CapabilityRegistry()

