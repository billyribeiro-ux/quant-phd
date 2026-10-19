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


def test_correction_record_does_not_stand_in_for_the_original() -> None:
    # A correction shares authors, venue and often the original's title words; it is not the article.
    c = parse_source("Politis & White (2004), Econometric Reviews 23(1)")
    correction = work(
        title="Correction to “Automatic Block-Length Selection for the Dependent Bootstrap” by D. Politis and H. White",
        authors=("Politis", "White"),
        container="Econometric Reviews",
        volume="23",
        issue="1",
        years=(2004,),
    )
    assert resolve(c, [correction]).status == "unresolved"


def test_citation_that_names_a_correction_matches_it() -> None:
    title = "Correction to “Automatic Block-Length Selection for the Dependent Bootstrap” by D. Politis and H. White"
    c = parse_source(f"Patton, Politis & White (2009), '{title}', Econometric Reviews 28(4)")
    correction = work(
        title=title,
        authors=("Patton", "Politis", "White"),
        container="Econometric Reviews",
        volume="28",
        issue="4",
        years=(2009,),
    )
    assert resolve(c, [correction]).status == "verified"
    # Naming a different marker than the record carries is still not a match.
    reply = work(
        title=f"Reply to {title}",
        authors=("Patton", "Politis", "White"),
        container="Econometric Reviews",
        volume="28",
        issue="4",
        years=(2009,),
    )
    assert resolve(c, [reply]).status == "unresolved"


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
    ("ours", "theirs", "ok"),
    [
        ("4", "4, Part 2", True),
        ("2-3", "2–3", True),
        ("2", "2-3", False),
        # Crossref zero-pads some issues (Econometric Theory 24 records "02"); the number is the same issue.
        ("2", "02", True),
        ("02", "2", True),
        ("2", "12", False),
        ("2", "20", False),
        ("02", "20", False),
        # A single issue never matches a double issue, in any spelling a range can take.
        ("2", "02–03", False),
        ("2", "2–3", False),
        ("2", "2—3", False),
        ("2", "2/3", False),
        ("2", "2 3", False),
        ("2–3", "2", False),
        ("02-03", "2-3", True),
        ("2–3", "2/3", True),
        ("2", "2, 3", False),
        ("2", "2&3", False),
        ("2", "2 & 3", False),
        ("2", "2+3", False),
        ("2", "2\u20153", False),
        ("2", "2\u22123", False),
        ("2-3", "2, 3", True),
        ("1-2", "3-4", False),
        ("2-3", "2-4", False),
        ("1-3", "2-3", False),
        ("2-3", "1-3", False),
        ("02-03", "2-4", False),
        ("1-2", "1-2, Suppl", True),
        # Not ranges: a part or a letter suffix still matches its issue.
        ("366", "366a", True),
        ("4", "4, Part 1", True),
    ],
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


# ---------------------------------------------------------------- non-DOI verification sources

JMLR_PAGE = """<html><head><title>Scikit-learn: Machine Learning in Python</title>
<meta name="citation_title" content="Scikit-learn: Machine Learning in Python">
<meta name="citation_author" content="Fabian Pedregosa">
<meta name="citation_author" content="Ga&euml;l Varoquaux">
<meta name="citation_journal_title" content="Journal of Machine Learning Research">
<meta name="citation_volume" content="12">
<meta name="citation_issue" content="85">
<meta name="citation_firstpage" content="2825">
<meta name="citation_lastpage" content="2830">
<meta name="citation_publication_date" content="2011">
</head><body><h1>Scikit-learn</h1></body></html>"""


def test_landing_meta_builds_a_work_the_matcher_accepts() -> None:
    # JMLR registers no DOIs; its landing page carries Highwire citation_* tags.
    from refs.web import citation_meta_to_work, landing_doi

    page = citation_meta_to_work(JMLR_PAGE, "https://www.jmlr.org/papers/v12/pedregosa11a.html")
    assert page is not None
    assert page.authors[0].family == "Pedregosa" and page.authors[1].given == "Gaël"
    assert (page.year, page.volume, page.pages, page.type) == (2011, "12", "2825-2830", "journal-article")
    assert landing_doi(JMLR_PAGE) is None
    res = resolve(parse_source("Pedregosa et al. (2011), Journal of Machine Learning Research 12"), [page])
    assert res.status == "verified"
    # Volume is the anchor here (no title in the string): a wrong volume must not pass.
    wrong_volume = parse_source("Pedregosa et al. (2011), Journal of Machine Learning Research 13")
    assert resolve(wrong_volume, [page]).work is None


def test_landing_page_with_a_doi_is_detected() -> None:
    from refs.web import landing_doi

    assert landing_doi('<meta name="citation_doi" content="10.1111/j.1540-6261.1964.tb02865.x">') == (
        "10.1111/j.1540-6261.1964.tb02865.x"
    )


def test_open_library_edition_builds_a_book_work() -> None:
    from refs.web import edition_to_work

    edition = {
        "title": "Calculus",
        "publish_date": "2008",
        "publishers": ["Publish or Perish, inc"],
        "isbn_13": ["9780914098911"],
        "edition_name": "Fourth Edition",
    }
    book = edition_to_work(edition, ["Michael Spivak"], "https://openlibrary.org/books/OL28292750M")
    assert (book.type, book.year, book.authors[0].family, book.isbn) == ("book", 2008, "Spivak", ("9780914098911",))
    assert resolve(parse_source("Spivak, Calculus, 4th ed. (2008)"), [book]).status == "verified"
    # Real Open Library record for the 1980 2nd edition: the year window rejects it.
    old = edition_to_work(edition | {"publish_date": "1980"}, ["Michael Spivak"], "u")
    assert resolve(parse_source("Spivak, Calculus, 4th ed. (2008)"), [old]).work is None


@pytest.mark.parametrize(
    ("text", "number"),
    [
        ("Spivak, Calculus, 4th ed. (2008)", 4),
        ("Fourth Edition", 4),
        ("2d ed.", 2),  # real Open Library edition statement for Spivak (1980)
        ("3 edition", 3),
        ("3rd, corrected ed.", None),  # ambiguous statement: no claim either way
        ("Cochrane, Asset Pricing, revised ed. (2005)", None),
        (None, None),
    ],
)
def test_edition_number(text: str | None, number: int | None) -> None:
    from refs.web import edition_number

    assert edition_number(text) == number


def test_primary_documents_need_an_authority_and_a_matching_title() -> None:
    from refs.web import Authority, authority_for, primary_title, primary_to_work, title_recall

    authorities = [Authority("federalreserve.gov", "Board of Governors of the Federal Reserve System", "frb")]
    raw = "Federal Reserve SR 11-7, Guidance on Model Risk Management (2011) (primary)"
    assert primary_title(raw) == "Federal Reserve SR 11-7, Guidance on Model Risk Management"
    assert authority_for("https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm", authorities)
    # A mirror on another domain is never authoritative, whatever its content.
    assert authority_for("https://www.federalreserve.gov.example.com/sr1107.htm", authorities) is None
    page = "<title>Supervisory Letter SR 11-7 on guidance on Model Risk Management -- April 4, 2011</title>"
    work, recall = primary_to_work(raw, page, "https://www.federalreserve.gov/x", authorities[0])
    assert recall >= 0.6 and work.year == 2011 and work.authors[0].family.startswith("Board of Governors")
    assert title_recall(primary_title(raw), ["Monetary Policy Report"]) < 0.6
    # A year the page does not confirm is not recorded.
    assert primary_to_work(raw, "<title>Model Risk Management SR 11-7</title>", "u", authorities[0])[0].year is None


# ---------------------------------------------------------------- registry integrity


def _entry(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "key": "spivak2008calculus",
        "doi": None,
        "url": "https://openlibrary.org/books/OL28292750M",
        "verified_by": "openlibrary",
        "isbn": ["9780914098911"],
        "type": "book",
        "title": "Calculus",
        "authors": [{"family": "Spivak", "given": "Michael"}],
        "year": 2008,
        "status": "verified",
        "origin": "manual",
        "used_by": ["M2"],
    }
    return base | overrides


def test_integrity_accepts_non_doi_entries_with_a_verification_source() -> None:
    from verify_refs import integrity

    primary = _entry(key="frb2011sr", url="https://www.federalreserve.gov/x", verified_by="issuer", type="primary")
    assert integrity([_entry(), primary | {"year": None, "isbn": []}]) == []


@pytest.mark.parametrize(
    ("overrides", "problem"),
    [
        ({"verified_by": "crossref"}, "verified by crossref but has no DOI"),
        ({"url": None}, "verified by openlibrary but has no URL"),
        ({"verified_by": "memory"}, "unknown verified_by"),
        ({"year": None}, "missing ['year']"),  # only primary documents may be undated
        ({"used_by": ["ZZ9"]}, "used_by unknown units"),
    ],
)
def test_integrity_rejects_entries_without_a_verifiable_source(overrides: dict[str, object], problem: str) -> None:
    from verify_refs import integrity

    assert any(problem in p for p in integrity([_entry(**overrides)]))


def test_seed_does_not_requeue_sources_admitted_by_hand() -> None:
    # A book admitted by ISBN must not reappear in the review queue on the next seeding run.
    from seed_references import Outcome, build

    cand = parse_source("Spivak, Calculus, 4th ed. (2008)")
    manual = _entry(source_strings=[cand.raw])
    entries, review, _ = build([Outcome(cand, ["M2"], None)], [manual])
    assert review == [] and entries == [manual]


def test_seeded_keys_avoid_keys_admitted_by_hand() -> None:
    # A re-seed must never mint a key that a manual entry (add_reference.py) already holds.
    w = work(doi="10.1/a", title="Backtesting", authors=("Harvey",), years=(2015,))
    entry = Entry("", w, "verified", "seed", [], [], {}, "now")
    assign_keys([entry], frozenset({"harvey2015backtesting"}))
    assert entry.key == "harvey2015backtestingb"
