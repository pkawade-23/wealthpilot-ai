# ADR-007: Reporting Architecture and Transaction Semantics

## Status

Accepted

## Context

WealthPilot AI requires financial reporting capabilities to power dashboards, analytics, and AI-driven insights. The current transaction model supports four transaction types (INCOME, EXPENSE, TRANSFER, ADJUSTMENT) and multi-currency operations, but no reporting layer exists.

We need a reusable reporting foundation that:
- Uses MongoDB aggregation pipelines for efficient database-side computation
- Respects the existing clean architecture (repository/service/schema separation)
- Handles transaction semantics correctly across all transaction types
- Preserves multi-currency boundaries without exchange-rate conversion
- Provides a foundation for future dashboard and AI features

## Decision

### 1. Reporting Architecture

Financial reports will be implemented as a dedicated reporting layer following the existing clean architecture:

```
API
  ↓
Reporting Service
  ↓
Reporting Repository
  ↓
MongoDB aggregation pipelines
```

- **Repositories** own MongoDB aggregation pipeline construction
- **Services** own business rules, date validation, and composition
- **Schemas** own request/response DTOs and validation

### 2. MongoDB Aggregation

Reporting queries must use MongoDB aggregation pipelines rather than loading transactions into Python for application-side computation.

All reports must be scoped by:
- `user_id` (authenticated user)
- `is_deleted = false`

### 3. Transaction Semantics

| Transaction Type | Income Summary | Expense Summary | Cash Flow | Spending by Category | Transaction Counts |
|-----------------|---------------|-----------------|-----------|---------------------|-------------------|
| INCOME          | ✅ Included   | ❌ Excluded     | +Positive | ❌ Excluded         | ✅ Counted        |
| EXPENSE         | ❌ Excluded   | ✅ Included     | -Negative | ✅ Grouped by category | ✅ Counted    |
| TRANSFER        | ❌ Excluded   | ❌ Excluded     | 0 Neutral | ❌ Excluded         | ✅ Counted        |
| ADJUSTMENT      | ❌ Excluded   | ❌ Excluded     | 0 Neutral | ❌ Excluded         | ✅ Counted        |

**TRANSFER**: Represents internal movement between user-owned accounts. Does not affect net worth, income, or expenses. Excluded from income, expenses, cash flow, and spending-by-category. Only appears in transaction counts.

**ADJUSTMENT**: For the initial implementation, treated as neutral correction:
- Excluded from income, expenses, cash flow, and spending-by-category
- Included only in transaction counts
- **Note**: ADJUSTMENT semantics may be revisited when account balance management is formally designed.

### 4. Multi-Currency

Reports must preserve currency boundaries:

- Aggregate independently per currency
- Never combine different currencies into a single monetary total
- No exchange-rate conversion in this implementation
- Currency conversion is explicitly deferred to a future feature requiring a dedicated exchange-rate design

### 5. Date Filtering

Reports operate on `transaction_date`:

- Support optional `date_from` and `date_to`
- Validate that `date_from` cannot be greater than `date_to`
- Do not introduce arbitrary timezone conversions

### 6. Spending by Category

Expense reporting may group transactions by `category_id`:

- Uncategorized expenses must remain representable (category_id may be null)
- Category joins via MongoDB aggregation must respect category ownership/user boundaries
- Only EXPENSE-type transactions participate in spending-by-category

### 7. Account Balances

Do NOT implement account balance reporting as part of this ADR's implementation.

**Rationale**: The current Account and Transaction models are insufficient for a fully correct dynamic balance calculation, particularly around transfer direction. The Transaction model lacks explicit source/destination account fields for transfers, making it impossible to determine whether a TRANSFER is incoming or outgoing for a given account.

Account balance calculation will be addressed by a separate future ADR when the model supports it correctly.

### 8. Reporting Scope

Initial reports:
- Income summary
- Expense summary
- Cash flow
- Spending by category
- Transaction summary

Account balances are explicitly deferred.

### 9. Performance

- MongoDB aggregation pipelines are preferred over application-side aggregation
- Indexes will be introduced only after the reporting query patterns are established and reviewed
- Do not add indexes as part of this ADR

### 10. Consequences

**Benefits:**
- Efficient database-side aggregation via MongoDB pipelines
- Clean separation from CRUD operations
- Reusable reporting layer for dashboards and AI features
- Precise Decimal128 monetary calculations without float conversion
- Clear transaction semantics prevent double-counting

**Trade-offs:**
- Multi-currency results require consumers to handle currencies separately (no unified total)
- Account balance reporting remains deferred until model supports transfer direction
- ADJUSTMENT semantics are provisional and may change with future ADR

## Rationale

The dedicated reporting layer maintains clean separation from CRUD operations while leveraging MongoDB's aggregation framework for performance. The transaction semantics table ensures consistent behavior across all reports and prevents the common pitfall of double-counting TRANSFER transactions. Multi-currency preservation avoids silent precision loss from premature currency conversion.

## Alternatives Considered

1. **Application-side aggregation**: Fetch all transactions to Python and compute — rejected due to memory/performance concerns and loss of database-level optimization
2. **Unified currency total**: Convert all amounts to a base currency — rejected because exchange-rate design is out of scope and introduces precision/conversion complexity
3. **TRANSFER as income+expense**: Would double-count money movement — rejected per ADR-004 and Finance domain design

## References

- ADR-001: Clean Architecture
- ADR-004: Transaction and Category Data Model
- docs/architecture/collections/Finance.md