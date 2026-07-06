from fastapi import APIRouter, status

from app.schemas.response import ApiResponse
from app.schemas.user import RegisterRequest, UserResponse
from app.services.auth_service import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
) -> ApiResponse[UserResponse]:
    user = await auth_service.register(request)

    response = UserResponse(
        id=user.id,
        email=user.email,
    )

    return ApiResponse.success_response(response)
