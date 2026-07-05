from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import settings


class DatabaseManager:
    """Manages the MongoDB client lifecycle."""

    def __init__(self) -> None:
        self._client: AsyncMongoClient | None = None
        self._database: AsyncDatabase | None = None

    async def connect(self) -> None:
        """Connect to MongoDB."""

        self._client = AsyncMongoClient(settings.mongodb_uri)

        # Verify the connection
        await self._client.admin.command("ping")

        self._database = self._client[settings.database_name]

    async def disconnect(self) -> None:
        """Close the MongoDB client."""

        if self._client is not None:
            self._client.close()

            self._client = None
            self._database = None

    def get_database(self) -> AsyncDatabase:
        """Return the configured database."""

        if self._database is None:
            raise RuntimeError("Database has not been initialized.")

        return self._database


db_manager = DatabaseManager()