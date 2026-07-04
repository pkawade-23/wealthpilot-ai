# AI Domain

## Purpose

The AI Domain contains all collections required to power the artificial intelligence capabilities of WealthPilot AI.

Unlike the Finance Domain, which stores verified financial records, the AI Domain stores AI-generated knowledge, conversations, retrieval context, recommendations, and model metadata.

The AI Domain enables:

- Conversational financial assistance
- AI-powered financial insights
- Retrieval-Augmented Generation (RAG)
- Personalized recommendations
- Scenario simulations
- AI reasoning history
- Model evaluation and improvement

The collections in this domain do not replace financial records.

Instead, they enhance the user experience by providing intelligent analysis based on verified financial data.

---

# Collections

The AI Domain consists of the following collections.

| Collection | Purpose |
|------------|---------|
| conversations | Chat sessions between the user and AI |
| messages | Individual conversation messages |
| insights | AI-generated financial insights |
| recommendations | Personalized AI recommendations |
| scenarios | What-if financial simulations |
| embeddings (ChromaDB) | Vector embeddings used for RAG |
| prompt_logs | AI prompt and response history |
| model_versions | AI model configuration and version history |

---

# Design Principles

## AI Never Owns Financial Data

Financial truth always resides in the Finance Domain.

AI only analyzes verified financial information.

---

## Explainability

Every AI recommendation should be traceable to the financial data that influenced it.

Users should understand why a recommendation was made.

---

## Human Control

AI recommendations are advisory.

The user always makes the final financial decision.

---

## Retrieval-Augmented Generation

Large Language Models should receive only the relevant financial context.

The AI Domain stores vector embeddings and retrieval metadata to support efficient semantic search.

---

## Privacy First

Financial data remains local whenever possible.

Ollama executes AI models locally.

Only embeddings and metadata required for retrieval are stored.

---

## Reproducibility

Important AI interactions should be reproducible.

Prompt templates, model versions, and retrieved context may be stored for debugging and evaluation.

---

## Continuous Improvement

The AI architecture supports future model upgrades without requiring changes to the Finance Domain.

# Conversations Collection

## Purpose

The `conversations` collection represents AI chat sessions between a user and WealthPilot AI.

A conversation serves as a logical container for a sequence of messages, preserving context across multiple interactions.

The collection stores conversation metadata only.

Individual messages are stored separately in the `messages` collection.

---

# Responsibilities

The `conversations` collection is responsible for:

- Managing AI chat sessions
- Organizing message history
- Supporting conversation search
- Maintaining conversation metadata
- Providing context for AI interactions

---

# Relationships

```text
users
   │
   ▼
conversations
   │
   ▼
messages
```

One user may have many conversations.

Each conversation contains multiple messages.

---

# Conversation Types

Supported values:

- GENERAL
- FINANCIAL_ANALYSIS
- BUDGETING
- GOAL_PLANNING
- INVESTMENT
- DEBT_MANAGEMENT
- SCENARIO_SIMULATION

Future versions may introduce additional specialized conversation types.

---

# Conversation Status

Supported values:

- ACTIVE
- ARCHIVED
- DELETED

Deleted conversations are soft-deleted to preserve auditability.

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Conversation owner |
| title | String | Yes | Conversation title |
| conversationType | Enum | Yes | Type of conversation |
| status | Enum | Yes | Conversation status |
| lastMessageAt | Date | Yes | Timestamp of latest message |
| messageCount | Number | Yes | Cached number of messages |
| pinned | Boolean | Yes | Whether conversation is pinned |
| createdAt | Date | Yes | Creation timestamp |
| updatedAt | Date | Yes | Last modification timestamp |

---

# Title Generation

Conversation titles may be:

Manual

Example:

"July Budget Planning"

or AI Generated

Example:

"How to Reduce Grocery Expenses"

The title may be regenerated until the conversation is pinned.

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve user conversations |
| lastMessageAt | Index | Recent conversations |
| status | Index | Active conversations |
| conversationType | Index | Filtering |

---

# Validation Rules

- Every conversation belongs to exactly one user.
- Title cannot be empty.
- Message count cannot be negative.
- Only active conversations may receive new messages.

---

# Security Considerations

- Users may access only their own conversations.
- Conversation deletion should use soft delete.
- Sensitive financial discussions must remain private.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "title": "Reduce Monthly Expenses",
  "conversationType": "FINANCIAL_ANALYSIS",
  "status": "ACTIVE",
  "lastMessageAt": "2026-07-04T16:45:00Z",
  "messageCount": 18,
  "pinned": false,
  "createdAt": "2026-07-04T16:20:00Z",
  "updatedAt": "2026-07-04T16:45:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Conversation folders
- Favorites
- Conversation sharing
- AI-generated summaries
- Conversation export
- Automatic archival

# Conversations Collection

## Purpose

The `conversations` collection represents AI chat sessions between a user and WealthPilot AI.

A conversation serves as a logical container for a sequence of messages, preserving context across multiple interactions.

The collection stores conversation metadata only.

Individual messages are stored separately in the `messages` collection.

---

# Responsibilities

The `conversations` collection is responsible for:

- Managing AI chat sessions
- Organizing message history
- Supporting conversation search
- Maintaining conversation metadata
- Providing context for AI interactions

---

# Relationships

```text
users
   │
   ▼
conversations
   │
   ▼
messages
```

One user may have many conversations.

Each conversation contains multiple messages.

---

# Conversation Types

Supported values:

- GENERAL
- FINANCIAL_ANALYSIS
- BUDGETING
- GOAL_PLANNING
- INVESTMENT
- DEBT_MANAGEMENT
- SCENARIO_SIMULATION

Future versions may introduce additional specialized conversation types.

---

# Conversation Status

Supported values:

- ACTIVE
- ARCHIVED
- DELETED

Deleted conversations are soft-deleted to preserve auditability.

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Conversation owner |
| title | String | Yes | Conversation title |
| conversationType | Enum | Yes | Type of conversation |
| status | Enum | Yes | Conversation status |
| lastMessageAt | Date | Yes | Timestamp of latest message |
| messageCount | Number | Yes | Cached number of messages |
| pinned | Boolean | Yes | Whether conversation is pinned |
| createdAt | Date | Yes | Creation timestamp |
| updatedAt | Date | Yes | Last modification timestamp |

---

# Title Generation

Conversation titles may be:

Manual

Example:

"July Budget Planning"

or AI Generated

Example:

"How to Reduce Grocery Expenses"

The title may be regenerated until the conversation is pinned.

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve user conversations |
| lastMessageAt | Index | Recent conversations |
| status | Index | Active conversations |
| conversationType | Index | Filtering |

---

# Validation Rules

- Every conversation belongs to exactly one user.
- Title cannot be empty.
- Message count cannot be negative.
- Only active conversations may receive new messages.

---

# Security Considerations

- Users may access only their own conversations.
- Conversation deletion should use soft delete.
- Sensitive financial discussions must remain private.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "title": "Reduce Monthly Expenses",
  "conversationType": "FINANCIAL_ANALYSIS",
  "status": "ACTIVE",
  "lastMessageAt": "2026-07-04T16:45:00Z",
  "messageCount": 18,
  "pinned": false,
  "createdAt": "2026-07-04T16:20:00Z",
  "updatedAt": "2026-07-04T16:45:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Conversation folders
- Favorites
- Conversation sharing
- AI-generated summaries
- Conversation export
- Automatic archival

# Messages Collection

## Purpose

The `messages` collection stores the individual messages exchanged between the user and WealthPilot AI.

Each message represents a single interaction within a conversation.

In addition to message content, the collection stores AI execution metadata, Retrieval-Augmented Generation (RAG) information, performance metrics, and model details.

This enables reproducibility, debugging, monitoring, and continuous improvement of the AI system.

---

# Responsibilities

The `messages` collection is responsible for:

- Storing user and AI messages
- Maintaining conversation history
- Recording AI execution metadata
- Tracking RAG retrieval information
- Measuring AI performance
- Supporting future model evaluation

---

# Relationships

```text
users
   │
   ▼
conversations
   │
   ▼
messages
```

Each message belongs to exactly one conversation.

One conversation contains many messages.

---

# Message Types

Supported values:

- USER
- ASSISTANT
- SYSTEM

---

# Message Status

Supported values:

- SENT
- PROCESSING
- COMPLETED
- FAILED

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| conversationId | ObjectId | Yes | Parent conversation |
| userId | ObjectId | Yes | Owner of the conversation |
| messageType | Enum | Yes | USER, ASSISTANT or SYSTEM |
| content | String | Yes | Message text |
| modelName | String | No | AI model used |
| promptTokens | Number | No | Prompt token count |
| completionTokens | Number | No | Response token count |
| totalTokens | Number | No | Total tokens |
| responseTimeMs | Number | No | AI response latency |
| ragEnabled | Boolean | Yes | Whether RAG was used |
| ragDocuments | Array | No | Retrieved document references |
| toolCalls | Array | No | Tools invoked during response generation |
| attachments | Array | No | Uploaded files/images |
| status | Enum | Yes | Message status |
| createdAt | Date | Yes | Creation timestamp |

---

# Retrieval-Augmented Generation (RAG)

When RAG is enabled, the message stores references to retrieved knowledge.

Example:

```json
[
  {
    "sourceType": "transaction",
    "sourceId": "ObjectId",
    "similarityScore": 0.94
  },
  {
    "sourceType": "document",
    "sourceId": "ObjectId",
    "similarityScore": 0.91
  }
]
```

The actual embeddings remain in ChromaDB.

MongoDB stores only references.

---

# Tool Calls

The AI may invoke backend tools while generating responses.

Examples:

- Fetch monthly spending
- Calculate net worth
- Search transactions
- Run financial simulation

Example:

```json
[
  {
    "tool": "calculate_net_worth",
    "durationMs": 42,
    "status": "SUCCESS"
  }
]
```

---

# Attachments

Messages may include uploaded files.

Supported examples:

- PDF
- Receipt
- Invoice
- Image

Only metadata is stored.

Files remain in storage.

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| conversationId | Index | Conversation history |
| userId | Index | User messages |
| messageType | Index | Filtering |
| createdAt | Index | Chronological order |

---

# Validation Rules

- Every message belongs to one conversation.
- Content cannot be empty.
- AI metadata exists only for assistant messages.
- User messages do not contain token statistics.
- RAG references must point to existing entities.

---

# Security Considerations

- Users may access only their own messages.
- AI metadata should not expose internal system details.
- Uploaded files must undergo validation before processing.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "conversationId": "ObjectId",
  "userId": "ObjectId",
  "messageType": "ASSISTANT",
  "content": "You spent ₹42,380 in June, which is 12% lower than May.",
  "modelName": "llama3.1:8b",
  "promptTokens": 1450,
  "completionTokens": 210,
  "totalTokens": 1660,
  "responseTimeMs": 1832,
  "ragEnabled": true,
  "ragDocuments": [
    {
      "sourceType": "transaction",
      "sourceId": "ObjectId",
      "similarityScore": 0.96
    }
  ],
  "toolCalls": [
    {
      "tool": "calculate_monthly_spending",
      "durationMs": 38,
      "status": "SUCCESS"
    }
  ],
  "attachments": [],
  "status": "COMPLETED",
  "createdAt": "2026-07-04T17:20:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Message editing
- Streaming responses
- Voice messages
- Multi-modal AI
- Message reactions
- AI citations
- Conversation branching
- Token cost analytics

# Recommendations Collection

## Purpose

The `recommendations` collection stores AI-generated financial suggestions that help users improve their financial health.

Recommendations are actionable.

Unlike insights, recommendations suggest one or more actions that the user can take based on their financial data.

Recommendations power:

- Dashboard recommendations
- AI chat responses
- Financial planning
- Goal optimization
- Budget coaching
- Debt reduction strategies

Recommendations never modify financial data automatically.

The user always decides whether to accept or ignore a recommendation.

---

# Responsibilities

The `recommendations` collection is responsible for:

- Suggesting financial improvements
- Prioritizing actions
- Estimating financial impact
- Tracking recommendation lifecycle
- Supporting AI coaching

---

# Relationships

```text
users
   │
   ▼
recommendations
   │
   ├────────► insights
   ├────────► transactions
   ├────────► budgets
   ├────────► financial_goals
   ├────────► liabilities
   └────────► accounts
```

A recommendation may be generated from one or more insights.

---

# Recommendation Types

Supported values:

- REDUCE_EXPENSES
- INCREASE_SAVINGS
- PAY_OFF_DEBT
- INCREASE_INVESTMENT
- ADJUST_BUDGET
- BUILD_EMERGENCY_FUND
- OPTIMIZE_CASH_FLOW
- GOAL_ACCELERATION
- CUSTOM

---

# Priority

Supported values:

- LOW
- MEDIUM
- HIGH
- CRITICAL

Higher priority recommendations should appear first on the dashboard.

---

# Recommendation Status

Supported values:

- ACTIVE
- ACCEPTED
- DISMISSED
- EXPIRED

Accepted recommendations remain in history for future analysis.

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Recommendation owner |
| insightId | ObjectId | No | Source insight |
| title | String | Yes | Recommendation title |
| description | String | Yes | Detailed explanation |
| recommendationType | Enum | Yes | Recommendation category |
| priority | Enum | Yes | Importance level |
| status | Enum | Yes | Current lifecycle state |
| confidenceScore | Number | Yes | AI confidence (0-1) |
| estimatedImpact | Object | No | Expected financial benefit |
| relatedEntities | Object | No | Referenced financial entities |
| generatedAt | Date | Yes | Generation timestamp |
| expiresAt | Date | No | Expiration timestamp |
| modelVersion | String | Yes | AI model version |
| createdAt | Date | Yes | Creation timestamp |

---

# Estimated Impact

Recommendations may estimate their financial benefit.

Example:

```json
{
    "monthlySavings": 2500,
    "annualSavings": 30000,
    "interestSaved": 850000,
    "goalCompletionMonthsReduced": 8
}
```

These values are estimates generated by the AI and should be clearly identified as projections.

---

# Related Entities

Recommendations may reference multiple financial objects.

Example:

```json
{
    "accounts": [
        "ObjectId"
    ],
    "budgets": [
        "ObjectId"
    ],
    "liabilities": [
        "ObjectId"
    ]
}
```

---

# Recommendation Lifecycle

```text
GENERATED

↓

ACTIVE

↓

┌──────────────┬──────────────┐
│              │              │
▼              ▼              ▼
ACCEPTED   DISMISSED     EXPIRED
```

Accepted recommendations may later be used to measure user engagement and AI effectiveness.

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve recommendations |
| recommendationType | Index | Filtering |
| priority | Index | Dashboard ordering |
| status | Index | Active recommendations |
| generatedAt | Index | Historical reports |

---

# Validation Rules

- Every recommendation belongs to exactly one user.
- Confidence score must be between 0 and 1.
- Title cannot be empty.
- Expiration date must be after generation date.

---

# Security Considerations

- Recommendations are advisory only.
- AI should never automatically execute financial actions.
- Recommendations must remain explainable and traceable.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "insightId": "ObjectId",
  "title": "Make a ₹50,000 home loan part-payment",
  "description": "Making a ₹50,000 part-payment this month could reduce your loan tenure by approximately 7 months and save around ₹8.4 lakh in interest.",
  "recommendationType": "PAY_OFF_DEBT",
  "priority": "HIGH",
  "status": "ACTIVE",
  "confidenceScore": 0.94,
  "estimatedImpact": {
    "interestSaved": 840000,
    "loanTenureReducedMonths": 7
  },
  "relatedEntities": {
    "liabilities": [
      "ObjectId"
    ]
  },
  "generatedAt": "2026-07-04T18:45:00Z",
  "modelVersion": "llama3.1:8b",
  "createdAt": "2026-07-04T18:45:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Recommendation feedback ("Useful" / "Not Useful")
- AI learning from accepted recommendations
- Scheduled recommendation reviews
- Personalized recommendation ranking
- Recommendation bundles
- Financial advisor review workflow
- Goal-aware recommendations

# Recommendations Collection

## Purpose

The `recommendations` collection stores AI-generated financial suggestions that help users improve their financial health.

Recommendations are actionable.

Unlike insights, recommendations suggest one or more actions that the user can take based on their financial data.

Recommendations power:

- Dashboard recommendations
- AI chat responses
- Financial planning
- Goal optimization
- Budget coaching
- Debt reduction strategies

Recommendations never modify financial data automatically.

The user always decides whether to accept or ignore a recommendation.

---

# Responsibilities

The `recommendations` collection is responsible for:

- Suggesting financial improvements
- Prioritizing actions
- Estimating financial impact
- Tracking recommendation lifecycle
- Supporting AI coaching

---

# Relationships

```text
users
   │
   ▼
recommendations
   │
   ├────────► insights
   ├────────► transactions
   ├────────► budgets
   ├────────► financial_goals
   ├────────► liabilities
   └────────► accounts
```

A recommendation may be generated from one or more insights.

---

# Recommendation Types

Supported values:

- REDUCE_EXPENSES
- INCREASE_SAVINGS
- PAY_OFF_DEBT
- INCREASE_INVESTMENT
- ADJUST_BUDGET
- BUILD_EMERGENCY_FUND
- OPTIMIZE_CASH_FLOW
- GOAL_ACCELERATION
- CUSTOM

---

# Priority

Supported values:

- LOW
- MEDIUM
- HIGH
- CRITICAL

Higher priority recommendations should appear first on the dashboard.

---

# Recommendation Status

Supported values:

- ACTIVE
- ACCEPTED
- DISMISSED
- EXPIRED

Accepted recommendations remain in history for future analysis.

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Recommendation owner |
| insightId | ObjectId | No | Source insight |
| title | String | Yes | Recommendation title |
| description | String | Yes | Detailed explanation |
| recommendationType | Enum | Yes | Recommendation category |
| priority | Enum | Yes | Importance level |
| status | Enum | Yes | Current lifecycle state |
| confidenceScore | Number | Yes | AI confidence (0-1) |
| estimatedImpact | Object | No | Expected financial benefit |
| relatedEntities | Object | No | Referenced financial entities |
| generatedAt | Date | Yes | Generation timestamp |
| expiresAt | Date | No | Expiration timestamp |
| modelVersion | String | Yes | AI model version |
| createdAt | Date | Yes | Creation timestamp |

---

# Estimated Impact

Recommendations may estimate their financial benefit.

Example:

```json
{
    "monthlySavings": 2500,
    "annualSavings": 30000,
    "interestSaved": 850000,
    "goalCompletionMonthsReduced": 8
}
```

These values are estimates generated by the AI and should be clearly identified as projections.

---

# Related Entities

Recommendations may reference multiple financial objects.

Example:

```json
{
    "accounts": [
        "ObjectId"
    ],
    "budgets": [
        "ObjectId"
    ],
    "liabilities": [
        "ObjectId"
    ]
}
```

---

# Recommendation Lifecycle

```text
GENERATED

↓

ACTIVE

↓

┌──────────────┬──────────────┐
│              │              │
▼              ▼              ▼
ACCEPTED   DISMISSED     EXPIRED
```

Accepted recommendations may later be used to measure user engagement and AI effectiveness.

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve recommendations |
| recommendationType | Index | Filtering |
| priority | Index | Dashboard ordering |
| status | Index | Active recommendations |
| generatedAt | Index | Historical reports |

---

# Validation Rules

- Every recommendation belongs to exactly one user.
- Confidence score must be between 0 and 1.
- Title cannot be empty.
- Expiration date must be after generation date.

---

# Security Considerations

- Recommendations are advisory only.
- AI should never automatically execute financial actions.
- Recommendations must remain explainable and traceable.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "insightId": "ObjectId",
  "title": "Make a ₹50,000 home loan part-payment",
  "description": "Making a ₹50,000 part-payment this month could reduce your loan tenure by approximately 7 months and save around ₹8.4 lakh in interest.",
  "recommendationType": "PAY_OFF_DEBT",
  "priority": "HIGH",
  "status": "ACTIVE",
  "confidenceScore": 0.94,
  "estimatedImpact": {
    "interestSaved": 840000,
    "loanTenureReducedMonths": 7
  },
  "relatedEntities": {
    "liabilities": [
      "ObjectId"
    ]
  },
  "generatedAt": "2026-07-04T18:45:00Z",
  "modelVersion": "llama3.1:8b",
  "createdAt": "2026-07-04T18:45:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Recommendation feedback ("Useful" / "Not Useful")
- AI learning from accepted recommendations
- Scheduled recommendation reviews
- Personalized recommendation ranking
- Recommendation bundles
- Financial advisor review workflow
- Goal-aware recommendations

# Scenarios Collection

## Purpose

The `scenarios` collection stores AI-generated financial simulations based on hypothetical user inputs.

Scenarios allow users to safely explore financial decisions without affecting their actual financial records.

Examples include:

- Increasing monthly SIP
- Making a loan part-payment
- Purchasing a new vehicle
- Increasing salary
- Changing monthly expenses
- Delaying retirement
- Buying a house

Scenario results are informational only and never modify production financial data.

---

# Responsibilities

The `scenarios` collection is responsible for:

- Running financial simulations
- Comparing current and projected outcomes
- Supporting AI planning
- Saving simulation history
- Enabling side-by-side scenario comparisons

---

# Relationships

```text
users
   │
   ▼
scenarios
   │
   ├────────► transactions
   ├────────► budgets
   ├────────► goals
   ├────────► assets
   ├────────► liabilities
   └────────► recommendations
```

Scenarios may reference multiple financial entities.

No financial records are modified.

---

# Scenario Types

Supported values:

- SIP_INCREASE
- SIP_DECREASE
- LOAN_PREPAYMENT
- EXPENSE_REDUCTION
- SALARY_INCREASE
- RETIREMENT_PLANNING
- HOME_PURCHASE
- VEHICLE_PURCHASE
- GOAL_ACCELERATION
- CUSTOM

---

# Scenario Status

Supported values:

- DRAFT
- COMPLETED
- ARCHIVED

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Scenario owner |
| title | String | Yes | Scenario title |
| scenarioType | Enum | Yes | Type of simulation |
| description | String | No | User description |
| assumptions | Object | Yes | Simulation assumptions |
| currentState | Object | Yes | Snapshot before simulation |
| projectedState | Object | Yes | Predicted outcome |
| summary | String | Yes | AI-generated summary |
| confidenceScore | Number | Yes | Confidence (0-1) |
| relatedEntities | Object | No | Referenced financial entities |
| createdAt | Date | Yes | Creation timestamp |
| updatedAt | Date | Yes | Last modification timestamp |

---

# Assumptions

Every simulation records its assumptions.

Example:

```json
{
    "monthlySipIncrease": 5000,
    "expectedReturn": 12,
    "inflation": 6,
    "salaryGrowth": 8
}
```

This ensures simulations remain reproducible.

---

# Current State

Represents the user's financial position when the simulation was created.

Example:

```json
{
    "netWorth": 4800000,
    "monthlyIncome": 180000,
    "monthlyExpenses": 92000,
    "loanOutstanding": 4825000
}
```

---

# Projected State

Represents the expected outcome after applying the scenario.

Example:

```json
{
    "projectedNetWorth": 7200000,
    "goalCompletionMonthsReduced": 14,
    "loanInterestSaved": 840000
}
```

---

# Scenario Lifecycle

```text
CREATED

↓

RUNNING

↓

COMPLETED

↓

ARCHIVED
```

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve scenarios |
| scenarioType | Index | Filtering |
| createdAt | Index | Historical simulations |

---

# Validation Rules

- Every scenario belongs to one user.
- Confidence score must be between 0 and 1.
- Current state cannot be modified after completion.
- Scenario assumptions are immutable after execution.

---

# Security Considerations

- Simulations never modify financial data.
- Users may only access their own scenarios.
- AI projections should clearly indicate uncertainty.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "title": "Increase SIP by ₹5,000",
  "scenarioType": "SIP_INCREASE",
  "description": "Evaluate the impact of increasing monthly SIP.",
  "assumptions": {
    "monthlySipIncrease": 5000,
    "expectedReturn": 12,
    "inflation": 6,
    "salaryGrowth": 8
  },
  "currentState": {
    "netWorth": 4800000,
    "monthlyIncome": 180000,
    "monthlyExpenses": 92000
  },
  "projectedState": {
    "projectedNetWorth": 7600000,
    "goalCompletionMonthsReduced": 16
  },
  "summary": "Increasing your SIP by ₹5,000 per month could help you reach your retirement goal approximately 16 months earlier.",
  "confidenceScore": 0.92,
  "relatedEntities": {
    "financialGoals": [
      "ObjectId"
    ]
  },
  "createdAt": "2026-07-04T19:30:00Z",
  "updatedAt": "2026-07-04T19:30:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Compare multiple scenarios
- Monte Carlo simulations
- Inflation-adjusted forecasting
- Tax-aware planning
- Investment risk analysis
- AI scenario recommendations
- Shareable scenario reports
- Interactive scenario editing

# Model Versions Collection

## Purpose

The `model_versions` collection maintains a registry of all AI models used by WealthPilot AI.

It enables model governance, reproducibility, performance comparison, and safe deployment of new models.

Rather than hardcoding model information throughout the application, all supported AI models are registered here.

---

# Responsibilities

The `model_versions` collection is responsible for:

- Tracking available AI models
- Recording model configurations
- Supporting model upgrades
- Enabling A/B testing
- Maintaining reproducibility
- Monitoring model lifecycle

---

# Relationships

```text
model_versions
      │
      ├────────► messages
      ├────────► insights
      ├────────► recommendations
      ├────────► scenarios
      └────────► prompt_logs
```

Multiple AI artifacts may reference the same model version.

---

# Model Providers

Supported values:

- Ollama
- OpenAI
- Anthropic
- Azure OpenAI
- Google Gemini
- Custom

---

# Model Status

Supported values:

- ACTIVE
- DEPRECATED
- EXPERIMENTAL
- DISABLED

Only ACTIVE models are available for production inference.

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| modelName | String | Yes | Model identifier |
| provider | Enum | Yes | AI provider |
| version | String | Yes | Model version |
| displayName | String | Yes | Friendly name |
| description | String | No | Model description |
| contextWindow | Number | Yes | Maximum context tokens |
| supportsToolCalling | Boolean | Yes | Tool calling support |
| supportsVision | Boolean | Yes | Image understanding support |
| supportsStreaming | Boolean | Yes | Streaming responses |
| defaultTemperature | Number | Yes | Default sampling temperature |
| embeddingModel | String | No | Associated embedding model |
| status | Enum | Yes | Lifecycle status |
| releasedAt | Date | No | Release date |
| createdAt | Date | Yes | Registration timestamp |
| updatedAt | Date | Yes | Last update timestamp |

---

# Model Lifecycle

```text
Experimental

↓

Testing

↓

Active

↓

Deprecated

↓

Disabled
```

Deprecated models remain available for historical traceability.

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| modelName | Index | Model lookup |
| provider | Index | Provider filtering |
| status | Index | Active model queries |
| version | Index | Version lookup |

---

# Validation Rules

- Model name must be unique within a provider.
- Context window must be greater than zero.
- Temperature must be between 0 and 2.
- Deprecated models cannot become active without a new deployment.

---

# Security Considerations

- Only administrators may register or modify models.
- Historical model configurations should never be deleted.
- Production systems should reference ACTIVE models only.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "modelName": "llama3.1:8b",
  "provider": "Ollama",
  "version": "3.1.0",
  "displayName": "Llama 3.1 8B",
  "description": "Primary conversational model",
  "contextWindow": 128000,
  "supportsToolCalling": true,
  "supportsVision": false,
  "supportsStreaming": true,
  "defaultTemperature": 0.2,
  "embeddingModel": "nomic-embed-text",
  "status": "ACTIVE",
  "releasedAt": "2026-06-15T00:00:00Z",
  "createdAt": "2026-07-04T20:45:00Z",
  "updatedAt": "2026-07-04T20:45:00Z"
}
```

---

# Future Enhancements

Future versions may support:

- Model benchmarking
- Cost per million tokens
- Latency metrics
- Accuracy evaluations
- Automatic model selection
- Canary deployments
- Rollback support
- Multi-model routing