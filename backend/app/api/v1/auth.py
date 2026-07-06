from fastapi import APIRouter, status

from app.core.dependencies import auth_service
from app.schemas.response import ApiResponse
from app.schemas.user import LoginRequest, RegisterRequest, TokenResponse, UserResponse

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


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(
    request: LoginRequest,
) -> ApiResponse[TokenResponse]:
    access_token = await auth_service.login(request)

    return ApiResponse.success_response(
        TokenResponse(
            access_token=access_token,
        )
    )
