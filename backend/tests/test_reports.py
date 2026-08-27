from datetime import UTC, datetime
from decimal import Decimal

from app.core.dependencies import transaction_service
from app.models.enums import TransactionType
from app.schemas.transaction import CreateTransactionRequest
from bson.decimal128 import Decimal128


def to_decimal(val):
    """Convert Decimal128 or Decimal to Decimal for comparison."""
    if isinstance(val, Decimal128):
        return val.to_decimal()
    return val


class TestIncomeSummary:
    """Tests for GET /reports/income-summary"""

    async def test_income_summary_no_filters(
        self, client, user_a_token, setup_test_data
    ):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get("/reports/income-summary", headers=headers)
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 2

        inr_income = next(i for i in data if i["currency"] == "INR")
        usd_income = next(i for i in data if i["currency"] == "USD")
        assert inr_income["total_income"] == "1000.00"
        assert usd_income["total_income"] == "500.00"
        assert inr_income["transaction_count"] == 1
        assert usd_income["transaction_count"] == 1

    async def test_income_summary_excludes_non_income(
        self, client, user_a_token, setup_test_data
    ):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get("/reports/income-summary", headers=headers)
        assert response.status_code == 200
        data = response.json()["data"]
        total_count = sum(item["transaction_count"] for item in data)
        assert total_count == 2

    async def test_income_summary_date_filtering(
        self, client, user_a_token, setup_test_data
    ):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get(
            "/reports/income-summary",
            headers=headers,
            params={"date_from": "2024-02-01", "date_to": "2024-02-28"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 1
        assert data[0]["currency"] == "USD"
        assert data[0]["total_income"] == "500.00"

    async def test_income_summary_invalid_date_range(
        self, client, user_a_token, setup_test_data
    ):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get(
            "/reports/income-summary",
            headers=headers,
            params={"date_from": "2024-12-31", "date_to": "2024-01-01"},
        )
        assert response.status_code == 422


class TestExpenseSummary:
    """Tests for GET /reports/expense-summary"""

    async def test_expense_summary_no_filters(
        self, client, user_a_token, setup_test_data
    ):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get("/reports/expense-summary", headers=headers)
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 2

        inr_exp = next(e for e in data if e["currency"] == "INR")
        usd_exp = next(e for e in data if e["currency"] == "USD")
        assert inr_exp["total_expenses"] == "500.00"
        assert usd_exp["total_expenses"] == "100.00"
        assert inr_exp["transaction_count"] == 2
        assert usd_exp["transaction_count"] == 1

    async def test_expense_summary_excludes_non_expense(
        self, client, user_a_token, setup_test_data
    ):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get("/reports/expense-summary", headers=headers)
        assert response.status_code == 200
        data = response.json()["data"]
        total_count = sum(item["transaction_count"] for item in data)
        assert total_count == 3

    async def test_expense_summary_date_filtering(
        self, client, user_a_token, setup_test_data
    ):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get(
            "/reports/expense-summary",
            headers=headers,
            params={"date_from": "2024-02-01", "date_to": "2024-02-28"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 1
        assert data[0]["currency"] == "INR"
        assert data[0]["total_expenses"] == "300.00"


class TestCashFlow:
    """Tests for GET /reports/cash-flow"""

    async def test_cash_flow_correct_signs(self, client, user_a_token, setup_test_data):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get("/reports/cash-flow", headers=headers)
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 2

        inr_cf = next(c for c in data if c["currency"] == "INR")
        usd_cf = next(c for c in data if c["currency"] == "USD")

        # INR: Income 1000 - Expense 500 = 500 (Transfer 500 and Adjustment 50 are neutral)
        assert inr_cf["income"]["total_income"] == "1000.00"
        assert inr_cf["expenses"]["total_expenses"] == "500.00"
        assert inr_cf["net_cash_flow"] == "500.00"
        assert inr_cf["income"]["transaction_count"] == 1
        assert inr_cf["expenses"]["transaction_count"] == 2

        # USD: Income 500 - Expense 100 = 400
        assert usd_cf["income"]["total_income"] == "500.00"
        assert usd_cf["expenses"]["total_expenses"] == "100.00"
        assert usd_cf["net_cash_flow"] == "400.00"
        assert usd_cf["income"]["transaction_count"] == 1
        assert usd_cf["expenses"]["transaction_count"] == 1

    async def test_cash_flow_transfer_neutrality(
        self, client, user_a_token, setup_test_data
    ):
        """Verify TRANSFER does not affect cash flow."""
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get("/reports/cash-flow", headers=headers)
        assert response.status_code == 200
        data = response.json()["data"]
        inr_cf = next(c for c in data if c["currency"] == "INR")
        # Transfer of 500 INR should NOT affect net_cash_flow
        # 1000 (income) - 500 (expense) = 500
        assert inr_cf["net_cash_flow"] == "500.00"

    async def test_cash_flow_adjustment_neutrality(
        self, client, user_a_token, setup_test_data
    ):
        """Verify ADJUSTMENT does not affect cash flow."""
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get("/reports/cash-flow", headers=headers)
        assert response.status_code == 200
        data = response.json()["data"]
        inr_cf = next(c for c in data if c["currency"] == "INR")
        # Adjustment of 50 INR should NOT affect net_cash_flow
        assert inr_cf["net_cash_flow"] == "500.00"


class TestSpendingByCategory:
    """Tests for GET /reports/spending-by-category"""

    async def test_spending_by_category_categorized(
        self, client, user_a_token, setup_test_data
    ):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get("/reports/spending-by-category", headers=headers)
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 2

        inr_report = next(s for s in data if s["currency"] == "INR")
        usd_report = next(s for s in data if s["currency"] == "USD")

        # INR: Food category with 500 total (200 + 300)
        assert len(inr_report["categories"]) == 1
        food_cat = inr_report["categories"][0]
        assert food_cat["category_name"] == "Food"
        assert food_cat["total_amount"] == "500.00"
        assert food_cat["percentage"] == "100.00"
        assert food_cat["transaction_count"] == 2
        assert food_cat["category_id"] is not None

        # USD: Uncategorized expense
        assert len(usd_report["categories"]) == 1
        usd_cat = usd_report["categories"][0]
        assert usd_cat["category_name"] == "Uncategorized"
        assert usd_cat["total_amount"] == "100.00"
        assert usd_cat["percentage"] == "100.00"
        assert usd_cat["category_id"] is None

    async def test_spending_by_category_percentages_per_currency(
        self, client, user_a_token, setup_test_data
    ):
        """Verify percentages are calculated per currency, not globally."""
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get("/reports/spending-by-category", headers=headers)
        assert response.status_code == 200
        data = response.json()["data"]

        for report in data:
            total_pct = sum(float(c["percentage"]) for c in report["categories"])
            assert abs(total_pct - 100.00) < 0.01


class TestTransactionSummary:
    """Tests for GET /reports/transaction-summary"""

    async def test_transaction_summary_counts(
        self, client, user_a_token, setup_test_data
    ):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get("/reports/transaction-summary", headers=headers)
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 2

        inr_summary = next(s for s in data if s["currency"] == "INR")
        usd_summary = next(s for s in data if s["currency"] == "USD")

        # INR: 1 income + 2 expense + 1 transfer + 1 adjustment = 5
        assert inr_summary["total_count"] == 5
        assert inr_summary["income_count"] == 1
        assert inr_summary["expense_count"] == 2
        assert inr_summary["transfer_count"] == 1
        assert inr_summary["adjustment_count"] == 1
        assert inr_summary["currency"] == "INR"

        # USD: 1 income + 1 expense = 2
        assert usd_summary["total_count"] == 2
        assert usd_summary["income_count"] == 1
        assert usd_summary["expense_count"] == 1
        assert usd_summary["transfer_count"] == 0
        assert usd_summary["adjustment_count"] == 0
        assert usd_summary["currency"] == "USD"


class TestMultiCurrency:
    """Tests for multi-currency separation"""

    async def test_no_currency_combination(self, client, user_a_token, setup_test_data):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get("/reports/income-summary", headers=headers)
        assert response.status_code == 200
        data = response.json()["data"]
        currencies = {item["currency"] for item in data}
        assert currencies == {"INR", "USD"}
        for item in data:
            assert item["currency"] in ["INR", "USD"]


class TestDateFiltering:
    """Tests for date filtering across all endpoints"""

    async def test_date_from_filter(self, client, user_a_token, setup_test_data):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get(
            "/reports/income-summary",
            headers=headers,
            params={"date_from": "2024-02-01"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 1
        assert data[0]["currency"] == "USD"

    async def test_date_to_filter(self, client, user_a_token, setup_test_data):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get(
            "/reports/income-summary", headers=headers, params={"date_to": "2024-01-31"}
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 1
        assert data[0]["currency"] == "INR"

    async def test_date_range(self, client, user_a_token, setup_test_data):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get(
            "/reports/income-summary",
            headers=headers,
            params={"date_from": "2024-01-01", "date_to": "2024-03-31"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 2

    async def test_date_range_no_results(self, client, user_a_token, setup_test_data):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get(
            "/reports/income-summary",
            headers=headers,
            params={"date_from": "2025-01-01", "date_to": "2025-12-31"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 0

    async def test_invalid_date_range_rejected(self, client, user_a_token):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get(
            "/reports/income-summary",
            headers=headers,
            params={"date_from": "2024-12-31", "date_to": "2024-01-01"},
        )
        assert response.status_code == 422


class TestSoftDelete:
    """Tests for soft-delete exclusion"""

    async def test_soft_deleted_excluded(
        self, client, user_a_token, setup_test_data, account_a, category_a1, user_a
    ):

        class MockUser:
            def __init__(self, user_id):
                self.id = user_id

        headers = {"Authorization": f"Bearer {user_a_token}"}

        # Create a transaction to delete
        delete_txn = CreateTransactionRequest(
            account_id=account_a.id,
            category_id=category_a1.id,
            type=TransactionType.EXPENSE,
            amount=Decimal("999.00"),
            currency="INR",
            transaction_date=datetime(2024, 5, 1, tzinfo=UTC),
            merchant="Test Delete",
            description="To be deleted",
            reference="DEL001",
        )
        to_delete = await transaction_service.create_transaction(
            MockUser(user_a.id), delete_txn
        )

        # Verify it appears
        before = await client.get("/reports/expense-summary", headers=headers)
        inr_exp_before = next(
            e for e in before.json()["data"] if e["currency"] == "INR"
        )
        print(f"Expense before delete: {inr_exp_before['total_expenses']}")

        # Delete it
        await transaction_service.delete_transaction(to_delete.id, MockUser(user_a.id))

        # Verify it's excluded
        after = await client.get("/reports/expense-summary", headers=headers)
        inr_exp_after = next(e for e in after.json()["data"] if e["currency"] == "INR")
        print(f"Expense after delete: {inr_exp_after['total_expenses']}")
        assert inr_exp_after["total_expenses"] == "500.00"


class TestUserIsolation:
    """Tests for user isolation (security)"""

    async def test_user_isolation_income(
        self, client, user_a_token, user_b_token, setup_test_data
    ):
        headers_a = {"Authorization": f"Bearer {user_a_token}"}
        headers_b = {"Authorization": f"Bearer {user_b_token}"}

        response_a = await client.get("/reports/income-summary", headers=headers_a)
        assert response_a.status_code == 200
        data_a = response_a.json()["data"]
        assert len(data_a) == 2

        response_b = await client.get("/reports/income-summary", headers=headers_b)
        assert response_b.status_code == 200
        data_b = response_b.json()["data"]
        assert len(data_b) == 1

    async def test_user_isolation_expense(
        self, client, user_a_token, user_b_token, setup_test_data
    ):
        headers_a = {"Authorization": f"Bearer {user_a_token}"}
        headers_b = {"Authorization": f"Bearer {user_b_token}"}

        response_a = await client.get("/reports/expense-summary", headers=headers_a)
        assert response_a.status_code == 200
        data_a = response_a.json()["data"]
        assert len(data_a) == 2

        response_b = await client.get("/reports/expense-summary", headers=headers_b)
        assert response_b.status_code == 200
        data_b = response_b.json()["data"]
        assert len(data_b) == 0


class TestAuthentication:
    """Tests for authentication requirements"""

    async def test_unauthenticated_income_summary(self, client):
        response = await client.get("/reports/income-summary")
        assert response.status_code == 401

    async def test_unauthenticated_expense_summary(self, client):
        response = await client.get("/reports/expense-summary")
        assert response.status_code == 401

    async def test_unauthenticated_cash_flow(self, client):
        response = await client.get("/reports/cash-flow")
        assert response.status_code == 401

    async def test_unauthenticated_spending_by_category(self, client):
        response = await client.get("/reports/spending-by-category")
        assert response.status_code == 401

    async def test_unauthenticated_transaction_summary(self, client):
        response = await client.get("/reports/transaction-summary")
        assert response.status_code == 401


class TestInvalidDateRange:
    """Tests for invalid date range validation"""

    async def test_invalid_date_range_income(
        self, client, user_a_token, setup_test_data
    ):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get(
            "/reports/income-summary",
            headers=headers,
            params={"date_from": "2024-12-31", "date_to": "2024-01-01"},
        )
        assert response.status_code == 422

    async def test_invalid_date_range_expense(self, client, user_a_token):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get(
            "/reports/expense-summary",
            headers=headers,
            params={"date_from": "2024-12-31", "date_to": "2024-01-01"},
        )
        assert response.status_code == 422

    async def test_invalid_date_range_cash_flow(self, client, user_a_token):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get(
            "/reports/cash-flow",
            headers=headers,
            params={"date_from": "2024-12-31", "date_to": "2024-01-01"},
        )
        assert response.status_code == 422

    async def test_invalid_date_range_spending(self, client, user_a_token):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get(
            "/reports/spending-by-category",
            headers=headers,
            params={"date_from": "2024-12-31", "date_to": "2024-01-01"},
        )
        assert response.status_code == 422

    async def test_invalid_date_range_transaction_summary(self, client, user_a_token):
        headers = {"Authorization": f"Bearer {user_a_token}"}
        response = await client.get(
            "/reports/transaction-summary",
            headers=headers,
            params={"date_from": "2024-12-31", "date_to": "2024-01-01"},
        )
        assert response.status_code == 422
