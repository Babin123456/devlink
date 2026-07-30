# DevLink API Versioning Strategy & Migration Guide

## 📌 Overview

This document outlines the API versioning strategy and migration policy for the DevLink developer collaboration platform.

As the platform evolves, API versioning ensures that updates, feature enhancements, and refactoring can occur without disrupting active frontend clients, third-party integrations, or mobile applications.

---

## 🎯 Versioning Architecture

DevLink follows **URL Path Versioning** for explicit, predictable, and cache-friendly API routing.

### Base URLs

- **Current Versioned API**: `/api/v1`
  - Example: `https://api.devlink.app/api/v1/auth/login`
  - Example: `https://api.devlink.app/api/v1/projects`
- **Legacy Unversioned API (Backward Compatibility)**: `/api`
  - Example: `https://api.devlink.app/api/projects`
  - _Note_: Unversioned `/api` routes map to the current stable API version (`v1`).

### Version Root Metadata

Requesting `GET /api` or `GET /api/v1` returns current versioning status and metadata:

```json
{
  "name": "DevLink API",
  "version": "v1",
  "current_version": "v1",
  "supported_versions": ["v1"],
  "status": "running",
  "docs": "/docs"
}
```

---

## ⚖️ Breaking vs. Non-Breaking Changes

### Non-Breaking Changes (In-place updates to current version)

Non-breaking changes **do not** require incrementing the API version number:

- Adding new API endpoints (e.g. `POST /api/v1/projects/{id}/star`).
- Adding optional query parameters or optional request body fields.
- Adding new response body properties.
- Performance optimizations and internal bug fixes.

### Breaking Changes (Requires new major API version, e.g., `v2`)

Breaking changes **require** introducing a new major version prefix (e.g., `/api/v2`):

- Removing or renaming existing endpoints or fields.
- Changing data types of response fields (e.g., string ID to integer ID).
- Altering authentication mechanisms or response structures.
- Changing error payload formats or HTTP status codes for existing behavior.

---

## ⏳ API Lifecycle & Deprecation Policy

When a major API version (e.g. `v1`) is superseded by a newer version (e.g. `v2`), DevLink follows a structured deprecation lifecycle:

### 1. Announcement & Grace Period

- Standard deprecation period is **6 months** minimum before retiring an old version.
- Developer notifications via developer docs, release notes, and OpenAPI specs.

### 2. HTTP Deprecation Headers

Deprecated endpoints will return standard HTTP response headers:

```http
Deprecation: @1798761600
Sunset: Sun, 01 Nov 2026 00:00:00 GMT
Link: <https://docs.devlink.app/api/migration/v1-to-v2>; rel="successor-version"
```

### 3. Retirement (Sunset)

- Upon reaching the `Sunset` date, requests to the retired version return `410 Gone`:

```json
{
  "success": false,
  "message": "API version v1 is retired. Please migrate to /api/v2.",
  "error_code": "API_VERSION_RETIRED"
}
```

---

## 🚀 Migration Strategy for Future Versions (e.g. v1 to v2)

When introducing a new API version (e.g. `v2`):

1. **Parallel Support**:
   - `v1` and `v2` run concurrently in backend (`app/api/v1/router.py` and `app/api/v2/router.py`).
   - Shared business logic resides in `app/services/` and `app/models/`.

2. **Client Migration Steps**:
   - Step 1: Update API client base URL configuration to point to `/api/v2`.
   - Step 2: Update payload schemas for modified endpoints.
   - Step 3: Run integration tests against `/api/v2`.

3. **Fallback & Monitoring**:
   - Monitor request metrics by route prefix (`/api/v1` vs `/api/v2`) to track client migration progress.

---

## 🔒 Backward Compatibility Guarantee

All current `/api/...` routes continue to be served without modification. Existing applications using unversioned endpoints will not experience breaking changes as the `/api/v1` structure is rolled out.
