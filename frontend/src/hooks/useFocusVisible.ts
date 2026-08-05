import { useEffect, useState } from "react";

/**
 * Whether the user is currently navigating by keyboard.
 *
 * `:focus-visible` covers most cases in CSS and should be preferred. This hook
 * exists for the cases CSS cannot reach: deciding whether to *render* a focus
 * affordance at all, whether to scroll a newly focused item into view, or
 * whether to open a menu on focus.
 *
 * The heuristic is the same one the browser uses: a keydown that could move
 * focus means keyboard, a pointer interaction means not. Tracked at the
 * document level with capture, so it sees the event before anything can stop
 * its propagation.
 */
export function useFocusVisible(): boolean {
  const [isKeyboard, setIsKeyboard] = useState(false);

  useEffect(() => {
    // Guarded rather than assumed: this app server-renders, and `document` is
    // not there during SSR.
    if (typeof document === "undefined") return;

    const onKeyDown = (event: KeyboardEvent) => {
      // A modifier on its own is not navigation, and neither is Ctrl+S.
      if (event.metaKey || event.altKey || event.ctrlKey) return;
      setIsKeyboard(true);
    };

    const onPointerDown = () => setIsKeyboard(false);

    document.addEventListener("keydown", onKeyDown, true);
    document.addEventListener("mousedown", onPointerDown, true);
    document.addEventListener("pointerdown", onPointerDown, true);
    document.addEventListener("touchstart", onPointerDown, true);

    return () => {
      document.removeEventListener("keydown", onKeyDown, true);
      document.removeEventListener("mousedown", onPointerDown, true);
      document.removeEventListener("pointerdown", onPointerDown, true);
      document.removeEventListener("touchstart", onPointerDown, true);
    };
  }, []);

  return isKeyboard;
}
