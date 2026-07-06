from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.schemas.response import ApiResponse
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=ApiResponse[UserResponse],
)
async def get_me(current_user=(Depends(get_current_user))):  # noqa: B008
    return ApiResponse.success_response(current_user)
