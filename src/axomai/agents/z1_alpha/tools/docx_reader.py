import docx
from pathlib import Path
from typing import Dict, Any, Optional, List
from axomai.agents.z1_alpha.tools.base import BaseFileTool
from axomai.core.udm import (
    UnifiedDocumentModel,
    DocumentPage,
    ExtractedTable,
    DocumentSection
)

class DocxReaderTool(BaseFileTool):
    name = "docx_reader"
    description = "Extracts structured text, headings, and tables from DOCX Word files"
    supported_extensions = {".docx", ".doc"}

    def parse(self, file_path: str | Path, options: Optional[Dict[str, Any]] = None) -> UnifiedDocumentModel:
        file_info = self.get_file_info(file_path, "DOCX")
        doc = docx.Document(file_info.file_path)

        paragraphs_text = []
        sections: List[DocumentSection] = []
        all_tables: List[ExtractedTable] = []
        total_words = 0

        # Read Paragraphs and Headings
        for p in doc.paragraphs:
            text = p.text.strip()
            if not text:
                continue

            paragraphs_text.append(text)
            words = len(text.split())
            total_words += words

            if p.style.name.startswith("Heading"):
                try:
                    level = int(p.style.name.replace("Heading", "").strip())
                except ValueError:
                    level = 1
                sections.append(DocumentSection(
                    title=text,
                    level=level,
                    content="",
                    page_number=1
                ))

        # Read Tables
        for t_idx, table in enumerate(doc.tables):
            raw_rows = []
            for row in table.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                raw_rows.append(row_data)

            headers = raw_rows[0] if raw_rows else []
            data_rows = raw_rows[1:] if len(raw_rows) > 1 else []

            table_obj = ExtractedTable(
                table_id=f"doc_t{t_idx+1}",
                page_number=1,
                headers=headers,
                rows=data_rows,
                row_count=len(data_rows),
                column_count=len(headers)
            )
            all_tables.append(table_obj)

        full_text = "\n\n".join(paragraphs_text)

        # Word docs do not have native fixed pages without rendering, treated as 1 unified page or section
        page = DocumentPage(
            page_number=1,
            text=full_text,
            sections=sections,
            tables=all_tables,
            images=[],
            metadata={"paragraphs_count": len(paragraphs_text)}
        )

        # Document core properties
        core_props = doc.core_properties
        meta = {
            "title": core_props.title,
            "author": core_props.author,
            "created": str(core_props.created) if core_props.created else None,
            "modified": str(core_props.modified) if core_props.modified else None
        }

        return UnifiedDocumentModel(
            file=file_info,
            metadata=meta,
            page_count=1,
            pages=[page],
            tables=all_tables,
            images=[],
            stats={
                "total_words": total_words,
                "total_tables": len(all_tables),
                "total_images": 0
            }
        )

