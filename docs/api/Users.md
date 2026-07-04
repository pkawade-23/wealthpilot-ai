# Users API

## Purpose

The Users API manages user profile information, preferences, and account settings.

Authentication is handled separately by the Authentication API.

Every endpoint in this document requires authentication.

---

# Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | /api/v1/users/me | Get current user's profile |
| PATCH | /api/v1/users/me | Update profile |
| POST | /api/v1/users/change-password | Change password |
| GET | /api/v1/users/preferences | Get user preferences |
| PATCH | /api/v1/users/preferences | Update user preferences |
| POST | /api/v1/users/avatar | Upload profile picture |
| DELETE | /api/v1/users/avatar | Remove profile picture |
| DELETE | /api/v1/users/me | Deactivate account |

---

# Get Profile

## Endpoint

```
GET /api/v1/users/me
```

## Authentication

Required

## Description

Returns the authenticated user's profile.

## Success Response

```json
{
    "success": true,
    "data": {
        "id": "6868b3f80b17f4450e0c1234",
        "firstName": "Pratik",
        "lastName": "Kawade",
        "email": "pratik@example.com",
        "avatarUrl": null,
        "createdAt": "2026-07-05T10:00:00Z",
        "updatedAt": "2026-07-05T12:15:00Z"
    }
}
```

---

# Update Profile

## Endpoint

```
PATCH /api/v1/users/me
```

## Authentication

Required

## Request

```json
{
    "firstName": "Pratik",
    "lastName": "Kawade"
}
```

## Business Rules

- Email cannot be changed using this endpoint.
- Only supplied fields are updated.
- Empty strings are not allowed.

## Success Response

```json
{
    "success": true,
    "message": "Profile updated successfully."
}
```

---

# Change Password

## Endpoint

```
POST /api/v1/users/change-password
```

## Authentication

Required

## Request

```json
{
    "currentPassword": "OldPassword123!",
    "newPassword": "NewPassword123!"
}
```

## Validation Rules

- Current password must match.
- New password must satisfy password policy.
- New password cannot match the current password.

## Success Response

```json
{
    "success": true,
    "message": "Password changed successfully."
}
```

---

# Get Preferences

## Endpoint

```
GET /api/v1/users/preferences
```

## Authentication

Required

## Description

Returns user-specific application preferences.

## Success Response

```json
{
    "success": true,
    "data": {
        "currency": "INR",
        "locale": "en-IN",
        "timeZone": "Asia/Kolkata",
        "theme": "SYSTEM",
        "dateFormat": "DD-MM-YYYY",
        "numberFormat": "INDIAN"
    }
}
```

---

# Update Preferences

## Endpoint

```
PATCH /api/v1/users/preferences
```

## Authentication

Required

## Request

```json
{
    "currency": "USD",
    "theme": "DARK",
    "timeZone": "America/New_York"
}
```

## Success Response

```json
{
    "success": true,
    "message": "Preferences updated successfully."
}
```

---

# Upload Avatar

## Endpoint

```
POST /api/v1/users/avatar
```

## Authentication

Required

## Content-Type

```
multipart/form-data
```

## Supported Formats

- PNG
- JPG
- JPEG

Maximum size: 5 MB

## Success Response

```json
{
    "success": true,
    "data": {
        "avatarUrl": "/uploads/avatar/user123.jpg"
    }
}
```

---

# Remove Avatar

## Endpoint

```
DELETE /api/v1/users/avatar
```

## Authentication

Required

## Success Response

```json
{
    "success": true,
    "message": "Avatar removed successfully."
}
```

---

# Deactivate Account

## Endpoint

```
DELETE /api/v1/users/me
```

## Authentication

Required

## Description

Deactivates the user's account.

The account is soft-deleted and can be restored by an administrator.

Financial data is preserved for auditability.

## Success Response

```json
{
    "success": true,
    "message": "Account deactivated successfully."
}
```

---

# Validation Rules

- Email addresses remain unique.
- User preferences must contain supported values.
- Uploaded avatars must pass file validation.
- Password changes invalidate existing refresh tokens.

---

# Business Rules

- Users may only modify their own profile.
- Profile updates are audited.
- Deactivated accounts cannot authenticate.
- Financial records remain intact after account deactivation.

---

# Security Considerations

- Authentication is required for every endpoint.
- File uploads are virus scanned before storage.
- Avatar uploads are validated by MIME type and file signature.
- Password changes require re-authentication.

---

# Future Enhancements

Future versions may support:

- Profile verification
- Multiple currencies
- Language selection
- Email change workflow
- Account export (GDPR)
- Account deletion request
- Connected devices
- Activity history