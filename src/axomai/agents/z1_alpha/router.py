import re
from pathlib import Path
from typing import Dict, Type, Optional, Tuple
from axomai.agents.z1_alpha.tools.base import BaseFileTool
from axomai.agents.z1_alpha.tools.pdf_reader import PDFReaderTool
from axomai.agents.z1_alpha.tools.docx_reader import DocxReaderTool
from axomai.agents.z1_alpha.tools.xlsx_reader import XLSXReaderTool
from axomai.agents.z1_alpha.tools.pptx_reader import PPTXReaderTool
from axomai.agents.z1_alpha.tools.text_reader import TextReaderTool
from axomai.agents.z1_alpha.tools.csv_reader import CSVReaderTool
from axomai.agents.z1_alpha.tools.image_reader import ImageReaderTool

class TaskType:
    SUMMARY = "SUMMARY"
    PAGE_QUERY = "PAGE_QUERY"
    TABLE_EXTRACT = "TABLE_EXTRACT"
    IMAGE_QUERY = "IMAGE_QUERY"
    IMAGE_ANALYSIS = "IMAGE_ANALYSIS"
    CHART_ANALYSIS = "CHART_ANALYSIS"
    OCR_TEXT = "OCR_TEXT"
    DATA_ANALYSIS = "DATA_ANALYSIS"
    AUDIT = "AUDIT"
    FILE_GENERATION = "FILE_GENERATION"
    SEARCH = "SEARCH"
    GENERAL_QA = "GENERAL_QA"

class ToolRouter:
    """
    Z1 Alpha Tool Router & Task Detector
    Matches file format to the correct tool and determines the task intent.
    """
    def __init__(self):
        self.tools: Dict[str, BaseFileTool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        registered_classes = [
            PDFReaderTool,
            DocxReaderTool,
            XLSXReaderTool,
            PPTXReaderTool,
            TextReaderTool,
            CSVReaderTool,
            ImageReaderTool
        ]
        for cls in registered_classes:
            tool_instance = cls()
            for ext in cls.supported_extensions:
                self.tools[ext.lower()] = tool_instance

    def route_file(self, file_path: str | Path) -> BaseFileTool:
        """Find the appropriate reader tool based on file extension"""
        path = Path(file_path)
        ext = path.suffix.lower()
        tool = self.tools.get(ext)
        if not tool:
            raise ValueError(f"No specialized reader tool registered for extension '{ext}' (File: {path.name})")
        return tool

    def detect_task(self, query: str) -> Tuple[str, Dict[str, any]]:
        """
        Classifies user intent from natural language query
        Returns: (TaskType, parameters_dict)
        """
        q = query.lower().strip()
        params = {}

        # 1. OCR text extraction
        if any(w in q for w in ["ocr", "transcribe", "likha hua text", "text nikalo", "extract text", "read text", "kya likha he", "kya likha hai"]):
            return TaskType.OCR_TEXT, params

        # 2. Chart, Graph, Diagram, Visual Workflow analysis
        if any(w in q for w in ["chart", "graph", "diagram", "flowchart", "architecture", "trend", "graphics", "plot", "bar chart", "pie chart", "axis"]):
            return TaskType.CHART_ANALYSIS, params

        # 3. General Image Scene / Visual inspection
        if any(w in q for w in ["image me kya hai", "image mein kya", "photo me kya", "describe image", "scene", "kya dekh raha hai"]):
            return TaskType.IMAGE_ANALYSIS, params

        # 4. Page query detection (e.g. "page 27 par kya likha hai", "what is on page 5")
        page_match = re.search(r'\bpage\s*(?:no\.?|number)?\s*(\d+)\b', q)
        if page_match:
            params["page_number"] = int(page_match.group(1))
            return TaskType.PAGE_QUERY, params

        # 5. Summary detection
        if any(w in q for w in ["summary", "summarize", "overview", "kya hai isme", "brief", "main points"]):
            return TaskType.SUMMARY, params

        # 6. Table detection
        if any(w in q for w in ["table", "tables", "tabular", "columns", "rows"]):
            return TaskType.TABLE_EXTRACT, params

        # 7. Image count/presence query
        if any(w in q for w in ["kitne photo", "kitni image", "how many images", "has images"]):
            return TaskType.IMAGE_QUERY, params

        # 8. Audit & Error Detection (Spreadsheets)
        if any(w in q for w in ["audit", "check error", "formula error", "anomaly", "health check", "corrupt", "duplicate", "clean sheet", "validate", "kharaabi", "galti", "mistake", "error check"]):
            return TaskType.AUDIT, params

        # 9. Autonomous File Creation & Downloader (Word DOCX, PDF, Excel, CSV)
        docx_patterns = [
            "docx", "doc file", "word file", "word doc", "word document", "doc bana", 
            "word bana", "generate doc", "gnerate doc", "make doc", "create doc", 
            "export doc", "save as doc", "save as word", "doc bhi", "doc format", 
            "word me", "word mein", "generate word", "ms word"
        ]
        pdf_patterns = [
            "pdf", "pdf file", "generate pdf", "gnerate pdf", "make pdf", "create pdf", 
            "export pdf", "export to pdf", "save as pdf", "convert to pdf", "pdf bana", 
            "pdf download", "pdf report", "download pdf", "pdf chahiye"
        ]
        file_gen_patterns = [
            "download", "bana kar do", "file bana", "create file", "export to excel", 
            "generate excel", "gnerate excel", "export csv", "download link", "nayi file", 
            "save as excel", "save as csv", "generate file", "gnerate file", "naya excel", 
            "nayi excel", "new file", "export clean", "export as", "make file", "create a file",
            "make a pdf", "give me pdf", "provide pdf"
        ]

        is_docx_intent = any(p in q for p in docx_patterns) or (any(w in q for w in ["doc", "docx", "word"]) and any(w in q for w in ["generate", "gnerate", "make", "create", "bana", "export", "download", "convert", "file", "layeak", "layak"]))
        is_pdf_intent = any(p in q for p in pdf_patterns) or ("pdf" in q and any(w in q for w in ["generate", "gnerate", "make", "create", "bana", "export", "download", "convert", "file"]))
        is_general_file_intent = any(w in q for w in file_gen_patterns)

        if is_docx_intent:
            params["format"] = "docx"
            return TaskType.FILE_GENERATION, params

        if is_pdf_intent:
            params["format"] = "pdf"
            return TaskType.FILE_GENERATION, params

        if is_general_file_intent:
            if "docx" in q or "word" in q:
                params["format"] = "docx"
            elif "csv" in q:
                params["format"] = "csv"
            elif "pdf" in q:
                params["format"] = "pdf"
            else:
                params["format"] = "xlsx"
            return TaskType.FILE_GENERATION, params

        # 10. Data / Calculation analysis
        if any(w in q for w in ["total", "sum", "average", "highest", "lowest", "max", "min", "sales", "revenue", "bonus"]):
            return TaskType.DATA_ANALYSIS, params

        # 11. Search query
        if any(w in q for w in ["find", "search", "dhundo", "kahan likha hai"]):
            return TaskType.SEARCH, params

        return TaskType.GENERAL_QA, params
