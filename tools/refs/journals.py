"""Venue abbreviations used in the curriculum, mapped to their full names.

Matching is done on normalized names (see ``text.norm_venue``), so the
leading 'The' and punctuation differences in Crossref container titles do not
matter. Only abbreviations need listing; full names pass through unchanged.
"""

from __future__ import annotations

from .text import norm_venue

ABBREVIATIONS: dict[str, str] = {
    "JF": "Journal of Finance",
    "JFE": "Journal of Financial Economics",
    "RFS": "Review of Financial Studies",
    "AER": "American Economic Review",
    "QJE": "Quarterly Journal of Economics",
    "JPE": "Journal of Political Economy",
    "JME": "Journal of Monetary Economics",
    "JET": "Journal of Economic Theory",
    "JPM": "Journal of Portfolio Management",
    "FAJ": "Financial Analysts Journal",
    "REStud": "Review of Economic Studies",
    "REStat": "Review of Economics and Statistics",
    "JEL": "Journal of Economic Literature",
    "JBES": "Journal of Business & Economic Statistics",
    "JFQA": "Journal of Financial and Quantitative Analysis",
    "JASA": "Journal of the American Statistical Association",
    "JRSS-B": "Journal of the Royal Statistical Society Series B",
    "PNAS": "Proceedings of the National Academy of Sciences",
    "AEJ: Macroeconomics": "American Economic Journal: Macroeconomics",
    "IER": "International Economic Review",
    "ACM SIGCOMM CCR": "ACM SIGCOMM Computer Communication Review",
}

# Venues whose Crossref container titles legitimately differ from the name
# used in the curriculum (renames, series suffixes). Values are alternative
# full names accepted as equivalent.
EQUIVALENT_VENUES: dict[str, tuple[str, ...]] = {
    "Journal of the Royal Statistical Society Series B": (
        "Journal of the Royal Statistical Society Series B Methodological",
        "Journal of the Royal Statistical Society Series B Statistical Methodology",
    ),
    "Bell Journal of Economics": ("Bell Journal of Economics and Management Science",),
    "Review of Accounting Studies": (),
    "Journal of Business": (),
    "European Finance Review": ("Review of Finance",),
    "Journal of Financial Econometrics": (),
    "Journal of End User Computing": ("Journal of Organizational and End User Computing",),
    "Carnegie-Rochester Conference Series on Public Policy": (),
    "Journal of Computational Finance": (),
}


def expand(venue: str) -> str:
    """Expand a curriculum venue abbreviation to its full name."""
    return ABBREVIATIONS.get(venue.strip(), venue.strip())


def venue_matches(expected: str, candidate: str) -> bool:
    """True when a Crossref container title denotes the expected venue.

    Exact match on normalized names only, against the full name and its listed
    equivalents. Prefix matching is deliberately not used: 'Journal of Business'
    is a prefix of 'Journal of Business & Economic Statistics', and 'American
    Economic Review' of 'American Economic Review: Insights'.
    """
    full = expand(expected)
    names = (full, *EQUIVALENT_VENUES.get(full, ()))
    cand = norm_venue(candidate)
    return bool(cand) and any(norm_venue(name) == cand for name in names)
