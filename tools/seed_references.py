#!/usr/bin/env python3
"""Seed the citation registry from every source named in the curriculum.

For each source string in ``curriculum/*.yaml`` (plus ``references/extra_sources.yaml``
for citations made in the blueprint itself) this script:

1. parses the string (``refs.parse``);
2. searches Crossref for articles and books;
3. accepts a work only if ``refs.match`` establishes identity;
4. writes accepted works to ``references/references.json``;
5. writes everything else to ``references/review_queue.json`` with the best
   Crossref candidates and the reason it was not accepted;
6. writes ``references/corrections.json``, listing curriculum strings whose
   details (year, issue, authors, title) differ from Crossref, so they can be fixed
   at the source;
7. writes ``references/SEED_REPORT.md``.

Entries added by hand through ``add_reference.py`` (origin ``manual``) are preserved.

Usage::

    python3 tools/seed_references.py [--workers 4] [--no-cache]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any

import yaml

from refs import registry
from refs.crossref import Crossref, CrossrefError, Work
from refs.journals import expand
from refs.match import Resolution, resolve
from refs.parse import Candidate, parse_source

ROOT = registry.ROOT
REFS_DIR = ROOT / "references"
CACHE_DIR = ROOT / ".cache" / "crossref"


@dataclass
class Outcome:
    candidate: Candidate
    used_by: list[str]
    resolution: Resolution | None
    error: str | None = None


def collect_sources() -> dict[str, list[str]]:
    """Map each distinct source string to the units that cite it, in curriculum order."""
    sources: dict[str, list[str]] = {}
    for path in sorted((ROOT / "curriculum").glob("[0-9][0-9]-*.yaml")):
        for part in yaml.safe_load(path.read_text(encoding="utf-8"))["parts"]:
            for module in part["modules"]:
                for source in module["sources"]:
                    sources.setdefault(source, []).append(module["id"])
    extra = REFS_DIR / "extra_sources.yaml"
    if extra.exists():
        for item in yaml.safe_load(extra.read_text(encoding="utf-8"))["sources"]:
            sources.setdefault(item["source"], []).extend(item["used_by"])
    return sources


def load_hints() -> dict[str, str]:
    """Source string -> DOI hypotheses. A hint only adds a candidate; identity is still checked."""
    path = REFS_DIR / "doi_hints.yaml"
    if not path.exists():
        return {}
    return {h["source"]: h["doi"] for h in yaml.safe_load(path.read_text(encoding="utf-8"))["hints"]}


HINTS = load_hints()


def search(client: Crossref, cand: Candidate) -> list[Work]:
    """Three passes, stopping at the first that resolves.

    1. Bibliographic query anchored on the first author.
    2. Bibliographic query alone (author matching sometimes fails on accents).
    3. Journal-scoped: every work by the first author in the named journal within
       the year window. This finds older JSTOR-era articles that free-text search
       ranks poorly when the curriculum string carries no title.
    """
    if cand.year is None:
        return []
    # Search wide: Crossref often dates a paper by its online-first release, up to a
    # few years before the print issue. Identity is still judged against the print,
    # online and issued years, within one year (refs.match).
    lo, hi = cand.year - 3, cand.year + 1
    works: list[Work] = []

    def extend(batch: list[Work]) -> bool:
        seen = {w.doi for w in works}
        works.extend(w for w in batch if w.doi not in seen)
        return resolve(cand, works).status != "unresolved"

    hint = HINTS.get(cand.raw)
    if hint:
        try:
            if extend([client.work(hint)]):
                return works
        except CrossrefError:
            pass  # a bad hint is reported through the unresolved review item
    if extend(client.search(cand.query(), author=cand.first_author, year_range=(lo, hi))):
        return works
    if extend(client.search(cand.query(), year_range=(lo, hi))):
        return works
    if cand.kind == "article" and cand.venue and cand.first_author:
        for issn in client.journal_issns(expand(cand.venue))[:2]:
            if extend(client.journal_works(issn, author=cand.first_author, year_range=(lo, hi))):
                break
    return works


def process(client: Crossref, cand: Candidate, used_by: list[str]) -> Outcome:
    if cand.kind not in ("article", "book"):
        return Outcome(cand, used_by, None)
    try:
        works = search(client, cand)
    except CrossrefError as exc:
        return Outcome(cand, used_by, None, error=str(exc))
    return Outcome(cand, used_by, resolve(cand, works))


_NO_DOI_VENUES = (
    "American Economic Review",
    "Journal of Economic Literature",
    "Harvard Business Review",
    "Risk",
    "NeurIPS",
    "Journal of Machine Learning Research",
    "Wilmott Magazine",
    "Journal of Financial Planning",
    "International Journal of Central Banking",
    "Jackson Hole Economic Policy Symposium",
    "Bank of England Quarterly Bulletin",
    "Proceedings of the Fourth Berkeley Symposium",
)


def cand_has_no_doi_venue(cand: Candidate) -> bool:
    venue = expand(cand.venue) if cand.venue else ""
    return any(venue.startswith(v) for v in _NO_DOI_VENUES)


def summarize(work: Work) -> dict[str, Any]:
    return {
        "doi": work.doi,
        "type": work.type,
        "title": work.title,
        "first_author": work.authors[0].family if work.authors else None,
        "authors": len(work.authors),
        "year": work.year,
        "container": work.container[0] if work.container else None,
        "volume": work.volume,
        "issue": work.issue,
    }


def build(
    outcomes: list[Outcome], preserved: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    by_doi: dict[str, registry.Entry] = {}
    corrections: list[dict[str, Any]] = []
    review: list[dict[str, Any]] = []
    stamp = registry.now()

    for out in outcomes:
        res = out.resolution
        if res is not None and res.work is not None:
            entry = by_doi.get(res.work.doi)
            if entry is None:
                entry = registry.Entry(
                    key="",
                    work=res.work,
                    status=res.status,
                    origin="seed",
                    source_strings=[],
                    used_by=[],
                    corrections={},
                    resolved_at=stamp,
                )
                by_doi[res.work.doi] = entry
            entry.source_strings.append(out.candidate.raw)
            entry.used_by.extend(out.used_by)
            for name, (ours, theirs) in res.info.items():
                entry.notes[name] = {"curriculum": ours, "crossref": theirs}
            if res.corrections:
                entry.status = "verified_with_corrections"
                for name, (ours, theirs) in res.corrections.items():
                    entry.corrections[name] = {"curriculum": ours, "crossref": theirs}
                corrections.append(
                    {
                        "source": out.candidate.raw,
                        "doi": res.work.doi,
                        "used_by": out.used_by,
                        "corrections": {k: {"curriculum": a, "crossref": b} for k, (a, b) in res.corrections.items()},
                    }
                )
            continue
        item: dict[str, Any] = {
            "source": out.candidate.raw,
            "kind": out.candidate.kind,
            "used_by": out.used_by,
            "flags": sorted(out.candidate.flags),
        }
        if out.error:
            item["reason"] = f"crossref error: {out.error}"
        elif res is None:
            item["reason"] = {
                "primary": "primary document: add manually with an authoritative URL",
                "practitioner": "practitioner source: add manually with an authoritative URL",
                "pointer": "pointer to a work not yet pinned down: identify the exact paper, then add by DOI",
                "other": "not a citable work: replace with specific registry keys",
            }.get(out.candidate.kind, "not resolvable automatically")
        else:
            item["reason"] = res.reason
            if cand_has_no_doi_venue(out.candidate):
                item["reason"] += (
                    "; venue has no Crossref DOIs for this period (e.g. pre-1999 AER/JEL on JSTOR, HBR, Risk,"
                    " NeurIPS, JMLR): verify against OpenAlex (set OPENALEX_API_KEY) or the publisher's stable URL,"
                    " then add as a manual entry"
                )
            ranked = sorted(res.candidates, key=lambda a: (not a.identity, len(a.notes)))[:3]
            item["candidates"] = [summarize(a.work) | {"notes": a.notes} for a in ranked]
        review.append(item)

    entries = list(by_doi.values())
    registry.assign_keys(entries)
    seeded = [e.to_json() for e in entries]
    manual = [e for e in preserved if e.get("origin") == "manual" and e["doi"] not in by_doi]
    return seeded + manual, review, corrections


def write_report(
    entries: list[dict[str, Any]],
    review: list[dict[str, Any]],
    corrections: list[dict[str, Any]],
    outcomes: list[Outcome],
) -> None:
    kinds = Counter(o.candidate.kind for o in outcomes)
    statuses = Counter((o.resolution.status if o.resolution else "not-searched") for o in outcomes)
    lines = [
        "# Reference seeding report",
        "",
        f"Generated {registry.now()} by `tools/seed_references.py`.",
        "",
        "| Measure | Count |",
        "|---|---|",
        f"| Distinct source strings | {len(outcomes)} |",
        *(f"| Kind: {k} | {v} |" for k, v in sorted(kinds.items())),
        *(f"| Status: {k} | {v} |" for k, v in sorted(statuses.items())),
        f"| Registry entries (distinct DOIs) | {len(entries)} |",
        f"| Curriculum strings needing correction | {len(corrections)} |",
        f"| Review queue | {len(review)} |",
        "",
        "## Corrections (curriculum string differs from Crossref)",
        "",
        "| Source string | Field | Curriculum | Crossref | DOI |",
        "|---|---|---|---|---|",
    ]
    for c in corrections:
        for field_name, diff in c["corrections"].items():
            lines.append(f"| {c['source']} | {field_name} | {diff['curriculum']} | {diff['crossref']} | {c['doi']} |")
    lines += ["", "## Review queue", ""]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in review:
        grouped[item["kind"]].append(item)
    for kind in sorted(grouped):
        lines.append(f"### {kind} ({len(grouped[kind])})\n")
        for item in grouped[kind]:
            lines.append(f"- `{item['source']}` — {item['reason']} (used by {', '.join(item['used_by'])})")
        lines.append("")
    (REFS_DIR / "SEED_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()

    client = Crossref(None if args.no_cache else CACHE_DIR)
    sources = collect_sources()
    candidates = [(parse_source(s), used_by) for s, used_by in sources.items()]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        outcomes = list(pool.map(lambda pair: process(client, *pair), candidates))

    entries, review, corrections = build(outcomes, registry.load())
    registry.save(entries)
    (REFS_DIR / "review_queue.json").write_text(json.dumps(review, indent=2, ensure_ascii=False) + "\n", "utf-8")
    (REFS_DIR / "corrections.json").write_text(json.dumps(corrections, indent=2, ensure_ascii=False) + "\n", "utf-8")
    write_report(entries, review, corrections, outcomes)

    errors = sum(1 for o in outcomes if o.error)
    print(
        f"sources={len(outcomes)} registry={len(entries)} corrections={len(corrections)} "
        f"review={len(review)} errors={errors}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
