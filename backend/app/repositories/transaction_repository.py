from bson import ObjectId
from bson.decimal128 import Decimal128

from app.models.transaction import Transaction
from app.query.models import CursorPage
from app.query.paginator import paginate
from app.query.params import QueryParams
from app.repositories.base import BaseRepository


class TransactionRepository(BaseRepository):
    @property
    def collection_name(self) -> str:
        return "transactions"

    def _to_model(
        self,
        document: dict,
    ) -> Transaction:
        document["id"] = str(document.pop("_id"))
        return Transaction.model_validate(document)

    async def find_by_id(
        self,
        transaction_id: str,
    ) -> Transaction | None:
        document = await self.collection.find_one(
            self._merge_filters(
                self._active_filter(),
                {"_id": ObjectId(transaction_id)},
            )
        )

        if document is None:
            return None

        return self._to_model(document)

    async def find_by_user(
        self,
        user_id: str,
        query: QueryParams,
    ) -> CursorPage[Transaction]:
        return await paginate(
            collection=self.collection,
            filter=self._merge_filters(
                self._active_filter(),
                {"user_id": user_id},
            ),
            query=query,
            model=Transaction,
        )

    async def create(
        self,
        transaction_data: Transaction,
    ) -> Transaction:
        document = transaction_data.model_dump(exclude={"id"})
        insertable_document = {
            **document,
            "amount": Decimal128(document["amount"]),
        }

        inserted_id = await super().create(insertable_document)

        return Transaction(
            id=str(inserted_id),
            **document,
        )

    async def update(
        self,
        transaction_id: str,
        update_data: Transaction,
    ) -> Transaction | None:
        document = update_data.model_dump(
            exclude={"id", "created_at"},
            exclude_none=True,
        )

        if not document:
            return await self.find_by_id(transaction_id)

        if "amount" in document:
            document["amount"] = Decimal128(document["amount"])

        await self.collection.update_one(
            self._merge_filters(
                self._active_filter(),
                {"_id": ObjectId(transaction_id)},
            ),
            {"$set": document},
        )

        return await self.find_by_id(transaction_id)

    async def delete(
        self,
        transaction_id: str,
    ) -> bool:
        return await self.soft_delete(transaction_id)
