import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { ProfileViewersList } from "../ProfileViewersList";

describe("ProfileViewersList Component (#593)", () => {
  it("renders visitor history and total viewer counts", () => {
    render(<ProfileViewersList totalViewers={25} />);
    expect(screen.getByText("Recent Profile Visitors")).toBeInTheDocument();
    expect(screen.getByText("25 developers viewed your profile recently.")).toBeInTheDocument();
    expect(screen.getByText("Sarah Chen")).toBeInTheDocument();
    expect(screen.getByText("Anonymous Developer")).toBeInTheDocument();
  });

  it("handles privacy opt-out toggle", () => {
    const handleToggle = vi.fn();
    render(<ProfileViewersList hideProfileViews={false} onTogglePrivacy={handleToggle} />);

    const toggleBtn = screen.getByRole("switch");
    fireEvent.click(toggleBtn);

    expect(handleToggle).toHaveBeenCalledWith(true);
  });

  it("handles pagination controls", () => {
    const handlePageChange = vi.fn();
    render(<ProfileViewersList currentPage={1} totalPages={3} onPageChange={handlePageChange} />);

    const nextBtn = screen.getByRole("button", { name: /Next/i });
    fireEvent.click(nextBtn);

    expect(handlePageChange).toHaveBeenCalledWith(2);
  });
});
