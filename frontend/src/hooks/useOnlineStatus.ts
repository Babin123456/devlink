import { useEffect, useState } from "react";

/**
 * Track browser connectivity.
 *
 * `navigator.onLine` is a coarse signal — it reports whether the machine has a
 * network interface up, not whether our API is reachable — but it is the only
 * thing that fires synchronously when a laptop's Wi-Fi drops, and it is enough
 * to explain to the user why their last action failed.
 *
 * Defaults to `true` during SSR and before the first effect, so the offline
 * banner never flashes on a perfectly healthy page load.
 */
export function useOnlineStatus(): boolean {
  const [isOnline, setIsOnline] = useState<boolean>(() => {
    if (typeof navigator === "undefined") return true;
    // Some environments (jsdom included) leave onLine undefined rather than
    // false; treating that as "offline" would be wrong.
    return navigator.onLine !== false;
  });

  useEffect(() => {
    if (typeof window === "undefined") return;

    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    // Connectivity can change between the initial render and this effect
    // running, so re-read rather than trusting the initial state.
    setIsOnline(navigator.onLine !== false);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  return isOnline;
}
