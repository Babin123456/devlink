### Configurable Security Headers

The following response headers can be enabled or disabled through environment settings:

- ENABLE_X_FRAME_OPTIONS
- ENABLE_X_CONTENT_TYPE_OPTIONS
- ENABLE_HSTS
- ENABLE_CSP
- ENABLE_DNS_PREFETCH_CONTROL
- ENABLE_CROSS_DOMAIN_POLICIES

## Backup & Restore

### Create a database backup

```bash
python scripts/backup_database.py
```

### Restore a database backup

```bash
python scripts/restore_database.py backups/<backup_file>.sql
```

### Backup uploaded files

```bash
python scripts/backup_storage.py
```

Database backups are stored in the `backups/` directory.

> Before restoring a backup, ensure the application is stopped and the target database is accessible.
