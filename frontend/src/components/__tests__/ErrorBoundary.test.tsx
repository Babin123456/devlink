import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { SectionErrorBoundary } from "../errors/SectionErrorBoundary";

function ProblematicComponent({ shouldThrow }: { shouldThrow?: boolean }) {
  if (shouldThrow) {
    throw new Error("Test runtime failure");
  }
  return <div>Normal Content</div>;
}

describe("SectionErrorBoundary", () => {
  const consoleErrorSpy = vi.spyOn(console, "error").mockImplementation(() => {});

  afterEach(() => {
    consoleErrorSpy.mockClear();
  });

  it("renders children when no error occurs", () => {
    render(
      <SectionErrorBoundary sectionName="TestSection">
        <ProblematicComponent shouldThrow={false} />
      </SectionErrorBoundary>,
    );

    expect(screen.getByText("Normal Content")).toBeInTheDocument();
  });

  it("renders friendly fallback UI when children throw an error", () => {
    render(
      <SectionErrorBoundary sectionName="TestSection">
        <ProblematicComponent shouldThrow={true} />
      </SectionErrorBoundary>,
    );

    expect(screen.getByText("Something went wrong in TestSection")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /try again/i })).toBeInTheDocument();
  });

  it("calls onRetry callback and attempts to reset error boundary on retry button click", () => {
    const onRetryMock = vi.fn();

    render(
      <SectionErrorBoundary sectionName="TestSection" onRetry={onRetryMock}>
        <ProblematicComponent shouldThrow={true} />
      </SectionErrorBoundary>,
    );

    const retryButton = screen.getByRole("button", { name: /try again/i });
    fireEvent.click(retryButton);

    expect(onRetryMock).toHaveBeenCalledTimes(1);
  });
});
