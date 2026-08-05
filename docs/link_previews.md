# Link Previews

Turns a URL somebody pasted into a title, description, site name and image, so
the reader can tell what a link is before clicking it.

## Endpoints

Both require authentication.

### `GET /api/link-previews?url=<url>`

Returns metadata for one URL.

```json
{
  "url": "https://example.com/blog/shipping-faster",
  "final_url": "https://example.com/blog/shipping-faster",
  "title": "Shipping faster without breaking things",
  "description": "How we cut our deploy time from 40 minutes to 4.",
  "site_name": "Example Engineering",
  "image_url": "https://example.com/img/shipping.png"
}
```

| Status | Meaning |
| --- | --- |
| `200` | Metadata found. Any individual field may still be `null`. |
| `400` | The URL is one we refuse to fetch. The `detail` says which rule it broke. |
| `404` | The URL was fetchable but yielded nothing — unreachable, timed out, or not HTML. |
| `429` | Rate limited (30/minute). |

### `POST /api/link-previews/batch`

Up to 10 URLs in one round trip. Always `200`; each entry carries either a
`preview` or an `error`, so one dead link in a message does not cost the reader
every other card in it.

```json
{
  "results": [
    { "url": "https://example.com/a", "preview": { "title": "…" } },
    { "url": "http://10.0.0.1/", "error": "That host resolves to a non-public address." }
  ]
}
```

Rate limited to 10/minute, because each call is up to ten outbound requests.

## Where the metadata comes from

For each field, the first source that yields a value wins:

| Field | Order |
| --- | --- |
| `title` | `og:title` → `twitter:title` → `<title>` |
| `description` | `og:description` → `twitter:description` → `<meta name="description">` |
| `site_name` | `og:site_name` → `application-name` |
| `image_url` | `og:image` → `twitter:image` |
| `final_url` | `og:url` → the URL after redirects |

`og:url` is preferred for `final_url` because it is the page's own canonical
spelling of itself, which is a better thing to store than whatever redirect
chain we happened to follow.

Relative image paths resolve against the **final** URL, not the submitted one.
Values are HTML-entity-decoded, whitespace-collapsed, and truncated (200
characters for a title, 500 for a description) on a word boundary where one is
nearby.

## The safety rules

This endpoint makes our server fetch a URL the caller chose, from inside our
network. Unguarded, that is a server-side request forgery hole: the caller
would get to read the cloud metadata endpoint, internal admin panels, and every
service on the private subnet, using our source address.

`app/utils/url_safety.py` enforces:

1. **Scheme allowlist** — `http` and `https` only.
2. **Port allowlist** — 80, 443, 8080, 8443.
3. **No credentials in the URL** — a phishing vector on its own, and we have no
   reason to forward them.
4. **Resolved-address checks** — the hostname is resolved and *every* returned
   address must be public. Loopback, link-local (including `169.254.169.254`),
   RFC 1918, unique-local, reserved, multicast and unspecified are all refused,
   for IPv4, IPv6, and IPv4-mapped IPv6.
5. **Length cap** — 2048 characters.

Point 4 is the one that matters most, and it is why the check resolves rather
than pattern-matching the hostname. `127.0.0.1.nip.io` is an ordinary public
name that resolves to loopback, and there is a whole family of such services.
Checking *all* resolved addresses matters too: a name with one public A record
and one private AAAA record is a working attack if only the first answer is
inspected, since nothing in this code chooses which one the HTTP client uses.

`app/services/link_preview_service.py` adds the fetch-time rules:

6. **Redirects are followed by hand**, and every hop is re-validated. A public
   URL that 302s to `http://169.254.169.254/latest/meta-data/` is refused at
   the second hop. `follow_redirects=True` would walk straight onto it.
7. **The body is streamed and capped** at 512 KiB, so a hostile server cannot
   make us buffer a gigabyte. Everything we want is in `<head>`.
8. **Only HTML content types are parsed.**
9. **Short timeouts** (5s) and a bounded hop count (3).

## Caching

Successful previews are cached for 24 hours; failures for 5 minutes. Without
this, a link pasted into a busy conversation is fetched once per reader. The
cache key is a normalised spelling of the URL — lowercased scheme and host,
redundant port dropped, fragment dropped — so links that differ only in those
respects share one entry.

Failures get a much shorter TTL so a site that was down for five minutes is not
written off for a day.

## Configuration

| Setting | Default | Notes |
| --- | --- | --- |
| `LINK_PREVIEW_TIMEOUT_SECONDS` | `5.0` | A slow site gets no card rather than a slow card. |
| `LINK_PREVIEW_MAX_BYTES` | `524288` | 512 KiB. |
| `LINK_PREVIEW_MAX_REDIRECTS` | `3` | A cost ceiling; each hop is re-validated regardless. |
| `LINK_PREVIEW_CACHE_TTL_SECONDS` | `86400` | |
| `LINK_PREVIEW_FAILURE_CACHE_TTL_SECONDS` | `300` | |
| `LINK_PREVIEW_USER_AGENT` | `DevLinkBot/1.0 (+…)` | Identifying ourselves honestly is what lets a site owner rate-limit us instead of blackholing us. |

## Reusing the guard

Any future feature that fetches a user-supplied URL — webhook delivery, avatar
import, repository metadata — should go through `validate_outbound_url` rather
than growing its own check.

```python
from app.utils.url_safety import UnsafeURL, validate_outbound_url

try:
    target = validate_outbound_url(url)
except UnsafeURL as exc:
    raise HTTPException(status_code=400, detail=str(exc))
```

`is_safe_outbound_url` and `filter_safe_urls` are boolean and list forms of the
same rules.
