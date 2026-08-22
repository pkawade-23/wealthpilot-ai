from fastapi import APIRouter, Depends, status

from app.core.auth import get_current_user
from app.core.dependencies import audit_service
from app.models.user import User
from app.query.params import QueryParams
from app.schemas.response import ApiResponse

router = APIRouter(
    prefix="/audit-trails",
    tags=["Audit Trails"],
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_audit_trails(
    query: QueryParams = Depends(),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return ApiResponse.success_response(
        await audit_service.get_audit_trails(current_user.id, query),
        message="Audit trails retrieved successfully.",
    )
