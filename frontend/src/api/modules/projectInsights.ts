import { api, isBackendConfigured } from "../client";

export interface SuggestedBuilder {
  name: string;
  role: string;
  match_score: number;
}

export interface RoleGap {
  role: string;
  urgency: "low" | "medium" | "high";
}

export interface RiskAlert {
  message: string;
  severity: "info" | "warning" | "critical";
}

export interface ProjectInsightsResponse {
  project_id: string;
  summary: string;
  suggested_builders: SuggestedBuilder[];
  role_gaps: RoleGap[];
  risk_alerts: RiskAlert[];
}

export interface ProjectInsightsRequest {
  project_id: string;
  title: string;
  description: string;
  tech_stack?: string;
  status?: string;
  members?: number;
}

const ROLE_KEYWORDS: Record<string, string[]> = {
  frontend: ["react", "vue", "angular", "css", "ui", "ux", "tailwind", "frontend"],
  backend: ["fastapi", "django", "node", "express", "api", "backend", "server"],
  devops: ["docker", "kubernetes", "ci/cd", "deploy", "aws", "cloud", "devops"],
  "ml/ai": ["ai", "ml", "machine learning", "tensorflow", "pytorch", "nlp"],
  mobile: ["mobile", "react native", "flutter", "ios", "android", "swift", "kotlin"],
};

function fallbackInsights(data: ProjectInsightsRequest): ProjectInsightsResponse {
  const text = `${data.title} ${data.description} ${data.tech_stack ?? ""}`.toLowerCase();
  const members = data.members ?? 1;

  // Detect role gaps from missing keywords
  const detectedRoles = Object.entries(ROLE_KEYWORDS)
    .filter(([, kws]) => kws.some((kw) => text.includes(kw)))
    .map(([role]) => role);
  const allRoles = Object.keys(ROLE_KEYWORDS);
  const gaps: RoleGap[] = allRoles
    .filter((r) => !detectedRoles.includes(r))
    .slice(0, 2)
    .map((role) => ({ role, urgency: "medium" as const }));

  // Risk alerts based on heuristics
  const risks: RiskAlert[] = [];
  if (members === 1)
    risks.push({ message: "Solo project — consider finding collaborators", severity: "warning" });
  if (data.status === "recruiting" && members < 3)
    risks.push({ message: "Team is small for the scope", severity: "info" });

  // Suggested builders based on detected roles
  const suggested: SuggestedBuilder[] = detectedRoles.slice(0, 2).map((role) => ({
    name: `${role.charAt(0).toUpperCase() + role.slice(1)} Developer`,
    role,
    match_score: 0.75,
  }));

  const summary =
    `This project uses ${detectedRoles.join(", ") || "general"} technologies.` +
    (gaps.length ? ` It may benefit from ${gaps.map((g) => g.role).join(" and ")} expertise.` : "");

  return {
    project_id: data.project_id,
    summary,
    suggested_builders: suggested,
    role_gaps: gaps,
    risk_alerts: risks,
  };
}

export const projectInsightsApi = {
  generate: async (data: ProjectInsightsRequest): Promise<ProjectInsightsResponse> => {
    if (!isBackendConfigured()) {
      return Promise.resolve(fallbackInsights(data));
    }
    return api.post<ProjectInsightsResponse>("/api/project-insights", data);
  },
};
