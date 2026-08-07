"""
Tests for the link preview service and its SSRF guard.

The guard's tests inject a fake resolver rather than touching DNS. The point is
to pin the *rules*, and a test that depends on what the CI runner's resolver
says about ``localhost`` today is a test that will eventually lie.
"""

import pytest

from app.services.link_preview_service import LinkPreviewService, _clean
from app.utils.url_safety import (
    UnsafeURL,
    filter_safe_urls,
    is_safe_outbound_url,
    normalise_url,
    validate_outbound_url,
)


def resolver_for(mapping):
    """A fake DNS resolver backed by a dict of host -> addresses."""

    def _resolve(host):
        if host not in mapping:
            raise UnsafeURL(f"Could not resolve host: {host}")
        return tuple(mapping[host])

    return _resolve


PUBLIC = resolver_for({"example.com": ["93.184.216.34"]})


# ----------------------------------------------------------------------
# Scheme, port and shape
# ----------------------------------------------------------------------


def test_accepts_a_plain_https_url():
    target = validate_outbound_url("https://example.com/post", resolver=PUBLIC)

    assert target.host == "example.com"
    assert target.port == 443
    assert target.addresses == ("93.184.216.34",)


def test_accepts_http_as_well():
    target = validate_outbound_url("http://example.com/post", resolver=PUBLIC)
    assert target.port == 80


@pytest.mark.parametrize(
    "url",
    [
        "file:///etc/passwd",
        "ftp://example.com/x",
        "gopher://example.com/x",
        "data:text/html,<h1>hi</h1>",
        "javascript:alert(1)",
    ],
)
def test_rejects_non_http_schemes(url):
    with pytest.raises(UnsafeURL):
        validate_outbound_url(url, resolver=PUBLIC)


def test_rejects_a_url_with_no_host():
    with pytest.raises(UnsafeURL):
        validate_outbound_url("https:///just-a-path", resolver=PUBLIC)


def test_rejects_credentials_in_the_url():
    # The browser shows the userinfo and the server sees something else, which
    # is a phishing vector on its own. We also have no reason to forward them.
    with pytest.raises(UnsafeURL):
        validate_outbound_url("https://user:pw@example.com/", resolver=PUBLIC)


def test_rejects_a_disallowed_port():
    with pytest.raises(UnsafeURL):
        validate_outbound_url("http://example.com:6379/", resolver=PUBLIC)


def test_rejects_an_over_long_url():
    with pytest.raises(UnsafeURL):
        validate_outbound_url(
            "https://example.com/" + "a" * 3000,
            resolver=PUBLIC,
        )


def test_rejects_empty_input():
    with pytest.raises(UnsafeURL):
        validate_outbound_url("   ", resolver=PUBLIC)


# ----------------------------------------------------------------------
# The addresses, which is the part that actually matters
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "address",
    [
        "127.0.0.1",  # loopback
        "10.0.0.5",  # RFC 1918
        "172.16.4.4",  # RFC 1918
        "192.168.1.1",  # RFC 1918
        "169.254.169.254",  # cloud metadata
        "0.0.0.0",  # unspecified
        "224.0.0.1",  # multicast
        "::1",  # IPv6 loopback
        "fe80::1",  # IPv6 link-local
        "fc00::1",  # IPv6 unique-local
        "::ffff:127.0.0.1",  # IPv4-mapped loopback
    ],
)
def test_rejects_hosts_resolving_to_non_public_addresses(address):
    # This is the case a hostname-string check misses entirely: the name is
    # public and innocuous, and the answer is not.
    resolver = resolver_for({"internal.example.com": [address]})

    with pytest.raises(UnsafeURL):
        validate_outbound_url("https://internal.example.com/", resolver=resolver)


def test_rejects_when_any_resolved_address_is_private():
    # One public A record and one private AAAA record is a working attack if
    # only the first answer is checked -- we do not get to choose which one
    # the HTTP client connects to.
    resolver = resolver_for({"mixed.example.com": ["93.184.216.34", "10.0.0.1"]})

    with pytest.raises(UnsafeURL):
        validate_outbound_url("https://mixed.example.com/", resolver=resolver)


def test_rejects_a_host_that_does_not_resolve():
    with pytest.raises(UnsafeURL):
        validate_outbound_url("https://nope.invalid/", resolver=PUBLIC)


def test_is_safe_outbound_url_is_the_boolean_form():
    assert is_safe_outbound_url("https://example.com/", resolver=PUBLIC) is True
    assert is_safe_outbound_url("file:///etc/passwd", resolver=PUBLIC) is False


def test_filter_safe_urls_keeps_order_and_drops_the_rest():
    urls = [
        "https://example.com/a",
        "file:///etc/passwd",
        "https://example.com/b",
    ]

    assert filter_safe_urls(urls, resolver=PUBLIC) == [
        "https://example.com/a",
        "https://example.com/b",
    ]


# ----------------------------------------------------------------------
# Cache key normalisation
# ----------------------------------------------------------------------


def test_normalise_lowercases_scheme_and_host():
    assert normalise_url("HTTPS://Example.COM/Path") == "https://example.com/Path"


def test_normalise_drops_a_redundant_port():
    assert normalise_url("https://example.com:443/x") == "https://example.com/x"


def test_normalise_keeps_a_meaningful_port():
    assert normalise_url("https://example.com:8443/x") == "https://example.com:8443/x"


def test_normalise_drops_the_fragment_but_keeps_the_query():
    # The server returns the same document either way, so two links differing
    # only by fragment should share one cache entry.
    assert normalise_url("https://example.com/x?a=1#top") == "https://example.com/x?a=1"


def test_normalise_supplies_a_root_path():
    assert normalise_url("https://example.com") == "https://example.com/"


# ----------------------------------------------------------------------
# Parsing
# ----------------------------------------------------------------------


@pytest.fixture
def service():
    return LinkPreviewService()


def parse(service, body, url="https://example.com/post"):
    return service._parse(body, requested_url=url, final_url=url)


def test_reads_open_graph_tags(service):
    body = """
    <html><head>
      <meta property="og:title" content="A Title">
      <meta property="og:description" content="A description.">
      <meta property="og:site_name" content="Example">
      <meta property="og:image" content="https://cdn.example.com/a.png">
    </head></html>
    """

    preview = parse(service, body)

    assert preview.title == "A Title"
    assert preview.description == "A description."
    assert preview.site_name == "Example"
    assert preview.image_url == "https://cdn.example.com/a.png"


def test_falls_back_to_twitter_card_tags(service):
    body = """
    <html><head>
      <meta name="twitter:title" content="Tweet Title">
      <meta name="twitter:description" content="Tweet description.">
    </head></html>
    """

    preview = parse(service, body)

    assert preview.title == "Tweet Title"
    assert preview.description == "Tweet description."


def test_falls_back_to_the_document_title(service):
    body = "<html><head><title>Just A Title</title></head></html>"

    assert parse(service, body).title == "Just A Title"


def test_open_graph_wins_over_twitter_and_title(service):
    body = """
    <html><head>
      <title>Document</title>
      <meta name="twitter:title" content="Twitter">
      <meta property="og:title" content="Open Graph">
    </head></html>
    """

    assert parse(service, body).title == "Open Graph"


def test_attribute_order_does_not_matter(service):
    # `content` before `property` is extremely common in the wild, and a
    # single fixed-order regex silently misses all of it.
    body = '<meta content="Backwards" property="og:title">'

    assert parse(service, body).title == "Backwards"


def test_single_quoted_attributes_are_read(service):
    body = "<meta property='og:title' content='Single Quoted'>"

    assert parse(service, body).title == "Single Quoted"


def test_the_first_duplicate_tag_wins(service):
    body = """
    <meta property="og:title" content="First">
    <meta property="og:title" content="Second">
    """

    assert parse(service, body).title == "First"


def test_relative_images_resolve_against_the_final_url(service):
    body = '<meta property="og:image" content="/img/card.png">'

    preview = service._parse(
        body,
        requested_url="https://example.com/a",
        final_url="https://blog.example.com/posts/x",
    )

    assert preview.image_url == "https://blog.example.com/img/card.png"


def test_og_url_is_preferred_as_the_canonical_link(service):
    body = '<meta property="og:url" content="https://example.com/canonical">'

    preview = service._parse(
        body,
        requested_url="https://example.com/?utm_source=x",
        final_url="https://example.com/after-redirect",
    )

    assert preview.final_url == "https://example.com/canonical"


def test_a_page_with_no_metadata_yields_an_empty_preview(service):
    preview = parse(service, "<html><body>nothing here</body></html>")

    assert preview.title is None
    assert preview.description is None
    assert preview.image_url is None
    # The URL fields are always populated, so the caller can still render a
    # bare link card.
    assert preview.url == "https://example.com/post"


# ----------------------------------------------------------------------
# Text cleaning
# ----------------------------------------------------------------------


def test_clean_decodes_entities():
    assert _clean("Tips &amp; tricks", 100) == "Tips & tricks"


def test_clean_collapses_whitespace():
    # These tags are routinely pretty-printed across several lines.
    assert _clean("A\n   long\t title", 100) == "A long title"


def test_clean_returns_none_for_blank_text():
    assert _clean("   \n  ", 100) is None
    assert _clean(None, 100) is None


def test_clean_truncates_on_a_word_boundary():
    result = _clean("the quick brown fox jumps over the lazy dog", 20)

    assert result.endswith("…")
    assert len(result) <= 21
    # Backing up to a space means we do not cut mid-word.
    assert not result[:-1].endswith(" ")


def test_clean_does_not_back_up_far_for_a_long_token():
    # A single unbroken token would otherwise shrink the text dramatically, so
    # a hard cut is the better answer here.
    result = _clean("short " + "x" * 100, 20)

    assert len(result) == 21
