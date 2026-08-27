import asyncio
import uuid
from datetime import UTC, datetime
from decimal import Decimal

import pytest
import pytest_asyncio
from app.core.security import create_access_token
from app.db.manager import db_manager
from app.main import app
from app.models.account import Account
from app.models.category import Category
from app.models.enums import AccountType, CategoryType, TransactionType
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.reporting_repository import ReportingRepository
from app.repositories.user_repository import UserRepository
from app.schemas.transaction import CreateTransactionRequest
from app.services.reporting_service import ReportingService
from httpx import ASGITransport, AsyncClient


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db():
    """Initialize database connection for each test."""
    await db_manager.connect()
    yield db_manager
    await db_manager.disconnect()


@pytest_asyncio.fixture
async def clean_db(db):
    """Clean up test collections before each test."""
    collections = [
        "transactions",
        "accounts",
        "categories",
        "audit_trails",
        "users",
    ]
    for collection_name in collections:
        await db_manager.database[collection_name].delete_many({})
    yield
    for collection_name in collections:
        await db_manager.database[collection_name].delete_many({})


@pytest_asyncio.fixture
async def user_a(clean_db):
    """Create user A for testing."""
    user_repo = UserRepository()
    user = User(
        email=f"usera_{uuid.uuid4().hex[:8]}@test.com",
        password_hash="hashed_password",
        full_name="User A",
    )
    created = await user_repo.create_user(user)
    return created


@pytest_asyncio.fixture
async def user_b(clean_db):
    """Create user B for testing."""
    user_repo = UserRepository()
    user = User(
        email=f"userb_{uuid.uuid4().hex[:8]}@test.com",
        password_hash="hashed_password",
        full_name="User B",
    )
    created = await user_repo.create_user(user)
    return created


@pytest_asyncio.fixture
async def user_a_token(user_a):
    """Generate JWT token for user A."""
    return create_access_token(user_a.id)


@pytest_asyncio.fixture
async def user_b_token(user_b):
    """Generate JWT token for user B."""
    return create_access_token(user_b.id)


@pytest_asyncio.fixture
async def account_a(user_a):
    """Create an account for user A."""
    account_repo = AccountRepository()
    account = Account(
        user_id=user_a.id,
        name="Test Account",
        institution="Test Bank",
        type=AccountType.BANK,
        currency="INR",
    )
    created = await account_repo.create(account)
    return created


@pytest_asyncio.fixture
async def account_b(user_b):
    """Create an account for user B."""
    account_repo = AccountRepository()
    account = Account(
        user_id=user_b.id,
        name="User B Account",
        institution="Test Bank",
        type=AccountType.BANK,
        currency="INR",
    )
    created = await account_repo.create(account)
    return created


@pytest_asyncio.fixture
async def category_a1(user_a):
    """Create first category for user A."""
    cat_repo = CategoryRepository()
    cat = Category(
        user_id=user_a.id,
        name="Food",
        type=CategoryType.EXPENSE,
    )
    created = await cat_repo.create(cat)
    return created


@pytest_asyncio.fixture
async def category_a2(user_a):
    """Create second category for user A."""
    cat_repo = CategoryRepository()
    cat = Category(
        user_id=user_a.id,
        name="Transport",
        type=CategoryType.EXPENSE,
    )
    created = await cat_repo.create(cat)
    return created


@pytest_asyncio.fixture
async def category_b1(user_b):
    """Create category for user B."""
    cat_repo = CategoryRepository()
    cat = Category(
        user_id=user_b.id,
        name="User B Category",
        type=CategoryType.EXPENSE,
    )
    created = await cat_repo.create(cat)
    return created


@pytest_asyncio.fixture
async def reporting_service():
    """Create reporting service instance."""
    repo = ReportingRepository()
    return ReportingService(reporting_repository=repo)


@pytest_asyncio.fixture
async def setup_test_data(
    user_a, user_b, account_a, account_b, category_a1, category_a2, category_b1
):
    """Create test transactions for all reports."""
    from app.core.dependencies import transaction_service

    class MockUser:
        def __init__(self, user_id):
            self.id = user_id

    current_user_a = MockUser(user_a.id)
    current_user_b = MockUser(user_b.id)

    # Create transactions for user A
    # 1. Income INR 1000
    txn1 = CreateTransactionRequest(
        account_id=account_a.id,
        category_id=None,
        type=TransactionType.INCOME,
        amount=Decimal("1000.00"),
        currency="INR",
        transaction_date=datetime(2024, 1, 15, tzinfo=UTC),
        merchant="Salary Corp",
        description="Salary",
        reference="REF001",
    )
    created1 = await transaction_service.create_transaction(MockUser(user_a.id), txn1)

    # 2. Income USD 500
    txn2 = CreateTransactionRequest(
        account_id=account_a.id,
        category_id=None,
        type=TransactionType.INCOME,
        amount=Decimal("500.00"),
        currency="USD",
        transaction_date=datetime(2024, 2, 15, tzinfo=UTC),
        merchant="Freelance",
        description="Freelance work",
        reference="REF002",
    )
    created2 = await transaction_service.create_transaction(MockUser(user_a.id), txn2)

    # 3. Expense INR 200 (Food category)
    txn3 = CreateTransactionRequest(
        account_id=account_a.id,
        category_id=category_a1.id,
        type=TransactionType.EXPENSE,
        amount=Decimal("200.00"),
        currency="INR",
        transaction_date=datetime(2024, 1, 20, tzinfo=UTC),
        merchant="Amazon",
        description="Shopping",
        reference="REF003",
    )
    created3 = await transaction_service.create_transaction(MockUser(user_a.id), txn3)

    # 4. Expense INR 300 (Food category)
    txn4 = CreateTransactionRequest(
        account_id=account_a.id,
        category_id=category_a1.id,
        type=TransactionType.EXPENSE,
        amount=Decimal("300.00"),
        currency="INR",
        transaction_date=datetime(2024, 2, 20, tzinfo=UTC),
        merchant="Swiggy",
        description="Food delivery",
        reference="REF004",
    )
    created4 = await transaction_service.create_transaction(MockUser(user_a.id), txn4)

    # 5. Expense USD 100 (no category - uncategorized)
    txn5 = CreateTransactionRequest(
        account_id=account_a.id,
        category_id=None,
        type=TransactionType.EXPENSE,
        amount=Decimal("100.00"),
        currency="USD",
        transaction_date=datetime(2024, 3, 15, tzinfo=UTC),
        merchant="Unknown",
        description="Misc",
        reference="REF005",
    )
    created5 = await transaction_service.create_transaction(MockUser(user_a.id), txn5)

    # 6. Transfer INR 500
    txn6 = CreateTransactionRequest(
        account_id=account_a.id,
        category_id=None,
        type=TransactionType.TRANSFER,
        amount=Decimal("500.00"),
        currency="INR",
        transaction_date=datetime(2024, 3, 20, tzinfo=UTC),
        merchant=None,
        description="Transfer to savings",
        reference="REF006",
    )
    created6 = await transaction_service.create_transaction(MockUser(user_a.id), txn6)

    # 7. Adjustment INR 50
    txn7 = CreateTransactionRequest(
        account_id=account_a.id,
        category_id=None,
        type=TransactionType.ADJUSTMENT,
        amount=Decimal("50.00"),
        currency="INR",
        transaction_date=datetime(2024, 4, 1, tzinfo=UTC),
        merchant=None,
        description="Bank fee adjustment",
        reference="REF007",
    )
    created7 = await transaction_service.create_transaction(MockUser(user_a.id), txn7)

    # Create a transaction for user B to test isolation
    txn_b = CreateTransactionRequest(
        account_id=account_b.id,
        category_id=None,
        type=TransactionType.INCOME,
        amount=Decimal("1000.00"),
        currency="INR",
        transaction_date=datetime(2024, 1, 15, tzinfo=UTC),
        merchant="User B Salary",
        description="Salary",
        reference="REFB001",
    )
    await transaction_service.create_transaction(MockUser(user_b.id), txn_b)

    return {
        "created1": created1,
        "created2": created2,
        "created3": created3,
        "created4": created4,
        "created5": created5,
        "created6": created6,
        "created7": created7,
    }


class MockUser:
    def __init__(self, user_id):
        self.id = user_id


@pytest_asyncio.fixture
async def auth_headers_user_a(user_a_token):
    """Auth headers for user A."""
    return {"Authorization": f"Bearer {user_a_token}"}


@pytest_asyncio.fixture
async def auth_headers_user_b(user_b_token):
    """Auth headers for user B."""
    return {"Authorization": f"Bearer {user_b_token}"}


@pytest_asyncio.fixture
async def async_client():
    """Create an async HTTP client for testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def client(async_client):
    """Alias for async_client for backward compatibility."""
    return async_client
