"""
Tests for the iCalendar writer and the feed token.

The writer tests are the important ones. iCalendar failures are not exceptions,
they are Outlook silently truncating a project name at the first comma, or
Google creating a duplicate event on every poll. Those only show up in a real
client, so the format details have to be pinned here instead.
"""

import uuid
from datetime import datetime, timedelta, timezone

import pytest

from app.services.calendar_feed_service import (
    InvalidFeedToken,
    generate_feed_token,
    parse_feed_token,
)
from app.utils.ics import (
    Alarm,
    Calendar,
    Event,
    escape_text,
    fold_line,
    format_date,
    format_utc,
    render_calendar,
)

STAMP = datetime(2026, 3, 1, 12, 0, 0, tzinfo=timezone.utc)


# ----------------------------------------------------------------------
# Escaping
# ----------------------------------------------------------------------


def test_escapes_a_comma():
    # An unescaped comma silently ends the field in several clients, so a
    # project called "Fast, cheap, good" loses two thirds of its name.
    assert escape_text("Fast, cheap, good") == "Fast\\, cheap\\, good"


def test_escapes_a_semicolon():
    assert escape_text("a;b") == "a\\;b"


def test_escapes_a_backslash_before_anything_else():
    # Order matters: escaping commas first and backslashes second would then
    # escape the backslashes we had just introduced.
    assert escape_text("a\\,b") == "a\\\\\\,b"


def test_turns_newlines_into_the_literal_escape():
    assert escape_text("line one\nline two") == "line one\\nline two"


def test_normalises_crlf_and_lone_cr():
    assert escape_text("a\r\nb") == "a\\nb"
    assert escape_text("a\rb") == "a\\nb"


# ----------------------------------------------------------------------
# Folding
# ----------------------------------------------------------------------


def test_short_lines_are_untouched():
    assert fold_line("SUMMARY:Hello") == "SUMMARY:Hello"


def test_long_lines_fold_at_seventy_five_octets():
    line = "DESCRIPTION:" + "a" * 200
    folded = fold_line(line)

    physical = folded.split("\r\n")
    assert len(physical) > 1
    assert len(physical[0].encode("utf-8")) <= 75

    # Every continuation begins with the single space the spec requires.
    for continuation in physical[1:]:
        assert continuation.startswith(" ")
        assert len(continuation.encode("utf-8")) <= 75


def test_folding_never_splits_a_multi_byte_character():
    # The limit is in octets, and a fold landing mid-sequence corrupts the
    # value for every parser. Emoji are four octets each, so a naive character
    # count gets this wrong immediately.
    line = "SUMMARY:" + "🎉" * 60
    folded = fold_line(line)

    for physical in folded.split("\r\n"):
        assert len(physical.encode("utf-8")) <= 75
        # Round-tripping proves nothing was cut mid-codepoint.
        physical.encode("utf-8").decode("utf-8")

    assert folded.replace("\r\n ", "") == line


def test_unfolding_recovers_the_original_line():
    line = "DESCRIPTION:" + ("word " * 60).strip()

    assert fold_line(line).replace("\r\n ", "") == line


# ----------------------------------------------------------------------
# Timestamps
# ----------------------------------------------------------------------


def test_formats_utc_timestamps():
    assert format_utc(datetime(2026, 3, 1, 9, 30, 0, tzinfo=timezone.utc)) == (
        "20260301T093000Z"
    )


def test_converts_a_non_utc_timestamp():
    tz = timezone(timedelta(hours=5, minutes=30))
    moment = datetime(2026, 3, 1, 15, 0, 0, tzinfo=tz)

    assert format_utc(moment) == "20260301T093000Z"


def test_treats_a_naive_timestamp_as_utc():
    assert format_utc(datetime(2026, 3, 1, 9, 30, 0)) == "20260301T093000Z"


def test_formats_dates():
    assert format_date(datetime(2026, 3, 1).date()) == "20260301"


# ----------------------------------------------------------------------
# Events
# ----------------------------------------------------------------------


def simple_event(**overrides):
    defaults = dict(
        uid="hackathon-123@devlink",
        summary="Spring Hack",
        starts_at=datetime(2026, 4, 1, 9, 0, tzinfo=timezone.utc),
        ends_at=datetime(2026, 4, 3, 18, 0, tzinfo=timezone.utc),
    )
    defaults.update(overrides)
    return Event(**defaults)


def render_one(event):
    return render_calendar("Test", [event], stamp=STAMP)


def test_a_timed_event_has_start_and_end():
    output = render_one(simple_event())

    assert "DTSTART:20260401T090000Z\r\n" in output
    assert "DTEND:20260403T180000Z\r\n" in output


def test_the_uid_is_emitted_verbatim():
    # Stability is the whole point: a changing UID makes a subscribed client
    # create a second event instead of updating the first.
    assert "UID:hackathon-123@devlink\r\n" in render_one(simple_event())


def test_an_all_day_event_uses_a_date_value():
    output = render_one(
        simple_event(
            all_day=True,
            starts_at=datetime(2026, 4, 1, 0, 0, tzinfo=timezone.utc),
            ends_at=None,
        )
    )

    assert "DTSTART;VALUE=DATE:20260401\r\n" in output
    # No DTEND: a single-day all-day event is the default, which is exactly
    # what a deadline should be.
    assert "DTEND" not in output


def test_a_url_is_not_escaped():
    # URI values are not TEXT. A comma in a query string is legal, and
    # escaping it produces a broken link.
    output = render_one(simple_event(url="https://example.com/e?a=1,2"))

    assert "URL:https://example.com/e?a=1,2\r\n" in output


def test_a_summary_is_escaped():
    output = render_one(simple_event(summary="Ship, then iterate"))

    assert "SUMMARY:Ship\\, then iterate\r\n" in output


def test_sequence_is_omitted_when_zero():
    assert "SEQUENCE" not in render_one(simple_event())


def test_sequence_is_emitted_when_set():
    # Clients ignore an update whose SEQUENCE has not moved.
    assert "SEQUENCE:3\r\n" in render_one(simple_event(sequence=3))


def test_alarms_are_rendered():
    output = render_one(
        simple_event(alarms=[Alarm(minutes_before=60, description="Starting soon")])
    )

    assert "BEGIN:VALARM\r\n" in output
    assert "TRIGGER:-PT60M\r\n" in output
    assert "DESCRIPTION:Starting soon\r\n" in output
    assert "END:VALARM\r\n" in output


def test_status_is_emitted_when_set():
    assert "STATUS:CANCELLED\r\n" in render_one(simple_event(status="CANCELLED"))


# ----------------------------------------------------------------------
# Calendar envelope
# ----------------------------------------------------------------------


def test_the_document_is_well_formed():
    output = render_one(simple_event())

    assert output.startswith("BEGIN:VCALENDAR\r\n")
    assert output.endswith("END:VCALENDAR\r\n")
    assert "VERSION:2.0\r\n" in output
    assert "PRODID:-//DevLink//Calendar Feed//EN\r\n" in output


def test_every_line_ends_with_crlf():
    # Some parsers accept a bare \n and some do not, and the ones that do not
    # fail in ways that are hard to trace back here.
    output = render_one(simple_event())

    for line in output.split("\r\n")[:-1]:
        assert "\n" not in line


def test_the_stamp_is_the_generation_time_not_the_event_time():
    assert "DTSTAMP:20260301T120000Z\r\n" in render_one(simple_event())


def test_an_empty_calendar_still_renders():
    # A user with nothing scheduled must get a valid empty calendar, not an
    # error -- their client polls this URL regardless.
    output = Calendar(name="Empty").render(stamp=STAMP)

    assert output.startswith("BEGIN:VCALENDAR\r\n")
    assert output.endswith("END:VCALENDAR\r\n")
    assert "BEGIN:VEVENT" not in output


def test_multiple_events_are_all_present():
    output = render_calendar(
        "Test",
        [simple_event(uid="a@devlink"), simple_event(uid="b@devlink")],
        stamp=STAMP,
    )

    assert output.count("BEGIN:VEVENT\r\n") == 2
    assert "UID:a@devlink\r\n" in output
    assert "UID:b@devlink\r\n" in output


def test_the_refresh_interval_is_advertised():
    output = Calendar(name="Test", refresh_minutes=180).render(stamp=STAMP)

    assert "REFRESH-INTERVAL;VALUE=DURATION:PT180M\r\n" in output
    assert "X-PUBLISHED-TTL:PT180M\r\n" in output


def test_a_calendar_name_containing_a_comma_is_escaped():
    output = Calendar(name="Work, and play").render(stamp=STAMP)

    assert "X-WR-CALNAME:Work\\, and play\r\n" in output


# ----------------------------------------------------------------------
# Feed tokens
# ----------------------------------------------------------------------


def test_a_token_round_trips():
    user_id = uuid.uuid4()

    assert parse_feed_token(generate_feed_token(user_id)) == user_id


def test_tokens_are_url_safe():
    token = generate_feed_token(uuid.uuid4())

    # It goes in a query string, so anything needing percent-encoding would
    # break a naive client.
    assert "+" not in token
    assert "/" not in token
    assert "=" not in token


def test_a_tampered_user_id_is_rejected():
    token = generate_feed_token(uuid.uuid4())
    version, encoded_id, issued, signature = token.split(".")

    forged = f"{version}.{generate_feed_token(uuid.uuid4()).split('.')[1]}.{issued}.{signature}"

    with pytest.raises(InvalidFeedToken):
        parse_feed_token(forged)


def test_a_tampered_signature_is_rejected():
    token = generate_feed_token(uuid.uuid4())
    version, encoded_id, issued, _ = token.split(".")

    with pytest.raises(InvalidFeedToken):
        parse_feed_token(f"{version}.{encoded_id}.{issued}.AAAAAAAA")


def test_an_expired_token_is_rejected():
    old = datetime.now(timezone.utc) - timedelta(days=400)

    with pytest.raises(InvalidFeedToken):
        parse_feed_token(generate_feed_token(uuid.uuid4(), issued_at=old))


def test_a_token_just_inside_the_window_is_accepted():
    user_id = uuid.uuid4()
    recent = datetime.now(timezone.utc) - timedelta(days=364)

    assert parse_feed_token(generate_feed_token(user_id, issued_at=recent)) == user_id


@pytest.mark.parametrize(
    "token",
    ["", "nonsense", "v1.a.b", "v1.a.b.c.d", "v2.a.b.c"],
)
def test_malformed_tokens_are_rejected(token):
    with pytest.raises(InvalidFeedToken):
        parse_feed_token(token)


def test_two_tokens_for_the_same_user_differ_by_issue_time():
    user_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    first = generate_feed_token(user_id, issued_at=now)
    second = generate_feed_token(user_id, issued_at=now + timedelta(seconds=1))

    assert first != second
    # Both are still valid: issuing a new one does not invalidate the old,
    # which is the documented limitation of stateless tokens.
    assert parse_feed_token(first) == user_id
    assert parse_feed_token(second) == user_id
