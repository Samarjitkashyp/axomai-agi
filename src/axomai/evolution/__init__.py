"""
AxomAI Evolution Engine package.
Provides Reflexion Engine, Autonomous Developer, Failure Detector, Hypothesis Engine,
Active Researcher, and Master Evolution Manager.
"""

from axomai.evolution.reflexion_engine import ReflexionEngine, reflexion_engine
from axomai.evolution.autonomous_developer import AutonomousDeveloper, autonomous_developer
from axomai.evolution.failure_detector import FailureDetector, failure_detector
from axomai.evolution.hypothesis_engine import HypothesisEngine, hypothesis_engine
from axomai.evolution.active_researcher import ActiveResearcher, active_researcher
from axomai.evolution.evolution_manager import EvolutionManager, evolution_manager

__all__ = [
    "ReflexionEngine",
    "reflexion_engine",
    "AutonomousDeveloper",
    "autonomous_developer",
    "FailureDetector",
    "failure_detector",
    "HypothesisEngine",
    "hypothesis_engine",
    "ActiveResearcher",
    "active_researcher",
    "EvolutionManager",
    "evolution_manager"
]
