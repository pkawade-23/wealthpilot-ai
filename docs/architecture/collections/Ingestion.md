# Ingestion Collections

## Purpose

The Ingestion domain is responsible for acquiring financial information from external sources and preparing it for AI processing.

Unlike the Finance domain, collections in the Ingestion domain primarily store **raw or intermediate data**.

The domain follows these principles:

- Preserve original data
- Never modify imported sources
- Support AI processing
- Maintain complete auditability
- Enable future reprocessing using improved AI models

---

# Collections

The Ingestion domain consists of the following collections.

| Collection | Purpose |
|------------|---------|
| emails | Stores forwarded financial emails |
| documents | Stores uploaded documents |
| imports | Stores metadata about bulk imports |
| transaction_candidates | Stores AI-extracted transactions awaiting review |

# Emails Collection

## Purpose

The `emails` collection stores the original forwarded financial emails exactly as they were received.

Emails are treated as immutable records and serve as the permanent source of truth for email-based financial imports.

The collection is **not** used directly for financial calculations.

Instead, emails pass through the AI extraction pipeline, producing one or more transaction candidates.

---

# Responsibilities

The `emails` collection is responsible for:

- Preserving original email content
- Supporting AI extraction
- Maintaining auditability
- Allowing future reprocessing
- Tracking processing status

---

# Relationships

```text
users
   │
   ▼
emails
   │
   ▼
transaction_candidates
   │
   ▼
transactions
```

One email may produce:

- zero transactions
- one transaction
- multiple transactions

Example:

```
Amazon Order

↓

Transaction 1
Laptop

↓

Transaction 2
Delivery Charge
```

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Owner of the email |
| subject | String | Yes | Email subject |
| sender | String | Yes | Sender email address |
| receivedAt | Date | Yes | Original email timestamp |
| rawContent | String | Yes | Original email body |
| htmlContent | String | No | Original HTML version |
| attachments | Array | No | Attachment metadata |
| processingStatus | Enum | Yes | Current processing state |
| aiProcessedAt | Date | No | Time AI completed extraction |
| extractionVersion | String | No | AI extraction model version |
| createdAt | Date | Yes | Record creation timestamp |

---

# Processing Status

Supported values:

- RECEIVED
- PROCESSING
- PROCESSED
- FAILED
- ARCHIVED

These values describe the lifecycle of the email within the ingestion pipeline.

---

# Attachment Metadata

Attachments are stored as metadata only.

Example:

```json
{
    "fileName": "statement.pdf",
    "contentType": "application/pdf",
    "fileSize": 245678,
    "storagePath": "/uploads/documents/statement.pdf"
}
```

Actual attachment files are stored outside MongoDB.

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve user emails |
| sender | Index | Search by sender |
| receivedAt | Index | Chronological sorting |
| processingStatus | Index | Processing queue |

---

# Validation Rules

- Subject cannot be empty.
- Sender must be a valid email address.
- Raw content is mandatory.
- Original email content cannot be modified after ingestion.
- Processing status must follow the defined lifecycle.

---

# Security Considerations

Emails may contain sensitive financial information.

The system should:

- Encrypt data at rest where appropriate.
- Restrict access to the owning user.
- Never expose raw email content unnecessarily.
- Preserve the original email exactly as received.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "subject": "Your Amazon Order",
  "sender": "order-update@amazon.in",
  "receivedAt": "2026-07-04T09:30:00Z",
  "rawContent": "Thank you for your purchase...",
  "htmlContent": "<html>...</html>",
  "attachments": [
    {
      "fileName": "invoice.pdf",
      "contentType": "application/pdf",
      "fileSize": 245678,
      "storagePath": "/uploads/documents/invoice.pdf"
    }
  ],
  "processingStatus": "PROCESSED",
  "aiProcessedAt": "2026-07-04T09:31:10Z",
  "extractionVersion": "v1.0.0",
  "createdAt": "2026-07-04T09:30:05Z"
}
```

---

# Future Enhancements

Future versions may support:

- IMAP integration
- Gmail API integration
- Outlook integration
- Duplicate email detection
- Spam filtering
- Automatic email classification
- AI-powered email summarization

# Documents Collection

## Purpose

The `documents` collection stores uploaded financial documents such as PDF statements, invoices, receipts, bills, and scanned images.

Like emails, documents are immutable and serve as the permanent source of truth for document-based financial imports.

The collection is not used directly for financial calculations. Instead, uploaded documents are processed by OCR (when required) and AI extraction to generate transaction candidates.

---

# Responsibilities

The `documents` collection is responsible for:

- Preserving original uploaded documents
- Tracking document processing status
- Supporting OCR extraction
- Supporting AI extraction
- Maintaining auditability
- Enabling future reprocessing

---

# Relationships

```text
users
   │
   ▼
documents
   │
   ▼
transaction_candidates
   │
   ▼
transactions
```

One document may generate:

- Zero transactions
- One transaction
- Multiple transactions

Examples:

Bank Statement

↓

25 Transactions

Invoice

↓

1 Expense Transaction

Salary Slip

↓

1 Income Transaction

---

# Supported Document Types

The initial version supports:

- PDF
- JPG
- JPEG
- PNG

Future versions may support:

- Excel
- CSV
- HEIC
- TIFF

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Owner of the document |
| fileName | String | Yes | Original file name |
| fileType | String | Yes | MIME type |
| fileSize | Number | Yes | File size in bytes |
| storagePath | String | Yes | Local storage path |
| uploadedAt | Date | Yes | Upload timestamp |
| processingStatus | Enum | Yes | Processing status |
| ocrStatus | Enum | No | OCR processing status |
| aiProcessedAt | Date | No | AI completion timestamp |
| extractionVersion | String | No | AI extraction version |
| pageCount | Number | No | Number of pages |
| createdAt | Date | Yes | Record creation timestamp |

---

# Processing Status

Supported values:

- UPLOADED
- OCR_PROCESSING
- OCR_COMPLETED
- AI_PROCESSING
- PROCESSED
- FAILED
- ARCHIVED

---

# OCR Status

Supported values:

- NOT_REQUIRED
- PENDING
- COMPLETED
- FAILED

---

# Storage Strategy

The uploaded file is stored outside MongoDB.

MongoDB stores only metadata.

Example:

```text
/uploads/documents/
    invoice.pdf
    statement.pdf
    receipt.jpg
```

Future versions may support:

- AWS S3
- Azure Blob Storage
- Google Cloud Storage

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve user documents |
| uploadedAt | Index | Sort by upload date |
| processingStatus | Index | Processing queue |
| fileType | Index | Filtering |

---

# Validation Rules

- File type must be supported.
- File size must not exceed the configured limit.
- Uploaded files cannot be modified after ingestion.
- Every document belongs to exactly one user.

---

# Security Considerations

Documents may contain highly sensitive financial information.

The system should:

- Restrict access to the owning user
- Validate uploaded file types
- Scan uploads for malicious content (future)
- Encrypt storage where appropriate
- Preserve original documents exactly as uploaded

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "fileName": "BankStatement_June2026.pdf",
  "fileType": "application/pdf",
  "fileSize": 1456230,
  "storagePath": "/uploads/documents/BankStatement_June2026.pdf",
  "uploadedAt": "2026-07-04T11:15:00Z",
  "processingStatus": "PROCESSED",
  "ocrStatus": "COMPLETED",
  "aiProcessedAt": "2026-07-04T11:16:45Z",
  "extractionVersion": "v1.0.0",
  "pageCount": 12,
  "createdAt": "2026-07-04T11:15:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Automatic document classification
- Duplicate document detection
- Digital signature validation
- OCR quality scoring
- Multi-language OCR
- Document versioning
- AI-generated document summaries

# Imports Collection

## Purpose

The `imports` collection tracks bulk import operations and their processing lifecycle.

Unlike the `emails` and `documents` collections, which represent individual source items, an import represents a batch of financial records originating from a single source.

Examples include:

- CSV uploads
- Bank statement imports
- Future bank API synchronizations
- Third-party financial platform imports

The collection stores metadata about the import operation and links it to the generated transaction candidates.

---

# Responsibilities

The `imports` collection is responsible for:

- Tracking import jobs
- Recording import statistics
- Monitoring processing progress
- Recording processing errors
- Maintaining auditability
- Supporting future reprocessing

The collection does **not** store financial transactions directly.

---

# Relationships

```text
users
   │
   ▼
imports
   │
   ▼
transaction_candidates
   │
   ▼
transactions
```

One import may generate:

- Zero transaction candidates
- One transaction candidate
- Thousands of transaction candidates

---

# Supported Import Types

Current:

- CSV

Future:

- Bank API
- Excel
- Open Banking
- Investment Platforms
- Credit Card Providers

---

# Import Status

Supported values:

- UPLOADED
- VALIDATING
- PROCESSING
- COMPLETED
- PARTIALLY_COMPLETED
- FAILED
- CANCELLED

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Owner of the import |
| importType | Enum | Yes | Type of import |
| originalFileName | String | Yes | Uploaded file name |
| storagePath | String | Yes | File storage location |
| totalRecords | Number | Yes | Total records detected |
| processedRecords | Number | Yes | Successfully processed records |
| failedRecords | Number | Yes | Failed records |
| processingStatus | Enum | Yes | Current processing status |
| startedAt | Date | No | Processing start time |
| completedAt | Date | No | Processing completion time |
| extractionVersion | String | No | AI extraction version |
| createdAt | Date | Yes | Creation timestamp |

---

# Import Statistics

Each import maintains processing statistics.

Example:

```text
Total Records:        320

Processed:            312

Failed:                 8

Success Rate:       97.5%
```

These statistics help users understand the outcome of the import process.

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve user imports |
| processingStatus | Index | Processing queue |
| importType | Index | Filter imports |
| createdAt | Index | Chronological sorting |

---

# Validation Rules

- Import type must be supported.
- Every import belongs to exactly one user.
- Original import file must be preserved.
- Processing statistics must remain consistent.

Example:

```
processedRecords + failedRecords <= totalRecords
```

---

# Security Considerations

The system should:

- Restrict access to the owning user.
- Preserve the original import file.
- Prevent modification after processing.
- Log processing failures for diagnostics.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "importType": "CSV",
  "originalFileName": "transactions_june_2026.csv",
  "storagePath": "/uploads/imports/transactions_june_2026.csv",
  "totalRecords": 320,
  "processedRecords": 312,
  "failedRecords": 8,
  "processingStatus": "COMPLETED",
  "startedAt": "2026-07-04T12:00:00Z",
  "completedAt": "2026-07-04T12:00:42Z",
  "extractionVersion": "v1.0.0",
  "createdAt": "2026-07-04T12:00:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Scheduled imports
- Incremental synchronization
- Automatic duplicate detection
- Import history comparison
- Import rollback
- Retry failed records
- Open Banking integrations

# Transaction Candidates Collection

## Purpose

The `transaction_candidates` collection stores financial transactions extracted by the AI from external sources before they become verified financial records.

A transaction candidate represents an intermediate state between raw financial data and an approved transaction.

Candidates must be reviewed by the user before they are promoted to the `transactions` collection.

This review process ensures data quality, transparency, and user trust.

---

# Responsibilities

The `transaction_candidates` collection is responsible for:

- Storing AI-extracted transaction data
- Maintaining AI confidence scores
- Supporting user review and corrections
- Tracking approval and rejection decisions
- Preserving links to original source data
- Maintaining a complete audit trail

---

# Relationships

```text
                emails
                   │
                   │
             documents
                   │
                   │
               imports
                   │
                   ▼
        transaction_candidates
                   │
         ┌─────────┴─────────┐
         │                   │
         ▼                   ▼
     Approved            Rejected
         │
         ▼
    transactions
```

One source may generate multiple transaction candidates.

Each approved candidate produces exactly one verified transaction.

---

# Candidate Lifecycle

```text
CREATED
    │
    ▼
AI_PROCESSED
    │
    ▼
PENDING_REVIEW
    │
 ┌──┴──────────────┐
 │                 │
 ▼                 ▼
APPROVED      REJECTED
 │
 ▼
TRANSACTION_CREATED
```

---

# Source Types

Each candidate records where it originated.

Supported values:

- EMAIL
- DOCUMENT
- CSV_IMPORT
- MANUAL_ENTRY
- BANK_API (Future)
- SMS (Future)

---

# Review Status

Supported values:

- PENDING_REVIEW
- APPROVED
- REJECTED

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Owner of the transaction |
| sourceType | Enum | Yes | Origin of the transaction |
| sourceId | ObjectId | Yes | Reference to the original source |
| merchant | String | No | Extracted merchant name |
| amount | Decimal | Yes | Transaction amount |
| currency | String | Yes | Currency code |
| transactionDate | Date | Yes | Transaction date |
| category | String | No | AI-suggested category |
| transactionType | Enum | Yes | EXPENSE, INCOME or TRANSFER |
| paymentMethod | String | No | Card, UPI, Cash, etc. |
| notes | String | No | AI-generated or user-added notes |
| confidenceScores | Object | Yes | AI confidence per field |
| reviewStatus | Enum | Yes | Current review status |
| reviewedBy | ObjectId | No | User who reviewed the candidate |
| reviewedAt | Date | No | Review timestamp |
| rejectionReason | String | No | Reason for rejection |
| finalTransactionId | ObjectId | No | Reference to approved transaction |
| extractionVersion | String | No | AI extraction model version |
| createdAt | Date | Yes | Creation timestamp |
| updatedAt | Date | Yes | Last update timestamp |

---

# AI Confidence Scores

Confidence is stored per extracted field.

Example:

```json
{
  "merchant": 0.99,
  "amount": 1.00,
  "transactionDate": 0.96,
  "category": 0.72
}
```

This allows the Review Center to highlight low-confidence fields instead of treating the entire extraction as equally reliable.

---

# User Corrections

Users may edit extracted values before approval.

The approved values become the official transaction.

The original AI extraction should remain available for audit purposes.

Future versions may store a complete field-level change history.

---

# Approval Workflow

When approved:

1. Validate required fields.
2. Create a new document in the `transactions` collection.
3. Store the new transaction's ID in `finalTransactionId`.
4. Update `reviewStatus` to `APPROVED`.

---

# Rejection Workflow

When rejected:

- No transaction is created.
- The candidate is retained for audit purposes.
- The rejection reason may be recorded.

Rejected candidates can be used to improve future AI models.

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve user candidates |
| reviewStatus | Index | Review queue |
| sourceType | Index | Filter by origin |
| sourceId | Index | Trace back to source |
| transactionDate | Index | Date filtering |
| createdAt | Index | Chronological sorting |

---

# Validation Rules

- Every candidate belongs to exactly one user.
- Every candidate references exactly one source.
- Amount must be greater than zero.
- Currency must use ISO 4217 codes.
- Transaction type must be valid.
- Approved candidates must reference a final transaction.

---

# Security Considerations

Transaction candidates may contain sensitive financial information.

The system should:

- Restrict access to the owning user.
- Record review actions.
- Preserve AI extraction results.
- Prevent unauthorized approval or rejection.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "sourceType": "EMAIL",
  "sourceId": "ObjectId",
  "merchant": "Amazon",
  "amount": 2499.00,
  "currency": "INR",
  "transactionDate": "2026-07-03T18:30:00Z",
  "category": "Shopping",
  "transactionType": "EXPENSE",
  "paymentMethod": "Credit Card",
  "notes": "Amazon order",
  "confidenceScores": {
    "merchant": 0.99,
    "amount": 1.0,
    "transactionDate": 0.97,
    "category": 0.74
  },
  "reviewStatus": "PENDING_REVIEW",
  "reviewedBy": null,
  "reviewedAt": null,
  "rejectionReason": null,
  "finalTransactionId": null,
  "extractionVersion": "v1.0.0",
  "createdAt": "2026-07-04T12:45:00Z",
  "updatedAt": "2026-07-04T12:45:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Batch approval
- AI-assisted correction suggestions
- Duplicate candidate detection
- Confidence threshold automation
- Reviewer comments
- Multi-user review workflows
- Active learning from user corrections