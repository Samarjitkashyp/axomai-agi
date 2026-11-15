import os
import base64
import mimetypes
from pathlib import Path
from typing import Optional, Dict, Any, Union
from openai import OpenAI
from dotenv import load_dotenv

from axomai.core.translators.xetu import xetu_translator

load_dotenv()

class VisionEngine:
    """
    Multimodal Vision Engine for Z1 Alpha.
    Priority Pipeline:
    1. Google Gemini 2.0 Flash (Primary for images, charts, graphics, presentations)
    2. Google Gemini 1.5 Flash (Fallback if Gemini 2.0 is unavailable)
    3. OpenAI GPT-4o (Fallback if Gemini API is disabled/permission denied)
    Integrated with Axom AI Xetu (সেতু) for authentic Assamese OCR & translation.
    """
    def __init__(self):
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

    @property
    def is_available(self) -> bool:
        return self.openai_client is not None or bool(self.gemini_key)

    def encode_image(self, image_input: Union[str, Path, bytes], mime_type: Optional[str] = None) -> tuple[str, str, bytes]:
        """Returns (base64_string, mime_type, raw_bytes)"""
        if isinstance(image_input, (str, Path)):
            path = Path(image_input)
            if not path.exists():
                raise FileNotFoundError(f"Image not found at: {image_input}")
            
            guessed_mime, _ = mimetypes.guess_type(str(path))
            mime = guessed_mime or "image/png"
            with open(path, "rb") as f:
                raw_bytes = f.read()
            b64_str = base64.b64encode(raw_bytes).decode("utf-8")
            return b64_str, mime, raw_bytes
        elif isinstance(image_input, bytes):
            mime = mime_type or "image/png"
            b64_str = base64.b64encode(image_input).decode("utf-8")
            return b64_str, mime, image_input
        else:
            raise ValueError("Unsupported image input type")

    def analyze(
        self,
        image_input: Union[str, Path, bytes],
        question: Optional[str] = None,
        task_mode: str = "comprehensive",
        mime_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Deep visual and OCR analysis of an image/graphics-heavy document.
        Executes Google Gemini 2.0 Flash -> Gemini 1.5 Flash -> OpenAI GPT-4o fallback pipeline.
        """
        if not self.is_available:
            return {
                "success": False,
                "error": "No active Vision LLM key found. Please configure GEMINI_API_KEY or OPENAI_API_KEY."
            }

        try:
            b64_data, detected_mime, raw_bytes = self.encode_image(image_input, mime_type)
            actual_question = question.strip() if question else "Analyze this image in detail, extract all text, brand names, and regional language content."

            sys_instruction = (
                "You are Z1 Alpha, an advanced Multimodal & Indic Vision Intelligence Agent.\n\n"
                "CRITICAL OCR & VISION PROTOCOLS:\n"
                "1. STRICT BRAND ACCURACY: Read brand names and titles letter-by-letter. Never autocorrect or replace names (e.g. if the image displays 'Axom AI', DO NOT write 'Axiom').\n"
                "2. MULTILINGUAL & INDIC OCR: Carefully transcribe all non-English text (Assamese 'অসমীয়া', Bengali, Hindi, etc.). Always transcribe the exact original script characters.\n"
                "3. COMPLETE UI & STRUCTURAL AUDIT:\n"
                "   - Header, Logo, and Taglines\n"
                "   - Navigation links and menus\n"
                "   - Headlines, Badges, and Subtitles\n"
                "   - Descriptions and Value propositions\n"
                "   - Call-to-action buttons\n"
                "   - Footer details, trust badges, and locations\n"
                "4. DIRECT USER ANSWERS: If the user asks a specific question, answer that directly first.\n"
                "5. LANGUAGE MATCHING: Respond in the user's language (Hindi, Hinglish, or English)."
            )

            raw_analysis = ""
            model_used = ""

            # --- STEP 1: GOOGLE GEMINI 3.5 FLASH (Primary Vision) ---
            if self.gemini_client:
                try:
                    from google.genai import types
                    image_part = types.Part.from_bytes(data=raw_bytes, mime_type=detected_mime)
                    prompt_text = f"{sys_instruction}\n\nUSER INSTRUCTION: {actual_question}"
                    res = self.gemini_client.models.generate_content(
                        model="gemini-3.5-flash",
                        contents=[image_part, prompt_text]
                    )
                    if res and res.text:
                        raw_analysis = res.text
                        model_used = "Google Gemini 3.5 Flash"
                except Exception:
                    # --- STEP 2: FALLBACK TO GOOGLE GEMINI 3.1 FLASH LITE ---
                    try:
                        from google.genai import types
                        image_part = types.Part.from_bytes(data=raw_bytes, mime_type=detected_mime)
                        prompt_text = f"{sys_instruction}\n\nUSER INSTRUCTION: {actual_question}"
                        res = self.gemini_client.models.generate_content(
                            model="gemini-3.1-flash-lite",
                            contents=[image_part, prompt_text]
                        )
                        if res and res.text:
                            raw_analysis = res.text
                            model_used = "Google Gemini 3.1 Flash Lite"
                    except Exception:
                        pass # Fall through to OpenAI GPT-4o

            # --- STEP 3: FALLBACK TO OPENAI GPT-4o ---
            if not raw_analysis and self.openai_client:
                data_url = f"data:{detected_mime};base64,{b64_data}"
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": sys_instruction},
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"USER INSTRUCTION: {actual_question}"},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": data_url,
                                        "detail": "high"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=2048,
                    temperature=0.1
                )
                raw_analysis = response.choices[0].message.content or ""
                model_used = "gpt-4o (OpenAI Vision)"

            if not raw_analysis:
                return {
                    "success": False,
                    "error": "Both Gemini and OpenAI vision services were unreachable."
                }

            # Check if Assamese text was detected and enrich with Xetu translation if applicable
            has_assamese_script = any('\u0980' <= char <= '\u09FF' for char in raw_analysis)
            xetu_enrichment = ""

            if has_assamese_script:
                import re
                assamese_phrases = re.findall(r'[\u0980-\u09FF\s]{5,}', raw_analysis)
                if assamese_phrases:
                    sample_phrase = assamese_phrases[0].strip()
                    xetu_res = xetu_translator.translate_assamese_to_english(sample_phrase)
                    if xetu_res.get("success") and xetu_res.get("translated_text"):
                        xetu_enrichment = (
                            f"\n\n---\n"
                            f"🌉 **Axom AI Xetu (সেতু) Verified Translation**:\n"
                            f"- *Original Assamese*: \"{sample_phrase}\"\n"
                            f"- *Native English*: \"{xetu_res.get('translated_text')}\"\n"
                            f"- *Linguistic Engine*: `{xetu_res.get('engine')}`"
                        )

            final_output = raw_analysis + xetu_enrichment

            return {
                "success": True,
                "analysis": final_output,
                "model_used": model_used,
                "xetu_active": bool(xetu_enrichment),
                "mime_type": detected_mime
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Vision analysis failed: {str(e)}"
            }

vision_engine = VisionEngine()
