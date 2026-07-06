from fastapi import APIRouter

from app.schemas.response import ApiResponse
from app.services.system_service import system_service

router = APIRouter(
    prefix="/system",
    tags=["System"],
)


@router.get("")
async def get_system_info() -> ApiResponse[dict[str, str]]:
    """Return information about the running application."""

    return ApiResponse.success_response(
        system_service.get_system_info(),
    )
