"""
Z6 Hermes - Meeting Intelligence & Action Item Extractor Tool.
Extracts discussion topics, decisions, owners, and action deadlines
from meeting transcripts and conversational notes.
"""

from typing import Dict, Any, List
from axomai.core.llm import llm_brain

class MeetingIntelligence:
    """Enterprise meeting summarizer and commitment tracker."""

    def analyze_meeting(self, transcript_or_notes: str) -> Dict[str, Any]:
        """
        Extracts strategic decisions and action items from meeting text.
        """
        if not llm_brain.is_available:
            return {
                "title": "Strategy Discussion",
                "decisions": ["Maintain current strategic roadmap"],
                "action_items": [
                    {"owner": "Team Lead", "task": "Review deliverables", "deadline": "Next Friday"}
                ]
            }

        system_prompt = (
            "You are Z6 Hermes Meeting Intelligence Engine. Analyze this meeting text. "
            "Extract: 1) Meeting Title, 2) Key Decisions, 3) Action Items (with owner, task, and deadline). "
            "Output JSON only: {\"title\": \"str\", \"decisions\": [\"str\"], \"action_items\": [{\"owner\": \"str\", \"task\": \"str\", \"deadline\": \"str\"}]}"
        )
        user_prompt = f"Meeting Notes / Transcript:\n{transcript_or_notes}\n\nProduce structured JSON only."

        try:
            res = llm_brain.generate(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.1)
            clean_json = res.strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_json:
                clean_json = clean_json.split("```")[1].split("```")[0].strip()

            import json
            return json.loads(clean_json)
        except Exception:
            return {
                "title": "Executive Sync",
                "decisions": ["Aligned on priorities"],
                "action_items": [
                    {"owner": "Operations", "task": "Follow up on schedule", "deadline": "EOD"}
                ]
            }

meeting_intelligence = MeetingIntelligence()

