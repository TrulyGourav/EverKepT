from __future__ import annotations

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EVERKEPT_", env_file=".env", extra="ignore")

    env: Literal["dev", "test", "prod"] = "dev"
    database_url: str = "postgresql+asyncpg://everkept:everkept@localhost:5432/everkept"
    s3_endpoint: str = "http://localhost:9000"
    s3_bucket: str = "everkept-blobs"
    # Demo mode shortens day-scale timers. It is refused in prod (see validate_for_env).
    demo_mode: bool = False

    def validate_for_env(self) -> None:
        if self.env == "prod" and self.demo_mode:
            raise RuntimeError("demo_mode must never be enabled in prod")
