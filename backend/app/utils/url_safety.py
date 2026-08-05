"""
Deciding whether it is safe for the server to fetch a URL a user gave us.

Any endpoint that takes a URL from a request and fetches it turns this service
into a proxy that sits *inside* the network perimeter. Left unguarded that is a
server-side request forgery hole: the caller gets to read the cloud metadata
endpoint, the internal admin panel on ``localhost:9000``, and every database
port on the private subnet, all with our source address and our credentials.

The guard here is deliberately conservative. It refuses anything it cannot
prove is a public destination, because the cost of a false negative is a
credential leak and the cost of a false positive is one link that does not get
a preview card.

Two things it does that the obvious implementation does not:

* It resolves the hostname and inspects the **resolved addresses**, not the
  hostname string. ``127.0.0.1.nip.io`` is a perfectly ordinary public name
  that resolves to loopback, and there is a whole family of such services.
* It exposes the resolved addresses to the caller, so a fetch can be re-checked
  at every redirect hop. A URL that passes on hop one and 302s to
  ``http://169.254.169.254/`` must fail on hop two.
"""

from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass
from typing import Iterable, Optional
from urllib.parse import urlparse, urlunparse

# Only these two ever make sense for a link somebody pasted into a message.
# `file:` reads our disk, `gopher:` and `dict:` are classic SSRF gadgets for
# speaking other protocols through an HTTP client.
ALLOWED_SCHEMES = frozenset({"http", "https"})

# Ports the fetch is allowed to reach. Restricting these is what stops a
# "public" hostname being pointed at, say, a Redis instance that happens to be
# internet-exposed.
ALLOWED_PORTS = frozenset({80, 443, 8080, 8443})

DEFAULT_PORTS = {"http": 80, "https": 443}

MAX_URL_LENGTH = 2048


class UnsafeURL(ValueError):
    """
    Raised when a URL must not be fetched.

    The message is written to be shown to the person who submitted the link.
    It says which rule was broken but never leaks what was found behind it --
    "that host resolves to a private address" is fine, echoing the address back
    would itself be an information leak about our network.
    """


@dataclass(frozen=True)
class SafeTarget:
    """A URL that passed every check, plus what it resolved to."""

    url: str
    scheme: str
    host: str
    port: int
    addresses: tuple[str, ...]


def _is_public_address(address: str) -> bool:
    """
    Whether an IP is one we are willing to connect out to.

    ``is_global`` covers most of this, but it is worth being explicit about the
    categories, because the interesting ones for SSRF are exactly the ones an
    attacker reaches for:

    * loopback -- ``127.0.0.0/8``, ``::1``: our own admin surfaces
    * link-local -- ``169.254.0.0/16``, ``fe80::/10``: cloud metadata
    * private -- RFC 1918 and ``fc00::/7``: the rest of the internal network
    * reserved / unspecified / multicast: nothing good lives here
    """
    try:
        ip = ipaddress.ip_address(address)
    except ValueError:
        # If it does not parse as an address we cannot reason about it, so we
        # refuse rather than guess.
        return False

    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped is not None:
        # ::ffff:127.0.0.1 is loopback wearing a hat.
        ip = ip.ipv4_mapped

    if (
        ip.is_loopback
        or ip.is_link_local
        or ip.is_private
        or ip.is_reserved
        or ip.is_multicast
        or ip.is_unspecified
    ):
        return False

    return ip.is_global


def _resolve(host: str) -> tuple[str, ...]:
    """
    Every address a hostname resolves to, both families.

    All of them matter. A name with one public A record and one private AAAA
    record is a working attack if we only check the first answer, since which
    one the HTTP client picks is not something this function controls.
    """
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise UnsafeURL(f"Could not resolve host: {host}") from exc

    addresses = {info[4][0] for info in infos}
    if not addresses:
        raise UnsafeURL(f"Could not resolve host: {host}")

    return tuple(sorted(addresses))


def validate_outbound_url(
    url: str,
    *,
    resolver=_resolve,
) -> SafeTarget:
    """
    Check a URL and return the target to connect to.

    ``resolver`` is injectable so the rules can be tested without a network and
    without depending on whatever the test machine's DNS happens to say today.

    Raises :class:`UnsafeURL` with a user-facing message on any failure.
    """
    if not url or not url.strip():
        raise UnsafeURL("No URL was provided.")

    url = url.strip()

    if len(url) > MAX_URL_LENGTH:
        raise UnsafeURL(f"URL is longer than {MAX_URL_LENGTH} characters.")

    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    if scheme not in ALLOWED_SCHEMES:
        raise UnsafeURL("Only http and https URLs can be previewed.")

    if not parsed.hostname:
        raise UnsafeURL("URL is missing a hostname.")

    host = parsed.hostname.lower()

    # Credentials in the URL are a phishing vector on their own (the browser
    # shows the userinfo, the server sees something else) and we have no reason
    # to forward them.
    if parsed.username or parsed.password:
        raise UnsafeURL("URLs containing credentials cannot be previewed.")

    try:
        port = parsed.port or DEFAULT_PORTS[scheme]
    except ValueError as exc:
        # urlparse raises when the port is not an integer.
        raise UnsafeURL("URL has an invalid port.") from exc

    if port not in ALLOWED_PORTS:
        raise UnsafeURL(f"Port {port} is not allowed.")

    addresses = resolver(host)

    for address in addresses:
        if not _is_public_address(address):
            raise UnsafeURL("That host resolves to a non-public address.")

    return SafeTarget(
        url=url,
        scheme=scheme,
        host=host,
        port=port,
        addresses=addresses,
    )


def is_safe_outbound_url(url: str, *, resolver=_resolve) -> bool:
    """Boolean form of :func:`validate_outbound_url`, for filtering lists."""
    try:
        validate_outbound_url(url, resolver=resolver)
    except UnsafeURL:
        return False
    return True


def normalise_url(url: str) -> str:
    """
    A stable spelling of a URL, for use as a cache key.

    Lowercases the scheme and host, drops a redundant explicit port and an
    empty query or fragment. Two links that differ only in these respects
    describe the same page and should share one cache entry.
    """
    parsed = urlparse(url.strip())
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()

    netloc = host
    if parsed.port and parsed.port != DEFAULT_PORTS.get(scheme):
        netloc = f"{host}:{parsed.port}"

    path = parsed.path or "/"

    # The fragment is a client-side concern; the server returns the same
    # document either way.
    return urlunparse((scheme, netloc, path, parsed.params, parsed.query, ""))


def filter_safe_urls(urls: Iterable[str], *, resolver=_resolve) -> list[str]:
    """Keep only the URLs that are safe to fetch, preserving order."""
    return [url for url in urls if is_safe_outbound_url(url, resolver=resolver)]


def describe_rejection(url: str, *, resolver=_resolve) -> Optional[str]:
    """The reason a URL was rejected, or ``None`` if it was not."""
    try:
        validate_outbound_url(url, resolver=resolver)
    except UnsafeURL as exc:
        return str(exc)
    return None
