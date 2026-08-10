/* eslint-disable @typescript-eslint/ban-ts-comment */
// @ts-nocheck
import { createFileRoute } from '@tanstack/react-router';
import { LoadingLibraryShowcase } from '@/components/ui/loading/LoadingLibraryShowcase';

export const Route = createFileRoute('/_app/loading-states')({
  component: LoadingStatesPage,
});

function LoadingStatesPage() {
  return (
    <div className="container mx-auto py-8 px-4">
      <LoadingLibraryShowcase />
    </div>
  );
}
