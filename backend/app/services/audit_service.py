import logging
from decimal import Decimal
from typing import Any

from bson.decimal128 import Decimal128

from app.models.audit_trail import AuditTrail
from app.models.enums import AuditAction
from app.query.models import CursorPage, map_cursor_page
from app.query.params import QueryParams
from app.repositories.audit_repository import AuditRepository
from app.schemas.audit_trail import AuditTrailResponse

logger = logging.getLogger(__name__)


def _convert_decimals(obj: Any) -> Any:
    """Recursively convert Decimal to Decimal128 for MongoDB storage."""
    if isinstance(obj, Decimal):
        return Decimal128(obj)
    if isinstance(obj, dict):
        return {k: _convert_decimals(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_convert_decimals(v) for v in obj]
    return obj


class AuditService:
    def __init__(self, audit_repository: AuditRepository) -> None:
        self.audit_repository = audit_repository

    async def get_audit_trails(
        self,
        user_id: str,
        query: QueryParams,
    ) -> CursorPage[AuditTrailResponse]:
        audit_trails = await self.audit_repository.find_by_user(
            user_id=user_id,
            query=query,
        )
        return map_cursor_page(
            audit_trails,
            AuditTrailResponse,
        )

    async def create_audit_trail(
        self,
        user_id: str,
        collection: str,
        document_id: str,
        action: AuditAction,
        before: dict[str, Any] | None = None,
        after: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str | None:
        audit_trail = AuditTrail(
            user_id=user_id,
            collection=collection,
            document_id=document_id,
            action=action,
            before=_convert_decimals(before),
            after=_convert_decimals(after),
            metadata=_convert_decimals(metadata),
        )

        try:
            return await self.audit_repository.create(audit_trail)
        except Exception:
            logger.exception(
                "Failed to record %s audit trail for %s/%s",
                action.value,
                collection,
                document_id,
            )
            return None
