"""
Z6 Hermes - Voice & Multilingual Regional Speech Synthesizer Tool.
Formats clean voice scripts and SSML cues for browser SpeechSynthesis
and multilingual voice playback across Assamese, Bengali, Hindi, and English.
"""

import re
from typing import Dict, Any

class VoiceProcessor:
    """Prepares natural spoken voice scripts from text."""

    def prepare_speech_script(self, text: str, language: str = "en") -> Dict[str, Any]:
        """
        Cleans markdown, tables, and code blocks to produce a natural, human-like voice script.
        """
        # Remove markdown symbols, code blocks, bold markers
        clean = re.sub(r'```.*?```', '[Code snippet omitted in speech]', text, flags=re.DOTALL)
        clean = re.sub(r'[#*`_~]', '', clean)
        clean = re.sub(r'\[.*?\]\(.*?\)', '', clean)
        clean = re.sub(r'\s+', ' ', clean).strip()

        lang_code_map = {
            "en": "en-IN",
            "hi": "hi-IN",
            "as": "as-IN",
            "bn": "bn-IN"
        }
        speech_lang = lang_code_map.get(language.lower(), "en-IN")

        return {
            "speech_text": clean[:800],
            "language_code": speech_lang,
            "estimated_duration_sec": max(5, round(len(clean.split()) / 2.5)),
            "voice_ready": True
        }

voice_processor = VoiceProcessor()

