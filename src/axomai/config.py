import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "AxomAI AGI"
    ENV: str = "development"
    
    # PostgreSQL Configuration (Strictly pulled from .env or environment)
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "axomai_agi_user"
    DB_PASSWORD: str = Field(default="", description="Database password securely supplied via .env")
    DB_NAME: str = "axomai_agi"
    
    DATABASE_URL: str = Field(
        default="postgresql://axomai_agi_user@localhost:5432/axomai_agi"
    )
    ASYNC_DATABASE_URL: str = Field(
        default="postgresql+asyncpg://axomai_agi_user@localhost:5432/axomai_agi"
    )
    
    # Storage
    STORAGE_DIR: Path = BASE_DIR / "storage"
    
    # Optional LLM Keys
    GEMINI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None

    @model_validator(mode="after")
    def assemble_db_urls(self):
        if self.DB_PASSWORD:
            user_auth = f"{self.DB_USER}:{self.DB_PASSWORD}"
            self.DATABASE_URL = f"postgresql://{user_auth}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            self.ASYNC_DATABASE_URL = f"postgresql+asyncpg://{user_auth}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return self

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
