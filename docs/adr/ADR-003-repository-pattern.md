# ADR-003: Repository Pattern

## Status

Accepted

## Date

2026-07-10

---

## Context

The application uses MongoDB as its primary database. Direct database access throughout the codebase would tightly couple business logic to persistence and make future changes difficult.

---

## Decision

All database access will be performed through repository classes.

Each aggregate owns a dedicated repository.

Examples include:

* UserRepository
* AccountRepository
* TransactionRepository
* CategoryRepository

Repositories inherit common functionality from a shared BaseRepository where appropriate.

---

## Responsibilities

Repositories are responsible for:

* CRUD operations
* Query execution
* Converting MongoDB documents into domain models

Repositories must not implement business rules.

Business rules belong in the service layer.

---

## Repository Structure

```text
Service
      │
      ▼
Repository
      │
      ▼
MongoDB
```

Services interact only with repositories and never directly with MongoDB.

---

## Base Repository

The BaseRepository provides reusable functionality shared across repositories, such as:

* Access to MongoDB collections
* Common create operations
* Shared utility methods

Individual repositories implement domain-specific queries.

---

## Consequences

### Advantages

* Encapsulates persistence logic
* Improves maintainability
* Simplifies testing
* Encourages reusable database code
* Keeps services focused on business logic

### Trade-offs

* Introduces additional abstraction
* Requires more classes than direct database access

These trade-offs are acceptable because they produce a cleaner and more scalable architecture.
