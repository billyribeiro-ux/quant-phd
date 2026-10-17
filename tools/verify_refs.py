#!/usr/bin/env python3
"""Re-verify every registry entry against the *current* record that established it.

Seeding establishes identity once; this gate keeps it true. Each entry is
re-fetched from its own verification source with the cache bypassed:

* ``crossref``: the DOI's Crossref record (title, first author, year, container,
  volume and issue must still match);
* ``openlibrary``: the ISBN's Open Library edition (title, first author, year);
* ``landing``: the publisher page's citation_* meta tags (as for Crossref);
* ``issuer``: the issuer's page, whose title must still cover the citation.

It also checks registry integrity: unique keys, DOIs, ISBNs and URLs; required
fields; a DOI or a URL on every entry; and that every ``used_by`` unit exists
in the curriculum (or is ``BLUEPRINT``).

Exit status is non-zero on any discrepancy, so CI can gate on it.

Usage::

    python3 tools/verify_refs.py             # full live re-verification
    python3 tools/verify_refs.py --offline   # integrity checks only (no network)
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import yaml

from refs import registry
from refs.crossref import Crossref, CrossrefError, Work
from refs.text import norm
from refs.web import (
    PRIMARY_TITLE_RECALL,
    Fetcher,
    OpenLibrary,
    WebError,
    citation_meta_to_work,
    parse_page,
    primary_title,
    title_recall,
)

REQUIRED = ("key", "type", "title", "authors", "status", "origin", "used_by")
VALID_STATUS = frozenset({"verified"})
VERIFIERS = frozenset({"crossref", "openlibrary", "landing", "issuer"})
# Living or undated documents (a codification, a data library) carry no year.
UNDATED_TYPES = frozenset({"primary"})


def curriculum_units() -> set[str]:
    units = {"BLUEPRINT"}
    for path in sorted((registry.ROOT / "curriculum").glob("[0-9][0-9]-*.yaml")):
        for part in yaml.safe_load(path.read_text(encoding="utf-8"))["parts"]:
            units.update(m["id"] for m in part["modules"])
    return units


def integrity(entries: list[dict[str, Any]]) -> list[str]:
    problems: list[str] = []
    units = curriculum_units()
    for name, counts in (
        ("key", Counter(e.get("key") for e in entries)),
        ("doi", Counter(e["doi"] for e in entries if e.get("doi"))),
        ("url", Counter(e["url"] for e in entries if e.get("url"))),
        ("isbn", Counter(i for e in entries if e.get("verified_by") == "openlibrary" for i in e.get("isbn") or [])),
    ):
        problems.extend(f"duplicate {name}: {value}" for value, n in counts.items() if n > 1)
    for e in entries:
        missing = [f for f in REQUIRED if e.get(f) in (None, "", [])]
        if e.get("year") is None and e.get("type") not in UNDATED_TYPES:
            missing.append("year")
        if missing:
            problems.append(f"{e.get('key')}: missing {missing}")
        verifier = e.get("verified_by", "crossref")
        if verifier not in VERIFIERS:
            problems.append(f"{e.get('key')}: unknown verified_by {verifier!r}")
        elif verifier == "crossref" and not e.get("doi"):
            problems.append(f"{e.get('key')}: verified by crossref but has no DOI")
        elif verifier != "crossref" and not e.get("url"):
            problems.append(f"{e.get('key')}: verified by {verifier} but has no URL")
        if e.get("status") not in VALID_STATUS:
            problems.append(f"{e.get('key')}: status {e.get('status')!r} is not citable")
        unknown = [u for u in e.get("used_by", []) if u not in units]
        if unknown:
            problems.append(f"{e.get('key')}: used_by unknown units {unknown}")
    return problems


ARTICLE_FIELDS = ("container", "volume", "issue")


def compare(entry: dict[str, Any], live: Work, *, fields: tuple[str, ...] = ARTICLE_FIELDS) -> list[str]:
    diffs: list[str] = []
    if norm(entry["title"]) != norm(live.title):
        diffs.append(f"title {entry['title']!r} != {live.title!r}")
    stored_first = entry["authors"][0]["family"] if entry["authors"] else ""
    live_first = live.authors[0].family if live.authors else ""
    if norm(stored_first) != norm(live_first):
        diffs.append(f"first author {stored_first!r} != {live_first!r}")
    if entry["year"] != live.year:
        diffs.append(f"year {entry['year']} != {live.year}")
    live_container = live.container[0] if live.container else None
    if "container" in fields and (entry.get("container") or None) != live_container:
        diffs.append(f"container {entry.get('container')!r} != {live_container!r}")
    for field in ("volume", "issue"):
        if field in fields and (entry.get(field) or None) != (getattr(live, field) or None):
            diffs.append(f"{field} {entry.get(field)!r} != {getattr(live, field)!r}")
    return diffs


def live_check(entry: dict[str, Any], crossref: Crossref, fetcher: Fetcher) -> list[str]:
    """Discrepancies between a stored entry and its verification source's current record."""
    verifier = entry.get("verified_by", "crossref")
    if verifier == "crossref":
        return compare(entry, crossref.work(entry["doi"], use_cache=False))
    if verifier == "openlibrary":
        isbn = next(iter(entry.get("isbn") or []), None)
        if isbn is None:
            return ["openlibrary entry has no ISBN"]
        return compare(entry, OpenLibrary(fetcher).edition(isbn, use_cache=False), fields=())
    final_url, html = fetcher.get(entry["url"], use_cache=False)
    if verifier == "landing":
        live = citation_meta_to_work(html, final_url)
        return ["landing page no longer carries citation meta tags"] if live is None else compare(entry, live)
    page = parse_page(html)
    titles = [*page.titles, *(c for n, c in page.meta if n in ("og:title", "dc.title", "citation_title"))]
    recall = max(title_recall(primary_title(s), titles) for s in entry["source_strings"])
    return [] if recall >= PRIMARY_TITLE_RECALL else [f"issuer page title now covers {recall:.0%} of the citation"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--offline", action="store_true", help="integrity checks only")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    entries = registry.load()
    problems = integrity(entries)

    if not args.offline:
        crossref, fetcher = Crossref(None), Fetcher(None)  # no cache: verify against the live record

        def check(entry: dict[str, Any]) -> list[str]:
            try:
                return [f"{entry['key']}: {d}" for d in live_check(entry, crossref, fetcher)]
            except (CrossrefError, WebError) as exc:
                return [f"{entry['key']}: {exc}"]

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for result in pool.map(check, entries):
                problems.extend(result)

    for problem in problems:
        print(f"FAIL {problem}")
    mode = "offline integrity" if args.offline else "live re-verification"
    print(f"{mode}: {len(entries)} entries, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
