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

---

# Embedding Sources

The following information may be converted into embeddings.

| Source | Embedded |
|----------|----------|
| Emails | Yes |
| Documents | Yes |
| Transactions | Yes |
| Categories | Optional |
| Budgets | Optional |
| Financial Goals | Yes |
| AI Insights | Yes |
| Recommendations | Yes |

Only information that improves semantic retrieval should be embedded.

Structured numerical data continues to reside in MongoDB.

---

# Embedding Pipeline

Every supported document passes through the same processing pipeline.

```text
Document

↓

Text Extraction

↓

Cleaning

↓

Chunking

↓

Embedding Generation

↓

ChromaDB Storage
```

The embedding pipeline runs after successful document ingestion and AI extraction.

Embeddings may be regenerated whenever the embedding model changes.

---

# Chunking Strategy

Documents are divided into smaller chunks before embedding.

Benefits include:

- Improved retrieval accuracy
- Lower token usage
- Better semantic similarity
- Reduced hallucinations

Recommended defaults:

Chunk Size

500 tokens

Chunk Overlap

75 tokens

Each chunk stores:

- Chunk ID
- Parent document ID
- Chunk index
- Source type
- Original text
- Embedding vector

Chunks remain linked to their original source document.

---

# ChromaDB Collection

Each vector record contains:

| Field | Description |
|--------|-------------|
| id | Unique chunk identifier |
| embedding | Vector embedding |
| document | Original chunk text |
| metadata.sourceType | Email, Document, Transaction |
| metadata.sourceId | MongoDB ObjectId |
| metadata.chunkIndex | Chunk order |
| metadata.userId | Owner |
| metadata.createdAt | Timestamp |

Example metadata:

```json
{
  "sourceType": "email",
  "sourceId": "ObjectId",
  "chunkIndex": 3,
  "userId": "ObjectId"
}
```

---

# Retrieval Pipeline

Every AI request follows the same retrieval workflow.

```text
User Question

↓

Generate Query Embedding

↓

Semantic Search

↓

Top K Results

↓

Metadata Filtering

↓

Prompt Builder

↓

LLM

↓

AI Response
```

Typical configuration:

Top K

5

Similarity Metric

Cosine Similarity

Minimum Similarity

0.80

---

# Prompt Assembly

LangChain constructs prompts using multiple information sources.

```text
System Prompt

+

Conversation Memory

+

Retrieved Documents

+

Financial Context

+

User Question

↓

Final Prompt

↓

Ollama
```

Only the most relevant context should be included to optimize token usage and response quality.

---

# End-to-End RAG Flow

```text
User

↓

FastAPI

↓

AI Gateway

↓

Conversation Service

↓

Context Builder

↓

Embedding Generator

↓

ChromaDB Search

↓

Top K Chunks

↓

Prompt Builder

↓

LangChain

↓

Ollama

↓

AI Response

↓

MongoDB
```