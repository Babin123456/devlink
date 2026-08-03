import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { FilterDrawer, FilterSection } from "@/components/ui/filter-drawer";

beforeEach(() => {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });
});

const sampleSections: FilterSection[] = [
  {
    id: "language",
    title: "Language",
    type: "multi",
    options: [
      { label: "TypeScript", value: "ts" },
      { label: "Python", value: "py" },
      { label: "Rust", value: "rust" },
    ],
  },
  {
    id: "experience",
    title: "Experience Level",
    type: "select",
    options: [
      { label: "Beginner", value: "beginner" },
      { label: "Intermediate", value: "intermediate" },
      { label: "Advanced", value: "advanced" },
    ],
  },
  {
    id: "query",
    title: "Search Term",
    type: "search",
    placeholder: "Search tags...",
  },
];

describe("FilterDrawer", () => {
  it("renders when open is true", () => {
    render(
      <FilterDrawer
        open={true}
        onOpenChange={vi.fn()}
        sections={sampleSections}
        values={{}}
        onApply={vi.fn()}
        onReset={vi.fn()}
      />,
    );

    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(screen.getByText("Language")).toBeInTheDocument();
    expect(screen.getByText("TypeScript")).toBeInTheDocument();
  });

  it("does not render content when open is false", () => {
    render(
      <FilterDrawer
        open={false}
        onOpenChange={vi.fn()}
        sections={sampleSections}
        values={{}}
        onApply={vi.fn()}
        onReset={vi.fn()}
      />,
    );

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("handles multi-select filter selection and apply button click", async () => {
    const onApplyMock = vi.fn();
    const onOpenChangeMock = vi.fn();

    render(
      <FilterDrawer
        open={true}
        onOpenChange={onOpenChangeMock}
        sections={sampleSections}
        values={{ language: [] }}
        onApply={onApplyMock}
        onReset={vi.fn()}
      />,
    );

    const tsButton = screen.getByRole("button", { name: /language: typescript/i });
    await userEvent.click(tsButton);

    const applyButton = screen.getByRole("button", { name: /apply filters/i });
    await userEvent.click(applyButton);

    expect(onApplyMock).toHaveBeenCalledWith({
      language: ["ts"],
    });
    expect(onOpenChangeMock).toHaveBeenCalledWith(false);
  });

  it("resets filter selections when Reset button is clicked", async () => {
    const onResetMock = vi.fn();
    const onOpenChangeMock = vi.fn();

    render(
      <FilterDrawer
        open={true}
        onOpenChange={onOpenChangeMock}
        sections={sampleSections}
        values={{ language: ["ts"] }}
        onApply={vi.fn()}
        onReset={onResetMock}
      />,
    );

    const resetButton = screen.getByRole("button", { name: /reset all filters/i });
    await userEvent.click(resetButton);

    expect(onResetMock).toHaveBeenCalled();
    expect(onOpenChangeMock).toHaveBeenCalledWith(false);
  });
});
