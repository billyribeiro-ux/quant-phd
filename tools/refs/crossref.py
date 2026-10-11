"""Minimal, dependency-free Crossref REST client with on-disk caching.

Caching makes seeding reproducible and cheap to re-run. ``verify_refs.py``
bypasses the cache so verification always reflects Crossref's current record.
No personal data (such as an email address) is sent; requests carry only a
descriptive User-Agent.
"""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

API = "https://api.crossref.org"
USER_AGENT = "quant-finance-curriculum/0.1 (reference-registry tooling; Python urllib)"
SELECT = ",".join(
    (
        "DOI",
        "type",
        "title",
        "subtitle",
        "author",
        "editor",
        "container-title",
        "volume",
        "issue",
        "page",
        "issued",
        "published-print",
        "published-online",
        "ISBN",
        "publisher",
    )
)
_RETRY_STATUS = frozenset({429, 500, 502, 503, 504})
_FOOTNOTE = re.compile(r"(\*{1,2}|☆|†|‡|\d?(?:We are grateful|We thank|Thanks to|The authors thank)\b).*$")
_TAGS = re.compile(r"<[^>]+>")


def clean(text: str) -> str:
    """Decode HTML entities, drop JATS tags and trailing footnote text ('Title**Thanks to ...')."""
    text = _TAGS.sub("", html.unescape(text))
    return " ".join(_FOOTNOTE.sub("", text).split())


class CrossrefError(RuntimeError):
    """Raised when Crossref cannot be reached or returns an unusable response."""


@dataclass(frozen=True)
class Author:
    family: str
    given: str


@dataclass(frozen=True)
class Work:
    """The subset of a Crossref work record the registry uses."""

    doi: str
    type: str
    title: str
    authors: tuple[Author, ...]
    container: tuple[str, ...]
    volume: str | None
    issue: str | None
    pages: str | None
    years: frozenset[int]
    year: int | None
    isbn: tuple[str, ...]
    publisher: str | None

    @classmethod
    def from_message(cls, item: dict[str, Any]) -> Work:
        title_parts = [*(item.get("title") or [])[:1], *(item.get("subtitle") or [])[:1]]
        title = ": ".join(clean(t) for t in title_parts if t and clean(t))
        people = item.get("author") or item.get("editor") or []
        authors = tuple(
            Author(family=str(p.get("family") or p.get("name") or ""), given=str(p.get("given") or "")) for p in people
        )
        years: set[int] = set()
        for key in ("issued", "published-print", "published-online"):
            parts = (item.get(key) or {}).get("date-parts") or []
            if parts and parts[0] and parts[0][0]:
                years.add(int(parts[0][0]))
        issued = (item.get("issued") or {}).get("date-parts") or [[None]]
        year = int(issued[0][0]) if issued and issued[0] and issued[0][0] else (min(years) if years else None)
        return cls(
            doi=str(item["DOI"]).lower(),
            type=str(item.get("type") or ""),
            title=title,
            authors=authors,
            container=tuple(clean(c) for c in item.get("container-title") or ()),
            volume=item.get("volume"),
            issue=item.get("issue"),
            pages=item.get("page"),
            years=frozenset(years),
            year=year,
            isbn=tuple(item.get("ISBN") or ()),
            publisher=item.get("publisher"),
        )


class Crossref:
    """Crossref client. Thread-safe for concurrent ``get`` calls (no shared mutable state)."""

    def __init__(self, cache_dir: Path | None, *, timeout: float = 30.0, max_retries: int = 5) -> None:
        self._cache_dir = cache_dir
        self._timeout = timeout
        self._max_retries = max_retries
        cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
        self._ssl = ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()
        if cache_dir is not None:
            cache_dir.mkdir(parents=True, exist_ok=True)

    def _get(self, path: str, params: dict[str, str] | None = None, *, use_cache: bool = True) -> dict[str, Any]:
        query = f"?{urllib.parse.urlencode(params)}" if params else ""
        url = f"{API}{path}{query}"
        cache_file = None
        if self._cache_dir is not None:
            cache_file = self._cache_dir / f"{hashlib.sha256(url.encode()).hexdigest()}.json"
            if use_cache and cache_file.exists():
                cached: dict[str, Any] = json.loads(cache_file.read_text(encoding="utf-8"))
                return cached

        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        delay = 1.0
        for attempt in range(self._max_retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self._timeout, context=self._ssl) as response:
                    payload: dict[str, Any] = json.load(response)
                break
            except urllib.error.HTTPError as exc:
                if exc.code == 404:
                    raise CrossrefError(f"not found: {url}") from exc
                if exc.code not in _RETRY_STATUS or attempt == self._max_retries:
                    raise CrossrefError(f"HTTP {exc.code} for {url}") from exc
                retry_after = exc.headers.get("Retry-After")
                time.sleep(float(retry_after) if retry_after and retry_after.isdigit() else delay)
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt == self._max_retries:
                    raise CrossrefError(f"network error for {url}: {exc}") from exc
                time.sleep(delay)
            delay *= 2
        else:  # pragma: no cover - loop always breaks or raises
            raise CrossrefError(f"exhausted retries for {url}")

        if payload.get("status") != "ok":
            raise CrossrefError(f"unexpected status {payload.get('status')!r} for {url}")
        if cache_file is not None:
            cache_file.write_text(json.dumps(payload), encoding="utf-8")
        return payload

    def work(self, doi: str, *, use_cache: bool = True) -> Work:
        payload = self._get(f"/works/{urllib.parse.quote(doi, safe='/')}", use_cache=use_cache)
        return Work.from_message(payload["message"])

    def journal_issns(self, title: str) -> list[str]:
        """ISSNs of journals whose title matches ``title`` exactly after normalization."""
        from .journals import venue_matches  # local import avoids a module cycle

        payload = self._get("/journals", {"query": title, "rows": "10"})
        issns: list[str] = []
        for item in payload["message"].get("items", []):
            if venue_matches(title, clean(str(item.get("title") or ""))):
                issns.extend(str(i) for i in item.get("ISSN") or [])
        return list(dict.fromkeys(issns))

    def journal_works(self, issn: str, *, author: str, year_range: tuple[int, int], rows: int = 40) -> list[Work]:
        """Works in one journal by an author within a year range."""
        params = {
            "query.author": author,
            "rows": str(rows),
            "select": SELECT,
            "filter": f"from-pub-date:{year_range[0]}-01-01,until-pub-date:{year_range[1]}-12-31",
        }
        try:
            payload = self._get(f"/journals/{issn}/works", params)
        except CrossrefError:
            return []
        return [Work.from_message(item) for item in payload["message"].get("items", [])]

    def search(
        self,
        bibliographic: str,
        *,
        author: str | None = None,
        year_range: tuple[int, int] | None = None,
        rows: int = 8,
    ) -> list[Work]:
        params = {"query.bibliographic": bibliographic, "rows": str(rows), "select": SELECT}
        if author:
            params["query.author"] = author
        if year_range:
            params["filter"] = f"from-pub-date:{year_range[0]}-01-01,until-pub-date:{year_range[1]}-12-31"
        payload = self._get("/works", params)
        return [Work.from_message(item) for item in payload["message"].get("items", [])]
