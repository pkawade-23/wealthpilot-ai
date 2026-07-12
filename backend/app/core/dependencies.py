from app.repositories.account_repository import AccountRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.user_repository import UserRepository
from app.services.account_service import AccountService
from app.services.auth_service import AuthService
from app.services.category_service import CategoryService

user_repository = UserRepository()
account_repository = AccountRepository()
category_repository = CategoryRepository()

auth_service = AuthService(
    user_repository=user_repository,
    category_repository=category_repository,
)

account_service = AccountService(
    account_repository=account_repository,
)

category_service = CategoryService(
    category_repository=category_repository,
)
