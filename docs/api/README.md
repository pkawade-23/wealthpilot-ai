# WealthPilot AI API

## Purpose

This directory defines the REST API contract for WealthPilot AI.

The API follows RESTful design principles and serves as the communication layer between the Angular frontend and the FastAPI backend.

The documentation acts as the single source of truth for request and response contracts.

---

# Design Principles

The API is designed around the following principles.

## Resource-Oriented

Endpoints represent business resources rather than actions.

Example:

```
GET /transactions
POST /transactions
GET /accounts
```

instead of

```
/getTransactions
/createTransaction
```

---

## Stateless

Each request contains all information required to process it.

The backend does not rely on server-side session state.

Authentication is handled using JWT access tokens.

---

## Versioned

All endpoints are versioned.

```
/api/v1/...
```

Future breaking changes will introduce:

```
/api/v2/...
```

without impacting existing clients.

---

## Consistent Responses

Every endpoint returns a consistent response structure.

Success:

```json
{
  "success": true,
  "data": {},
  "message": "Operation completed successfully."
}
```

Error:

```json
{
  "success": false,
  "error": {
    "code": "TRANSACTION_NOT_FOUND",
    "message": "Transaction not found."
  }
}
```

---

## Secure by Default

All endpoints require authentication unless explicitly marked as public.

Authorization is enforced at the resource level.

Users can only access their own financial data.

---

## OpenAPI First

The FastAPI implementation will generate OpenAPI documentation directly from the endpoint definitions.

This documentation serves as both developer reference and client contract.

---

# API Categories

| Document | Purpose |
|----------|---------|
| Authentication | Login, registration, JWT |
| Users | User profile and preferences |
| Dashboard | Financial overview |
| Accounts | Bank accounts, wallets, cards |
| Transactions | Financial transactions |
| Ingestion | Email and document ingestion |
| Review Center | AI extraction review |
| AI | Conversations, insights, recommendations |
| Scenarios | Financial simulations |
| Reports | Analytics and exports |
| Notifications | User notifications |
| Errors | Standard error definitions |

---

# Naming Conventions

## URLs

Use plural nouns.

```
/transactions
/accounts
/goals
```

---

## HTTP Methods

GET

Retrieve data.

POST

Create resources.

PUT

Replace resources.

PATCH

Partial updates.

DELETE

Soft delete resources.

---

## Status Codes

| Code | Meaning |
|-------|----------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Validation Error |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 409 | Conflict |
| 422 | Business Rule Violation |
| 500 | Internal Server Error |

---

# Authentication

Authentication uses JWT.

Every authenticated request includes:

```
Authorization: Bearer <access_token>
```

---

# Pagination

Collection endpoints support pagination.

Example:

```
GET /transactions?page=1&pageSize=20
```

Standard response:

```json
{
  "items": [],
  "page": 1,
  "pageSize": 20,
  "totalItems": 245,
  "totalPages": 13
}
```

---

# Filtering

Resources may be filtered using query parameters.

Example:

```
GET /transactions?category=Groceries&from=2026-06-01&to=2026-06-30
```

---

# Sorting

Example:

```
GET /transactions?sort=date&order=desc
```

---

# Idempotency

PUT, PATCH and DELETE operations should be idempotent.

Creating resources with POST may optionally support an Idempotency-Key header for future integrations.

---

# Future Enhancements

Future versions may introduce:

- GraphQL
- WebSocket support
- Server-Sent Events
- Bulk operations
- API rate limiting
- API keys for third-party integrations