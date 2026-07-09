from datetime import UTC, datetime

from pydantic import BaseModel, Field

from app.models.enums import AccountType


class Account(BaseModel):
    id: str | None = None
    user_id: str

    name: str
    institution: str
    type: AccountType
    currency: str = "INR"

    created_at: datetime | None = None
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
