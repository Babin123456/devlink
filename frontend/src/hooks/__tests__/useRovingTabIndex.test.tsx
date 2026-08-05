import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { useRovingTabIndex, type RovingOrientation } from "../useRovingTabIndex";

const ITEMS = ["Bold", "Italic", "Strikethrough", "Code"];

function Toolbar({
  orientation = "horizontal",
  loop = true,
  typeahead = false,
}: {
  orientation?: RovingOrientation;
  loop?: boolean;
  typeahead?: boolean;
}) {
  const { containerRef, getItemProps, containerProps } = useRovingTabIndex<HTMLDivElement>({
    orientation,
    loop,
    typeahead,
  });

  return (
    <>
      <button>before</button>
      <div ref={containerRef} role="toolbar" {...containerProps}>
        {ITEMS.map((label, index) => (
          <button key={label} {...getItemProps(index)}>
            {label}
          </button>
        ))}
      </div>
      <button>after</button>
    </>
  );
}

describe("useRovingTabIndex", () => {
  it("exposes the group as a single tab stop", () => {
    // The point of the pattern: a six-item toolbar should cost one Tab press
    // to get past, not six.
    render(<Toolbar />);

    const stops = ITEMS.map((label) => screen.getByText(label).tabIndex);

    expect(stops).toEqual([0, -1, -1, -1]);
  });

  it("tabs past the whole group in one press", async () => {
    const user = userEvent.setup();
    render(<Toolbar />);

    screen.getByText("before").focus();
    await user.tab();
    expect(document.activeElement).toBe(screen.getByText("Bold"));

    await user.tab();
    expect(document.activeElement).toBe(screen.getByText("after"));
  });

  it("moves right and left with the arrow keys", async () => {
    const user = userEvent.setup();
    render(<Toolbar />);

    screen.getByText("Bold").focus();

    await user.keyboard("{ArrowRight}");
    expect(document.activeElement).toBe(screen.getByText("Italic"));

    await user.keyboard("{ArrowLeft}");
    expect(document.activeElement).toBe(screen.getByText("Bold"));
  });

  it("wraps at both ends when looping", async () => {
    const user = userEvent.setup();
    render(<Toolbar />);

    screen.getByText("Bold").focus();
    await user.keyboard("{ArrowLeft}");
    expect(document.activeElement).toBe(screen.getByText("Code"));

    await user.keyboard("{ArrowRight}");
    expect(document.activeElement).toBe(screen.getByText("Bold"));
  });

  it("stops at the ends when not looping", async () => {
    const user = userEvent.setup();
    render(<Toolbar loop={false} />);

    screen.getByText("Bold").focus();
    await user.keyboard("{ArrowLeft}");

    expect(document.activeElement).toBe(screen.getByText("Bold"));
  });

  it("ignores the cross-axis arrows for a horizontal group", async () => {
    // A horizontal toolbar must not swallow ArrowDown -- the page still needs
    // to scroll.
    const user = userEvent.setup();
    render(<Toolbar orientation="horizontal" />);

    screen.getByText("Bold").focus();
    await user.keyboard("{ArrowDown}");

    expect(document.activeElement).toBe(screen.getByText("Bold"));
  });

  it("uses up and down for a vertical group", async () => {
    const user = userEvent.setup();
    render(<Toolbar orientation="vertical" />);

    screen.getByText("Bold").focus();
    await user.keyboard("{ArrowDown}");

    expect(document.activeElement).toBe(screen.getByText("Italic"));
  });

  it("accepts both axes when orientation is both", async () => {
    const user = userEvent.setup();
    render(<Toolbar orientation="both" />);

    screen.getByText("Bold").focus();
    await user.keyboard("{ArrowDown}");
    expect(document.activeElement).toBe(screen.getByText("Italic"));

    await user.keyboard("{ArrowRight}");
    expect(document.activeElement).toBe(screen.getByText("Strikethrough"));
  });

  it("jumps to the ends with Home and End", async () => {
    const user = userEvent.setup();
    render(<Toolbar />);

    screen.getByText("Bold").focus();

    await user.keyboard("{End}");
    expect(document.activeElement).toBe(screen.getByText("Code"));

    await user.keyboard("{Home}");
    expect(document.activeElement).toBe(screen.getByText("Bold"));
  });

  it("follows focus when the user clicks into the middle", async () => {
    // Somebody can click or shift-tab straight into the middle of a group. If
    // the index does not follow, the next arrow press jumps back to wherever
    // the index was left.
    const user = userEvent.setup();
    render(<Toolbar />);

    await user.click(screen.getByText("Strikethrough"));
    await user.keyboard("{ArrowRight}");

    expect(document.activeElement).toBe(screen.getByText("Code"));
  });

  it("jumps by typed letter when typeahead is on", async () => {
    const user = userEvent.setup();
    render(<Toolbar typeahead />);

    screen.getByText("Bold").focus();
    await user.keyboard("c");

    expect(document.activeElement).toBe(screen.getByText("Code"));
  });

  it("does not typeahead when it is off", async () => {
    const user = userEvent.setup();
    render(<Toolbar />);

    screen.getByText("Bold").focus();
    await user.keyboard("c");

    expect(document.activeElement).toBe(screen.getByText("Bold"));
  });

  it("skips disabled items", async () => {
    const user = userEvent.setup();

    function WithDisabled() {
      const { containerRef, getItemProps, containerProps } = useRovingTabIndex<HTMLDivElement>();

      return (
        <div ref={containerRef} role="toolbar" {...containerProps}>
          <button {...getItemProps(0)}>one</button>
          <button {...getItemProps(1)} disabled>
            two
          </button>
          <button {...getItemProps(2)}>three</button>
        </div>
      );
    }

    render(<WithDisabled />);

    screen.getByText("one").focus();
    await user.keyboard("{ArrowRight}");

    expect(document.activeElement).toBe(screen.getByText("three"));
  });
});
