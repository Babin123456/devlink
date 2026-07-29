import { Lock } from "lucide-react";

import { ErrorLayout } from "./ErrorLayout";

export function UnauthorizedPage() {
  return (
    <ErrorLayout
      icon={<Lock className="h-16 w-16 text-warning" />}
      title="401 • Unauthorized"
      description="You need to sign in to access this page."
      primaryLabel="Go to Login"
      primaryTo="/auth"
    />
  );
}
