# ADR-001: Clean Architecture

## Status

Accepted

## Date

2026-07-10

---

## Context

WealthPilot AI is intended to be a production-quality financial platform rather than a simple CRUD application. The application is expected to grow to include authentication, financial accounts, transactions, dashboards, AI-powered document ingestion, retrieval-augmented generation (RAG), and financial insights.

As the application grows, separating business logic from infrastructure and HTTP concerns becomes essential to maintain readability, testability, and scalability.

---

## Decision

The backend will follow a layered architecture with clearly defined responsibilities.

```text
Client
    │
    ▼
FastAPI Router
    │
    ▼
Service Layer
    │
    ▼
Repository Layer
    │
    ▼
MongoDB
```

### Router

Responsible for:

* HTTP request handling
* Authentication dependencies
* Request validation
* Returning API responses

Routers must not contain business logic or database operations.

---

### Service Layer

Responsible for:

* Business rules
* Validation beyond schema validation
* Authorization decisions
* Coordinating repositories
* Preparing response models

Services should remain independent of HTTP concerns.

---

### Repository Layer

Responsible for:

* Reading and writing data
* MongoDB queries
* Mapping database documents to domain models

Repositories must not contain business logic.

---

### Models

Models represent the application's internal domain objects.

---

### Schemas

Schemas define the API contracts for requests and responses.

Internal models should never be exposed directly through the API.

---

## Dependency Direction

Dependencies always flow downward.

```text
Router
    ↓
Service
    ↓
Repository
    ↓
Database
```

Lower layers must never depend on higher layers.

This prevents circular imports and improves maintainability.

---

## Consequences

### Advantages

* Clear separation of concerns
* Easier testing
* Improved maintainability
* Consistent module structure
* Better scalability

### Trade-offs

* More files and classes
* Slightly more boilerplate for small features

These trade-offs are acceptable because they support long-term project growth.
