"""
Z5 Chronos - Autonomous Scheduler & Proactive Workflow Agent.
Automates cron schedules, monitors metric thresholds for autonomous alerts,
and synthesizes proactive morning executive briefings.
"""

from typing import Dict, Any, Generator, Optional
from axomai.core.llm import llm_brain
from axomai.agents.z5_chronos.tools.task_scheduler import task_scheduler
from axomai.agents.z5_chronos.tools.metric_monitor import metric_monitor
from axomai.agents.z5_chronos.tools.morning_briefing import morning_briefing

class Z5ChronosAgent:
    """Enterprise Scheduler and Proactive Task Orchestrator."""

    def __init__(self):
        self.name = "Z5 Chronos"
        self.role = "Autonomous Scheduler & Proactive Workflow Agent"

    def schedule_stream(
        self,
        query: str,
        session_id: Optional[str] = "chronos_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        q_lower = query.lower()

        # Check if user wants to create a new schedule
        import re
        is_create_intent = bool(re.search(r'\b(schedule a\b|create a (task|schedule)|remind me to\b|set a cron\b|run every\b)', q_lower))
        if is_create_intent:
            yield {
                "type": "status",
                "stage": "create_schedule",
                "message": "⏱️ Z5 Chronos: Registering new autonomous cron schedule..."
            }
            # Parse title and action
            new_job = task_scheduler.add_job(
                title=query[:60],
                schedule_human="Every day at 9:00 AM",
                target_agent="Master Orchestrator",
                action=query
            )
            jobs = task_scheduler.list_jobs()

            meta_event = {
                "type": "meta",
                "agent": self.name,
                "task_type": "SCHEDULE_CREATED",
                "new_job": new_job,
                "all_jobs": jobs,
                "tools_used": ["cron_registry", "task_scheduler"]
            }
            yield meta_event

            msg = (
                f"### ⏱️ Z5 Chronos: Autonomous Task Scheduled\n\n"
                f"- **Task Title:** `{new_job['title']}`\n"
                f"- **Cadence:** `{new_job['schedule_human']}`\n"
                f"- **Assigned Autonomous Agent:** `{new_job['target_agent']}`\n"
                f"- **Action:** {new_job['action']}\n"
                f"- **Status:** `ACTIVE` (Next run scheduled for tomorrow)\n\n"
                "> AxomAI AGI will autonomously execute this task in the background and deliver results to your workspace."
            )
            for tok in msg.split(" "):
                yield {"type": "token", "content": tok + " "}
            yield {"type": "done", "answer": msg}
            return

        # Proactive Morning Briefing / Status
        yield {
            "type": "status",
            "stage": "chronos_eval",
            "message": "⏱️ Z5 Chronos: Evaluating active cron triggers & metric thresholds..."
        }

        brief = morning_briefing.compile_briefing()
        jobs = brief["jobs"]
        alerts = brief["all_alerts"]

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "MORNING_EXECUTIVE_BRIEFING",
            "schedules": jobs,
            "alerts": alerts,
            "tools_used": ["metric_monitor", "task_scheduler", "morning_briefing"]
        }
        yield meta_event

        prompt = (
            f"You are Z5 Chronos, Enterprise Scheduler & Workflow Orchestrator.\n"
            f"User Query: '{query}'\n\n"
            f"Active Background Cron Schedules ({len(jobs)}):\n"
            f"{str(jobs)}\n\n"
            f"Active Metric Watchdog Alerts:\n"
            f"{str(alerts)}\n\n"
            "Format a high-impact, professional Executive Morning Briefing in GitHub Markdown:\n"
            "1. ⏱️ Active Autonomous Cron Agenda (table of tasks, cadences, and next runs)\n"
            "2. 🚨 Watchdog Threshold & Anomaly Alerts (urgent vs healthy signals)\n"
            "3. 💡 Proactive Strategic Next Steps"
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z5 Chronos, Enterprise Scheduler.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = f"### ⏱️ Z5 Chronos: Executive Schedule & Alerts\n\n**Active Tasks:** {len(jobs)}\n**Alerts:** {len(alerts)}"
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": full_answer}

z5_chronos_agent = Z5ChronosAgent()
