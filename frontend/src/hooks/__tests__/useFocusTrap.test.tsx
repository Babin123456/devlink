import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { describe, expect, it, vi } from "vitest";

import { useFocusTrap } from "../useFocusTrap";

function Dialog({
  active,
  onEscape,
  extra,
}: {
  active: boolean;
  onEscape?: () => void;
  extra?: boolean;
}) {
  const ref = useFocusTrap<HTMLDivElement>({ active, onEscape });

  return (
    <div ref={ref} role="dialog">
      <button>first</button>
      <button>middle</button>
      {extra ? <button>added later</button> : null}
      <button>last</button>
    </div>
  );
}

function Page({ extra = false, onEscape }: { extra?: boolean; onEscape?: () => void }) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button onClick={() => setOpen(true)}>open</button>
      <button>outside</button>
      {open ? <Dialog active onEscape={onEscape ?? (() => setOpen(false))} extra={extra} /> : null}
    </>
  );
}

describe("useFocusTrap", () => {
  it("moves focus into the container when it activates", async () => {
    const user = userEvent.setup();
    render(<Page />);

    await user.click(screen.getByText("open"));

    expect(document.activeElement).toBe(screen.getByText("first"));
  });

  it("wraps forward from the last element to the first", async () => {
    const user = userEvent.setup();
    render(<Page />);
    await user.click(screen.getByText("open"));

    screen.getByText("last").focus();
    await user.tab();

    expect(document.activeElement).toBe(screen.getByText("first"));
  });

  it("wraps backward from the first element to the last", async () => {
    const user = userEvent.setup();
    render(<Page />);
    await user.click(screen.getByText("open"));

    screen.getByText("first").focus();
    await user.tab({ shift: true });

    expect(document.activeElement).toBe(screen.getByText("last"));
  });

  it("keeps focus inside across a full cycle", async () => {
    // The failure this guards against is subtle: focus escaping into the page
    // behind an overlay, where the user is typing into something covered.
    const user = userEvent.setup();
    render(<Page />);
    await user.click(screen.getByText("open"));

    const dialog = screen.getByRole("dialog");

    for (let i = 0; i < 8; i += 1) {
      await user.tab();
      expect(dialog.contains(document.activeElement)).toBe(true);
    }
  });

  it("pulls focus back when it has escaped the container", async () => {
    const user = userEvent.setup();
    render(<Page />);
    await user.click(screen.getByText("open"));

    // Simulates a click on something behind the overlay, or a script moving
    // focus out from under us.
    screen.getByText("outside").focus();
    await user.tab();

    expect(screen.getByRole("dialog").contains(document.activeElement)).toBe(true);
  });

  it("notices elements added after the trap opened", async () => {
    // The edges are recomputed per keypress rather than cached on open,
    // because dialog content changes -- validation errors, disclosures,
    // buttons becoming enabled.
    const user = userEvent.setup();
    render(<Page extra />);
    await user.click(screen.getByText("open"));

    screen.getByText("last").focus();
    await user.tab();

    expect(document.activeElement).toBe(screen.getByText("first"));

    screen.getByText("first").focus();
    await user.tab({ shift: true });

    expect(document.activeElement).toBe(screen.getByText("last"));
  });

  it("calls onEscape when Escape is pressed", async () => {
    const onEscape = vi.fn();
    const user = userEvent.setup();

    render(<Page onEscape={onEscape} />);
    await user.click(screen.getByText("open"));

    await user.keyboard("{Escape}");

    expect(onEscape).toHaveBeenCalledTimes(1);
  });

  it("restores focus to the trigger when it closes", async () => {
    // Without this, focus falls to <body> and the next Tab starts from the top
    // of the document instead of from the button the user just used.
    const user = userEvent.setup();

    function Closable() {
      const [open, setOpen] = useState(false);
      return (
        <>
          <button onClick={() => setOpen(true)}>trigger</button>
          {open ? <Dialog active onEscape={() => setOpen(false)} /> : null}
        </>
      );
    }

    render(<Closable />);

    const trigger = screen.getByText("trigger");
    await user.click(trigger);
    expect(document.activeElement).not.toBe(trigger);

    await user.keyboard("{Escape}");

    expect(document.activeElement).toBe(trigger);
  });

  it("does nothing while inactive", async () => {
    const user = userEvent.setup();

    render(
      <>
        <button>outside</button>
        <Dialog active={false} />
      </>,
    );

    screen.getByText("outside").focus();
    await user.tab();

    // No trap, so Tab behaves normally and leaves the button.
    expect(document.activeElement).not.toBe(screen.getByText("outside"));
  });
});
