# Dashboard API

## Purpose

The Dashboard API provides a consolidated financial overview for the authenticated user.

Unlike CRUD APIs, the Dashboard API aggregates data from multiple domains to provide a single optimized response for the application's home dashboard.

This minimizes frontend network requests and improves application performance.

---

# Endpoint

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | /api/v1/dashboard | Retrieve dashboard summary |

Authentication is required.

---

# Dashboard Sections

The dashboard consists of the following sections.

| Section | Source |
|----------|--------|
| Financial Summary | Accounts + Transactions |
| Spending Overview | Transactions |
| Income Overview | Transactions |
| Account Balances | Accounts |
| Budget Progress | Budgets |
| Goal Progress | Financial Goals |
| Recent Transactions | Transactions |
| Pending Reviews | Transaction Candidates |
| AI Insights | Insights |
| AI Recommendations | Recommendations |
| Notifications | Notifications |

---

# Endpoint

```
GET /api/v1/dashboard
```

---

# Authentication

Required

---

# Query Parameters

Optional

| Parameter | Description |
|-----------|-------------|
| month | Dashboard month |
| year | Dashboard year |

Example

```
GET /api/v1/dashboard?month=7&year=2026
```

If omitted, the current month is used.

---

# Success Response

```json
{
  "success": true,
  "data": {
    "financialSummary": {
      "netWorth": 5400000,
      "monthlyIncome": 180000,
      "monthlyExpense": 92000,
      "monthlySavings": 88000
    },
    "accountBalances": [],
    "budgetSummary": {},
    "goalSummary": {},
    "recentTransactions": [],
    "pendingReviewCount": 4,
    "insights": [],
    "recommendations": [],
    "notifications": []
  }
}
```

---

# Financial Summary

Contains high-level financial metrics.

Fields

- Net Worth
- Total Assets
- Total Liabilities
- Monthly Income
- Monthly Expenses
- Monthly Savings
- Savings Rate

---

# Spending Overview

Provides spending breakdowns.

Examples

- Category spending
- Weekly spending
- Monthly trend
- Top merchants

---

# Budget Summary

Returns:

- Active budgets
- Budget utilization
- Remaining amount
- Over-budget alerts

---

# Goal Summary

Returns:

- Active goals
- Progress percentage
- Estimated completion
- Upcoming milestones

---

# Recent Transactions

Returns the most recent verified transactions.

Default

10 records

Sorted

Newest first

---

# Pending Reviews

Returns:

- Number of transaction candidates awaiting review
- High-confidence approvals
- Low-confidence extractions

---

# AI Insights

Returns the highest priority active insights.

Default

5 insights

---

# AI Recommendations

Returns active recommendations.

Sorted by:

1. Priority
2. Estimated impact
3. Generated date

---

# Notifications

Returns unread notifications.

Maximum

10

---

# Validation Rules

- Dashboard data is always user-specific.
- Deleted resources are excluded.
- Only verified transactions contribute to financial summaries.
- Pending transaction candidates are excluded from calculations.

---

# Performance Requirements

Target response time:

< 500 ms

The backend should aggregate data using optimized queries and parallel service calls where possible.

---

# Caching Strategy

Dashboard responses may be cached for a short duration (e.g., 30–60 seconds) to improve performance.

Cache invalidation occurs after:

- Transaction creation or update
- Budget changes
- Goal updates
- AI insight generation
- Recommendation generation

---

# Error Responses

Possible errors:

- Unauthorized
- Invalid query parameters
- Internal server error

---

# Security Considerations

- Users may only retrieve their own dashboard.
- Financial calculations must use verified data only.
- Cached responses must be isolated per user.

---

# Future Enhancements

Future versions may support:

- Customizable dashboard widgets
- Multi-currency summaries
- Real-time updates using WebSockets
- Dashboard personalization
- AI-generated daily summaries
- Dashboard export