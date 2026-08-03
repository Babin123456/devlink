# DevLink Project Milestone Management Documentation (#618)

DevLink provides a complete **Project Milestone Management System** allowing project owners and team maintainers to define milestones, set due dates, track progress percentage, view interactive timelines, and archive completed milestones.

---

## 1. Features & Overview

- **Milestone CRUD Operations**: Create, view, update, archive, and delete milestones.
- **Due Date Tracking**: Associate milestones with due dates and track remaining days or overdue status.
- **Progress Calculations**: Automatically calculates completion percentages (`(completed / total_active) * 100%`) and status breakdowns (`total`, `completed`, `active`, `archived`, `overdue`).
- **Timeline View**: Chronological view with status badges (`upcoming`, `overdue`, `completed`, `archived`) and remaining days countdown.
- **Milestone Archiving**: Archive completed or obsolete milestones to keep active project timelines clean without losing historical progress.
- **Role-Based Permissions**: Only project owners, co-owners, admins, and maintainers can manage milestones; project members and public users can view timelines and progress.

---

## 2. API Endpoints Reference

Base path: `/api/v1/projects/{project_id}/milestones` (also registered under `/api/projects/{project_id}/milestones`)

| Method | Endpoint Path | Role Required | Description |
|---|---|---|---|
| `GET` | `/` | Any / Public | List project milestones (with `include_archived` and `is_completed` filters) |
| `POST` | `/` | Owner / Maintainer | Create a new project milestone |
| `GET` | `/progress` | Any / Public | Calculate completion percentage and milestone breakdown metrics |
| `GET` | `/timeline` | Any / Public | Get chronological timeline view with status tags and days remaining |
| `GET` | `/{milestone_id}` | Any / Public | Get detailed information for a single milestone |
| `PATCH` | `/{milestone_id}` | Owner / Maintainer | Update milestone (title, description, due date, completion/archive state) |
| `POST` | `/{milestone_id}/archive` | Owner / Maintainer | Archive a milestone |
| `POST` | `/{milestone_id}/unarchive` | Owner / Maintainer | Restore an archived milestone back to active status |
| `DELETE` | `/{milestone_id}` | Owner / Maintainer | Delete a milestone from the project |

---

## 3. Data Schemas

### `MilestoneResponse`
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "project_id": "4a7b5f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Beta Launch",
  "description": "Release core MVP features for community testing",
  "due_date": "2026-08-15T00:00:00Z",
  "is_completed": false,
  "completed_at": null,
  "is_archived": false,
  "archived_at": null,
  "created_at": "2026-08-01T10:00:00Z",
  "updated_at": "2026-08-03T10:00:00Z"
}
```

### `MilestoneProgressResponse`
```json
{
  "total_milestones": 5,
  "completed_milestones": 3,
  "active_milestones": 4,
  "archived_milestones": 1,
  "overdue_milestones": 0,
  "completion_percentage": 75.0
}
```

### `MilestoneTimelineResponse`
```json
{
  "project_id": "4a7b5f64-5717-4562-b3fc-2c963f66afa6",
  "project_title": "DevLink Mobile App",
  "progress": {
    "total_milestones": 3,
    "completed_milestones": 1,
    "active_milestones": 2,
    "archived_milestones": 1,
    "overdue_milestones": 1,
    "completion_percentage": 50.0
  },
  "timeline": [
    {
      "milestone": {
        "id": "...",
        "title": "Database Schema Design",
        "is_completed": true
      },
      "status": "completed",
      "days_remaining": null
    },
    {
      "milestone": {
        "id": "...",
        "title": "API Integration",
        "due_date": "2026-08-10T00:00:00Z",
        "is_completed": false
      },
      "status": "upcoming",
      "days_remaining": 7
    }
  ]
}
```

---

## 4. Running Tests

Run backend unit and integration tests:
```bash
cd backend
./venv/bin/pytest tests/test_project_milestones.py -v
```

Expected result: **11 passed**.
