import pptx
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pathlib import Path
from typing import Dict, Any, Optional, List
from axomai.agents.z1_alpha.tools.base import BaseFileTool
from axomai.core.udm import (
    UnifiedDocumentModel,
    DocumentPage,
    ExtractedTable,
    DocumentSection
)

class PPTXReaderTool(BaseFileTool):
    name = "pptx_reader"
    description = "Extracts slides, slide titles, bullet points, tables, and speaker notes from PowerPoint presentations"
    supported_extensions = {".pptx", ".ppt"}

    def parse(self, file_path: str | Path, options: Optional[Dict[str, Any]] = None) -> UnifiedDocumentModel:
        file_info = self.get_file_info(file_path, "PPTX")
        prs = pptx.Presentation(file_info.file_path)

        pages: List[DocumentPage] = []
        all_tables: List[ExtractedTable] = []
        total_words = 0

        for slide_idx, slide in enumerate(prs.slides):
            slide_num = slide_idx + 1
            slide_texts = []
            slide_tables: List[ExtractedTable] = []
            slide_title = None

            # Detect title if present
            if slide.shapes.title and slide.shapes.title.text.strip():
                slide_title = slide.shapes.title.text.strip()
                slide_texts.append(f"## Slide {slide_num}: {slide_title}")

            # Iterate shapes
            for shape_idx, shape in enumerate(slide.shapes):
                # Text Frames
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        text = paragraph.text.strip()
                        if text and text != slide_title:
                            slide_texts.append(f"- {text}")
                            total_words += len(text.split())

                # Tables
                if shape.has_table:
                    table = shape.table
                    raw_rows = []
                    for row in table.rows:
                        row_data = [cell.text.strip() for cell in row.cells]
                        raw_rows.append(row_data)

                    headers = raw_rows[0] if raw_rows else []
                    data_rows = raw_rows[1:] if len(raw_rows) > 1 else []

                    table_obj = ExtractedTable(
                        table_id=f"slide{slide_num}_t{shape_idx+1}",
                        page_number=slide_num,
                        title=f"Slide {slide_num} Table",
                        headers=headers,
                        rows=data_rows,
                        row_count=len(data_rows),
                        column_count=len(headers)
                    )
                    slide_tables.append(table_obj)
                    all_tables.append(table_obj)

            # Speaker Notes
            notes_text = ""
            if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
                notes_text = slide.notes_slide.notes_text_frame.text.strip()
                if notes_text:
                    slide_texts.append(f"\n*Speaker Notes:* {notes_text}")

            full_slide_text = "\n".join(slide_texts)

            sections = []
            if slide_title:
                sections.append(DocumentSection(title=slide_title, level=1, content=full_slide_text, page_number=slide_num))

            pages.append(DocumentPage(
                page_number=slide_num,
                text=full_slide_text,
                sections=sections,
                tables=slide_tables,
                images=[],
                metadata={"title": slide_title, "has_notes": bool(notes_text)}
            ))

        return UnifiedDocumentModel(
            file=file_info,
            metadata={"total_slides": len(prs.slides)},
            page_count=len(prs.slides),
            pages=pages,
            tables=all_tables,
            images=[],
            stats={
                "total_slides": len(prs.slides),
                "total_words": total_words,
                "total_tables": len(all_tables)
            }
        )

