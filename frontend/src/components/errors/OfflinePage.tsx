import { WifiOff } from "lucide-react";

import { ErrorLayout } from "./ErrorLayout";

export function OfflinePage() {
  return (
    <ErrorLayout
      icon={<WifiOff className="h-16 w-16 text-muted-foreground" />}
      title="You're Offline"
      description="Please check your internet connection and try again."
      primaryLabel="Retry"
      primaryTo="/"
    />
  );
}
