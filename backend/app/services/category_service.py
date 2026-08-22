from app.core.exceptions import ConflictException
from app.models.category import Category
from app.models.enums import AuditAction
from app.models.user import User
from app.query.models import CursorPage, map_cursor_page
from app.query.params import QueryParams
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryResponse, CreateCategoryRequest
from app.services.audit_service import AuditService


class CategoryService:
    def __init__(
        self,
        category_repository: CategoryRepository,
        audit_service: AuditService,
    ) -> None:
        self.category_repository = category_repository
        self.audit_service = audit_service

    async def create_category(
        self,
        current_user: User,
        request: CreateCategoryRequest,
    ) -> CategoryResponse:
        existing_category = await self.category_repository.find_by_name(
            current_user.id, request.name, request.type
        )

        if existing_category is not None:
            raise ConflictException(
                message="Category with this name and type already exists for the user.",
                code="CATEGORY_ALREADY_EXISTS",
            )
        request.name = request.name.strip()
        category = Category(user_id=current_user.id, **request.model_dump())
        created_category = await self.category_repository.create(category)

        await self.audit_service.create_audit_trail(
            user_id=current_user.id,
            collection=self.category_repository.collection_name,
            document_id=created_category.id,
            action=AuditAction.CREATE,
            after=created_category.model_dump(),
        )

        return CategoryResponse.model_validate(created_category)

    async def get_categories(
        self,
        current_user: User,
        query: QueryParams,
    ) -> CursorPage[CategoryResponse]:
        categories = await self.category_repository.find_by_user(
            user_id=current_user.id,
            query=query,
        )
        return map_cursor_page(
            categories,
            CategoryResponse,
        )

    async def get_category_by_id(
        self,
        category_id: str,
        current_user: User,
    ) -> CategoryResponse:
        category = await self.category_repository.find_by_id(category_id)

        if category is None or category.user_id != current_user.id:
            raise ConflictException(
                message="Category not found or does not belong to the user.",
                code="CATEGORY_NOT_FOUND",
            )

        return CategoryResponse.model_validate(category)

    async def update_category(
        self,
        category_id: str,
        request: CreateCategoryRequest,
        current_user: User,
    ) -> CategoryResponse:
        category = await self.category_repository.find_by_id(category_id)

        if category is not None and category.is_system:
            raise ConflictException(
                message="System categories cannot be updated.", code="SYSTEM_CATEGORY"
            )

        if category is None or category.user_id != current_user.id:
            raise ConflictException(
                message="Category not found or does not belong to the user.",
                code="CATEGORY_NOT_FOUND",
            )

        # Check for name conflict with other accounts of the user
        existing_category = await self.category_repository.find_by_name(
            current_user.id, request.name, request.type
        )
        if existing_category is not None and existing_category.id != category_id:
            raise ConflictException(
                message="Category with this name already exists for the user.",
                code="CATEGORY_ALREADY_EXISTS",
            )

        updated_category_data = Category(
            id=category.id,
            user_id=category.user_id,
            **request.model_dump(),
        )
        updated_category = await self.category_repository.update(
            category_id, updated_category_data
        )

        await self.audit_service.create_audit_trail(
            user_id=current_user.id,
            collection=self.category_repository.collection_name,
            document_id=category_id,
            action=AuditAction.UPDATE,
            before=category.model_dump(),
            after=updated_category.model_dump(),
        )

        return CategoryResponse.model_validate(updated_category)

    async def delete_category(
        self,
        category_id: str,
        current_user: User,
    ) -> None:
        category = await self.category_repository.find_by_id(category_id)

        if category is None or category.user_id != current_user.id:
            raise ConflictException(
                message="Category not found or does not belong to the user.",
                code="CATEGORY_NOT_FOUND",
            )

        if category.is_system:
            raise ConflictException(
                message="System categories cannot be deleted.", code="SYSTEM_CATEGORY"
            )

        state_before_delete = category.model_dump()

        await self.category_repository.delete(category_id)

        await self.audit_service.create_audit_trail(
            user_id=current_user.id,
            collection=self.category_repository.collection_name,
            document_id=category_id,
            action=AuditAction.DELETE,
            before=state_before_delete,
            after={**state_before_delete, "is_deleted": True},
        )

        return CategoryResponse.model_validate(category)
