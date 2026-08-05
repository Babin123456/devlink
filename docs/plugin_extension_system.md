# Plugin & Extension System Documentation (#582)

DevLink provides a complete **Plugin & Extension Architecture** allowing third-party developers, community builders, and core maintainers to extend DevLink with custom integrations, UI widgets, and automated event workflows.

---

## 1. Extension System Architecture

The plugin architecture consists of 4 core building blocks:

1. **Plugin Marketplace & Registry**: Stores registered plugins with versioning, plugin types (`integration`, `widget`, `workflow`), verification status, and installation counters.
2. **Extension Manifest Schema**: Declarative JSON payload specifying extension points, requested permissions, UI widget embedding rules, JSON configuration schema, and webhook delivery endpoints.
3. **Installation & Configuration Manager**: Manages user-level or organization-level plugin installations, enable/disable toggles, and user configuration settings.
4. **Workflow Execution & Event Dispatcher**: Triggers workflow events (e.g. `on_project_created`, `on_application_submitted`, `on_build_completed`, `dashboard_widget`) and queues asynchronous webhooks to matching enabled installations.

---

## 2. Plugin Types & Extension Points

### Plugin Types
- **`integration`**: Connects DevLink with external developer tools (e.g., Slack, Jira, GitHub Actions, Discord).
- **`widget`**: Custom dashboard and project UI components embedded into DevLink pages.
- **`workflow`**: Custom automation routines executed on DevLink platform trigger events.

### Extension Points
- `on_project_created` — Triggered when a new project is created.
- `on_project_updated` — Triggered when project settings or status changes.
- `on_application_submitted` — Triggered when a builder submits a project application.
- `on_issue_created` — Triggered when a project issue or task is opened.
- `on_milestone_completed` — Triggered when a project milestone is marked complete.
- `dashboard_widget` — Embedded widget on developer profile or project dashboard.

---

## 3. Extension Manifest Schema

```json
{
  "extension_points": [
    "on_project_created",
    "dashboard_widget"
  ],
  "webhook_url": "https://plugins.example.com/devlink-hook",
  "permissions": [
    "read_projects",
    "write_notifications"
  ],
  "widget_config": {
    "title": "Build Status Widget",
    "height": 300,
    "entrypoint": "https://plugins.example.com/widget.js"
  },
  "config_schema": {
    "type": "object",
    "properties": {
      "api_token": {
        "type": "string",
        "title": "API Token"
      },
      "notify_channel": {
        "type": "string",
        "title": "Slack Channel"
      }
    },
    "required": ["api_token"]
  }
}
```

---

## 4. API Reference

Base path: `/api/v1/plugins` (also registered under `/api/plugins`)

| Method | Endpoint Path | Role Required | Description |
|---|---|---|---|
| `GET` | `/` | Any / Public | Browse & search marketplace plugins (filters: `plugin_type`, `status`, `is_verified`, `search`) |
| `POST` | `/` | Authenticated User | Register a new plugin/extension with manifest payload |
| `GET` | `/installed/me` | Authenticated User | List current user's or organization's installed plugins |
| `POST` | `/dispatch-event` | System / Internal | Dispatch an extension point event (`event`, `payload`) to matching active installations |
| `GET` | `/{plugin_id_or_slug}` | Any / Public | Get plugin details, author info, and manifest schema |
| `PATCH` | `/{plugin_id}` | Plugin Author / Admin | Update plugin details, version string, or manifest configuration |
| `POST` | `/{plugin_id}/install` | Authenticated User | Install plugin for user or organization |
| `DELETE` | `/{plugin_id}/install` | Authenticated User | Uninstall plugin for user or organization |
| `PATCH` | `/installations/{installation_id}` | User / Admin | Update installation enable/disable state or custom settings |
| `POST` | `/{plugin_id}/verify` | System Admin | Verify or mark plugin as official |

---

## 5. Running Tests

Run backend unit and integration tests:
```bash
cd backend
./venv/bin/pytest tests/test_plugins.py -v
```

Expected output: **12 passed**.
