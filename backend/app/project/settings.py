from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR.parent / "static"


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    email_service_url: str
    email_service_api_key: str
    email_service_sender: str
    run_mode: Literal["dev", "stage", "prod"] = "dev"
    allow_origins: list[str] = ["*"]
    secret_key: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env.dev", env_prefix="APP_", extra="allow")


settings = Settings()  # pyright: ignore[reportCallIssue]
