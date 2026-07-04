# Accounts API

## Purpose

The Accounts API manages the user's financial accounts.

Accounts represent financial sources or destinations used to record transactions and calculate financial summaries.

Examples include:

- Bank accounts
- Credit cards
- Cash wallets
- Digital wallets
- Investment accounts
- Loan accounts

Accounts serve as the foundation for financial tracking throughout WealthPilot AI.

---

# Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | /api/v1/accounts | Retrieve accounts |
| GET | /api/v1/accounts/{id} | Retrieve account details |
| POST | /api/v1/accounts | Create account |
| PATCH | /api/v1/accounts/{id} | Update account |
| DELETE | /api/v1/accounts/{id} | Archive account |

Authentication is required for all endpoints.

---

# Get Accounts

## Endpoint

```
GET /api/v1/accounts
```

## Description

Returns all active accounts belonging to the authenticated user.

## Query Parameters

| Parameter | Description |
|------------|-------------|
| type | Filter by account type |
| status | ACTIVE / ARCHIVED |
| includeBalance | true/false |

Example

```
GET /api/v1/accounts?type=BANK
```

---

## Success Response

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "6868b3f80b17f4450e0c1234",
        "name": "HDFC Salary Account",
        "type": "BANK",
        "balance": 125450.25,
        "currency": "INR",
        "status": "ACTIVE"
      }
    ]
  }
}
```

---

# Get Account Details

## Endpoint

```
GET /api/v1/accounts/{id}
```

## Description

Returns detailed information about a single account.

## Success Response

```json
{
  "success": true,
  "data": {
    "id": "...",
    "name": "HDFC Salary Account",
    "institution": "HDFC Bank",
    "type": "BANK",
    "currency": "INR",
    "openingBalance": 100000,
    "currentBalance": 125450.25,
    "status": "ACTIVE",
    "createdAt": "2026-07-05T10:00:00Z"
  }
}
```

---

# Create Account

## Endpoint

```
POST /api/v1/accounts
```

## Request

```json
{
  "name": "ICICI Savings",
  "institution": "ICICI Bank",
  "type": "BANK",
  "currency": "INR",
  "openingBalance": 50000
}
```

## Business Rules

- Account name is required.
- Currency must be supported.
- Opening balance cannot be negative.
- Duplicate account names are allowed.

## Success Response

HTTP 201

```json
{
  "success": true,
  "message": "Account created successfully."
}
```

---

# Update Account

## Endpoint

```
PATCH /api/v1/accounts/{id}
```

## Description

Updates editable account information.

Editable fields:

- Name
- Institution
- Currency
- Status

Opening balance cannot be modified after account creation.

---

# Archive Account

## Endpoint

```
DELETE /api/v1/accounts/{id}
```

## Description

Archives the account.

Archived accounts:

- Remain in reports.
- Cannot receive new transactions.
- Continue to preserve transaction history.

Accounts are never permanently deleted.

---

# Account Types

Supported values:

- BANK
- CREDIT_CARD
- CASH
- DIGITAL_WALLET
- INVESTMENT
- LOAN
- EPF
- PPF
- NPS
- OTHER

---

# Account Status

Supported values:

- ACTIVE
- ARCHIVED

---

# Validation Rules

- Every account belongs to one user.
- Opening balance cannot be negative.
- Currency must be supported.
- Archived accounts cannot accept new transactions.

---

# Business Rules

- Transactions reference accounts.
- Dashboard balances are calculated using active accounts.
- Archived accounts remain available for historical reporting.
- Account deletion is always a soft delete.

---

# Error Responses

Possible errors:

- Account not found
- Validation error
- Unauthorized
- Account already archived

---

# Security Considerations

- Users may only access their own accounts.
- All account modifications are audited.
- Archived accounts remain immutable except for administrative recovery.

---

# Future Enhancements

Future versions may support:

- Automatic bank synchronization
- Multiple currencies per account
- Interest rate tracking
- Joint accounts
- Recurring balance reconciliation
- Account groups
- Bank logos
- Account color customization