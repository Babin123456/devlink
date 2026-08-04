# Progressive Web App

DevLink ships a small PWA layer: a web app manifest, a service worker, an
offline fallback page, and an in-app offline indicator.

The goal is modest and deliberately so. This is not an offline-first rewrite.
It makes the app installable, stops a dropped connection producing the
browser's default error page, and tells the user when they are offline instead
of letting mutations fail silently.

## What's included

| File                              | Purpose                                          |
| :-------------------------------- | :----------------------------------------------- |
| `public/manifest.webmanifest`     | Name, colours, icons, app shortcuts               |
| `public/sw.js`                    | The service worker                                |
| `public/offline.html`             | Fallback page when a navigation fails             |
| `public/icons/icon.svg`           | App icon                                          |
| `public/icons/icon-maskable.svg`  | Maskable variant, scaled for the 80% safe zone    |
| `src/lib/pwa.ts`                  | Registration and update handling                  |
| `src/hooks/useOnlineStatus.ts`    | Connectivity hook                                 |
| `src/components/OfflineBanner.tsx`| The banner                                        |

## Caching strategy

The worker only touches same-origin `GET` requests. Everything else goes
straight to the network.

**Cache-first — `/_build/`, `/assets/`, `/icons/`**
These URLs are content-hashed, so a cache hit can never be stale. A new deploy
produces new filenames.

**Network-first — navigations**
Try the network, fall back to the cached shell, then to `offline.html`. Not
cache-first: a stale app shell paired with a newer API is a worse failure than
a slightly slower navigation.

**Never cached — `/api/`, `/uploads/`**
API responses are user-scoped and change constantly; serving a stale one is
worse than failing the request. Caching an authenticated response also risks
handing it to the wrong user on a shared device.

The page cache is capped at 40 entries, evicting oldest-first.

## Updates

When a deploy lands while a tab is open, the new worker installs and waits.
`src/lib/pwa.ts` detects that and the app shows a toast with a **Reload**
action, which posts `SKIP_WAITING` to the waiting worker and reloads once it
takes over.

Users are never force-reloaded mid-task. The `controllerchange` handler is
guarded by a flag, because Chrome can fire it more than once and a reload loop
is a spectacularly bad failure mode.

`activate` deletes every cache that is not the current version, so deploys do
not leak storage. Bumping `CACHE_VERSION` in `sw.js` invalidates everything.

## Registration

Only in **production browser builds**:

```ts
registerServiceWorker({ onUpdateAvailable: (registration) => { ... } });
```

Not in dev — a service worker there is a reliable way to spend an afternoon
debugging a stale bundle — and not under Vitest. Pass `force: true` when
deliberately testing the worker.

Registration never throws. A failure degrades the app to exactly how it behaved
before the worker existed.

## Offline indicator

`useOnlineStatus()` wraps `navigator.onLine` and the `online`/`offline` events.
It is a coarse signal — it reports whether a network interface is up, not
whether our API is reachable — but it fires immediately when Wi-Fi drops, which
is enough to explain a failed action.

It defaults to `true` during SSR and when `navigator.onLine` is `undefined`, so
the banner never flashes on a healthy load.

## Testing it locally

The worker does not run in `vite dev`. Use a production build:

```bash
npm run build
npm run preview
```

Then in DevTools:

- **Application → Manifest** — check installability
- **Application → Service Workers** — confirm registration and activation
- **Network → Offline**, then reload — you should get the app shell, or
  `offline.html` on a route never visited

## Not included

Background sync and push notifications are deliberately out of scope. Both need
a server-side story (a VAPID key pair, a subscription store, a delivery
pipeline) and belong with the notification work, not here.
