# ADR-004: Transaction and Category Data Model

## Status

Accepted

## Date

2026-07-10

---

## Context

WealthPilot AI is a personal finance platform that aims to become an AI-powered financial assistant.

The application will support:

* Manual transaction entry
* Email ingestion
* PDF statement ingestion
* SMS parsing
* Future bank API integrations
* Financial dashboards
* Spending analysis
* AI-generated insights
* Goal tracking
* Investment tracking

Since almost every feature depends on financial transactions, the transaction data model must be flexible, scalable, and maintainable.

---

## Decision

### Transaction Model

Each financial event will be represented by a single transaction.

A transaction contains:

* id
* user_id
* account_id
* type
* status
* source
* amount
* currency
* category_id
* merchant
* description
* transaction_date
* source_reference
* created_at
* updated_at

---

### Transaction Types

Supported transaction types are:

* Income
* Expense
* Transfer
* Adjustment

Transfers are treated as their own transaction type instead of being represented as an expense from one account and an income into another account.

This keeps reporting accurate and avoids double-counting money movement.

---

### Transaction Status

Transactions support lifecycle states:

* Pending
* Posted
* Cancelled

This allows future support for pending card transactions, bank synchronization, and cancelled payments.

---

### Transaction Source

Each transaction records its origin.

Supported sources include:

* Manual
* Email
* PDF
* SMS
* Bank API

Recording the source enables auditing, duplicate detection, and AI-assisted repair workflows.

---

### Monetary Values

Transaction amounts will always be stored as positive values.

The transaction type determines whether the amount represents income, expense, transfer, or adjustment.

The project will use Decimal for monetary values to avoid floating-point precision errors.

---

### Dates

Two different timestamps are stored.

transaction_date represents when the financial event actually occurred.

created_at represents when the record was created inside WealthPilot AI.

This distinction enables accurate historical reporting.

---

### Categories

Categories are stored in a dedicated collection.

Transactions reference categories using category_id.

Category names are never duplicated inside transaction documents.

This allows category names to be changed without updating historical transactions.

---

### Category Types

Categories are divided into:

* Income
* Expense

Transfers are intentionally not represented as categories because they are not income or expenses.

---

### System and User Categories

The application supports two kinds of categories.

System categories are available to every user.

Examples include:

* Salary
* Groceries
* Fuel
* Travel
* Shopping

User-defined categories are owned by a specific user.

This is achieved by storing nullable user_id.

System categories have:

user_id = null

User-created categories have:

user_id = <user id>

---

### Duplicate Detection

Imported transactions may contain a source_reference field.

Examples include:

* Email Message-ID
* PDF fingerprint
* SMS hash
* Bank transaction identifier

This field will support future duplicate detection during ingestion.

---

## Consequences

### Advantages

* Supports manual entry and automated imports.
* Scales to AI ingestion workflows.
* Enables accurate financial reporting.
* Avoids duplicated category data.
* Prevents floating-point rounding errors.
* Supports future bank integrations.
* Provides a clean foundation for dashboards and analytics.

### Trade-offs

* Categories require an additional lookup.
* Transfer transactions require dedicated business logic.
* More metadata is stored than a basic budgeting application.

These trade-offs are acceptable because they significantly improve maintainability and future extensibility.

---

## Future Considerations

The model is intentionally designed to support future enhancements, including:

* Recurring transactions
* Attachments and receipts
* Merchant normalization
* AI-assisted categorization
* Budgeting
* Investment transactions
* Multi-currency support
* Bank synchronization
* Financial forecasting
