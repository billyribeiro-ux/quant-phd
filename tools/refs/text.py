"""Text normalization shared by the parser and the matcher."""

from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher

_NON_ALNUM = re.compile(r"[^a-z0-9]+")
_LEADING_THE = re.compile(r"^the\s+")


# Letters that are not base-letter + combining-mark sequences, so NFKD leaves them intact.
_SPECIAL = str.maketrans(
    {
        "Ø": "O",
        "ø": "o",
        "Æ": "AE",
        "æ": "ae",
        "ß": "ss",
        "Ł": "L",
        "ł": "l",
        "Đ": "D",
        "đ": "d",
        "Þ": "Th",
        "þ": "th",
        "Œ": "OE",
        "œ": "oe",
    }
)


def ascii_fold(text: str) -> str:
    """Strip accents: 'Zakrajšek' -> 'Zakrajsek', 'López' -> 'Lopez', 'Øksendal' -> 'Oksendal'."""
    decomposed = unicodedata.normalize("NFKD", text.translate(_SPECIAL))
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def norm(text: str) -> str:
    """Lowercase, accent-free, '&' -> 'and', punctuation collapsed to single spaces."""
    folded = ascii_fold(text).lower().replace("&", " and ")
    return _NON_ALNUM.sub(" ", folded).strip()


def norm_venue(text: str) -> str:
    """Venue comparison key: normalized, leading 'the' removed."""
    return _LEADING_THE.sub("", norm(text))


def surname_matches(expected: str, candidate_family: str) -> bool:
    """True when two surnames denote the same person.

    Handles particles and compound names ('López de Prado' vs 'Lopez de Prado',
    'de Roon' vs 'De Roon', 'Collin-Dufresne' vs 'Collin Dufresne') by
    comparing normalized forms, then the final token.
    """
    a, b = norm(expected), norm(candidate_family)
    if not a or not b:
        return False
    if a == b or a.replace(" ", "") == b.replace(" ", ""):
        return True
    return a.split()[-1] == b.split()[-1]


def similarity(a: str, b: str) -> float:
    """Normalized similarity in [0, 1] between two titles."""
    return SequenceMatcher(None, norm(a), norm(b)).ratio()


def norm_issue(issue: str) -> str:
    """Issue comparison key: '1-2', '1/2', '1 2' and the en-dash range all compare equal."""
    return _NON_ALNUM.sub("-", ascii_fold(issue).lower().replace("–", "-")).strip("-")


def surname_fuzzy(expected: str, candidate_family: str) -> bool:
    """Lenient surname match for malformed Crossref names ('XIAOYANNI' for Ni, 'Collin-Dufresn').

    Only ever used as a fallback when title, volume and issue already agree exactly.
    """
    a, b = norm(expected).replace(" ", ""), norm(candidate_family).replace(" ", "")
    if not a or not b:
        return False
    return b.endswith(a) or a.endswith(b) or SequenceMatcher(None, a, b).ratio() >= 0.85
