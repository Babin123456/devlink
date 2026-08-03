# Security Audit Dashboard — DevLink Admin (#622)

A role-restricted administrative dashboard for reviewing platform security events,
identifying suspicious activity, and exporting audit records.

---

## Access Control

All endpoints require `system_role == "admin"` or `role == "admin"`.
Non-admin requests receive **HTTP 403 Forbidden**.

---

## API Reference

Base path: `/api/v1/admin/security`

### Overview

| Method | Path | Description |
|---|---|---|
| `GET` | `/summary` | Aggregated counters (24 h & 7 d windows) |
| `GET` | `/failed-logins` | Failed login attempt events |
| `GET` | `/failed-logins/export` | Download as CSV |
| `GET` | `/blocked-ips` | IPs with ≥ N failed logins |
| `GET` | `/suspicious-sessions` | Suspicious session events |
| `GET` | `/suspicious-sessions/export` | Download as CSV |
| `GET` | `/password-resets` | Password reset events |
| `GET` | `/password-resets/export` | Download as CSV |
| `GET` | `/api-abuse` | Failed API access events |
| `GET` | `/api-abuse/export` | Download as CSV |
| `GET` | `/alerts` | High-severity security alerts |
| `GET` | `/alerts/export` | Download as CSV |
| `GET` | `/search` | Full-text search across all security events |

---

## Dashboard Sections

### 1. Summary (`GET /summary`)

Returns a `SecurityDashboardSummary` with:

```json
{
  "failed_logins_24h": 42,
  "failed_logins_7d": 310,
  "suspicious_sessions_24h": 3,
  "password_resets_24h": 7,
  "api_abuse_events_24h": 18,
  "total_security_alerts_24h": 55,
  "blocked_ips": ["5.5.5.5", "10.0.0.1"],
  "top_threat_ips": [
    {"ip": "5.5.5.5", "count": 87},
    {"ip": "10.0.0.1", "count": 34}
  ]
}
```

---

### 2. Failed Login Attempts (`GET /failed-logins`)

Paginated list of `FAILED_LOGIN` audit events.

**Query parameters:**

| Parameter | Type | Description |
|---|---|---|
| `page` | int (≥1) | Page number |
| `limit` | int (1–500) | Items per page |
| `start_date` | ISO 8601 datetime | Filter from date |
| `end_date` | ISO 8601 datetime | Filter to date |
| `ip_address` | string | Filter by exact IP |
| `actor_id` | UUID | Filter by user |
| `search` | string | Search description/IP/entity |

---

### 3. Blocked IPs (`GET /blocked-ips`)

Returns IPs that have generated ≥ `threshold` (default 5) failed login events.

```json
[
  {
    "ip_address": "5.5.5.5",
    "failed_login_count": 87,
    "last_seen": "2025-01-15T10:42:00Z",
    "associated_user_ids": ["uuid-1", "uuid-2"]
  }
]
```

**Query parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `threshold` | int (≥1) | 5 | Min failures to flag an IP |
| `start_date` | datetime | — | Filter from date |
| `end_date` | datetime | — | Filter to date |

---

### 4. Suspicious Sessions (`GET /suspicious-sessions`)

Paginated list of `SUSPICIOUS_LOGIN_ATTEMPT` events. Supports all common filters.

---

### 5. Password Resets (`GET /password-resets`)

Paginated list of `PASSWORD_RESET` events.

---

### 6. API Abuse Reports (`GET /api-abuse`)

Paginated list of failed `API_ACCESS` events (potential scraping / brute-force via API).

---

### 7. Security Alerts (`GET /alerts`)

High-severity events with computed severity labels:

| Action | Severity |
|---|---|
| `suspicious_login_attempt` | **critical** |
| `user_banned` | **critical** |
| `user_suspended` | **high** |
| `token_revoked` | **high** |
| `failed_login` | **medium** |

**Query parameters:** supports `severity` filter (`critical` / `high` / `medium`) plus common filters.

---

### 8. Universal Search (`GET /search`)

Full-text search across all security audit logs (description, IP, entity ID).

```
GET /api/v1/admin/security/search?q=192.168.1.1
GET /api/v1/admin/security/search?q=brute+force&start_date=2025-01-01T00:00:00Z
```

---

## CSV Export

Every filterable section has a companion `/export` endpoint returning `text/csv`.
Export includes up to **10,000 rows** per request.

CSV columns:
`ID, Timestamp, Action, Actor ID, Target User ID, Entity Type, Entity ID, Description,
IP Address, User Agent, Request Method, Request Path, Success, Status Code, Error Message`

---

## Pagination Response Shape

All paginated endpoints return:

```json
{
  "items": [...],
  "total": 310,
  "page": 1,
  "limit": 50,
  "pages": 7
}
```

---

## Implementation Notes

- Built on top of the existing `AuditLog` model — **no schema changes required**.
- All heavy queries use `sqlalchemy` `select()` with server-side aggregations.
- The `require_admin` FastAPI dependency enforces RBAC at the router level, keeping
  business logic in the service layer clean.
- Blocked IP detection uses a configurable threshold (`BLOCKED_IP_THRESHOLD = 5`).

---

## Running the Tests

```bash
cd backend
./venv/bin/pytest tests/test_security_audit_dashboard.py -v
```

Expected output: **30 passed**.
