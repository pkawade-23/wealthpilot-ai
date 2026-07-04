# Review Center API

## Purpose

The Review Center API manages AI-extracted transaction candidates before they become verified financial transactions.

Every AI-extracted financial event must pass through the Review Center for human verification.

This ensures that dashboards, reports, budgets, and AI insights are generated only from verified financial data.

---

# Workflow

```text
Email / Document

↓

AI Extraction

↓

Transaction Candidate

↓

Review Center

↓

Approve

↓

Verified Transaction

↓

Dashboard
```

Rejected candidates never become transactions.

---

# Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/v1/review-center | List transaction candidates |
| GET | /api/v1/review-center/{id} | Candidate details |
| PATCH | /api/v1/review-center/{id} | Update extracted values |
| POST | /api/v1/review-center/{id}/approve | Approve candidate |
| POST | /api/v1/review-center/{id}/reject | Reject candidate |
| POST | /api/v1/review-center/bulk-approve | Approve multiple candidates |
| POST | /api/v1/review-center/bulk-reject | Reject multiple candidates |
| GET | /api/v1/review-center/summary | Review queue summary |

Authentication is required.

---

# Candidate Status

Supported values:

- NEW
- AI_PROCESSED
- PENDING_REVIEW
- APPROVED
- REJECTED
- TRANSACTION_CREATED

---

# Get Candidates

## Endpoint

```
GET /api/v1/review-center
```

---

## Query Parameters

| Parameter | Description |
|----------|-------------|
| status | Filter by status |
| source | EMAIL / DOCUMENT |
| minConfidence | Minimum confidence score |
| from | Extraction start date |
| to | Extraction end date |
| search | Merchant or description |
| page | Page number |
| pageSize | Items per page |

Example

```
GET /api/v1/review-center?status=PENDING_REVIEW
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
        "merchant": "Amazon",
        "amount": 1499,
        "currency": "INR",
        "date": "2026-07-01",
        "confidence": 0.97,
        "status": "PENDING_REVIEW",
        "sourceType": "EMAIL"
      }
    ]
  }
}
```

---

# Get Candidate

## Endpoint

```
GET /api/v1/review-center/{id}
```

Returns:

- Extracted fields
- Confidence scores
- Original email/document
- Suggested category
- Suggested account
- Extraction metadata

---

# Update Candidate

## Endpoint

```
PATCH /api/v1/review-center/{id}
```

Allows correction before approval.

Example

```json
{
    "merchant": "Amazon India",
    "amount": 1599,
    "categoryId": "...",
    "accountId": "..."
}
```

---

# Approve Candidate

## Endpoint

```
POST /api/v1/review-center/{id}/approve
```

Approval performs:

1. Validation
2. Transaction creation
3. Candidate status update
4. Audit log creation
5. Dashboard refresh

---

## Success Response

```json
{
    "success": true,
    "message": "Transaction approved successfully."
}
```

---

# Reject Candidate

## Endpoint

```
POST /api/v1/review-center/{id}/reject
```

Rejected candidates remain stored for auditing and AI model improvement.

Optional request:

```json
{
    "reason": "Incorrect amount extracted"
}
```

---

# Bulk Approve

## Endpoint

```
POST /api/v1/review-center/bulk-approve
```

Example

```json
{
    "candidateIds": [
        "...",
        "...",
        "..."
    ]
}
```

Maximum:

100 candidates.

---

# Bulk Reject

## Endpoint

```
POST /api/v1/review-center/bulk-reject
```

Supports optional rejection reason.

---

# Review Summary

## Endpoint

```
GET /api/v1/review-center/summary
```

Returns:

- Pending reviews
- High-confidence candidates
- Low-confidence candidates
- Approved today
- Rejected today
- Average review time

---

# Confidence Scores

Every extracted field includes an AI confidence score.

Example

```json
{
    "merchant": {
        "value": "Amazon",
        "confidence": 0.99
    },
    "amount": {
        "value": 1499,
        "confidence": 1.00
    },
    "category": {
        "value": "Shopping",
        "confidence": 0.71
    }
}
```

The frontend should highlight fields with lower confidence to assist reviewers.

---

# Business Rules

- Every candidate belongs to one user.
- Approved candidates create verified transactions.
- Rejected candidates never affect financial reports.
- Candidates cannot be approved twice.
- Transactions created from candidates maintain a reference to the original source.

---

# Validation Rules

- Required fields must be present before approval.
- Referenced accounts and categories must exist.
- Archived accounts cannot receive transactions.

---

# Security Considerations

- Users may only review their own candidates.
- All review actions are audited.
- Original source documents remain immutable.

---

# Future Enhancements

Future versions may support:

- Auto-approve above configurable confidence thresholds
- Keyboard shortcuts for rapid review
- Side-by-side OCR highlighting
- AI explanation of extracted values
- Duplicate candidate detection
- Reviewer statistics
- Collaborative review workflows