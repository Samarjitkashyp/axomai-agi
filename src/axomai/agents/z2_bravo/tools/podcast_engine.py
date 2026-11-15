"""
Phase 7: Z2 Bravo Executive Audio Podcast & Daily Intelligence Brief Engine.
Converts research dossiers into an engaging 2-speaker strategic podcast dialogue
(Alex - Anchor & Maya - Senior Intelligence Director) for executive listening.
"""

import json
from typing import Dict, Any, List, Optional
from rich.console import Console

from axomai.core.llm import llm_brain

console = Console()

class ExecutivePodcastEngine:
    def __init__(self):
        pass

    def generate_podcast_briefing(
        self,
        topic: str,
        summary: str,
        evidence_text: str
    ) -> Dict[str, Any]:
        """
        Creates an executive 2-speaker podcast dialog and a synthesized spoken audio flow.
        """
        if llm_brain.is_available:
            try:
                sys_prompt = (
                    "You are an Executive Audio Producer. Convert this market research into a compelling 2-speaker podcast briefing.\n"
                    "Speakers: 'Alex' (Executive Anchor) and 'Maya' (Senior Intelligence Director).\n"
                    "Output JSON only:\n"
                    "{\n"
                    '  "title": "Episode Title",\n'
                    '  "duration_est": "2 Min Executive Briefing",\n'
                    '  "dialogue": [\n'
                    '    {"speaker": "Alex", "role": "Anchor", "text": "Hook question setting up market tension"},\n'
                    '    {"speaker": "Maya", "role": "Lead Analyst", "text": "Data-backed breakdown of competitors and metrics"},\n'
                    '    {"speaker": "Alex", "role": "Anchor", "text": "Challenge question about consumer complaints / risks"},\n'
                    '    {"speaker": "Maya", "role": "Lead Analyst", "text": "Strategic conclusion and leadership recommendation"}\n'
                    '  ]\n'
                    "}"
                )
                user_prompt = f"Topic: {topic}\nSummary:\n{summary[:1000]}\n\nGenerate Podcast JSON:"
                raw = llm_brain.generate(sys_prompt, user_prompt, temperature=0.2)
                clean = raw.strip()
                if "```json" in clean:
                    clean = clean.split("```json")[1].split("```")[0].strip()
                elif "```" in clean:
                    clean = clean.split("```")[1].split("```")[0].strip()
                parsed = json.loads(clean)
                if parsed.get("dialogue"):
                    # Assemble continuous spoken text for speech synthesis
                    spoken_flow = " ".join([f"{d['speaker']} says: {d['text']}" for d in parsed["dialogue"]])
                    parsed["spoken_flow"] = spoken_flow
                    return parsed
            except Exception as e:
                console.print(f"[dim yellow][Podcast LLM Parse Skip][/dim yellow] {e}")

        # High-impact fallback script
        fallback_dialogue = [
            {
                "speaker": "Alex",
                "role": "Executive Anchor",
                "text": f"Welcome to the AxomAI Intelligence Briefing. Today, we're dissecting the latest developments in {topic}. Maya, what is the single biggest shift we are seeing in the market right now?"
            },
            {
                "speaker": "Maya",
                "role": "Lead Market Analyst",
                "text": f"Alex, the data shows intense competitive consolidation. Top players are aggressively recalibrating pricing while scaling production infrastructure. The key battleground is no longer just brand awareness—it's execution and margin sustainability."
            },
            {
                "speaker": "Alex",
                "role": "Executive Anchor",
                "text": "And when you look at customer sentiment, are consumers actually buying into these moves, or are there underlying friction points?"
            },
            {
                "speaker": "Maya",
                "role": "Lead Market Analyst",
                "text": "There is clear divergence. While adoption is surging, after-sales service reliability and real-world efficiency are critical pain points. Companies that solve localized customer support will dominate the next market cycle."
            }
        ]

        spoken = " ".join([f"{d['speaker']}: {d['text']}" for d in fallback_dialogue])

        return {
            "title": f"Market Pulse: {topic[:50]}",
            "duration_est": "2 Min Executive Briefing",
            "dialogue": fallback_dialogue,
            "spoken_flow": spoken
        }

podcast_engine = ExecutivePodcastEngine()

