# Database Design

## Purpose

This document defines the database design for WealthPilot AI.

The primary objectives of the database are to:

- Store financial information securely.
- Preserve original source documents and emails.
- Maintain a single source of truth for financial transactions.
- Support AI-powered financial analysis.
- Enable Retrieval-Augmented Generation (RAG).
- Maintain complete auditability of imported financial data.
- Support future scalability without major schema redesign.

The database is designed using MongoDB as the primary document database and ChromaDB as the vector database for semantic search.

---

# Database Design Principles

The database architecture follows the principles below.

## 1. Single Source of Truth

All financial calculations within WealthPilot AI are based on the **Transactions** collection.

Regardless of whether data originates from:

- Manual entry
- Forwarded emails
- Uploaded documents
- CSV imports
- Future bank integrations

every verified financial event ultimately becomes a Transaction.

This ensures:

- Consistent reporting
- Simplified analytics
- Easier reconciliation
- Reliable AI insights

---

## 2. Preserve Original Sources

Original data is never modified.

Examples include:

- Forwarded emails
- Uploaded PDF statements
- Bank documents
- CSV imports

These records remain immutable and serve as the permanent source of truth for auditing and future AI improvements.

---

## 3. AI-Assisted Verification

AI-generated information is never automatically trusted.

Every AI-extracted financial record passes through a review workflow before becoming an official transaction.

This allows users to:

- Review extracted information
- Correct inaccuracies
- Approve valid transactions
- Reject incorrect extractions

Human verification always takes precedence over AI predictions.

---

## 4. Separation of Raw and Processed Data

The system separates:

Raw Data

↓

AI Extraction

↓

Verified Financial Data

This separation improves traceability, debugging, and future model retraining.

---

## 5. Auditability

Every imported financial record should be traceable back to its original source.

The system maintains relationships between:

- Original email
- Original document
- AI extraction
- User modifications
- Final transaction

This enables complete transparency throughout the data lifecycle.

---

## 6. Extensibility

The schema is designed to support future data sources without requiring significant redesign.

Potential future sources include:

- Bank APIs
- SMS parsing
- Investment platforms
- Accounting software
- Credit card providers

All future sources should integrate into the same ingestion pipeline.

---

## 7. Privacy by Design

Sensitive financial information is stored locally.

The database design minimizes unnecessary duplication of personal data and supports local AI processing using Ollama.

No financial information is shared with external AI providers by default.

---

# Database Technology

WealthPilot AI uses two databases, each optimized for a specific purpose.

## MongoDB

MongoDB serves as the primary operational database.

Responsibilities include:

- User accounts
- Financial transactions
- Documents
- Emails
- Categories
- Goals
- Notifications
- AI conversations
- Application configuration

MongoDB stores structured business data.

---

## ChromaDB

ChromaDB stores vector embeddings generated from financial documents and AI-processed content.

Responsibilities include:

- Document embeddings
- Email embeddings
- AI retrieval context
- Semantic search

ChromaDB is used exclusively to support Retrieval-Augmented Generation (RAG).

It is not considered the primary source of business data.

---

# Data Ingestion Pipeline

All external financial information enters the system through a unified ingestion pipeline.

```text
              External Sources
                     │
     ┌───────────────┼───────────────┐
     │               │               │
     ▼               ▼               ▼
 Forwarded Email   PDF Upload    Manual Import
     │               │               │
     └───────────────┼───────────────┘
                     ▼
            AI Extraction Engine
                     ▼
        Transaction Candidates
                     ▼
            Review Center (UI)
                     ▼
       Approved Transactions
                     ▼
      Dashboard • Reports • AI
```

The ingestion pipeline provides a consistent workflow regardless of the source of the financial data.

---

# Transaction Candidate Workflow

Before a financial record becomes an official transaction, it passes through an intermediate review stage.

Workflow:

```text
Original Source

↓

AI Extraction

↓

Transaction Candidate

↓

User Review

↓

Approved Transaction
```

This review process ensures that AI-generated data is verified before affecting financial reports or analytics.

---

# Transaction Candidate Lifecycle

Each transaction candidate progresses through a defined lifecycle.

```text
NEW
    │
    ▼
AI_PROCESSED
    │
    ▼
PENDING_REVIEW
    │
 ┌──┴───────────────┐
 │                  │
 ▼                  ▼
APPROVED        REJECTED
 │
 ▼
TRANSACTION_CREATED
```

This lifecycle enables clear tracking of each imported financial record.

---

# Review Center

The Review Center is the primary interface for validating AI-extracted financial information.

Users can:

- Review extracted fields
- Edit incorrect values
- Approve transactions
- Reject invalid extractions
- Compare extracted data with the original source

Only approved records become permanent transactions.

---

# AI Confidence Scores

Each extracted field may include a confidence score generated by the AI extraction pipeline.

Example:

- Merchant: 99%
- Amount: 100%
- Category: 72%
- Date: 96%

Low-confidence fields can be highlighted in the Review Center, allowing users to focus on areas that require verification.

Confidence scores are advisory and do not replace user validation.

---

# Collections Overview

The WealthPilot AI database is organized into logical business domains rather than UI features.

Each collection has a single responsibility and participates in the overall financial data lifecycle.

Collections are grouped into the following domains:

1. Identity
2. Ingestion
3. Finance
4. AI
5. System

The following sections provide a high-level overview of each domain.