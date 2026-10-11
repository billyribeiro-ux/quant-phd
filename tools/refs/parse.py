"""Parse curriculum source strings into structured citation candidates.

Curriculum sources are written in a small set of house formats::

    Moskowitz, Ooi & Pedersen (2012), JFE 104(2)                    article
    Harvey et al. (2018), JPM 45(1)                                 article, et al.
    Goldberg (1991), 'What Every Computer Scientist ...', ACM Computing Surveys 23(1)
    Cochrane, Asset Pricing, revised ed. (2005)                     book
    FASB Accounting Standards Codification (primary)                primary document
    Gabaix & Koijen, inelastic markets hypothesis [WP][V]           unresolved pointer

The parser is intentionally conservative: anything it cannot classify with
confidence is returned as kind ``other`` and routed to human review rather
than guessed at.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal

from .journals import expand

Kind = Literal["article", "book", "primary", "practitioner", "pointer", "other"]

_FLAGS = re.compile(r"\s*\[(WP|V)\]")
_ARTICLE = re.compile(
    r"""^(?P<authors>[^()]+?)\s\((?P<year>\d{4})\),\s
        (?:'(?P<title>[^']+(?:'[a-z][^']*)*)',\s)?
        (?P<venue>.+?)
        (?:\s(?P<volume>\d+)(?:\((?P<issue>[^)]+)\))?)?
        (?P<tail>\s\(Supplement\)|,\s(?:Vol\.\s\d+|[A-Z][\w ]*))?$""",
    re.VERBOSE,
)
_BOOK = re.compile(r"^(?P<head>.+?),\s(?P<rest>.+?)\s\((?P<year>\d{4})\)$")
_EDITION = re.compile(r",\s(?:\d+(?:st|nd|rd|th)|revised|anniversary|latest)\sed\.$")
_AUTHOR_SPLIT = re.compile(r",\s|\s&\s")
_CASE = re.compile(r"\bv\.\s")  # court opinions: "Dirks v. SEC, 463 U.S. 646 (1983)"


@dataclass(frozen=True)
class Candidate:
    """A parsed curriculum source string."""

    raw: str
    kind: Kind
    authors: tuple[str, ...] = ()
    et_al: bool = False
    year: int | None = None
    title: str | None = None
    venue: str | None = None
    volume: str | None = None
    issue: str | None = None
    flags: frozenset[str] = field(default_factory=frozenset)

    @property
    def first_author(self) -> str | None:
        return self.authors[0] if self.authors else None

    def query(self) -> str:
        """Free-text bibliographic query for Crossref."""
        parts = [*self.authors]
        if self.title:
            parts.append(self.title)
        if self.venue:
            parts.append(expand(self.venue))
        if self.year:
            parts.append(str(self.year))
        return " ".join(parts) if parts else _FLAGS.sub("", self.raw)


def _split_authors(text: str) -> tuple[tuple[str, ...], bool]:
    et_al = text.endswith(" et al.")
    if et_al:
        text = text[: -len(" et al.")]
    names = tuple(n.strip() for n in _AUTHOR_SPLIT.split(text) if n.strip())
    return names, et_al


def _looks_like_author_list(text: str) -> bool:
    """Surname lists are short capitalized tokens; titles contain lowercase function words."""
    names, _ = _split_authors(text)
    if not names or len(names) > 8:
        return False
    for name in names:
        words = name.split()
        if len(words) > 4:
            return False
        if not any(w[:1].isupper() for w in words):
            return False
        if any(w.lower() in {"of", "the", "for", "in", "and", "to", "with", "a"} for w in words):
            return False
    return True


def parse_source(raw: str) -> Candidate:
    """Classify and parse one curriculum source string."""
    flags = frozenset(_FLAGS.findall(raw))
    text = _FLAGS.sub("", raw).strip()
    lowered = text.lower()

    if "(primary)" in lowered or lowered.endswith("primary)") or _CASE.search(text):
        return Candidate(raw=raw, kind="primary", flags=flags)
    if "practitioner" in lowered:
        return Candidate(raw=raw, kind="practitioner", flags=flags)

    match = _ARTICLE.match(text)
    if match and _looks_like_author_list(match["authors"]):
        authors, et_al = _split_authors(match["authors"])
        return Candidate(
            raw=raw,
            kind="article",
            authors=authors,
            et_al=et_al,
            year=int(match["year"]),
            title=match["title"],
            venue=match["venue"].strip(),
            volume=match["volume"],
            issue=match["issue"],
            flags=flags,
        )

    match = _BOOK.match(text)
    if match:
        # Book format: "<authors>, <title>[, <edition>]". Multi-author lists end with
        # "X & Y", so the author list runs through the first chunk containing " & ";
        # with no such chunk the book has a single author (the first chunk). Titles are
        # never peeled by capitalization: "Calculus" or "Valuation" look like surnames.
        chunks = [c.strip() for c in f"{match['head']}, {match['rest']}".split(", ")]
        end = next((i for i, c in enumerate(chunks[:-1]) if " & " in c), 0)
        authors_text = ", ".join(chunks[: end + 1]).replace(" (eds.)", "")
        title = _EDITION.sub("", ", ".join(chunks[end + 1 :]))
        if _looks_like_author_list(authors_text) and title:
            authors, et_al = _split_authors(authors_text)
            return Candidate(
                raw=raw,
                kind="book",
                authors=authors,
                et_al=et_al,
                year=int(match["year"]),
                title=title,
                flags=flags,
            )

    if "V" in flags or "WP" in flags:
        head = text.split(",", 1)[0]
        authors, et_al = _split_authors(head) if _looks_like_author_list(head) else ((), False)
        return Candidate(raw=raw, kind="pointer", authors=authors, et_al=et_al, flags=flags)
    return Candidate(raw=raw, kind="other", flags=flags)
