"""Verification sources for works that have no Crossref DOI.

Three record sources, each producing the same ``Work`` the matcher already
judges, so a non-DOI work must pass the same identity rules as a DOI:

* **Open Library editions** (books, by ISBN). Title, authors, publication year
  and publisher come from the edition record, never from the citation string.
* **Publisher landing pages** (articles in venues without DOIs, such as JMLR
  or NeurIPS). Metadata comes from the page's Highwire ``citation_*`` meta
  tags, which Google Scholar requires publishers to expose.
* **Issuer pages** (primary documents: statutes, rules, court opinions,
  official data libraries). Only pages on a domain listed in
  ``references/authorities.yaml`` qualify, and the page's own title must
  contain the citation's title words.

Like the Crossref client, this module sends no personal data: requests carry
only a descriptive User-Agent.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from .crossref import Author, Work, clean
from .text import norm

USER_AGENT = "quant-finance-curriculum/0.1 (reference-registry tooling; Python urllib)"
OPEN_LIBRARY = "https://openlibrary.org"
_RETRY_STATUS = frozenset({429, 500, 502, 503, 504})
_YEAR = re.compile(r"\b(1[5-9]\d{2}|20\d{2})\b")
_TITLE_STOPWORDS = frozenset(
    {"a", "an", "the", "of", "on", "in", "for", "and", "to", "with", "from", "by", "at", "as", "v", "s"}
)
PRIMARY_TITLE_RECALL = 0.6


class WebError(RuntimeError):
    """Raised when a verification source cannot be reached or returns an unusable record."""


class Fetcher:
    """HTTP GET with retries and an optional on-disk cache keyed by URL."""

    def __init__(self, cache_dir: Path | None, *, timeout: float = 30.0, max_retries: int = 4) -> None:
        self._cache_dir = cache_dir
        self._timeout = timeout
        self._max_retries = max_retries
        cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
        self._ssl = ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()
        if cache_dir is not None:
            cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, url: str, *, use_cache: bool = True) -> tuple[str, str]:
        """Return ``(final_url, body)`` for a GET request, following redirects."""
        cache_file = None
        if self._cache_dir is not None:
            cache_file = self._cache_dir / f"{hashlib.sha256(url.encode()).hexdigest()}.json"
            if use_cache and cache_file.exists():
                cached: dict[str, str] = json.loads(cache_file.read_text(encoding="utf-8"))
                return cached["url"], cached["body"]
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        delay = 1.0
        for attempt in range(self._max_retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self._timeout, context=self._ssl) as response:
                    final_url = str(response.geturl())
                    charset = response.headers.get_content_charset() or "utf-8"
                    body = response.read().decode(charset, errors="replace")
                break
            except urllib.error.HTTPError as exc:
                if exc.code == 404:
                    raise WebError(f"not found: {url}") from exc
                if exc.code not in _RETRY_STATUS or attempt == self._max_retries:
                    raise WebError(f"HTTP {exc.code} for {url}") from exc
                retry_after = exc.headers.get("Retry-After")
                time.sleep(float(retry_after) if retry_after and retry_after.isdigit() else delay)
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt == self._max_retries:
                    raise WebError(f"network error for {url}: {exc}") from exc
                time.sleep(delay)
            delay *= 2
        else:  # pragma: no cover - loop always breaks or raises
            raise WebError(f"exhausted retries for {url}")
        if cache_file is not None:
            cache_file.write_text(json.dumps({"url": final_url, "body": body}), encoding="utf-8")
        return final_url, body

    def get_json(self, url: str, *, use_cache: bool = True) -> tuple[str, dict[str, Any]]:
        final_url, body = self.get(url, use_cache=use_cache)
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise WebError(f"not JSON: {url}") from exc
        if not isinstance(payload, dict):
            raise WebError(f"unexpected JSON shape: {url}")
        return final_url, payload


# ---------------------------------------------------------------- shared helpers


def family_of(name: str) -> str:
    """Family name from a display name: 'Hennessy, John L.' -> 'Hennessy'; 'Michael Spivak' -> 'Spivak'."""
    name = " ".join(name.split())
    if "," in name:
        return name.split(",", 1)[0].strip()
    return name.split()[-1] if name else ""


def given_of(name: str) -> str:
    name = " ".join(name.split())
    if "," in name:
        return name.split(",", 1)[1].strip()
    return " ".join(name.split()[:-1])


def first_year(text: str | None) -> int | None:
    match = _YEAR.search(text or "")
    return int(match.group()) if match else None


_ORDINAL_WORDS = {
    w: i + 1
    for i, w in enumerate(
        [
            "first",
            "second",
            "third",
            "fourth",
            "fifth",
            "sixth",
            "seventh",
            "eighth",
            "ninth",
            "tenth",
            "eleventh",
            "twelfth",
            "thirteenth",
            "fourteenth",
            "fifteenth",
            "sixteenth",
            "seventeenth",
            "eighteenth",
            "nineteenth",
            "twentieth",
        ]
    )
}
_EDITION_NUMBER = re.compile(r"\b(\d{1,2})\s*(?:st|nd|rd|th|d)?\b\.?\s*(?:ed\b|edition\b)", re.IGNORECASE)


def edition_number(text: str | None) -> int | None:
    """Edition number in a citation or edition statement: '4th ed.' / 'Fourth Edition' / '2d ed.' -> 4 / 4 / 2."""
    if not text:
        return None
    match = _EDITION_NUMBER.search(text)
    if match:
        return int(match.group(1))
    lowered = text.lower()
    for word, number in _ORDINAL_WORDS.items():
        if re.search(rf"\b{word}\b\s+(?:ed\b|edition\b)", lowered):
            return number
    return None


def normalize_isbn(isbn: str) -> str:
    digits = re.sub(r"[^0-9Xx]", "", isbn).upper()
    if len(digits) not in (10, 13):
        raise WebError(f"not an ISBN-10 or ISBN-13: {isbn!r}")
    return digits


# ---------------------------------------------------------------- Open Library


def edition_to_work(edition: dict[str, Any], author_names: list[str], url: str) -> Work:
    """Build a book ``Work`` from an Open Library edition record and its resolved author names."""
    title = clean(str(edition.get("title") or ""))
    subtitle = clean(str(edition.get("subtitle") or ""))
    if subtitle:
        title = f"{title}: {subtitle}"
    if not title:
        raise WebError(f"edition has no title: {url}")
    year = first_year(str(edition.get("publish_date") or ""))
    isbns = tuple(dict.fromkeys(str(i) for i in (*edition.get("isbn_13", ()), *edition.get("isbn_10", ()))))
    publishers = edition.get("publishers") or []
    return Work(
        doi="",
        type="book",
        title=title,
        authors=tuple(Author(family=family_of(n), given=given_of(n)) for n in author_names if n.strip()),
        container=(),
        volume=None,
        issue=None,
        pages=None,
        years=frozenset({year} if year else set()),
        year=year,
        isbn=isbns,
        publisher=str(publishers[0]) if publishers else None,
        url=url,
    )


class OpenLibrary:
    def __init__(self, fetcher: Fetcher) -> None:
        self._fetcher = fetcher

    def _author_names(self, refs: list[dict[str, Any]], *, use_cache: bool) -> list[str]:
        names: list[str] = []
        for ref in refs:
            key = ref.get("key") or (ref.get("author") or {}).get("key")
            if not key:
                continue
            _, record = self._fetcher.get_json(f"{OPEN_LIBRARY}{key}.json", use_cache=use_cache)
            name = str(record.get("personal_name") or record.get("name") or "")
            if name:
                names.append(name)
        return names

    def edition(self, isbn: str, *, use_cache: bool = True) -> Work:
        return self.edition_record(isbn, use_cache=use_cache)[0]

    def edition_record(self, isbn: str, *, use_cache: bool = True) -> tuple[Work, str | None]:
        """The edition as a ``Work``, plus its edition statement ('Fourth Edition'), if recorded."""
        url = f"{OPEN_LIBRARY}/isbn/{normalize_isbn(isbn)}.json"
        final_url, edition = self._fetcher.get_json(url, use_cache=use_cache)
        names = self._author_names(edition.get("authors") or [], use_cache=use_cache)
        if not names:
            for work_ref in edition.get("works") or []:
                _, work = self._fetcher.get_json(f"{OPEN_LIBRARY}{work_ref['key']}.json", use_cache=use_cache)
                names = self._author_names(work.get("authors") or [], use_cache=use_cache)
                if names:
                    break
        key = str(edition.get("key") or "")
        url = f"{OPEN_LIBRARY}{key}" if key.startswith("/books/") else final_url.removesuffix(".json")
        statement = edition.get("edition_name")
        return edition_to_work(edition, names, url), str(statement) if statement else None

    def search(self, title: str, author: str, *, limit: int = 3) -> list[dict[str, Any]]:
        """Every edition (ISBNs, date, publisher, edition name) of the best-matching works.

        For an architect choosing an ISBN to admit; it never admits anything itself.
        """
        params = urllib.parse.urlencode({"title": title, "author": author, "limit": str(limit), "fields": "key,title"})
        _, payload = self._fetcher.get_json(f"{OPEN_LIBRARY}/search.json?{params}")
        hits: list[dict[str, Any]] = []
        for doc in payload.get("docs") or []:
            key = str(doc.get("key") or "")
            if not key.startswith("/works/"):
                continue  # search can return non-work keys; only works have edition listings
            try:
                _, editions = self._fetcher.get_json(f"{OPEN_LIBRARY}{key}/editions.json?limit=100")
            except WebError:
                continue  # one broken work record must not hide the others
            for edition in editions.get("entries") or []:
                isbns = [*edition.get("isbn_13", []), *edition.get("isbn_10", [])]
                if isbns:
                    hits.append(
                        {
                            "work": doc.get("title"),
                            "title": edition.get("title"),
                            "edition": edition.get("edition_name"),
                            "date": edition.get("publish_date"),
                            "publisher": (edition.get("publishers") or [None])[0],
                            "isbn": isbns,
                        }
                    )
        return hits


# ---------------------------------------------------------------- landing pages


class _MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: list[tuple[str, str]] = []
        self.titles: list[str] = []
        self._capture: str | None = None
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta":
            name = values.get("name") or values.get("property") or ""
            if name:
                self.meta.append((name.lower(), values.get("content", "")))
        elif tag in ("title", "h1"):
            self._capture, self._buffer = tag, []

    def handle_endtag(self, tag: str) -> None:
        if tag == self._capture:
            text = " ".join("".join(self._buffer).split())
            if text:
                self.titles.append(text)
            self._capture = None

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buffer.append(data)


def parse_page(html: str) -> _MetaParser:
    parser = _MetaParser()
    parser.feed(html)
    parser.close()
    return parser


def landing_doi(html: str) -> str | None:
    """The DOI a landing page declares, if any (such works must be admitted by DOI instead)."""
    for name, content in parse_page(html).meta:
        if name in ("citation_doi", "dc.identifier") and content.strip().lower().startswith(("10.", "doi:10.")):
            return content.strip().lower().removeprefix("doi:")
    return None


def citation_meta_to_work(html: str, url: str) -> Work | None:
    """Build an article ``Work`` from Highwire ``citation_*`` meta tags; ``None`` if the page has none."""
    meta = parse_page(html).meta

    def first(*names: str) -> str | None:
        for wanted in names:
            for name, content in meta:
                if name == wanted and content.strip():
                    return clean(content)
        return None

    title = first("citation_title")
    authors = [clean(c) for n, c in meta if n == "citation_author" and c.strip()]
    if not title or not authors:
        return None
    journal = first("citation_journal_title")
    conference = first("citation_conference_title", "citation_inbook_title")
    year = first_year(first("citation_publication_date", "citation_date", "citation_year", "citation_online_date"))
    first_page, last_page = first("citation_firstpage"), first("citation_lastpage")
    pages = f"{first_page}-{last_page}" if first_page and last_page else first_page
    return Work(
        doi="",
        type="journal-article" if journal else "proceedings-article" if conference else "report",
        title=title,
        authors=tuple(Author(family=family_of(a), given=given_of(a)) for a in authors),
        container=tuple(c for c in (journal or conference,) if c),
        volume=first("citation_volume"),
        issue=first("citation_issue"),
        pages=pages,
        years=frozenset({year} if year else set()),
        year=year,
        isbn=(),
        publisher=first("citation_publisher", "dc.publisher"),
        url=url,
    )


# ---------------------------------------------------------------- primary documents


def significant_tokens(text: str) -> set[str]:
    return {t for t in norm(text).split() if t not in _TITLE_STOPWORDS and (len(t) > 1 or t.isdigit())}


def primary_title(raw: str) -> str:
    """The title words of a primary-source string: flags, '(primary)' and a trailing year removed."""
    text = re.sub(r"\s*\[(?:WP|V)\]", "", raw)
    text = re.sub(r"\s*\((?:primary|practitioner)\)", "", text, flags=re.IGNORECASE)
    return re.sub(r"\s*\(\d{4}\)\s*$", "", text).strip()


def title_recall(citation_title: str, page_titles: list[str]) -> float:
    """Share of the citation's significant title words that appear in the page's own titles."""
    wanted = significant_tokens(citation_title)
    if not wanted:
        return 0.0
    present = set().union(*(significant_tokens(t) for t in page_titles)) if page_titles else set()
    return len(wanted & present) / len(wanted)


@dataclass(frozen=True)
class Authority:
    domain: str
    issuer: str
    short: str


def authority_for(url: str, authorities: list[Authority]) -> Authority | None:
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    for authority in authorities:
        if host == authority.domain or host.endswith(f".{authority.domain}"):
            return authority
    return None


def primary_to_work(raw: str, html: str, url: str, authority: Authority) -> tuple[Work, float]:
    """Build a primary-document ``Work`` from the issuer page. Returns the work and its title recall."""
    page = parse_page(html)
    titles = [*page.titles, *(c for n, c in page.meta if n in ("og:title", "dc.title", "citation_title"))]
    recall = title_recall(primary_title(raw), titles)
    # A year is recorded only when the citation states one and the issuer's page confirms it.
    stated = re.search(r"\((\d{4})\)", raw)
    year = int(stated.group(1)) if stated and stated.group(1) in html else None
    page_title = next((t for t in titles if t), primary_title(raw))
    work = Work(
        doi="",
        type="primary",
        title=clean(page_title),
        authors=(Author(family=authority.issuer, given=""),),
        container=(),
        volume=None,
        issue=None,
        pages=None,
        years=frozenset({year} if year else set()),
        year=year,
        isbn=(),
        publisher=authority.issuer,
        url=url,
    )
    return work, recall
