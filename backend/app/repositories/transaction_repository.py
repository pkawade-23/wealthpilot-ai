import re
from typing import TYPE_CHECKING, Any

from bson import ObjectId
from bson.decimal128 import Decimal128

if TYPE_CHECKING:
    from pymongo.asynchronous.client_session import AsyncClientSession

from app.models.transaction import Transaction
from app.query.models import CursorPage
from app.query.paginator import paginate
from app.repositories.base import BaseRepository
from app.schemas.transaction import TransactionQueryParams


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
        query: TransactionQueryParams,
    ) -> CursorPage[Transaction]:
        return await paginate(
            collection=self.collection,
            filter=self._build_transaction_filter(user_id, query),
            query=query,
            model=Transaction,
        )

    def _build_transaction_filter(
        self,
        user_id: str,
        query: TransactionQueryParams,
    ) -> dict[str, Any]:
        filter_dict = self._merge_filters(
            self._active_filter(),
            {"user_id": user_id},
        )

        if query.account_id is not None:
            filter_dict["account_id"] = query.account_id

        if query.category_id is not None:
            filter_dict["category_id"] = query.category_id

        if query.type is not None:
            filter_dict["type"] = query.type.value

        if query.currency is not None:
            filter_dict["currency"] = query.currency

        if query.date_from is not None or query.date_to is not None:
            date_filter: dict[str, Any] = {}
            if query.date_from is not None:
                date_filter["$gte"] = query.date_from
            if query.date_to is not None:
                date_filter["$lte"] = query.date_to
            filter_dict["transaction_date"] = date_filter

        if query.min_amount is not None or query.max_amount is not None:
            amount_filter: dict[str, Any] = {}
            if query.min_amount is not None:
                amount_filter["$gte"] = Decimal128(query.min_amount)
            if query.max_amount is not None:
                amount_filter["$lte"] = Decimal128(query.max_amount)
            filter_dict["amount"] = amount_filter

        if query.merchant is not None:
            escaped = re.escape(query.merchant)
            filter_dict["merchant"] = {"$regex": escaped, "$options": "i"}

        if query.search is not None:
            escaped_search = re.escape(query.search)
            filter_dict["$or"] = [
                {"merchant": {"$regex": escaped_search, "$options": "i"}},
                {"description": {"$regex": escaped_search, "$options": "i"}},
                {"reference": {"$regex": escaped_search, "$options": "i"}},
            ]

        return filter_dict

    async def create(
        self,
        transaction_data: Transaction,
        session: AsyncClientSession | None = None,
    ) -> Transaction:
        document = transaction_data.model_dump(exclude={"id"})
        insertable_document = {
            **document,
            "amount": Decimal128(document["amount"]),
        }

        inserted_id = await super().create(insertable_document, session=session)

        return Transaction(
            id=str(inserted_id),
            **document,
        )

    async def update(
        self,
        transaction_id: str,
        update_data: Transaction,
        session: AsyncClientSession | None = None,
    ) -> Transaction | None:
        document = update_data.model_dump(
            exclude={"id", "created_at"},
            exclude_none=True,
        )

        if not document:
            return await self.find_by_id(transaction_id)

        if "amount" in document:
            document["amount"] = Decimal128(document["amount"])

        await super().update_one(
            self._merge_filters(
                self._active_filter(),
                {"_id": ObjectId(transaction_id)},
            ),
            {"$set": document},
            session=session,
        )

        return await self.find_by_id(transaction_id)

    async def delete(
        self,
        transaction_id: str,
        session: AsyncClientSession | None = None,
    ) -> bool:
        return await self.soft_delete(transaction_id, session=session)
