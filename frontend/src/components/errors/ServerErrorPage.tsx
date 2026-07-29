import { TriangleAlert } from "lucide-react";

import { ErrorLayout } from "./ErrorLayout";

export function ServerErrorPage() {
  return (
    <ErrorLayout
      icon={<TriangleAlert className="h-16 w-16 text-warning" />}
      title="500 • Server Error"
      description="Something went wrong on our end. Please try again in a few moments."
    />
  );
}
