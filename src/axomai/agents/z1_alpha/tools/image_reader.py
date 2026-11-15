from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image

from axomai.agents.z1_alpha.tools.base import BaseFileTool
from axomai.core.udm import (
    UnifiedDocumentModel,
    DocumentPage,
    ExtractedImage
)

class ImageReaderTool(BaseFileTool):
    name = "image_reader"
    description = "Inspects image files, extracts image metadata, resolution, and prepares visual payload for Vision LLM"
    supported_extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".gif"}

    def parse(self, file_path: str | Path, options: Optional[Dict[str, Any]] = None) -> UnifiedDocumentModel:
        file_info = self.get_file_info(file_path, "IMAGE")
        path = Path(file_info.file_path)

        with Image.open(path) as img:
            width, height = img.size
            img_format = img.format or path.suffix.lstrip(".").upper()
            mode = img.mode
            info = img.info or {}

        img_obj = ExtractedImage(
            image_id="img_primary_1",
            page_number=1,
            format=img_format.lower(),
            width=width,
            height=height,
            saved_path=str(path.resolve()),
            metadata={
                "color_mode": mode,
                "dpi": info.get("dpi"),
                "aspect_ratio": round(width / height, 2) if height else 1.0
            }
        )

        page_text = (
            f"### Image File: {file_info.filename}\n"
            f"- Format: {img_format}\n"
            f"- Dimensions: {width} × {height} pixels\n"
            f"- Aspect Ratio: {round(width / height, 2) if height else 'N/A'}\n"
            f"- Color Mode: {mode}\n"
            f"- File Size: {file_info.file_size_bytes / 1024:.1f} KB\n"
        )

        page = DocumentPage(
            page_number=1,
            text=page_text,
            tables=[],
            images=[img_obj],
            metadata={"width": width, "height": height, "format": img_format}
        )

        return UnifiedDocumentModel(
            file=file_info,
            metadata={"format": img_format, "width": width, "height": height, "mode": mode},
            page_count=1,
            pages=[page],
            tables=[],
            images=[img_obj],
            stats={
                "total_images": 1,
                "resolution": f"{width}x{height}",
                "format": img_format
            }
        )

