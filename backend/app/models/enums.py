from dataclasses import dataclass
from enum import StrEnum


class AccountType(StrEnum):
    BANK = "BANK"
    CREDIT_CARD = "CREDIT_CARD"
    BROKERAGE = "BROKERAGE"
    CASH = "CASH"
    LOAN = "LOAN"


class CategoryType(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass(frozen=True)
class DefaultCategory:
    name: str
    type: CategoryType


DEFAULT_CATEGORIES = [
    DefaultCategory("Salary", CategoryType.INCOME),
    DefaultCategory("Bonus", CategoryType.INCOME),
    DefaultCategory("Interest", CategoryType.INCOME),
    DefaultCategory("Dividend", CategoryType.INCOME),
    DefaultCategory("Gift", CategoryType.INCOME),
    DefaultCategory("Food", CategoryType.EXPENSE),
    DefaultCategory("Groceries", CategoryType.EXPENSE),
    DefaultCategory("Rent", CategoryType.EXPENSE),
    DefaultCategory("Utilities", CategoryType.EXPENSE),
    DefaultCategory("Fuel", CategoryType.EXPENSE),
    DefaultCategory("Transport", CategoryType.EXPENSE),
    DefaultCategory("Shopping", CategoryType.EXPENSE),
    DefaultCategory("Healthcare", CategoryType.EXPENSE),
    DefaultCategory("Entertainment", CategoryType.EXPENSE),
    DefaultCategory("Travel", CategoryType.EXPENSE),
    DefaultCategory("Education", CategoryType.EXPENSE),
]
