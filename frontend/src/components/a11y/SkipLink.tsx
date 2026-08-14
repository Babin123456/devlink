import type { MouseEvent } from "react";

export interface SkipLinkProps {
  /** Id of the element to jump to, without the `#`. */
  targetId?: string;
  children?: React.ReactNode;
}

/**
 * The first thing in the tab order: a link straight to the main content.
 *
 * Without one, a keyboard user landing on any page has to tab through the
 * entire sidebar and header before reaching what they came for. On the
 * dashboard that is roughly forty stops, on **every single navigation**.
 *
 * Visually hidden until focused, then it appears. That is the whole pattern:
 * `display: none` would remove it from the tab order and defeat the point, so
 * it is clipped instead.
 */
export function SkipLink({
  targetId = "main-content",
  children = "Skip to main content",
}: SkipLinkProps) {
  /**
   * A bare `href="#main-content"` moves the *scroll position* but not focus,
   * unless the target is focusable. So the target gets `tabindex="-1"` on
   * demand and is focused explicitly -- otherwise the next Tab press starts
   * from the top of the document again and the user is back where they began.
   */
  const handleClick = (event: MouseEvent<HTMLAnchorElement>) => {
    const target = document.getElementById(targetId);
    if (!target) return;

    event.preventDefault();

    if (!target.hasAttribute("tabindex")) {
      target.setAttribute("tabindex", "-1");
    }

    target.focus();

    // Focusing usually scrolls on its own; this just makes sure the target
    // lands at the top rather than wherever the browser chose. Guarded
    // because it is not implemented in every environment (jsdom, notably) and
    // it is a refinement, not the point of the link.
    target.scrollIntoView?.({ block: "start" });
  };

  return (
    <a
      href={`#${targetId}`}
      onClick={handleClick}
      className={[
        // Clipped rather than hidden: it has to stay in the tab order.
        "sr-only",
        // focus:not-sr-only undoes the clipping once it is reached.
        "focus:not-sr-only",
        "focus:fixed focus:left-4 focus:top-4 focus:z-[100]",
        "focus:rounded-md focus:bg-primary focus:px-4 focus:py-2",
        "focus:text-sm focus:font-semibold focus:text-primary-foreground",
        "focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
      ].join(" ")}
    >
      {children}
    </a>
  );
}
