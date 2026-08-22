from app.models.audit_trail import AuditTrail
from app.query.models import CursorPage
from app.query.paginator import paginate
from app.query.params import QueryParams
from app.repositories.base import BaseRepository


class AuditRepository(BaseRepository):
    @property
    def collection_name(self) -> str:
        return "audit_trails"

    async def find_by_user(
        self,
        user_id: str,
        query: QueryParams,
    ) -> CursorPage[AuditTrail]:
        return await paginate(
            collection=self.collection,
            filter={"user_id": user_id},
            query=query,
            model=AuditTrail,
        )

    async def create(
        self,
        audit: AuditTrail,
    ) -> str:
        document = audit.model_dump(
            exclude={"id"},
        )

        return await super().create(document)
