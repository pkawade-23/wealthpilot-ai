from fastapi import APIRouter, Depends, status

from app.core.auth import get_current_user
from app.core.dependencies import category_service
from app.models.user import User
from app.query.params import QueryParams
from app.schemas.category import CreateCategoryRequest
from app.schemas.response import ApiResponse

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_category(
    request: CreateCategoryRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return ApiResponse.success_response(
        await category_service.create_category(
            current_user,
            request,
        ),
        message="Category created successfully.",
    )


@router.get("", status_code=status.HTTP_200_OK)
async def get_categories(
    query: QueryParams = Depends(),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return ApiResponse.success_response(
        await category_service.get_categories(current_user, query),
        message="Categories retrieved successfully.",
    )


@router.get("/{category_id}", status_code=status.HTTP_200_OK)
async def get_category_by_id(
    category_id: str,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    category = await category_service.get_category_by_id(category_id, current_user)
    return ApiResponse.success_response(
        category, message="Category retrieved successfully."
    )


@router.patch("/{category_id}", status_code=status.HTTP_200_OK)
async def update_category(
    category_id: str,
    request: CreateCategoryRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    category = await category_service.update_category(
        category_id, request, current_user
    )
    return ApiResponse.success_response(
        category, message="Category updated successfully."
    )


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: str,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    await category_service.delete_category(category_id, current_user)
    return ApiResponse.success_response(message="Category deleted successfully.")
