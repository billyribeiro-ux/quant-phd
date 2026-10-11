"""Decide whether a Crossref work is the source a curriculum string refers to.

Identity is established conservatively. A work is accepted only when the
evidence that it *is* the cited item is strong; differences in secondary
fields (issue number, a one-year online-first offset, author count) are then
recorded as corrections to the curriculum string, never silently ignored.
Anything weaker goes to human review.

Article identity requires all of:
  * first-author surname match
  * venue match (after abbreviation expansion); for proceedings and book
    chapters, whose container names vary, a title match replaces it
  * publication year within one year
  * when both sides give a volume, the volumes agree
  * an anchor: matching volume, or matching title
  * when both sides give an issue and there is no title match, the issues agree
    (volume alone is weak for journals with one volume per year, such as PNAS)
  * the work is not an erratum, corrigendum, reply, discussion or front matter

When several works establish identity, the tie-break prefers, in order:
a matching title, matching issue, a complete author match, the exact year. Records that share a
normalized title (JSTOR and publisher DOIs for the same article) are
duplicates; the publisher DOI is kept.

Book identity requires all of:
  * first-author (or first-editor) surname match
  * a book-type record
  * title similarity >= 0.75
  * publication year within one year (editions drift)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal

from .crossref import Work
from .journals import venue_matches
from .parse import Candidate
from .text import norm, norm_issue, similarity, surname_fuzzy, surname_matches

_LEADING_NUMBER = re.compile(r"\d+")


def issue_matches(ours: str, theirs: str) -> bool:
    """'4' matches '4, Part 2'; a hyphenated range matches its en-dash spelling."""
    if norm_issue(ours) == norm_issue(theirs):
        return True
    a, b = _LEADING_NUMBER.match(ours.strip()), _LEADING_NUMBER.match(theirs.strip())
    return bool(a and b and a.group() == b.group() and not ("-" in ours or "-" in theirs))


Status = Literal["verified", "verified_with_corrections", "unresolved"]

ARTICLE_TYPES = frozenset({"journal-article", "proceedings-article", "book-chapter"})
# Working-paper records (NBER reports, SSRN posted-content) are acceptable only when
# the curriculum string itself cites a working paper; otherwise they are a different
# version of the cited article and must not stand in for it.
WORKING_PAPER_TYPES = frozenset({"report", "posted-content"})
BOOK_TYPES = frozenset({"book", "monograph", "edited-book", "reference-book", "book-set"})
_NOT_ORIGINAL = (
    "erratum",
    "corrigendum",
    "correction",
    "reply",
    "comment on",
    "retraction",
    "discussion",
    "front matter",
    "back matter",
    "issue information",
    "masthead",
    "editorial",
    "session",
)
_LOOSE_VENUE_TYPES = frozenset({"proceedings-article", "book-chapter"})
TITLE_MATCH = 0.80
BOOK_TITLE_MATCH = 0.75


@dataclass
class Assessment:
    work: Work
    identity: bool
    # field -> (curriculum, crossref). Corrections mean the curriculum string is wrong
    # and must be fixed; info records benign differences (an online-first year, or
    # a Crossref record that lists fewer authors than the article has).
    corrections: dict[str, tuple[str, str]] = field(default_factory=dict)
    info: dict[str, tuple[str, str]] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    fit: tuple[bool, bool, bool, bool] = (False, False, False, False)


@dataclass
class Resolution:
    status: Status
    work: Work | None
    corrections: dict[str, tuple[str, str]]
    candidates: list[Assessment]
    reason: str
    info: dict[str, tuple[str, str]] = field(default_factory=dict)


def _is_original(work: Work) -> bool:
    title = norm(work.title)
    return not any(title.startswith(norm(marker)) for marker in _NOT_ORIGINAL)


def _year_ok(cand_year: int | None, work: Work) -> tuple[bool, bool]:
    """(within one year, exact)."""
    if cand_year is None or not work.years:
        return False, False
    exact = cand_year in work.years
    close = exact or any(abs(cand_year - y) <= 1 for y in work.years)
    return close, exact


_VOLUME_MARKERS = frozenset({"i", "ii", "iii", "iv", "v", "vi", "1", "2", "3", "4", "5", "6"})


def volume_marker(title: str) -> str | None:
    """Trailing volume numeral of a title's main part: 'Stochastic Calculus for Finance II' -> 'ii'."""
    words = norm(title.split(":")[0]).split()
    return words[-1] if words and words[-1] in _VOLUME_MARKERS else None


def assess_article(cand: Candidate, work: Work) -> Assessment:
    a = Assessment(work=work, identity=False)
    if not work.authors or not cand.first_author:
        a.notes.append("no authors to compare")
        return a
    first = surname_matches(cand.first_author, work.authors[0].family)
    title_ok = (
        cand.title is not None
        and similarity(cand.title, work.title) >= TITLE_MATCH
        and volume_marker(cand.title) == volume_marker(work.title)
    )
    venue = cand.venue is not None and any(venue_matches(cand.venue, c) for c in work.container)
    if (
        not venue
        and title_ok
        and (work.type in _LOOSE_VENUE_TYPES or ("WP" in cand.flags and work.type in WORKING_PAPER_TYPES))
    ):
        venue = True
    year_close, year_exact = _year_ok(cand.year, work)
    both_volumes = cand.volume is not None and work.volume is not None
    volume_ok = both_volumes and cand.volume == str(work.volume).strip()
    issue_ok = None if not (cand.issue and work.issue) else issue_matches(cand.issue, work.issue)
    malformed_author = False
    if not first and title_ok and volume_ok and issue_ok and surname_fuzzy(cand.first_author, work.authors[0].family):
        first = malformed_author = True
    checks = {
        "first_author": first,
        "venue": venue,
        "year": year_close,
        "volume": volume_ok or not both_volumes,
        "anchor": volume_ok or title_ok,
        "issue": issue_ok is not False or title_ok,
        "original": _is_original(work),
        "type": work.type in ARTICLE_TYPES or ("WP" in cand.flags and work.type in WORKING_PAPER_TYPES),
    }
    a.identity = all(checks.values())
    a.fit = (title_ok, issue_ok is True, False, year_exact)
    if not a.identity:
        a.notes.append(" ".join(f"{k}={v}" for k, v in checks.items()))
        return a

    if not year_exact and cand.year is not None and work.year is not None:
        a.info["year"] = (str(cand.year), str(work.year))
    if malformed_author:
        a.info["crossref_author_name"] = (cand.first_author, work.authors[0].family)
    if issue_ok is False:
        a.corrections["issue"] = (str(cand.issue), str(work.issue))
    if cand.title and not title_ok:
        a.corrections["title"] = (cand.title, work.title)
    if not cand.et_al:
        ours_missing = [s for s in cand.authors if not any(surname_matches(s, w.family) for w in work.authors)]
        listed = work.authors[1:] if malformed_author else work.authors
        theirs_missing = [w.family for w in listed if not any(surname_matches(s, w.family) for s in cand.authors)]
        if theirs_missing:
            a.corrections["authors"] = (" & ".join(cand.authors), " & ".join(w.family for w in work.authors))
        elif ours_missing:
            a.info["authors"] = (" & ".join(cand.authors), " & ".join(w.family for w in work.authors))
        a.fit = (a.fit[0], a.fit[1], not theirs_missing and not ours_missing, a.fit[3])
    return a


def assess_book(cand: Candidate, work: Work) -> Assessment:
    a = Assessment(work=work, identity=False)
    if not work.authors or not cand.first_author or not cand.title:
        a.notes.append("missing authors or title")
        return a
    first = surname_matches(cand.first_author, work.authors[0].family)
    title_score = max(similarity(cand.title, work.title), similarity(cand.title, work.title.split(":")[0]))
    same_volume = volume_marker(cand.title) == volume_marker(work.title)
    year_close, year_exact = _year_ok(cand.year, work)
    a.identity = first and work.type in BOOK_TYPES and title_score >= BOOK_TITLE_MATCH and same_volume and year_close
    if not a.identity:
        a.notes.append(
            f"first_author={first} type={work.type} title={title_score:.2f} "
            f"volume_marker={same_volume} year={year_close}"
        )
    elif not year_exact and cand.year is not None and work.year is not None:
        a.info["year"] = (str(cand.year), str(work.year))
    a.fit = (title_score >= BOOK_TITLE_MATCH, False, first, year_exact)
    return a


def _dedupe(matches: list[Assessment]) -> list[Assessment]:
    """Collapse records of the same article (same normalized title), keeping the publisher DOI."""
    by_title: dict[str, Assessment] = {}
    for a in sorted(matches, key=lambda m: (m.work.doi.startswith("10.2307/"), m.work.doi)):
        by_title.setdefault(norm(a.work.title), a)
    return list(by_title.values())


def resolve(cand: Candidate, works: list[Work]) -> Resolution:
    """Pick the unique work that the candidate identifies, or explain why not."""
    assess = assess_article if cand.kind == "article" else assess_book
    assessments = [assess(cand, w) for w in works]
    matches = _dedupe([a for a in assessments if a.identity])
    if not matches:
        return Resolution("unresolved", None, {}, assessments, "no candidate established identity")
    best_fit = max(a.fit for a in matches)
    top = [a for a in matches if a.fit == best_fit]
    if len(top) > 1:
        options = "; ".join(f"{a.work.doi} '{a.work.title[:60]}'" for a in top)
        return Resolution("unresolved", None, {}, assessments, f"ambiguous: {options}")
    chosen = top[0]
    status: Status = "verified_with_corrections" if chosen.corrections else "verified"
    return Resolution(status, chosen.work, chosen.corrections, assessments, "identity established", chosen.info)
