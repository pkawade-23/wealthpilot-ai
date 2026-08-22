from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import AuditAction


class AuditTrail(BaseModel):
    id: str | None = None
    user_id: str
    collection: str
    document_id: str
    action: AuditAction
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
    metadata: dict[str, Any] | None = None
