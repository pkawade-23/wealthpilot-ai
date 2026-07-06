from datetime import UTC, datetime

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: str | None = None
    email: EmailStr
    password_hash: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
