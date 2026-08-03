# Developer Portfolio Export (#598)

The **Developer Portfolio Export** feature allows DevLink users to export their profile into a clean, professional, shareable portfolio document.

## Export Formats Supported

1. **PDF (Responsive Layout / Printable Document):**
   - High quality, modern styled document suitable for printing or converting to PDF.
   - Includes profile header, bio, skills chips, experience, and project highlights.
2. **Markdown (`.md`):**
   - Clean, GitHub-formatted markdown file.
   - Ideal for inclusion in GitHub profile READMEs or personal documentation.
3. **JSON (`.json`):**
   - Structured JSON schema containing full profile details, skills, project memberships, and activity data.

## API Endpoint

`GET /api/users/me/portfolio/export?format={json|markdown|pdf}`

### Query Parameters

| Parameter | Type   | Required | Default | Allowed Values         |
| --------- | ------ | -------- | ------- | ---------------------- |
| `format`  | string | No       | `json`  | `pdf`, `markdown`, `json` |

### Example Request

```bash
curl -X GET "http://localhost:8000/api/users/me/portfolio/export?format=markdown" \
     -H "Authorization: Bearer <your_jwt_token>"
```
