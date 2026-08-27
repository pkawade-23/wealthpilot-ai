from datetime import datetime
from typing import Any

from bson.decimal128 import Decimal128

from app.models.enums import TransactionType
from app.repositories.base import BaseRepository


class ReportingRepository(BaseRepository):
    @property
    def collection_name(self) -> str:
        return "transactions"

    def _build_base_filter(
        self,
        user_id: str,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> dict[str, Any]:
        filter_dict = self._merge_filters(
            self._active_filter(),
            {"user_id": user_id},
        )

        if date_from is not None or date_to is not None:
            date_filter: dict[str, Any] = {}
            if date_from is not None:
                date_filter["$gte"] = date_from
            if date_to is not None:
                date_filter["$lte"] = date_to
            filter_dict["transaction_date"] = date_filter

        return filter_dict

    async def get_income_summary(
        self,
        user_id: str,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[dict[str, Any]]:
        base_filter = self._build_base_filter(user_id, date_from, date_to)
        base_filter["type"] = TransactionType.INCOME.value

        pipeline: list[dict[str, Any]] = [
            {"$match": base_filter},
            {
                "$group": {
                    "_id": "$currency",
                    "total_income": {"$sum": "$amount"},
                    "transaction_count": {"$sum": 1},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "currency": "$_id",
                    "total_income": 1,
                    "transaction_count": 1,
                }
            },
        ]

        cursor = await self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        return results

    async def get_expense_summary(
        self,
        user_id: str,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[dict[str, Any]]:
        base_filter = self._build_base_filter(user_id, date_from, date_to)
        base_filter["type"] = TransactionType.EXPENSE.value

        pipeline: list[dict[str, Any]] = [
            {"$match": base_filter},
            {
                "$group": {
                    "_id": "$currency",
                    "total_expenses": {"$sum": "$amount"},
                    "transaction_count": {"$sum": 1},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "currency": "$_id",
                    "total_expenses": 1,
                    "transaction_count": 1,
                }
            },
        ]

        cursor = await self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        return results

    async def get_cash_flow(
        self,
        user_id: str,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[dict[str, Any]]:
        base_filter = self._build_base_filter(user_id, date_from, date_to)

        pipeline: list[dict[str, Any]] = [
            {"$match": base_filter},
            {
                "$project": {
                    "currency": 1,
                    "type": 1,
                    "amount": 1,
                    "signed_amount": {
                        "$switch": {
                            "branches": [
                                {
                                    "case": {
                                        "$eq": [
                                            "$type",
                                            TransactionType.INCOME.value,
                                        ]
                                    },
                                    "then": "$amount",
                                },
                                {
                                    "case": {
                                        "$eq": [
                                            "$type",
                                            TransactionType.EXPENSE.value,
                                        ]
                                    },
                                    "then": {"$multiply": ["$amount", -1]},
                                },
                            ],
                            "default": Decimal128("0"),
                        }
                    },
                }
            },
            {
                "$group": {
                    "_id": "$currency",
                    "total_income": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$type", TransactionType.INCOME.value]},
                                "$amount",
                                0,
                            ]
                        }
                    },
                    "income_transaction_count": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$type", TransactionType.INCOME.value]},
                                1,
                                0,
                            ]
                        }
                    },
                    "total_expenses": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$type", TransactionType.EXPENSE.value]},
                                "$amount",
                                0,
                            ]
                        }
                    },
                    "expense_transaction_count": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$type", TransactionType.EXPENSE.value]},
                                1,
                                0,
                            ]
                        }
                    },
                    "net_cash_flow": {"$sum": "$signed_amount"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "currency": "$_id",
                    "total_income": 1,
                    "income_transaction_count": 1,
                    "total_expenses": 1,
                    "expense_transaction_count": 1,
                    "net_cash_flow": 1,
                }
            },
        ]

        cursor = await self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        return results

    async def get_spending_by_category(
        self,
        user_id: str,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[dict[str, Any]]:
        base_filter = self._build_base_filter(user_id, date_from, date_to)
        base_filter["type"] = TransactionType.EXPENSE.value

        pipeline: list[dict[str, Any]] = [
            {"$match": base_filter},
            {
                "$lookup": {
                    "from": "categories",
                    "let": {"cat_id": "$category_id", "txn_user_id": "$user_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {
                                            "$eq": [
                                                "$_id",
                                                {
                                                    "$convert": {
                                                        "input": "$$cat_id",
                                                        "to": "objectId",
                                                        "onError": None,
                                                        "onNull": None,
                                                    },
                                                },
                                            ]
                                        },
                                        {"$eq": ["$user_id", "$$txn_user_id"]},
                                    ]
                                }
                            }
                        },
                        {"$project": {"_id": 1, "name": 1}},
                    ],
                    "as": "category_info",
                }
            },
            {
                "$unwind": {
                    "path": "$category_info",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {
                "$group": {
                    "_id": {"category_id": "$category_id", "currency": "$currency"},
                    "category_name": {"$first": "$category_info.name"},
                    "total_amount": {"$sum": "$amount"},
                    "transaction_count": {"$sum": 1},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "category_id": "$_id.category_id",
                    "currency": "$_id.currency",
                    "category_name": 1,
                    "total_amount": 1,
                    "transaction_count": 1,
                }
            },
        ]

        cursor = await self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        return results

    async def get_transaction_summary(
        self,
        user_id: str,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[dict[str, Any]]:
        base_filter = self._build_base_filter(user_id, date_from, date_to)

        pipeline: list[dict[str, Any]] = [
            {"$match": base_filter},
            {
                "$group": {
                    "_id": "$currency",
                    "total_count": {"$sum": 1},
                    "income_count": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$type", TransactionType.INCOME.value]},
                                1,
                                0,
                            ]
                        }
                    },
                    "expense_count": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$type", TransactionType.EXPENSE.value]},
                                1,
                                0,
                            ]
                        }
                    },
                    "transfer_count": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$type", TransactionType.TRANSFER.value]},
                                1,
                                0,
                            ]
                        }
                    },
                    "adjustment_count": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$eq": [
                                        "$type",
                                        TransactionType.ADJUSTMENT.value,
                                    ]
                                },
                                1,
                                0,
                            ]
                        }
                    },
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "currency": "$_id",
                    "total_count": 1,
                    "income_count": 1,
                    "expense_count": 1,
                    "transfer_count": 1,
                    "adjustment_count": 1,
                }
            },
        ]

        cursor = await self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        return results
