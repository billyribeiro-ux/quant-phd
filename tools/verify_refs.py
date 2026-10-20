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

It also checks that each citation string's year is the year the site shows
(``registry.display_year``: the printed issue's year when Crossref has one), so
a miscited year cannot reach a page.

Exit status is non-zero on any discrepancy, so CI can gate on it.

Usage::

    python3 tools/verify_refs.py             # full live re-verification
    python3 tools/verify_refs.py --offline   # integrity checks only (no network)
    python3 tools/verify_refs.py --unit S7   # live re-verification of the entries S7 uses (integrity: whole registry)
    python3 tools/verify_refs.py --backfill-print-years   # record Crossref's print year where it is missing
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
        if verifier == "crossref" and "print_year" not in e:
            problems.append(f"{e.get('key')}: print_year not recorded (run --backfill-print-years)")
        # A year disagreement recorded at admission (notes['year']: curriculum against record) is acknowledged.
        shown, cited = registry.display_year(e), registry.cited_years(e)
        if shown is not None and cited and shown not in cited and "year" not in (e.get("notes") or {}):
            problems.append(f"{e.get('key')}: citation strings name {sorted(cited)} but the site shows {shown}")
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
    if entry.get("verified_by", "crossref") == "crossref" and entry.get("print_year") != live.print_year:
        diffs.append(f"print_year {entry.get('print_year')} != {live.print_year}")
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


def live_scope(entries: list[dict[str, Any]], unit: str | None) -> list[dict[str, Any]]:
    """The entries a live run re-fetches: all of them, or only those whose ``used_by`` names the unit."""
    return entries if unit is None else [e for e in entries if unit in e.get("used_by", [])]


def backfill_print_years(entries: list[dict[str, Any]], workers: int) -> int:
    """Store print_year on every Crossref entry from its live record; nothing else in an entry changes."""
    crossref = Crossref(None)
    todo = [e for e in entries if e.get("verified_by", "crossref") == "crossref" and e.get("doi")]

    def fetch(entry: dict[str, Any]) -> tuple[str, int | None, str | None]:
        try:
            return entry["key"], crossref.work(entry["doi"], use_cache=False).print_year, None
        except CrossrefError as exc:
            return entry["key"], None, str(exc)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(fetch, todo))
    failures = [f"{key}: {error}" for key, _, error in results if error]
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        print(f"backfill: {len(failures)} of {len(todo)} records could not be fetched; registry unchanged")
        return 1
    years = {key: year for key, year, _ in results}
    updated = []
    for entry in entries:
        if entry["key"] not in years:
            updated.append(entry)
            continue
        # Same field order as a new entry (registry.Entry.to_json): print_year follows years.
        fields = {k: v for k, v in entry.items() if k != "print_year"}
        ordered: dict[str, Any] = {}
        for name, value in fields.items():
            ordered[name] = value
            if name == "years":
                ordered["print_year"] = years[entry["key"]]
        updated.append(ordered)
    registry.save(updated)
    printed = sum(year is not None for year in years.values())
    print(f"backfill: print_year recorded on {len(years)} Crossref entries ({printed} with a print date)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--offline", action="store_true", help="integrity checks only")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--backfill-print-years",
        action="store_true",
        help="fetch each Crossref entry's record and store its published-print year (entries added before it existed)",
    )
    parser.add_argument(
        "--unit",
        help="re-verify live only the entries this unit uses; the integrity checks still cover the whole registry",
    )
    args = parser.parse_args()
    if args.unit is not None:
        if args.offline or args.backfill_print_years:
            parser.error("--unit selects the entries of a live run")
        if args.unit not in curriculum_units():
            parser.error(f"--unit {args.unit!r} is not a curriculum unit")

    entries = registry.load()
    if args.backfill_print_years:
        return backfill_print_years(entries, args.workers)
    problems = integrity(entries)

    if not args.offline:
        crossref, fetcher = Crossref(None), Fetcher(None)  # no cache: verify against the live record

        def check(entry: dict[str, Any]) -> list[str]:
            try:
                return [f"{entry['key']}: {d}" for d in live_check(entry, crossref, fetcher)]
            except (CrossrefError, WebError) as exc:
                return [f"{entry['key']}: {exc}"]

        live = live_scope(entries, args.unit)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for result in pool.map(check, live):
                problems.extend(result)

    for problem in problems:
        print(f"FAIL {problem}")
    if args.offline:
        print(f"offline integrity: {len(entries)} entries, {len(problems)} problems")
    elif args.unit is None:
        print(f"live re-verification: {len(entries)} entries, {len(problems)} problems")
    else:
        print(f"live re-verification of {args.unit}: {len(live)} of {len(entries)} entries, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
