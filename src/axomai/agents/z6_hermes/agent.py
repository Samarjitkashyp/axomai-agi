"""
Z6 Hermes - Omnichannel Voice & Regional Comms Agent.
Powers voice speech synthesis, meeting action item extraction,
and automated WhatsApp / Telegram / Webhook dispatch.
"""

from typing import Dict, Any, Generator, Optional
from axomai.core.llm import llm_brain
from axomai.agents.z6_hermes.tools.meeting_intelligence import meeting_intelligence
from axomai.agents.z6_hermes.tools.omnichannel_dispatcher import omnichannel_dispatcher
from axomai.agents.z6_hermes.tools.voice_processor import voice_processor

class Z6HermesAgent:
    """Enterprise Communications, Speech & Omnichannel Dispatch Agent."""

    def __init__(self):
        self.name = "Z6 Hermes"
        self.role = "Omnichannel Voice & Regional Comms Agent"

    def comms_stream(
        self,
        query: str,
        session_id: Optional[str] = "hermes_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        q_lower = query.lower()

        # 1. Meeting Intelligence Route
        if any(k in q_lower for k in ["meeting", "transcript", "minutes of", "action items", "who is assigned", "sync notes"]):
            yield {
                "type": "status",
                "stage": "meeting_intel",
                "message": "🎙️ Z6 Hermes: Extracting key decisions, owners, and action deadlines..."
            }

            meeting_data = meeting_intelligence.analyze_meeting(query)
            speech_info = voice_processor.prepare_speech_script(f"Meeting summary: {meeting_data.get('title')}. {len(meeting_data.get('action_items', []))} action items assigned.")
            dispatch_info = omnichannel_dispatcher.prepare_dispatch(
                title=f"Meeting Digest: {meeting_data.get('title')}",
                summary=f"Key decisions: {', '.join(meeting_data.get('decisions', []))}"
            )

            meta_event = {
                "type": "meta",
                "agent": self.name,
                "task_type": "MEETING_INTELLIGENCE",
                "meeting_data": meeting_data,
                "speech_script": speech_info,
                "dispatch": dispatch_info,
                "tools_used": ["meeting_intelligence", "voice_processor", "omnichannel_dispatcher"]
            }
            yield meta_event

            prompt = (
                f"You are Z6 Hermes, Enterprise Communications & Meeting Intelligence Agent.\n"
                f"User Request: '{query}'\n\n"
                f"Meeting Data:\n{str(meeting_data)}\n\n"
                "Provide a polished, boardroom-ready Meeting Intelligence Brief in GitHub Markdown:\n"
                "1. 📌 Executive Summary & Key Decisions\n"
                "2. ✅ Concrete Action Items (Table: Owner, Task, Deadline)\n"
                "3. 📲 Omnichannel Dispatch Status (Ready for WhatsApp / Telegram)"
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate("You are Z6 Hermes, Enterprise Comms Agent.", prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = f"### 🎙️ Z6 Hermes Meeting Intelligence\n\n**Title:** {meeting_data.get('title')}\n\n**Action Items:** {len(meeting_data.get('action_items', []))}"
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # 2. Voice / Omnichannel Dispatch Route
        yield {
            "type": "status",
            "stage": "voice_comms",
            "message": "🎙️ Z6 Hermes: Synthesizing natural voice script & preparing omnichannel broadcast..."
        }

        speech_info = voice_processor.prepare_speech_script(query)
        dispatch_info = omnichannel_dispatcher.prepare_dispatch(
            title="AxomAI Executive Update",
            summary=query[:200]
        )

        meta_event = {
            "type": "meta",
            "agent": self.name,
            "task_type": "OMNICHANNEL_VOICE_DISPATCH",
            "speech_script": speech_info,
            "dispatch": dispatch_info,
            "tools_used": ["voice_processor", "omnichannel_dispatcher"]
        }
        yield meta_event

        prompt = (
            f"You are Z6 Hermes, Omnichannel Voice & Communications Agent.\n"
            f"User Prompt: '{query}'\n\n"
            f"Generated Speech Text:\n{speech_info.get('speech_text')}\n\n"
            f"WhatsApp Payload:\n{dispatch_info.get('whatsapp_message')}\n\n"
            "Respond concisely with the voice audio transcript and the formatted omnichannel dispatch preview in GitHub Markdown."
        )

        full_answer = ""
        if llm_brain.is_available:
            for chunk in llm_brain.stream_generate("You are Z6 Hermes.", prompt):
                full_answer += chunk
                yield {"type": "token", "content": chunk}
        else:
            full_answer = f"### 🎙️ Z6 Hermes Voice & Broadcast\n\n**Voice Script:** {speech_info.get('speech_text')}\n\n**WhatsApp:**\n{dispatch_info.get('whatsapp_message')}"
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

        yield {"type": "done", "answer": full_answer}

z6_hermes_agent = Z6HermesAgent()

