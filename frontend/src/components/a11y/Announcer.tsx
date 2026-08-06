import { createContext, useCallback, useContext, useMemo, useRef, useState } from "react";
import type { ReactNode } from "react";

export type Urgency = "polite" | "assertive";

interface AnnouncerContextValue {
  announce: (message: string, urgency?: Urgency) => void;
}

const AnnouncerContext = createContext<AnnouncerContextValue | null>(null);

/**
 * Screen readers only re-announce a live region when its **text changes**.
 * Announcing the same string twice -- "3 results", then "3 results" again
 * after a different search -- produces silence the second time, and the user
 * concludes nothing happened.
 *
 * Appending a zero-width space makes the text technically different while
 * being inaudible and invisible. It is the standard workaround, and it is the
 * kind of thing every hand-rolled live region rediscovers the hard way.
 *
 * Written as an escape rather than a literal, so it is visible to whoever
 * reads this file next.
 */
const ZERO_WIDTH_SPACE = "\u200B";

function differentiate(previous: string, next: string): string {
  return previous === next ? `${next}${ZERO_WIDTH_SPACE}` : next;
}

/**
 * Mounts the two live regions and provides `announce`.
 *
 * Two regions rather than one, because `aria-live` cannot be changed on the
 * fly reliably -- most screen readers read the attribute when the region is
 * first seen, so flipping it between polite and assertive on an existing
 * region has no effect.
 *
 * Mount this once, near the root.
 */
export function AnnouncerProvider({ children }: { children: ReactNode }) {
  const [polite, setPolite] = useState("");
  const [assertive, setAssertive] = useState("");

  const lastPolite = useRef("");
  const lastAssertive = useRef("");

  const announce = useCallback((message: string, urgency: Urgency = "polite") => {
    if (!message) return;

    if (urgency === "assertive") {
      const next = differentiate(lastAssertive.current, message);
      lastAssertive.current = next;
      setAssertive(next);
      return;
    }

    const next = differentiate(lastPolite.current, message);
    lastPolite.current = next;
    setPolite(next);
  }, []);

  const value = useMemo(() => ({ announce }), [announce]);

  return (
    <AnnouncerContext.Provider value={value}>
      {children}
      <LiveRegion urgency="polite" message={polite} />
      <LiveRegion urgency="assertive" message={assertive} />
    </AnnouncerContext.Provider>
  );
}

function LiveRegion({ urgency, message }: { urgency: Urgency; message: string }) {
  return (
    <div
      // `aria-atomic` makes the reader announce the whole region rather than
      // diffing it, which is what we want for a self-contained status message.
      aria-atomic="true"
      aria-live={urgency}
      // `role="status"` and `role="alert"` are what older screen readers
      // actually respond to; aria-live alone is not enough on all of them.
      role={urgency === "assertive" ? "alert" : "status"}
      // Not `hidden` and not `display: none` -- either removes the region from
      // the accessibility tree, which is exactly what we do not want. This is
      // the standard visually-hidden recipe: present, sized to nothing, and
      // clipped.
      style={{
        position: "absolute",
        width: 1,
        height: 1,
        margin: -1,
        padding: 0,
        overflow: "hidden",
        clip: "rect(0, 0, 0, 0)",
        whiteSpace: "nowrap",
        border: 0,
      }}
    >
      {message}
    </div>
  );
}

/**
 * Announce a message to screen reader users.
 *
 * Use `"polite"` (the default) for anything the user can catch up on --
 * "Saved", "12 results". Use `"assertive"` only when the current utterance
 * should be interrupted, which in practice means errors that block what the
 * user was doing.
 *
 * Falls back to a no-op outside a provider, so a component using it is still
 * usable in isolation and in tests that do not care about announcements.
 */
export function useAnnouncer(): AnnouncerContextValue {
  const context = useContext(AnnouncerContext);

  const fallback = useMemo<AnnouncerContextValue>(
    () => ({
      announce: () => {
        /* no provider mounted; announcing is a no-op rather than a crash */
      },
    }),
    [],
  );

  return context ?? fallback;
}
