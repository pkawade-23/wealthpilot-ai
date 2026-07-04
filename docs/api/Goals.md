# Financial Goals API

## Purpose

The Financial Goals API manages the user's short-term and long-term financial objectives.

Goals help users save toward specific targets, monitor progress, forecast completion dates, and receive AI-powered recommendations to improve the likelihood of success.

Goals integrate with transactions, budgets, dashboards, AI insights, and financial scenarios.

---

# Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/v1/goals | List goals |
| GET | /api/v1/goals/{id} | Get goal details |
| POST | /api/v1/goals | Create goal |
| PATCH | /api/v1/goals/{id} | Update goal |
| DELETE | /api/v1/goals/{id} | Archive goal |
| POST | /api/v1/goals/{id}/contributions | Add contribution |
| GET | /api/v1/goals/summary | Goal summary |

Authentication is required for all endpoints.

---

# Goal Types

Supported values:

- EMERGENCY_FUND
- HOME
- VEHICLE
- VACATION
- RETIREMENT
- EDUCATION
- INVESTMENT
- DEBT_REPAYMENT
- CUSTOM

---

# Goal Status

Supported values:

- ACTIVE
- COMPLETED
- PAUSED
- ARCHIVED

---

# Get Goals

## Endpoint

```
GET /api/v1/goals
```

## Query Parameters

| Parameter | Description |
|----------|-------------|
| status | ACTIVE / COMPLETED |
| goalType | Goal type |
| targetYear | Filter by target year |

Example

```
GET /api/v1/goals?status=ACTIVE
```

---

## Success Response

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "...",
        "name": "Emergency Fund",
        "goalType": "EMERGENCY_FUND",
        "targetAmount": 600000,
        "currentAmount": 185000,
        "progress": 30.8,
        "targetDate": "2028-12-31",
        "status": "ACTIVE"
      }
    ]
  }
}
```

---

# Get Goal

## Endpoint

```
GET /api/v1/goals/{id}
```

Returns detailed goal information including contribution history and AI projections.

---

# Create Goal

## Endpoint

```
POST /api/v1/goals
```

## Request

```json
{
  "name": "Emergency Fund",
  "goalType": "EMERGENCY_FUND",
  "targetAmount": 600000,
  "currentAmount": 100000,
  "targetDate": "2028-12-31",
  "linkedAccountId": "...",
  "notes": "Six months of expenses"
}
```

---

## Validation Rules

- Goal name is required.
- Target amount must be greater than zero.
- Current amount cannot exceed target amount.
- Target date must be in the future.

---

# Update Goal

## Endpoint

```
PATCH /api/v1/goals/{id}
```

Editable fields:

- Name
- Target Amount
- Target Date
- Notes
- Status

---

# Archive Goal

## Endpoint

```
DELETE /api/v1/goals/{id}
```

Goals are archived instead of permanently deleted.

Historical analytics remain available.

---

# Add Contribution

## Endpoint

```
POST /api/v1/goals/{id}/contributions
```

## Request

```json
{
  "amount": 5000,
  "accountId": "...",
  "date": "2026-07-10",
  "notes": "Monthly contribution"
}
```

A contribution creates a linked financial transaction and updates the goal's progress.

---

# Goal Summary

## Endpoint

```
GET /api/v1/goals/summary
```

Returns:

- Total active goals
- Total target amount
- Total saved
- Overall progress
- Goals at risk
- Recently completed goals

---

# Goal Progress

Progress is calculated as:

```
Current Amount

÷

Target Amount

×

100
```

---

# Goal Forecast

The backend estimates:

- Expected completion date
- Monthly contribution required
- Progress trend
- Probability of meeting the target

Forecasts use historical contribution patterns and AI analysis.

---

# Business Rules

- Goals belong to a single user.
- Contributions must reference a valid account.
- Archived goals cannot receive new contributions.
- Completed goals become read-only.

---

# Validation Rules

- Target amount must be positive.
- Target date cannot be in the past.
- Contributions must be greater than zero.
- Linked accounts must belong to the authenticated user.

---

# Security Considerations

- Users may only manage their own goals.
- Contributions are fully audited.
- Forecasts use only verified financial data.

---

# Future Enhancements

Future versions may support:

- Shared family goals
- Goal templates
- Automatic recurring contributions
- Investment-linked goals
- Goal milestones
- AI-generated savings plans
- Goal dependencies
- Goal reminders