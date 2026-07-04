# User Stories

**Project:** WealthPilot AI  
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** 2026-07-02  
**Owner:** Pratik Kawade

---

# Purpose

This document defines the user stories for WealthPilot AI.

Each user story captures a business requirement from the perspective of the end user and includes acceptance criteria that define when the feature is considered complete.

These user stories will serve as the foundation for sprint planning, API design, UI development, and testing.

---

# Epic 1 — Authentication

## US-001 — User Registration

**Priority:** Must Have

### User Story

As a new user, I want to create an account so that I can securely access my financial data.

### Acceptance Criteria

- User can register using name, email, and password.
- Email must be unique.
- Password meets security requirements.
- Password is securely hashed.
- Email verification is supported.
- User cannot access protected resources until authenticated.

---

## US-002 — User Login

**Priority:** Must Have

### User Story

As a registered user, I want to securely log in to my account.

### Acceptance Criteria

- Login using email and password.
- JWT Access Token generated.
- Refresh Token generated.
- Invalid credentials return an appropriate error.
- Authenticated users can access protected APIs.

---

## US-003 — Password Management

**Priority:** Should Have

### User Story

As a user, I want to reset or change my password.

### Acceptance Criteria

- Forgot password workflow.
- Password reset token.
- Password change after login.
- Old password verification.

---

# Epic 2 — Dashboard

## US-004 — Financial Dashboard

**Priority:** Must Have

### User Story

As a user, I want to view my financial health at a glance.

### Acceptance Criteria

Dashboard displays:

- Net Worth
- Monthly Income
- Monthly Expenses
- Savings Rate
- Investment Summary
- Loan Summary
- Recent Transactions
- Spending Categories
- AI Financial Summary

---

# Epic 3 — Transaction Management

## US-005 — Manual Transaction Entry

**Priority:** Must Have

### User Story

As a user, I want to manually record financial transactions.

### Acceptance Criteria

User can:

- Add Income
- Add Expense
- Select Category
- Enter Amount
- Choose Date
- Add Notes

Validation prevents invalid values.

---

## US-006 — Edit Transaction

**Priority:** Must Have

### User Story

As a user, I want to update incorrect transaction details.

### Acceptance Criteria

User can modify:

- Amount
- Category
- Date
- Notes

Changes are immediately reflected in reports.

---

## US-007 — Delete Transaction

**Priority:** Must Have

### User Story

As a user, I want to remove unwanted transactions.

### Acceptance Criteria

- Confirmation before deletion.
- Dashboard updates automatically.

---

## US-008 — Search & Filter Transactions

**Priority:** Should Have

### Acceptance Criteria

User can filter by:

- Date
- Category
- Merchant
- Amount
- Tags

---

# Epic 4 — Email Intelligence

## US-009 — Process Financial Emails

**Priority:** Must Have

### User Story

As a user, I want WealthPilot AI to understand my forwarded financial emails.

### Acceptance Criteria

System:

- Receives email
- Extracts sender
- Identifies financial information
- Extracts transaction details
- Suggests category
- Saves as Pending Review

---

## US-010 — Review Extracted Transactions

**Priority:** Must Have

### Acceptance Criteria

User can:

- Approve
- Reject
- Edit
- Merge duplicates

Only approved transactions affect reports.

---

# Epic 5 — Document Intelligence

## US-011 — Upload Financial Documents

**Priority:** Must Have

### User Story

As a user, I want to upload financial documents for automatic analysis.

### Acceptance Criteria

Supported:

- PDF
- JPG
- PNG

System:

- Stores original file
- Extracts text
- Extracts financial information
- Generates embeddings
- Makes document searchable

---

## US-012 — View Uploaded Documents

**Priority:** Should Have

### Acceptance Criteria

User can:

- Search documents
- Download originals
- Delete documents

---

# Epic 6 — AI Assistant

## US-013 — Ask Financial Questions

**Priority:** Must Have

### User Story

As a user, I want to ask questions about my finances using natural language.

### Example Questions

- How much did I spend last month?
- Which subscriptions do I have?
- What are my biggest expenses?
- Can I save more?
- Summarize my financial health.

### Acceptance Criteria

Responses should:

- Use user-specific financial data.
- Use uploaded documents when relevant.
- Explain calculations.
- Return helpful recommendations.

---

## US-014 — AI Financial Summary

**Priority:** Must Have

### User Story

As a user, I want AI to summarize my financial situation.

### Acceptance Criteria

Summary includes:

- Income overview
- Expense overview
- Savings insights
- Risk observations
- Personalized recommendations

---

# Epic 7 — Scenario Simulator

## US-015 — Financial Scenario Simulation

**Priority:** Should Have

### User Story

As a user, I want to understand the impact of financial decisions before making them.

### Examples

- Increase salary
- Increase SIP
- Buy a car
- Prepay home loan
- Purchase a house

### Acceptance Criteria

Simulation returns:

- Updated savings
- Cash flow
- Net worth impact
- AI recommendations

---

# Epic 8 — Financial Timeline

## US-016 — Financial Timeline

**Priority:** Should Have

### User Story

As a user, I want a chronological view of my financial history.

### Acceptance Criteria

Timeline includes:

- Salary credits
- Investments
- Loan payments
- Credit card bills
- Insurance premiums
- Major purchases
- AI insights

---

# Epic 9 — Knowledge Base

## US-017 — Search Financial Documents

**Priority:** Should Have

### User Story

As a user, I want AI to search my uploaded documents.

### Acceptance Criteria

Example Questions:

- Show my home loan statement.
- Find my insurance policy.
- What was my bonus in 2025?

Responses use Retrieval-Augmented Generation (RAG).

---

# Epic 10 — Profile & Settings

## US-018 — Manage Profile

**Priority:** Could Have

### Acceptance Criteria

User can:

- Update profile
- Change password
- Configure currency
- Configure AI preferences
- Set financial goals

---

# Definition of Done (DoD)

A user story is considered complete when:

- Functional requirements are implemented.
- Unit tests pass.
- Integration tests pass.
- API documentation is updated.
- UI is responsive.
- Validation is complete.
- Error handling is implemented.
- Logging is added.
- Security review is completed.
- Code review is approved.
- CI pipeline passes.
- Documentation is updated.

---

# Story Priority Legend

| Priority | Description |
|----------|-------------|
| Must Have | Required for MVP |
| Should Have | Important but can be deferred if necessary |
| Could Have | Nice-to-have feature for future releases |

---

# Notes

These user stories represent the initial product backlog for WealthPilot AI.

Additional stories may be introduced as the project evolves, but all new functionality should align with the Product Requirements Document (PRD) and be supported by relevant Architecture Decision Records (ADRs) where applicable.