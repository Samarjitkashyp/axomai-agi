from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TableCell(BaseModel):
    value: Any
    row_span: int = 1
    col_span: int = 1

class ExtractedTable(BaseModel):
    table_id: str
    page_number: Optional[int] = None
    sheet_name: Optional[str] = None
    title: Optional[str] = None
    headers: List[str] = Field(default_factory=list)
    rows: List[List[Any]] = Field(default_factory=list)
    row_count: int = 0
    column_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_markdown(self) -> str:
        """Convert table to readable Markdown for LLMs"""
        if not self.headers and not self.rows:
            return ""
        
        md_lines = []
        if self.title:
            md_lines.append(f"### Table: {self.title}")
            
        cols = self.headers if self.headers else [f"Col {i+1}" for i in range(self.column_count)]
        md_lines.append("| " + " | ".join(str(c) for c in cols) + " |")
        md_lines.append("| " + " | ".join(["---"] * len(cols)) + " |")
        
        for r in self.rows[:50]: # limit preview to 50 rows in markdown string
            row_str = [str(cell) if cell is not None else "" for cell in r]
            # pad or truncate if length mismatch
            if len(row_str) < len(cols):
                row_str.extend([""] * (len(cols) - len(row_str)))
            elif len(row_str) > len(cols):
                row_str = row_str[:len(cols)]
            md_lines.append("| " + " | ".join(row_str) + " |")
            
        if len(self.rows) > 50:
            md_lines.append(f"\n*(... {len(self.rows) - 50} more rows truncated for prompt)*")
            
        return "\n".join(md_lines)


class ExtractedImage(BaseModel):
    image_id: str
    page_number: Optional[int] = None
    format: str = "png"
    width: Optional[int] = None
    height: Optional[int] = None
    caption: Optional[str] = None
    ocr_text: Optional[str] = None
    saved_path: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DocumentSection(BaseModel):
    title: Optional[str] = None
    level: int = 1 # 1=H1, 2=H2, etc.
    content: str
    page_number: Optional[int] = None


class DocumentPage(BaseModel):
    page_number: int # 1-based index
    text: str = ""
    sections: List[DocumentSection] = Field(default_factory=list)
    tables: List[ExtractedTable] = Field(default_factory=list)
    images: List[ExtractedImage] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FileInfo(BaseModel):
    filename: str
    file_path: str
    file_type: str # PDF, DOCX, XLSX, PPTX, CSV, TXT, IMAGE, etc.
    mime_type: Optional[str] = None
    file_size_bytes: int
    file_hash: str # SHA256


class UnifiedDocumentModel(BaseModel):
    """
    Unified Document Model (UDM)
    Standard representation across all document types (PDF, Word, Excel, PPT, CSV, Images)
    """
    file: FileInfo
    metadata: Dict[str, Any] = Field(default_factory=dict)
    page_count: int = 1
    pages: List[DocumentPage] = Field(default_factory=list)
    
    # Aggregated references for quick agent lookup
    tables: List[ExtractedTable] = Field(default_factory=list)
    images: List[ExtractedImage] = Field(default_factory=list)
    
    stats: Dict[str, Any] = Field(default_factory=lambda: {
        "total_words": 0,
        "total_tables": 0,
        "total_images": 0
    })

    def get_full_text(self, max_pages: Optional[int] = None) -> str:
        """Concatenate text from pages"""
        target_pages = self.pages[:max_pages] if max_pages else self.pages
        return "\n\n".join([f"--- Page {p.page_number} ---\n{p.text}" for p in target_pages if p.text.strip()])

    def get_page(self, page_number: int) -> Optional[DocumentPage]:
        """Get specific page by 1-based index"""
        for page in self.pages:
            if page.page_number == page_number:
                return page
        return None

