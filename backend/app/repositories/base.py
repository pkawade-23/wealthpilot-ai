from abc import ABC, abstractmethod
from typing import TypeVar

from bson import ObjectId
from pymongo.asynchronous.client_session import AsyncClientSession
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

    def _active_filter(self) -> dict:
        return {
            "is_deleted": False,
        }

    def _merge_filters(
        self,
        *filters: dict,
    ) -> dict:
        query = {}

        for filter_dict in filters:
            query.update(filter_dict)

        return query

    async def create(
        self,
        document: dict,
        session: AsyncClientSession | None = None,
    ) -> str:
        result = await self.collection.insert_one(document, session=session)
        return result.inserted_id

    async def create_many(
        self,
        documents: list[dict],
        session: AsyncClientSession | None = None,
    ) -> list[str]:

        result = await self.collection.insert_many(documents, session=session)

        return [str(id) for id in result.inserted_ids]

    async def soft_delete(
        self,
        id: str,
        session: AsyncClientSession | None = None,
    ) -> bool:
        result = await self.collection.update_one(
            self._merge_filters(
                self._active_filter(),
                {"_id": ObjectId(id)},
            ),
            {
                "$set": {
                    "is_deleted": True,
                }
            },
            session=session,
        )

        return result.modified_count > 0

    async def update_one(
        self,
        filter: dict,
        update: dict,
        session: AsyncClientSession | None = None,
    ):
        return await self.collection.update_one(filter, update, session=session)
