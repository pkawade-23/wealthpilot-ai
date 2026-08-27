from fastapi import APIRouter, Depends, status

from app.core.auth import get_current_user
from app.core.dependencies import reporting_service
from app.models.user import User
from app.schemas.reporting import ReportQueryParams
from app.schemas.response import ApiResponse

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/income-summary", status_code=status.HTTP_200_OK)
async def get_income_summary(
    query: ReportQueryParams = Depends(),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return ApiResponse.success_response(
        await reporting_service.get_income_summary(current_user, query),
        message="Income summary retrieved successfully.",
    )


@router.get("/expense-summary", status_code=status.HTTP_200_OK)
async def get_expense_summary(
    query: ReportQueryParams = Depends(),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return ApiResponse.success_response(
        await reporting_service.get_expense_summary(current_user, query),
        message="Expense summary retrieved successfully.",
    )


@router.get("/cash-flow", status_code=status.HTTP_200_OK)
async def get_cash_flow(
    query: ReportQueryParams = Depends(),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return ApiResponse.success_response(
        await reporting_service.get_cash_flow(current_user, query),
        message="Cash flow report retrieved successfully.",
    )


@router.get("/spending-by-category", status_code=status.HTTP_200_OK)
async def get_spending_by_category(
    query: ReportQueryParams = Depends(),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return ApiResponse.success_response(
        await reporting_service.get_spending_by_category(current_user, query),
        message="Spending by category report retrieved successfully.",
    )


@router.get("/transaction-summary", status_code=status.HTTP_200_OK)
async def get_transaction_summary(
    query: ReportQueryParams = Depends(),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return ApiResponse.success_response(
        await reporting_service.get_transaction_summary(current_user, query),
        message="Transaction summary retrieved successfully.",
    )
