import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, BigInteger, Text, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from axomai.db.session import Base

def utc_now():
    return datetime.now(timezone.utc)

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False, index=True)
    file_path = Column(Text, nullable=False)
    file_type = Column(String(50), nullable=False, index=True) # PDF, DOCX, XLSX, PPTX, etc.
    mime_type = Column(String(100), nullable=True)
    file_size_bytes = Column(BigInteger, nullable=False)
    file_hash = Column(String(64), nullable=False, unique=True, index=True) # SHA256
    page_count = Column(Integer, default=1)
    
    # Unified Document Model (Full structured AST in JSONB)
    udm_data = Column(JSONB, nullable=True)
    
    # General extracted metadata (author, created date, sheet names, etc.)
    metadata_ = Column("metadata", JSONB, default=dict)
    
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    # Relationships
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Document {self.filename} ({self.file_type}) - Pages: {self.page_count}>"


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    page_number = Column(Integer, nullable=True, index=True) # 1-based page index
    content_type = Column(String(50), default="text") # text, table, chart, image_caption, code
    content = Column(Text, nullable=False)
    
    # Specific attributes (section title, bbox coordinates, table headers)
    chunk_metadata = Column(JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    document = relationship("Document", back_populates="chunks")

    __table_args__ = (
        Index("ix_chunks_doc_page", "document_id", "page_number"),
    )


class AgentSession(Base):
    __tablename__ = "agent_sessions"

    id = Column(String(64), primary_key=True) # session uuid or custom id
    agent_name = Column(String(100), default="Z1 Alpha", index=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    logs = relationship("AgentTaskLog", back_populates="session", cascade="all, delete-orphan")


class AgentTaskLog(Base):
    __tablename__ = "agent_task_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), ForeignKey("agent_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True, index=True)
    
    user_query = Column(Text, nullable=False)
    task_type = Column(String(100), nullable=True) # SUMMARY, DATA_ANALYSIS, TABLE_EXTRACT, etc.
    tools_used = Column(JSONB, default=list) # List of tools executed with timestamps
    evidence = Column(JSONB, default=list) # List of sources (page_number, snippet, table_id)
    response = Column(Text, nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=utc_now)

    session = relationship("AgentSession", back_populates="logs")

