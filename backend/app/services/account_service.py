from app.core.exceptions import ConflictException
from app.models.account import Account
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountResponse, CreateAccountRequest


class AccountService:
    def __init__(self) -> None:
        self.account_repository = AccountRepository()

    async def create_account(
        self,
        current_user: User,
        request: CreateAccountRequest,
    ) -> AccountResponse:
        existing_account = await self.account_repository.find_by_user_and_name(
            current_user.id, request.name
        )

        if existing_account is not None:
            raise ConflictException(
                message="An account with this name already exists for the user.",
                code="ACCOUNT_ALREADY_EXISTS",
            )

        account = Account(user_id=current_user.id, **request.model_dump())
        created_account = await self.account_repository.create(account)

        return AccountResponse.model_validate(created_account)

    async def get_accounts(
        self,
        current_user: User,
    ) -> list[AccountResponse]:
        accounts = await self.account_repository.find_by_user(current_user.id)
        return [AccountResponse.model_validate(account) for account in accounts]

    async def get_account_by_id(
        self,
        account_id: str,
        current_user: User,
    ) -> AccountResponse:
        account = await self.account_repository.find_by_id(account_id)

        if account is None or account.user_id != current_user.id:
            raise ConflictException(
                message="Account not found or does not belong to the user.",
                code="ACCOUNT_NOT_FOUND",
            )

        return AccountResponse.model_validate(account)

    async def update_account(
        self,
        account_id: str,
        request: CreateAccountRequest,
        current_user: User,
    ) -> AccountResponse:
        account = await self.account_repository.find_by_id(account_id)

        if account is None or account.user_id != current_user.id:
            raise ConflictException(
                message="Account not found or does not belong to the user.",
                code="ACCOUNT_NOT_FOUND",
            )

        # Check for name conflict with other accounts of the user
        existing_account = await self.account_repository.find_by_user_and_name(
            current_user.id, request.name
        )
        if existing_account is not None and existing_account.id != account_id:
            raise ConflictException(
                message="An account with this name already exists for the user.",
                code="ACCOUNT_ALREADY_EXISTS",
            )

        updated_account_data = Account(
            id=account.id,
            user_id=account.user_id,
            **request.model_dump(),
        )
        updated_account = await self.account_repository.update(
            account_id, updated_account_data
        )

        return AccountResponse.model_validate(updated_account)

    async def delete_account(
        self,
        account_id: str,
        current_user: User,
    ) -> None:
        account = await self.account_repository.find_by_id(account_id)

        if account is None or account.user_id != current_user.id:
            raise ConflictException(
                message="Account not found or does not belong to the user.",
                code="ACCOUNT_NOT_FOUND",
            )

        await self.account_repository.delete(account_id)

        return AccountResponse.model_validate(account)
