import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import {
  applyServiceWorkerUpdate,
  registerServiceWorker,
  shouldRegisterServiceWorker,
  unregisterServiceWorkers,
  watchForUpdates,
} from "@/lib/pwa";

/**
 * Minimal stand-in for a ServiceWorker that records its listeners so a test
 * can drive `statechange` by hand.
 */
function createFakeWorker(state = "installing") {
  const listeners: Record<string, Array<() => void>> = {};

  return {
    state,
    postMessage: vi.fn(),
    addEventListener: vi.fn((event: string, handler: () => void) => {
      (listeners[event] ??= []).push(handler);
    }),
    emit(event: string) {
      (listeners[event] ?? []).forEach((handler) => handler());
    },
    setState(next: string) {
      this.state = next;
    },
  };
}

function createFakeRegistration(overrides: Partial<Record<string, unknown>> = {}) {
  const listeners: Record<string, Array<() => void>> = {};

  return {
    waiting: null,
    installing: null,
    unregister: vi.fn().mockResolvedValue(true),
    addEventListener: vi.fn((event: string, handler: () => void) => {
      (listeners[event] ??= []).push(handler);
    }),
    emit(event: string) {
      (listeners[event] ?? []).forEach((handler) => handler());
    },
    ...overrides,
  };
}

function installServiceWorkerMock(controller: unknown = {}) {
  const register = vi.fn().mockResolvedValue(createFakeRegistration());

  Object.defineProperty(window.navigator, "serviceWorker", {
    configurable: true,
    value: {
      register,
      controller,
      getRegistrations: vi.fn().mockResolvedValue([]),
      addEventListener: vi.fn(),
    },
  });

  return register;
}

function removeServiceWorkerSupport() {
  // `delete` does not work on a defineProperty'd value, so shadow it instead.
  Object.defineProperty(window.navigator, "serviceWorker", {
    configurable: true,
    value: undefined,
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllEnvs();
  removeServiceWorkerSupport();
});

describe("shouldRegisterServiceWorker", () => {
  it("is false under test, where import.meta.env.PROD is false", () => {
    installServiceWorkerMock();

    expect(shouldRegisterServiceWorker()).toBe(false);
  });

  it("is true in a production build", () => {
    installServiceWorkerMock();
    vi.stubEnv("PROD", true);

    expect(shouldRegisterServiceWorker()).toBe(true);
  });

  it("is false when the browser has no service worker support", () => {
    removeServiceWorkerSupport();
    vi.stubEnv("PROD", true);

    expect(shouldRegisterServiceWorker()).toBe(false);
  });

  it("can be forced regardless of environment", () => {
    expect(shouldRegisterServiceWorker(true)).toBe(true);
  });
});

describe("registerServiceWorker", () => {
  it("does not register outside a production build", async () => {
    const register = installServiceWorkerMock();

    const result = await registerServiceWorker();

    expect(result).toBeNull();
    expect(register).not.toHaveBeenCalled();
  });

  it("registers at the root scope when forced", async () => {
    const register = installServiceWorkerMock();

    await registerServiceWorker({ force: true });

    expect(register).toHaveBeenCalledWith("/sw.js", { scope: "/" });
  });

  it("returns null instead of throwing when registration fails", async () => {
    const register = installServiceWorkerMock();
    register.mockRejectedValue(new Error("insecure origin"));
    vi.spyOn(console, "warn").mockImplementation(() => {});

    await expect(registerServiceWorker({ force: true })).resolves.toBeNull();
  });

  it("returns null when the browser has no support, even if forced", async () => {
    removeServiceWorkerSupport();

    await expect(registerServiceWorker({ force: true })).resolves.toBeNull();
  });
});

describe("watchForUpdates", () => {
  it("fires immediately when a worker is already waiting", () => {
    const registration = createFakeRegistration({ waiting: createFakeWorker() });
    const onUpdate = vi.fn();

    watchForUpdates(registration as never, onUpdate);

    expect(onUpdate).toHaveBeenCalledWith(registration);
  });

  it("fires when an update installs while the tab is open", () => {
    installServiceWorkerMock({ scriptURL: "/sw.js" });

    const installing = createFakeWorker();
    const registration = createFakeRegistration({ installing });
    const onUpdate = vi.fn();

    watchForUpdates(registration as never, onUpdate);
    registration.emit("updatefound");

    installing.setState("installed");
    installing.emit("statechange");

    expect(onUpdate).toHaveBeenCalledWith(registration);
  });

  it("does not fire on a first install", () => {
    // controller is null before any worker has ever controlled the page.
    // Announcing an "update" to a first-time visitor would be nonsense.
    installServiceWorkerMock(null);

    const installing = createFakeWorker();
    const registration = createFakeRegistration({ installing });
    const onUpdate = vi.fn();

    watchForUpdates(registration as never, onUpdate);
    registration.emit("updatefound");

    installing.setState("installed");
    installing.emit("statechange");

    expect(onUpdate).not.toHaveBeenCalled();
  });

  it("does not fire while the worker is still installing", () => {
    installServiceWorkerMock({ scriptURL: "/sw.js" });

    const installing = createFakeWorker("installing");
    const registration = createFakeRegistration({ installing });
    const onUpdate = vi.fn();

    watchForUpdates(registration as never, onUpdate);
    registration.emit("updatefound");
    installing.emit("statechange");

    expect(onUpdate).not.toHaveBeenCalled();
  });

  it("ignores an updatefound with no installing worker", () => {
    const registration = createFakeRegistration({ installing: null });
    const onUpdate = vi.fn();

    watchForUpdates(registration as never, onUpdate);

    expect(() => registration.emit("updatefound")).not.toThrow();
    expect(onUpdate).not.toHaveBeenCalled();
  });
});

describe("applyServiceWorkerUpdate", () => {
  beforeEach(() => {
    installServiceWorkerMock();
  });

  it("tells the waiting worker to activate", () => {
    const waiting = createFakeWorker("installed");
    const registration = createFakeRegistration({ waiting });

    applyServiceWorkerUpdate(registration as never);

    expect(waiting.postMessage).toHaveBeenCalledWith("SKIP_WAITING");
  });

  it("does nothing when no worker is waiting", () => {
    const registration = createFakeRegistration({ waiting: null });

    expect(() => applyServiceWorkerUpdate(registration as never)).not.toThrow();
    expect(window.navigator.serviceWorker.addEventListener).not.toHaveBeenCalled();
  });

  it("reloads only once, even if controllerchange fires repeatedly", () => {
    const waiting = createFakeWorker("installed");
    const registration = createFakeRegistration({ waiting });

    const handlers: Array<() => void> = [];
    (
      window.navigator.serviceWorker.addEventListener as ReturnType<typeof vi.fn>
    ).mockImplementation((event: string, handler: () => void) => {
      if (event === "controllerchange") handlers.push(handler);
    });

    const reload = vi.fn();
    Object.defineProperty(window, "location", {
      configurable: true,
      value: { ...window.location, reload },
    });

    applyServiceWorkerUpdate(registration as never);

    handlers.forEach((handler) => handler());
    handlers.forEach((handler) => handler());

    expect(reload).toHaveBeenCalledTimes(1);
  });
});

describe("unregisterServiceWorkers", () => {
  it("is a no-op without service worker support", async () => {
    removeServiceWorkerSupport();

    await expect(unregisterServiceWorkers()).resolves.toBeUndefined();
  });

  it("unregisters every registration", async () => {
    const first = createFakeRegistration();
    const second = createFakeRegistration();

    installServiceWorkerMock();
    (window.navigator.serviceWorker.getRegistrations as ReturnType<typeof vi.fn>).mockResolvedValue(
      [first, second],
    );

    Object.defineProperty(window, "caches", {
      configurable: true,
      value: {
        keys: vi.fn().mockResolvedValue(["devlink-assets-v1"]),
        delete: vi.fn().mockResolvedValue(true),
      },
    });

    await unregisterServiceWorkers();

    expect(first.unregister).toHaveBeenCalled();
    expect(second.unregister).toHaveBeenCalled();
    expect(window.caches.delete).toHaveBeenCalledWith("devlink-assets-v1");
  });
});
