# ADR-005: Cursor-Based Pagination

- **Status:** Accepted
- **Date:** 2026-07-12

---

# Context

Many resources in WealthPilot, such as Transactions, Accounts, Categories, Documents, and AI-generated records, are expected to grow significantly over time.

Traditional offset pagination (`skip` + `limit`) is simple to implement but becomes increasingly inefficient as the collection size grows. MongoDB must traverse skipped documents before returning the requested page, causing query performance to degrade as the offset increases.

Since WealthPilot is designed as a long-term personal finance platform, pagination must scale efficiently regardless of collection size.

---

# Decision

The application will use **cursor-based pagination** for all collection endpoints.

Pagination is implemented using MongoDB's `_id` field as the cursor.

Each request returns:

- A page of results
- A cursor representing the last document in the current page
- A flag indicating whether another page exists

Clients request the next page by providing the cursor received from the previous response.

Example:

```
GET /transactions?limit=25

↓

{
    "items": [...],
    "next_cursor": "eyJsYXN0X2lkIjoiNjY4..."
}
```

Next request:

```
GET /transactions?limit=25&cursor=eyJsYXN0X2lkIjoiNjY4...
```

---

# Sorting

Cursor pagination is tightly coupled with sorting.

All paginated endpoints must define a deterministic ordering before applying the cursor.

The default ordering throughout WealthPilot is:

```
created_at DESC
_id DESC
```

When sorting by another field, `_id` is always used as the secondary sort key to guarantee deterministic pagination.

This prevents duplicate or missing records between pages.

---

# Cursor Format

The cursor is an opaque Base64-encoded JSON payload.

Example:

```json
{
    "last_id": "668cb4b8e4..."
}
```

Clients must never interpret or modify cursor contents.

Invalid cursors result in a `400 Bad Request`.

---

# Implementation

Pagination is implemented as reusable shared infrastructure.

Key components:

- `QueryParams`
- `CursorPage`
- `paginate()`
- `build_sort()`
- Cursor encoder/decoder

Repositories delegate pagination to the shared paginator rather than implementing pagination individually.

The shared paginator validates:

- Maximum page size
- Cursor format
- Cursor decoding
- Sort direction
- Supported sort fields

Invalid input results in standardized application exceptions.

---

# Consequences

## Advantages

- Excellent performance on very large collections.
- No expensive MongoDB `skip`.
- Consistent paging performance.
- Reusable across all repositories.
- Generic implementation with minimal duplication.
- AI-generated and imported datasets remain performant.

## Trade-offs

- Clients cannot request arbitrary page numbers.
- Cursor values are opaque.
- Pagination logic is more complex than offset-based pagination.

---

# Alternatives Considered

## Offset Pagination

Example:

```
GET /transactions?page=8&page_size=25
```

Rejected because:

- MongoDB must scan skipped documents.
- Performance degrades as data grows.
- Unsuitable for large financial datasets.

---

## In-memory Pagination

Rejected because it requires loading excessive data into application memory and does not scale.

---

# Rationale

WealthPilot is intended to manage years of financial history.

Choosing cursor-based pagination early ensures the application remains performant without requiring future API redesigns.

This decision aligns with the project's goals of scalability, maintainability, and production-quality architecture.

---

# Related ADRs

- ADR-001 Clean Architecture
- ADR-003 Repository Pattern