import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from app.core.exceptions import ConflictException
from app.db.manager import db_manager
from app.models.enums import AuditAction, TransactionType
from app.models.transaction import Transaction
from app.models.user import User
from app.query.models import CursorPage, map_cursor_page
from app.query.params import QueryParams
from app.repositories.account_repository import AccountRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import (
    CreateTransactionRequest,
    CreateTransferRequest,
    TransactionResponse,
    UpdateTransactionRequest,
)
from app.services.audit_service import AuditService


class TransactionService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        account_repository: AccountRepository,
        category_repository: CategoryRepository,
        audit_service: AuditService,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.account_repository = account_repository
        self.category_repository = category_repository
        self.audit_service = audit_service

    async def create_transaction(
        self,
        current_user: User,
        request: CreateTransactionRequest,
    ) -> TransactionResponse:
        account = await self.account_repository.find_by_id(request.account_id)
        if account is None or account.user_id != current_user.id:
            raise ConflictException(
                message="Account not found or does not belong to the user.",
                code="ACCOUNT_NOT_FOUND",
            )

        if request.category_id is not None:
            category = await self.category_repository.find_by_id(request.category_id)
            if category is None or category.user_id != current_user.id:
                raise ConflictException(
                    message="Category not found or does not belong to the user.",
                    code="CATEGORY_NOT_FOUND",
                )

        transaction = Transaction(
            user_id=current_user.id,
            transfer_id=None,
            **request.model_dump(),
        )
        created_transaction = await self.transaction_repository.create(transaction)

        await self.audit_service.create_audit_trail(
            user_id=current_user.id,
            collection=self.transaction_repository.collection_name,
            document_id=created_transaction.id,
            action=AuditAction.CREATE,
            after=created_transaction.model_dump(),
        )

        return TransactionResponse.model_validate(created_transaction)

    async def get_transactions(
        self,
        current_user: User,
        query: QueryParams,
    ) -> CursorPage[TransactionResponse]:
        transactions = await self.transaction_repository.find_by_user(
            user_id=current_user.id,
            query=query,
        )
        return map_cursor_page(
            transactions,
            TransactionResponse,
        )

    async def get_transaction(
        self,
        transaction_id: str,
        current_user: User,
    ) -> TransactionResponse:
        transaction = await self.transaction_repository.find_by_id(transaction_id)

        if transaction is None or transaction.user_id != current_user.id:
            raise ConflictException(
                message="Transaction not found or does not belong to the user.",
                code="TRANSACTION_NOT_FOUND",
            )

        return TransactionResponse.model_validate(transaction)

    async def update_transaction(
        self,
        transaction_id: str,
        request: UpdateTransactionRequest,
        current_user: User,
    ) -> TransactionResponse:
        transaction = await self.transaction_repository.find_by_id(transaction_id)

        if transaction is None or transaction.user_id != current_user.id:
            raise ConflictException(
                message="Transaction not found or does not belong to the user.",
                code="TRANSACTION_NOT_FOUND",
            )

        if request.category_id is not None:
            category = await self.category_repository.find_by_id(request.category_id)
            if category is None or category.user_id != current_user.id:
                raise ConflictException(
                    message="Category not found or does not belong to the user.",
                    code="CATEGORY_NOT_FOUND",
                )

        before_state = transaction.model_dump()

        update_data = request.model_dump(exclude_none=True)
        if not update_data:
            return TransactionResponse.model_validate(transaction)

        update_data["updated_at"] = datetime.now(UTC)

        updated_transaction_data = Transaction(
            id=transaction.id,
            user_id=transaction.user_id,
            account_id=transaction.account_id,
            transfer_id=transaction.transfer_id,
            created_at=transaction.created_at,
            is_deleted=transaction.is_deleted,
            **update_data,
        )
        updated_transaction = await self.transaction_repository.update(
            transaction_id, updated_transaction_data
        )

        await self.audit_service.create_audit_trail(
            user_id=current_user.id,
            collection=self.transaction_repository.collection_name,
            document_id=transaction_id,
            action=AuditAction.UPDATE,
            before=before_state,
            after=updated_transaction.model_dump(),
        )

        return TransactionResponse.model_validate(updated_transaction)

    async def delete_transaction(
        self,
        transaction_id: str,
        current_user: User,
    ) -> None:
        transaction = await self.transaction_repository.find_by_id(transaction_id)

        if transaction is None or transaction.user_id != current_user.id:
            raise ConflictException(
                message="Transaction not found or does not belong to the user.",
                code="TRANSACTION_NOT_FOUND",
            )

        state_before_delete = transaction.model_dump()

        await self.transaction_repository.delete(transaction_id)

        await self.audit_service.create_audit_trail(
            user_id=current_user.id,
            collection=self.transaction_repository.collection_name,
            document_id=transaction_id,
            action=AuditAction.DELETE,
            before=state_before_delete,
            after={**state_before_delete, "is_deleted": True},
        )

        return None

    async def create_transfer(
        self,
        current_user: User,
        request: CreateTransferRequest,
    ) -> tuple[TransactionResponse, TransactionResponse]:
        if request.source_account_id == request.destination_account_id:
            raise ConflictException(
                message="Source and destination accounts must be different.",
                code="TRANSFER_ACCOUNTS_MATCH",
            )

        source_account = await self.account_repository.find_by_id(
            request.source_account_id
        )
        if source_account is None or source_account.user_id != current_user.id:
            raise ConflictException(
                message="Source account not found or does not belong to the user.",
                code="SOURCE_ACCOUNT_NOT_FOUND",
            )

        destination_account = await self.account_repository.find_by_id(
            request.destination_account_id
        )
        if (
            destination_account is None
            or destination_account.user_id != current_user.id
        ):
            raise ConflictException(
                message="Destination account not found or does not belong to the user.",
                code="DESTINATION_ACCOUNT_NOT_FOUND",
            )

        transfer_id = str(uuid.uuid4())

        session = db_manager.start_session()
        async with session:
            async with await session.start_transaction():
                source_transaction = Transaction(
                    user_id=current_user.id,
                    account_id=request.source_account_id,
                    category_id=None,
                    type=TransactionType.TRANSFER,
                    amount=request.amount,
                    currency=request.currency,
                    transaction_date=request.transaction_date,
                    merchant=None,
                    description=request.description,
                    reference=request.reference,
                    transfer_id=transfer_id,
                    is_deleted=False,
                )
                created_source = await self.transaction_repository.create(
                    source_transaction, session=session
                )

                destination_transaction = Transaction(
                    user_id=current_user.id,
                    account_id=request.destination_account_id,
                    category_id=None,
                    type=TransactionType.TRANSFER,
                    amount=request.amount,
                    currency=request.currency,
                    transaction_date=request.transaction_date,
                    merchant=None,
                    description=request.description,
                    reference=request.reference,
                    transfer_id=transfer_id,
                    is_deleted=False,
                )
                created_destination = await self.transaction_repository.create(
                    destination_transaction, session=session
                )

                await self.audit_service.create_audit_trail(
                    user_id=current_user.id,
                    collection=self.transaction_repository.collection_name,
                    document_id=created_source.id,
                    action=AuditAction.CREATE,
                    after=created_source.model_dump(),
                    session=session,
                    raise_on_error=True,
                )

                await self.audit_service.create_audit_trail(
                    user_id=current_user.id,
                    collection=self.transaction_repository.collection_name,
                    document_id=created_destination.id,
                    action=AuditAction.CREATE,
                    after=created_destination.model_dump(),
                    session=session,
                    raise_on_error=True,
                )

        return (
            TransactionResponse.model_validate(created_source),
            TransactionResponse.model_validate(created_destination),
        )
