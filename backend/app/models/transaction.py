from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated

from bson.decimal128 import Decimal128
from pydantic import BaseModel, BeforeValidator, Field

from app.models.enums import TransactionType


def coerce_decimal128(value: object) -> object:
    if isinstance(value, Decimal128):
        return value.to_decimal()

    return value


class Transaction(BaseModel):
    id: str | None = None
    user_id: str
    account_id: str
    category_id: str | None = None
    type: TransactionType

    amount: Annotated[Decimal, BeforeValidator(coerce_decimal128)] = Field(gt=0)
    currency: str
    transaction_date: datetime

    merchant: str | None = None
    description: str | None = None
    reference: str | None = None
    transfer_id: str | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
    is_deleted: bool = False
