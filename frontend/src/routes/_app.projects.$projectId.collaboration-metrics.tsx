/* eslint-disable @typescript-eslint/ban-ts-comment */
// @ts-nocheck
import { createFileRoute } from '@tanstack/react-router';
import { ProjectCollaborationMetrics } from '@/components/project/ProjectCollaborationMetrics';

export const Route = createFileRoute('/_app/projects/$projectId/collaboration-metrics')({
  component: ProjectCollaborationMetricsPage,
});

function ProjectCollaborationMetricsPage() {
  const { projectId } = Route.useParams();
  return (
    <div className="container mx-auto py-8 px-4">
      <ProjectCollaborationMetrics projectId={Number(projectId) || 1} />
    </div>
  );
}
