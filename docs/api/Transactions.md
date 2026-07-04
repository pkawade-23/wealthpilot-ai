# Transactions API

## Purpose

The Transactions API manages all verified financial transactions within WealthPilot AI.

Transactions represent the single source of truth for all financial calculations, reports, analytics, dashboards, budgets, and AI insights.

Every financial event ultimately becomes a verified transaction.

---

# Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | /api/v1/transactions | List transactions |
| GET | /api/v1/transactions/{id} | Get transaction details |
| POST | /api/v1/transactions | Create transaction |
| PATCH | /api/v1/transactions/{id} | Update transaction |
| DELETE | /api/v1/transactions/{id} | Archive transaction |
| POST | /api/v1/transactions/bulk | Bulk create/update |
| POST | /api/v1/transactions/transfer | Create transfer |
| GET | /api/v1/transactions/summary | Financial summary |

Authentication is required for every endpoint.

---

# Get Transactions

## Endpoint

```
GET /api/v1/transactions
```

## Description

Returns verified transactions belonging to the authenticated user.

---

## Query Parameters

| Parameter | Description |
|------------|-------------|
| page | Page number |
| pageSize | Items per page |
| search | Free-text search |
| accountId | Filter by account |
| categoryId | Filter by category |
| type | INCOME / EXPENSE / TRANSFER |
| status | VERIFIED / ARCHIVED |
| from | Start date |
| to | End date |
| minAmount | Minimum amount |
| maxAmount | Maximum amount |
| sort | Sort field |
| order | asc / desc |

Example

```
GET /api/v1/transactions?page=1&pageSize=20&categoryId=abc123&from=2026-06-01&to=2026-06-30&sort=date&order=desc
```

---

# Success Response

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "...",
        "date": "2026-07-05",
        "description": "Amazon Purchase",
        "amount": 1499,
        "currency": "INR",
        "type": "EXPENSE",
        "category": "Shopping",
        "account": "HDFC Salary Account",
        "merchant": "Amazon",
        "status": "VERIFIED"
      }
    ],
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "totalItems": 245,
      "totalPages": 13,
      "hasNext": true,
      "hasPrevious": false
    }
  }
}
```

---

# Get Transaction

## Endpoint

```
GET /api/v1/transactions/{id}
```

Returns the complete transaction including audit information and attachments.

---

# Create Transaction

## Endpoint

```
POST /api/v1/transactions
```

## Request

```json
{
  "date": "2026-07-05",
  "description": "Fuel",
  "amount": 3500,
  "currency": "INR",
  "type": "EXPENSE",
  "accountId": "...",
  "categoryId": "...",
  "merchant": "Indian Oil",
  "notes": "Business travel"
}
```

---

## Validation Rules

- Amount must be greater than zero.
- Account must exist.
- Category must exist.
- Date cannot be in an invalid format.
- Currency must be supported.

---

# Update Transaction

## Endpoint

```
PATCH /api/v1/transactions/{id}
```

Allows partial updates.

Editable fields include:

- Description
- Category
- Notes
- Merchant
- Date
- Amount

---

# Archive Transaction

## Endpoint

```
DELETE /api/v1/transactions/{id}
```

Transactions are archived instead of permanently deleted.

Historical reports remain accurate.

---

# Bulk Operations

## Endpoint

```
POST /api/v1/transactions/bulk
```

Supports:

- Bulk creation
- Bulk category updates
- Bulk archive
- Bulk tag assignment

Maximum:

500 transactions per request.

---

# Transfer

## Endpoint

```
POST /api/v1/transactions/transfer
```

Transfers move money between two accounts.

Example

```json
{
  "fromAccountId": "...",
  "toAccountId": "...",
  "amount": 25000,
  "date": "2026-07-05",
  "description": "Salary transfer"
}
```

The backend automatically creates:

- One debit transaction
- One credit transaction

linked by a common transfer identifier.

---

# Transaction Summary

## Endpoint

```
GET /api/v1/transactions/summary
```

Returns:

- Income
- Expenses
- Savings
- Transaction count
- Average transaction
- Largest expense
- Largest income

Supports the same filtering parameters as the transaction list.

---

# Transaction Types

Supported values

- INCOME
- EXPENSE
- TRANSFER

---

# Transaction Status

Supported values

- VERIFIED
- ARCHIVED

---

# Validation Rules

- Every transaction belongs to one account.
- Every transaction belongs to one user.
- Transfers require two different accounts.
- Archived transactions cannot be modified.
- Only verified transactions appear in reports.

---

# Business Rules

- Transactions are immutable from an audit perspective.
- Updates create audit history.
- Transactions imported from AI remain linked to their original source.
- Dashboard calculations use verified transactions only.
- Transfers never affect income or expense totals.

---

# Performance Requirements

The API should support:

- Millions of transactions
- Efficient pagination
- Indexed filtering
- Full-text search
- Parallel aggregation queries

---

# Security Considerations

- Users can only access their own transactions.
- Bulk operations validate ownership.
- Audit logs record all modifications.

---

# Future Enhancements

Future versions may support:

- Recurring transactions
- Transaction splitting
- Attachments
- OCR receipt scanning
- Duplicate detection
- Geolocation
- Merchant normalization
- AI-assisted categorization