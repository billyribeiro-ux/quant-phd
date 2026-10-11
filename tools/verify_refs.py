#!/usr/bin/env python3
"""Re-verify every registry entry against Crossref's *current* record.

Seeding establishes identity once; this gate keeps it true. For every entry it
re-fetches the DOI with the cache bypassed and checks that the stored title,
first author, year, container, volume and issue still match. It also checks
registry integrity: unique keys, unique DOIs, required fields, and that every
``used_by`` unit exists in the curriculum (or is ``BLUEPRINT``).

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

REQUIRED = ("key", "doi", "type", "title", "authors", "year", "status", "origin", "used_by")
VALID_STATUS = frozenset({"verified"})


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
        ("doi", Counter(e.get("doi") for e in entries)),
    ):
        problems.extend(f"duplicate {name}: {value}" for value, n in counts.items() if n > 1)
    for e in entries:
        missing = [f for f in REQUIRED if e.get(f) in (None, "", [])]
        if missing:
            problems.append(f"{e.get('key')}: missing {missing}")
        if e.get("status") not in VALID_STATUS:
            problems.append(f"{e.get('key')}: status {e.get('status')!r} is not citable")
        unknown = [u for u in e.get("used_by", []) if u not in units]
        if unknown:
            problems.append(f"{e.get('key')}: used_by unknown units {unknown}")
    return problems


def compare(entry: dict[str, Any], live: Work) -> list[str]:
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
    if (entry.get("container") or None) != live_container:
        diffs.append(f"container {entry.get('container')!r} != {live_container!r}")
    for field in ("volume", "issue"):
        if (entry.get(field) or None) != (getattr(live, field) or None):
            diffs.append(f"{field} {entry.get(field)!r} != {getattr(live, field)!r}")
    return diffs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--offline", action="store_true", help="integrity checks only")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    entries = registry.load()
    problems = integrity(entries)

    if not args.offline:
        client = Crossref(None)  # no cache: verify against the live record

        def check(entry: dict[str, Any]) -> list[str]:
            try:
                return [f"{entry['key']}: {d}" for d in compare(entry, client.work(entry["doi"], use_cache=False))]
            except CrossrefError as exc:
                return [f"{entry['key']}: {exc}"]

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for result in pool.map(check, entries):
                problems.extend(result)

    for problem in problems:
        print(f"FAIL {problem}")
    mode = "offline integrity" if args.offline else "live Crossref re-verification"
    print(f"{mode}: {len(entries)} entries, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
