import { useCallback, useEffect, useRef } from "react";

import { focusFirst, getTabbableEdges } from "@/lib/a11y/tabbable";

export interface UseFocusTrapOptions {
  /** Whether the trap is active. Usually the dialog's open state. */
  active: boolean;
  /** Move focus into the container when the trap activates. Default `true`. */
  autoFocus?: boolean;
  /** Restore focus to the previously focused element on release. Default `true`. */
  restoreFocus?: boolean;
  /** Called when Escape is pressed while the trap is active. */
  onEscape?: () => void;
}

/**
 * Keep Tab and Shift+Tab inside a container while it is open.
 *
 * Without this, a modal is only visually modal: press Tab enough times and
 * focus walks out of the dialog and into the page behind it, which is still
 * there, still focusable, and covered by an overlay. The user is now typing
 * into something they cannot see.
 *
 * Two things this does that a minimal version does not:
 *
 * - **Restores focus on release.** Closing a dialog without restoring drops
 *   focus to `<body>`, so the next Tab starts from the top of the document
 *   rather than from the button the user just pressed.
 * - **Recomputes the edges on every keypress** rather than caching them when
 *   the trap opens. Dialog content changes -- a validation error appears, a
 *   disclosure expands, a button becomes enabled -- and a cached last element
 *   sends focus to something that is no longer there.
 */
export function useFocusTrap<T extends HTMLElement = HTMLElement>({
  active,
  autoFocus = true,
  restoreFocus = true,
  onEscape,
}: UseFocusTrapOptions) {
  const containerRef = useRef<T | null>(null);
  const previouslyFocused = useRef<HTMLElement | null>(null);

  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onEscape?.();
        return;
      }

      if (event.key !== "Tab") return;

      const container = containerRef.current;
      if (!container) return;

      // Recomputed per keypress on purpose; see the docstring.
      const edges = getTabbableEdges(container);

      if (!edges) {
        // Nothing to tab to. Swallow the key so focus cannot escape into the
        // page behind an empty dialog.
        event.preventDefault();
        return;
      }

      const activeElement = container.ownerDocument.activeElement as HTMLElement | null;

      // Focus may be outside the container entirely -- the user clicked
      // something behind the overlay, or a script moved it. Pull it back
      // rather than letting the wrap logic no-op.
      if (!activeElement || !container.contains(activeElement)) {
        event.preventDefault();
        (event.shiftKey ? edges.last : edges.first).focus();
        return;
      }

      if (event.shiftKey && activeElement === edges.first) {
        event.preventDefault();
        edges.last.focus();
        return;
      }

      if (!event.shiftKey && activeElement === edges.last) {
        event.preventDefault();
        edges.first.focus();
      }
    },
    [onEscape],
  );

  useEffect(() => {
    if (!active) return;

    const container = containerRef.current;
    if (!container) return;

    const doc = container.ownerDocument;

    previouslyFocused.current = doc.activeElement as HTMLElement | null;

    if (autoFocus) {
      focusFirst(container);
    }

    doc.addEventListener("keydown", handleKeyDown, true);

    return () => {
      doc.removeEventListener("keydown", handleKeyDown, true);

      if (restoreFocus) {
        const target = previouslyFocused.current;
        // The element may have been removed while the dialog was open -- a
        // row deleted, a list re-rendered -- so check it is still in the
        // document before trying to focus it.
        if (target && doc.contains(target)) {
          target.focus();
        }
      }
    };
  }, [active, autoFocus, restoreFocus, handleKeyDown]);

  return containerRef;
}
