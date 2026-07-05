import logging

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages the MongoDB client lifecycle."""

    def __init__(self) -> None:
        self._client: AsyncMongoClient | None = None
        self._database: AsyncDatabase | None = None

    async def connect(self) -> None:
        logger.info(
            "Connecting to MongoDB database '%s'...",
            settings.database_name,
        )

        try:
            self._client = AsyncMongoClient(
                settings.mongodb_uri,
                serverSelectionTimeoutMS=5000,
            )

            await self._client.admin.command("ping")

            self._database = self._client[settings.database_name]

            logger.info(
                "Connected to MongoDB database '%s'.",
                settings.database_name,
            )

        except Exception:
            logger.exception("Failed to connect to MongoDB.")
            raise

    async def disconnect(self) -> None:
        """Close the MongoDB client."""

        if self._client is not None:
            logger.info("Closing MongoDB connection...")

            await self._client.close()

            self._client = None
            self._database = None

    def get_database(self) -> AsyncDatabase:
        """Return the configured database."""

        if self._database is None:
            raise RuntimeError("Database has not been initialized.")

        return self._database


db_manager = DatabaseManager()
