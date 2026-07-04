# Budgets API

## Purpose

The Budgets API manages spending budgets for users.

Budgets help users track planned spending, monitor progress, receive alerts, and generate AI-powered recommendations to improve financial discipline.

Budgets are evaluated against verified transactions only.

---

# Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | /api/v1/budgets | List budgets |
| GET | /api/v1/budgets/{id} | Get budget details |
| POST | /api/v1/budgets | Create budget |
| PATCH | /api/v1/budgets/{id} | Update budget |
| DELETE | /api/v1/budgets/{id} | Archive budget |
| GET | /api/v1/budgets/summary | Budget overview |

Authentication is required for all endpoints.

---

# Budget Periods

Supported values:

- MONTHLY
- QUARTERLY
- YEARLY
- CUSTOM

---

# Budget Status

Supported values:

- ACTIVE
- COMPLETED
- ARCHIVED

---

# Get Budgets

## Endpoint

```
GET /api/v1/budgets
```

---

## Query Parameters

| Parameter | Description |
|------------|-------------|
| status | ACTIVE / ARCHIVED |
| categoryId | Filter by category |
| period | MONTHLY / YEARLY |
| year | Budget year |

Example

```
GET /api/v1/budgets?period=MONTHLY
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
                "name": "Groceries Budget",
                "categoryId": "...",
                "budgetAmount": 15000,
                "spentAmount": 9200,
                "remainingAmount": 5800,
                "utilization": 61.3,
                "period": "MONTHLY",
                "status": "ACTIVE"
            }
        ]
    }
}
```

---

# Get Budget

## Endpoint

```
GET /api/v1/budgets/{id}
```

Returns detailed budget information including spending history and progress.

---

# Create Budget

## Endpoint

```
POST /api/v1/budgets
```

## Request

```json
{
    "name": "Groceries",
    "categoryId": "...",
    "budgetAmount": 15000,
    "period": "MONTHLY",
    "startDate": "2026-07-01",
    "endDate": "2026-07-31"
}
```

---

## Validation Rules

- Budget amount must be greater than zero.
- Category must exist.
- Active budget periods must not overlap for the same category.
- End date must be after start date.

---

# Update Budget

## Endpoint

```
PATCH /api/v1/budgets/{id}
```

Editable fields:

- Name
- Budget Amount
- Start Date
- End Date
- Status

---

# Archive Budget

## Endpoint

```
DELETE /api/v1/budgets/{id}
```

Budgets are archived rather than deleted.

Historical reports continue to include archived budgets.

---

# Budget Summary

## Endpoint

```
GET /api/v1/budgets/summary
```

Returns:

- Total budget
- Total spent
- Remaining budget
- Over-budget categories
- Highest utilization
- Lowest utilization
- Budget health score

---

# Budget Calculation

Budget utilization is calculated as:

```
Spent Amount

÷

Budget Amount

×

100
```

Example:

```
Budget = ₹20,000

Spent = ₹15,000

Utilization = 75%
```

---

# Budget Alerts

The backend automatically generates notifications when configurable thresholds are reached.

Default thresholds:

- 50%
- 75%
- 90%
- 100%

Threshold values may become user-configurable in future versions.

---

# Business Rules

- Budgets are evaluated using verified transactions only.
- Archived transactions are excluded.
- Transfers do not affect budgets.
- Multiple budgets may exist for different categories.
- One active budget per category and period.

---

# Validation Rules

- Budget amount must be positive.
- Category must belong to the authenticated user or be a system category.
- Date ranges must not overlap for the same category and period.

---

# Security Considerations

- Users may only access their own budgets.
- Budget modifications are audited.
- Calculations use verified financial data only.

---

# Future Enhancements

Future versions may support:

- Overall monthly budgets
- Multi-category budgets
- Shared family budgets
- Rollover budgets
- Budget templates
- AI-generated budget recommendations
- Predictive overspending alerts
- Dynamic budget adjustments