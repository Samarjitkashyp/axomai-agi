import fitz # PyMuPDF
import pdfplumber
from pathlib import Path
from typing import Dict, Any, Optional, List
from axomai.agents.z1_alpha.tools.base import BaseFileTool
from axomai.core.udm import (
    UnifiedDocumentModel,
    DocumentPage,
    ExtractedTable,
    ExtractedImage,
    DocumentSection
)

class PDFReaderTool(BaseFileTool):
    name = "pdf_reader"
    description = "Extracts structured text, tables, images and layout from PDF files"
    supported_extensions = {".pdf"}

    def parse(self, file_path: str | Path, options: Optional[Dict[str, Any]] = None) -> UnifiedDocumentModel:
        options = options or {}
        extract_tables = options.get("extract_tables", True)
        extract_images = options.get("extract_images", True)
        max_pages = options.get("max_pages", None)

        file_info = self.get_file_info(file_path, "PDF")
        doc_fitz = fitz.open(file_info.file_path)
        total_pages = len(doc_fitz)
        limit_pages = min(total_pages, max_pages) if max_pages else total_pages

        pages: List[DocumentPage] = []
        all_tables: List[ExtractedTable] = []
        all_images: List[ExtractedImage] = []
        total_words = 0

        # Step 1: Open pdfplumber for table detection if requested
        plumber_doc = None
        if extract_tables:
            try:
                plumber_doc = pdfplumber.open(file_info.file_path)
            except Exception:
                plumber_doc = None

        try:
            for page_idx in range(limit_pages):
                page_num = page_idx + 1
                fitz_page = doc_fitz[page_idx]
                page_text = fitz_page.get_text("text")
                words_count = len(page_text.split())
                total_words += words_count

                # Extract Tables via pdfplumber
                page_tables: List[ExtractedTable] = []
                if plumber_doc and page_idx < len(plumber_doc.pages):
                    try:
                        p_page = plumber_doc.pages[page_idx]
                        extracted_raw_tables = p_page.extract_tables()
                        for t_idx, raw_table in enumerate(extracted_raw_tables):
                            if not raw_table or len(raw_table) == 0:
                                continue
                            
                            # Clean rows
                            cleaned_rows = [
                                [str(cell).strip() if cell is not None else "" for cell in r]
                                for r in raw_table
                            ]
                            headers = cleaned_rows[0] if cleaned_rows else []
                            data_rows = cleaned_rows[1:] if len(cleaned_rows) > 1 else []

                            table_obj = ExtractedTable(
                                table_id=f"p{page_num}_t{t_idx+1}",
                                page_number=page_num,
                                headers=headers,
                                rows=data_rows,
                                row_count=len(data_rows),
                                column_count=len(headers)
                            )
                            page_tables.append(table_obj)
                            all_tables.append(table_obj)
                    except Exception:
                        pass

                # Extract Images info via PyMuPDF
                page_images: List[ExtractedImage] = []
                if extract_images:
                    image_list = fitz_page.get_images(full=True)
                    for img_idx, img_info in enumerate(image_list):
                        xref = img_info[0]
                        base_image = doc_fitz.extract_image(xref)
                        img_format = base_image.get("ext", "png")
                        width = base_image.get("width")
                        height = base_image.get("height")

                        img_obj = ExtractedImage(
                            image_id=f"p{page_num}_img{img_idx+1}",
                            page_number=page_num,
                            format=img_format,
                            width=width,
                            height=height,
                            metadata={"xref": xref}
                        )
                        page_images.append(img_obj)
                        all_images.append(img_obj)

                # Page Sections (simple heuristic based on text blocks)
                sections = []
                blocks = fitz_page.get_text("blocks")
                for b in blocks:
                    block_text = b[4].strip()
                    if block_text and len(block_text.split("\n")) <= 2 and len(block_text) < 100:
                        sections.append(DocumentSection(
                            title=block_text,
                            content="",
                            page_number=page_num
                        ))

                pages.append(DocumentPage(
                    page_number=page_num,
                    text=page_text,
                    sections=sections,
                    tables=page_tables,
                    images=page_images,
                    metadata={"char_count": len(page_text), "word_count": words_count}
                ))
        finally:
            doc_fitz.close()
            if plumber_doc:
                plumber_doc.close()

        # Document metadata
        meta = {
            "format": doc_fitz.metadata.get("format") if hasattr(doc_fitz, "metadata") else "PDF",
            "title": doc_fitz.metadata.get("title") if hasattr(doc_fitz, "metadata") else None,
            "author": doc_fitz.metadata.get("author") if hasattr(doc_fitz, "metadata") else None,
        }

        return UnifiedDocumentModel(
            file=file_info,
            metadata=meta,
            page_count=total_pages,
            pages=pages,
            tables=all_tables,
            images=all_images,
            stats={
                "total_words": total_words,
                "total_tables": len(all_tables),
                "total_images": len(all_images)
            }
        )

