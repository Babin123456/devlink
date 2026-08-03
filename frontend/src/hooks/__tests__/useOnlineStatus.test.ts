import { act, renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { useOnlineStatus } from "@/hooks/useOnlineStatus";

/** jsdom leaves navigator.onLine writable only via defineProperty. */
function setOnLine(value: boolean | undefined) {
  Object.defineProperty(window.navigator, "onLine", {
    configurable: true,
    value,
  });
}

afterEach(() => {
  setOnLine(true);
  vi.restoreAllMocks();
});

describe("useOnlineStatus", () => {
  it("reports online when the browser is connected", () => {
    setOnLine(true);

    const { result } = renderHook(() => useOnlineStatus());

    expect(result.current).toBe(true);
  });

  it("reports offline when the browser is disconnected", () => {
    setOnLine(false);

    const { result } = renderHook(() => useOnlineStatus());

    expect(result.current).toBe(false);
  });

  it("treats an undefined navigator.onLine as online", () => {
    // Some environments never set the property. Defaulting to offline there
    // would show the banner permanently.
    setOnLine(undefined);

    const { result } = renderHook(() => useOnlineStatus());

    expect(result.current).toBe(true);
  });

  it("flips to offline when the offline event fires", () => {
    setOnLine(true);
    const { result } = renderHook(() => useOnlineStatus());

    act(() => {
      setOnLine(false);
      window.dispatchEvent(new Event("offline"));
    });

    expect(result.current).toBe(false);
  });

  it("flips back to online when the online event fires", () => {
    setOnLine(false);
    const { result } = renderHook(() => useOnlineStatus());

    act(() => {
      setOnLine(true);
      window.dispatchEvent(new Event("online"));
    });

    expect(result.current).toBe(true);
  });

  it("removes its listeners on unmount", () => {
    const removeSpy = vi.spyOn(window, "removeEventListener");

    const { unmount } = renderHook(() => useOnlineStatus());
    unmount();

    const removed = removeSpy.mock.calls.map(([event]) => event);
    expect(removed).toContain("online");
    expect(removed).toContain("offline");
  });

  it("does not update after unmount", () => {
    setOnLine(true);
    const { result, unmount } = renderHook(() => useOnlineStatus());

    unmount();

    act(() => {
      setOnLine(false);
      window.dispatchEvent(new Event("offline"));
    });

    // The last rendered value stands; no state update on an unmounted hook.
    expect(result.current).toBe(true);
  });
});
