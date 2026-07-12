# ADR-002: JWT Authentication

## Status

Accepted

## Date

2026-07-10

---

## Context

WealthPilot AI requires secure authentication for all user-specific financial data. The application is expected to expose REST APIs consumed by a web frontend and, potentially, mobile clients.

A stateless authentication mechanism is preferred to simplify deployment and horizontal scaling.

---

## Decision

The application will use JSON Web Tokens (JWT) for authentication.

Access tokens are issued after successful login and must be included in the `Authorization` header using the Bearer scheme.

Passwords are hashed using Argon2 before storage.

---

## Token Contents

Each access token includes:

* User identifier (`sub`)
* Expiration time (`exp`)

Sensitive user information is never embedded in the token.

---

## Authentication Flow

```text
Register
      │
      ▼
Password Hashing
      │
      ▼
MongoDB

Login
      │
      ▼
Password Verification
      │
      ▼
JWT Generation
      │
      ▼
Client

Authenticated Request
      │
      ▼
JWT Validation
      │
      ▼
Current User
```

---

## Security Decisions

* Passwords are never stored in plain text.
* Argon2 is used for password hashing.
* JWTs are signed using HS256.
* Expired or invalid tokens result in an Unauthorized response.
* Authentication is enforced using FastAPI dependencies.

---

## Consequences

### Advantages

* Stateless authentication
* Scalable across multiple instances
* Widely supported
* Suitable for SPA frontends

### Trade-offs

* Tokens cannot be revoked without additional mechanisms.
* Refresh tokens will be introduced in a future ADR if required.
