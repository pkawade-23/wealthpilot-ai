# Categories API

## Purpose

The Categories API manages the classification of financial transactions.

Categories provide structure for budgeting, reporting, analytics, AI recommendations, and spending insights.

The system supports both system-defined categories and user-defined custom categories.

---

# Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | /api/v1/categories | List categories |
| GET | /api/v1/categories/{id} | Get category details |
| POST | /api/v1/categories | Create custom category |
| PATCH | /api/v1/categories/{id} | Update custom category |
| DELETE | /api/v1/categories/{id} | Archive custom category |

Authentication is required for all endpoints.

---

# Category Types

Categories are grouped by transaction type.

Supported values:

- INCOME
- EXPENSE

Transfers do not require categories.

---

# Category Sources

Two types of categories exist.

## System Categories

Provided by WealthPilot AI.

Examples:

- Salary
- Groceries
- Rent
- Utilities
- Fuel
- Shopping
- Entertainment
- Medical
- Insurance
- Investments

System categories cannot be deleted.

---

## Custom Categories

Created by users.

Examples:

- Baby Expenses
- Home Renovation
- Side Business
- Pet Care

Users can create, rename, and archive their own categories.

---

# Get Categories

## Endpoint

```
GET /api/v1/categories
```

---

## Query Parameters

| Parameter | Description |
|------------|-------------|
| type | INCOME / EXPENSE |
| source | SYSTEM / CUSTOM |
| status | ACTIVE / ARCHIVED |

Example

```
GET /api/v1/categories?type=EXPENSE
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
                "name": "Groceries",
                "type": "EXPENSE",
                "source": "SYSTEM",
                "icon": "shopping_cart",
                "color": "#4CAF50",
                "status": "ACTIVE"
            }
        ]
    }
}
```

---

# Get Category

## Endpoint

```
GET /api/v1/categories/{id}
```

Returns detailed category information.

---

# Create Category

## Endpoint

```
POST /api/v1/categories
```

## Request

```json
{
    "name": "Baby Expenses",
    "type": "EXPENSE",
    "icon": "child_care",
    "color": "#3F51B5"
}
```

---

## Validation Rules

- Name is required.
- Name must be unique per user.
- Type must be valid.
- Color must be a valid hexadecimal value.
- Icon must be from the supported icon library.

---

# Update Category

## Endpoint

```
PATCH /api/v1/categories/{id}
```

Editable fields:

- Name
- Icon
- Color

System categories cannot be modified.

---

# Archive Category

## Endpoint

```
DELETE /api/v1/categories/{id}
```

Categories are archived rather than deleted.

Transactions remain linked to archived categories.

---

# Business Rules

- Every transaction references one category.
- Categories belong to one transaction type.
- System categories are read-only.
- Custom categories belong to a single user.
- Archived categories cannot be assigned to new transactions.

---

# Validation Rules

- Duplicate category names are not allowed for the same user.
- Users may not archive system categories.
- Transactions retain historical category references.

---

# Security Considerations

- Users can only manage their own custom categories.
- System categories are shared and immutable.
- Category changes are audited.

---

# Future Enhancements

Future versions may support:

- Parent/child categories
- Category aliases
- AI-generated categories
- Emoji support
- Spending limits per category
- Category merge
- Bulk category updates
- Category templates