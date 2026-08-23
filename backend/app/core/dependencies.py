from app.repositories.account_repository import AccountRepository
from app.repositories.audit_repository import AuditRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository
from app.services.account_service import AccountService
from app.services.audit_service import AuditService
from app.services.auth_service import AuthService
from app.services.category_service import CategoryService
from app.services.transaction_service import TransactionService

user_repository = UserRepository()
account_repository = AccountRepository()
category_repository = CategoryRepository()
transaction_repository = TransactionRepository()
audit_repository = AuditRepository()

audit_service = AuditService(
    audit_repository=audit_repository,
)

auth_service = AuthService(
    user_repository=user_repository,
    category_repository=category_repository,
)

account_service = AccountService(
    account_repository=account_repository,
    audit_service=audit_service,
)

category_service = CategoryService(
    category_repository=category_repository,
    audit_service=audit_service,
)

transaction_service = TransactionService(
    transaction_repository=transaction_repository,
    account_repository=account_repository,
    category_repository=category_repository,
    audit_service=audit_service,
)
