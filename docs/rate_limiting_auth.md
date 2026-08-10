# Rate Limiting for Authentication Endpoints Documentation (#590)

DevLink **Authentication Rate Limiting** protects user accounts and authorization services from brute-force login attempts, credential stuffing, email enumeration, and MFA code guessing.

---

## 1. Overview & Protected Endpoints

Rate limits are configured globally and on a per-endpoint basis using SlowAPI and remote client IP address keys.

| Category | Endpoint(s) | Default Rate Limit | Config Setting |
|---|---|---|---|
| **Login** | `POST /api/auth/login`<br>`POST /api/v1/auth/login`<br>`POST /api/auth/github`<br>`POST /api/auth/linkedin` | `5/minute` | `LOGIN_RATE_LIMIT` |
| **Signup** | `POST /api/auth/register`<br>`POST /api/v1/auth/register` | `3/hour` | `REGISTER_RATE_LIMIT` |
| **Password Reset** | `POST /api/auth/forgot-password`<br>`GET /api/auth/verify-recovery-token`<br>`POST /api/auth/reset-password` | `3/15minutes` | `PASSWORD_RESET_RATE_LIMIT` |
| **Email Verification** | `POST /api/auth/verify-email`<br>`POST /api/auth/resend-verification` | `5/minute` | `VERIFY_EMAIL_RATE_LIMIT` |
| **MFA / OTP** | `POST /api/auth/mfa/verify-login`<br>`POST /api/auth/mfa/enable`<br>`POST /api/auth/mfa/disable`<br>`POST /api/auth/mfa/setup`<br>`POST /api/auth/mfa/recovery-codes` | `5/minute` | `MFA_RATE_LIMIT` |

---

## 2. Response Standard & HTTP 429

When a client exceeds the allowed rate limit, the API returns **HTTP 429 Too Many Requests** with:
1. `Retry-After: <seconds>` header indicating the duration until requests are permitted again.
2. Standardized JSON error response payload:

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Rate limit exceeded. Please try again later.",
    "details": {
      "retry_after_seconds": 60
    }
  }
}
```

---

## 3. Configuration

Rate limit settings are defined in `app/core/config.py` and can be overridden via environment variables:

```bash
ENABLE_RATE_LIMIT=True
LOGIN_RATE_LIMIT="5/minute"
REGISTER_RATE_LIMIT="3/hour"
PASSWORD_RESET_RATE_LIMIT="3/15minutes"
VERIFY_EMAIL_RATE_LIMIT="5/minute"
MFA_RATE_LIMIT="5/minute"
```

---

## 4. Running Tests

Execute unit tests covering auth rate limit configuration, HTTP 429 responses, and `Retry-After` headers:

```bash
cd backend
./venv/bin/pytest tests/test_rate_limit_auth.py -v
```

Expected output: **4 passed**.
