import { auditApi, AuditLog } from "@/api";
import { isBackendConfigured } from "@/api/client";

const delay = 120;
const mock = <T>(v: T): Promise<T> => new Promise((r) => setTimeout(() => r(v), delay));

// Fallback data for offline/mock mode
const seedAuditLogs: AuditLog[] = [
  {
    id: "log-1",
    actor_id: "user-1",
    target_user_id: null,
    project_id: "proj-1",
    organization_id: null,
    action: "project_created",
    entity_type: "project",
    entity_id: "proj-1",
    description: "Project created",
    old_values: null,
    new_values: { name: "Project Alpha" },
    metadata_info: null,
    ip_address: "127.0.0.1",
    user_agent: "Mozilla/5.0",
    request_method: "POST",
    request_path: "/projects/",
    success: true,
    status_code: 201,
    error_message: null,
    created_at: new Date().toISOString(),
  }
];

async function withFallback<T>(call: () => Promise<T>, fallback: T): Promise<T> {
  if (!isBackendConfigured()) return mock(fallback);
  try {
    return await call();
  } catch (err) {
    if (import.meta.env.DEV) console.warn("[services] API call failed, using fallback:", err);
    return fallback;
  }
}

export const auditService = {
  list: (params?: {
    skip?: number;
    limit?: number;
    actor_id?: string;
    project_id?: string;
    organization_id?: string;
    action?: string;
    entity_type?: string;
  }) => withFallback(() => auditApi.list(params), seedAuditLogs),
};
