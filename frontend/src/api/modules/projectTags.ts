import { api, isBackendConfigured } from "../client";

export interface TagSuggestion {
  name: string;
  confidence: number;
}

export interface ProjectTagResponse {
  tags: TagSuggestion[];
}

export interface ProjectTagRequest {
  title: string;
  description: string;
  tech_stack?: string;
}

function fallbackTags(data: ProjectTagRequest): ProjectTagResponse {
  const text = `${data.title} ${data.description} ${data.tech_stack ?? ""}`.toLowerCase();
  const keywords: Record<string, { name: string; confidence: number }[]> = {
    ai: [{ name: "AI", confidence: 0.85 }],
    "machine learning": [{ name: "Machine Learning", confidence: 0.85 }],
    nlp: [{ name: "NLP", confidence: 0.85 }],
    fastapi: [{ name: "FastAPI", confidence: 0.75 }],
    react: [{ name: "React", confidence: 0.75 }],
    python: [{ name: "Python", confidence: 0.75 }],
    javascript: [{ name: "JavaScript", confidence: 0.75 }],
    typescript: [{ name: "TypeScript", confidence: 0.75 }],
    node: [{ name: "Node.js", confidence: 0.75 }],
    backend: [{ name: "Backend", confidence: 0.7 }],
    frontend: [{ name: "Frontend", confidence: 0.7 }],
    api: [{ name: "API", confidence: 0.7 }],
    database: [{ name: "Database", confidence: 0.7 }],
    web: [{ name: "Web", confidence: 0.7 }],
    mobile: [{ name: "Mobile", confidence: 0.7 }],
  };
  const found: Map<string, { name: string; confidence: number }> = new Map();
  for (const [kw, tags] of Object.entries(keywords)) {
    if (text.includes(kw)) {
      for (const t of tags) {
        if (!found.has(t.name)) found.set(t.name, t);
      }
    }
  }
  if (found.size === 0) {
    found.set("Web", { name: "Web", confidence: 0.5 });
    found.set("Full Stack", { name: "Full Stack", confidence: 0.4 });
  }
  return { tags: [...found.values()] };
}

export const projectTagsApi = {
  generate: async (data: ProjectTagRequest): Promise<ProjectTagResponse> => {
    if (!isBackendConfigured()) {
      return fallbackTags(data);
    }
    return api.post<ProjectTagResponse>("/api/project-tags", data);
  },
};
