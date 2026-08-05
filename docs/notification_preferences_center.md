# Notification Preferences Center Documentation (#586)

The **Notification Preferences Center** provides a centralized interface and RESTful APIs allowing developers to manage notification delivery channels, event categories, and email notification controls.

---

## 1. Supported Notification Categories

The system supports granular toggles across 6 primary categories:

1. **Messages (`messages` & `email_messages`)**: Direct messages and active conversation alerts.
2. **Team Invitations (`team_invitations` & `email_team_invitations`)**: Project invitations, team membership, and role updates.
3. **Project Updates (`project_updates` & `email_project_updates`)**: Milestones, status updates, and repository activity.
4. **Mentions (`mentions` & `email_mentions`)**: Developers tagging or mentioning `@username` in discussions and issues.
5. **System Announcements (`system_announcements` & `email_system_announcements`)**: Platform updates, scheduled maintenance, and system alerts.
6. **Email Notifications (`email_enabled` master toggle)**: Master email toggle and per-category email controls.

---

## 2. API Reference

### Get Notification Preferences
`GET /api/v1/notifications/preferences` (and `/api/notifications/preferences`)

**Authorization:** Requires authenticated user session (`get_current_user`).

**Response Payload Example:**
```json
{
  "id": "e2a1b3c4-d5e6-7890-abcd-ef1234567890",
  "user_id": "c1a2b3c4-d5e6-7890-abcd-ef1234567890",
  "email_enabled": true,
  "websocket_enabled": true,
  "database_enabled": true,
  "messages": true,
  "team_invitations": true,
  "project_updates": true,
  "mentions": true,
  "system_announcements": true,
  "email_messages": true,
  "email_team_invitations": true,
  "email_project_updates": true,
  "email_mentions": true,
  "email_system_announcements": true,
  "updated_at": "2026-08-04T10:00:00Z"
}
```

---

### Update Notification Preferences
`PUT /api/v1/notifications/preferences` or `PATCH /api/v1/notifications/preferences`

**Request Payload Example:**
```json
{
  "email_enabled": true,
  "messages": true,
  "email_messages": false,
  "team_invitations": true,
  "project_updates": true,
  "mentions": true,
  "system_announcements": true
}
```

---

## 3. Frontend Settings Component

Location: `frontend/src/routes/_app.settings.notifications.tsx`

Features:
- Master Delivery Channel Switches (Email, Database, Real-time WebSockets)
- Per-category matrix for In-App and Email notifications
- Auto-saves changes per switch toggle with instant toast feedback
- Disables per-category email switches automatically when Master Email is disabled

---

## 4. Running Unit Tests

Execute backend unit tests:
```bash
cd backend
./venv/bin/pytest tests/test_notification_preferences.py -v
```

Expected output: **4 passed**.
