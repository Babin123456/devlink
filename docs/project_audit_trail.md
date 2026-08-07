# Project Audit Trail Documentation (#585)

DevLink maintains a **Secure Audit Trail for Project Changes** to log, store, and query significant project events, enabling project maintainers, owners, and system administrators to review historical modifications.

---

## 1. Tracked Project Events

The platform logs 10 specific project lifecycle and team audit events:

1. **`project_created`**: Project initialization and initial metadata setup.
2. **`project_updated`**: Overall project update payload.
3. **`project_title_updated`**: Project title modifications (stores `old_values` and `new_values`).
4. **`project_description_updated`**: Detailed project description modifications.
5. **`project_status_changed`**: Project stage, visibility, or hiring status changes (e.g., `IDEA` -> `MVP`, `PUBLIC` -> `PRIVATE`).
6. **`project_member_added`**: New team member added to the project.
7. **`project_member_role_updated`**: Member role promotion/demotion (e.g. `Contributor` -> `Maintainer`).
8. **`project_ownership_transferred`**: Transfer of project ownership to another member.
9. **`project_member_removed`**: Removal or departure of a team member.
10. **`project_archived`**: Project archiving.

---

## 2. Secure Audit Record Structure

Each project audit log entry contains:

| Field | Type | Description |
|---|---|---|
| `id` | `UUID` | Unique audit log entry ID |
| `actor_id` | `UUID` | User who initiated the change |
| `target_user_id` | `UUID` | Affected target user (for member/ownership changes) |
| `project_id` | `UUID` | Target project ID |
| `action` | `String / Enum` | Event type (`project_created`, `project_title_updated`, `project_member_role_updated`, etc.) |
| `entity_type` | `String` | Entity type (`project`, `project_member`) |
| `entity_id` | `String` | Unique ID of changed entity |
| `old_values` | `JSON` | Pre-change value snapshot |
| `new_values` | `JSON` | Post-change value snapshot |
| `ip_address` | `String` | Client IPv4 / IPv6 |
| `user_agent` | `String` | Client browser / API User-Agent |
| `created_at` | `DateTime` | ISO-8601 UTC creation timestamp |

---

## 3. API Reference

### Get Project Audit Trail
`GET /api/v1/projects/{project_id}/audit-trail` (and `/api/projects/{project_id}/audit-trail`)

**Query Parameters:**
- `event_type` (optional string): Filter by action name (e.g. `title_updated`, `member`)
- `user_id` (optional UUID): Filter by actor or target user ID
- `page` (int, default `1`)
- `limit` (int, default `20`, max `100`)

**Authorization:**
Accessible to authorized project members, project owner (`require_project_permission("project:read")`), or system administrators.

**Response Payload Example:**
```json
{
  "items": [
    {
      "id": "e2a1b3c4-d5e6-7890-abcd-ef1234567890",
      "actor_id": "c1a2b3c4-d5e6-7890-abcd-ef1234567890",
      "target_user_id": null,
      "project_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "action": "project_title_updated",
      "entity_type": "project",
      "entity_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "old_values": { "title": "Old DevLink App" },
      "new_values": { "title": "DevLink Platform" },
      "ip_address": "127.0.0.1",
      "user_agent": "Mozilla/5.0",
      "created_at": "2026-08-04T10:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 20,
  "pages": 1
}
```

---

## 4. Running Tests

Run backend unit and integration tests:
```bash
cd backend
./venv/bin/pytest tests/test_project_audit_trail.py -v
```

Expected result: **5 passed**.
