from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import TransactionType


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
