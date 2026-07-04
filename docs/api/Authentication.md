# Authentication API

## Purpose

The Authentication API is responsible for user identity, authentication, authorization, and session management.

It provides secure access to WealthPilot AI using JSON Web Tokens (JWT).

All authenticated API requests require a valid access token.

---

# Authentication Flow

```text
          Register
              │
              ▼
        User Account
              │
              ▼
            Login
              │
              ▼
 Access Token + Refresh Token
              │
              ▼
 Authenticated Requests
              │
              ▼
      Refresh Token
              │
              ▼
     New Access Token
              │
              ▼
           Logout
```

---

# Endpoints

| Method | Endpoint | Description | Authentication |
|----------|----------|-------------|----------------|
| POST | /api/v1/auth/register | Register a new user | Public |
| POST | /api/v1/auth/login | Login | Public |
| POST | /api/v1/auth/refresh | Refresh access token | Refresh Token |
| POST | /api/v1/auth/logout | Logout current session | Required |
| GET | /api/v1/auth/me | Get current user | Required |

---

# Register

## Endpoint

```
POST /api/v1/auth/register
```

## Description

Creates a new WealthPilot AI account.

## Authentication

Not required.

## Request

```json
{
    "firstName": "Pratik",
    "lastName": "Kawade",
    "email": "pratik@example.com",
    "password": "StrongPassword123!"
}
```

## Validation Rules

- First name is required
- Last name is required
- Email must be unique
- Email must be valid
- Password must satisfy password policy

## Success Response

HTTP 201

```json
{
    "success": true,
    "message": "Account created successfully."
}
```

## Errors

- Email already exists
- Invalid email
- Weak password

---

# Login

## Endpoint

```
POST /api/v1/auth/login
```

## Description

Authenticates a user and returns JWT tokens.

## Authentication

Not required.

## Request

```json
{
    "email": "pratik@example.com",
    "password": "StrongPassword123!"
}
```

## Success Response

HTTP 200

```json
{
    "success": true,
    "data": {
        "accessToken": "...",
        "refreshToken": "...",
        "expiresIn": 900,
        "user": {
            "id": "...",
            "firstName": "Pratik",
            "lastName": "Kawade",
            "email": "pratik@example.com"
        }
    }
}
```

## Errors

- Invalid credentials
- User disabled
- Too many failed login attempts

---

# Refresh Token

## Endpoint

```
POST /api/v1/auth/refresh
```

## Description

Issues a new access token using a valid refresh token.

## Request

```json
{
    "refreshToken": "..."
}
```

## Success Response

```json
{
    "success": true,
    "data": {
        "accessToken": "...",
        "expiresIn": 900
    }
}
```

## Errors

- Invalid refresh token
- Expired refresh token
- Revoked refresh token

---

# Logout

## Endpoint

```
POST /api/v1/auth/logout
```

## Authentication

Required.

## Description

Revokes the current refresh token and terminates the active session.

## Success Response

HTTP 200

```json
{
    "success": true,
    "message": "Logged out successfully."
}
```

---

# Current User

## Endpoint

```
GET /api/v1/auth/me
```

## Authentication

Required.

## Description

Returns information about the authenticated user.

## Success Response

```json
{
    "success": true,
    "data": {
        "id": "...",
        "firstName": "Pratik",
        "lastName": "Kawade",
        "email": "pratik@example.com",
        "createdAt": "2026-07-05T10:00:00Z"
    }
}
```

---

# JWT Token Strategy

## Access Token

Purpose

Access protected APIs.

Lifetime

15 minutes

Stored

Frontend memory

---

## Refresh Token

Purpose

Generate new access tokens.

Lifetime

30 days

Stored

HttpOnly Secure Cookie

---

# Password Policy

Passwords must:

- Be at least 8 characters long
- Contain one uppercase letter
- Contain one lowercase letter
- Contain one number
- Contain one special character

---

# Security Features

The authentication system includes:

- BCrypt password hashing
- JWT access tokens
- Refresh token rotation
- HTTPS-only communication
- HttpOnly cookies for refresh tokens
- CSRF protection
- Brute-force protection
- Rate limiting (future enhancement)

---

# Authentication Middleware

Protected endpoints validate:

- JWT signature
- Token expiration
- User existence
- User status

Invalid tokens return HTTP 401 Unauthorized.

---

# Business Rules

- Email addresses must be unique.
- Passwords are never stored in plain text.
- Refresh tokens are invalidated after logout.
- Disabled users cannot authenticate.
- Users may have multiple active sessions.

---

# Future Enhancements

Future versions may support:

- Multi-factor authentication (MFA)
- Passkeys (WebAuthn)
- Social login
- Single Sign-On (SSO)
- Device management
- Login history
- Trusted devices
- Biometric authentication