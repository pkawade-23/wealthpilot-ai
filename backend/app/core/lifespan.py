from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.manager import db_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown.
    """

    # Startup
    await db_manager.connect()

    yield

    # Shutdown
    await db_manager.disconnect()