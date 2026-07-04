# Finance Domain

## Purpose

The Finance domain contains the verified financial data of the user.

Unlike the Ingestion domain, which stores raw and intermediate data, the Finance domain stores only validated and approved financial records.

All dashboards, analytics, reports, budgets, AI insights, and financial simulations use data exclusively from this domain.

---

# Collections

The Finance domain consists of the following collections.

| Collection | Purpose |
|------------|---------|
| transactions | Verified financial transactions |
| accounts | Bank accounts, wallets, credit cards and investment accounts |
| categories | Transaction categories |
| budgets | User-defined budgets |
| financial_goals | Savings and investment goals |
| assets | User-owned assets |
| liabilities | Loans and financial obligations |

---

# Design Principles

The Finance domain follows these principles.

## Verified Data Only

Only verified transactions are stored in this domain.

No AI-generated or unreviewed data should exist here.

---

## Single Source of Truth

The `transactions` collection is the canonical source of financial activity.

All financial calculations originate from this collection.

---

## Immutable Financial History

Financial transactions should never be physically deleted.

Corrections should create an audit trail rather than removing historical data.

---

## User Ownership

Every financial record belongs to exactly one user.

There is no shared financial data between users.

---

## Referential Integrity

Finance collections reference one another using MongoDB ObjectIds.

Examples:

- Transactions reference Accounts
- Transactions reference Categories
- Budgets reference Categories
- Assets reference Users

---

## Auditability

Every financial record should remain traceable back to its origin.

Example:

Transaction

↓

Transaction Candidate

↓

Email / Document / Import

This enables complete transparency throughout the financial lifecycle.

# Transactions Collection

## Purpose

The `transactions` collection is the canonical source of financial activity within WealthPilot AI.

Every approved financial event is represented as a transaction. All dashboards, reports, budgets, AI insights, and financial calculations are generated exclusively from this collection.

Transactions are created only after successful user verification through the Review Center or through trusted manual entry.

---

# Responsibilities

The `transactions` collection is responsible for:

- Recording verified financial events
- Tracking money movement
- Supporting financial reporting
- Supporting budgeting
- Supporting AI analysis
- Maintaining traceability to the original source

---

# Relationships

```text
users
   │
   ▼
transactions
   │
   ├────────► accounts
   │
   ├────────► categories
   │
   ├────────► transaction_candidates
   │
   ├────────► budgets
   │
   └────────► financial_goals
```

Each transaction belongs to exactly one user.

Each transaction references:

- One account
- One category
- Zero or one transaction candidate

---

# Transaction Types

Supported values:

- EXPENSE
- INCOME
- TRANSFER

Examples:

Expense

- Grocery purchase
- Electricity bill
- Restaurant payment

Income

- Salary
- Bonus
- Interest
- Rental income

Transfer

- Bank to Wallet
- Wallet to Credit Card
- Savings Transfer

Transfers do not affect overall net worth and should be handled separately in reporting.

---

# Transaction Status

Supported values:

- POSTED
- PENDING
- CANCELLED

Normally, approved transactions are created as `POSTED`.

Future bank integrations may initially create transactions with a `PENDING` status.

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Owner of the transaction |
| accountId | ObjectId | Yes | Financial account |
| categoryId | ObjectId | Yes | Transaction category |
| candidateId | ObjectId | No | Source transaction candidate |
| merchant | String | No | Merchant or payer/payee |
| amount | Decimal128 | Yes | Transaction amount |
| currency | String | Yes | ISO 4217 currency |
| transactionType | Enum | Yes | Expense, Income, Transfer |
| transactionStatus | Enum | Yes | Posted, Pending, Cancelled |
| transactionDate | Date | Yes | Date of financial event |
| paymentMethod | String | No | UPI, Credit Card, Cash, etc. |
| description | String | No | User description |
| tags | Array | No | User-defined labels |
| notes | String | No | Additional notes |
| createdAt | Date | Yes | Creation timestamp |
| updatedAt | Date | Yes | Last modification timestamp |

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | User queries |
| transactionDate | Index | Timeline and reports |
| categoryId | Index | Spending analysis |
| accountId | Index | Account statements |
| transactionType | Index | Reporting |
| transactionStatus | Index | Pending transactions |

---

# Validation Rules

- Every transaction belongs to one user.
- Amount must be greater than zero.
- Currency must use ISO 4217 codes.
- Category must exist.
- Account must exist.
- Transaction date cannot be null.
- Transfer transactions require special validation.

---

# Transfer Transactions

Transfers represent movement of money between two user-owned accounts.

Example:

Savings Account

↓

Wallet

↓

Credit Card

Transfers should not be counted as income or expense.

Future versions may introduce:

- sourceAccountId
- destinationAccountId

to better model internal transfers.

---

# Auditability

Every transaction should be traceable.

```text
Transaction

↓

Transaction Candidate

↓

Email / Document / Import
```

Manual transactions simply omit the candidate reference.

---

# Security Considerations

Transactions contain sensitive financial information.

The system should:

- Restrict access to the owning user.
- Record all modifications.
- Prevent unauthorized updates.
- Preserve transaction history.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "accountId": "ObjectId",
  "categoryId": "ObjectId",
  "candidateId": "ObjectId",
  "merchant": "Amazon",
  "amount": 2499.00,
  "currency": "INR",
  "transactionType": "EXPENSE",
  "transactionStatus": "POSTED",
  "transactionDate": "2026-07-03T18:30:00Z",
  "paymentMethod": "Credit Card",
  "description": "Laptop accessories",
  "tags": [
    "electronics",
    "office"
  ],
  "notes": "Purchased during sale",
  "createdAt": "2026-07-04T13:15:00Z",
  "updatedAt": "2026-07-04T13:15:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Recurring transactions
- Installments (EMIs)
- Split transactions
- Attachments
- Geolocation
- Exchange rate tracking
- Multi-currency accounting
- Fraud detection

# Accounts Collection

## Purpose

The `accounts` collection represents financial accounts owned by a user.

Every transaction belongs to exactly one account, allowing WealthPilot AI to organize financial activity across different sources of funds.

Examples include:

- Savings Account
- Current Account
- Credit Card
- Cash Wallet
- UPI Wallet
- Investment Account

---

# Responsibilities

The `accounts` collection is responsible for:

- Organizing financial transactions
- Tracking account balances
- Supporting account-level reporting
- Managing account status
- Providing context for AI insights

The collection does not store individual financial transactions.

---

# Relationships

```text
users
   │
   ▼
accounts
   │
   ▼
transactions
```

One user may own multiple accounts.

Each transaction belongs to exactly one account.

---

# Account Types

Supported values:

- SAVINGS
- CURRENT
- CREDIT_CARD
- CASH
- UPI_WALLET
- INVESTMENT
- LOAN

Future versions may support:

- Cryptocurrency Wallet
- Fixed Deposit
- Recurring Deposit
- Foreign Currency Account

---

# Account Status

Supported values:

- ACTIVE
- INACTIVE
- CLOSED

Closed accounts remain in the database to preserve transaction history.

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Owner of the account |
| accountName | String | Yes | User-friendly account name |
| accountType | Enum | Yes | Type of account |
| institutionName | String | No | Bank or financial institution |
| accountNumberMasked | String | No | Masked account number (e.g., XXXX1234) |
| currency | String | Yes | ISO 4217 currency code |
| openingBalance | Decimal128 | Yes | Initial balance |
| currentBalance | Decimal128 | No | Cached current balance (optional) |
| accountStatus | Enum | Yes | Current account status |
| includeInNetWorth | Boolean | Yes | Whether to include this account in net worth calculations |
| createdAt | Date | Yes | Creation timestamp |
| updatedAt | Date | Yes | Last modification timestamp |

---

# Balance Strategy

The account balance may be calculated in one of two ways.

Option 1 (Recommended)

Calculate balance dynamically from transactions.

Advantages:

- Always accurate
- No synchronization issues

Option 2

Store a cached balance for faster dashboard loading.

The cached balance must always be recalculated whenever a transaction changes.

For Version 1, WealthPilot AI should calculate balances dynamically.

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve user accounts |
| accountType | Index | Filtering |
| accountStatus | Index | Active account queries |

---

# Validation Rules

- Every account belongs to exactly one user.
- Currency must use ISO 4217 codes.
- Account name cannot be empty.
- Closed accounts cannot receive new transactions.
- Opening balance may be zero.

---

# Security Considerations

The system should:

- Store only masked account numbers.
- Never store banking credentials.
- Restrict access to the owning user.
- Preserve historical accounts for audit purposes.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "accountName": "HDFC Salary Account",
  "accountType": "SAVINGS",
  "institutionName": "HDFC Bank",
  "accountNumberMasked": "XXXX4321",
  "currency": "INR",
  "openingBalance": 5000.00,
  "currentBalance": 124350.50,
  "accountStatus": "ACTIVE",
  "includeInNetWorth": true,
  "createdAt": "2026-07-04T13:45:00Z",
  "updatedAt": "2026-07-04T13:45:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Bank logos
- Account colors and icons
- Automatic bank synchronization
- Interest rates
- Credit limits
- Account statements
- Multi-currency accounts

# Categories Collection

## Purpose

The `categories` collection defines the classification system used for financial transactions.

Categories enable meaningful financial reporting, budgeting, AI insights, and spending analysis.

Each transaction references exactly one category.

---

# Responsibilities

The `categories` collection is responsible for:

- Classifying transactions
- Organizing spending and income
- Supporting budgets
- Improving AI categorization
- Enabling analytics and reports

Categories do not store transaction data.

---

# Relationships

```text
users
   │
   ▼
categories
   │
   ├────────► transactions
   │
   └────────► budgets
```

One category may be referenced by thousands of transactions.

---

# Category Types

Supported values:

- EXPENSE
- INCOME
- TRANSFER

Examples

Expense

- Food
- Shopping
- Transportation
- Healthcare
- Entertainment
- Utilities

Income

- Salary
- Bonus
- Interest
- Rental Income
- Dividend

Transfer

- Internal Transfer

---

# System vs Custom Categories

Categories may be either:

System Categories

Built into WealthPilot AI.

Examples:

- Food
- Shopping
- Salary
- Utilities

Custom Categories

Created by the user.

Examples:

- Baby Expenses
- Home Renovation
- Side Business
- Vacation Fund

System categories cannot be deleted.

Custom categories can be edited or archived.

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | No | Null for system categories; set for user-created categories |
| name | String | Yes | Category name |
| description | String | No | Optional description |
| categoryType | Enum | Yes | EXPENSE, INCOME or TRANSFER |
| icon | String | Yes | Material icon identifier |
| color | String | Yes | Hex color code |
| isSystem | Boolean | Yes | Indicates a built-in category |
| isActive | Boolean | Yes | Active status |
| sortOrder | Number | No | Display order |
| createdAt | Date | Yes | Creation timestamp |
| updatedAt | Date | Yes | Last update timestamp |

---

# Default Categories

The application ships with a default set of categories.

Expense Categories

- Food & Dining
- Groceries
- Shopping
- Transportation
- Utilities
- Healthcare
- Education
- Entertainment
- Travel
- Insurance
- Housing
- Miscellaneous

Income Categories

- Salary
- Bonus
- Interest
- Dividend
- Rental Income
- Refund

Transfer

- Internal Transfer

Users may create additional categories.

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve user categories |
| categoryType | Index | Filtering |
| isSystem | Index | Load default categories |
| isActive | Index | Active categories |

---

# Validation Rules

- Category names must not be empty.
- Category type must be valid.
- User categories cannot duplicate an existing category name for the same user.
- System categories cannot be deleted.
- Icons should use supported Material Symbols.

---

# Security Considerations

- Users can modify only their own custom categories.
- System categories are read-only.
- Archived categories remain available for historical transactions.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": null,
  "name": "Food & Dining",
  "description": "Restaurants and food delivery",
  "categoryType": "EXPENSE",
  "icon": "restaurant",
  "color": "#FF7043",
  "isSystem": true,
  "isActive": true,
  "sortOrder": 1,
  "createdAt": "2026-07-04T14:00:00Z",
  "updatedAt": "2026-07-04T14:00:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Hierarchical categories
- AI-generated categories
- Category merge and split
- Spending limits per category
- Category-specific AI insights
- Localized category names

# Budgets Collection

## Purpose

The `budgets` collection allows users to define spending limits for specific categories over a given period.

Budgets are planning entities and do not store transactional data.

Actual spending is always calculated dynamically from the `transactions` collection.

---

# Responsibilities

The `budgets` collection is responsible for:

- Defining spending limits
- Supporting budget tracking
- Powering dashboard widgets
- Enabling AI recommendations
- Triggering budget alerts

The collection does not store spending totals.

---

# Relationships

```text
users
   │
   ▼
budgets
   │
   ▼
categories
   │
   ▼
transactions
```

One user may have many budgets.

Each budget belongs to one category.

---

# Budget Periods

Supported values:

- WEEKLY
- MONTHLY
- QUARTERLY
- YEARLY

Future versions may support:

- Custom Date Range

---

# Budget Status

Supported values:

- ACTIVE
- PAUSED
- COMPLETED
- ARCHIVED

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Budget owner |
| categoryId | ObjectId | Yes | Budget category |
| name | String | Yes | Budget name |
| budgetAmount | Decimal128 | Yes | Spending limit |
| currency | String | Yes | ISO 4217 currency |
| budgetPeriod | Enum | Yes | Weekly, Monthly, etc. |
| startDate | Date | Yes | Budget start date |
| endDate | Date | Yes | Budget end date |
| alertThreshold | Number | No | Alert percentage (e.g., 80) |
| status | Enum | Yes | Budget status |
| createdAt | Date | Yes | Creation timestamp |
| updatedAt | Date | Yes | Last modification timestamp |

---

# Budget Calculation

The system calculates budget progress using verified transactions.

Example:

Budget

₹10,000

Verified Transactions

₹7,250

Remaining Budget

₹2,750

Percentage Used

72.5%

No spending values are stored inside the budget document.

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve user budgets |
| categoryId | Index | Category lookup |
| status | Index | Active budgets |
| startDate | Index | Period queries |
| endDate | Index | Period queries |

---

# Validation Rules

- Budget amount must be greater than zero.
- Start date must be before end date.
- Category must exist.
- Currency must use ISO 4217 codes.
- Alert threshold must be between 1 and 100.

---

# Security Considerations

- Users may only manage their own budgets.
- Budget history should remain available even after completion.
- Budget calculations should always use verified transactions.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "categoryId": "ObjectId",
  "name": "Monthly Groceries",
  "budgetAmount": 10000.00,
  "currency": "INR",
  "budgetPeriod": "MONTHLY",
  "startDate": "2026-07-01T00:00:00Z",
  "endDate": "2026-07-31T23:59:59Z",
  "alertThreshold": 80,
  "status": "ACTIVE",
  "createdAt": "2026-07-01T00:00:00Z",
  "updatedAt": "2026-07-01T00:00:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Multiple categories per budget
- Rollover budgets
- Shared family budgets
- AI-generated budgets
- Predictive budget forecasting
- Budget templates
- Budget recommendations

# Financial Goals Collection

## Purpose

The `financial_goals` collection allows users to define long-term financial objectives and track their progress over time.

Goals help users save towards specific targets and provide the foundation for AI-powered planning, forecasting, and financial recommendations.

Unlike budgets, which focus on spending limits, financial goals focus on wealth accumulation.

---

# Responsibilities

The `financial_goals` collection is responsible for:

- Defining financial objectives
- Tracking savings progress
- Estimating completion timelines
- Supporting AI recommendations
- Powering goal-based dashboards

The collection stores goal definitions only.

Actual progress is calculated using verified transactions and user contributions.

---

# Relationships

```text
users
   │
   ▼
financial_goals
   │
   ├────────► transactions
   │
   └────────► accounts
```

One user may have multiple financial goals.

A goal may receive contributions from one or more transactions.

---

# Goal Types

Supported values:

- EMERGENCY_FUND
- HOUSE
- VEHICLE
- EDUCATION
- RETIREMENT
- VACATION
- INVESTMENT
- CUSTOM

---

# Goal Status

Supported values:

- ACTIVE
- COMPLETED
- PAUSED
- CANCELLED

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Goal owner |
| goalName | String | Yes | Goal title |
| goalType | Enum | Yes | Goal category |
| targetAmount | Decimal128 | Yes | Desired amount |
| currency | String | Yes | ISO 4217 currency |
| targetDate | Date | No | Target completion date |
| linkedAccountId | ObjectId | No | Savings account associated with the goal |
| status | Enum | Yes | Goal status |
| description | String | No | Additional notes |
| createdAt | Date | Yes | Creation timestamp |
| updatedAt | Date | Yes | Last modification timestamp |

---

# Goal Progress

Progress is calculated dynamically.

Example:

Target Amount

₹500,000

Current Contributions

₹185,000

Completion

37%

Remaining

₹315,000

No progress values are permanently stored.

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve user goals |
| goalType | Index | Filter by goal type |
| status | Index | Active goals |
| targetDate | Index | Upcoming goals |

---

# Validation Rules

- Target amount must be greater than zero.
- Goal name cannot be empty.
- Currency must use ISO 4217 codes.
- Linked account must exist if provided.
- Completed goals cannot be modified.

---

# Security Considerations

- Users may only manage their own goals.
- Goal history should remain available after completion.
- Goal calculations must use verified financial data.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "goalName": "Emergency Fund",
  "goalType": "EMERGENCY_FUND",
  "targetAmount": 600000.00,
  "currency": "INR",
  "targetDate": "2028-12-31T00:00:00Z",
  "linkedAccountId": "ObjectId",
  "status": "ACTIVE",
  "description": "Maintain 12 months of expenses.",
  "createdAt": "2026-07-04T15:00:00Z",
  "updatedAt": "2026-07-04T15:00:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Automatic contributions
- Goal milestones
- Shared family goals
- Goal prioritization
- AI-generated savings plans
- Goal forecasting
- Investment-linked goals
- Goal reminders

# Assets Collection

## Purpose

The `assets` collection stores valuable items owned by the user that contribute to their overall net worth.

Assets represent resources with financial value and are tracked independently from financial transactions.

Examples include:

- Real Estate
- Vehicles
- Investments
- Fixed Deposits
- Gold
- Cryptocurrency
- Cash Holdings
- Business Ownership

---

# Responsibilities

The `assets` collection is responsible for:

- Tracking owned assets
- Estimating net worth
- Supporting wealth analytics
- Powering AI financial insights
- Monitoring asset appreciation or depreciation

The collection stores asset metadata only.

Historical valuation changes may be stored separately in future versions.

---

# Relationships

```text
users
   │
   ▼
assets
```

Assets are independent financial entities.

Transactions may contribute to purchasing assets, but ownership is maintained separately.

---

# Asset Types

Supported values:

- REAL_ESTATE
- VEHICLE
- INVESTMENT
- GOLD
- SILVER
- CASH
- FIXED_DEPOSIT
- CRYPTOCURRENCY
- BUSINESS
- OTHER

---

# Asset Status

Supported values:

- ACTIVE
- SOLD
- DISPOSED

Sold assets remain in the database to preserve historical net worth calculations.

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Owner of the asset |
| assetName | String | Yes | Display name |
| assetType | Enum | Yes | Asset classification |
| purchaseValue | Decimal128 | Yes | Original purchase price |
| currentValue | Decimal128 | Yes | Current estimated value |
| currency | String | Yes | ISO 4217 currency |
| purchaseDate | Date | No | Purchase date |
| status | Enum | Yes | Asset status |
| description | String | No | Additional notes |
| createdAt | Date | Yes | Creation timestamp |
| updatedAt | Date | Yes | Last modification timestamp |

---

# Valuation

Assets have two important values:

Purchase Value

Amount originally paid.

Current Value

Estimated market value.

Example:

Purchase Price

₹75,00,000

Current Value

₹92,00,000

Appreciation

₹17,00,000

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve user assets |
| assetType | Index | Asset filtering |
| status | Index | Active assets |

---

# Validation Rules

- Purchase value must be greater than zero.
- Current value cannot be negative.
- Currency must use ISO 4217 codes.
- Asset name cannot be empty.

---

# Security Considerations

- Users may only manage their own assets.
- Historical asset records should never be deleted.
- Valuation updates should be logged.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "assetName": "Runwal Gardens Apartment",
  "assetType": "REAL_ESTATE",
  "purchaseValue": 7500000.00,
  "currentValue": 9200000.00,
  "currency": "INR",
  "purchaseDate": "2021-08-15T00:00:00Z",
  "status": "ACTIVE",
  "description": "Residential apartment",
  "createdAt": "2026-07-04T15:30:00Z",
  "updatedAt": "2026-07-04T15:30:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Asset valuation history
- Automatic market price updates
- Property details
- Stock portfolio integration
- Gold price synchronization
- Asset performance charts
- Depreciation calculations

# Assets Collection

## Purpose

The `assets` collection stores valuable items owned by the user that contribute to their overall net worth.

Assets represent resources with financial value and are tracked independently from financial transactions.

Examples include:

- Real Estate
- Vehicles
- Investments
- Fixed Deposits
- Gold
- Cryptocurrency
- Cash Holdings
- Business Ownership

---

# Responsibilities

The `assets` collection is responsible for:

- Tracking owned assets
- Estimating net worth
- Supporting wealth analytics
- Powering AI financial insights
- Monitoring asset appreciation or depreciation

The collection stores asset metadata only.

Historical valuation changes may be stored separately in future versions.

---

# Relationships

```text
users
   │
   ▼
assets
```

Assets are independent financial entities.

Transactions may contribute to purchasing assets, but ownership is maintained separately.

---

# Asset Types

Supported values:

- REAL_ESTATE
- VEHICLE
- INVESTMENT
- GOLD
- SILVER
- CASH
- FIXED_DEPOSIT
- CRYPTOCURRENCY
- BUSINESS
- OTHER

---

# Asset Status

Supported values:

- ACTIVE
- SOLD
- DISPOSED

Sold assets remain in the database to preserve historical net worth calculations.

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Owner of the asset |
| assetName | String | Yes | Display name |
| assetType | Enum | Yes | Asset classification |
| purchaseValue | Decimal128 | Yes | Original purchase price |
| currentValue | Decimal128 | Yes | Current estimated value |
| currency | String | Yes | ISO 4217 currency |
| purchaseDate | Date | No | Purchase date |
| status | Enum | Yes | Asset status |
| description | String | No | Additional notes |
| createdAt | Date | Yes | Creation timestamp |
| updatedAt | Date | Yes | Last modification timestamp |

---

# Valuation

Assets have two important values:

Purchase Value

Amount originally paid.

Current Value

Estimated market value.

Example:

Purchase Price

₹75,00,000

Current Value

₹92,00,000

Appreciation

₹17,00,000

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve user assets |
| assetType | Index | Asset filtering |
| status | Index | Active assets |

---

# Validation Rules

- Purchase value must be greater than zero.
- Current value cannot be negative.
- Currency must use ISO 4217 codes.
- Asset name cannot be empty.

---

# Security Considerations

- Users may only manage their own assets.
- Historical asset records should never be deleted.
- Valuation updates should be logged.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "assetName": "Runwal Gardens Apartment",
  "assetType": "REAL_ESTATE",
  "purchaseValue": 7500000.00,
  "currentValue": 9200000.00,
  "currency": "INR",
  "purchaseDate": "2021-08-15T00:00:00Z",
  "status": "ACTIVE",
  "description": "Residential apartment",
  "createdAt": "2026-07-04T15:30:00Z",
  "updatedAt": "2026-07-04T15:30:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Asset valuation history
- Automatic market price updates
- Property details
- Stock portfolio integration
- Gold price synchronization
- Asset performance charts
- Depreciation calculations