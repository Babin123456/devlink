# DevLink Backup & Restore — User Data (#635)

DevLink lets users create a **portable, tamper-proof backup** of all their DevLink
data and restore it to any account.

---

## Overview

| Feature | Details |
|---|---|
| **Backup format** | Signed JSON wrapped in a ZIP archive |
| **Integrity** | SHA-256 checksum embedded in every backup |
| **Restore strategy** | Non-destructive merge — existing records are never deleted |
| **Sensitive data** | Passwords, MFA secrets, tokens are **never** included |

---

## API Endpoints

All endpoints require a valid Bearer token (`Authorization: Bearer <token>`).

### `POST /api/v1/users/me/backup`
Create a full backup and **download** it as a `.zip` file.

**Response:** `application/zip` — contains `devlink_backup_<id>.json`

---

### `POST /api/v1/users/me/backup/meta`
Create a backup and receive only the **metadata** (no file download).

**Response:**
```json
{
  "success": true,
  "backup_id": "3fa85f64-...",
  "created_at": "2025-01-15T10:00:00Z",
  "message": "Backup created successfully..."
}
```

---

### `POST /api/v1/users/me/backup/validate`
Upload a backup JSON file to verify its **integrity and structure** before restoring.

**Request:** `multipart/form-data` — field `file` containing the JSON file.

**Response:**
```json
{
  "valid": true,
  "errors": []
}
```

If the file has been tampered with, `valid` will be `false` and `errors` will describe each problem.

---

### `POST /api/v1/users/me/backup/preview`
Preview what would be restored **without making any changes**.

**Request:** `multipart/form-data` — field `file`.

**Response:**
```json
{
  "backup_id": "3fa85f64-...",
  "created_at": "2025-01-15T10:00:00Z",
  "username": "alice",
  "records": {
    "profile_fields": 18,
    "projects": 4,
    "skills": 6,
    "bookmarks": 12,
    "messages": 87,
    "connections": 23,
    "organizations": 1,
    "applications": 3,
    "activities": 145,
    "notifications": 50,
    "builder_flares": 2
  }
}
```

---

### `POST /api/v1/users/me/backup/restore`
Restore user data from a backup file.

**Request:** `multipart/form-data` — field `file`.

**Response:**
```json
{
  "success": true,
  "message": "Backup restored successfully.",
  "restored": {
    "profile_fields": 3,
    "bookmarks": 8,
    "skills": 2
  }
}
```

---

## Backup File Format

The extracted JSON has three top-level sections:

```json
{
  "metadata": {
    "version": "1.0",
    "backup_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_at": "2025-01-15T10:00:00Z",
    "app_name": "DevLink",
    "user_id": "...",
    "username": "alice"
  },
  "checksum": "<sha256 of data section>",
  "data": {
    "profile": { ... },
    "skills": [ ... ],
    "projects": [ ... ],
    "bookmarks": [ ... ],
    "messages": [ ... ],
    "connections": [ ... ],
    "organizations": [ ... ],
    "applications": [ ... ],
    "activities": [ ... ],
    "notifications": [ ... ],
    "builder_flares": [ ... ]
  }
}
```

> [!IMPORTANT]
> The `checksum` is a SHA-256 digest of the `data` section serialised as JSON (keys sorted, no whitespace). Any modification to the `data` section will invalidate the backup and it will be rejected on restore.

---

## Data Included in Backup

| Section | Included |
|---|---|
| Profile fields | ✅ All public and private profile fields |
| Skills | ✅ Skill associations + proficiency level |
| Projects | ✅ All owned projects |
| Bookmarks | ✅ All bookmarks |
| Messages | ✅ Up to 1,000 sent messages |
| Connections | ✅ Followers and following |
| Organizations | ✅ Owned organizations |
| Applications | ✅ All submitted applications |
| Activities | ✅ Up to 500 activity records |
| Notifications | ✅ Up to 500 notifications |
| Builder Flares | ✅ All posted flares |

---

## What Gets Restored

The restore operation is a **non-destructive merge**:

| Section | Restore behaviour |
|---|---|
| **Profile fields** | Mutable fields (bio, headline, location, etc.) are updated if the backup value differs |
| **Bookmarks** | Re-created for projects that still exist in DevLink |
| **Skills** | User-skill associations re-created for skills that still exist |
| Messages | **Not restored** — privacy/conversation ownership |
| Connections | **Not restored** — live social graph |
| Organizations | **Not restored** — require separate ownership transfer |
| Notifications | **Not restored** — ephemeral |

---

## Security Considerations

- Backup files **never** contain passwords, MFA secrets, refresh tokens, or API keys.
- The SHA-256 checksum prevents silent data tampering.
- Only the **authenticated user** can create or restore their own backup.
- Restore is scoped to the **currently authenticated user** — you cannot restore a backup into another user's account.

---

## Typical Workflow

1. **Download backup**: `POST /api/v1/users/me/backup` → save the `.zip` file.
2. **Extract JSON**: Unzip `devlink_backup_<username>.zip`.
3. *(Optional)* **Validate**: `POST /api/v1/users/me/backup/validate` with the JSON file.
4. *(Optional)* **Preview**: `POST /api/v1/users/me/backup/preview` to see what would change.
5. **Restore**: `POST /api/v1/users/me/backup/restore` with the JSON file.

---

## Running the Tests

```bash
cd backend
./venv/bin/pytest tests/test_backup_restore.py -v
```

Expected output: **21 passed**.
