from fastapi import APIRouter, Depends, status

from app.core.auth import get_current_user
from app.core.dependencies import transaction_service
from app.models.user import User
from app.query.params import QueryParams
from app.schemas.response import ApiResponse
from app.schemas.transaction import (
    CreateTransactionRequest,
    CreateTransferRequest,
    UpdateTransactionRequest,
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    request: CreateTransactionRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return ApiResponse.success_response(
        await transaction_service.create_transaction(
            current_user,
            request,
        ),
        message="Transaction created successfully.",
    )


@router.get("", status_code=status.HTTP_200_OK)
async def get_transactions(
    query: QueryParams = Depends(),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return ApiResponse.success_response(
        await transaction_service.get_transactions(current_user, query),
        message="Transactions retrieved successfully.",
    )


@router.post("/transfer", status_code=status.HTTP_201_CREATED)
async def create_transfer(
    request: CreateTransferRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    source, destination = await transaction_service.create_transfer(
        current_user,
        request,
    )
    return ApiResponse.success_response(
        {"source": source, "destination": destination},
        message="Transfer created successfully.",
    )


@router.get("/{transaction_id}", status_code=status.HTTP_200_OK)
async def get_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    transaction = await transaction_service.get_transaction(
        transaction_id, current_user
    )
    return ApiResponse.success_response(
        transaction, message="Transaction retrieved successfully."
    )


@router.patch("/{transaction_id}", status_code=status.HTTP_200_OK)
async def update_transaction(
    transaction_id: str,
    request: UpdateTransactionRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    transaction = await transaction_service.update_transaction(
        transaction_id, request, current_user
    )
    return ApiResponse.success_response(
        transaction, message="Transaction updated successfully."
    )


@router.delete("/{transaction_id}", status_code=status.HTTP_200_OK)
async def delete_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    await transaction_service.delete_transaction(transaction_id, current_user)
    return ApiResponse.success_response(message="Transaction deleted successfully.")
