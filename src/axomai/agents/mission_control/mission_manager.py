"""
AxomAI Mission Control - Autonomous Mission Manager.
Manages the end-to-end closed-loop execution of strategic goals formulated by Cognitive Core:
1. Decomposes goal into ordered multi-agent milestones with explicit input/output dependency chaining.
2. Dispatches and executes milestones across specialized agent fleet (Z1-Z17, Y1-Y5) via authoritative MissionExecutor.
3. Passes rich, untruncated structured context via MissionArtifactStore (no [:500] data starvation).
4. Conducts rigorous multi-criteria verification via MissionVerifier + Z Sentinel.
5. Performs autonomous self-healing, diagnostic re-prompting, and alternative agent re-routing on failure.
6. Updates World Model and Episodic Memory with full verified deliverables.
"""

import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from axomai.agents.mission_control.planner import mission_planner, MissionPlan, MissionMilestone
from axomai.agents.mission_control.executor import mission_executor
from axomai.agents.mission_control.verifier import mission_verifier, VerificationResult
from axomai.agents.mission_control.artifact_store import mission_artifact_store, MissionArtifact
from axomai.memory.episodic_memory import episodic_memory
from axomai.cognition.world_model import world_model
from axomai.cognition.self_model import self_model

class AutonomousMissionManager:
    """Master executive controller for autonomous closed-loop mission orchestration."""

    def __init__(self):
        self.active_missions: Dict[str, Dict[str, Any]] = {}
        self.mission_history: List[Dict[str, Any]] = []

    def execute_goal_as_mission(
        self,
        goal_title: str,
        action_directive: str,
        target_agent: Optional[str] = None,
        doc_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Orchestrates an autonomous mission from a strategic goal to verified completion
        with active verification, untruncated artifact chaining, and self-recovery replanning.
        """
        t0 = time.time()
        now = datetime.now(timezone.utc).isoformat()
        
        # 1. Plan the Mission Graph
        query = f"{goal_title}: {action_directive}"
        plan: MissionPlan = mission_planner.plan_mission(query, doc_id=doc_id)
        mission_id = plan.mission_id

        # 2. Register Active Mission in World Model
        world_model.update_entity("active_mission", {
            "mission_id": mission_id,
            "title": plan.title,
            "status": "EXECUTING_PIPELINE",
            "total_steps": plan.total_steps,
            "current_step": 1,
            "started_at": now
        })

        self.active_missions[mission_id] = {
            "mission_id": mission_id,
            "title": plan.title,
            "plan": plan.model_dump(),
            "status": "EXECUTING"
        }

        # 3. Chained Step-by-Step Execution with Verification & Recovery
        executed_milestones: List[Dict[str, Any]] = []
        failure_detected = False
        final_failure_reason = ""
        total_recoveries = 0

        for m in plan.milestones:
            step_id = m.step_id
            world_model.update_entity("active_mission", {
                "current_step": step_id,
                "current_agent": m.agent_name,
                "current_objective": m.objective
            })

            # Retrieve rich, untruncated structured context from preceding artifacts
            upstream_context = mission_artifact_store.get_chained_context(mission_id, step_id)
            step_prompt = f"{m.prompt}\n{upstream_context}" if upstream_context else m.prompt

            step_output = ""
            verification: Optional[VerificationResult] = None
            step_recovered = False
            recovery_notes = []

            # Execute Primary Dispatch
            try:
                step_output = mission_executor.execute_milestone(
                    target_agent=m.target_agent,
                    prompt=step_prompt
                )
                # Verify Primary Deliverable
                verification = mission_verifier.verify_milestone(
                    output=step_output,
                    milestone_title=m.title,
                    milestone_objective=m.objective,
                    target_agent=m.target_agent,
                    context_str=upstream_context
                )
            except Exception as ex:
                verification = VerificationResult(
                    passed=False,
                    quality_score=0.0,
                    feedback=f"Execution exception: {str(ex)}",
                    missing_criteria=["execution_success"],
                    sanitized_output=""
                )

            # Auto-Recovery & Re-planning Loop if Verification Failed
            if not verification.passed:
                total_recoveries += 1
                recovery_notes.append(f"Primary attempt failed: {verification.feedback}")

                # Attempt 1: Remedial Re-Prompt with Diagnostic Feedback
                remedial_prompt = (
                    f"{step_prompt}\n\n"
                    f"⚠️ PREVIOUS ATTEMPT DEFICIENCY DIAGNOSTIC:\n"
                    f"{verification.feedback}\n"
                    f"Please regenerate deliverable resolving all listed deficiencies strictly."
                )
                try:
                    remedial_output = mission_executor.execute_milestone(
                        target_agent=m.target_agent,
                        prompt=remedial_prompt
                    )
                    remedial_verif = mission_verifier.verify_milestone(
                        output=remedial_output,
                        milestone_title=m.title,
                        milestone_objective=m.objective,
                        target_agent=m.target_agent,
                        context_str=upstream_context
                    )
                    if remedial_verif.passed:
                        step_output = remedial_output
                        verification = remedial_verif
                        step_recovered = True
                        recovery_notes.append("Recovered successfully via remedial re-prompting.")
                except Exception as ex2:
                    recovery_notes.append(f"Remedial attempt exception: {str(ex2)}")

                # Attempt 2: Dynamic Re-routing to Alternative Agent (if still failing)
                if not verification.passed:
                    fallback_agent = "z4" if m.target_agent != "z4" else "z9"
                    recovery_notes.append(f"Re-routing milestone to fallback authority: {fallback_agent}")
                    try:
                        fallback_output = mission_executor.execute_milestone(
                            target_agent=fallback_agent,
                            prompt=step_prompt
                        )
                        fallback_verif = mission_verifier.verify_milestone(
                            output=fallback_output,
                            milestone_title=m.title,
                            milestone_objective=m.objective,
                            target_agent=fallback_agent,
                            context_str=upstream_context
                        )
                        if fallback_verif.passed:
                            step_output = fallback_output
                            verification = fallback_verif
                            step_recovered = True
                            recovery_notes.append(f"Recovered successfully via fallback agent {fallback_agent}.")
                        else:
                            recovery_notes.append(f"Fallback agent {fallback_agent} also failed verification: {fallback_verif.feedback}")
                    except Exception as ex3:
                        recovery_notes.append(f"Fallback routing exception: {str(ex3)}")

            # If still failed after all recovery attempts, record failure and break
            if not verification.passed:
                failure_detected = True
                final_failure_reason = f"Stage {step_id} ({m.title}) failed verification: {verification.feedback}"
                
                # Record in Self-Model failure ledger for introspective learning
                self_model.record_failure_mode(
                    domain=f"mission_milestone_{m.target_agent}",
                    error_context=f"Failed objective: {m.objective[:120]}",
                    mitigation=f"Replan required. Verification deficiencies: {'; '.join(verification.missing_criteria)}"
                )
                
                executed_milestones.append({
                    "step_id": step_id,
                    "title": m.title,
                    "agent": m.agent_name,
                    "status": "FAILED",
                    "error": final_failure_reason,
                    "quality_score": verification.quality_score,
                    "recovery_history": recovery_notes
                })
                break

            # Store verified deliverable into structured ArtifactStore
            clean_output = verification.sanitized_output or step_output
            stored_artifact = mission_artifact_store.store_artifact(
                mission_id=mission_id,
                step_id=step_id,
                agent_name=m.agent_name,
                title=m.title,
                deliverable_type=m.deliverable_type,
                full_content=clean_output,
                quality_score=verification.quality_score,
                verification_criteria=verification.criteria_met
            )

            # Record successful milestone execution in Self-Model performance telemetry
            self_model.record_execution(
                domain=m.target_agent,
                success=True,
                latency_sec=round(time.time() - t0, 2)
            )

            executed_milestones.append({
                "step_id": step_id,
                "title": m.title,
                "agent": m.agent_name,
                "status": "RECOVERED_AND_COMPLETED" if step_recovered else "COMPLETED",
                "quality_score": verification.quality_score,
                "criteria_met": verification.criteria_met,
                "artifact_id": stored_artifact.artifact_id,
                "output_preview": clean_output[:300],
                "recovery_history": recovery_notes if step_recovered else []
            })

        # 4. Final Mission Status & Verification
        duration_sec = round(time.time() - t0, 2)
        mission_status = "COMPLETED" if not failure_detected else "PARTIALLY_EXECUTED_REPLAN_REQUIRED"

        # Update World Model with final mission state
        world_model.update_entity("active_mission", {
            "status": mission_status,
            "completed_steps": len(executed_milestones),
            "total_steps": plan.total_steps,
            "total_recoveries": total_recoveries,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "duration_sec": duration_sec
        })

        # 5. Permanent Episodic Memory Consolidation
        dossier = mission_artifact_store.export_dossier(mission_id)
        try:
            episodic_memory.record_episode(
                query=f"Autonomous Mission: {plan.title}",
                agent_id="autonomous_mission_manager",
                outcome_status="SUCCESS" if not failure_detected else "PARTIAL_FAILURE",
                reward_score=1.0 if not failure_detected else 0.4,
                reflection=(
                    f"Executed {len(executed_milestones)}/{plan.total_steps} milestones for mission '{mission_id}'. "
                    f"Recoveries triggered: {total_recoveries}."
                ),
                lesson_learned=f"Mission objective '{plan.strategic_objective[:120]}' completed in {duration_sec}s with {len(dossier.get('artifacts', []))} artifacts.",
                metadata={
                    "mission_id": mission_id,
                    "duration_sec": duration_sec,
                    "artifacts_count": len(dossier.get("artifacts", [])),
                    "total_recoveries": total_recoveries
                }
            )
        except Exception:
            pass

        result_record = {
            "mission_id": mission_id,
            "title": plan.title,
            "strategic_objective": plan.strategic_objective,
            "total_steps": plan.total_steps,
            "milestones_executed": len(executed_milestones),
            "milestones": executed_milestones,
            "status": mission_status,
            "total_recoveries": total_recoveries,
            "artifacts_generated": len(dossier.get("artifacts", [])),
            "duration_sec": duration_sec,
            "completed_at": datetime.now(timezone.utc).isoformat()
        }

        self.mission_history.append(result_record)
        return result_record

autonomous_mission_manager = AutonomousMissionManager()
