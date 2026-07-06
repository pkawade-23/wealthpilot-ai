from app.core.exceptions import ConflictException
from app.core.security import password_hasher
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import RegisterRequest


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

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

        hashed_password = password_hasher.hash(request.password)

        user = User(
            email=request.email,
            password_hash=hashed_password,
        )

        return await self.user_repository.create_user(user)


auth_service = AuthService(UserRepository())
