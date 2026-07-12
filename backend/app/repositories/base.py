from abc import ABC, abstractmethod
from typing import TypeVar

from pymongo.asynchronous.collection import AsyncCollection

from app.db.manager import db_manager

T = TypeVar("T")


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
        return result.inserted_id

    async def create_many(
        self,
        documents: list[dict],
    ) -> list[str]:

        result = await self.collection.insert_many(documents)

        return [str(id) for id in result.inserted_ids]
