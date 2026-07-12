# WealthPilot AI Roadmap

## Vision

WealthPilot AI is an AI-powered personal finance platform that helps users organize, understand, and optimize their financial life.

The long-term vision is to combine traditional personal finance management with artificial intelligence. Instead of simply recording transactions, WealthPilot AI will automatically ingest financial information from emails and documents, assist users in repairing extracted data, generate financial insights, and provide an AI-powered conversational assistant.

The project is being built as a production-quality application with clean architecture, comprehensive documentation, and a scalable backend.

---

# Guiding Principles

* Clean Architecture
* Domain-driven module organization
* Strong separation of concerns
* API-first development
* AI-ready data model
* Security by default
* Maintainable and extensible codebase
* Comprehensive documentation

---

# Technology Stack

## Backend

* FastAPI
* Python 3.14
* MongoDB
* Pydantic v2
* PyMongo Async
* JWT Authentication
* Argon2 Password Hashing

## Frontend (Planned)

* Angular
* Angular Material
* AG Grid

## Artificial Intelligence (Planned)

* Ollama
* LangChain
* ChromaDB
* Retrieval-Augmented Generation (RAG)

---

# Project Phases

## ✅ Phase 1 — Backend Foundation (Completed)

### Infrastructure

* FastAPI application setup
* Configuration management
* Logging
* Dockerized MongoDB
* Database manager
* Application lifecycle

### Architecture

* Clean Architecture
* Repository Pattern
* Service Layer
* Standard API responses
* Global exception handling

### Authentication

* User registration
* User login
* JWT authentication
* Password hashing with Argon2
* Current user dependency

### Accounts

* Create account
* List accounts
* Get account by ID
* Update account
* Delete account
* Ownership validation
* Duplicate account prevention

### Documentation

* Architecture documentation
* Database documentation
* Ingestion design
* Architecture Decision Records (ADR)

---

## 🚧 Phase 2 — Financial Domain

### Categories

* Category model
* System categories
* User-defined categories
* Category management API

### Transactions

* Transaction model
* Transaction CRUD
* Income
* Expense
* Transfer
* Adjustment
* Merchant support
* Filtering
* Pagination
* Reporting foundation

### Dashboard

* Net worth
* Income summary
* Expense summary
* Cash flow
* Account balances
* Spending by category
* Recent transactions

---

## 🔜 Phase 3 — Intelligent Data Ingestion

### Email Processing

* Email forwarding
* Email parser
* AI extraction
* Duplicate detection

### Document Processing

* PDF upload
* OCR
* Statement parsing
* Receipt parsing

### Repair Station

* Review extracted transactions
* Correct AI mistakes
* Manual approval workflow

---

## 🔮 Phase 4 — AI Financial Assistant

### Retrieval-Augmented Generation (RAG)

* Financial knowledge base
* Document embeddings
* Semantic search

### AI Assistant

* Financial Q&A
* Spending analysis
* Personalized recommendations
* Investment insights
* Budget guidance
* Goal planning

---

## 🌍 Phase 5 — Advanced Features

* Investment portfolio management
* Loan tracking
* Goal tracking
* Budget planning
* Multi-currency support
* Bank API integrations
* Notifications
* Mobile application
* Analytics and forecasting

---

# Development Workflow

Each major feature follows the same lifecycle:

1. Requirements
2. Architecture & Design
3. Architecture Decision Record (ADR) (when applicable)
4. Data Model
5. API Design
6. Implementation
7. Testing
8. Documentation
9. Code Review
10. Release

---

# Current Status

**Current Phase:** Phase 2 — Financial Domain

**Next Milestone:** Category Module

**Long-Term Goal:** Deliver an AI-powered personal finance platform capable of securely ingesting financial data, providing intelligent insights, and acting as a conversational financial assistant.

---

# Success Criteria

The project will be considered successful when it:

* Demonstrates production-quality backend architecture.
* Provides a complete personal finance management experience.
* Supports AI-assisted financial data ingestion.
* Delivers meaningful financial insights through AI.
* Serves as a strong portfolio project showcasing backend engineering, system design, and applied AI.
