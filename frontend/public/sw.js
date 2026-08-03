/**
 * DevLink service worker.
 *
 * Hand-rolled rather than generated, because what we need is small and the
 * generated variety tends to bring a build plugin, a config file and a set of
 * defaults nobody on the team can explain.
 *
 * Two strategies:
 *
 *   - Build assets (`/_build/`, `/assets/`, `/icons/`) are content-hashed and
 *     therefore immutable, so they are served cache-first.
 *   - Navigations are network-first with a cache fallback, so a dropped
 *     connection lands on the last-seen shell (or the offline page) instead of
 *     the browser's dinosaur.
 *
 * Everything else -- crucially every API call -- is left alone and goes
 * straight to the network.
 *
 * Bump CACHE_VERSION to invalidate every cache on the next deploy.
 */

const CACHE_VERSION = "v1";
const ASSET_CACHE = `devlink-assets-${CACHE_VERSION}`;
const PAGE_CACHE = `devlink-pages-${CACHE_VERSION}`;
const OFFLINE_URL = "/offline.html";

/** Prefixes whose contents are immutable and safe to serve cache-first. */
const IMMUTABLE_PREFIXES = ["/_build/", "/assets/", "/icons/"];

/**
 * Never cached. API responses are user-scoped and frequently mutated; serving
 * a stale one is worse than failing the request. Auth is excluded outright.
 */
const NEVER_CACHE_PREFIXES = ["/api/", "/uploads/"];

/** How many navigation responses to retain before evicting the oldest. */
const MAX_PAGE_ENTRIES = 40;

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(PAGE_CACHE)
      .then((cache) => cache.addAll([OFFLINE_URL]))
      // Take over as soon as the new worker is ready rather than waiting for
      // every old tab to close.
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((key) => key !== ASSET_CACHE && key !== PAGE_CACHE)
            .map((key) => caches.delete(key)),
        ),
      )
      // Without this, the freshly activated worker would not control the page
      // that registered it until the next navigation.
      .then(() => self.clients.claim()),
  );
});

self.addEventListener("message", (event) => {
  // Lets the page tell a waiting worker to activate immediately, which is how
  // the "reload to update" prompt in src/lib/pwa.ts works.
  if (event.data === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

self.addEventListener("fetch", (event) => {
  const { request } = event;

  // Only GET is cacheable, and only same-origin. Cross-origin requests are
  // opaque, so caching them would fill storage with responses we cannot read.
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (NEVER_CACHE_PREFIXES.some((prefix) => url.pathname.startsWith(prefix))) {
    return;
  }

  if (request.mode === "navigate") {
    event.respondWith(networkFirst(request));
    return;
  }

  if (IMMUTABLE_PREFIXES.some((prefix) => url.pathname.startsWith(prefix))) {
    event.respondWith(cacheFirst(request));
  }
});

/**
 * Serve from cache, falling back to the network and storing what comes back.
 * Only used for content-hashed URLs, so a cache hit can never be stale.
 */
async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;

  const response = await fetch(request);

  if (response.ok) {
    const cache = await caches.open(ASSET_CACHE);
    cache.put(request, response.clone());
  }

  return response;
}

/**
 * Try the network, fall back to whatever we have, then to the offline page.
 *
 * Network-first rather than cache-first because a stale app shell that no
 * longer matches the deployed API is a worse experience than a slightly slower
 * navigation.
 */
async function networkFirst(request) {
  try {
    const response = await fetch(request);

    if (response.ok) {
      const cache = await caches.open(PAGE_CACHE);
      cache.put(request, response.clone());
      trimCache(PAGE_CACHE, MAX_PAGE_ENTRIES);
    }

    return response;
  } catch (error) {
    const cached = await caches.match(request);
    if (cached) return cached;

    const offline = await caches.match(OFFLINE_URL);
    if (offline) return offline;

    // Nothing cached at all -- first visit while offline.
    return new Response("You are offline.", {
      status: 503,
      statusText: "Offline",
      headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
  }
}

/**
 * Evict oldest entries once a cache grows past `maxEntries`.
 *
 * `cache.keys()` returns insertion order, so the front of the list is the
 * least recently added.
 */
async function trimCache(cacheName, maxEntries) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();

  if (keys.length <= maxEntries) return;

  await Promise.all(keys.slice(0, keys.length - maxEntries).map((key) => cache.delete(key)));
}
