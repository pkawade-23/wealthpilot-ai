from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import LoginRequest, RegisterRequest


class AuthService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()

    async def register(
        self,
        request: RegisterRequest,
    ) -> User:
        existing_user = await self.user_repository.find_by_email(request.email)

        if existing_user is not None:
            raise ConflictException(
                message="Email is already registered.",
                code="EMAIL_ALREADY_EXISTS",
            )

        hashed_password = hash_password(request.password)

        user = User(
            email=request.email,
            password_hash=hashed_password,
        )

        return await self.user_repository.create_user(user)

    async def login(self, request: LoginRequest) -> str:
        user = await self.user_repository.find_by_email(request.email)

        if user is None:
            raise UnauthorizedException(
                message="Invalid email or password.",
                code="INVALID_CREDENTIALS",
            )

        if not verify_password(request.password, user.password_hash):
            raise UnauthorizedException(
                message="Invalid email or password.",
                code="INVALID_CREDENTIALS",
            )

        return create_access_token(user.id)

    async def find_by_id(self, user_id: str) -> User | None:
        return await self.user_repository.find_by_id(user_id)
