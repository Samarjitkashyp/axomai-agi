import os
import json
import uuid
from typing import Dict, Any, Optional, List, Generator
from pathlib import Path
import fitz # PyMuPDF
from rich.console import Console

from axomai.config import settings
from axomai.db.session import SyncSessionLocal
from axomai.db.models import Document, DocumentChunk, AgentSession, AgentTaskLog
from axomai.core.udm import UnifiedDocumentModel
from axomai.core.llm import llm_brain
from axomai.core.vision import vision_engine
from axomai.core.retriever import retriever
from axomai.agents.z1_alpha.router import ToolRouter, TaskType
from axomai.agents.z1_alpha.tools.code_interpreter import data_engine
from axomai.agents.z1_alpha.tools.pdf_generator import pdf_generator_engine
from axomai.agents.z1_alpha.tools.docx_generator import docx_generator_engine

console = Console()

class Z1AlphaAgent:
    """
    Z1 Alpha - Autonomous File Intelligence Agent
    Orchestrates file parsing, multimodal vision understanding, task detection,
    pandas code execution sandbox, PostgreSQL caching, and LLM grounded reasoning.
    """
    def __init__(self):
        self.name = "Z1 Alpha"
        self.role = "Autonomous File Intelligence Agent"
        self.router = ToolRouter()

    def process_file(self, file_path: str | Path, force_reparse: bool = False) -> UnifiedDocumentModel:
        """
        Processes a file, normalizes it to UDM, and caches it in PostgreSQL.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        tool = self.router.route_file(path)
        file_info = tool.get_file_info(path, path.suffix.lstrip(".").upper())

        with SyncSessionLocal() as db:
            if not force_reparse:
                existing_doc = db.query(Document).filter(Document.file_hash == file_info.file_hash).first()
                if existing_doc and existing_doc.udm_data:
                    existing_doc.file_path = str(path.resolve())
                    existing_doc.filename = path.name
                    db.commit()
                    console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Found cached UDM in PostgreSQL for [yellow]{path.name}[/yellow]")
                    return UnifiedDocumentModel.model_validate(existing_doc.udm_data)

            console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Routing [yellow]{path.name}[/yellow] to tool: [green]{tool.name}[/green]")
            udm = tool.parse(path)

            if existing_doc := db.query(Document).filter(Document.file_hash == file_info.file_hash).first():
                existing_doc.udm_data = udm.model_dump()
                existing_doc.page_count = udm.page_count
                existing_doc.file_size_bytes = udm.file.file_size_bytes
                doc_record = existing_doc
            else:
                doc_record = Document(
                    id=uuid.uuid4(),
                    filename=udm.file.filename,
                    file_path=udm.file.file_path,
                    file_type=udm.file.file_type,
                    mime_type=udm.file.mime_type,
                    file_size_bytes=udm.file.file_size_bytes,
                    file_hash=udm.file.file_hash,
                    page_count=udm.page_count,
                    udm_data=udm.model_dump(),
                    metadata_=udm.metadata
                )
                db.add(doc_record)
                db.flush()

            # Create Chunks for fast search & evidence retrieval
            db.query(DocumentChunk).filter(DocumentChunk.document_id == doc_record.id).delete()
            
            chunk_idx = 0
            for page in udm.pages:
                if page.text.strip():
                    db.add(DocumentChunk(
                        document_id=doc_record.id,
                        chunk_index=chunk_idx,
                        page_number=page.page_number,
                        content_type="text",
                        content=page.text,
                        chunk_metadata=page.metadata
                    ))
                    chunk_idx += 1

                for table in page.tables:
                    db.add(DocumentChunk(
                        document_id=doc_record.id,
                        chunk_index=chunk_idx,
                        page_number=page.page_number,
                        content_type="table",
                        content=table.to_markdown(),
                        chunk_metadata={"table_id": table.table_id, "rows": table.row_count, "cols": table.column_count}
                    ))
                    chunk_idx += 1

                for img in page.images:
                    db.add(DocumentChunk(
                        document_id=doc_record.id,
                        chunk_index=chunk_idx,
                        page_number=page.page_number,
                        content_type="image_metadata",
                        content=f"Image: {img.image_id} (Format: {img.format}, Dimensions: {img.width}x{img.height})",
                        chunk_metadata={"image_id": img.image_id, "format": img.format}
                    ))
                    chunk_idx += 1

            db.commit()
            console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Saved UDM + {chunk_idx} chunks to PostgreSQL for [yellow]{path.name}[/yellow]")
            return udm

    def generate_auto_summary(self, file_path: str | Path, udm: Optional[UnifiedDocumentModel] = None) -> Dict[str, Any]:
        """
        Generates an instant executive overview + 3 tailored smart follow-up prompts
        immediately upon file upload, without the user having to type anything.
        """
        path = Path(file_path)
        if not udm:
            udm = self.process_file(path)

        is_image = udm.file.file_type == "IMAGE"
        
        # If it's an image, use vision engine to get the initial brief in English
        if is_image:
            vis_res = vision_engine.analyze(
                image_input=path,
                question="Provide a clear, professional 3-bullet executive summary in English explaining what is visible in this image.",
                task_mode="comprehensive"
            )
            raw_text = vis_res.get("analysis", "") if vis_res.get("success") else "Image analysis ready."
            prompts = [
                "Transcribe all visible text from this image (OCR)",
                "Explain the visual design, colors, and layout details",
                "Extract all brand names, headlines, and call-to-actions"
            ]
            return {
                "summary": raw_text,
                "prompts": prompts
            }

        # For text / PDF / Excel / Word / Presentations
        context_snippet = udm.get_full_text(max_pages=2)[:1500]
        tables_preview = ""
        if udm.tables:
            tables_preview = f"\nExtracted Tables ({len(udm.tables)}): " + ", ".join([t.title or t.table_id for t in udm.tables[:2]])

        system_prompt = (
            "You are Z1 Alpha, an Autonomous File Intelligence Agent.\n"
            "Analyze the provided document excerpt and return a JSON object with:\n"
            "1. 'summary': A concise, high-value 3-bullet executive overview strictly in professional English explaining what this document is about.\n"
            "2. 'prompts': Exactly 3 smart, specific follow-up questions in English tailored to this file that the user can ask.\n"
            "Return STRICT JSON only format: {\"summary\": [\"bullet 1\", \"bullet 2\", \"bullet 3\"], \"prompts\": [\"question 1\", \"question 2\", \"question 3\"]}"
        )

        user_prompt = (
            f"Filename: {udm.file.filename}\n"
            f"Type: {udm.file.file_type} | Pages: {udm.page_count} {tables_preview}\n\n"
            f"Content excerpt:\n{context_snippet}\n"
        )

        try:
            raw_json_res = llm_brain.generate(system_prompt, user_prompt, temperature=0.1)
            clean_str = raw_json_res.strip()
            if "```json" in clean_str:
                clean_str = clean_str.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_str:
                clean_str = clean_str.split("```")[1].split("```")[0].strip()
            data = json.loads(clean_str)
            summary_val = data.get("summary", "")
            if isinstance(summary_val, list):
                summary_val = "\n".join([f"- {s}" for s in summary_val])
            elif not summary_val:
                summary_val = f"**{udm.file.filename}** ({udm.file.file_type}) successfully processed with {udm.page_count} page(s)."

            return {
                "summary": summary_val,
                "prompts": data.get("prompts", ["What is this document about?", "Summarize the key findings", "Show all extracted data"])
            }
        except Exception:
            return {
                "summary": f"**{udm.file.filename}** ({udm.file.file_type}) has been parsed successfully with {udm.page_count} page(s).",
                "prompts": [
                    "Give me a comprehensive summary of this document",
                    "What are the most critical takeaways?",
                    "Are there any key tables, numbers, or statistics?"
                ]
            }

    def query(
        self,
        question: str,
        file_path: str | Path,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end intelligence workflow:
        1. Retrieve or parse UDM from PostgreSQL
        2. Detect Task Type (Summary, Page, Table, Data Math, Image/Chart Analysis, OCR)
        3. Multimodal Vision Handling for Images or Rendered PDF Pages
        4. Pandas Sandbox for Excel/CSV data math
        5. Grounded LLM reasoning with citations
        6. Store interaction in PostgreSQL
        """
        session_id = session_id or str(uuid.uuid4())[:8]
        path = Path(file_path)
        udm = self.process_file(path)

        # Detect Task
        task_type, params = self.router.detect_task(question)
        console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Detected Task: [bold magenta]{task_type}[/bold magenta] (Params: {params})")

        tools_used = [self.router.route_file(path).name]
        evidence: List[Dict[str, Any]] = []
        answer_text = ""
        chart_data = None
        generated_file_data = None

        is_image = udm.file.file_type == "IMAGE"
        is_tabular = udm.file.file_type in ["XLSX", "XLS", "CSV", "TSV"]
        is_pdf = udm.file.file_type == "PDF"

        # --- CASE 1: MULTIMODAL VISION ENGINE FOR IMAGES ---
        if is_image:
            console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Invoking [bold cyan]Vision Intelligence Engine[/bold cyan]...")
            
            if task_type == TaskType.CHART_ANALYSIS:
                mode = "chart_analysis"
            elif task_type == TaskType.OCR_TEXT:
                mode = "ocr"
            else:
                mode = "comprehensive"

            vision_res = vision_engine.analyze(
                image_input=path,
                question=question,
                task_mode=mode
            )

            if vision_res.get("success"):
                tools_used.append(f"vision_engine ({vision_res.get('model_used')})")
                evidence.append({
                    "source": f"Visual Inspection of {udm.file.filename}",
                    "resolution": udm.stats.get("resolution", "N/A"),
                    "mode": mode,
                    "content_type": "image",
                    "snippet": f"Visual analysis performed on {udm.file.filename} using {vision_res.get('model_used')}."
                })
                answer_text = vision_res.get("analysis", "")
            else:
                answer_text = f"Vision Error: {vision_res.get('error')}"

        # --- CASE 2: PDF WITH CHARTS / SCANNED PAGES (RENDER PAGE TO VISION) ---
        elif is_pdf and task_type in [TaskType.CHART_ANALYSIS, TaskType.OCR_TEXT]:
            target_page_num = params.get("page_number", 1)
            target_idx = max(0, min(target_page_num - 1, udm.page_count - 1))
            
            console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Rendering PDF Page {target_idx + 1} for [bold cyan]Vision Engine[/bold cyan]...")
            try:
                pdf_doc = fitz.open(path)
                page = pdf_doc[target_idx]
                pix = page.get_pixmap(dpi=150)
                img_bytes = pix.tobytes("png")
                pdf_doc.close()

                mode = "chart_analysis" if task_type == TaskType.CHART_ANALYSIS else "ocr"
                vision_res = vision_engine.analyze(
                    image_input=img_bytes,
                    question=question,
                    task_mode=mode,
                    mime_type="image/png"
                )

                if vision_res.get("success"):
                    tools_used.extend(["pdf_renderer", f"vision_engine ({vision_res.get('model_used')})"])
                    evidence.append({
                        "source": f"Page {target_idx + 1} (High-Res Rendered Image)",
                        "page_number": target_idx + 1,
                        "mode": mode,
                        "content_type": "rendered_page",
                        "snippet": f"Page {target_idx + 1} of PDF rendered to high-res image and visually analyzed."
                    })
                    answer_text = (
                        f"### 👁️ Visual & Graphic Analysis (Page {target_idx + 1})\n\n"
                        f"{vision_res.get('analysis')}"
                    )
            except Exception as e:
                console.print(f"[red]PDF Page render vision failed: {e}[/red]")

        # --- CASE 3: PANDAS CODE SANDBOX & CHART VISUALIZATION FOR EXCEL / CSV ---
        elif is_tabular and (task_type in [TaskType.CHART_ANALYSIS, TaskType.DATA_ANALYSIS] or any(w in question.lower() for w in ["chart", "graph", "plot", "bar", "pie", "visual", "trend"])):
            is_visual_request = any(w in question.lower() for w in ["chart", "graph", "plot", "bar", "pie", "visual", "trend"]) or task_type == TaskType.CHART_ANALYSIS
            
            if is_visual_request:
                console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Invoking [bold cyan]Chart Visualization Engine[/bold cyan]...")
                chart_res = data_engine.generate_chart(path, question)
                if chart_res.get("success"):
                    tools_used.append("chart_visualizer")
                    chart_data = chart_res.get("chart")
                    evidence.append({
                        "source": f"Visual Chart Engine on {udm.file.filename}",
                        "content_type": "chart",
                        "snippet": f"Generated {chart_data.get('type', 'bar')} chart '{chart_data.get('title')}' with {len(chart_data.get('labels', []))} data series."
                    })
                    answer_text = (
                        f"### 📊 Interactive Visual Chart: {chart_data.get('title', 'Data Visualization')}\n\n"
                        f"The interactive {chart_data.get('type', 'bar')} chart has been rendered below from **{udm.file.filename}**.\n"
                    )

            if not answer_text and task_type == TaskType.DATA_ANALYSIS:
                console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Invoking [bold green]Pandas Code Engine[/bold green] for calculations...")
                calc_res = data_engine.analyze(path, question)
                if calc_res.get("success"):
                    tools_used.append("pandas_code_interpreter")
                    evidence.append({
                        "source": f"Pandas Code Sandbox on {udm.file.filename}",
                        "content_type": "calculation",
                        "calculation": calc_res.get("calculation"),
                        "code_snippet": calc_res.get("code"),
                        "snippet": f"Exact Code: {calc_res.get('code')}\n\nResult:\n{calc_res.get('calculation')}"
                    })
                    
                    answer_text = (
                        f"### 📊 Data Analysis Result\n\n"
                        f"**Exact Calculated Result:**\n```\n{calc_res.get('calculation')}\n```\n\n"
                        f"**Python Pandas Code Executed:**\n```python\n{calc_res.get('code')}\n```\n"
                    )

        # --- CASE 3B: SMART SPREADSHEET AUDIT ---
        elif is_tabular and task_type == TaskType.AUDIT:
            console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Executing [bold magenta]Smart Spreadsheet Audit[/bold magenta]...")
            audit_res = data_engine.audit_spreadsheet(path)
            if audit_res.get("success"):
                tools_used.append("spreadsheet_auditor")
                m = audit_res["metrics"]
                score = audit_res["health_score"]
                status = audit_res["health_status"]
                grade = audit_res["health_grade"]

                evidence.append({
                    "source": f"Spreadsheet Auditor on {udm.file.filename}",
                    "content_type": "audit_report",
                    "snippet": f"Audit: Health Score {score}/100 ({status}), {m['formula_errors_count']} formula errors, {m['duplicate_rows_count']} duplicates, {m['missing_values_count']} missing cells."
                })

                issues_md = []
                if audit_res["formula_errors"]:
                    issues_md.append("\n**⚠️ Formula / Calculation Errors:**")
                    for err in audit_res["formula_errors"][:5]:
                        issues_md.append(f"- Row {err['row']}, Column `{err['column']}`: `{err['error_type']}`")

                if audit_res["duplicate_rows"]:
                    issues_md.append(f"\n**⚠️ Duplicate Rows:** {len(audit_res['duplicate_rows'])} identical row(s) found at rows: {audit_res['duplicate_rows']}")

                if audit_res["negative_anomalies"]:
                    issues_md.append("\n**⚠️ Financial Anomalies (Negative Values):**")
                    for neg in audit_res["negative_anomalies"][:5]:
                        issues_md.append(f"- Row {neg['row']}, Column `{neg['column']}`: Value `{neg['value']}`")

                if audit_res["missing_by_column"]:
                    issues_md.append("\n**⚠️ Missing / Blank Data:**")
                    for col, inf in audit_res["missing_by_column"].items():
                        issues_md.append(f"- Column `{col}`: {inf['count']} missing values ({inf['percentage']}%)")

                recs_md = "\n".join([f"1. {r}" for r in audit_res["recommendations"]])
                issues_block = "\n".join(issues_md) if issues_md else "✅ **Zero errors detected.** All cells and formulas are valid."

                answer_text = (
                    f"### 🛡️ Smart Spreadsheet Audit Report\n\n"
                    f"**File:** `{udm.file.filename}` | **Total Rows:** {audit_res['total_rows']} | **Total Columns:** {audit_res['total_columns']}\n\n"
                    f"| Health Metric | Result |\n"
                    f"| :--- | :--- |\n"
                    f"| **Overall Health Score** | **{score}/100 (Grade {grade} — {status})** |\n"
                    f"| **Formula Failures** | `{m['formula_errors_count']}` |\n"
                    f"| **Duplicate Rows** | `{m['duplicate_rows_count']}` |\n"
                    f"| **Missing Data Cells** | `{m['missing_values_count']}` |\n"
                    f"| **Financial Anomalies** | `{m['negative_anomalies_count']}` |\n"
                    f"| **Statistical Outliers** | `{m['outliers_count']}` |\n\n"
                    f"#### 🔍 Detailed Findings:\n{issues_block}\n\n"
                    f"#### 💡 Actionable Remediation Plan:\n{recs_md}\n"
                )

        # --- CASE 3C: AUTONOMOUS DOCUMENT CREATOR & DOWNLOADER (WORD DOCX, PDF, XLSX, CSV) ---
        elif task_type == TaskType.FILE_GENERATION:
            console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Executing [bold cyan]Autonomous Document Creator[/bold cyan]...")
            is_docx_target = params.get("format") == "docx" or any(w in question.lower() for w in ["docx", "doc file", "word", "word doc", "word document", "doc bana", "doc format", "doc bhi"]) or ("doc" in question.lower() and "pdf" not in question.lower() and "excel" not in question.lower())
            is_pdf_target = params.get("format") == "pdf" or "pdf" in question.lower() or (not is_tabular and not is_docx_target)

            if is_docx_target:
                gen_res = docx_generator_engine.generate_docx(path, question, udm=udm)
                tools_used.append("docx_generator_engine")
            elif is_pdf_target:
                gen_res = pdf_generator_engine.generate_pdf(path, question, udm=udm)
                tools_used.append("pdf_generator_engine")
            else:
                gen_res = data_engine.generate_file(path, question)
                tools_used.append("data_engine_document_creator")

            if gen_res.get("success"):
                generated_file_data = gen_res
                dims_str = f"{gen_res.get('page_count', 1)} page(s)" if gen_res["file_type"] == "PDF" else (f"{gen_res.get('row_count', 0)} records" if gen_res["file_type"] == "DOCX" else f"{gen_res.get('row_count', 0)} rows × {gen_res.get('column_count', 0)} columns")
                evidence.append({
                    "source": f"Autonomous Document Creator on {udm.file.filename}",
                    "content_type": "generated_file",
                    "snippet": f"Created new {gen_res['file_type']} file '{gen_res['filename']}' ({gen_res['file_size_kb']} KB) with {dims_str}."
                })
                answer_text = (
                    f"### 📥 {gen_res['file_type']} Document Generated Successfully!\n\n"
                    f"**{gen_res['description']}**\n\n"
                    f"- **File Name:** `{gen_res['filename']}`\n"
                    f"- **Format:** {gen_res['file_type']}\n"
                    f"- **Size:** {gen_res['file_size_kb']} KB\n"
                    f"- **Details:** {dims_str}\n\n"
                    f"A direct download button has been prepared for you below."
                )
            else:
                answer_text = f"File Generation Error: {gen_res.get('error')}"

        # --- CASE 4: STANDARD GROUNDED LLM REASONING ---
        if not answer_text:
            doc_id = None
            with SyncSessionLocal() as db:
                doc_record = db.query(Document).filter(Document.file_hash == udm.file.file_hash).first()
                if doc_record:
                    doc_id = doc_record.id

            target_page = params.get("page_number")
            retrieved_chunks = []
            if doc_id:
                retrieved_chunks = retriever.retrieve(doc_id, question, target_page=target_page)

            context_blocks = []
            for c in retrieved_chunks:
                p_num = c.get("page_number")
                src_label = f"Page {p_num}" if p_num else "Document Section"
                evidence.append({
                    "source": src_label,
                    "page_number": p_num,
                    "content_type": c.get("content_type"),
                    "snippet": c.get("content", "")[:500]
                })
                context_blocks.append(f"[{src_label} - Type: {c.get('content_type')}]:\n{c.get('content')}")

            if not context_blocks:
                for pg in udm.pages[:3]:
                    src_label = f"Page {pg.page_number}"
                    evidence.append({
                        "source": src_label,
                        "page_number": pg.page_number,
                        "content_type": "text",
                        "snippet": pg.text[:500]
                    })
                    context_blocks.append(f"[{src_label}]:\n{pg.text}")

            context_str = "\n\n---\n\n".join(context_blocks)

            system_prompt = (
                "You are Z1 Alpha, an Autonomous File Intelligence Agent developed by the AxomAI AGI team.\n"
                "Your objective is to provide precise, authoritative, and helpful answers strictly based on the provided document context.\n\n"
                "CRITICAL GUIDELINES:\n"
                "1. Grounding: Answer ONLY based on the provided document context. If information is missing, state it clearly.\n"
                "2. Citations: Explicitly cite sources in your answer using badges like [Page X] or [Table Y].\n"
                "3. Language: Match the user's language (Hindi, Hinglish, or English).\n"
                "4. Structure: Use markdown formatting, bullet points, and bold text for clarity."
            )

            user_prompt = (
                f"File: {udm.file.filename} (Type: {udm.file.file_type}, Total Pages/Sheets: {udm.page_count})\n"
                f"Detected Task: {task_type}\n\n"
                f"DOCUMENT CONTEXT:\n{context_str}\n\n"
                f"USER QUESTION: {question}\n\n"
                f"Please provide your verified and grounded answer with citations:"
            )

            if llm_brain.is_available:
                console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Generating reasoning with [green]{llm_brain.model_name}[/green]...")
                answer_text = llm_brain.generate(system_prompt, user_prompt, temperature=0.2)
                tools_used.append(f"openai_{llm_brain.model_name}")
            else:
                answer_text = (
                    f"### Context Extracted from {udm.file.filename}:\n\n"
                    + "\n\n".join(context_blocks[:2])
                )

        # --- LOG INTERACTION IN POSTGRESQL ---
        with SyncSessionLocal() as db:
            session = db.query(AgentSession).filter(AgentSession.id == session_id).first()
            if not session:
                session = AgentSession(id=session_id, agent_name=self.name)
                db.add(session)
                db.flush()

            doc_record = db.query(Document).filter(Document.file_hash == udm.file.file_hash).first()
            task_log = AgentTaskLog(
                session_id=session.id,
                document_id=doc_record.id if doc_record else None,
                user_query=question,
                task_type=task_type,
                tools_used=tools_used,
                evidence=evidence,
                response=answer_text
            )
            db.add(task_log)
            db.commit()

        return {
            "agent": self.name,
            "file": udm.file.filename,
            "task_type": task_type,
            "tools_used": tools_used,
            "evidence": evidence,
            "answer": answer_text,
            "chart": chart_data,
            "generated_file": generated_file_data
        }

    def query_stream(
        self,
        question: str,
        file_path: str | Path,
        session_id: Optional[str] = None
    ):
        """
        Streamed execution of Z1 Alpha File Intelligence:
        Yields JSON event dictionaries:
        - {"type": "meta", "task_type": ..., "tools_used": ..., "evidence": ..., "chart": ..., "generated_file": ...}
        - {"type": "token", "content": ...}
        - {"type": "done", "answer": ...}
        """
        session_id = session_id or str(uuid.uuid4())[:8]
        path = Path(file_path)
        udm = self.process_file(path)

        task_type, params = self.router.detect_task(question)
        tools_used = [self.router.route_file(path).name]
        evidence: List[Dict[str, Any]] = []
        chart_data = None
        generated_file_data = None
        answer_text = ""

        is_image = udm.file.file_type == "IMAGE"
        is_tabular = udm.file.file_type in ["XLSX", "XLS", "CSV", "TSV"]
        is_pdf = udm.file.file_type == "PDF"

        # Case 1: Image
        if is_image:
            mode = "chart_analysis" if task_type == TaskType.CHART_ANALYSIS else ("ocr" if task_type == TaskType.OCR_TEXT else "comprehensive")
            vision_res = vision_engine.analyze(image_input=path, question=question, task_mode=mode)
            if vision_res.get("success"):
                tools_used.append(f"vision_engine ({vision_res.get('model_used')})")
                evidence.append({
                    "source": f"Visual Inspection of {udm.file.filename}",
                    "content_type": "image",
                    "snippet": f"Visual analysis on {udm.file.filename} using {vision_res.get('model_used')}."
                })
                answer_text = vision_res.get("analysis", "")
            else:
                answer_text = f"Vision Error: {vision_res.get('error')}"

        # Case 2: PDF with charts / OCR
        elif is_pdf and task_type in [TaskType.CHART_ANALYSIS, TaskType.OCR_TEXT]:
            target_page_num = params.get("page_number", 1)
            target_idx = max(0, min(target_page_num - 1, udm.page_count - 1))
            try:
                import fitz
                pdf_doc = fitz.open(path)
                page = pdf_doc[target_idx]
                pix = page.get_pixmap(dpi=150)
                img_bytes = pix.tobytes("png")
                pdf_doc.close()

                mode = "chart_analysis" if task_type == TaskType.CHART_ANALYSIS else "ocr"
                vision_res = vision_engine.analyze(
                    image_input=img_bytes, question=question, task_mode=mode, mime_type="image/png"
                )
                if vision_res.get("success"):
                    tools_used.extend(["pdf_renderer", f"vision_engine ({vision_res.get('model_used')})"])
                    evidence.append({
                        "source": f"Page {target_idx + 1} (High-Res Rendered Image)",
                        "page_number": target_idx + 1,
                        "mode": mode,
                        "content_type": "rendered_page",
                        "snippet": f"Page {target_idx + 1} of PDF rendered to high-res image and visually analyzed."
                    })
                    answer_text = (
                        f"### 👁️ Visual & Graphic Analysis (Page {target_idx + 1})\n\n"
                        f"{vision_res.get('analysis')}"
                    )
            except Exception as e:
                answer_text = f"PDF render error: {e}"

        # Case 3: Tabular Chart request or Pandas Analysis
        elif is_tabular and (task_type in [TaskType.CHART_ANALYSIS, TaskType.DATA_ANALYSIS] or any(w in question.lower() for w in ["chart", "graph", "plot", "bar", "pie", "visual", "trend"])):
            is_visual_request = any(w in question.lower() for w in ["chart", "graph", "plot", "bar", "pie", "visual", "trend"]) or task_type == TaskType.CHART_ANALYSIS
            if is_visual_request:
                chart_res = data_engine.generate_chart(path, question)
                if chart_res.get("success"):
                    tools_used.append("chart_visualizer")
                    chart_data = chart_res.get("chart")
                    evidence.append({
                        "source": f"Visual Chart Engine on {udm.file.filename}",
                        "content_type": "chart",
                        "snippet": f"Generated {chart_data.get('type', 'bar')} chart '{chart_data.get('title')}'."
                    })
                    answer_text = (
                        f"### 📊 Interactive Visual Chart: {chart_data.get('title', 'Data Visualization')}\n\n"
                        f"The interactive {chart_data.get('type', 'bar')} chart has been rendered below from **{udm.file.filename}**.\n"
                    )

            if not answer_text and task_type == TaskType.DATA_ANALYSIS:
                calc_res = data_engine.analyze(path, question)
                if calc_res.get("success"):
                    tools_used.append("pandas_code_interpreter")
                    evidence.append({
                        "source": f"Pandas Code Sandbox on {udm.file.filename}",
                        "content_type": "calculation",
                        "calculation": calc_res.get("calculation"),
                        "code": calc_res.get("code"),
                        "snippet": f"Executed Python Code:\n{calc_res.get('code')}\n\nOutput:\n{calc_res.get('calculation')}"
                    })
                    answer_text = (
                        f"### 📊 Data Analysis Result\n\n"
                        f"**Exact Calculated Result:**\n```\n{calc_res.get('calculation')}\n```\n\n"
                        f"**Python Pandas Code Executed:**\n```python\n{calc_res.get('code')}\n```\n"
                    )

        # --- CASE 3B: SMART SPREADSHEET AUDIT ---
        elif is_tabular and task_type == TaskType.AUDIT:
            console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Executing [bold magenta]Smart Spreadsheet Audit[/bold magenta]...")
            audit_res = data_engine.audit_spreadsheet(path)
            if audit_res.get("success"):
                tools_used.append("spreadsheet_auditor")
                m = audit_res["metrics"]
                score = audit_res["health_score"]
                status = audit_res["health_status"]
                grade = audit_res["health_grade"]

                evidence.append({
                    "source": f"Spreadsheet Auditor on {udm.file.filename}",
                    "content_type": "audit_report",
                    "snippet": f"Audit: Health Score {score}/100 ({status}), {m['formula_errors_count']} formula errors, {m['duplicate_rows_count']} duplicates, {m['missing_values_count']} missing cells."
                })

                issues_md = []
                if audit_res["formula_errors"]:
                    issues_md.append("\n**⚠️ Formula / Calculation Errors:**")
                    for err in audit_res["formula_errors"][:5]:
                        issues_md.append(f"- Row {err['row']}, Column `{err['column']}`: `{err['error_type']}`")

                if audit_res["duplicate_rows"]:
                    issues_md.append(f"\n**⚠️ Duplicate Rows:** {len(audit_res['duplicate_rows'])} identical row(s) found at rows: {audit_res['duplicate_rows']}")

                if audit_res["negative_anomalies"]:
                    issues_md.append("\n**⚠️ Financial Anomalies (Negative Values):**")
                    for neg in audit_res["negative_anomalies"][:5]:
                        issues_md.append(f"- Row {neg['row']}, Column `{neg['column']}`: Value `{neg['value']}`")

                if audit_res["missing_by_column"]:
                    issues_md.append("\n**⚠️ Missing / Blank Data:**")
                    for col, inf in audit_res["missing_by_column"].items():
                        issues_md.append(f"- Column `{col}`: {inf['count']} missing values ({inf['percentage']}%)")

                recs_md = "\n".join([f"1. {r}" for r in audit_res["recommendations"]])
                issues_block = "\n".join(issues_md) if issues_md else "✅ **Zero errors detected.** All cells and formulas are valid."

                answer_text = (
                    f"### 🛡️ Smart Spreadsheet Audit Report\n\n"
                    f"**File:** `{udm.file.filename}` | **Total Rows:** {audit_res['total_rows']} | **Total Columns:** {audit_res['total_columns']}\n\n"
                    f"| Health Metric | Result |\n"
                    f"| :--- | :--- |\n"
                    f"| **Overall Health Score** | **{score}/100 (Grade {grade} — {status})** |\n"
                    f"| **Formula Failures** | `{m['formula_errors_count']}` |\n"
                    f"| **Duplicate Rows** | `{m['duplicate_rows_count']}` |\n"
                    f"| **Missing Data Cells** | `{m['missing_values_count']}` |\n"
                    f"| **Financial Anomalies** | `{m['negative_anomalies_count']}` |\n"
                    f"| **Statistical Outliers** | `{m['outliers_count']}` |\n\n"
                    f"#### 🔍 Detailed Findings:\n{issues_block}\n\n"
                    f"#### 💡 Actionable Remediation Plan:\n{recs_md}\n"
                )

        # --- CASE 3C: AUTONOMOUS DOCUMENT CREATOR & DOWNLOADER (WORD DOCX, PDF, XLSX, CSV) ---
        elif task_type == TaskType.FILE_GENERATION:
            console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Executing [bold cyan]Autonomous Document Creator[/bold cyan]...")
            is_docx_target = params.get("format") == "docx" or any(w in question.lower() for w in ["docx", "doc file", "word", "word doc", "word document", "doc bana", "doc format", "doc bhi"]) or ("doc" in question.lower() and "pdf" not in question.lower() and "excel" not in question.lower())
            is_pdf_target = params.get("format") == "pdf" or "pdf" in question.lower() or (not is_tabular and not is_docx_target)

            if is_docx_target:
                gen_res = docx_generator_engine.generate_docx(path, question, udm=udm)
                tools_used.append("docx_generator_engine")
            elif is_pdf_target:
                gen_res = pdf_generator_engine.generate_pdf(path, question, udm=udm)
                tools_used.append("pdf_generator_engine")
            else:
                gen_res = data_engine.generate_file(path, question)
                tools_used.append("data_engine_document_creator")

            if gen_res.get("success"):
                generated_file_data = gen_res
                dims_str = f"{gen_res.get('page_count', 1)} page(s)" if gen_res["file_type"] == "PDF" else (f"{gen_res.get('row_count', 0)} records" if gen_res["file_type"] == "DOCX" else f"{gen_res.get('row_count', 0)} rows × {gen_res.get('column_count', 0)} columns")
                evidence.append({
                    "source": f"Autonomous Document Creator on {udm.file.filename}",
                    "content_type": "generated_file",
                    "snippet": f"Created new {gen_res['file_type']} file '{gen_res['filename']}' ({gen_res['file_size_kb']} KB) with {dims_str}."
                })
                answer_text = (
                    f"### 📥 {gen_res['file_type']} Document Generated Successfully!\n\n"
                    f"**{gen_res['description']}**\n\n"
                    f"- **File Name:** `{gen_res['filename']}`\n"
                    f"- **Format:** {gen_res['file_type']}\n"
                    f"- **Size:** {gen_res['file_size_kb']} KB\n"
                    f"- **Details:** {dims_str}\n\n"
                    f"A direct download button has been prepared for you below."
                )
            else:
                answer_text = f"File Generation Error: {gen_res.get('error')}"

        # If answer_text is already determined (from vision, pandas, or chart)
        if answer_text:
            yield {
                "type": "meta",
                "task_type": task_type,
                "tools_used": tools_used,
                "evidence": evidence,
                "chart": chart_data,
                "generated_file": generated_file_data
            }
            # Stream words with small chunks for live typewriter effect
            words = answer_text.split(" ")
            for i in range(0, len(words), 3):
                chunk = " ".join(words[i:i+3]) + (" " if i+3 < len(words) else "")
                yield {"type": "token", "content": chunk}
            yield {"type": "done", "answer": answer_text}
            return

        # Case 4: Standard Grounded LLM reasoning (GPT-4o streaming)
        doc_id = None
        with SyncSessionLocal() as db:
            doc_record = db.query(Document).filter(Document.file_hash == udm.file.file_hash).first()
            if doc_record:
                doc_id = doc_record.id

        target_page = params.get("page_number")
        retrieved_chunks = []
        if doc_id:
            retrieved_chunks = retriever.retrieve(doc_id, question, target_page=target_page)

        context_blocks = []
        for c in retrieved_chunks:
            p_num = c.get("page_number")
            src_label = f"Page {p_num}" if p_num else "Document Section"
            evidence.append({
                "source": src_label,
                "page_number": p_num,
                "content_type": c.get("content_type"),
                "snippet": c.get("content", "")[:500]
            })
            context_blocks.append(f"[{src_label} - Type: {c.get('content_type')}]:\n{c.get('content')}")

        if not context_blocks:
            for pg in udm.pages[:3]:
                src_label = f"Page {pg.page_number}"
                evidence.append({
                    "source": src_label,
                    "page_number": pg.page_number,
                    "content_type": "text",
                    "snippet": pg.text[:500]
                })
                context_blocks.append(f"[{src_label}]:\n{pg.text}")

        context_str = "\n\n---\n\n".join(context_blocks)

        system_prompt = (
            "You are Z1 Alpha, an Autonomous File Intelligence Agent developed by the AxomAI AGI team.\n"
            "Your objective is to provide precise, authoritative, and helpful answers strictly based on the provided document context.\n\n"
            "CRITICAL GUIDELINES:\n"
            "1. Grounding: Answer ONLY based on the provided document context. If information is missing, state it clearly.\n"
            "2. Citations: Explicitly cite sources in your answer using badges like [Page X] or [Table Y].\n"
            "3. Language: Match the user's language (Hindi, Hinglish, or English).\n"
            "4. Structure: Use markdown formatting, bullet points, and bold text for clarity."
        )

        user_prompt = (
            f"File: {udm.file.filename} (Type: {udm.file.file_type}, Total Pages/Sheets: {udm.page_count})\n"
            f"Detected Task: {task_type}\n\n"
            f"DOCUMENT CONTEXT:\n{context_str}\n\n"
            f"USER QUESTION: {question}\n\n"
            f"Please provide your verified and grounded answer with citations:"
        )

        tools_used.append(f"openai_{llm_brain.model_name}")

        # Yield metadata first (badges, evidence, etc.)
        yield {
            "type": "meta",
            "task_type": task_type,
            "tools_used": tools_used,
            "evidence": evidence,
            "chart": chart_data,
            "generated_file": generated_file_data
        }

        # Stream token by token from GPT-4o
        accumulated_tokens = []
        for token in llm_brain.stream_generate(system_prompt, user_prompt, temperature=0.2):
            accumulated_tokens.append(token)
            yield {"type": "token", "content": token}

        full_answer = "".join(accumulated_tokens)

        # Log to PostgreSQL
        try:
            with SyncSessionLocal() as db:
                session = db.query(AgentSession).filter(AgentSession.id == session_id).first()
                if not session:
                    session = AgentSession(id=session_id, agent_name=self.name)
                    db.add(session)
                    db.flush()

                doc_record = db.query(Document).filter(Document.file_hash == udm.file.file_hash).first()
                task_log = AgentTaskLog(
                    session_id=session.id,
                    document_id=doc_record.id if doc_record else None,
                    user_query=question,
                    task_type=task_type,
                    tools_used=tools_used,
                    evidence=evidence,
                    response=full_answer
                )
                db.add(task_log)
                db.commit()
        except Exception:
            pass

        yield {"type": "done", "answer": full_answer}

    def query_multi(
        self,
        question: str,
        file_paths: List[str | Path],
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes Multi-Document Comparison and Cross-Document Synthesis:
        1. Loads and normalizes each document UDM from PostgreSQL cache.
        2. Gathers contextual snippets, page text, and tables from all target files.
        3. Formulates a cross-document synthesis prompt with strict document-level citations.
        4. Generates comparative breakdown, differences, and matches.
        5. Logs multi-document session interaction into PostgreSQL.
        """
        session_id = session_id or str(uuid.uuid4())[:8]
        udms: List[UnifiedDocumentModel] = []
        tools_used = ["multi_doc_synthesizer"]
        evidence: List[Dict[str, Any]] = []

        for p in file_paths:
            path_obj = Path(p)
            if path_obj.exists():
                u = self.process_file(path_obj)
                udms.append(u)
                tool = self.router.route_file(path_obj)
                if tool.name not in tools_used:
                    tools_used.append(tool.name)

        if not udms:
            return {
                "agent": self.name,
                "task_type": "MULTI_DOC_SYNTHESIS",
                "tools_used": tools_used,
                "evidence": [],
                "answer": "Kripya valid documents select karein compare karne ke liye."
            }

        # Build context from each document
        multi_context_blocks = []
        for idx, u in enumerate(udms, start=1):
            doc_label = f"Doc {idx}: {u.file.filename} ({u.file.file_type})"
            
            # Fetch relevant text or first few pages/tables
            doc_text_parts = []
            if u.pages:
                for pg in u.pages[:3]:
                    pg_summary = f"[Page {pg.page_number}]: {pg.text[:600]}"
                    doc_text_parts.append(pg_summary)
            if u.tables:
                for tb in u.tables[:2]:
                    doc_text_parts.append(f"[Table: {tb.title or tb.table_id}]:\n{tb.to_markdown()[:600]}")

            combined_doc_text = "\n".join(doc_text_parts) if doc_text_parts else u.get_full_text(max_pages=2)
            multi_context_blocks.append(
                f"### ================================\n"
                f"### {doc_label}\n"
                f"### ================================\n"
                f"{combined_doc_text}"
            )
            evidence.append({
                "source": u.file.filename,
                "file_type": u.file.file_type,
                "page_count": u.page_count,
                "snippet": combined_doc_text[:600]
            })

        all_context = "\n\n".join(multi_context_blocks)

        system_prompt = (
            "You are Z1 Alpha, an Autonomous Multi-Document Intelligence Agent developed by AxomAI AGI.\n"
            "Your objective is to perform comprehensive cross-document analysis, side-by-side comparison, "
            "and factual synthesis across the provided documents.\n\n"
            "CRITICAL RULES:\n"
            "1. Side-by-Side Comparison: Clearly identify common themes, matching records, differences, or discrepancies.\n"
            "2. Grounded Citations: Always explicitly mention which document a fact comes from (e.g. `[Doc 1: filename.pdf]` or `[Doc 2: data.xlsx]`).\n"
            "3. Structured Presentation: Use markdown tables for comparisons wherever appropriate, followed by bullet points.\n"
            "4. Language: Answer in Hindi, Hinglish, or English to match the user's inquiry."
        )

        file_list_str = ", ".join([f"'{u.file.filename}'" for u in udms])
        user_prompt = (
            f"TARGET DOCUMENTS ({len(udms)} files): {file_list_str}\n\n"
            f"DOCUMENT CONTEXTS:\n{all_context}\n\n"
            f"USER COMPARISON / SYNTHESIS QUERY: {question}\n\n"
            f"Provide a structured, accurate comparison and synthesis with exact citations:"
        )

        console.print(f"[dim cyan][Z1 Alpha][/dim cyan] Performing Multi-Document Synthesis on {len(udms)} files...")
        if llm_brain.is_available:
            answer_text = llm_brain.generate(system_prompt, user_prompt, temperature=0.2, max_tokens=2500)
            tools_used.append(f"openai_{llm_brain.model_name}")
        else:
            answer_text = (
                f"### Multi-Document Overview for: {file_list_str}\n\n"
                + "\n\n".join(multi_context_blocks[:2])
            )

        # Log in PostgreSQL
        with SyncSessionLocal() as db:
            session = db.query(AgentSession).filter(AgentSession.id == session_id).first()
            if not session:
                session = AgentSession(id=session_id, agent_name=self.name)
                db.add(session)
                db.flush()

            task_log = AgentTaskLog(
                session_id=session.id,
                document_id=None,
                user_query=question,
                task_type="MULTI_DOC_SYNTHESIS",
                tools_used=tools_used,
                evidence=evidence,
                response=answer_text
            )
            db.add(task_log)
            db.commit()

        return {
            "agent": self.name,
            "files": [u.file.filename for u in udms],
            "task_type": "MULTI_DOC_SYNTHESIS",
            "tools_used": tools_used,
            "evidence": evidence,
            "answer": answer_text
        }

    def query_multi_stream(
        self,
        question: str,
        file_paths: List[str | Path],
        session_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Executes Multi-Document Comparison and Cross-Document Synthesis with real-time SSE token streaming.
        """
        session_id = session_id or str(uuid.uuid4())[:8]
        udms: List[UnifiedDocumentModel] = []
        tools_used = ["multi_doc_synthesizer"]
        evidence: List[Dict[str, Any]] = []

        yield {
            "type": "status",
            "stage": "parsing_files",
            "message": f"📊 Loading and cross-indexing {len(file_paths)} documents for comparative synthesis..."
        }

        for p in file_paths:
            path_obj = Path(p)
            if path_obj.exists():
                u = self.process_file(path_obj)
                udms.append(u)
                tool = self.router.route_file(path_obj)
                if tool.name not in tools_used:
                    tools_used.append(tool.name)

        if not udms:
            yield {
                "type": "meta",
                "task_type": "MULTI_DOC_SYNTHESIS",
                "tools_used": tools_used,
                "evidence": []
            }
            msg = "Kripya valid documents select karein compare karne ke liye."
            yield {"type": "token", "content": msg}
            yield {"type": "done", "answer": msg}
            return

        # Build context from each document
        multi_context_blocks = []
        for idx, u in enumerate(udms, start=1):
            doc_label = f"Doc {idx}: {u.file.filename} ({u.file.file_type})"
            doc_text_parts = []
            if u.pages:
                for pg in u.pages[:3]:
                    pg_summary = f"[Page {pg.page_number}]: {pg.text[:600]}"
                    doc_text_parts.append(pg_summary)
            if u.tables:
                for tb in u.tables[:2]:
                    doc_text_parts.append(f"[Table: {tb.title or tb.table_id}]:\n{tb.to_markdown()[:600]}")

            combined_doc_text = "\n".join(doc_text_parts) if doc_text_parts else u.get_full_text(max_pages=2)
            multi_context_blocks.append(
                f"### ================================\n"
                f"### {doc_label}\n"
                f"### ================================\n"
                f"{combined_doc_text}"
            )
            evidence.append({
                "source": u.file.filename,
                "file_type": u.file.file_type,
                "page_count": u.page_count,
                "snippet": combined_doc_text[:600]
            })

        all_context = "\n\n".join(multi_context_blocks)

        system_prompt = (
            "You are Z1 Alpha, an Autonomous Multi-Document Intelligence Agent developed by AxomAI AGI.\n"
            "Your objective is to perform comprehensive cross-document analysis, side-by-side comparison, "
            "and factual synthesis across the provided documents.\n\n"
            "CRITICAL RULES:\n"
            "1. Side-by-Side Comparison: Clearly identify common themes, matching records, differences, or discrepancies.\n"
            "2. Grounded Citations: Always explicitly mention which document a fact comes from (e.g. `[Doc 1: filename.pdf]` or `[Doc 2: data.xlsx]`).\n"
            "3. Structured Presentation: Use markdown tables for comparisons wherever appropriate, followed by bullet points.\n"
            "4. Language: Answer in Hindi, Hinglish, or English to match the user's inquiry."
        )

        file_list_str = ", ".join([f"'{u.file.filename}'" for u in udms])
        user_prompt = (
            f"TARGET DOCUMENTS ({len(udms)} files): {file_list_str}\n\n"
            f"DOCUMENT CONTEXTS:\n{all_context}\n\n"
            f"USER COMPARISON / SYNTHESIS QUERY: {question}\n\n"
            f"Provide a structured, accurate comparison and synthesis with exact citations:"
        )

        tools_used.append(f"openai_{llm_brain.model_name}")

        yield {
            "type": "meta",
            "task_type": "MULTI_DOC_SYNTHESIS",
            "tools_used": tools_used,
            "evidence": evidence,
            "compared_files": [u.file.filename for u in udms]
        }

        accumulated_tokens = []
        if llm_brain.is_available:
            for token in llm_brain.stream_generate(system_prompt, user_prompt, temperature=0.2):
                accumulated_tokens.append(token)
                yield {"type": "token", "content": token}
        else:
            fallback = f"### Multi-Document Overview for {file_list_str}\n\n" + "\n\n".join(multi_context_blocks[:2])
            for t in fallback.split(" "):
                accumulated_tokens.append(t + " ")
                yield {"type": "token", "content": t + " "}

        full_answer = "".join(accumulated_tokens)

        # Log in PostgreSQL
        try:
            with SyncSessionLocal() as db:
                session = db.query(AgentSession).filter(AgentSession.id == session_id).first()
                if not session:
                    session = AgentSession(id=session_id, agent_name=self.name)
                    db.add(session)
                    db.flush()

                task_log = AgentTaskLog(
                    session_id=session.id,
                    document_id=None,
                    user_query=question,
                    task_type="MULTI_DOC_SYNTHESIS",
                    tools_used=tools_used,
                    evidence=evidence,
                    response=full_answer
                )
                db.add(task_log)
                db.commit()
        except Exception:
            pass

        yield {"type": "done", "answer": full_answer}
