from __future__ import annotations

from fastapi import FastAPI

from everkept import __version__
from everkept.platform.config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    settings.validate_for_env()
    app = FastAPI(title="EverKepT", version=__version__)

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    return app
