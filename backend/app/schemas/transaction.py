from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import TransactionType
from app.query.params import QueryParams


class TransactionSortField(StrEnum):
    TRANSACTION_DATE = "transaction_date"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    AMOUNT = "amount"
    MERCHANT = "merchant"
    CURRENCY = "currency"
    TYPE = "type"


class TransactionQueryParams(QueryParams):
    account_id: str | None = None
    category_id: str | None = None
    type: TransactionType | None = None
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    date_from: datetime | None = None
    date_to: datetime | None = None
    min_amount: Decimal | None = Field(default=None, gt=0)
    max_amount: Decimal | None = Field(default=None, gt=0)
    merchant: str | None = None

    sort_by: TransactionSortField = TransactionSortField.TRANSACTION_DATE

    @model_validator(mode="after")
    def validate_ranges(self) -> TransactionQueryParams:
        if (
            self.min_amount is not None
            and self.max_amount is not None
            and self.min_amount > self.max_amount
        ):
            raise ValueError("min_amount cannot exceed max_amount")
        if (
            self.date_from is not None
            and self.date_to is not None
            and self.date_from > self.date_to
        ):
            raise ValueError("date_from cannot exceed date_to")
        return self


class CreateTransactionRequest(BaseModel):
    account_id: str = Field(min_length=1)
    category_id: str | None = None
    type: TransactionType = TransactionType.EXPENSE
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    transaction_date: datetime
    merchant: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=500)
    reference: str | None = Field(default=None, max_length=100)


class UpdateTransactionRequest(BaseModel):
    category_id: str | None = None
    type: TransactionType | None = None
    amount: Decimal | None = Field(default=None, gt=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    transaction_date: datetime | None = None
    merchant: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=500)
    reference: str | None = Field(default=None, max_length=100)


class CreateTransferRequest(BaseModel):
    source_account_id: str = Field(min_length=1)
    destination_account_id: str = Field(min_length=1)
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    transaction_date: datetime
    description: str | None = Field(default=None, max_length=500)
    reference: str | None = Field(default=None, max_length=100)


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    account_id: str
    category_id: str | None
    type: TransactionType
    amount: Decimal
    currency: str
    transaction_date: datetime
    merchant: str | None
    description: str | None
    reference: str | None
    transfer_id: str | None
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False
