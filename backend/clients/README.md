# DevLink API SDKs

DevLink automatically generates client SDKs for **TypeScript** and **Python**
from the FastAPI OpenAPI specification. SDKs are versioned alongside the API
schema and regenerated on every push to `main` and on release tags.

## Layout

```
clients/
├── openapi.json            # Exported OpenAPI 3.1 schema (the single source of truth)
├── typescript/             # TypeScript SDK (openapi-typescript)
│   └── src/api/generated.ts
└── python/                 # Python SDK (openapi-python-client)
    ├── pyproject.toml
    └── dev_link_api_client/
```

## Regenerating

The `sdk-generation` GitHub Actions workflow (`/.github/workflows/sdk-generation.yml`)
handles regeneration automatically on every push to `main` and on `v*` tags.

To regenerate locally:

```bash
# 1. Export the OpenAPI schema from the FastAPI app
cd backend
python scripts/export_openapi.py

# 2. Generate both SDKs
cd ..
python backend/scripts/generate_sdks.py
```

## TypeScript SDK

```bash
cd clients/typescript
npm install
npm run build
```

Usage example:

```ts
import type { components } from "./src/api/generated";

type User = components["schemas"]["CurrentUser"];

async function fetchMe(token: string): Promise<User> {
  const res = await fetch(`${API_BASE_URL}/api/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}
```

## Python SDK

```bash
cd clients/python
pip install -e .
```

Usage example:

```python
from dev_link_api_client.client import Client

client = Client(base_url="https://api.devlink.io")

# Authenticated requests
from dev_link_api_client.models import LoginRequest

login = client.get_httpx_client().post(
    "/api/auth/login",
    json=LoginRequest(email="you@example.com", password="secret").to_dict(),
)
print(login.status_code)
```

## Authentication

The API uses `HTTPBearer` JWT authentication. Include the access token in the
`Authorization` header on every protected call:

```
Authorization: Bearer <access_token>
```

## Versioning

SDKs are versioned to match the API. The version lives in:

- `clients/openapi.json` → `info.version` (from the FastAPI app)
- `clients/typescript/package.json` → `version`
- `clients/python/pyproject.toml` → `version`

On every `v*` release tag the workflow regenerates the SDKs and attaches them
as release artifacts (`devlink-sdks-<tag>`).

## CI Automation

`.github/workflows/sdk-generation.yml` runs:

1. Checkout + install backend dependencies.
2. `python scripts/export_openapi.py` — export the schema.
3. `python scripts/generate_sdks.py` — generate TypeScript + Python SDKs.
4. Verify generated output exists.
5. Auto-commit regenerated SDKs on pushes to `main`.
6. Upload `clients/typescript` + `clients/python` as release artifacts on tags.
