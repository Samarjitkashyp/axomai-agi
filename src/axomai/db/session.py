from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from axomai.config import settings

# Base model for SQLAlchemy ORM
Base = declarative_base()

# Synchronous Engine & Session
sync_engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Asynchronous Engine & Session
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

def get_db():
    """Dependency for synchronous DB session"""
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    """Dependency for asynchronous DB session"""
    async with AsyncSessionLocal() as session:
        yield session

def init_db():
    """Create all tables in PostgreSQL"""
    Base.metadata.create_all(bind=sync_engine)

