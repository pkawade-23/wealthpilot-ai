from datetime import UTC, datetime
from typing import TYPE_CHECKING

from bson import ObjectId

if TYPE_CHECKING:
    from pymongo.asynchronous.client_session import AsyncClientSession

from app.models.category import Category
from app.models.enums import DEFAULT_CATEGORIES
from app.query.models import CursorPage
from app.query.paginator import paginate
from app.query.params import QueryParams
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository):
    @property
    def collection_name(self) -> str:
        return "categories"

    def _to_model(
        self,
        document: dict,
    ) -> Category:
        document["id"] = str(document.pop("_id"))
        return Category.model_validate(document)

    async def find_by_id(self, category_id: str) -> Category | None:
        document = await self.collection.find_one(
            self._merge_filters(
                self._active_filter(),
                {"_id": ObjectId(category_id)},
            )
        )

        if document is None:
            return None

        return self._to_model(document)

    async def find_by_user(
        self,
        user_id: str,
        query: QueryParams,
    ) -> CursorPage[Category]:
        return await paginate(
            collection=self.collection,
            filter=self._merge_filters(
                self._active_filter(),
                {"user_id": user_id},
            ),
            query=query,
            model=Category,
        )

    async def find_by_name(
        self,
        user_id: str,
        name: str,
        type: str,
    ) -> Category | None:
        document = await self.collection.find_one(
            self._merge_filters(
                self._active_filter(),
                {
                    "user_id": user_id,
                    "name": name,
                    "type": type,
                },
            )
        )

        if document is None:
            return None

        return self._to_model(document)

    async def create(
        self,
        category_data: Category,
        session: AsyncClientSession | None = None,
    ) -> Category:
        document = category_data.model_dump(exclude={"id"})
        document["created_at"] = datetime.now(UTC)
        inserted_id = await super().create(document, session=session)
        return Category(
            id=str(inserted_id),
            **document,
        )

    async def update(
        self,
        category_id: str,
        update_data: Category,
        session: AsyncClientSession | None = None,
    ) -> Category | None:
        document = update_data.model_dump(
            exclude={"id", "created_at"},
            exclude_none=True,
        )

        if not document:
            return await self.find_by_id(category_id)

        await super().update_one(
            self._merge_filters(
                self._active_filter(),
                {"_id": ObjectId(category_id)},
            ),
            {"$set": document},
            session=session,
        )

        return await self.find_by_id(category_id)

    async def delete(
        self,
        category_id: str,
        session: AsyncClientSession | None = None,
    ) -> bool:
        return await self.soft_delete(category_id, session=session)

    async def seed_default_categories(
        self,
        user_id: str,
        session: AsyncClientSession | None = None,
    ) -> None:
        documents = [
            {
                "user_id": user_id,
                "name": category.name,
                "type": category.type,
                "is_system": True,
                "is_deleted": False,
            }
            for category in DEFAULT_CATEGORIES
        ]

        await super().create_many(documents, session=session)
