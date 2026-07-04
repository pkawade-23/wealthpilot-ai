# Identity Collections

## Purpose

The Identity domain manages user authentication, authorization, profile information, user preferences, and active sessions.

These collections are responsible for identifying users and securing access to the WealthPilot AI platform.

---

# Collections

The Identity domain consists of the following collections:

| Collection | Purpose |
|------------|---------|
| users | User profile, authentication details, and preferences |
| sessions | Refresh tokens and active login sessions |

---

# Collection Standards

Unless otherwise specified, all collections in WealthPilot AI follow these conventions.

## Primary Key

Every document uses MongoDB's ObjectId as the primary key.

Example:

```json
"_id": ObjectId(...)
```

---

## Audit Fields

Every mutable document should contain the following audit fields.

| Field | Description |
|--------|-------------|
| createdAt | Date the document was created |
| updatedAt | Date the document was last modified |
| createdBy | User who created the document |
| updatedBy | User who last modified the document |

These fields improve traceability and debugging.

---

## Soft Delete

Collections representing user-managed business data should support soft deletion.

Standard fields include:

```json
"isDeleted": false,
"deletedAt": null,
"deletedBy": null
```

Soft deletes prevent accidental data loss while preserving historical records.

Collections such as `emails` and `audit_logs` are immutable and should not use soft deletion.

---

## Timestamps

All timestamps should be stored in UTC using the ISO 8601 format.

Example:

```text
2026-07-04T10:15:23Z
```

---

## Naming Conventions

Field names follow these rules:

- camelCase
- descriptive names
- avoid abbreviations
- avoid UI-specific terminology

Examples:

- firstName
- lastName
- preferredCurrency
- monthlyIncome

---

## References

Relationships between collections should use ObjectId references.

Example:

```json
"userId": ObjectId(...)
```

Embedding should be used only when the embedded data is tightly coupled and rarely queried independently.

---

## Validation

Application-level validation is performed using Pydantic models in the FastAPI backend.

MongoDB schema validation may be added for critical collections in future releases.

---

## Indexing Principles

Indexes should be created only for fields that are:

- Frequently searched
- Frequently filtered
- Frequently sorted
- Used in relationships
- Required for uniqueness

Over-indexing should be avoided to reduce write overhead.

---

# Users Collection

## Purpose

The `users` collection stores user identity, authentication details, profile information, preferences, and account status.

Each user owns all financial data within WealthPilot AI. Every business entity in the system is associated with exactly one user.

The collection is designed to support secure authentication, personalization, and future expansion without requiring schema redesign.

---

# Responsibilities

The `users` collection is responsible for:

- User registration
- Authentication
- User profile information
- User preferences
- Account status
- Ownership of financial data

It is **not** responsible for storing active sessions or authentication tokens.

---

# Relationships

The `users` collection is the parent entity for most business collections.

```text
users
 │
 ├── sessions
 ├── accounts
 ├── transactions
 ├── transaction_candidates
 ├── emails
 ├── documents
 ├── budgets
 ├── financial_goals
 ├── assets
 ├── liabilities
 ├── ai_conversations
 ├── notifications
 └── audit_logs
```

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| email | String | Yes | Unique email address |
| passwordHash | String | Yes | BCrypt hashed password |
| firstName | String | Yes | User's first name |
| lastName | String | Yes | User's last name |
| preferredCurrency | String | Yes | Default currency (e.g. INR) |
| timezone | String | Yes | User timezone |
| language | String | Yes | Preferred language |
| profilePicture | String | No | Profile image URL |
| accountStatus | Enum | Yes | Current account status |
| emailVerified | Boolean | Yes | Email verification status |
| lastLoginAt | Date | No | Last successful login |
| createdAt | Date | Yes | Creation timestamp |
| updatedAt | Date | Yes | Last update timestamp |
| createdBy | ObjectId | No | Creator reference |
| updatedBy | ObjectId | No | Last updater reference |
| isDeleted | Boolean | Yes | Soft delete flag |
| deletedAt | Date | No | Soft delete timestamp |
| deletedBy | ObjectId | No | User who performed deletion |

---

# Account Status

Supported values:

- ACTIVE
- PENDING_VERIFICATION
- LOCKED
- SUSPENDED
- DELETED

These states determine whether a user can access the application.

---

# Preferences

User preferences are stored directly within the user document.

Example preferences include:

- Preferred currency
- Language
- Timezone

Future versions may include:

- Theme
- Notification preferences
- AI personalization settings

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| email | Unique | Prevent duplicate accounts |
| accountStatus | Index | Administrative queries |
| createdAt | Index | Sorting and reporting |

---

# Validation Rules

- Email must be unique.
- Email must follow RFC-compliant email format.
- Passwords are never stored in plain text.
- Passwords are hashed using BCrypt.
- First and last names cannot be empty.
- Preferred currency must use ISO 4217 currency codes.
- Timezone should use IANA timezone identifiers.
- Language should use ISO language codes.

---

# Security Considerations

Passwords are never stored in plain text.

Authentication uses:

- BCrypt password hashing
- JWT access tokens
- Refresh tokens stored in the `sessions` collection

Sensitive fields should never be returned by public APIs.

Examples:

- passwordHash
- internal audit fields

---

# Example Document

```json
{
  "_id": "ObjectId",
  "email": "pratik@example.com",
  "passwordHash": "$2b$12$...",
  "firstName": "Pratik",
  "lastName": "Kawade",
  "preferredCurrency": "INR",
  "timezone": "Asia/Kolkata",
  "language": "en",
  "profilePicture": null,
  "accountStatus": "ACTIVE",
  "emailVerified": true,
  "lastLoginAt": "2026-07-04T10:15:23Z",
  "createdAt": "2026-06-01T09:00:00Z",
  "updatedAt": "2026-07-04T10:15:23Z",
  "createdBy": null,
  "updatedBy": null,
  "isDeleted": false,
  "deletedAt": null,
  "deletedBy": null
}
```

---

# Future Enhancements

Future versions of the `users` collection may support:

- Multi-factor authentication (MFA)
- Biometric authentication
- OAuth providers (Google, Microsoft, Apple)
- Profile customization
- Multiple currencies
- Localization preferences
- AI personalization settings

# Sessions Collection

## Purpose

The `sessions` collection manages authenticated user sessions and refresh tokens.

It enables secure session management across multiple devices while supporting token rotation, session expiration, and logout functionality.

The collection is designed to improve security by allowing refresh tokens to be revoked independently without affecting the user's account.

---

# Responsibilities

The `sessions` collection is responsible for:

- Storing refresh tokens
- Managing active user sessions
- Supporting multiple concurrent devices
- Session expiration
- Token revocation
- Secure logout

The collection does **not** store access tokens, as JWT access tokens are stateless and short-lived.

---

# Relationships

```text
users
   │
   └──────────────► sessions
```

Each session belongs to exactly one user.

A user may have multiple active sessions.

Examples:

- Laptop
- Mobile App
- Tablet
- Work Computer

---

# Document Schema

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| _id | ObjectId | Yes | Primary key |
| userId | ObjectId | Yes | Reference to users collection |
| refreshTokenHash | String | Yes | Hashed refresh token |
| deviceName | String | No | Device identifier |
| platform | String | No | Operating system or platform |
| browser | String | No | Browser information |
| ipAddress | String | No | Last known IP address |
| userAgent | String | No | Full user agent string |
| expiresAt | Date | Yes | Refresh token expiration |
| lastUsedAt | Date | Yes | Last successful token usage |
| isRevoked | Boolean | Yes | Session revocation status |
| revokedAt | Date | No | Revocation timestamp |
| createdAt | Date | Yes | Session creation time |

---

# Session Lifecycle

```text
User Login
      │
      ▼
Create Session
      │
      ▼
Issue Access Token
      │
      ▼
Issue Refresh Token
      │
      ▼
Authenticated Requests
      │
      ▼
Refresh Token Used
      │
      ▼
Rotate Refresh Token
      │
      ▼
Session Expires / Logout
      │
      ▼
Session Revoked
```

---

# Index Strategy

| Field | Type | Purpose |
|--------|------|---------|
| userId | Index | Retrieve user sessions |
| refreshTokenHash | Unique | Validate refresh token |
| expiresAt | TTL (Optional) | Automatic cleanup of expired sessions |
| isRevoked | Index | Administrative queries |

---

# Validation Rules

- Each session must reference a valid user.
- Refresh tokens are stored only as hashes.
- Expired sessions cannot be reused.
- Revoked sessions cannot be reactivated.
- Token rotation invalidates the previous refresh token.

---

# Security Considerations

The following security practices should be followed:

- Never store refresh tokens in plain text.
- Hash refresh tokens before storing.
- Rotate refresh tokens after every successful refresh.
- Immediately revoke sessions during logout.
- Automatically expire inactive sessions.

The backend should validate every refresh request against the stored session record.

---

# Example Document

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "refreshTokenHash": "$2b$12$...",
  "deviceName": "Pratik's Laptop",
  "platform": "Windows 11",
  "browser": "Chrome",
  "ipAddress": "192.168.1.100",
  "userAgent": "Mozilla/5.0 ...",
  "expiresAt": "2026-08-04T10:15:23Z",
  "lastUsedAt": "2026-07-04T10:15:23Z",
  "isRevoked": false,
  "revokedAt": null,
  "createdAt": "2026-07-04T10:15:23Z"
}
```

---

# Future Enhancements

Future versions may include:

- Device trust management
- Session location history
- Concurrent session limits
- Suspicious login detection
- User-controlled session management
- Device fingerprinting
- Push notification on new login