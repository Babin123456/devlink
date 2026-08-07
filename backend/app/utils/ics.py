"""
Writing iCalendar (RFC 5545) documents.

Calendar clients are strict in ways that are easy to miss and hard to notice,
because the failure mode is not an error -- it is Outlook quietly truncating a
project name at the first comma, or Google creating a duplicate event on every
poll. So this module is fussy on purpose about four things:

* **Line folding at 75 octets.** Folded on octet boundaries, never in the middle
  of a UTF-8 sequence, because a split codepoint corrupts the field.
* **Escaping.** ``\\``, ``;``, ``,`` and newlines are special inside a text
  value. An unescaped comma silently ends the field in several clients.
* **CRLF line endings.** The spec says CRLF; some parsers accept ``\\n`` and
  some do not, and the ones that do not fail obscurely.
* **Stable UIDs.** If a UID changes between polls, the client does not update
  the event, it creates a second one. Deriving the UID from the entity type and
  id is what makes a subscribed feed converge instead of accumulating.

Deliberately hand-rolled rather than pulling in ``icalendar``: what we emit is
a small, fixed subset, and the dependency would be larger than the code.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Iterable, Optional

PRODUCT_ID = "-//DevLink//Calendar Feed//EN"

# RFC 5545 section 3.1: lines are folded so no line exceeds 75 octets, not
# counting the CRLF. Continuation lines begin with a single space.
MAX_LINE_OCTETS = 75


def escape_text(value: str) -> str:
    """
    Escape a string for use as an iCalendar TEXT value.

    Backslash first, or we would then escape the backslashes we just added.
    """
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
        .replace("\r", "\\n")
    )


def fold_line(line: str) -> str:
    """
    Fold a content line to 75 octets per physical line.

    The limit is in **octets**, not characters, and the fold must not land in
    the middle of a multi-byte sequence -- a split codepoint corrupts the value
    for every parser. So this walks the encoded bytes and only breaks where a
    character actually ends.
    """
    encoded = line.encode("utf-8")

    if len(encoded) <= MAX_LINE_OCTETS:
        return line

    pieces: list[str] = []
    current: list[str] = []
    current_octets = 0

    # A continuation line carries a leading space that counts toward its own
    # limit, so subsequent lines have one octet less room.
    limit = MAX_LINE_OCTETS

    for char in line:
        char_octets = len(char.encode("utf-8"))

        if current_octets + char_octets > limit:
            pieces.append("".join(current))
            current = [char]
            current_octets = char_octets
            limit = MAX_LINE_OCTETS - 1
        else:
            current.append(char)
            current_octets += char_octets

    pieces.append("".join(current))

    return "\r\n ".join(pieces)


def format_utc(moment: datetime) -> str:
    """
    Format an instant as a UTC date-time value: ``YYYYMMDDTHHMMSSZ``.

    A naive datetime is assumed to be UTC. That assumption is safe here because
    every column this module reads is ``DateTime(timezone=True)``; it exists
    only so a hand-built object in a test does not have to be explicit.
    """
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)

    return moment.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def format_date(day: date) -> str:
    """Format a calendar date for a ``VALUE=DATE`` property."""
    return day.strftime("%Y%m%d")


@dataclass
class Alarm:
    """
    A reminder, expressed as an offset before the event starts.

    ``minutes_before`` rather than a raw duration string because every reminder
    we generate is "some time before the start", and the string form is easy to
    get subtly wrong.
    """

    minutes_before: int
    description: str = "Reminder"

    def to_lines(self) -> list[str]:
        return [
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            f"DESCRIPTION:{escape_text(self.description)}",
            f"TRIGGER:-PT{self.minutes_before}M",
            "END:VALARM",
        ]


@dataclass
class Event:
    """
    One ``VEVENT``.

    ``uid`` must be stable for the life of the thing it describes. See the
    module docstring: an unstable UID turns every poll into a duplicate.

    Set ``all_day`` for something with a due date but no meaningful time -- a
    milestone deadline, say. All-day events use ``VALUE=DATE`` and an exclusive
    end date, which is why the end is bumped by a day below.
    """

    uid: str
    summary: str
    starts_at: datetime
    ends_at: Optional[datetime] = None
    description: Optional[str] = None
    location: Optional[str] = None
    url: Optional[str] = None
    all_day: bool = False
    status: Optional[str] = None
    # Incremented when the event is edited. Clients ignore an update whose
    # SEQUENCE has not moved.
    sequence: int = 0
    created_at: Optional[datetime] = None
    alarms: list[Alarm] = field(default_factory=list)

    def to_lines(self, *, stamp: datetime) -> list[str]:
        lines = [
            "BEGIN:VEVENT",
            f"UID:{self.uid}",
            # DTSTAMP is when this representation was generated, which is not
            # the same thing as when the event was created.
            f"DTSTAMP:{format_utc(stamp)}",
        ]

        if self.all_day:
            lines.append(f"DTSTART;VALUE=DATE:{format_date(self.starts_at.date())}")
            # DTEND is exclusive for all-day events: a one-day event on the 5th
            # ends on the 6th. Omitting it makes the event one day long, which
            # is what we want for a deadline, so only emit an explicit end when
            # the caller gave a different one.
            if self.ends_at is not None:
                lines.append(f"DTEND;VALUE=DATE:{format_date(self.ends_at.date())}")
        else:
            lines.append(f"DTSTART:{format_utc(self.starts_at)}")
            if self.ends_at is not None:
                lines.append(f"DTEND:{format_utc(self.ends_at)}")

        lines.append(f"SUMMARY:{escape_text(self.summary)}")

        if self.description:
            lines.append(f"DESCRIPTION:{escape_text(self.description)}")

        if self.location:
            lines.append(f"LOCATION:{escape_text(self.location)}")

        if self.url:
            # URI values are not TEXT and must not be escaped -- a comma in a
            # query string is legal and escaping it breaks the link.
            lines.append(f"URL:{self.url}")

        if self.status:
            lines.append(f"STATUS:{self.status}")

        if self.created_at is not None:
            lines.append(f"CREATED:{format_utc(self.created_at)}")

        if self.sequence:
            lines.append(f"SEQUENCE:{self.sequence}")

        for alarm in self.alarms:
            lines.extend(alarm.to_lines())

        lines.append("END:VEVENT")
        return lines


@dataclass
class Calendar:
    """A ``VCALENDAR`` wrapping a set of events."""

    name: str
    description: Optional[str] = None
    events: list[Event] = field(default_factory=list)
    # X-PUBLISHED-TTL is a hint to the client about how often to poll. Without
    # it, clients pick their own interval, which is often an hour for a feed
    # that changes daily.
    refresh_minutes: int = 60

    def add(self, event: Event) -> None:
        self.events.append(event)

    def render(self, *, stamp: Optional[datetime] = None) -> str:
        """
        Serialise to an iCalendar document.

        ``stamp`` is injectable so tests can assert on exact output.
        """
        stamp = stamp or datetime.now(timezone.utc)

        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            f"PRODID:{PRODUCT_ID}",
            "CALSCALE:GREGORIAN",
            # PUBLISH means "here is a calendar", as opposed to REQUEST, which
            # would be an invitation the recipient is expected to answer.
            "METHOD:PUBLISH",
            f"X-WR-CALNAME:{escape_text(self.name)}",
            f"REFRESH-INTERVAL;VALUE=DURATION:PT{self.refresh_minutes}M",
            f"X-PUBLISHED-TTL:PT{self.refresh_minutes}M",
        ]

        if self.description:
            lines.append(f"X-WR-CALDESC:{escape_text(self.description)}")

        for event in self.events:
            lines.extend(event.to_lines(stamp=stamp))

        lines.append("END:VCALENDAR")

        return "".join(fold_line(line) + "\r\n" for line in lines)


def render_calendar(
    name: str,
    events: Iterable[Event],
    *,
    description: Optional[str] = None,
    stamp: Optional[datetime] = None,
) -> str:
    """Convenience wrapper for the common "render this list" case."""
    calendar = Calendar(name=name, description=description, events=list(events))
    return calendar.render(stamp=stamp)
