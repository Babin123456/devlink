import { api, isBackendConfigured } from "../client";

export interface TechStackRecommendation {
  name: string;
  category: string;
  reason: string;
  confidence: number;
}

export interface TechStackResponse {
  project_idea: string;
  recommendations: TechStackRecommendation[];
  summary?: string | null;
}

const KEYWORD_STACKS: Record<
  string,
  { name: string; category: string; reason: string; confidence: number }[]
> = {
  food: [
    {
      name: "React",
      category: "frontend",
      reason: "Component-based UI ideal for product catalogs and real-time order tracking.",
      confidence: 0.85,
    },
    {
      name: "FastAPI",
      category: "backend",
      reason: "Async Python framework handles concurrent orders and real-time updates.",
      confidence: 0.8,
    },
    {
      name: "PostgreSQL",
      category: "database",
      reason: "Reliable storage for orders, users, inventory, and payments.",
      confidence: 0.85,
    },
    {
      name: "Redis",
      category: "cache",
      reason: "Caches sessions, carts, and real-time order status.",
      confidence: 0.75,
    },
  ],
  chat: [
    {
      name: "React",
      category: "frontend",
      reason: "Component architecture ideal for real-time chat interfaces.",
      confidence: 0.85,
    },
    {
      name: "Node.js",
      category: "backend",
      reason: "Event-driven architecture handles many concurrent WebSocket connections.",
      confidence: 0.85,
    },
    {
      name: "Redis",
      category: "cache",
      reason: "Pub/Sub powers real-time message broadcasting.",
      confidence: 0.8,
    },
  ],
  ai: [
    {
      name: "Python",
      category: "backend",
      reason: "Rich ML/AI ecosystem (scikit-learn, PyTorch, TensorFlow).",
      confidence: 0.9,
    },
    {
      name: "FastAPI",
      category: "backend",
      reason: "Async support serves ML inference without blocking.",
      confidence: 0.85,
    },
    {
      name: "PostgreSQL",
      category: "database",
      reason: "Structured storage with JSON support for flexible schemas.",
      confidence: 0.8,
    },
  ],
};

const DEFAULT_STACK = [
  {
    name: "React",
    category: "frontend",
    reason: "Industry-standard component library with a huge ecosystem.",
    confidence: 0.8,
  },
  {
    name: "FastAPI",
    category: "backend",
    reason: "Modern, fast Python framework with automatic OpenAPI docs.",
    confidence: 0.8,
  },
  {
    name: "PostgreSQL",
    category: "database",
    reason: "Battle-tested relational database with strong performance.",
    confidence: 0.85,
  },
  {
    name: "Docker",
    category: "devops",
    reason: "Standard containerization for reproducible deployments.",
    confidence: 0.75,
  },
];

export function fallbackTechStack(projectIdea: string): TechStackResponse {
  const text = projectIdea.toLowerCase();
  const matches = new Map<string, TechStackRecommendation>();
  for (const [kw, stack] of Object.entries(KEYWORD_STACKS)) {
    if (text.includes(kw)) {
      for (const rec of stack) matches.set(rec.name, rec);
    }
  }
  if (matches.size === 0) {
    for (const rec of DEFAULT_STACK) matches.set(rec.name, rec);
  }
  return {
    project_idea: projectIdea,
    recommendations: [...matches.values()],
    summary: "Rule-based suggestions generated offline because the backend is unreachable.",
  };
}

export const recommendationsApi = {
  recommendTechStack: (projectIdea: string): Promise<TechStackResponse> => {
    if (!isBackendConfigured()) {
      return Promise.resolve(fallbackTechStack(projectIdea));
    }
    return api.post<TechStackResponse>("/recommendations/tech-stack", {
      project_idea: projectIdea,
    });
  },
  builders: (query?: { project_id?: string; limit?: number }) =>
    api.get<{ results: unknown[] }>("/recommendations/builders", { query }),
};
