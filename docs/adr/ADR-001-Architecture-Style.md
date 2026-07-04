# ADR-001: Adopt a Modular Monolith with Clean Architecture

**Project:** WealthPilot AI  
**ADR ID:** ADR-001  
**Status:** Accepted  
**Date:** 2026-07-02  
**Decision Makers:** Project Team

---

# Context

WealthPilot AI is an AI-powered personal finance platform that combines multiple business domains, including:

- User Authentication
- Financial Management
- Email Processing
- Document Processing
- AI Chat Assistant
- Retrieval-Augmented Generation (RAG)
- Financial Scenario Simulation

As the application grows, these domains will evolve independently and require clear separation of responsibilities.

Two common architectural approaches were considered:

- Traditional Layered Monolith
- Microservices

A traditional layered monolith is simple initially but often becomes tightly coupled as the application grows. Conversely, adopting microservices from the beginning introduces unnecessary operational complexity for a single-developer project, including distributed deployments, service communication, and infrastructure management.

The project requires an architecture that:

- Is easy to develop and maintain.
- Encourages separation of concerns.
- Supports comprehensive testing.
- Allows future scalability.
- Demonstrates enterprise-grade software engineering practices.

---

# Decision

The backend will adopt a **Modular Monolith** architecture based on **Clean Architecture** principles.

The application will be deployed as a single FastAPI service while being internally organized into independent feature modules.

Each feature module will encapsulate its own business logic and follow the same architectural layers:

```text
Presentation
    ↓
Application
    ↓
Domain
    ↓
Infrastructure
```

Each module will expose only well-defined public interfaces and should not depend directly on the internal implementation of other modules.

Example project structure:

```text
backend/
└── app/
    ├── auth/
    ├── finance/
    ├── documents/
    ├── email/
    ├── ai/
    ├── simulation/
    └── shared/
```

Example module structure:

```text
finance/
├── presentation/
├── application/
├── domain/
└── infrastructure/
```

---

# Rationale

This architecture provides several advantages for the project.

### Maintainability

Business functionality is grouped by domain, making the codebase easier to understand and evolve.

### Separation of Concerns

Each architectural layer has a single responsibility:

- **Presentation** handles HTTP requests and responses.
- **Application** implements business use cases.
- **Domain** contains core business rules.
- **Infrastructure** integrates external systems such as MongoDB, Ollama, and ChromaDB.

### Testability

Business logic can be tested independently of web frameworks, databases, and AI services.

### Scalability

The modular structure allows future extraction of individual modules into microservices if scaling requirements change.

### Portfolio Quality

This architecture demonstrates modern software engineering practices commonly used in production systems while avoiding unnecessary operational complexity.

---

# Alternatives Considered

## Option 1 — Traditional Layered Monolith

Example:

```text
controllers/
services/
repositories/
models/
```

### Advantages

- Easy to start.
- Minimal boilerplate.
- Familiar architecture.

### Disadvantages

- Weak feature boundaries.
- Business logic becomes tightly coupled.
- Difficult to maintain as the project grows.
- Harder to isolate features for testing.

**Decision:** Rejected

---

## Option 2 — Microservices

Example:

```text
Authentication Service
Finance Service
AI Service
Email Service
Document Service
```

### Advantages

- Independent deployment.
- Independent scaling.
- Strong service isolation.

### Disadvantages

- Increased infrastructure complexity.
- Multiple deployments.
- Service communication overhead.
- Distributed logging and debugging.
- Higher operational costs.
- Unnecessary complexity for the current project scope.

**Decision:** Rejected

---

# Consequences

## Positive

- Clear feature boundaries.
- High maintainability.
- Improved testability.
- Easier onboarding for contributors.
- Better separation of business logic from infrastructure.
- Simplified deployment.
- Future-ready architecture.

## Negative

- More initial project structure.
- Slightly higher learning curve.
- Requires discipline to maintain module boundaries.

---

# Architectural Principles

The following principles apply to all modules:

- Modular Monolith
- Clean Architecture
- Feature-First Organization
- SOLID Principles
- Dependency Inversion Principle (DIP)
- Separation of Concerns
- API-First Design
- Asynchronous Processing where appropriate
- Configuration via Environment Variables
- Explicit Dependency Injection

---

# Impact

This decision establishes the architectural foundation for WealthPilot AI.

All future backend modules should follow the modular structure and Clean Architecture layering described in this ADR unless superseded by a future Architecture Decision Record.

---

# References

- Robert C. Martin — *Clean Architecture*
- Eric Evans — *Domain-Driven Design*
- Michael Nygard — *Documenting Architecture Decisions*
- Harry Percival & Bob Gregory — *Architecture Patterns with Python*