from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logging import setup_logging


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

    app.include_router(health_router)

    return app