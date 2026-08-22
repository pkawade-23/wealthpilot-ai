# ADR-00X: Audit Trail and Change History

## Status

Accepted

## Context

WealthPilot AI manages financial data where maintaining a history of changes is important for traceability, debugging, data integrity, and future financial insights.

Business entities such as Accounts, Categories, and Transactions can be created, updated, and deleted over their lifetime.

The application also uses soft deletion for business entities. Therefore, deleting an entity does not physically remove the document from MongoDB. However, the current state of the document alone does not provide a complete history of how or why the data changed.

We need a centralized mechanism to record changes performed across the application's collections.

The audit mechanism should:

- Record important changes to business data.
- Preserve the state of data before and after a change where applicable.
- Identify the user responsible for the action.
- Identify the affected collection and document.
- Record when the action occurred.
- Support the existing soft-delete strategy.
- Be reusable across different repositories and services.
- Keep audit records separate from business collections.

## Decision

We will implement a centralized Audit Trail module backed by a dedicated MongoDB collection named `audit_trails`.

The Audit Trail module will consist of:

- `AuditTrail` model
- `AuditRepository`
- `AuditService`

Business operations will create audit records through the audit service rather than implementing audit logic independently inside every repository.

### Audit Record

Each audit record will contain the following information:

- `id`
- `user_id`
- `collection`
- `document_id`
- `action`
- `before`
- `after`
- `created_at`
- `metadata`

### Actions

The initial supported audit actions will be:

- `CREATE`
- `UPDATE`
- `DELETE`

Additional actions such as `RESTORE` may be introduced later if required.

### Before and After State

For `CREATE` operations:

- `before` will be `null`.
- `after` will contain the created document state.

For `UPDATE` operations:

- `before` will contain the state before the update.
- `after` will contain the state after the update.

For `DELETE` operations:

- `before` will contain the state before deletion.
- `after` will contain the resulting state after deletion.

For soft deletion, the resulting state will contain:

```text
is_deleted = true