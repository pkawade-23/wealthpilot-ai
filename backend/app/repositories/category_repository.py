from datetime import UTC, datetime

from bson import ObjectId

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
        document = await self.collection.find_one({"_id": ObjectId(category_id)})

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
            filter={"user_id": user_id},
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
            {"user_id": user_id, "name": name, "type": type}
        )

        if document is None:
            return None

        return self._to_model(document)

    async def create(
        self,
        category_data: Category,
    ) -> Category:
        document = category_data.model_dump(exclude={"id"})
        document["created_at"] = datetime.now(UTC)
        inserted_id = await super().create(document)
        return Category(
            id=str(inserted_id),
            **document,
        )

    async def update(
        self,
        category_id: str,
        update_data: Category,
    ) -> Category | None:
        document = update_data.model_dump(
            exclude={"id", "created_at"},
            exclude_none=True,
        )

        if not document:
            return await self.find_by_id(category_id)

        await self.collection.update_one(
            {"_id": ObjectId(category_id)}, {"$set": document}
        )

        return await self.find_by_id(category_id)

    async def delete(
        self,
        category_id: str,
    ) -> bool:
        category = await self.find_by_id(category_id)
        if category is None:
            return False
        await self.collection.delete_one({"_id": ObjectId(category_id)})
        return True

    async def seed_default_categories(
        self,
        user_id: str,
    ) -> None:
        documents = [
            {
                "user_id": user_id,
                "name": category.name,
                "type": category.type,
                "is_system": True,
            }
            for category in DEFAULT_CATEGORIES
        ]

        await self.create_many(documents)
