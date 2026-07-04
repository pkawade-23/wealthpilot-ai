# API Conventions

## Purpose

This document defines the API design conventions for WealthPilot AI.

All REST endpoints must follow these standards to ensure consistency, maintainability, and a predictable developer experience.

This document applies to every API endpoint in the system.

---

# Base URL

All API endpoints are versioned.

```
/api/v1
```

Examples:

```
GET /api/v1/transactions
GET /api/v1/accounts
POST /api/v1/auth/login
```

Future breaking changes will introduce a new API version.

Example:

```
/api/v2/...
```

---

# URL Naming

## Rules

Use:

- lowercase
- plural nouns
- hyphens when needed

Good

```
/transactions
/accounts
/financial-goals
```

Avoid

```
/GetTransactions
/getTransactions
/accountList
```

Resources represent business entities, not actions.

---

# HTTP Methods

| Method | Purpose |
|---------|----------|
| GET | Retrieve resources |
| POST | Create resources |
| PUT | Replace an entire resource |
| PATCH | Update part of a resource |
| DELETE | Soft delete a resource |

Examples

```
GET /transactions
GET /transactions/{id}

POST /transactions

PATCH /transactions/{id}

DELETE /transactions/{id}
```

---

# JSON Naming

All JSON fields use camelCase.

Example

```json
{
    "transactionId": "...",
    "accountId": "...",
    "createdAt": "...",
    "monthlyIncome": 120000
}
```

Avoid

```json
{
    "transaction_id": "...",
    "monthly_income": 120000
}
```

---

# Date Format

All dates use ISO 8601 UTC.

Example

```
2026-07-05T18:30:15Z
```

Dates should never be returned in localized formats.

Avoid

```
05/07/2026
```

---

# Currency

Currency values use ISO 4217 currency codes.

Example

```json
{
    "amount": 2500.50,
    "currency": "INR"
}
```

Amounts are stored as decimal values.

Currency formatting belongs to the frontend.

---

# Object Identifiers

MongoDB ObjectIds are represented as strings.

Example

```json
{
    "id": "6868b3f80b17f4450e0c1234"
}
```

Internal ObjectId types are never exposed.

---

# Pagination

Collection endpoints support pagination.

Query Parameters

```
?page=1&pageSize=20
```

Response

```json
{
    "items": [],
    "page": 1,
    "pageSize": 20,
    "totalItems": 215,
    "totalPages": 11
}
```

---

# Filtering

Filtering uses query parameters.

Example

```
GET /transactions?category=Groceries

GET /transactions?status=APPROVED

GET /transactions?from=2026-06-01&to=2026-06-30
```

Multiple filters may be combined.

---

# Sorting

Sorting uses query parameters.

```
?sort=date
```

Descending

```
?sort=date&order=desc
```

Ascending

```
?sort=amount&order=asc
```

---

# Searching

Free-text search uses the `search` parameter.

Example

```
GET /transactions?search=amazon
```

---

# Success Response

Every successful request returns a consistent envelope.

```json
{
    "success": true,
    "data": {},
    "message": "Operation completed successfully."
}
```

---

# Error Response

Errors use a consistent structure.

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

# Validation Errors

Validation errors include field-level details.

Example

```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Request validation failed.",
        "details": [
            {
                "field": "amount",
                "message": "Amount must be greater than zero."
            }
        ]
    }
}
```

---

# HTTP Status Codes

| Status | Meaning |
|---------|----------|
| 200 | Success |
| 201 | Resource created |
| 204 | No content |
| 400 | Invalid request |
| 401 | Authentication required |
| 403 | Access denied |
| 404 | Resource not found |
| 409 | Conflict |
| 422 | Business validation failed |
| 429 | Too many requests |
| 500 | Internal server error |

---

# Authentication

Protected endpoints require JWT authentication.

Header

```
Authorization: Bearer <access_token>
```

Public endpoints explicitly state that authentication is not required.

---

# Idempotency

The following operations are idempotent:

- GET
- PUT
- PATCH
- DELETE

POST endpoints may optionally support the `Idempotency-Key` header for future integrations.

---

# Soft Delete

Resources are never physically deleted unless explicitly required.

Deleted resources are marked with a status or deletion timestamp.

Example

```json
{
    "deletedAt": "2026-07-05T10:15:00Z"
}
```

---

# Correlation ID

Every request should include a correlation identifier.

Header

```
X-Correlation-ID
```

If omitted, the backend generates one.

This identifier is included in application logs to simplify debugging and request tracing across services.

---

# Request ID

Every API response includes a request identifier.

Example

```json
{
    "requestId": "bca2d67d-f634-4c7f-bdb3-74b4c1b0d5b7"
}
```

The request ID is useful when reporting issues or investigating logs.

---

# API Versioning

Major breaking changes require a new API version.

Example

```
/api/v1
/api/v2
```

Minor, backward-compatible enhancements should not require a version change.

---

# Rate Limiting

Version 1 does not implement rate limiting.

Future versions may introduce endpoint-specific rate limits.

---

# File Uploads

File uploads use `multipart/form-data`.

Supported upload types include:

- PDF
- CSV
- JPEG
- PNG

Maximum file size limits are enforced by the backend and documented per endpoint.

---

# Time Zone

All timestamps are stored and returned in UTC.

Time zone conversion is handled by the frontend based on the user's preferences.

---

# API Documentation

Every endpoint must include:

- Purpose
- Authentication requirements
- Request parameters
- Request body
- Response examples
- Error responses
- Business rules

FastAPI automatically generates OpenAPI documentation from the implementation.

This document defines the standards that every endpoint must follow.