import os
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from axomai.core.llm import llm_brain

load_dotenv()

class XetuAssameseTranslator:
    """
    Axom AI Bridge - Xetu (সেতু)
    Assam's Sovereign English <-> Assamese Neural Translation Engine
    Repository: axom-ai/axomai-trans-xetu (Hugging Face)
    """
    def __init__(self):
        self.model_id = "axom-ai/axomai-trans-xetu"
        self.hf_token = os.getenv("HF_TOKEN")
        self.hf_router_url = f"https://router.huggingface.co/hf-inference/models/{self.model_id}"

    def translate_assamese_to_english(self, text: str) -> Dict[str, Any]:
        """
        Translates Assamese text to English using Xetu Engine with native cultural preservation.
        """
        if not text or not text.strip():
            return {"success": True, "translated_text": "", "source_lang": "as", "target_lang": "en"}

        # Attempt 1: Hugging Face Router
        if self.hf_token:
            try:
                payload = json.dumps({"inputs": text}).encode("utf-8")
                req = urllib.request.Request(
                    self.hf_router_url,
                    data=payload,
                    headers={
                        "Authorization": f"Bearer {self.hf_token}",
                        "Content-Type": "application/json"
                    }
                )
                with urllib.request.urlopen(req, timeout=10) as response:
                    raw_data = json.loads(response.read().decode("utf-8"))
                    if isinstance(raw_data, list) and len(raw_data) > 0 and "translation_text" in raw_data[0]:
                        return {
                            "success": True,
                            "translated_text": raw_data[0]["translation_text"],
                            "engine": "xetu-hf-remote",
                            "source_lang": "as",
                            "target_lang": "en"
                        }
            except Exception:
                pass # Proceed to specialized in-agent bridge

        # Fallback / Specialized In-Agent Bridge with strict Assamese linguistic prompting
        sys_prompt = (
            "You are the linguistic core of 'Axom AI Xetu (সেতু)', Assam's Sovereign Translation Engine.\n"
            "Your task is to accurately translate authentic Assamese text into clear English while preserving native cultural terminology and tone.\n"
            "Provide ONLY the translated English text, without conversational prefixes."
        )
        user_prompt = f"Assamese text: \"{text}\"\n\nEnglish translation:"
        
        fallback_res = llm_brain.generate(sys_prompt, user_prompt, temperature=0.0)
        return {
            "success": True,
            "translated_text": fallback_res.strip().strip('"'),
            "engine": "xetu-agentic-bridge",
            "source_lang": "as",
            "target_lang": "en"
        }

    def translate_english_to_assamese(self, text: str) -> Dict[str, Any]:
        """
        Translates English text to authentic Assamese (অসমীয়া).
        """
        if not text or not text.strip():
            return {"success": True, "translated_text": "", "source_lang": "en", "target_lang": "as"}

        sys_prompt = (
            "You are the linguistic core of 'Axom AI Xetu (সেতু)', Assam's Sovereign Translation Engine.\n"
            "Translate the given English text into pure, grammatical, and culturally accurate Assamese (অসমীয়া লিপি).\n"
            "Provide ONLY the Assamese translation text."
        )
        user_prompt = f"English text: \"{text}\"\n\nঅসমীয়া অনুবাদ:"
        fallback_res = llm_brain.generate(sys_prompt, user_prompt, temperature=0.0)
        return {
            "success": True,
            "translated_text": fallback_res.strip().strip('"'),
            "engine": "xetu-agentic-bridge",
            "source_lang": "en",
            "target_lang": "as"
        }

xetu_translator = XetuAssameseTranslator()
