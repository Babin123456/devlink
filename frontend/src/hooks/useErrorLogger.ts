import { useCallback } from "react";
import { reportLovableError } from "@/lib/lovable-error-reporting";

export interface ErrorLogPayload {
  error: Error;
  errorInfo?: React.ErrorInfo | { componentStack?: string };
  sectionName?: string;
  metadata?: Record<string, unknown>;
}

export function useErrorLogger() {
  const logError = useCallback(
    ({ error, errorInfo, sectionName = "unknown_section", metadata }: ErrorLogPayload) => {
      console.error(`[ErrorBoundary:${sectionName}] Captured runtime error:`, error, errorInfo);

      reportLovableError(error, {
        boundary: `section_${sectionName}`,
        componentStack: errorInfo?.componentStack ?? "",
        ...metadata,
      });
    },
    [],
  );

  return { logError };
}
