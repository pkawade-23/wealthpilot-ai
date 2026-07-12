import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.manager import db_manager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown.
    """

    # Startup
    logger.info("Starting WealthPilot AI...")
    await db_manager.connect()

    yield

    # Shutdown
    logger.info("Shutting down WealthPilot AI...")
    await db_manager.disconnect()
