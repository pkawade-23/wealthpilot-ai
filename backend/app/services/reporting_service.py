from decimal import Decimal
from datetime import datetime

from app.core.exceptions import ValidationException
from app.models.user import User
from app.repositories.reporting_repository import ReportingRepository
from app.schemas.reporting import (
    CashFlowReport,
    CategorySpending,
    ExpenseSummary,
    IncomeSummary,
    ReportQueryParams,
    SpendingByCategoryReport,
    TransactionSummary,
)


class ReportingService:
    def __init__(
        self,
        reporting_repository: ReportingRepository,
    ) -> None:
        self.reporting_repository = reporting_repository

    def _convert_decimal128(self, value: object) -> Decimal:
        from bson.decimal128 import Decimal128

        if isinstance(value, Decimal):
            return value
        if isinstance(value, Decimal128):
            return value.to_decimal()
        return Decimal(str(value))

    def _validate_date_range(self, query: ReportQueryParams) -> None:
        if query.date_from is not None and query.date_to is not None:
            if query.date_from > query.date_to:
                raise ValidationException(
                    message="date_from cannot exceed date_to",
                    code="INVALID_DATE_RANGE",
                )

    async def get_income_summary(
        self,
        current_user: User,
        query: ReportQueryParams,
    ) -> list[IncomeSummary]:
        self._validate_date_range(query)
        results = await self.reporting_repository.get_income_summary(
            user_id=current_user.id,
            date_from=query.date_from,
            date_to=query.date_to,
        )

        return [
            IncomeSummary(
                total_income=self._convert_decimal128(r["total_income"]),
                currency=r["currency"],
                transaction_count=r["transaction_count"],
            )
            for r in results
        ]

    async def get_expense_summary(
        self,
        current_user: User,
        query: ReportQueryParams,
    ) -> list[ExpenseSummary]:
        self._validate_date_range(query)
        results = await self.reporting_repository.get_expense_summary(
            user_id=current_user.id,
            date_from=query.date_from,
            date_to=query.date_to,
        )

        return [
            ExpenseSummary(
                total_expenses=self._convert_decimal128(r["total_expenses"]),
                currency=r["currency"],
                transaction_count=r["transaction_count"],
            )
            for r in results
        ]

    async def get_cash_flow(
        self,
        current_user: User,
        query: ReportQueryParams,
    ) -> list[CashFlowReport]:
        self._validate_date_range(query)
        results = await self.reporting_repository.get_cash_flow(
            user_id=current_user.id,
            date_from=query.date_from,
            date_to=query.date_to,
        )

        return [
            CashFlowReport(
                income=IncomeSummary(
                    total_income=self._convert_decimal128(r["total_income"]),
                    currency=r["currency"],
                    transaction_count=r["income_transaction_count"],
                ),
                expenses=ExpenseSummary(
                    total_expenses=self._convert_decimal128(r["total_expenses"]),
                    currency=r["currency"],
                    transaction_count=r["expense_transaction_count"],
                ),
                net_cash_flow=self._convert_decimal128(r["net_cash_flow"]),
                currency=r["currency"],
            )
            for r in results
        ]

    async def get_spending_by_category(
        self,
        current_user: User,
        query: ReportQueryParams,
    ) -> list[SpendingByCategoryReport]:
        self._validate_date_range(query)
        results = await self.reporting_repository.get_spending_by_category(
            user_id=current_user.id,
            date_from=query.date_from,
            date_to=query.date_to,
        )

        by_currency: dict[str, list[dict]] = {}
        for r in results:
            currency = r["currency"]
            if currency not in by_currency:
                by_currency[currency] = []
            by_currency[currency].append(r)

        reports: list[SpendingByCategoryReport] = []

        for currency, items in by_currency.items():
            total_expenses = sum(
                self._convert_decimal128(item["total_amount"]) for item in items
            )

            categories = []
            for item in items:
                category_name = item.get("category_name")
                if category_name is None:
                    category_name = "Uncategorized"

                total_amount = self._convert_decimal128(item["total_amount"])
                percentage = (
                    Decimal("0")
                    if total_expenses == 0
                    else (total_amount / total_expenses * Decimal("100")).quantize(
                        Decimal("0.01")
                    )
                )

                categories.append(
                    CategorySpending(
                        category_id=item.get("category_id"),
                        category_name=item.get("category_name") or "Uncategorized",
                        total_amount=self._convert_decimal128(item["total_amount"]),
                        percentage=percentage,
                        transaction_count=item["transaction_count"],
                        currency=currency,
                    )
                )

            reports.append(
                SpendingByCategoryReport(
                    categories=categories,
                    total_expenses=total_expenses,
                    currency=currency,
                )
            )

        return reports

    async def get_transaction_summary(
        self,
        current_user: User,
        query: ReportQueryParams,
    ) -> list[TransactionSummary]:
        self._validate_date_range(query)
        results = await self.reporting_repository.get_transaction_summary(
            user_id=current_user.id,
            date_from=query.date_from,
            date_to=query.date_to,
        )

        return [
            TransactionSummary(
                total_count=r["total_count"],
                income_count=r["income_count"],
                expense_count=r["expense_count"],
                transfer_count=r["transfer_count"],
                adjustment_count=r["adjustment_count"],
                currency=r["currency"],
            )
            for r in results
        ]
