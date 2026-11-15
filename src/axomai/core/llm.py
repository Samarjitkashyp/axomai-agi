import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
from axomai.config import settings

load_dotenv()

class LLMBrain:
    """
    Central LLM Client for AxomAI Agents.
    Defaults to OpenAI GPT-4o for document reasoning, table synthesis, and multi-doc analysis.
    """
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_client: Optional[OpenAI] = None
        self.gemini_client = None

        if self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)

        if self.gemini_key:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=self.gemini_key)
            except Exception:
                self.gemini_client = None

    def set_model(self, model_name: str):
        """Dynamically switch model provider"""
        self.model_name = model_name

    @property
    def is_available(self) -> bool:
        if self.model_name.startswith("gemini"):
            return self.gemini_client is not None
        return self.openai_client is not None

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        model_override: Optional[str] = None
    ) -> str:
        """
        Generate grounded reasoning from LLM.
        """
        active_model = model_override or self.model_name

        # --- GOOGLE GEMINI PATH ---
        if active_model.startswith("gemini"):
            if not self.gemini_client:
                return "[Error: GEMINI_API_KEY not configured or google-genai client unavailable]"
            try:
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
                response = self.gemini_client.models.generate_content(
                    model=active_model,
                    contents=full_prompt,
                )
                return response.text or ""
            except Exception as e:
                return f"[Gemini Inference Error: {str(e)}]"

        # --- OPENAI PATH ---
        if not self.openai_client:
            return "[Error: OPENAI_API_KEY not configured]"

        try:
            response = self.openai_client.chat.completions.create(
                model=active_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"[LLM Inference Error: {str(e)}]"

    def stream_generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        model_override: Optional[str] = None
    ):
        """
        Stream grounded reasoning tokens from LLM.
        """
        active_model = model_override or self.model_name

        if active_model.startswith("gemini"):
            if not self.gemini_client:
                yield "[Error: GEMINI_API_KEY not configured or google-genai client unavailable]"
                return
            try:
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
                response = self.gemini_client.models.generate_content_stream(
                    model=active_model,
                    contents=full_prompt,
                )
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
            except Exception as e:
                yield f"[Gemini Inference Error: {str(e)}]"
            return

        if not self.openai_client:
            yield "[Error: OPENAI_API_KEY not configured]"
            return

        try:
            response = self.openai_client.chat.completions.create(
                model=active_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"[LLM Stream Error: {str(e)}]"

# Global Singleton instance
llm_brain = LLMBrain()

