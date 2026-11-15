"""
Z7 Visionary - Autonomous PowerPoint (PPTX) Deck Builder Tool.
Generates styled, boardroom-ready PowerPoint presentation files (.pptx)
with executive layouts, bullet cards, and financial takeaways.
"""

import uuid
from pathlib import Path
from typing import Dict, Any, List
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from axomai.config import settings

class PPTXBuilder:
    """Builds native Microsoft PowerPoint presentations."""

    def __init__(self):
        self.output_dir = settings.STORAGE_DIR / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_deck(
        self,
        title: str,
        subtitle: str,
        slides_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        prs = Presentation()
        # Set 16:9 widescreen
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

        blank_slide_layout = prs.slide_layouts[6] # blank layout

        # SLIDE 1: TITLE SLIDE (Navy/Dark Theme)
        slide1 = prs.slides.add_slide(blank_slide_layout)
        background = slide1.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(10, 15, 30) # Dark Navy

        txBox = slide1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.0))
        tf = txBox.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.bold = True
        p1.font.size = Pt(44)
        p1.font.color.rgb = RGBColor(0, 229, 255) # Cyan Accent
        p1.alignment = PP_ALIGN.LEFT

        p2 = tf.add_paragraph()
        p2.text = f"\n{subtitle}\nAxomAI AGI • Executive Boardroom Presentation"
        p2.font.size = Pt(20)
        p2.font.color.rgb = RGBColor(180, 200, 220)

        # SLIDES 2+: CONTENT SLIDES
        for s in slides_data:
            slide = prs.slides.add_slide(blank_slide_layout)
            bg = slide.background
            f = bg.fill
            f.solid()
            f.fore_color.rgb = RGBColor(15, 23, 42) # Slate Dark

            # Header
            header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(1.2))
            htf = header_box.text_frame
            hp = htf.paragraphs[0]
            hp.text = s.get("heading", "Strategic Insight")
            hp.font.bold = True
            hp.font.size = Pt(28)
            hp.font.color.rgb = RGBColor(255, 255, 255)

            # Content bullets
            content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
            ctf = content_box.text_frame
            ctf.word_wrap = True

            bullets = s.get("bullets", [])
            for i, bullet in enumerate(bullets):
                bp = ctf.paragraphs[0] if i == 0 else ctf.add_paragraph()
                bp.text = f"•  {bullet}"
                bp.font.size = Pt(20)
                bp.font.color.rgb = RGBColor(203, 213, 225)
                bp.space_after = Pt(14)

        # Save to disk
        filename = f"deck_{uuid.uuid4().hex[:8]}.pptx"
        file_path = self.output_dir / filename
        prs.save(str(file_path))

        return {
            "filename": filename,
            "file_path": str(file_path),
            "download_url": f"/api/download/generated/{filename}",
            "slide_count": len(slides_data) + 1,
            "title": title
        }

pptx_builder = PPTXBuilder()

