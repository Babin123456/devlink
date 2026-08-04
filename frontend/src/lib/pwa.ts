/**
 * Service worker registration.
 *
 * Registration is deliberately narrow: production builds only, in a browser
 * that supports it, once per page load. A service worker in development is a
 * reliable way to spend an afternoon debugging a stale bundle, and in tests it
 * is simply noise.
 */

const SERVICE_WORKER_URL = "/sw.js";

export type ServiceWorkerUpdateHandler = (registration: ServiceWorkerRegistration) => void;

export interface RegisterServiceWorkerOptions {
  /**
   * Called when a new worker has installed and is waiting to take over,
   * i.e. a new version has been deployed while this tab was open.
   */
  onUpdateAvailable?: ServiceWorkerUpdateHandler;

  /**
   * Register even outside a production build. Only useful when deliberately
   * testing the worker itself.
   */
  force?: boolean;
}

/**
 * The browser's service worker container, or `null` where there isn't one.
 *
 * Checked by truthiness rather than `"serviceWorker" in navigator`: the key
 * can exist while holding `undefined` (jsdom, some embedded webviews, and
 * anything that has shimmed it), and an `in` check happily passes there before
 * blowing up on first use.
 */
function getServiceWorkerContainer(): ServiceWorkerContainer | null {
  if (typeof navigator === "undefined") return null;
  return navigator.serviceWorker ?? null;
}

/** Whether this environment should run a service worker at all. */
export function shouldRegisterServiceWorker(force = false): boolean {
  if (force) return true;
  if (typeof window === "undefined") return false;
  if (!getServiceWorkerContainer()) return false;

  // import.meta.env.PROD is false in dev and under Vitest.
  return import.meta.env.PROD === true;
}

/**
 * Register the service worker, resolving to the registration or `null` when
 * this environment should not have one.
 *
 * Never throws. A failed registration should degrade the app to "works exactly
 * as it did before", not break boot.
 */
export async function registerServiceWorker(
  options: RegisterServiceWorkerOptions = {},
): Promise<ServiceWorkerRegistration | null> {
  const { onUpdateAvailable, force = false } = options;

  if (!shouldRegisterServiceWorker(force)) return null;

  const container = getServiceWorkerContainer();
  if (!container) return null;

  try {
    const registration = await container.register(SERVICE_WORKER_URL, {
      scope: "/",
    });

    if (onUpdateAvailable) {
      watchForUpdates(registration, onUpdateAvailable);
    }

    return registration;
  } catch (error) {
    console.warn("[pwa] Service worker registration failed:", error);
    return null;
  }
}

/**
 * Watch a registration for a newly installed worker waiting to activate.
 *
 * Two cases have to be handled: a worker that is *already* waiting when we
 * attach (the update finished before this code ran), and one that arrives
 * later via `updatefound`.
 */
export function watchForUpdates(
  registration: ServiceWorkerRegistration,
  onUpdateAvailable: ServiceWorkerUpdateHandler,
): void {
  if (registration.waiting) {
    onUpdateAvailable(registration);
    return;
  }

  registration.addEventListener("updatefound", () => {
    const installing = registration.installing;
    if (!installing) return;

    installing.addEventListener("statechange", () => {
      // `controller` is null on the very first install. Without this check
      // every first-time visitor would be told an update is available.
      if (installing.state === "installed" && getServiceWorkerContainer()?.controller) {
        onUpdateAvailable(registration);
      }
    });
  });
}

/**
 * Tell a waiting worker to activate, then reload so the page is controlled by
 * the new version.
 */
export function applyServiceWorkerUpdate(registration: ServiceWorkerRegistration): void {
  if (!registration.waiting) return;

  const container = getServiceWorkerContainer();
  if (!container) return;

  registration.waiting.postMessage("SKIP_WAITING");

  // `controllerchange` fires once the new worker takes over. Guarding with a
  // flag because Chrome can fire it more than once, and a reload loop is a
  // spectacularly bad failure mode.
  let reloading = false;
  container.addEventListener("controllerchange", () => {
    if (reloading) return;
    reloading = true;
    window.location.reload();
  });
}

/**
 * Unregister every service worker and drop the caches.
 *
 * Not called by the app; kept as the escape hatch for when a bad worker gets
 * shipped and a user needs to be talked out of it from the console.
 */
export async function unregisterServiceWorkers(): Promise<void> {
  const container = getServiceWorkerContainer();
  if (!container) return;

  const registrations = await container.getRegistrations();
  await Promise.all(registrations.map((registration) => registration.unregister()));

  if (typeof caches !== "undefined") {
    const keys = await caches.keys();
    await Promise.all(keys.map((key) => caches.delete(key)));
  }
}
