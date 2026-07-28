import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { UserAvatar } from "@/components/user-avatar";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const DEMO_SRC = "https://example.com/avatar.png";

// ---------------------------------------------------------------------------
// Image & initials fallback
// ---------------------------------------------------------------------------

describe("UserAvatar — image & initials fallback", () => {
  it("renders an img element when src is provided", () => {
    render(<UserAvatar src={DEMO_SRC} name="Ada Lovelace" />);
    expect(screen.getByRole("img")).toBeInTheDocument();
  });

  it("img has the correct src attribute", () => {
    render(<UserAvatar src={DEMO_SRC} name="Ada Lovelace" />);
    expect(screen.getByRole("img")).toHaveAttribute("src", DEMO_SRC);
  });

  it("img aria-label uses name when no alt is passed", () => {
    render(<UserAvatar src={DEMO_SRC} name="Ada Lovelace" />);
    expect(screen.getByRole("img", { name: "Ada Lovelace" })).toBeInTheDocument();
  });

  it("img aria-label uses the alt prop when provided", () => {
    render(<UserAvatar src={DEMO_SRC} name="Ada Lovelace" alt="Profile photo" />);
    expect(screen.getByRole("img", { name: "Profile photo" })).toBeInTheDocument();
  });

  it("shows 'AL' initials for 'Ada Lovelace' when no src", () => {
    render(<UserAvatar name="Ada Lovelace" />);
    expect(screen.getByText("AL")).toBeInTheDocument();
  });

  it("shows single-word initials (first two chars) for one-word names", () => {
    render(<UserAvatar name="Linus" />);
    expect(screen.getByText("LI")).toBeInTheDocument();
  });

  it("shows '?' fallback when name is undefined", () => {
    render(<UserAvatar />);
    expect(screen.getByText("?")).toBeInTheDocument();
  });

  it("honours the initials override prop", () => {
    render(<UserAvatar name="Ada Lovelace" initials="XX" />);
    expect(screen.getByText("XX")).toBeInTheDocument();
  });
});

// ---------------------------------------------------------------------------
// Online status indicator
// ---------------------------------------------------------------------------

describe("UserAvatar — status indicator", () => {
  it("renders a status dot when status='online'", () => {
    render(<UserAvatar name="Ada Lovelace" status="online" />);
    expect(screen.getByRole("status")).toBeInTheDocument();
  });

  it("status dot label reflects the status value", () => {
    render(<UserAvatar name="Ada Lovelace" status="away" />);
    expect(screen.getByRole("status")).toHaveAccessibleName("Status: away");
  });

  it("status='online' dot has bg-emerald-500 class", () => {
    render(<UserAvatar name="Ada Lovelace" status="online" />);
    expect(screen.getByRole("status")).toHaveClass("bg-emerald-500");
  });

  it("status='away' dot has bg-amber-500 class", () => {
    render(<UserAvatar name="Ada Lovelace" status="away" />);
    expect(screen.getByRole("status")).toHaveClass("bg-amber-500");
  });

  it("status='busy' dot has bg-red-500 class", () => {
    render(<UserAvatar name="Ada Lovelace" status="busy" />);
    expect(screen.getByRole("status")).toHaveClass("bg-red-500");
  });

  it("status='offline' dot uses muted colour class", () => {
    render(<UserAvatar name="Ada Lovelace" status="offline" />);
    expect(screen.getByRole("status")).toHaveClass("bg-muted-foreground/50");
  });

  it("status={true} shorthand maps to online — dot is rendered", () => {
    render(<UserAvatar name="Ada Lovelace" status={true} />);
    expect(screen.getByRole("status")).toHaveClass("bg-emerald-500");
  });

  it("status={false} hides the dot", () => {
    render(<UserAvatar name="Ada Lovelace" status={false} />);
    expect(screen.queryByRole("status")).not.toBeInTheDocument();
  });

  it("no status prop hides the dot", () => {
    render(<UserAvatar name="Ada Lovelace" />);
    expect(screen.queryByRole("status")).not.toBeInTheDocument();
  });
});

// ---------------------------------------------------------------------------
// Verification badge
// ---------------------------------------------------------------------------

describe("UserAvatar — verification badge", () => {
  it("renders the verified badge when verified=true", () => {
    render(<UserAvatar name="Ada Lovelace" verified />);
    expect(screen.getByLabelText("Verified")).toBeInTheDocument();
  });

  it("does not render the badge when verified is omitted", () => {
    render(<UserAvatar name="Ada Lovelace" />);
    expect(screen.queryByLabelText("Verified")).not.toBeInTheDocument();
  });

  it("does not render the badge when verified=false", () => {
    render(<UserAvatar name="Ada Lovelace" verified={false} />);
    expect(screen.queryByLabelText("Verified")).not.toBeInTheDocument();
  });

  it("aria-label on the outer span includes ', verified' when verified and named", () => {
    render(<UserAvatar name="Ada Lovelace" verified />);
    // The AvatarFallback aria-label reflects the resolved label
    expect(screen.getByLabelText("Ada Lovelace, verified")).toBeInTheDocument();
  });

  it("can combine verified and status together", () => {
    render(<UserAvatar name="Ada Lovelace" verified status="online" />);
    expect(screen.getByLabelText("Verified")).toBeInTheDocument();
    expect(screen.getByRole("status")).toBeInTheDocument();
  });
});

// ---------------------------------------------------------------------------
// Size presets
// ---------------------------------------------------------------------------

describe("UserAvatar — size presets", () => {
  const sizes = ["xs", "sm", "md", "lg", "xl", "2xl"] as const;

  sizes.forEach((size) => {
    it(`renders without crashing at size="${size}"`, () => {
      const { container } = render(<UserAvatar name="Test User" size={size} />);
      expect(container.firstChild).toBeInTheDocument();
    });
  });

  it("defaults to md size when size prop is omitted", () => {
    const { container } = render(<UserAvatar name="Test User" />);
    // The Avatar element inside should have h-10 w-10 (md preset)
    expect(container.querySelector(".h-10.w-10")).toBeInTheDocument();
  });

  it("applies h-6 w-6 classes for size='xs'", () => {
    const { container } = render(<UserAvatar name="Test User" size="xs" />);
    expect(container.querySelector(".h-6.w-6")).toBeInTheDocument();
  });

  it("applies h-24 w-24 classes for size='2xl'", () => {
    const { container } = render(<UserAvatar name="Test User" size="2xl" />);
    expect(container.querySelector(".h-24.w-24")).toBeInTheDocument();
  });
});

// ---------------------------------------------------------------------------
// Accessibility & composability
// ---------------------------------------------------------------------------

describe("UserAvatar — accessibility & composability", () => {
  it("forwards additional className to the root span", () => {
    const { container } = render(
      <UserAvatar name="Ada Lovelace" className="ring-2 ring-background" />,
    );
    expect(container.firstChild).toHaveClass("ring-2", "ring-background");
  });

  it("forwards arbitrary HTML attributes via ...props", () => {
    render(<UserAvatar name="Ada Lovelace" data-testid="my-avatar" />);
    expect(screen.getByTestId("my-avatar")).toBeInTheDocument();
  });

  it("root element is a span (not a div or button)", () => {
    const { container } = render(<UserAvatar name="Ada Lovelace" />);
    expect(container.firstChild?.nodeName).toBe("SPAN");
  });
});
