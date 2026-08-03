# AI-Powered Profile Improvement Suggestions Documentation (#619)

DevLink provides an **AI-powered developer profile improvement engine** designed to analyze developer profiles and recommend actionable improvements across 5 core categories to increase developer visibility and collaboration opportunities.

---

## 1. Overview & Key Capabilities

- **Profile Completeness Scoring**: Calculates a dynamic 0–100 profile completeness score based on skills, bio depth, portfolio links, GitHub connection, and availability.
- **5 Core Suggestion Categories**:
  1. `missing_skills` — Identifies missing core technical skills, low skill count, or role-specific skill gaps (e.g. missing React/TypeScript for Frontend engineers).
  2. `weak_bio` — Detects empty, brief (< 40 characters), or headline-less bios and recommends structured bios.
  3. `portfolio_improvements` — Highlights missing personal website/portfolio links or zero project showcases.
  4. `github_connection` — Detects unlinked GitHub accounts and prompts for repository integration.
  5. `experience_gaps` — Identifies missing experience levels, current company/role information, or availability status (`open_to_work`).
- **AI & Rule-based Intelligence**: Uses OpenAI (`gpt-4o-mini`) when configured to generate hyper-personalized suggestions and descriptions. Automatically falls back to a rule-based inference engine if AI API keys are unavailable.
- **Dismissal Mechanism**: Developers can dismiss suggestions individually or all at once. Dismissals persist across sessions.
- **Recommendation Refresh**: Allows developers to trigger a fresh analysis and optionally reset dismissed items to re-evaluate their updated profile.

---

## 2. API Endpoints

### 1. Get Profile Suggestions
- **`GET /api/v1/profile-suggestions`** (also accessible via `GET /api/v1/users/me/profile-suggestions`)
- **Query Parameters**:
  - `include_dismissed` (`bool`, optional, default: `false`): Include previously dismissed suggestions.
- **Response**: `ProfileSuggestionsResponse`
  ```json
  {
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "profile_score": 65,
    "total_suggestions": 4,
    "active_suggestions_count": 3,
    "dismissed_suggestions_count": 1,
    "suggestions": [
      {
        "id": "missing_skills_none",
        "category": "missing_skills",
        "title": "No Skills Listed",
        "description": "Your profile currently has no skills listed. Adding key technical skills improves collaborator matching.",
        "impact": "high",
        "action_label": "Add Skills",
        "action_url": "/settings/skills",
        "is_dismissed": false
      }
    ],
    "generated_at": "2026-08-02T22:45:00Z"
  }
  ```

### 2. Dismiss a Suggestion
- **`POST /api/v1/profile-suggestions/{suggestion_id}/dismiss`**
- **Response**: `DismissSuggestionResponse`
  ```json
  {
    "success": true,
    "message": "Suggestion 'missing_skills_none' has been dismissed.",
    "suggestion_id": "missing_skills_none",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  }
  ```

### 3. Dismiss All Suggestions
- **`POST /api/v1/profile-suggestions/dismiss-all`**
- **Response**:
  ```json
  {
    "success": true,
    "message": "Dismissed 3 active suggestions.",
    "dismissed_count": 3,
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  }
  ```

### 4. Refresh Recommendations
- **`POST /api/v1/profile-suggestions/refresh`**
- **Query Parameters**:
  - `reset_dismissed` (`bool`, optional, default: `false`): If true, resets previously dismissed suggestions to allow re-evaluation.
- **Response**: `RefreshSuggestionsResponse`
  ```json
  {
    "success": true,
    "message": "Profile suggestions re-evaluated and refreshed successfully.",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "reset_dismissed_count": 1
  }
  ```

---

## 3. Data Models

### `profile_suggestion_dismissals` Table
- `id` (`UUID`, Primary Key)
- `user_id` (`UUID`, Foreign Key to `users.id`, Index)
- `suggestion_id` (`VARCHAR(100)`, Index)
- `category` (`VARCHAR(50)`)
- `dismissed_at` (`TIMESTAMPTZ`)
- Unique constraint on `(user_id, suggestion_id)`.

---

## 4. Testing & Verification

Run backend unit tests:
```bash
cd backend
./venv/bin/pytest tests/test_profile_suggestions.py -v
```

Tests cover:
- Dynamic profile score calculation across incomplete and full profiles.
- Suggestion generation for all 5 core categories (`missing_skills`, `weak_bio`, `portfolio_improvements`, `github_connection`, `experience_gaps`).
- AI enrichment and rule-based fallback handling.
- Dismissing individual and all suggestions.
- Refreshing suggestions with and without resetting dismissals.
