from datetime import UTC, datetime

from bson import ObjectId

from app.models.account import Account
from app.query.models import CursorPage
from app.query.paginator import paginate
from app.query.params import QueryParams
from app.repositories.base import BaseRepository


class AccountRepository(BaseRepository):
    @property
    def collection_name(self) -> str:
        return "accounts"

    def _to_model(
        self,
        document: dict,
    ) -> Account:
        document["id"] = str(document.pop("_id"))
        return Account.model_validate(document)

    async def find_by_id(
        self,
        account_id: str,
    ) -> Account | None:
        document = await self.collection.find_one(
            self._merge_filters(
                self._active_filter(),
                {"_id": ObjectId(account_id)},
            )
        )

        if document is None:
            return None

        return self._to_model(document)

    # async def find_by_user(
    #     self,
    #     user_id: str,
    #     query: QueryParams,
    # ) -> CursorPage[Account]:
    #     filter = (
    #         self._merge_filters(
    #             self._active_filter(),
    #             {"user_id": user_id},
    #         ),
    #     )
    #     return await paginate(
    #         collection=self.collection,
    #         filter=filter,
    #         query=query,
    #         model=Account,
    #     )

    async def find_by_user(
        self,
        user_id: str,
        query: QueryParams,
    ) -> CursorPage[Account]:
        return await paginate(
            collection=self.collection,
            filter=self._merge_filters(
                self._active_filter(),
                {"user_id": user_id},
            ),
            query=query,
            model=Account,
        )

    async def create(
        self,
        account_data: Account,
    ) -> Account:
        document = account_data.model_dump(exclude={"id"})
        document["created_at"] = datetime.now(UTC)
        inserted_id = await super().create(document)
        return Account(
            id=str(inserted_id),
            **document,
        )

    async def update(
        self,
        account_id: str,
        update_data: Account,
    ) -> Account | None:
        document = update_data.model_dump(
            exclude={"id", "created_at"},
            exclude_none=True,
        )
        if not document:
            return await self.find_by_id(account_id)
        await self.collection.update_one(
            self._merge_filters(
                self._active_filter(),
                {"_id": ObjectId(account_id)},
            ),
            {"$set": document},
        )
        return await self.find_by_id(account_id)

    async def delete(
        self,
        account_id: str,
    ) -> bool:
        return await self.soft_delete(account_id)

    async def find_by_user_and_name(
        self,
        user_id: str,
        name: str,
    ) -> Account | None:
        filter = self._merge_filters(
            self._active_filter(),
            {
                "user_id": user_id,
                "name": name,
            },
        )
        document = await self.collection.find_one(filter)

        if document is None:
            return None

        return self._to_model(document)
