from datetime import UTC, datetime

from pydantic import BaseModel, Field

from app.models.enums import CategoryType


class Category(BaseModel):
    id: str | None = None

    user_id: str

    name: str

    type: CategoryType

    is_system: bool = False

    created_at: datetime | None = None

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
