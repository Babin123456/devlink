# Backend API Unit Tests Documentation (#388)

Comprehensive unit test suite for backend API endpoints using Pytest, covering success/failure scenarios, status codes, authentication, authorization, and error handling.

---

## Endpoint Test Coverage Scope

| Feature / Domain | Test File | Covered Endpoints & Actions | Status Code Assertions |
|---|---|---|---|
| **Authentication** | `backend/tests/test_auth.py` | Signup (`POST /api/auth/signup`), Login (`POST /api/auth/login`), Token Refresh, Invalid Credentials, Duplicate User, Invalid Payload | `201 Created`, `200 OK`, `400 Bad Request`, `401 Unauthorized`, `422 Unprocessable` |
| **User Profiles** | `backend/tests/test_users.py` | Get Me (`GET /api/users/me`), Get Profile (`GET /api/users/{username}`), Update Profile (`PUT /api/users/me`), User Search, 404 Non-existent Profile | `200 OK`, `404 Not Found`, `401 Unauthorized`, `422 Unprocessable` |
| **Projects** | `backend/tests/test_projects.py` | Create Project (`POST /api/projects/`), Get Project (`GET /api/projects/{id}`), List Projects (`GET /api/projects/`), Update Project (`PUT /api/projects/{id}`), Status Transitions, Delete/Archive | `201 Created`, `200 OK`, `400 Bad Request`, `404 Not Found`, `422 Unprocessable` |
| **Applications** | `backend/tests/test_applications.py` | Create Application (`POST /api/applications/`), Get Application (`GET /api/applications/{id}`), My Applications (`GET /api/applications/me`), Project Applications (`GET /api/applications/project/{id}`), Accept (`PATCH /accept`), Reject (`PATCH /reject`), Withdraw (`PATCH /withdraw`), Delete (`DELETE /{id}`) | `201 Created`, `200 OK`, `204 No Content`, `404 Not Found`, `422 Unprocessable` |
| **Notifications** | `backend/tests/test_notifications.py` | List Notifications (`GET /api/notifications/`), Unread Count (`GET /api/notifications/unread-count`), Mark Read (`PATCH /api/notifications/{id}/read`), Mark All Read (`POST /api/notifications/mark-all-read`), Delete (`DELETE /{id}`) | `200 OK`, `204 No Content`, `404 Not Found`, `401 Unauthorized` |

---

## Execution Command

```bash
cd backend && ./venv/bin/python -m pytest tests/test_auth.py tests/test_users.py tests/test_projects.py tests/test_applications.py tests/test_notifications.py -v
```

All 80 unit tests pass cleanly.
