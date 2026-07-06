from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

user_repository = UserRepository()

auth_service = AuthService(user_repository)
