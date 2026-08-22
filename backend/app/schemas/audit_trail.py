from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.enums import AuditAction


class AuditTrailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    collection: str
    document_id: str
    action: AuditAction
    before: dict[str, Any] | None
    after: dict[str, Any] | None
    created_at: datetime
    metadata: dict[str, Any] | None
