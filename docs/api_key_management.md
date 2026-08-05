# API Key Management Documentation (#605)

DevLink **API Key Management** allows users and organizations to generate, manage, regenerate, and revoke secure API keys for integrating third-party external tools, bots, and automated services with DevLink.

---

## 1. Security Architecture

- **Token Structure**: API keys follow the format `dlk_live_<32-byte-urlsafe-secret>` (e.g. `dlk_live_x8F2k...`).
- **One-Time Secret Display**: Raw API key secrets are returned **ONLY ONCE** upon creation or secret regeneration.
- **SHA-256 Storage Hashing**: Only cryptographically secure SHA-256 hashes (`hashed_key`) are stored in the database.
- **Last Used Timestamp**: Every authenticated API request updates `last_used_at` automatically.
- **Expiration Enforcement**: Optional `expires_at` / `expires_in_days` expiration timestamps are strictly checked on access.
- **Scope Scoping**: API keys are restricted to configured permissions (`read:projects`, `write:projects`, `read:profile`, `read:organizations`, `full_access`).

---

## 2. API Reference

### 1. Create API Key
`POST /api/v1/api-keys`

**Request Payload:**
```json
{
  "name": "GitHub Actions Integration",
  "scopes": ["read:projects", "write:projects"],
  "expires_in_days": 30
}
```

**Response (Raw key secret shown ONLY ONCE):**
```json
{
  "id": "c1a2b3c4-d5e6-7890-abcd-ef1234567890",
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "GitHub Actions Integration",
  "prefix": "dlk_live_x8F2k",
  "scopes": ["read:projects", "write:projects"],
  "expires_at": "2026-09-03T12:00:00Z",
  "last_used_at": null,
  "is_active": true,
  "created_at": "2026-08-04T12:00:00Z",
  "updated_at": "2026-08-04T12:00:00Z",
  "raw_key": "dlk_live_x8F2k9a3b4c5d6e7f8g9h0i1j2k3l4m5"
}
```

---

### 2. List API Keys
`GET /api/v1/api-keys`

**Query Parameters:** `page` (default 1), `limit` (default 20)

Returns metadata for active and historical API keys (omits raw secret).

---

### 3. Update API Key
`PATCH /api/v1/api-keys/{key_id}`

**Request Payload:**
```json
{
  "name": "Updated Bot Label",
  "scopes": ["read:projects", "read:profile"]
}
```

---

### 4. Regenerate API Key Secret
`POST /api/v1/api-keys/{key_id}/regenerate`

Invalidates the previous key hash, generates a new token secret, resets `last_used_at`, and returns the new `raw_key` secret once.

---

### 5. Revoke API Key
`DELETE /api/v1/api-keys/{key_id}` or `POST /api/v1/api-keys/{key_id}/revoke`

Immediately deactivates the key (`is_active = false`), blocking all future authentication attempts.

---

### 6. Organization API Keys
- `POST /api/v1/organizations/{organization_id}/api-keys`
- `GET /api/v1/organizations/{organization_id}/api-keys`

---

## 3. Authenticating API Requests

External tools can authenticate requests by sending either header:

1. **`X-API-Key` Header**:
   ```http
   GET /api/v1/projects HTTP/1.1
   Host: api.devlink.com
   X-API-Key: dlk_live_x8F2k9a3b4c5d6e7f8g9h0i1j2k3l4m5
   ```

2. **`Authorization: Bearer` Header**:
   ```http
   GET /api/v1/projects HTTP/1.1
   Host: api.devlink.com
   Authorization: Bearer dlk_live_x8F2k9a3b4c5d6e7f8g9h0i1j2k3l4m5
   ```

---

## 4. Running Tests

Execute backend unit and integration tests:
```bash
cd backend
./venv/bin/pytest tests/test_api_key_management.py -v
```

Expected output: **8 passed**.
