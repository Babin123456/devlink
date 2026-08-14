import { useState, useEffect } from "react";

/**
 * Reactive wrapper around window.matchMedia.
 * Returns true when the media query matches.
 *
 * @example
 * const isTablet = useMediaQuery("(min-width: 768px) and (max-width: 1279px)");
 */
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(() => {
    if (typeof window === "undefined") return false;
    return window.matchMedia(query).matches;
  });

  useEffect(() => {
    const mql = window.matchMedia(query);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mql.addEventListener("change", handler);
    setMatches(mql.matches);
    return () => mql.removeEventListener("change", handler);
  }, [query]);

  return matches;
}
