# User Achievement Badges System

The User Achievement Badges feature automatically awards developers achievement badges on reaching platform milestones.

---

## Badge Categories & Standard Milestones

| Badge Slug | Name | Description | Category | Points | Trigger Condition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `first-project` | First Project | Created your first project on DevLink | Milestone | 20 | Created ≥ 1 project |
| `first-collaboration` | First Collaboration | Joined your first project team | Collaboration | 20 | Joined or created ≥ 1 project team |
| `top-contributor` | Top Contributor | Contributed to 5 or more projects | Achievement | 50 | Total projects + collaborations ≥ 5 |
| `ai-builder` | AI Builder | Created an AI-focused project | Specialty | 30 | Created ≥ 1 project with AI keywords |
| `community-helper` | Community Helper | Submitted feedback or community issues | Community | 25 | Submitted ≥ 1 feedback submission |
| `100-followers` | 100 Followers | Reached 100 followers on developer profile | Social | 100 | Follower count ≥ 100 |

---

## API Endpoints (`/api/badges`)

### 1. Get All Badges
- **Endpoint**: `/api/badges/`
- **Method**: `GET`
- **Authentication**: None (Public)
- **Response**: Array of `BadgeResponse` objects

### 2. Get Earned User Badges
- **Endpoint**: `/api/badges/user/{user_id}` or `/api/badges/me`
- **Method**: `GET`
- **Authentication**: Bearer Token for `/me`
- **Response**: Array of `UserBadgeResponse` objects

### 3. Evaluate Achievement Badges
- **Endpoint**: `/api/badges/evaluate`
- **Method**: `POST`
- **Authentication**: Bearer Token
- **Response**: `BadgeEvaluationResponse` containing newly awarded badges, total badge count, and total points.

---

## Frontend Integration

The `BadgeDisplay` component in `src/components/profile/BadgeDisplay.tsx` renders earned and available badges dynamically with icons, point scores, and tooltips.
