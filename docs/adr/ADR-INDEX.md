# Architecture Decision Records (ADR)

**Project:** WealthPilot AI  
**Version:** 1.0  
**Status:** Active  
**Last Updated:** 2026-07-02  
**Owner:** Pratik Kawade

---

# Purpose

This directory contains the **Architecture Decision Records (ADRs)** for WealthPilot AI.

An Architecture Decision Record (ADR) captures a significant architectural or technical decision made during the lifecycle of the project. Each ADR documents the problem being addressed, the available options, the selected solution, and the reasoning behind that decision.

Maintaining ADRs provides a historical record of architectural choices, promotes transparency, and helps future contributors understand *why* decisions were made—not just *what* was implemented.

---

# ADR Lifecycle

Each ADR progresses through one of the following states:

| Status | Description |
|----------|-------------|
| **Proposed** | Decision is under discussion. |
| **Accepted** | Decision has been approved and adopted. |
| **Superseded** | Decision has been replaced by a newer ADR. |
| **Deprecated** | Decision is no longer recommended but retained for historical reference. |

---

# ADR Index

| ADR | Title | Status |
|-----|-------|--------|
| ADR-001 | Adopt a Modular Monolith with Clean Architecture | ✅ Accepted |
| ADR-002 | Use FastAPI as the Backend Framework | 📋 Planned |
| ADR-003 | Use MongoDB as the Primary Database | 📋 Planned |
| ADR-004 | Use Angular as the Frontend Framework | 📋 Planned |
| ADR-005 | Use Ollama for Local LLM Inference | 📋 Planned |
| ADR-006 | Use LangChain for AI Orchestration | 📋 Planned |
| ADR-007 | Use ChromaDB for Vector Storage | 📋 Planned |
| ADR-008 | Use JWT Authentication with Refresh Tokens | 📋 Planned |
| ADR-009 | Use Docker Compose for Local Development | 📋 Planned |
| ADR-010 | Use GitHub Actions for Continuous Integration | 📋 Planned |
| ADR-011 | Adopt OpenAPI-First API Design | 📋 Planned |
| ADR-012 | Background Job Processing Strategy | 📋 Planned |

---

# ADR Template

Each ADR should follow the structure below to ensure consistency across the project.

```text
Title
Status
Date
Context
Decision
Rationale
Alternatives Considered
Consequences
References (Optional)
```

---

# Guidelines

- Every significant architectural or technical decision should have an ADR.
- ADRs should be created before or during implementation.
- Existing ADRs should not be modified to change historical decisions.
- If a decision changes, create a new ADR and mark the previous one as **Superseded**.
- Keep each ADR focused on a single architectural decision.
- Link related ADRs whenever appropriate.

---

# Naming Convention

Use the following filename format:

```text
ADR-XXX-Short-Descriptive-Title.md
```

Examples:

```text
ADR-001-Architecture-Style.md
ADR-002-Backend-Framework.md
ADR-003-Database-Selection.md
ADR-004-AI-Provider.md
```

---

# References

- Michael Nygard — *Documenting Architecture Decisions*
- Robert C. Martin — *Clean Architecture*
- Eric Evans — *Domain-Driven Design*
- Harry Percival & Bob Gregory — *Architecture Patterns with Python*