# Calendar Feeds

DevLink knows about two kinds of dated commitment — hackathons a user has
registered for, and milestones on projects they are a member of. This exposes
both as iCalendar (RFC 5545), the format Google Calendar, Apple Calendar and
Outlook all understand.

## Two shapes, two problems

**A single-event download** works offline, works when the user is not signed in
on their phone, and creates no ongoing relationship with us. Good for an "Add
to calendar" button.

**A subscribable feed** is a URL the user pastes into their calendar client
once. The client then polls it forever and their DevLink dates stay in sync
without them doing anything. This is the one people actually want.

## Endpoints

| Endpoint | Auth | Purpose |
| --- | --- | --- |
| `GET /api/calendar/feed-token` | Session | Mint a feed token and return the subscribe URL |
| `GET /api/calendar/events.ics?token=…` | Feed token | The subscribable feed |
| `GET /api/calendar/hackathons/{id}.ics` | Session | One hackathon |
| `GET /api/calendar/milestones/{id}.ics` | Session | One milestone |

The single-event endpoints send `Content-Disposition: attachment`, which is
what makes a browser hand the file to the calendar application instead of
rendering it as text. The feed endpoint deliberately does **not** — it is polled
by a subscription, and an attachment header turns every manual visit into a
download prompt.

## Why the feed needs its own token

Calendar clients do not do OAuth. They do "GET this URL, forever, with no
headers I control". So the feed cannot use a session cookie or a bearer token;
the secret has to live in the URL.

The token is:

* **Scoped.** It authenticates nothing except the calendar feed. A leaked feed
  URL exposes the user's hackathon and milestone titles, and nothing else — no
  messages, no profile edits, no session.
* **Signed.** HMAC-SHA256 over the version, user id and issue time, using a key
  derived from `SECRET_KEY` and `CALENDAR_FEED_TOKEN_SALT`. Deriving rather
  than using `SECRET_KEY` directly means a feed token can never be confused
  with a session token even if one format changes later.
* **Expiring.** A year by default, so a URL abandoned in a browser history
  stops working.
* **Stateless.** No new table, no migration.

A bad token gets **404, not 401**. A 401 that distinguishes "wrong token" from
"no such feed" is an oracle for guessing tokens, and a calendar client cannot
do anything useful with a 401 anyway.

### The limitation, stated plainly

Because tokens are stateless, **a single leaked token cannot be revoked on its
own**. Two levers exist today:

1. Wait for it to expire (365 days by default; lower
   `CALENDAR_FEED_TOKEN_MAX_AGE_DAYS` to shorten that).
2. Change `CALENDAR_FEED_TOKEN_SALT` and restart, which invalidates **every**
   issued feed URL at once.

Calling `GET /api/calendar/feed-token` again issues a new token but does not
invalidate the old one.

Proper per-user revocation needs something to revoke against — a
`calendar_feed_tokens` table with a row per issued token, or a nonce column on
`users`. That is a small change and a good follow-up; it was left out here
because the repository already carries 13 alembic heads and adding a 14th
inside a feature PR is not a trade worth making.

## What ends up in the feed

**Hackathons** the user has registered for. Not every hackathon on the platform
— that is a newsletter, not a calendar. Rendered as a timed event from
`starts_at` to `ends_at`, with the theme, prize and registration deadline in
the description, and an alarm an hour before it starts.

**Milestones** on projects the user is an active member of, with a due date,
not completed and not archived. Rendered as an **all-day** event, because a due
date has no meaningful time of day and rendering it at midnight puts every
deadline in the small hours of the client's display. Alarm a day before.

Both are limited to a rolling window: 90 days back, 365 forward. A hackathon
that finished two years ago is not something anybody wants filling their
calendar.

## Getting the format right

iCalendar failures are not exceptions. They are Outlook quietly truncating a
project name at the first comma, or Google creating a duplicate event on every
poll. Those only surface in a real client, which is why `app/utils/ics.py` is
fussy about four things and the tests pin all of them:

**Line folding at 75 octets.** The limit is in octets, not characters, and a
fold that lands in the middle of a UTF-8 sequence corrupts the value for every
parser. The folder walks encoded lengths and only breaks where a character
ends. Continuation lines carry the leading space the spec requires — and that
space counts toward the next line's own limit.

**Escaping.** `\`, `;`, `,` and newlines are special inside a TEXT value.
Backslash is escaped first, or we would escape the backslashes we had just
introduced. URI values such as `URL:` are **not** TEXT and must not be escaped
— a comma in a query string is legal and escaping it breaks the link.

**CRLF.** The spec says CRLF. Some parsers accept a bare `\n` and some do not,
and the ones that do not fail obscurely.

**Stable UIDs.** `hackathon-{id}@devlink`, `milestone-{id}@devlink`. If a UID
changes between polls, the client does not update the event — it creates a
second one. This is the single most common way a hand-rolled feed goes wrong,
and it only shows up after the user has been subscribed for a week.

`SEQUENCE` is emitted when non-zero, because clients ignore an update whose
sequence has not moved.

## Configuration

| Setting | Default | Notes |
| --- | --- | --- |
| `CALENDAR_FEED_TOKEN_SALT` | `devlink-calendar-feed` | Change to invalidate every issued feed URL. |
| `CALENDAR_FEED_TOKEN_MAX_AGE_DAYS` | `365` | |
| `CALENDAR_FEED_REFRESH_MINUTES` | `360` | Advertised via `REFRESH-INTERVAL` and `X-PUBLISHED-TTL`. Without a hint, clients pick their own interval. |

## Subscribing

1. `GET /api/calendar/feed-token` → copy `feed_url`.
2. Google Calendar: *Other calendars → From URL*.
   Apple Calendar: *File → New Calendar Subscription*.
   Outlook: *Add calendar → Subscribe from web*.

Clients cache aggressively and mostly ignore `REFRESH-INTERVAL`; an hour or two
of lag on a newly added event is normal and not a bug in the feed.
