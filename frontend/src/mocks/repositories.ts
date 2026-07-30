export interface RepositoryItem {
  id: string;
  name: string;
  description: string;
  stars: number;
  language: string;
  projectId: string;
}

export const repositories: RepositoryItem[] = [
  {
    id: "repo-1",
    name: "devlink/web-client",
    description: "DevLink core frontend React/TypeScript web application",
    stars: 142,
    language: "TypeScript",
    projectId: "p1",
  },
  {
    id: "repo-2",
    name: "devlink/api-server",
    description: "FastAPI REST and WebSocket backend services",
    stars: 98,
    language: "Python",
    projectId: "p2",
  },
  {
    id: "repo-3",
    name: "devlink/ai-matching-engine",
    description: "Machine learning model and vector search pipeline",
    stars: 76,
    language: "Python",
    projectId: "p2",
  },
  {
    id: "repo-4",
    name: "devlink/ui-design-system",
    description: "Accessible Tailwind CSS components and tokens",
    stars: 54,
    language: "TypeScript",
    projectId: "p5",
  },
  {
    id: "repo-5",
    name: "devlink/k8s-deployments",
    description: "Kubernetes manifests, Helm charts, and GitOps config",
    stars: 39,
    language: "Go",
    projectId: "p3",
  },
];
