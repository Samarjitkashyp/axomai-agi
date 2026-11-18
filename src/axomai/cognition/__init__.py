"""
AxomAI Cognition Engine package.
Provides Self-Model, World-Model, Capability Registry, Dynamic Capability Acquisition,
Belief Manager, Deliberative Goal Formation, Counterfactual War-Game Simulator, and Master Cognitive Core.
"""

from axomai.cognition.self_model import SelfModel, self_model
from axomai.cognition.world_model import WorldModel, world_model
from axomai.cognition.capability_model import CapabilityDefinition, CapabilityRegistry, capability_registry
from axomai.cognition.capability_acquisition import CapabilityAcquisitionEngine, capability_acquisition_engine
from axomai.cognition.belief_manager import Belief, BeliefManager, belief_manager
from axomai.cognition.goal_formation import StrategicGoal, CognitiveGoalFormation, cognitive_goal_formation
from axomai.cognition.war_game_simulator import WarGameSimulator, war_game_simulator
from axomai.cognition.counterfactual_engine import CounterfactualEngine, counterfactual_engine
from axomai.cognition.cognitive_core import CognitiveCore, cognitive_core
from axomai.cognition.cognitive_intent_profiler import CognitiveIntentProfiler, CognitiveProfile, cognitive_intent_profiler

__all__ = [
    "SelfModel",
    "self_model",
    "WorldModel",
    "world_model",
    "CapabilityDefinition",
    "CapabilityRegistry",
    "capability_registry",
    "CapabilityAcquisitionEngine",
    "capability_acquisition_engine",
    "Belief",
    "BeliefManager",
    "belief_manager",
    "StrategicGoal",
    "CognitiveGoalFormation",
    "cognitive_goal_formation",
    "WarGameSimulator",
    "war_game_simulator",
    "CounterfactualEngine",
    "counterfactual_engine",
    "CognitiveCore",
    "cognitive_core",
    "CognitiveIntentProfiler",
    "CognitiveProfile",
    "cognitive_intent_profiler"
]
