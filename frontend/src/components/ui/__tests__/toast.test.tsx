import { renderHook, act } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { useToast, toast } from "../use-toast";

vi.mock("sonner", () => ({
  toast: Object.assign(vi.fn(), {
    success: vi.fn(),
    error: vi.fn(),
    warning: vi.fn(),
    info: vi.fn(),
    dismiss: vi.fn(),
  }),
}));

describe("Centralized Toast System (#589)", () => {
  it("should provide toast helpers for all notification types (Success, Error, Warning, Info)", () => {
    act(() => {
      toast.success("Saved successfully");
      toast.error("Operation failed");
      toast.warning("Check your network connection");
      toast.info("Update available");
    });

    const { result } = renderHook(() => useToast());
    expect(result.current.toasts).toHaveLength(4);
    expect(result.current.toasts[0].type).toBe("info");
    expect(result.current.toasts[1].type).toBe("warning");
    expect(result.current.toasts[2].type).toBe("error");
    expect(result.current.toasts[3].type).toBe("success");
  });

  it("should support configurable duration and queued notifications", () => {
    act(() => {
      toast({ title: "Custom toast", duration: 8000, type: "info" });
    });

    const { result } = renderHook(() => useToast());
    const latest = result.current.toasts[0];
    expect(latest.duration).toBe(8000);
    expect(latest.title).toBe("Custom toast");
  });
});
