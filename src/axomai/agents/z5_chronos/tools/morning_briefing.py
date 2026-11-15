"""
Z5 Chronos - Proactive Morning Executive Briefing Synthesizer.
Compiles overnight alerts, daily task agendas, and strategic highlights
into an executive brief for leadership.
"""

from typing import Dict, Any
from axomai.agents.z5_chronos.tools.task_scheduler import task_scheduler
from axomai.agents.z5_chronos.tools.metric_monitor import metric_monitor

class MorningBriefing:
    """Autonomous morning brief synthesizer."""

    def compile_briefing(self) -> Dict[str, Any]:
        jobs = task_scheduler.list_jobs()
        alerts = metric_monitor.evaluate_triggers()

        return {
            "briefing_title": "Executive Morning Horizon Briefing",
            "active_schedules_count": len(jobs),
            "triggered_alerts": [a for a in alerts if a["status"] == "TRIGGERED"],
            "all_alerts": alerts,
            "jobs": jobs
        }

morning_briefing = MorningBriefing()

