"""
AxomAI Mission Control - Autonomous Artifact Store.
Replaces brittle string-slicing (e.g. [:500]) with a structured, multi-artifact repository.
Maintains typed deliverables, executive digests, and delivers full contextual payloads
to downstream agents in the execution pipeline.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class MissionArtifact(BaseModel):
    artifact_id: str
    mission_id: str
    step_id: int
    agent_name: str
    title: str
    deliverable_type: str
    summary: str
    full_content: str
    quality_score: float = 1.0
    verification_criteria: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class MissionArtifactStore:
    """In-memory and persistent structured artifact store for autonomous missions."""

    def __init__(self):
        self._artifacts: Dict[str, List[MissionArtifact]] = {}

    def store_artifact(
        self,
        mission_id: str,
        step_id: int,
        agent_name: str,
        title: str,
        deliverable_type: str,
        full_content: str,
        quality_score: float = 1.0,
        verification_criteria: Optional[List[str]] = None
    ) -> MissionArtifact:
        """Stores a structured deliverable from an executed milestone."""
        # Generate clean executive summary (up to 3 paragraphs or first 500 words)
        words = full_content.strip().split()
        summary_words = words[:120]
        summary = " ".join(summary_words) + ("..." if len(words) > 120 else "")

        art = MissionArtifact(
            artifact_id=f"art_{mission_id}_{step_id}_{agent_name.lower().replace(' ', '_')[:10]}",
            mission_id=mission_id,
            step_id=step_id,
            agent_name=agent_name,
            title=title,
            deliverable_type=deliverable_type,
            summary=summary,
            full_content=full_content,
            quality_score=quality_score,
            verification_criteria=verification_criteria or []
        )

        if mission_id not in self._artifacts:
            self._artifacts[mission_id] = []
        self._artifacts[mission_id].append(art)
        return art

    def get_artifacts(self, mission_id: str) -> List[MissionArtifact]:
        """Retrieves all artifacts produced in a mission."""
        return self._artifacts.get(mission_id, [])

    def get_chained_context(self, mission_id: str, current_step_id: int) -> str:
        """
        Builds rich, structured context without arbitrary character truncation.
        Provides:
        1. High-level roadmap digest of all completed milestones.
        2. Full verbatim content of the immediately preceding milestone for direct dependency injection.
        """
        arts = self.get_artifacts(mission_id)
        if not arts:
            return ""

        completed_digest = []
        for a in arts:
            completed_digest.append(
                f"- [Stage {a.step_id} - {a.agent_name}]: {a.title} ({a.deliverable_type})\n"
                f"  Summary: {a.summary}\n"
                f"  Quality Score: {int(a.quality_score * 100)}%"
            )

        context_blocks = [
            "### 🔗 UPSTREAM MISSION INTELLIGENCE & ARTIFACT REPOSITORY:",
            "#### 📋 Summary of Completed Milestones:",
            "\n".join(completed_digest)
        ]

        # Inject the entire content of the most recent prior milestone
        prior_art = arts[-1]
        context_blocks.append(
            f"\n#### 📑 Direct Preceding Stage Deliverable (Full Content from {prior_art.agent_name} - Stage {prior_art.step_id}):\n"
            f"```text\n{prior_art.full_content}\n```"
        )

        return "\n\n" + "\n".join(context_blocks) + "\n\n"

    def export_dossier(self, mission_id: str) -> Dict[str, Any]:
        """Exports the full comprehensive mission dossier with all structured artifacts."""
        arts = self.get_artifacts(mission_id)
        return {
            "mission_id": mission_id,
            "total_artifacts": len(arts),
            "artifacts": [a.model_dump() for a in arts]
        }

mission_artifact_store = MissionArtifactStore()
