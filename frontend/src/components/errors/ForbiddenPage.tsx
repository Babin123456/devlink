import { ShieldAlert } from "lucide-react";

import { ErrorLayout } from "./ErrorLayout";

export function ForbiddenPage() {
  return (
    <ErrorLayout
      icon={<ShieldAlert className="h-16 w-16 text-destructive" />}
      title="403 • Forbidden"
      description="You don't have permission to access this resource."
    />
  );
}
