#!/usr/bin/env python3
"""Add one reference to the registry by DOI, verified against its citation string.

The architect uses this to admit a reference a builder requested
(BUILDER_RULES §2.4). The DOI's Crossref record must establish identity with
the given citation string under the same rules as seeding (``refs.match``),
so a wrong DOI or a misremembered citation is rejected rather than admitted.

Usage::

    python3 tools/add_reference.py --doi 10.1016/j.jfineco.2011.11.003 \\
        --source "Moskowitz, Ooi & Pedersen (2012), JFE 104(2)" --used-by F3
"""

from __future__ import annotations

import argparse
import sys

from refs import registry
from refs.crossref import Crossref, CrossrefError
from refs.match import resolve
from refs.parse import parse_source

CACHE_DIR = registry.ROOT / ".cache" / "crossref"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--doi", required=True)
    parser.add_argument("--source", required=True, help="citation string in curriculum house format")
    parser.add_argument("--used-by", required=True, nargs="+", help="unit IDs that cite it")
    args = parser.parse_args()

    cand = parse_source(args.source)
    if cand.kind not in ("article", "book"):
        print(f"REJECT: source parses as {cand.kind!r}; only articles and books resolve by DOI", file=sys.stderr)
        return 1
    try:
        work = Crossref(CACHE_DIR).work(args.doi)
    except CrossrefError as exc:
        print(f"REJECT: {exc}", file=sys.stderr)
        return 1

    res = resolve(cand, [work])
    if res.work is None:
        notes = "; ".join(n for a in res.candidates for n in a.notes)
        print(f"REJECT: DOI does not match the citation ({notes})", file=sys.stderr)
        print(
            f"  Crossref: {work.authors[0].family if work.authors else '?'} ({work.year}) "
            f"'{work.title}', {work.container[:1]} {work.volume}({work.issue})",
            file=sys.stderr,
        )
        return 1
    if res.corrections:
        print(
            f"REJECT: citation string differs from Crossref: {res.corrections}; fix the string first", file=sys.stderr
        )
        return 1

    entries = registry.load()
    existing = next((e for e in entries if e["doi"] == work.doi), None)
    if existing is not None:
        existing["used_by"] = sorted(set(existing["used_by"]) | set(args.used_by))
        existing["source_strings"] = sorted(set(existing["source_strings"]) | {args.source})
        registry.save(entries)
        print(f"UPDATED {existing['key']} used_by={existing['used_by']}")
        return 0

    entry = registry.Entry(
        key="",
        work=work,
        status="verified",
        origin="manual",
        source_strings=[args.source],
        used_by=list(args.used_by),
        corrections={},
        resolved_at=registry.now(),
        notes={k: {"curriculum": a, "crossref": b} for k, (a, b) in res.info.items()},
    )
    taken = {e["key"] for e in entries}
    base = registry.base_key(work)
    entry.key = next(k for k in (base, *(f"{base}{c}" for c in "bcdefghij")) if k not in taken)
    entries.append(entry.to_json())
    registry.save(entries)
    print(f"ADDED {entry.key} -> {work.doi}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
