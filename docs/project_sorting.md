# Advanced Project Sorting Capabilities

DevLink provides advanced project sorting parameters to help developers discover relevant open source projects quickly across web and mobile.

---

## Sorting Options

| `sort_by` Value | Label | Description | Sorting Criteria |
| :--- | :--- | :--- | :--- |
| `newest` *(default)* | Newest | Most recently created projects | `created_at DESC` |
| `oldest` | Oldest | Earliest created projects | `created_at ASC` |
| `most_active` | Most Active | Projects with recent activity & updates | `updated_at DESC` |
| `most_bookmarked` | Most Bookmarked | Popular projects saved by developers | `bookmarks_count DESC` |
| `most_applications` | Most Applications | High-demand projects receiving join requests | `applications_count DESC` |
| `recently_updated` | Recently Updated | Projects updated recently by owners | `updated_at DESC` |
| `ai_match_score` | AI Match Score | Relevance based on developer tech stack & interest | `updated_at DESC, created_at DESC` |

---

## API Usage

Query parameter: `sort_by`

```http
GET /api/projects/?sort_by=most_active&limit=20 HTTP/1.1
Authorization: Bearer <access_token>
```

---

## Frontend Integration

The `ProjectSortSelector` component in `frontend/src/components/projects/ProjectSortSelector.tsx` provides:
- Persisted sorting via URL search params (`?sort_by=...`).
- Responsive, mobile-compatible layout.
- Loading state indicator while fetching sorted results.
