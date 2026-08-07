import { api } from "../client";

export interface AuditLog {
  id: string;
  actor_id: string;
  target_user_id: string | null;
  project_id: string | null;
  organization_id: string | null;
  action: string;
  entity_type: string;
  entity_id: string | null;
  description: string | null;
  old_values: Record<string, unknown> | null;
  new_values: Record<string, unknown> | null;
  metadata_info: Record<string, unknown> | null;
  ip_address: string | null;
  user_agent: string | null;
  request_method: string | null;
  request_path: string | null;
  success: boolean;
  status_code: number | null;
  error_message: string | null;
  created_at: string;
}

export interface AuditLogQuery {
  skip?: number;
  limit?: number;
  actor_id?: string;
  project_id?: string;
  organization_id?: string;
  action?: string;
  entity_type?: string;
}

export const auditApi = {
  list: (params?: AuditLogQuery) =>
    api.get<AuditLog[]>("/api/audit/", {
      query: (params ?? {}) as Record<string, string | number | boolean | null | undefined>,
    }),
};
