from pathlib import Path
from typing import Dict, Any, Optional, List
from axomai.agents.z1_alpha.tools.base import BaseFileTool
from axomai.core.udm import (
    UnifiedDocumentModel,
    DocumentPage,
    DocumentSection
)

class TextReaderTool(BaseFileTool):
    name = "text_reader"
    description = "Reads plain text, Markdown, JSON, YAML, and log files"
    supported_extensions = {".txt", ".md", ".markdown", ".log", ".json", ".yaml", ".yml"}

    def parse(self, file_path: str | Path, options: Optional[Dict[str, Any]] = None) -> UnifiedDocumentModel:
        file_info = self.get_file_info(file_path, "TEXT")
        
        # Read with utf-8 fallback to latin-1
        try:
            with open(file_info.file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_info.file_path, "r", encoding="latin-1") as f:
                content = f.read()

        words = len(content.split())
        lines = content.splitlines()

        # Simple section detection for Markdown
        sections: List[DocumentSection] = []
        for line in lines:
            if line.startswith("#"):
                header_level = len(line) - len(line.lstrip("#"))
                title = line.lstrip("#").strip()
                if title:
                    sections.append(DocumentSection(title=title, level=header_level, content="", page_number=1))

        page = DocumentPage(
            page_number=1,
            text=content,
            sections=sections,
            tables=[],
            images=[],
            metadata={"lines_count": len(lines), "word_count": words}
        )

        return UnifiedDocumentModel(
            file=file_info,
            metadata={"lines": len(lines)},
            page_count=1,
            pages=[page],
            tables=[],
            images=[],
            stats={
                "total_words": words,
                "total_lines": len(lines),
                "total_tables": 0,
                "total_images": 0
            }
        )

