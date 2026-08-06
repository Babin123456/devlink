import { useCallback, useEffect, useRef, useState } from "react";

import { getTabbableElements, isFocusable } from "@/lib/a11y/tabbable";

export type RovingOrientation = "horizontal" | "vertical" | "both";

export interface UseRovingTabIndexOptions {
  /** Which arrow keys move between items. Default `"horizontal"`. */
  orientation?: RovingOrientation;
  /** Wrap from the last item to the first. Default `true`. */
  loop?: boolean;
  /** Jump to an item by typing the start of its text. Default `false`. */
  typeahead?: boolean;
  /** Index focused when the group is first reached. Default `0`. */
  defaultIndex?: number;
}

/** How long a typeahead buffer stays alive between keystrokes. */
const TYPEAHEAD_TIMEOUT_MS = 500;

/**
 * Make a group of controls behave as a single tab stop.
 *
 * A toolbar, tab list, menu or segmented control should be **one** stop in the
 * page's tab order, with arrow keys moving between its items. Ours are
 * currently N stops, so tabbing through a page with a six-item toolbar costs
 * six presses to get past it.
 *
 * This is the "roving tabindex" pattern from the WAI-ARIA authoring practices:
 * exactly one item carries `tabIndex={0}` and the rest carry `-1`, and the
 * index moves as the user arrows around.
 *
 * ```tsx
 * const { containerRef, getItemProps } = useRovingTabIndex({ orientation: "horizontal" });
 *
 * <div ref={containerRef} role="toolbar">
 *   {items.map((item, i) => <button key={item.id} {...getItemProps(i)}>{item.label}</button>)}
 * </div>
 * ```
 */
export function useRovingTabIndex<T extends HTMLElement = HTMLElement>({
  orientation = "horizontal",
  loop = true,
  typeahead = false,
  defaultIndex = 0,
}: UseRovingTabIndexOptions = {}) {
  const containerRef = useRef<T | null>(null);
  const [activeIndex, setActiveIndex] = useState(defaultIndex);

  const typeaheadBuffer = useRef("");
  const typeaheadTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const items = useCallback((): HTMLElement[] => {
    const container = containerRef.current;
    if (!container) return [];

    // Items carry tabIndex={-1} while inactive, which makes them focusable but
    // not tabbable -- so getTabbableElements would return only the active one.
    // Query the group's own children instead and filter on focusability.
    return Array.from(container.querySelectorAll<HTMLElement>("[data-roving-item]")).filter(
      isFocusable,
    );
  }, []);

  const focusIndex = useCallback(
    (index: number) => {
      const list = items();
      if (list.length === 0) return;

      let next = index;

      if (next < 0) next = loop ? list.length - 1 : 0;
      if (next >= list.length) next = loop ? 0 : list.length - 1;

      setActiveIndex(next);
      list[next]?.focus();
    },
    [items, loop],
  );

  const runTypeahead = useCallback(
    (char: string) => {
      if (typeaheadTimer.current) clearTimeout(typeaheadTimer.current);

      typeaheadBuffer.current += char.toLowerCase();

      typeaheadTimer.current = setTimeout(() => {
        typeaheadBuffer.current = "";
      }, TYPEAHEAD_TIMEOUT_MS);

      const list = items();
      const query = typeaheadBuffer.current;

      // Search from the item after the current one and wrap, so repeatedly
      // typing "s" cycles through every item starting with S rather than
      // sticking on the first.
      const ordered = [...list.slice(activeIndex + 1), ...list.slice(0, activeIndex + 1)];

      const match = ordered.find((item) =>
        (item.textContent ?? "").trim().toLowerCase().startsWith(query),
      );

      if (match) focusIndex(list.indexOf(match));
    },
    [activeIndex, focusIndex, items],
  );

  const handleKeyDown = useCallback(
    (event: React.KeyboardEvent) => {
      const horizontal = orientation === "horizontal" || orientation === "both";
      const vertical = orientation === "vertical" || orientation === "both";

      switch (event.key) {
        case "ArrowRight":
          if (!horizontal) return;
          event.preventDefault();
          focusIndex(activeIndex + 1);
          return;
        case "ArrowLeft":
          if (!horizontal) return;
          event.preventDefault();
          focusIndex(activeIndex - 1);
          return;
        case "ArrowDown":
          if (!vertical) return;
          event.preventDefault();
          focusIndex(activeIndex + 1);
          return;
        case "ArrowUp":
          if (!vertical) return;
          event.preventDefault();
          focusIndex(activeIndex - 1);
          return;
        case "Home":
          event.preventDefault();
          focusIndex(0);
          return;
        case "End":
          event.preventDefault();
          focusIndex(items().length - 1);
          return;
        default:
          break;
      }

      // Single printable characters only; modifiers mean the user is reaching
      // for a shortcut, not typing a label.
      if (typeahead && event.key.length === 1 && !event.metaKey && !event.ctrlKey) {
        runTypeahead(event.key);
      }
    },
    [activeIndex, focusIndex, items, orientation, runTypeahead, typeahead],
  );

  useEffect(() => {
    return () => {
      if (typeaheadTimer.current) clearTimeout(typeaheadTimer.current);
    };
  }, []);

  /**
   * Props for each item. Spread onto the element.
   *
   * `onFocus` matters as much as the keyboard handling: a user can click or
   * shift-tab straight into the middle of the group, and if the index does not
   * follow, the next arrow press jumps back to wherever the index was left.
   */
  const getItemProps = useCallback(
    (index: number) => ({
      "data-roving-item": "",
      tabIndex: index === activeIndex ? 0 : -1,
      onFocus: () => setActiveIndex(index),
    }),
    [activeIndex],
  );

  return {
    containerRef,
    activeIndex,
    setActiveIndex,
    focusIndex,
    getItemProps,
    /** Spread onto the group container. */
    containerProps: { onKeyDown: handleKeyDown },
  };
}

/** Re-exported so callers do not need a second import for the common case. */
export { getTabbableElements };
