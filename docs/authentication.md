# API Authentication Guide

## Overview

DevLink uses JSON Web Tokens (JWT) to authenticate users and secure protected API endpoints. After a successful login, the backend generates a signed JWT that must be included in requests requiring authentication.

---

## Authentication Workflow

1. User submits valid login credentials.
2. The backend verifies the credentials.
3. A JWT access token is generated.
4. The client stores the token securely.
5. The token is sent with every request to protected endpoints using the `Authorization` header.
6. The backend validates the token before processing the request.

---

## JWT Authentication

The application uses JWT tokens signed with the configured `SECRET_KEY` and the algorithm defined by `JWT_ALGORITHM` (default: `HS256`).

Keep the following in mind:

- Never expose your JWT token publicly.
- Do not commit tokens to version control.
- Use a strong `SECRET_KEY` in production.
- Replace expired tokens by logging in again or using the project's refresh mechanism (if enabled).

---

## Public Endpoints

These endpoints generally do not require authentication.

- Landing page
- Login
- Registration
- Public project browsing
- Public developer profiles

---

## Protected Endpoints

These endpoints require a valid JWT token.

- User profile
- Project management
- Team applications
- Messaging
- Notifications
- Bookmark management

---

## Authorization Header

Include the JWT token using the `Bearer` scheme.

```http
Authorization: Bearer <your_jwt_token>
```

---

## Example Request

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
http://localhost:8000/api/v1/protected-endpoint
```

---

## Common Authentication Errors

### 401 Unauthorized

- Missing token
- Expired token
- Invalid token

### 403 Forbidden

The authenticated user does not have permission to access the requested resource.

---

## Best Practices

- Store JWT tokens securely.
- Never hardcode tokens in source code.
- Keep `SECRET_KEY` private.
- Use HTTPS in production environments.
- Regularly rotate secrets and credentials.