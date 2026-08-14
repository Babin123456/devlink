import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { AnnouncerProvider, useAnnouncer } from "../Announcer";
import { SkipLink } from "../SkipLink";

function Trigger({ message, urgency }: { message: string; urgency?: "polite" | "assertive" }) {
  const { announce } = useAnnouncer();

  return <button onClick={() => announce(message, urgency)}>say</button>;
}

describe("AnnouncerProvider", () => {
  it("mounts a polite and an assertive live region", () => {
    render(
      <AnnouncerProvider>
        <span>content</span>
      </AnnouncerProvider>,
    );

    // Two regions rather than one, because aria-live is read when the region
    // is first seen -- flipping it on an existing region does nothing.
    expect(screen.getByRole("status")).toHaveAttribute("aria-live", "polite");
    expect(screen.getByRole("alert")).toHaveAttribute("aria-live", "assertive");
  });

  it("puts a polite message in the status region", async () => {
    const user = userEvent.setup();

    render(
      <AnnouncerProvider>
        <Trigger message="Saved" />
      </AnnouncerProvider>,
    );

    await user.click(screen.getByText("say"));

    expect(screen.getByRole("status")).toHaveTextContent("Saved");
    expect(screen.getByRole("alert")).toHaveTextContent("");
  });

  it("puts an assertive message in the alert region", async () => {
    const user = userEvent.setup();

    render(
      <AnnouncerProvider>
        <Trigger message="Upload failed" urgency="assertive" />
      </AnnouncerProvider>,
    );

    await user.click(screen.getByText("say"));

    expect(screen.getByRole("alert")).toHaveTextContent("Upload failed");
    expect(screen.getByRole("status")).toHaveTextContent("");
  });

  it("changes the text when the same message is announced twice", async () => {
    // Screen readers only re-announce when the text *changes*. Saying "3
    // results" twice would be silent the second time, and the user concludes
    // nothing happened. A zero-width space makes it technically different.
    const user = userEvent.setup();

    render(
      <AnnouncerProvider>
        <Trigger message="3 results" />
      </AnnouncerProvider>,
    );

    const button = screen.getByText("say");
    const region = screen.getByRole("status");

    await user.click(button);
    const first = region.textContent;

    await user.click(button);
    const second = region.textContent;

    expect(second).not.toBe(first);
    // Still reads as the same sentence to a person.
    expect(region).toHaveTextContent("3 results");
  });

  it("ignores an empty message", async () => {
    const user = userEvent.setup();

    render(
      <AnnouncerProvider>
        <Trigger message="" />
      </AnnouncerProvider>,
    );

    await user.click(screen.getByText("say"));

    expect(screen.getByRole("status")).toHaveTextContent("");
  });

  it("keeps the live regions out of sight but in the accessibility tree", () => {
    render(
      <AnnouncerProvider>
        <span>content</span>
      </AnnouncerProvider>,
    );

    const region = screen.getByRole("status");

    // `hidden` or `display: none` would remove it from the accessibility
    // tree, which is exactly what we do not want.
    expect(region).not.toHaveAttribute("hidden");
    expect(region.style.position).toBe("absolute");
    expect(region.style.overflow).toBe("hidden");
  });
});

describe("useAnnouncer outside a provider", () => {
  it("is a no-op rather than a crash", async () => {
    // A component using announce() should still be usable in isolation and in
    // tests that do not care about announcements.
    const user = userEvent.setup();

    render(<Trigger message="nobody is listening" />);

    await expect(user.click(screen.getByText("say"))).resolves.not.toThrow();
  });
});

describe("SkipLink", () => {
  it("renders a link to the main content", () => {
    render(<SkipLink />);

    expect(screen.getByRole("link")).toHaveAttribute("href", "#main-content");
  });

  it("stays in the tab order while visually hidden", () => {
    // display:none would remove it from the tab order and defeat the point.
    render(<SkipLink />);

    expect(screen.getByRole("link").className).toContain("sr-only");
    expect(screen.getByRole("link").className).toContain("focus:not-sr-only");
  });

  it("moves focus to the target, not just the scroll position", async () => {
    // A bare href="#main" scrolls but does not move focus unless the target is
    // focusable -- so the next Tab would start from the top of the document
    // again and the user is back where they began.
    const user = userEvent.setup();

    render(
      <>
        <SkipLink />
        <main id="main-content">
          <button>first thing</button>
        </main>
      </>,
    );

    await user.click(screen.getByRole("link"));

    const main = document.getElementById("main-content")!;
    expect(main.getAttribute("tabindex")).toBe("-1");
    expect(document.activeElement).toBe(main);
  });

  it("does nothing when the target is missing", async () => {
    const user = userEvent.setup();

    render(<SkipLink targetId="not-here" />);

    await expect(user.click(screen.getByRole("link"))).resolves.not.toThrow();
  });

  it("accepts a custom target and label", () => {
    render(<SkipLink targetId="results">Skip to results</SkipLink>);

    const link = screen.getByRole("link");

    expect(link).toHaveAttribute("href", "#results");
    expect(link).toHaveTextContent("Skip to results");
  });
});
