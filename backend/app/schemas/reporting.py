from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ReportQueryParams(BaseModel):
    date_from: datetime | None = None
    date_to: datetime | None = None


class IncomeSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_income: Decimal
    currency: str
    transaction_count: int


class ExpenseSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_expenses: Decimal
    currency: str
    transaction_count: int


class CashFlowReport(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    income: IncomeSummary
    expenses: ExpenseSummary
    net_cash_flow: Decimal
    currency: str


class CategorySpending(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_id: str | None
    category_name: str
    total_amount: Decimal
    percentage: Decimal
    transaction_count: int
    currency: str


class SpendingByCategoryReport(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    categories: list[CategorySpending]
    total_expenses: Decimal
    currency: str


class TransactionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_count: int
    income_count: int
    expense_count: int
    transfer_count: int
    adjustment_count: int
    currency: str


IncomeSummary.model_rebuild()
ExpenseSummary.model_rebuild()
CashFlowReport.model_rebuild()
SpendingByCategoryReport.model_rebuild()
TransactionSummary.model_rebuild()
