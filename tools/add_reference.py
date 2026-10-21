#!/usr/bin/env python3
"""Add one reference to the registry, verified against its citation string.

The architect uses this to admit a reference a builder requested
(BUILDER_RULES §2.4) or one the seeding pass could not resolve. Every mode
fetches an authoritative record and judges it against the citation string with
the same identity rules as seeding (``refs.match``), so a wrong identifier or a
misremembered citation is rejected rather than admitted. No bibliographic field
is ever taken from the command line.

Modes (exactly one):

``--doi``   Crossref record. The default for anything that has a DOI.
``--isbn``  Open Library edition record, for books. Use ``--list-editions`` first
            to see candidate ISBNs with their dates and publishers.
``--url``   For an article in a venue without DOIs: the publisher's landing page,
            which must sit on a ``publishers`` domain in references/authorities.yaml
            and carry citation_* meta tags. For a primary document: the issuer's
            page, which must sit on an ``issuers`` domain and whose own title must
            contain the citation's title words.

Usage::

    python3 tools/add_reference.py --doi 10.1016/j.jfineco.2011.11.003 \\
        --source "Moskowitz, Ooi & Pedersen (2012), JFE 104(2)" --used-by F3
    python3 tools/add_reference.py --list-editions --source "Spivak, Calculus, 4th ed. (2008)"
    python3 tools/add_reference.py --isbn 9780914098911 --source "Spivak, Calculus, 4th ed. (2008)" --used-by M2
    python3 tools/add_reference.py --url https://www.jmlr.org/papers/v12/pedregosa11a.html \\
        --source "Pedregosa et al. (2011), Journal of Machine Learning Research 12" --used-by QR3
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import yaml

from refs import registry
from refs.crossref import Crossref, CrossrefError, Work
from refs.match import resolve
from refs.parse import Candidate, parse_source
from refs.web import (
    PRIMARY_TITLE_RECALL,
    Authority,
    Fetcher,
    OpenLibrary,
    WebError,
    authority_for,
    citation_meta_to_work,
    edition_number,
    landing_doi,
    primary_to_work,
)

CACHE_DIR = registry.ROOT / ".cache"
AUTHORITIES = registry.ROOT / "references" / "authorities.yaml"


def load_authorities(section: str) -> list[Authority]:
    data = yaml.safe_load(AUTHORITIES.read_text(encoding="utf-8"))
    return [Authority(str(a["domain"]), str(a["issuer"]), str(a["short"])) for a in data.get(section) or []]


def reject(message: str) -> int:
    print(f"REJECT: {message}", file=sys.stderr)
    return 1


def describe(work: Work) -> str:
    first = work.authors[0].family if work.authors else "?"
    return f"{first} ({work.year}) '{work.title}', {', '.join(work.container[:1])} {work.volume}({work.issue})"


def judged(cand: Candidate, work: Work, label: str = "record") -> tuple[Work | None, dict[str, dict[str, str]], str]:
    """Run the identity rules. Returns (work or None, notes keyed curriculum/<label>, rejection reason)."""
    res = resolve(cand, [work])
    if res.work is None:
        notes = "; ".join(n for a in res.candidates for n in a.notes)
        return None, {}, f"record does not match the citation ({notes})\n  record: {describe(work)}"
    if res.corrections:
        return None, {}, f"citation string differs from the record: {res.corrections}; fix the string first"
    return res.work, {k: {"curriculum": a, label: b} for k, (a, b) in res.info.items()}, ""


def registered(entries: list[dict[str, Any]], work: Work) -> dict[str, Any] | None:
    """The entry that already holds ``work``: the same DOI, else a shared ISBN or the same URL."""

    def same(e: dict[str, Any]) -> bool:
        if work.doi:
            return bool(e.get("doi") == work.doi)
        if work.isbn and set(e.get("isbn") or []) & set(work.isbn):
            return True
        return bool(work.url and e.get("url") == work.url)

    return next((e for e in entries if same(e)), None)


def admit(
    work: Work, *, source: str, used_by: list[str], verified_by: str, notes: dict[str, dict[str, str]], short: str = ""
) -> int:
    entries = registry.load()
    existing = registered(entries, work)
    if existing is not None:
        existing["used_by"] = sorted(set(existing["used_by"]) | set(used_by))
        existing["source_strings"] = sorted(set(existing["source_strings"]) | {source})
        registry.save(entries)
        print(f"UPDATED {existing['key']} used_by={existing['used_by']}")
        return 0

    entry = registry.Entry(
        key="",
        work=work,
        status="verified",
        origin="manual",
        source_strings=[source],
        used_by=list(used_by),
        corrections={},
        resolved_at=registry.now(),
        notes=notes,
        verified_by=verified_by,
    )
    taken = {e["key"] for e in entries}
    base = registry.base_key(work, short or None)
    entry.key = next(k for k in (base, *(f"{base}{c}" for c in "bcdefghij")) if k not in taken)
    entries.append(entry.to_json())
    registry.save(entries)
    print(f"ADDED {entry.key} -> {work.doi or work.url}")
    return 0


def by_doi(cand: Candidate, doi: str) -> tuple[Work | None, dict[str, dict[str, str]], str]:
    if cand.kind not in ("article", "book"):
        return None, {}, f"source parses as {cand.kind!r}; only articles and books resolve by DOI"
    try:
        work = Crossref(CACHE_DIR / "crossref").work(doi)
    except CrossrefError as exc:
        return None, {}, str(exc)
    return judged(cand, work, "crossref")


def by_isbn(cand: Candidate, isbn: str, fetcher: Fetcher) -> tuple[Work | None, dict[str, dict[str, str]], str]:
    if cand.kind != "book":
        return None, {}, f"source parses as {cand.kind!r}; only books resolve by ISBN"
    try:
        work, statement = OpenLibrary(fetcher).edition_record(isbn)
    except WebError as exc:
        return None, {}, str(exc)
    # Books are cited by edition. When both sides state one, they must agree: the year
    # window alone cannot separate editions published in consecutive years.
    ours, theirs = edition_number(cand.raw), edition_number(statement)
    if ours is not None and theirs is not None and ours != theirs:
        return None, {}, f"edition mismatch: citation says {ours}, the record says {statement!r}"
    return judged(cand, work)


def by_landing(cand: Candidate, url: str, fetcher: Fetcher) -> tuple[Work | None, dict[str, dict[str, str]], str]:
    if authority_for(url, load_authorities("publishers")) is None:
        return None, {}, f"{url} is not on a publishers domain in references/authorities.yaml"
    try:
        final_url, html = fetcher.get(url)
    except WebError as exc:
        return None, {}, str(exc)
    doi = landing_doi(html)
    if doi:
        return None, {}, f"the page declares DOI {doi}: admit it with --doi"
    work = citation_meta_to_work(html, final_url)
    if work is None:
        return None, {}, "the page carries no citation_title / citation_author meta tags"
    return judged(cand, work)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--doi")
    mode.add_argument("--isbn")
    mode.add_argument("--url")
    mode.add_argument("--list-editions", action="store_true", help="print Open Library editions; admits nothing")
    parser.add_argument("--source", required=True, help="citation string in curriculum house format")
    parser.add_argument("--used-by", nargs="+", default=[], help="unit IDs that cite it")
    parser.add_argument("--dry-run", action="store_true", help="verify and print the record; write nothing")
    args = parser.parse_args()

    cand = parse_source(args.source)
    fetcher = Fetcher(CACHE_DIR / "web")

    if args.list_editions:
        if cand.kind != "book" or not cand.title or not cand.first_author:
            return reject(f"source parses as {cand.kind!r}; editions can be listed only for books")
        try:
            hits = OpenLibrary(fetcher).search(cand.title, cand.first_author, limit=10)
        except WebError as exc:
            return reject(str(exc))
        print(json.dumps(hits, indent=2, ensure_ascii=False))
        return 0
    if not args.used_by:
        return reject("--used-by is required when admitting a reference")

    if args.doi:
        work, notes, reason = by_doi(cand, args.doi)
        verified_by, short = "crossref", ""
    elif args.isbn:
        work, notes, reason = by_isbn(cand, args.isbn, fetcher)
        verified_by, short = "openlibrary", ""
    elif cand.kind in ("primary", "practitioner"):
        authority = authority_for(args.url, load_authorities("issuers"))
        if authority is None:
            return reject(f"{args.url} is not on an issuers domain in references/authorities.yaml")
        try:
            final_url, html = fetcher.get(args.url)
        except WebError as exc:
            return reject(str(exc))
        work, recall = primary_to_work(args.source, html, final_url, authority)
        if recall < PRIMARY_TITLE_RECALL:
            return reject(f"the page's title covers {recall:.0%} of the citation's title words: '{work.title}'")
        notes, reason = {"title_recall": {"curriculum": args.source, "record": f"{recall:.2f}"}}, ""
        verified_by, short = "issuer", authority.short
    elif cand.kind == "article":
        work, notes, reason = by_landing(cand, args.url, fetcher)
        verified_by, short = "landing", ""
    else:
        return reject(f"source parses as {cand.kind!r}; --url admits articles and primary documents only")

    if work is None:
        return reject(reason)
    if args.dry_run:
        existing = registered(registry.load(), work)
        if existing is not None:
            print(f"WOULD UPDATE {existing['key']} used_by={sorted(set(existing['used_by']) | set(args.used_by))}")
        else:
            print(f"WOULD ADD ({verified_by}): {describe(work)} url={work.url} isbn={list(work.isbn)} notes={notes}")
        return 0
    return admit(work, source=args.source, used_by=args.used_by, verified_by=verified_by, notes=notes, short=short)


if __name__ == "__main__":
    sys.exit(main())
