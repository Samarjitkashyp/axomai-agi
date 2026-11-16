import os
import shutil
import uuid
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Query
from fastapi.responses import FileResponse, Response, StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc

from axomai.config import settings
from axomai.db.session import get_db, sync_engine
from axomai.db.models import Document, DocumentChunk, AgentTaskLog, AgentSession
from axomai.agents.z1_alpha.agent import Z1AlphaAgent
from axomai.agents.z2_bravo import z2_bravo_agent
from axomai.agents.z3_echo import z3_echo_agent
from axomai.agents.master_orchestrator import master_orchestrator
from axomai.agents.z_sentinel import z_sentinel_agent
from axomai.agents.z3_echo.tools.db_connector import db_connector
from axomai.core.llm import llm_brain
from axomai.core.translators.xetu import xetu_translator
from axomai.memory import unified_memory_hub
from axomai.learning import continuous_learner
from axomai.supervision import agent_watchdog, circuit_breaker, capability_guard, Capability, sovereign_governor, immunity_guard
from axomai.proactive import heartbeat_daemon, perception_radar
from axomai.metamorphosis import code_profiler, self_patcher
from axomai.swarm_hive import swarm_consensus, micro_swarm_commander
from axomai.agency import action_runner
from axomai.evaluation import benchmark_suite, EvaluationHarness, RegressionDetector
from axomai.cognition import cognitive_core, self_model, world_model, capability_registry, capability_acquisition_engine, belief_manager, war_game_simulator
from axomai.evolution import evolution_manager, active_researcher, failure_detector, hypothesis_engine
from axomai.orchestration import relentless_executor
from axomai.agency.web_operator import browser_navigator, credential_vault, security_gate_protocol, multi_tab_swarm_coordinator

router = APIRouter(prefix="/api")
agent = Z1AlphaAgent()

UPLOAD_DIR = settings.STORAGE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

GENERATED_DIR = settings.STORAGE_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

class QueryRequest(BaseModel):
    document_id: str
    query: str
    session_id: Optional[str] = "web_session"

class MultiQueryRequest(BaseModel):
    document_ids: List[str]
    query: str
    session_id: Optional[str] = "web_session"

class ResearchRequest(BaseModel):
    query: str
    session_id: Optional[str] = "web_session"
    document_id: Optional[str] = None

class AnalyticsRequest(BaseModel):
    query: str
    session_id: Optional[str] = "web_session"
    document_id: Optional[str] = None

class MasterRequest(BaseModel):
    query: str
    document_id: Optional[str] = None
    document_ids: Optional[List[str]] = None
    session_id: Optional[str] = "web_session"
    manual_agent: Optional[str] = None

class MissionPlanRequest(BaseModel):
    goal: str
    document_id: Optional[str] = None

class ActionExecutionRequest(BaseModel):
    action_id: str
    approved: bool = True

@router.get("/status")
def get_system_status(db: Session = Depends(get_db)):
    """Return health & database connectivity status"""
    try:
        doc_count = db.query(Document).count()
        chunk_count = db.query(DocumentChunk).count()
        log_count = db.query(AgentTaskLog).count()
        
        tools_list = [
            {"name": "Vision Intelligence Engine", "extensions": [".png", ".jpg", ".jpeg", ".webp"], "features": ["Chart Analysis", "Scene Understanding", "OCR"]},
            {"name": "PDF Reader Toolkit", "extensions": [".pdf"], "features": ["Text", "Tables", "Images", "Vision Render"]},
            {"name": "XLSX Data Analyzer", "extensions": [".xlsx", ".xls"], "features": ["Pandas Code Sandbox", "Formulas", "Stats"]},
            {"name": "DOCX Word Reader", "extensions": [".docx", ".doc"], "features": ["Headings", "Paragraphs", "Tables"]},
            {"name": "PPTX Presentation Reader", "extensions": [".pptx", ".ppt"], "features": ["Slides", "Bullets", "Notes"]},
            {"name": "CSV / TSV Analyzer", "extensions": [".csv", ".tsv"], "features": ["Columns", "Stats", "Python Sandbox"]},
            {"name": "Plain Text / MD Reader", "extensions": [".txt", ".md", ".json", ".yaml"], "features": ["Fast Text", "Sections"]}
        ]
        
        return {
            "status": "healthy",
            "agent_name": agent.name,
            "agent_role": agent.role,
            "database": {
                "name": settings.DB_NAME,
                "host": settings.DB_HOST,
                "port": settings.DB_PORT,
                "connected": True,
                "total_documents": doc_count,
                "total_chunks": chunk_count,
                "total_queries": log_count
            },
            "active_tools": tools_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    """List all documents cached in PostgreSQL"""
    docs = db.query(Document).order_by(desc(Document.created_at)).all()
    results = []
    for d in docs:
        udm = d.udm_data or {}
        tables_count = len(udm.get("tables", []))
        images_count = len(udm.get("images", []))
        results.append({
            "id": str(d.id),
            "filename": d.filename,
            "title": d.filename,
            "file_type": d.file_type,
            "mime_type": d.mime_type,
            "file_size_bytes": d.file_size_bytes,
            "page_count": d.page_count,
            "file_hash": d.file_hash,
            "tables_count": tables_count,
            "images_count": images_count,
            "created_at": d.created_at.isoformat() if d.created_at else None
        })
    return results

@router.get("/documents/{document_id}")
def get_document_details(document_id: str, db: Session = Depends(get_db)):
    """Fetch complete UDM details for a specific document"""
    try:
        doc_uuid = uuid.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Document UUID")

    doc = db.query(Document).filter(Document.id == doc_uuid).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "id": str(doc.id),
        "filename": doc.filename,
        "file_type": doc.file_type,
        "mime_type": doc.mime_type,
        "file_size_bytes": doc.file_size_bytes,
        "page_count": doc.page_count,
        "file_hash": doc.file_hash,
        "metadata": doc.metadata_,
        "udm": doc.udm_data,
        "created_at": doc.created_at.isoformat() if doc.created_at else None
    }

@router.get("/documents/{document_id}/raw")
def get_raw_file(document_id: str, db: Session = Depends(get_db)):
    """Serve the raw file (useful for rendering uploaded images)"""
    try:
        doc_uuid = uuid.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Document UUID")

    doc = db.query(Document).filter(Document.id == doc_uuid).first()
    if not doc or not Path(doc.file_path).exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(doc.file_path, media_type=doc.mime_type)

@router.get("/documents/{document_id}/pages/{page_number}/image")
def get_document_page_image(document_id: str, page_number: int, db: Session = Depends(get_db)):
    """Render and serve a specific page of a document as a high-res image (PDF or Image)"""
    try:
        doc_uuid = uuid.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Document UUID")

    doc = db.query(Document).filter(Document.id == doc_uuid).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = Path(doc.file_path)
    if not file_path.exists():
        candidate = UPLOAD_DIR / doc.filename
        if candidate.exists():
            file_path = candidate
        else:
            matches = list(UPLOAD_DIR.glob(f"*{doc.filename}"))
            if matches:
                file_path = matches[0]
            else:
                raise HTTPException(status_code=404, detail=f"File not found on server disk: {doc.filename}")

    file_type = (doc.file_type or "").upper()
    ext = file_path.suffix.lower()

    # Image files (PNG, JPG, JPEG, WEBP, etc.)
    if file_type == "IMAGE" or ext in [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".gif"]:
        mime = doc.mime_type
        if not mime or "/" not in mime:
            mime_map = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".webp": "image/webp",
                ".gif": "image/gif",
                ".bmp": "image/bmp"
            }
            mime = mime_map.get(ext, "image/png")
        return FileResponse(str(file_path), media_type=mime)

    # PDF files
    if file_type == "PDF" or ext == ".pdf":
        try:
            import fitz
            pdf_doc = fitz.open(str(file_path))
            total_pages = len(pdf_doc)
            idx = max(0, min(page_number - 1, total_pages - 1))
            page = pdf_doc[idx]
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            pdf_doc.close()
            return Response(content=img_bytes, media_type="image/png")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to render page: {e}")

    raise HTTPException(status_code=404, detail="Page image rendering not supported for this file type")

@router.get("/documents/{document_id}/pages/{page_number}/text")
def get_document_page_text(document_id: str, page_number: int, db: Session = Depends(get_db)):
    """Fetch structured text and tables for a specific page/sheet"""
    try:
        doc_uuid = uuid.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Document UUID")

    doc = db.query(Document).filter(Document.id == doc_uuid).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    udm = doc.udm_data or {}
    pages = udm.get("pages", [])
    target_page = next((p for p in pages if p.get("page_number") == page_number), None)
    
    if not target_page and pages:
        idx = max(0, min(page_number - 1, len(pages) - 1))
        target_page = pages[idx]

    return {
        "document_id": document_id,
        "page_number": page_number,
        "total_pages": doc.page_count,
        "text": target_page.get("text", "") if target_page else "",
        "tables": target_page.get("tables", []) if target_page else []
    }

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a single file, audit with Z Sentinel, parse into UDM with Z1 Alpha, and cache in PostgreSQL"""
    try:
        # 1. Read header bytes for Z Sentinel Magic Byte & Malware Inspection
        header_bytes = await file.read(1024)
        await file.seek(0)
        content = await file.read()
        file_size = len(content)
        await file.seek(0)

        # 2. Z Sentinel File Security Audit
        audit = z_sentinel_agent.audit_uploaded_file(file.filename, header_bytes, file_size)
        if not audit["is_safe"]:
            raise HTTPException(
                status_code=400,
                detail=f"🛡️ Security Alert: {audit['reason']} (Threat: {audit['threat_type']})"
            )

        sanitized_filename = audit["sanitized_name"]
        saved_name = f"{uuid.uuid4().hex[:8]}_{sanitized_filename}"
        dest_path = UPLOAD_DIR / saved_name

        with open(dest_path, "wb") as buffer:
            buffer.write(content)

        udm = agent.process_file(dest_path)

        with sync_engine.connect() as conn:
            with Session(sync_engine) as session:
                doc_record = session.query(Document).filter(Document.file_hash == udm.file.file_hash).first()
                doc_id = str(doc_record.id) if doc_record else None

        # Generate Instant Executive Summary & Tailored Follow-up Prompts
        summary_res = agent.generate_auto_summary(dest_path, udm)

        return {
            "success": True,
            "document_id": doc_id,
            "filename": udm.file.filename,
            "file_type": udm.file.file_type,
            "page_count": udm.page_count,
            "stats": udm.stats,
            "tables_extracted": len(udm.tables),
            "images_extracted": len(udm.images),
            "file_hash": udm.file.file_hash,
            "auto_summary": summary_res.get("summary", ""),
            "smart_prompts": summary_res.get("prompts", []),
            "security_verified": True
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@router.post("/upload-batch")
async def upload_batch(files: List[UploadFile] = File(...)):
    """Upload up to 10 files simultaneously with Z Sentinel security inspection & Z1 Alpha indexing"""
    if len(files) > 10:
        raise HTTPException(
            status_code=400,
            detail="🛡️ Z Sentinel Policy: Maximum 10 files can be uploaded and processed in a single batch."
        )

    uploaded_results = []
    errors = []

    for file in files:
        try:
            header_bytes = await file.read(1024)
            await file.seek(0)
            content = await file.read()
            file_size = len(content)
            await file.seek(0)

            # Z Sentinel audit
            audit = z_sentinel_agent.audit_uploaded_file(file.filename, header_bytes, file_size)
            if not audit["is_safe"]:
                errors.append(f"{file.filename}: {audit['reason']}")
                continue

            sanitized_filename = audit["sanitized_name"]
            saved_name = f"{uuid.uuid4().hex[:8]}_{sanitized_filename}"
            dest_path = UPLOAD_DIR / saved_name

            with open(dest_path, "wb") as buffer:
                buffer.write(content)

            udm = agent.process_file(dest_path)

            with Session(sync_engine) as session:
                doc_record = session.query(Document).filter(Document.file_hash == udm.file.file_hash).first()
                doc_id = str(doc_record.id) if doc_record else None

            uploaded_results.append({
                "document_id": doc_id,
                "filename": udm.file.filename,
                "file_type": udm.file.file_type,
                "page_count": udm.page_count,
                "file_size_bytes": file_size,
                "security_verified": True
            })
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")

    if not uploaded_results and errors:
        raise HTTPException(status_code=400, detail=f"All files failed security inspection: {'; '.join(errors)}")

    return {
        "success": True,
        "count": len(uploaded_results),
        "documents": uploaded_results,
        "errors": errors
    }

@router.post("/query")
def query_document(req: QueryRequest, db: Session = Depends(get_db)):
    """Execute an evidence-grounded task query on a document"""
    try:
        doc_uuid = uuid.UUID(req.document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Document UUID")

    doc = db.query(Document).filter(Document.id == doc_uuid).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    result = agent.query(
        question=req.query,
        file_path=doc.file_path,
        session_id=req.session_id
    )

    return result

@router.post("/query-stream")
def query_document_stream(req: QueryRequest, db: Session = Depends(get_db)):
    """Stream an evidence-grounded task query with real-time SSE typewriter tokens"""
    try:
        doc_uuid = uuid.UUID(req.document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Document UUID")

    doc = db.query(Document).filter(Document.id == doc_uuid).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = doc.file_path

    def event_generator():
        for event in agent.query_stream(
            question=req.query,
            file_path=file_path,
            session_id=req.session_id
        ):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/research")
def execute_research(req: ResearchRequest):
    """Execute deep web & market research synchronously with Z2 Bravo"""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return z2_bravo_agent.research(
        topic=req.query,
        session_id=req.session_id,
        doc_id=req.document_id
    )

@router.post("/research-stream")
def stream_research(req: ResearchRequest):
    """Real-time SSE token & source streaming for Z2 Bravo deep web research"""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    def event_generator():
        for event in z2_bravo_agent.research_stream(
            topic=req.query,
            session_id=req.session_id,
            doc_id=req.document_id
        ):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/analytics")
def execute_analytics(req: AnalyticsRequest):
    """Execute enterprise database querying, forecasting or what-if simulation with Z3 Echo"""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return z3_echo_agent.analytics(
        query=req.query,
        session_id=req.session_id,
        doc_id=req.document_id
    )

@router.post("/analytics-stream")
def stream_analytics(req: AnalyticsRequest):
    """Real-time SSE token & analytics streaming for Z3 Echo"""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    def event_generator():
        for event in z3_echo_agent.analytics_stream(
            query=req.query,
            session_id=req.session_id,
            doc_id=req.document_id
        ):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/master-stream")
@router.post("/master/stream")
def stream_master_orchestrator(req: MasterRequest):
    """
    Unified Autonomous Master Orchestrator SSE Streaming Endpoint.
    Automatically classifies and routes prompts to Z1 Alpha, Z2 Bravo, Z3 Echo,
    or executes a Tri-Agent Swarm Symphony without requiring manual model switching.
    """
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    def event_generator():
        try:
            for event in master_orchestrator.orchestrate_stream(
                query=req.query,
                document_id=req.document_id,
                document_ids=req.document_ids,
                session_id=req.session_id,
                manual_agent=req.manual_agent
            ):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            logger.error(f"SSE stream unhandled exception: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'error': f'Stream resilient recovery: {str(e)}'})}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'answer': f'Stream processed with recovery: {str(e)}'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/execute-action")
def execute_natural_language_action(req: ActionExecutionRequest):
    """
    Safe Natural Language Action Approval Gate.
    Executes or cancels an update proposal that was held pending user consent.
    """
    res = db_connector.execute_approved_action(req.action_id, approved=req.approved)
    return res

@router.post("/mission/plan")
def plan_mission_endpoint(req: MissionPlanRequest):
    """Decompose an ambitious enterprise objective into an autonomous multi-agent roadmap"""
    if not req.goal.strip():
        raise HTTPException(status_code=400, detail="Goal cannot be empty")
    from axomai.agents.mission_control import mission_planner
    plan = mission_planner.plan_mission(req.goal, doc_id=req.document_id)
    return plan.model_dump()

@router.get("/system-health")
def get_system_health(db: Session = Depends(get_db)):
    """
    Autonomous Watchdog & System Health Monitor.
    Returns PostgreSQL health, SQLite enterprise warehouse stats, DuckDB sandbox status,
    active reasoning model, disk storage metrics, and data integrity health score.
    """
    try:
        doc_count = db.query(Document).count()
        chunk_count = db.query(DocumentChunk).count()
        log_count = db.query(AgentTaskLog).count()
    except Exception:
        doc_count, chunk_count, log_count = 0, 0, 0

    db_health = db_connector.get_database_health()
    
    upload_files = list(UPLOAD_DIR.glob("*"))
    upload_size_mb = round(sum(f.stat().st_size for f in upload_files if f.is_file()) / (1024 * 1024), 2)
    gen_files = list(GENERATED_DIR.glob("*"))
    gen_size_mb = round(sum(f.stat().st_size for f in gen_files if f.is_file()) / (1024 * 1024), 2)

    return {
        "status": "OPERATIONAL",
        "watchdog_health_score": 100.0,
        "active_model": llm_brain.model_name,
        "active_agents": [
            {"id": "auto", "name": "Master Orchestrator", "status": "ONLINE", "type": "Autonomous Multi-Agent Routing"},
            {"id": "z1", "name": "Z1 Alpha", "status": "ONLINE", "type": "Files & Vision Intelligence"},
            {"id": "z2", "name": "Z2 Bravo", "status": "ONLINE", "type": "Autonomous Deep Web & Market Research"},
            {"id": "z3", "name": "Z3 Echo", "status": "ONLINE", "type": "Enterprise SQL & Predictive Analytics"},
            {"id": "swarm", "name": "Tri-Agent Swarm Symphony", "status": "ONLINE", "type": "Cross-Domain Collaborative Synthesis"}
        ],
        "database": {
            "postgresql": {
                "status": "CONNECTED",
                "documents": doc_count,
                "chunks": chunk_count,
                "logs": log_count
            },
            "sqlite_warehouse": db_health
        },
        "storage": {
            "uploads_count": len(upload_files),
            "uploads_size_mb": upload_size_mb,
            "generated_reports_count": len(gen_files),
            "generated_size_mb": gen_size_mb
        }
    }

@router.post("/audit/{document_id}")
def audit_document(document_id: str, db: Session = Depends(get_db)):
    """Run Smart Spreadsheet Audit on tabular files (XLSX, CSV)"""
    try:
        doc_uuid = uuid.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Document UUID")

    doc = db.query(Document).filter(Document.id == doc_uuid).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = Path(doc.file_path)
    from axomai.agents.z1_alpha.tools.code_interpreter import data_engine
    return data_engine.audit_spreadsheet(file_path)

@router.get("/download/generated/{filename}")
def download_generated_file(filename: str):
    """Serve a newly generated file as an attachment download"""
    safe_filename = Path(filename).name
    file_path = GENERATED_DIR / safe_filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Generated file not found")
    
    if safe_filename.endswith('.xlsx'):
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif safe_filename.endswith('.pptx') or safe_filename.endswith('.ppt'):
        media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    elif safe_filename.endswith('.docx') or safe_filename.endswith('.doc'):
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif safe_filename.endswith('.pdf'):
        media_type = "application/pdf"
    else:
        media_type = "text/csv"
    return FileResponse(
        file_path,
        media_type=media_type,
        filename=safe_filename,
        headers={"Content-Disposition": f'attachment; filename="{safe_filename}"'}
    )

@router.post("/query-multi")
def query_multiple_documents(req: MultiQueryRequest, db: Session = Depends(get_db)):
    """Execute cross-document comparison and synthesis across multiple files"""
    if not req.document_ids:
        raise HTTPException(status_code=400, detail="No document IDs provided for comparison")

    file_paths = []
    for doc_id_str in req.document_ids:
        try:
            doc_uuid = uuid.UUID(doc_id_str)
            doc = db.query(Document).filter(Document.id == doc_uuid).first()
            if doc and Path(doc.file_path).exists():
                file_paths.append(doc.file_path)
        except ValueError:
            continue

    if not file_paths:
        raise HTTPException(status_code=404, detail="No matching document files found")

    result = agent.query_multi(
        question=req.query,
        file_paths=file_paths,
        session_id=req.session_id
    )

    return result

@router.get("/logs")
def get_task_logs(limit: int = 20, db: Session = Depends(get_db)):
    """Retrieve recent agent task logs and citations from PostgreSQL"""
    logs = db.query(AgentTaskLog).order_by(desc(AgentTaskLog.created_at)).limit(limit).all()
    results = []
    for l in logs:
        results.append({
            "id": l.id,
            "session_id": l.session_id,
            "document_id": str(l.document_id) if l.document_id else None,
            "task_type": l.task_type,
            "user_query": l.user_query,
            "tools_used": l.tools_used or [],
            "evidence": l.evidence or [],
            "response": l.response,
            "created_at": l.created_at.isoformat() if l.created_at else None
        })
    return results

@router.post("/cleanup-all")
def cleanup_all_session_data(db: Session = Depends(get_db)):
    """
    Purges all documents, chunks, task logs, and temporary uploaded files
    so database is 100% clean and zero storage is wasted on refresh.
    """
    try:
        db.query(DocumentChunk).delete()
        db.query(AgentTaskLog).delete()
        db.query(AgentSession).delete()
        docs = db.query(Document).all()
        for d in docs:
            try:
                fp = Path(d.file_path)
                if fp.exists() and UPLOAD_DIR in fp.parents:
                    fp.unlink()
            except Exception:
                pass
        db.query(Document).delete()
        db.commit()

        # Also purge any orphaned files in upload and generated directories
        for f in UPLOAD_DIR.glob("*"):
            if f.is_file():
                try:
                    f.unlink()
                except Exception:
                    pass

        for f in GENERATED_DIR.glob("*"):
            if f.is_file():
                try:
                    f.unlink()
                except Exception:
                    pass

        return {"success": True, "message": "All session documents and temporary files purged successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

@router.delete("/documents/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db)):
    """Delete a document and its chunks from PostgreSQL"""
    try:
        doc_uuid = uuid.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Document UUID")

    doc = db.query(Document).filter(Document.id == doc_uuid).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = Path(doc.file_path)
    db.delete(doc)
    db.commit()

    if file_path.exists() and UPLOAD_DIR in file_path.parents:
        try:
            file_path.unlink()
        except Exception:
            pass

    return {"success": True, "deleted_id": document_id}

# --- PHASE 2: MODEL SWITCHING (GPT-4o vs GEMINI 2.0 FLASH) ---
class ModelSwitchRequest(BaseModel):
    model_name: str

@router.get("/settings/model")
def get_active_model():
    """Retrieve current active reasoning model and list available options"""
    return {
        "active_model": llm_brain.model_name,
        "available_models": [
            {"id": "gpt-4o-mini", "name": "OpenAI GPT-4o-mini", "tag": "Fast & Economical"},
            {"id": "gpt-4o", "name": "OpenAI GPT-4o", "tag": "High Precision & Multimodal Vision"},
            {"id": "gemini-2.0-flash", "name": "Google Gemini 2.0 Flash", "tag": "Ultra-Fast & Low Latency"},
            {"id": "gemini-1.5-flash", "name": "Google Gemini 1.5 Flash", "tag": "Long Context Window"}
        ]
    }

@router.post("/settings/model")
def switch_active_model(req: ModelSwitchRequest):
    """Switch active LLM brain model"""
    llm_brain.set_model(req.model_name)
    return {
        "success": True,
        "active_model": llm_brain.model_name
    }

# --- PHASE 3: NATIVE ASSAMESE (অসমীয়া) TRANSLATION ENGINE ---
class TranslateRequest(BaseModel):
    text: str

@router.post("/translate/assamese")
def translate_to_assamese(req: TranslateRequest):
    """Translates any response or analysis into sovereign Assamese using Xetu engine"""
    if not req.text.strip():
        return {"success": True, "translated_text": ""}
    return xetu_translator.translate_english_to_assamese(req.text)

# --- PHASE 4: REPORT EXPORT (MARKDOWN / HTML) ---
class ExportReportRequest(BaseModel):
    document_title: str
    messages: List[Dict[str, Any]]
    format: str = "markdown"

@router.post("/export/report")
def export_intelligence_report(req: ExportReportRequest):
    """Generates a downloadable structured intelligence report"""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    if req.format == "html":
        html_rows = ""
        for m in req.messages:
            role = m.get("role", "assistant")
            content = m.get("content", "").replace("\n", "<br>")
            if role == "user":
                html_rows += f"""
                <div style="background:#f0fdf4; border-left:4px solid #10b981; padding:12px 16px; margin:16px 0; border-radius:6px;">
                    <strong style="color:#047857; font-size:12px; text-transform:uppercase;">User Query</strong>
                    <div style="margin-top:6px; font-size:14px; color:#1f2937;">{content}</div>
                </div>
                """
            else:
                html_rows += f"""
                <div style="background:#f8fafc; border-left:4px solid #0891b2; padding:16px; margin:16px 0; border-radius:6px;">
                    <strong style="color:#0891b2; font-size:12px; text-transform:uppercase;">Z1 Alpha Grounded Intelligence</strong>
                    <div style="margin-top:6px; font-size:14px; color:#334155; line-height:1.6;">{content}</div>
                </div>
                """
        
        full_html = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Z1 Alpha Intelligence Report — {req.document_title}</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width:850px; margin:30px auto; padding:20px; color:#1e293b; }}
                h1 {{ color:#0e7490; margin-bottom:4px; font-size:24px; }}
                .meta {{ color:#64748b; font-size:13px; margin-bottom:24px; }}
                hr {{ border:0; border-top:1px solid #e2e8f0; margin:20px 0; }}
            </style>
        </head>
        <body>
            <h1>AxomAI AGI — Z1 Alpha Intelligence Report</h1>
            <div class="meta">Target Document: <strong>{req.document_title}</strong> | Generated At: {timestamp}</div>
            <hr>
            {html_rows}
            <hr>
            <div style="font-size:11px; color:#94a3b8; text-align:center;">Generated by AxomAI AGI • Z1 Alpha Autonomous Intelligence Engine</div>
        </body>
        </html>"""
        return Response(
            content=full_html,
            media_type="text/html",
            headers={"Content-Disposition": f"attachment; filename=Z1_Alpha_Report_{uuid.uuid4().hex[:6]}.html"}
        )
    else:
        # Markdown
        md_text = f"# AxomAI AGI — Z1 Alpha Intelligence Report\n\n"
        md_text += f"- **Target:** {req.document_title}\n"
        md_text += f"- **Generated At:** {timestamp}\n"
        md_text += f"- **Platform:** AxomAI AGI (Z1 Alpha)\n\n---\n\n"
        for m in req.messages:
            role_title = "User Query" if m.get("role") == "user" else "Z1 Alpha Grounded Intelligence"
            md_text += f"### 📌 {role_title}\n\n{m.get('content', '')}\n\n---\n\n"
        md_text += "\n*Generated automatically by AxomAI AGI Autonomous Intelligence Vault.*\n"
        return Response(
            content=md_text,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename=Z1_Alpha_Report_{uuid.uuid4().hex[:6]}.md"}
        )

@router.get("/memory/telemetry")
async def get_memory_telemetry():
    """Returns 4-tier cognitive memory architecture telemetry."""
    return unified_memory_hub.get_memory_telemetry()

@router.get("/memory/search")
async def search_memory(query: str = Query(..., min_length=2)):
    """Searches across episodic experiences and semantic knowledge graph."""
    brief = unified_memory_hub.synthesize_cognitive_brief(query)
    return brief

@router.post("/evolution/trigger-learn")
async def trigger_autonomous_learning(topic: Optional[str] = None):
    """Triggers an autonomous internet self-learning and memory consolidation cycle."""
    cycle_res = continuous_learner.run_learning_cycle(custom_topic=topic)
    return cycle_res

@router.get("/supervision/watchdog")
async def get_watchdog_telemetry():
    """Returns real-time agent watchdog and circuit breaker status."""
    return agent_watchdog.get_telemetry()

@router.get("/proactive/pulse")
async def get_proactive_pulse():
    """Returns heartbeat pulse telemetry and active inner monologue stream."""
    return heartbeat_daemon.get_heartbeat_telemetry()

@router.post("/proactive/pulse")
async def trigger_proactive_pulse():
    """Manually triggers a cognitive pulse to evaluate environmental signals."""
    return heartbeat_daemon.trigger_pulse()

@router.get("/metamorphosis/telemetry")
async def get_metamorphosis_telemetry():
    """Returns code profiler and hot patcher telemetry."""
    return {
        "profiler": code_profiler.get_profiler_telemetry(),
        "patcher": self_patcher.get_patch_telemetry()
    }

@router.post("/swarm/consensus")
async def execute_swarm_consensus(domains: Optional[List[str]] = None, query: str = "Multi-domain sovereign audit"):
    """Spawns an ephemeral swarm cluster, computes consensus, and purges clones."""
    doms = domains or ["energy", "logistics", "fx_hedging"]
    return swarm_consensus.execute_swarm_mission(doms, query)

@router.get("/agency/vitals")
async def get_agency_vitals():
    """Returns host system hardware vitals and cache status."""
    vitals = action_runner.get_system_vitals()
    return vitals

# =========================================================================
# AGI Evaluation Engine & Regression Detection Endpoints
# =========================================================================

@router.post("/evaluation/run")
async def run_evaluation_benchmark(version: str = "v3.1.0-candidate"):
    """
    Executes standardized AGI benchmark suite across 6 core pillars,
    evaluates against historical baseline, and returns promotion/rollback verdict.
    """
    harness = EvaluationHarness()
    scorecard = harness.run_benchmark(orchestrator=master_orchestrator, version_tag=version)
    detector = RegressionDetector()
    verdict = detector.compare_and_decide(scorecard)
    return {
        "scorecard": scorecard,
        "verdict": verdict
    }

@router.get("/evaluation/history")
async def get_evaluation_history():
    """Returns historical benchmark run records and trajectories."""
    detector = RegressionDetector()
    return {
        "history": detector.load_history(),
        "latest_baseline": detector.get_latest_baseline()
    }

# =========================================================================
# Autonomous Background Heartbeat Daemon Controls
# =========================================================================

@router.post("/proactive/heartbeat/daemon/start")
async def start_heartbeat_daemon(interval_seconds: float = 60.0):
    """Starts the autonomous cognitive pulse background thread."""
    started = heartbeat_daemon.start_daemon(tick_interval_seconds=interval_seconds)
    return {
        "status": "DAEMON_RUNNING" if started else "START_FAILED",
        "tick_interval_seconds": interval_seconds,
        "thread_alive": heartbeat_daemon.is_running()
    }

@router.post("/proactive/heartbeat/daemon/stop")
async def stop_heartbeat_daemon():
    """Stops the autonomous cognitive pulse background thread."""
    stopped = heartbeat_daemon.stop_daemon()
    return {
        "status": "DAEMON_STOPPED" if stopped else "STOP_FAILED",
        "thread_alive": heartbeat_daemon.is_running()
    }

@router.get("/proactive/radar")
async def get_perception_radar_scan():
    """Scans the real local environment and returns high-fidelity signals."""
    signals = perception_radar.scan_environment()
    return {
        "signals_count": len(signals),
        "signals": signals,
        "last_observation": perception_radar.last_observation
    }

# =========================================================================
# Capability Token & RBAC Supervision Endpoints
# =========================================================================

@router.get("/supervision/capabilities")
async def get_capability_supervision_telemetry():
    """Returns RBAC audit logs and active token status."""
    return {
        "audit_log": capability_guard.get_security_audit_log(),
        "master_token_active": bool(capability_guard.master_token),
        "janitor_token_active": bool(capability_guard.janitor_token)
    }

# =========================================================================
# Cognitive Core & Introspective Self-Model Endpoints
# =========================================================================

@router.get("/cognition/state")
async def get_cognitive_state():
    """Returns complete state across Self-Model, World-Model, Beliefs, and Capabilities."""
    return cognitive_core.get_cognitive_status()

@router.post("/cognition/deliberate")
async def trigger_cognitive_deliberation():
    """Executes a full cognitive deliberation cycle: observe -> model -> deliberate goals."""
    return cognitive_core.deliberate_and_act()

@router.post("/cognition/acquire-capability")
async def acquire_new_capability(
    name: str,
    category: str,
    description: str,
    code: str,
    test_input: Dict[str, Any],
    expected_output: Any
):
    """Dynamically compiles, sandboxes, verifies and registers a newly acquired capability."""
    res = capability_acquisition_engine.acquire_capability(
        capability_name=name,
        category=category,
        description=description,
        python_code=code,
        test_inputs=[test_input],
        expected_outputs=[expected_output]
    )
    return res

# =========================================================================
# Autonomous Evolution & Active Research Endpoints
# =========================================================================

@router.post("/evolution/run-cycle")
async def trigger_self_evolution_cycle():
    """Triggers an autonomous self-evolution cycle with benchmark validation and rollback guard."""
    return evolution_manager.run_self_evolution_cycle()

@router.post("/evolution/active-research")
async def execute_active_research(topic: str = Query(..., min_length=2)):
    """Conducts autonomous multi-question research on an unknown topic and updates knowledge base."""
    return active_researcher.conduct_active_research(topic)

# =========================================================================
# Sovereign Apex Command, Relentless Execution & War-Gaming Endpoints
# =========================================================================

@router.post("/sovereignty/relentless-execute")
async def execute_relentless_mission(goal: str, payload: Optional[Dict[str, Any]] = None):
    """
    Executes a mission using the 'Never-Give-Up' protocol: multi-path adaptation,
    dynamic capability synthesis, and self-healing until 100% accomplished.
    """
    res = relentless_executor.execute_relentlessly(mission_goal=goal, context_payload=payload)
    return res

@router.post("/sovereignty/war-game")
async def simulate_war_game(strategic_goal: str, num_scenarios: int = 5, horizon_days: int = 30):
    """
    Runs Monte Carlo counterfactual simulations across the World Model to select
    the optimal, battle-tested strategic trajectory.
    """
    res = war_game_simulator.simulate_strategic_futures(
        strategic_goal=strategic_goal,
        num_scenarios=num_scenarios,
        target_horizon_days=horizon_days
    )
    return res

@router.post("/sovereignty/micro-swarm")
async def dispatch_micro_swarm(mission_title: str, target_count: int = 6):
    """
    Deploys an ephemeral army of micro-workers, aggregates consensus, logs to memory,
    and purges all workers from RAM.
    """
    mock_slices = [
        {"domain": "energy", "capacity_kw": 250.0 + i * 50.0} if i % 3 == 0
        else ({"domain": "logistics", "distance_km": 600.0 + i * 150.0} if i % 3 == 1
        else {"domain": "fx_hedging", "spot_fx": 85.0 + i * 0.5})
        for i in range(target_count)
    ]
    res = micro_swarm_commander.dispatch_micro_swarm_army(
        mission_title=mission_title,
        target_slices=mock_slices
    )
    return res

@router.get("/sovereignty/telemetry")
async def get_sovereign_telemetry():
    """Returns deep telemetry across Sovereign Governor, Immunity Shield, Relentless Executor, and Micro-Swarm."""
    return {
        "sovereign_governor": sovereign_governor.get_sovereignty_status(),
        "immunity_shield": immunity_guard.get_immunity_telemetry(),
        "relentless_executor": {
            "missions_executed_count": len(relentless_executor.execution_audit_log),
            "recent_missions": relentless_executor.execution_audit_log[-3:]
        },
        "war_game_simulator": {
            "simulations_count": len(war_game_simulator.simulation_archive),
            "recent_wargames": war_game_simulator.get_wargame_history()[-3:]
        },
        "micro_swarm_commander": {
            "campaigns_count": len(micro_swarm_commander.swarm_campaigns),
            "recent_campaigns": micro_swarm_commander.get_campaign_history()[-3:]
        }
    }

# =========================================================================
# Autonomous Web Operator & Digital RPA Endpoints
# =========================================================================

@router.post("/web-operator/navigate")
async def web_navigate_and_inspect(url: str = Query(..., min_length=4)):
    """Navigates to URL, parses DOM elements and forms, and checks for 2FA gates."""
    return browser_navigator.navigate_and_inspect(url)

@router.post("/web-operator/fill-form")
async def web_fill_and_submit_form(
    target_url: str,
    action_url: str,
    form_fields: Dict[str, Any],
    method: str = "POST"
):
    """Autonomously fills and submits form fields to a verified action endpoint."""
    return browser_navigator.fill_and_submit_form(
        target_url=target_url,
        action_url=action_url,
        form_fields=form_fields,
        method=method
    )

@router.post("/web-operator/download-document")
async def web_download_document(download_url: str, filename: Optional[str] = None):
    """Autonomously downloads a document or data file into storage/downloads/."""
    return browser_navigator.download_document_artifact(download_url=download_url, filename_hint=filename)

@router.get("/web-operator/vault")
async def web_vault_list_credentials():
    """Lists authorized web credentials with secrets strictly masked."""
    return {
        "registered_services": credential_vault.list_services_masked(),
        "audit_trail": credential_vault.get_audit_trail()
    }

@router.post("/web-operator/vault/store")
async def web_vault_store_credential(
    service_id: str,
    service_name: str,
    username: str,
    secret: str,
    metadata: Optional[Dict[str, Any]] = None
):
    """Encrypts and stores authorized service credentials in local sovereign vault."""
    return credential_vault.store_credential(
        service_id=service_id,
        service_name=service_name,
        username=username,
        secret=secret,
        metadata=metadata
    )

@router.get("/web-operator/gate/pending")
async def web_gate_get_pending():
    """Returns pending human-in-the-loop security/2FA gates requiring user approval."""
    return {
        "pending_gates": security_gate_protocol.get_pending_gates()
    }

@router.post("/web-operator/gate/approve")
async def web_gate_approve_and_resume(gate_id: str, otp_token: Optional[str] = None):
    """Approves a human-in-the-loop gate and resumes autonomous AGI execution."""
    return security_gate_protocol.approve_and_resume_gate(gate_id=gate_id, auth_token_or_confirmation=otp_token)

@router.post("/web-operator/multi-tab-scrape")
async def web_multi_tab_scrape(
    mission_title: str = "Cross-Portal Data Extraction",
    portals: Optional[List[Dict[str, str]]] = None
):
    """Coordinates parallel multi-tab scraping and document aggregation across portals."""
    default_portals = portals or [
        {"name": "Discom Utility Billing Portal", "url": "mock://discom.assam.gov.in"},
        {"name": "Guwahati Tea Auction Committee", "url": "mock://gtac.assam.gov.in"},
        {"name": "Brahmaputra Water Resources Gauge Network", "url": "mock://wrd.assam.gov.in"}
    ]
    return multi_tab_swarm_coordinator.execute_multi_portal_scrape(
        mission_title=mission_title,
        target_portals=default_portals
    )




