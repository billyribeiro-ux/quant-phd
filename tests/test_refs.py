"""Offline tests for the reference tooling.

Every test that encodes a failure mode found while seeding the real registry
names it, so the regression stays explained.
"""

from __future__ import annotations

import pytest

from refs.crossref import Author, Work, clean
from refs.journals import expand, venue_matches
from refs.match import issue_matches, resolve, volume_marker
from refs.parse import parse_source
from refs.registry import Entry, assign_keys, base_key
from refs.text import ascii_fold, surname_fuzzy, surname_matches


def work(
    *,
    doi: str = "10.1/x",
    type: str = "journal-article",
    title: str = "A Title",
    authors: tuple[str, ...] = ("Smith",),
    container: str | None = "Journal of Finance",
    volume: str | None = "50",
    issue: str | None = "1",
    years: tuple[int, ...] = (1995,),
) -> Work:
    return Work(
        doi=doi,
        type=type,
        title=title,
        authors=tuple(Author(family=a, given="") for a in authors),
        container=(container,) if container else (),
        volume=volume,
        issue=issue,
        pages=None,
        years=frozenset(years),
        year=min(years),
        isbn=(),
        publisher=None,
    )


# ---------------------------------------------------------------- text / venues


def test_ascii_fold_handles_non_decomposable_letters() -> None:
    # 'Ø' has no combining-mark decomposition; NFKD alone leaves it intact.
    assert ascii_fold("Øksendal") == "Oksendal"
    assert ascii_fold("Zakrajšek") == "Zakrajsek"


@pytest.mark.parametrize(
    ("ours", "theirs"),
    [("López de Prado", "Lopez de Prado"), ("de Roon", "De Roon"), ("Collin-Dufresne", "Collin‐Dufresne")],
)
def test_surname_matches_compound_names(ours: str, theirs: str) -> None:
    assert surname_matches(ours, theirs)


def test_surname_fuzzy_covers_malformed_crossref_names() -> None:
    # Real Crossref records: 'XIAOYANNI' for Ni (2005), 'Collin-Dufresn' for Collin-Dufresne (2001).
    assert surname_fuzzy("Ni", "XIAOYANNI")
    assert surname_fuzzy("Collin-Dufresne", "Collin-Dufresn")
    assert not surname_matches("Ni", "XIAOYANNI")


def test_venue_prefix_is_not_a_match() -> None:
    # Real prefix pairs: one venue's normalized name is a prefix of another's.
    assert not venue_matches("Journal of Business", "Journal of Business & Economic Statistics")
    assert not venue_matches("AER", "American Economic Review: Insights")
    assert not venue_matches("JF", "Journal of Financial Economics")
    assert venue_matches("JF", "The Journal of Finance")
    assert venue_matches("JRSS-B", "Journal of the Royal Statistical Society: Series B (Methodological)")


def test_clean_decodes_entities_and_footnotes() -> None:
    # Real Crossref containers carry '&amp;'; titles carry glued acknowledgement footnotes.
    assert clean("Journal of Business &amp; Economic Statistics") == "Journal of Business & Economic Statistics"
    assert clean("IPO Underpricing**Thanks for helpful comments go to") == "IPO Underpricing"
    assert clean("A model of investor sentiment1We are grateful to the NSF") == "A model of investor sentiment"


def test_expand_abbreviations() -> None:
    assert expand("JFE") == "Journal of Financial Economics"
    assert expand("Econometrica") == "Econometrica"


# ---------------------------------------------------------------- parsing


def test_parse_article_with_issue() -> None:
    c = parse_source("Moskowitz, Ooi & Pedersen (2012), JFE 104(2)")
    assert (c.kind, c.authors, c.year, c.venue, c.volume, c.issue) == (
        "article",
        ("Moskowitz", "Ooi", "Pedersen"),
        2012,
        "JFE",
        "104",
        "2",
    )


def test_parse_article_with_title_and_et_al() -> None:
    c = parse_source("Harris et al. (2020), 'Array Programming with NumPy', Nature 585(7825)")
    assert c.kind == "article" and c.et_al and c.title == "Array Programming with NumPy"
    assert (c.venue, c.volume, c.issue) == ("Nature", "585", "7825")


@pytest.mark.parametrize(
    ("raw", "authors", "title"),
    [
        # Single-word titles must not be mistaken for surnames.
        ("Spivak, Calculus, 4th ed. (2008)", ("Spivak",), "Calculus"),
        ("Koller, Goedhart & Wessels, Valuation, 7th ed. (2020)", ("Koller", "Goedhart", "Wessels"), "Valuation"),
        (
            "Hull, Options, Futures, and Other Derivatives, 11th ed. (2021)",
            ("Hull",),
            "Options, Futures, and Other Derivatives",
        ),
        (
            "MacLean, Thorp & Ziemba (eds.), The Kelly Capital Growth Investment Criterion (2011)",
            ("MacLean", "Thorp", "Ziemba"),
            "The Kelly Capital Growth Investment Criterion",
        ),
    ],
)
def test_parse_books(raw: str, authors: tuple[str, ...], title: str) -> None:
    c = parse_source(raw)
    assert (c.kind, c.authors, c.title) == ("book", authors, title)


@pytest.mark.parametrize(
    ("raw", "kind"),
    [
        ("FASB Accounting Standards Codification (primary)", "primary"),
        ("Dirks v. SEC, 463 U.S. 646 (1983)", "primary"),
        ("Gabaix & Koijen, inelastic markets hypothesis [WP][V]", "pointer"),
        ("All finance-degree module sources", "other"),
    ],
)
def test_parse_non_resolvable_kinds(raw: str, kind: str) -> None:
    assert parse_source(raw).kind == kind


# ---------------------------------------------------------------- matching


def test_exact_article_is_verified() -> None:
    c = parse_source("Smith (1995), JF 50(1)")
    res = resolve(c, [work()])
    assert res.status == "verified" and res.work is not None


def test_same_author_volume_but_wrong_issue_is_rejected_without_title() -> None:
    # PNAS has one volume per year: 'Freeman, PNAS 111' matched an unrelated Freeman paper.
    c = parse_source("Freeman et al. (2014), PNAS 111(23)")
    birds = work(
        title="Rapid upslope shifts",
        authors=("Freeman",),
        container="Proceedings of the National Academy of Sciences",
        volume="111",
        issue="12",
        years=(2014,),
    )
    assert resolve(c, [birds]).status == "unresolved"


def test_working_paper_version_does_not_stand_in_for_article() -> None:
    # Shiller (1981, AER) resolved to the 1980 NBER working paper before this rule.
    c = parse_source("Shiller (1981), 'Do Stock Prices Move Too Much', AER 71(3)")
    nber = work(
        type="report",
        title="Do Stock Prices Move Too Much",
        authors=("Shiller",),
        container=None,
        volume=None,
        issue=None,
        years=(1980,),
    )
    assert resolve(c, [nber]).status == "unresolved"


def test_working_paper_type_rejected_even_when_venue_matches() -> None:
    # The type rule must hold on its own, not only because a WP record lacks a venue.
    c = parse_source("Shiller (1981), 'Do Stock Prices Move Too Much', AER 71(3)")
    wp = work(
        type="report",
        title="Do Stock Prices Move Too Much",
        authors=("Shiller",),
        container="American Economic Review",
        volume="71",
        issue="3",
        years=(1981,),
    )
    assert resolve(c, [wp]).status == "unresolved"


def test_working_paper_accepted_when_source_cites_one() -> None:
    c = parse_source(
        "Svensson (1994), 'Estimating and Interpreting Forward Interest Rates', NBER Working Paper 4871 [WP]"
    )
    nber = work(
        type="report",
        title="Estimating and Interpreting Forward Interest Rates",
        authors=("Svensson",),
        container=None,
        volume=None,
        issue=None,
        years=(1994,),
    )
    assert resolve(c, [nber]).status == "verified"


def test_title_breaks_tie_between_same_issue_papers() -> None:
    # Cox, Ingersoll & Ross published two papers in Econometrica 53(2).
    c = parse_source(
        "Cox, Ingersoll & Ross (1985), 'A Theory of the Term Structure of Interest Rates', Econometrica 53(2)"
    )
    cir = ("Cox", "Ingersoll", "Ross")
    a = work(
        doi="10.2307/1911241",
        title="An Intertemporal General Equilibrium Model of Asset Prices",
        authors=cir,
        container="Econometrica",
        volume="53",
        issue="2",
        years=(1985,),
    )
    b = work(
        doi="10.2307/1911242",
        title="A Theory of the Term Structure of Interest Rates",
        authors=cir,
        container="Econometrica",
        volume="53",
        issue="2",
        years=(1985,),
    )
    res = resolve(c, [a, b])
    assert res.work is not None and res.work.doi == "10.2307/1911242"


def test_jstor_duplicate_collapses_to_publisher_doi() -> None:
    c = parse_source("Smith (1995), JF 50(1)")
    res = resolve(c, [work(doi="10.2307/123"), work(doi="10.1111/abc")])
    assert res.work is not None and res.work.doi == "10.1111/abc"


def test_book_volume_numerals_must_agree() -> None:
    # 'Stochastic Calculus for Finance II' matched volume I before this rule.
    c = parse_source("Shreve, Stochastic Calculus for Finance II (2004)")
    vol1 = work(
        type="book",
        title="Stochastic Calculus for Finance I: The Binomial Asset Pricing Model",
        authors=("Shreve",),
        container=None,
        volume=None,
        issue=None,
        years=(2004,),
    )
    assert volume_marker("Stochastic Calculus for Finance II") == "ii"
    assert resolve(c, [vol1]).status == "unresolved"


def test_online_first_year_is_info_not_correction() -> None:
    c = parse_source("Corsi (2009), Journal of Financial Econometrics 7(2)")
    w = work(
        title="A Simple Approximate Long-Memory Model",
        authors=("Corsi",),
        container="Journal of Financial Econometrics",
        volume="7",
        issue="2",
        years=(2008,),
    )
    res = resolve(c, [w])
    assert res.status == "verified" and "year" in res.info and not res.corrections


@pytest.mark.parametrize(
    ("ours", "theirs", "ok"), [("4", "4, Part 2", True), ("2-3", "2–3", True), ("2", "2-3", False)]
)
def test_issue_matching(ours: str, theirs: str, ok: bool) -> None:
    assert issue_matches(ours, theirs) is ok


# ---------------------------------------------------------------- registry keys


def test_keys_are_stable_and_unique() -> None:
    w1 = work(doi="10.1/a", title="The Cost of Capital", authors=("Modigliani", "Miller"), years=(1958,))
    w2 = work(doi="10.1/b", title="The Cost of Equity", authors=("Modigliani",), years=(1958,))
    assert base_key(w1) == "modigliani1958cost"
    entries = [Entry("", w, "verified", "seed", [], [], {}, "now") for w in (w2, w1)]
    assign_keys(entries)
    assert sorted(e.key for e in entries) == ["modigliani1958cost", "modigliani1958costb"]
    assert next(e for e in entries if e.work.doi == "10.1/a").key == "modigliani1958cost"
