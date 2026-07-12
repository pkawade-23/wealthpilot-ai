from fastapi import APIRouter, Depends, status

from app.core.auth import get_current_user
from app.core.dependencies import account_service
from app.models.user import User
from app.query.params import QueryParams
from app.schemas.account import CreateAccountRequest
from app.schemas.response import ApiResponse

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_account(
    request: CreateAccountRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return ApiResponse.success_response(
        await account_service.create_account(
            current_user,
            request,
        )
    )


@router.get("", status_code=status.HTTP_200_OK)
async def get_accounts(
    query: QueryParams = Depends(),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return ApiResponse.success_response(
        await account_service.get_accounts(current_user, query)
    )


@router.get("/{account_id}", status_code=status.HTTP_200_OK)
async def get_account_by_id(
    account_id: str,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    account = await account_service.get_account_by_id(account_id, current_user)
    return ApiResponse.success_response(account)


@router.patch("/{account_id}", status_code=status.HTTP_200_OK)
async def update_account(
    account_id: str,
    request: CreateAccountRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    account = await account_service.update_account(account_id, request, current_user)
    return ApiResponse.success_response(account)


@router.delete("/{account_id}", status_code=status.HTTP_200_OK)
async def delete_account(
    account_id: str,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    await account_service.delete_account(account_id, current_user)
    return ApiResponse.success_response(message="Account deleted successfully.")
