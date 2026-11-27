"""
Z7 Visionary - Surgical Slide-by-Slide PPTX Editor.
Opens an existing .pptx presentation on disk, updates a specific slide number
(heading/bullets) or appends a new slide cleanly without rebuilding the entire deck.
"""

import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

from axomai.config import settings


class SurgicalSlideEditor:
    """Performs targeted surgical edits on existing .pptx files."""

    def __init__(self):
        self.output_dir = settings.STORAGE_DIR / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def edit_existing_slide(
        self,
        source_filename: str,
        slide_number: int = 2,
        new_heading: Optional[str] = None,
        new_bullets: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        src_path = self.output_dir / Path(source_filename).name
        if not src_path.exists():
            return {"status": "FILE_NOT_FOUND", "source_filename": source_filename}

        prs = Presentation(str(src_path))
        total = len(prs.slides)
        idx = max(0, min(total - 1, slide_number - 1))
        slide = prs.slides[idx]

        updated_fields = []
        text_shapes = [sh for sh in slide.shapes if sh.has_text_frame]
        if new_heading and len(text_shapes) >= 1:
            text_shapes[0].text_frame.paragraphs[0].text = new_heading
            updated_fields.append("heading")
        if new_bullets and len(text_shapes) >= 2:
            tf = text_shapes[1].text_frame
            tf.clear()
            for i, b in enumerate(new_bullets):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                p.text = f"▸  {b}"
                p.font.size = Pt(19)
                p.font.color.rgb = RGBColor(226, 232, 240)
            updated_fields.append("bullets")

        out_name = f"edited_{uuid.uuid4().hex[:6]}_{src_path.name}"
        out_path = self.output_dir / out_name
        prs.save(str(out_path))

        return {
            "status": "SURGICAL_EDIT_SUCCESS",
            "edited_slide_number": idx + 1,
            "updated_fields": updated_fields,
            "filename": out_name,
            "download_url": f"/api/download/generated/{out_name}",
            "total_slides": total
        }


surgical_slide_editor = SurgicalSlideEditor()
