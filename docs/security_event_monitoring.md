# Security Event Monitoring Documentation (#613)

DevLink provides a dedicated **Security Event Monitoring & Alerting System** to log, evaluate, and review critical security events across the platform.

---

## 1. Monitored Event Types

The system monitors 6 critical security event types:

1. **`failed_login`**: Failed authentication attempts (elevated to `HIGH`/`CRITICAL` alert if repeated from the same IP/user within 15 minutes).
2. **`password_reset`**: Password reset requests and executions.
3. **`email_change`**: Email address modifications.
4. **`permission_update`**: System role promotions/demotions or permission policy changes.
5. **`suspicious_api_usage`**: Abnormal API call bursts, rate-limit violations, or unauthorized access attempts.
6. **`account_lockout`**: Account suspensions, bans, or lockouts due to security breaches (automatically triggers a `CRITICAL` alert).

---

## 2. Alert-Ready Event Structure & Evaluation

Each logged security event evaluates risk scores and frequency rules:

| Field | Type | Description |
|---|---|---|
| `id` | `UUID` | Unique event identifier |
| `event_type` | `Enum` | Classification (`failed_login`, `password_reset`, `email_change`, `permission_update`, `suspicious_api_usage`, `account_lockout`) |
| `severity` | `Enum` | `info`, `low`, `medium`, `high`, `critical` |
| `risk_score` | `Float` | Risk score between `0.0` and `1.0` |
| `description` | `String` | Detailed event description |
| `actor_id` | `UUID` | Initiating user ID |
| `target_user_id` | `UUID` | Affected user ID |
| `ip_address` | `String` | Client IPv4 / IPv6 |
| `user_agent` | `String` | Client User-Agent string |
| `alert_triggered` | `Boolean` | True if severity/frequency rules triggered an automated alert |
| `alert_message` | `String` | Alert notification message |
| `is_resolved` | `Boolean` | Resolution state |
| `resolved_at` | `DateTime` | Resolution timestamp |
| `resolved_by_id` | `UUID` | Admin user ID who resolved the alert |
| `resolution_notes` | `String` | Admin resolution notes |

---

## 3. Admin API Reference

Base paths: `/api/v1/admin/security-events` (and `/api/admin/security-events`).
Requires system administrator privileges (`require_admin`).

| Method | Endpoint Path | Description |
|---|---|---|
| `GET` | `/` | Paginated and filterable list of security events |
| `GET` | `/summary` | Monitoring summary metrics & dashboard statistics |
| `POST` | `/log` | Programmatically or manually log a security event |
| `GET` | `/{event_id}` | Retrieve details of a specific security event |
| `POST` | `/{event_id}/resolve` | Mark a security alert/event as resolved |
| `POST` | `/{event_id}/acknowledge` | Acknowledge a security event |

---

## 4. Running Tests

Run backend unit and integration tests:
```bash
cd backend
./venv/bin/pytest tests/test_security_events.py -v
```

Expected result: **15 passed**.
