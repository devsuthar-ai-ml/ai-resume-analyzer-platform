from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "AI Resume Analyzer Platform"
    api_prefix: str = "/api"
    secret_key: str = "change-this-secret"
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/resume_analyzer"
    max_upload_size_mb: int = 5
    allowed_file_extensions: str = ".pdf,.docx"
    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @field_validator("allowed_file_extensions")
    @classmethod
    def normalize_extensions(cls, value: str) -> str:
        return ",".join(ext.strip().lower() for ext in value.split(",") if ext.strip())


@lru_cache
def get_settings() -> Settings:
    return Settings()
