from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "AxomAI AGI"
    ENV: str = "development"
    
    # PostgreSQL
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "axomai_agi_user"
    DB_PASSWORD: str = "samarjit"
    DB_NAME: str = "axomai_agi"
    
    DATABASE_URL: str = Field(
        default="postgresql://axomai_agi_user:samarjit@localhost:5432/axomai_agi"
    )
    ASYNC_DATABASE_URL: str = Field(
        default="postgresql+asyncpg://axomai_agi_user:samarjit@localhost:5432/axomai_agi"
    )
    
    # Storage
    STORAGE_DIR: Path = BASE_DIR / "storage"
    
    # Optional LLM Keys
    GEMINI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)

