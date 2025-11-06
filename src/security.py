"""Security helpers for the ZapPro API."""

from __future__ import annotations

import logging
import math
import re
import secrets
import time
from collections import deque
from dataclasses import dataclass
from ipaddress import ip_address, ip_network
from typing import Deque, Dict, List, Optional, Tuple

LOGGER = logging.getLogger("zappro.security")
REQUEST_ID_PATTERN = re.compile(r"^[A-Fa-f0-9-]{16,128}$")


def build_request_id(
    existing: str | None = None, *, allow_existing: bool = False
) -> str:
    """Return a secure request id, optionally preserving a trusted existing value."""
    if allow_existing and existing and REQUEST_ID_PATTERN.match(existing):
        return existing
    return secrets.token_hex(16)


@dataclass
class _RateBucket:
    window_start: float
    count: int
    last_seen: float


class FixedWindowRateLimiter:
    """Fixed-window rate limiter with TTL eviction."""

    def __init__(
        self,
        max_requests: int,
        window_seconds: int,
        *,
        ttl_seconds: Optional[int] = None,
        max_entries: int = 10_000,
    ) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.ttl_seconds = ttl_seconds or window_seconds * 2
        self.max_entries = max_entries
        self._buckets: Dict[str, _RateBucket] = {}
        self._order: Deque[Tuple[float, str]] = deque()

    def allow(self, identifier: str) -> Tuple[bool, float]:
        """Return whether the identifier can proceed and the retry-after seconds."""
        if self.max_requests <= 0:
            return True, 0.0

        now = time.monotonic()
        window_start = math.floor(now / self.window_seconds) * self.window_seconds
        bucket = self._buckets.get(identifier)

        if bucket and bucket.window_start == window_start:
            if bucket.count >= self.max_requests:
                retry_after = max(0.0, window_start + self.window_seconds - now)
                bucket.last_seen = now
                self._order.append((now, identifier))
                self._evict(now)
                return False, retry_after

            bucket.count += 1
            bucket.last_seen = now
        else:
            bucket = _RateBucket(window_start=window_start, count=1, last_seen=now)
            self._buckets[identifier] = bucket

        self._order.append((now, identifier))
        self._evict(now)
        return True, 0.0

    def reset(self, identifier: str) -> None:
        """Clear stored hits for the identifier."""
        self._buckets.pop(identifier, None)

    def _evict(self, now: float) -> None:
        """Remove stale or excess entries."""
        while self._order:
            ts, key = self._order[0]
            bucket = self._buckets.get(key)

            expired = bucket is None or (now - bucket.last_seen) > self.ttl_seconds
            oversized = len(self._buckets) > self.max_entries

            if not expired and not oversized:
                break

            self._order.popleft()
            if bucket is None:
                continue
            if expired or oversized:
                self._buckets.pop(key, None)


class RequestIdTracker:
    """Track request IDs to spot collisions."""

    def __init__(self, ttl_seconds: int = 300, max_entries: int = 20_000) -> None:
        self.ttl_seconds = max(ttl_seconds, 1)
        self.max_entries = max(max_entries, 1)
        self._seen: Dict[str, float] = {}
        self._order: Deque[Tuple[float, str]] = deque()

    def register(self, request_id: str) -> bool:
        """Register a request id and return True if it has been observed recently."""
        now = time.monotonic()
        duplicate = request_id in self._seen

        self._seen[request_id] = now
        self._order.append((now, request_id))
        self._evict(now)

        return duplicate

    def _evict(self, now: float) -> None:
        while self._order:
            ts, rid = self._order[0]
            if len(self._seen) <= self.max_entries and (now - ts) <= self.ttl_seconds:
                break
            self._order.popleft()
            latest = self._seen.get(rid)
            if latest is None:
                continue
            if (now - latest) > self.ttl_seconds or len(self._seen) > self.max_entries:
                self._seen.pop(rid, None)


def resolve_client_ip(
    client_host: Optional[str],
    headers: Dict[str, str],
    *,
    trusted_proxies: List[str],
    client_ip_header: str,
) -> str:
    """Return normalized client IP considering trusted proxies."""
    candidate = client_host or "anonymous"
    if not trusted_proxies:
        return candidate

    try:
        remote_ip = ip_address(candidate)
    except ValueError:
        return candidate

    for proxy_entry in trusted_proxies:
        try:
            network = ip_network(proxy_entry, strict=False)
        except ValueError:
            LOGGER.warning("Invalid trusted proxy entry configured: %s", proxy_entry)
            continue
        if remote_ip in network:
            header_value = headers.get(client_ip_header.lower())
            if not header_value:
                continue
            forwarded = _extract_first_forwarded_ip(header_value)
            if forwarded:
                return forwarded
    return candidate


def _extract_first_forwarded_ip(header_value: str) -> Optional[str]:
    for part in header_value.split(","):
        candidate = part.strip()
        if candidate:
            return candidate
    return None
