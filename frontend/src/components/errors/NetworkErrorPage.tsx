import { GlobeX } from "lucide-react";

import { ErrorLayout } from "./ErrorLayout";

export function NetworkErrorPage() {
  return (
    <ErrorLayout
      icon={<GlobeX className="h-16 w-16 text-warning" />}
      title="Network Error"
      description="We couldn't reach the server. Please try again."
      primaryLabel="Retry"
      primaryTo="/"
    />
  );
}
