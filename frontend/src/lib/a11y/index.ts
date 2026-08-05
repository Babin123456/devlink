/**
 * Shared accessibility primitives.
 *
 * Import from here rather than reaching into the individual files, so the
 * surface stays small and the next person building a menu finds all of it in
 * one place instead of writing a sixth focus trap.
 *
 * See `docs/accessibility.md`.
 */

export {
  focusFirst,
  getTabbableEdges,
  getTabbableElements,
  isFocusable,
  isTabbable,
} from "./tabbable";
