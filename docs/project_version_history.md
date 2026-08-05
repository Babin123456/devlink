# Project Version History Documentation (#606)

DevLink **Project Version History** maintains a complete, efficiently stored historical log of edits made to project details. Project owners and authorized maintainers can review previous versions, compare field-level diffs, and restore previous project states if needed.

---

## 1. Tracked Fields

The versioning system snapshots and tracks changes across the following core project attributes:

- **Project Title**: Name and title changes
- **Description & Tagline**: Full project description text and summary tagline
- **Tech Stack**: Technologies, frameworks, and tools specification
- **Requirements & Specifications**: Explicit project requirements and developer prerequisites
- **Team Roles**: Team membership roles snapshot
- **Project Stage & Visibility**: `IDEA`, `MVP`, `BETA`, `PRODUCTION` stage transitions and visibility settings

---

## 2. Version Storage & Workflow

### Automatic Snapshots
1. **Initial Creation**: When a project is created, Version 1 is automatically generated as the baseline snapshot.
2. **Project Edit**: Whenever project details are updated, a new incremental version (`v2`, `v3`, etc.) is recorded.
3. **Pre-Restore Backup**: Before reverting to a historical version, the system automatically creates a backup snapshot of the current state, ensuring zero data loss during restoration.

---

## 3. API Reference

### 1. List Version History
`GET /api/v1/projects/{project_id}/versions`

**Query Parameters:** `page` (default 1), `limit` (default 20, max 100)

**Response:**
```json
{
  "items": [
    {
      "id": "e2a1b3c4-d5e6-7890-abcd-ef1234567890",
      "project_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "version_number": 2,
      "title": "DevLink Platform Beta",
      "tagline": "Connect developers worldwide",
      "description": "Updated project description",
      "tech_stack": "React, FastAPI, PostgreSQL",
      "requirements": "Python 3.13, Docker",
      "stage": "mvp",
      "visibility": "public",
      "change_summary": "Updated project details",
      "created_at": "2026-08-04T12:00:00Z"
    }
  ],
  "total": 2,
  "page": 1,
  "limit": 20,
  "pages": 1
}
```

---

### 2. Compare Versions
`GET /api/v1/projects/{project_id}/versions/compare`

**Query Parameters:**
- `v1` (required): Version number or version UUID (e.g. `1`)
- `v2` (optional, default `"current"`): Version number or `"current"`

**Response:**
```json
{
  "project_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "v1_version_number": 1,
  "v2_version_number": "current",
  "diff": {
    "title": {
      "old": "DevLink Alpha",
      "new": "DevLink Platform Beta"
    },
    "tech_stack": {
      "old": "React",
      "new": "React, FastAPI, PostgreSQL"
    }
  }
}
```

---

### 3. Restore Previous Version
`POST /api/v1/projects/{project_id}/versions/{version_identifier}/restore`

**Authorization:** Requires project owner or user with `project:update` permission.

**Behavior:**
- Creates a backup version of current project state.
- Reverts title, description, tech stack, requirements, language, stage, and visibility to target version snapshot.
- Emits `AuditAction.PROJECT_VERSION_RESTORED` log.
- Returns restored project response.

---

## 4. Frontend Component

Component: `frontend/src/components/project/ProjectVersionHistory.tsx`

Features:
- Version timeline list displaying version revision numbers and creation timestamps.
- Side-by-side comparison view highlighting field diffs (Old vs Current/New).
- One-click version restoration button with immediate UI state invalidation and toast feedback.

---

## 5. Running Tests

Execute backend unit and integration tests:
```bash
cd backend
./venv/bin/pytest tests/test_project_version_history.py -v
```

Expected output: **4 passed**.
