# Centralized Analytics Service

The Centralized Analytics Service collects, aggregates, and stores application metrics across all major developer activities on DevLink.

---

## Tracked Events

| Event Type Slug | Display Name | Event Trigger Description |
| :--- | :--- | :--- |
| `user_registration` | User Registration | Triggered when a new user registers an account |
| `project_creation` | Project Creation | Triggered when a developer creates a new project |
| `application_sent` | Applications | Triggered when a user submits an application to join a project |
| `profile_view` | Profile Views | Triggered when a profile is viewed by a developer |
| `search_performed` | Searches | Triggered when a search query is submitted |
| `message_sent` | Messages Sent | Triggered when a message is sent in chat/conversations |
| `team_invitation_sent` | Team Invitations | Triggered when a project owner invites a team member |

---

## API Endpoints (`/api/centralized-analytics`)

### 1. Track Event
- **Endpoint**: `/api/centralized-analytics/track`
- **Method**: `POST`
- **Authentication**: Optional Bearer Token
- **Request Body**:

```json
{
  "event_type": "project_creation",
  "properties": {
    "project_id": "41de898b-5c8d-4b25-98d7-754bea5404bf",
    "category": "Web"
  },
  "session_id": "sess_12345"
}
```

### 2. Get Aggregated Metrics Summary
- **Endpoint**: `/api/centralized-analytics/metrics?days=30`
- **Method**: `GET`
- **Authentication**: None (Public/Admin)
- **Response**:

```json
{
  "total_events": 1420,
  "event_counts": {
    "user_registration": 120,
    "project_creation": 85,
    "application_sent": 310,
    "profile_view": 540,
    "search_performed": 210,
    "message_sent": 115,
    "team_invitation_sent": 40
  },
  "period_days": 30
}
```

### 3. List Recent Analytics Events
- **Endpoint**: `/api/centralized-analytics/events?limit=50&event_type=project_creation`
- **Method**: `GET`
- **Authentication**: None (Admin/Analytics Inspector)
- **Response**: Array of `AnalyticsEventResponse` objects.
