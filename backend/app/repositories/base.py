from abc import ABC, abstractmethod

from pymongo.asynchronous.collection import AsyncCollection

from app.db.manager import db_manager


class BaseRepository(ABC):
    """Base class for MongoDB repositories."""

    @property
    @abstractmethod
    def collection_name(self) -> str:
        """MongoDB collection name."""
        raise NotImplementedError

    @property
    def collection(self) -> AsyncCollection:
        """MongoDB collection instance."""
        return db_manager.database[self.collection_name]

    async def create(self, document: dict) -> str:
        result = await self.collection.insert_one(document)
        return str(result.inserted_id)
