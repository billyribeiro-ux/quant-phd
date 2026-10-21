"""Offline tests for the reference tooling.

Every test that encodes a failure mode found while seeding the real registry
names it, so the regression stays explained.
"""

from __future__ import annotations

from pathlib import Path

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
        # Leading whitespace before a range is not part of the issue: " 2-3" is Crossref's "02-03".
        (" 2-3", "02-03", True),
        ("02-03", " 2/3", True),
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


def test_a_unit_live_run_re_fetches_only_the_entries_the_unit_uses() -> None:
    from verify_refs import live_scope

    s7, both, other = _entry(key="a", used_by=["S7"]), _entry(key="b", used_by=["M2", "S7"]), _entry(key="c")
    assert live_scope([s7, both, other], "S7") == [s7, both]
    assert live_scope([s7, both, other], None) == [s7, both, other]


@pytest.mark.parametrize(
    "argv",
    [["--unit", "ZZ9"], ["--unit", "S7", "--offline"], ["--unit", "S7", "--backfill-print-years"]],
    ids=["unknown-unit", "offline", "backfill"],
)
def test_a_unit_live_run_refuses_an_unknown_unit_and_other_modes(
    argv: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    import verify_refs

    monkeypatch.setattr("sys.argv", ["verify_refs.py", *argv])
    with pytest.raises(SystemExit) as stop:
        verify_refs.main()
    assert stop.value.code == 2


def test_a_unit_live_run_re_fetches_its_entries_but_checks_the_whole_registry(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    import verify_refs
    from refs import registry

    scoped = _entry(key="scoped", used_by=["S7"], url="https://openlibrary.org/books/OL1M", isbn=["9780000000011"])
    other = _entry(key="other", url="https://openlibrary.org/books/OL2M", isbn=["9780000000022"])
    broken = _entry(key="broken", used_by=["ZZ9"], url="https://openlibrary.org/books/OL3M", isbn=["9780000000033"])
    fetched: list[object] = []

    def live_check(entry: dict[str, object], crossref: object, fetcher: object) -> list[str]:
        fetched.append(entry["key"])
        return []

    monkeypatch.setattr(registry, "load", lambda: [scoped, other, broken])
    monkeypatch.setattr(verify_refs, "live_check", live_check)
    monkeypatch.setattr("sys.argv", ["verify_refs.py", "--unit", "S7"])
    assert verify_refs.main() == 1  # an integrity problem outside the unit still fails the run
    assert fetched == ["scoped"]
    out = capsys.readouterr().out.splitlines()
    assert "FAIL broken: used_by unknown units ['ZZ9']" in out
    assert out[-1] == "live re-verification of S7: 1 of 3 entries, 1 problems"


@pytest.mark.parametrize(
    ("argv", "held_units", "expected", "writes"),
    [
        (["--doi", "10.1/held", "--dry-run"], ["M2", "S7"], "WOULD UPDATE held1995title used_by=['M2', 'S7']", 0),
        (["--doi", "10.1/held"], ["M2", "S7"], "UPDATED held1995title used_by=['M2', 'S7']", 1),
        (["--doi", "10.1/held", "--dry-run"], ["M2"], "WOULD UPDATE held1995title used_by=['M2', 'S7']", 0),
        (["--doi", "10.1/held"], ["M2"], "UPDATED held1995title used_by=['M2', 'S7']", 1),
        (
            ["--doi", "10.1/new", "--dry-run"],
            ["M2", "S7"],
            "WOULD ADD (crossref): Smith (1995) 'A Title', Journal of Finance 50(1) url=None isbn=[] notes={}",
            0,
        ),
    ],
    ids=["dry-run-unit-held", "run-unit-held", "dry-run-unit-added", "run-unit-added", "dry-run-new"],
)
def test_a_dry_run_reports_what_the_run_would_do(
    argv: list[str],
    held_units: list[str],
    expected: str,
    writes: int,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # A dry run for a DOI the registry already holds said WOULD ADD, though the run itself updates that entry.
    # used_by is the union of the held units and S7: S7 neither repeated when held nor dropped when new.
    import copy

    import add_reference
    from refs import registry

    held = _entry(key="held1995title", doi="10.1/held", url=None, isbn=[], verified_by="crossref", used_by=held_units)
    stored = dict(held, source_strings=[])
    saved: list[list[dict[str, object]]] = []
    monkeypatch.setattr(add_reference, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(add_reference, "by_doi", lambda cand, doi: (work(doi=doi), {}, ""))
    monkeypatch.setattr(registry, "load", lambda: [stored])
    monkeypatch.setattr(
        registry, "save", lambda entries: saved.append(copy.deepcopy(entries))
    )  # as saved, not as later
    source = "Smith (1995), Journal of Finance 50(1)"
    monkeypatch.setattr("sys.argv", ["add_reference.py", *argv, "--source", source, "--used-by", "S7"])
    assert add_reference.main() == 0
    assert capsys.readouterr().out == expected + "\n"  # one line: a dry run never reports both outcomes
    assert len(saved) == writes
    if writes:
        (entry,) = saved[0]
        assert entry["source_strings"] == [source] and entry["used_by"] == ["M2", "S7"]


_HOLDERS = (
    _entry(key="by_doi", doi="10.1/a", url="https://example.org/a", isbn=[]),
    _entry(key="by_isbn", doi=None, isbn=["9780000000011", "9780000000022"], url="https://openlibrary.org/books/OL1M"),
    _entry(key="by_url", doi=None, isbn=[], url="https://example.org/u"),
    _entry(key="by_doi_only", doi="10.1/d", isbn=[], url=None),  # no URL: a work without one must not match it
)


@pytest.mark.parametrize(
    ("doi", "isbn", "url", "holder"),
    [
        ("10.1/a", (), None, "by_doi"),
        ("10.1/z", (), "https://example.org/u", None),  # a DOI decides: a URL alone does not make it the same work
        ("", ("9780000000022", "9780000000033"), None, "by_isbn"),  # one shared ISBN is enough
        ("", (), "https://example.org/u", "by_url"),
        ("", (), "https://example.org/other", None),
        ("", (), None, None),  # no identifier matches nothing
        ("", ("9780000000033", "9780000000022"), None, "by_isbn"),  # the shared ISBN need not come first
        ("", ("9780000000099",), "https://example.org/u", "by_url"),  # an ISBN that matches nothing leaves the URL
    ],
    ids=["doi", "doi-beats-url", "shared-isbn", "url", "other-url", "no-identifier", "isbn-second", "isbn-miss-url"],
)
def test_registered_finds_the_entry_that_holds_the_work(
    doi: str, isbn: tuple[str, ...], url: str | None, holder: str | None
) -> None:
    from dataclasses import replace

    from add_reference import registered

    entries = [dict(e) for e in _HOLDERS]
    found = registered(entries, replace(work(doi=doi), isbn=isbn, url=url))
    assert (found["key"] if found else None) == holder
    if found is not None:
        assert any(found is e for e in entries)  # the stored entry itself, which the run updates and saves


def _admit_with(
    held: list[dict[str, object]], argv: list[str], monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> tuple[int, list[list[dict[str, object]]]]:
    import copy

    import add_reference
    from refs import registry

    saved: list[list[dict[str, object]]] = []
    monkeypatch.setattr(add_reference, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(add_reference, "by_doi", lambda cand, doi: (work(doi=doi), {}, ""))
    monkeypatch.setattr(registry, "load", lambda: held)
    monkeypatch.setattr(registry, "save", lambda entries: saved.append(copy.deepcopy(entries)))
    monkeypatch.setattr("sys.argv", ["add_reference.py", *argv])
    return add_reference.main(), saved


_SOURCE = ["--source", "Smith (1995), Journal of Finance 50(1)"]


def test_admit_adds_a_new_work_with_its_unit_source_and_status(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    code, saved = _admit_with([], ["--doi", "10.1/new", *_SOURCE, "--used-by", "S7"], monkeypatch, tmp_path)
    assert code == 0 and capsys.readouterr().out == "ADDED smith1995title -> 10.1/new\n"
    ((entry,),) = saved
    assert entry["key"] == "smith1995title" and entry["doi"] == "10.1/new"
    assert entry["used_by"] == ["S7"] and entry["source_strings"] == [_SOURCE[1]]
    assert (entry["status"], entry["origin"], entry["verified_by"]) == ("verified", "manual", "crossref")


def test_admit_does_not_reuse_a_key_the_registry_holds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    other = _entry(key="smith1995title", doi="10.1/other", url=None, isbn=[], source_strings=[])
    code, saved = _admit_with([other], ["--doi", "10.1/new", *_SOURCE, "--used-by", "S7"], monkeypatch, tmp_path)
    assert code == 0 and capsys.readouterr().out == "ADDED smith1995titleb -> 10.1/new\n"
    assert [e["key"] for e in saved[0]] == ["smith1995title", "smith1995titleb"]


def test_admitting_a_reference_needs_a_unit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    code, saved = _admit_with([], ["--doi", "10.1/new", *_SOURCE], monkeypatch, tmp_path)
    assert code == 1 and saved == []
    assert "--used-by is required" in capsys.readouterr().err


def test_describe_names_the_first_author() -> None:
    from add_reference import describe

    assert describe(work(authors=("Smith", "Jones"))).startswith("Smith (1995) ")


def test_describe_names_the_first_container_title_only() -> None:
    from dataclasses import replace

    from add_reference import describe

    two = replace(work(), container=("Journal of Finance", "J. Fin."))
    assert describe(two) == "Smith (1995) 'A Title', Journal of Finance 50(1)"


def test_describe_handles_a_work_without_a_container() -> None:
    # A book admitted by ISBN has no container title.
    from dataclasses import replace

    from add_reference import describe

    assert describe(replace(work(), container=())).startswith("Smith (1995) 'A Title',")


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


# ---------------------------------------------------------------- add_reference: every mode and every stored field


def test_admit_stores_the_identity_and_the_notes_of_a_new_book(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # A book admitted by ISBN keeps its ISBN, URL, author, title, year and the notes recorded at admission.
    import copy
    from dataclasses import replace

    import add_reference
    from refs import registry

    book = replace(
        work(),
        doi="",
        type="book",
        title="Calculus",
        authors=(Author(family="Spivak", given="Michael"),),
        container=(),
        volume=None,
        issue=None,
        isbn=("9780914098911",),
        url="https://openlibrary.org/books/OL28292750M",
        years=frozenset({2008}),
        year=2008,
    )
    notes = {"year": {"curriculum": "2008", "openlibrary": "2008"}}
    saved: list[list[dict[str, object]]] = []
    monkeypatch.setattr(registry, "load", lambda: [])
    monkeypatch.setattr(registry, "save", lambda entries: saved.append(copy.deepcopy(entries)))
    source = "Spivak, Calculus, 4th ed. (2008)"
    assert add_reference.admit(book, source=source, used_by=["M2"], verified_by="openlibrary", notes=notes) == 0
    assert capsys.readouterr().out == "ADDED spivak2008calculus -> https://openlibrary.org/books/OL28292750M\n"
    ((entry,),) = saved
    assert entry["isbn"] == ["9780914098911"] and entry["url"] == "https://openlibrary.org/books/OL28292750M"
    assert entry["title"] == "Calculus" and entry["authors"] == [{"family": "Spivak", "given": "Michael"}]
    assert entry["year"] == 2008 and entry["notes"] == notes and entry["verified_by"] == "openlibrary"


def test_admit_keys_an_issuer_document_from_the_issuer_short_name(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # The key of a primary document starts from the issuer's short name (authorities.yaml), not the record's author.
    import add_reference
    from refs import registry

    monkeypatch.setattr(registry, "load", lambda: [])
    monkeypatch.setattr(registry, "save", lambda entries: None)
    code = add_reference.admit(
        work(),
        source="Smith (1995), Journal of Finance 50(1)",
        used_by=["S7"],
        verified_by="issuer",
        notes={},
        short="frb",
    )
    assert code == 0 and capsys.readouterr().out == "ADDED frb1995title -> 10.1/x\n"


def test_by_isbn_refuses_a_citation_of_another_edition(monkeypatch: pytest.MonkeyPatch) -> None:
    # A 2nd-edition citation is not admitted against the record of the 3rd edition.
    import add_reference
    from refs.parse import parse_source
    from refs.web import Fetcher

    class Record:
        def __init__(self, fetcher: Fetcher) -> None:
            self.fetcher = fetcher

        def edition_record(self, isbn: str, *, use_cache: bool = True) -> tuple[Work, str | None]:
            return work(), "3 edition"

    monkeypatch.setattr(add_reference, "OpenLibrary", Record)
    found, _, reason = add_reference.by_isbn(
        parse_source("Spivak, Calculus, 2nd ed. (2008)"), "9780914098911", Fetcher(None)
    )
    assert found is None and reason == "edition mismatch: citation says 2, the record says '3 edition'"


def test_by_landing_refuses_a_page_that_declares_a_doi(monkeypatch: pytest.MonkeyPatch) -> None:
    # A page that declares a DOI is admitted with --doi, so that Crossref verifies it, never through --url.
    from add_reference import by_landing
    from refs.parse import parse_source
    from refs.web import Fetcher

    fetcher = Fetcher(None)
    page = '<meta name="citation_doi" content="10.1111/j.1540-6261.1964.tb02865.x">'
    monkeypatch.setattr(fetcher, "get", lambda url, **kwargs: (url, page))
    url = "https://www.jmlr.org/papers/v12/pedregosa11a.html"
    found, _, reason = by_landing(
        parse_source("Pedregosa et al. (2011), Journal of Machine Learning Research 12"), url, fetcher
    )
    assert found is None and reason.startswith("the page declares DOI 10.1111/j.1540-6261.1964.tb02865.x")


def test_by_landing_refuses_a_site_that_is_not_a_publisher(monkeypatch: pytest.MonkeyPatch) -> None:
    from add_reference import by_landing
    from refs.parse import parse_source
    from refs.web import Fetcher

    fetcher = Fetcher(None)
    monkeypatch.setattr(fetcher, "get", lambda url, **kwargs: pytest.fail("fetched a site that is not a publisher"))
    found, _, reason = by_landing(
        parse_source("Smith (1995), Journal of Finance 50(1)"), "https://example.org/a", fetcher
    )
    assert (
        found is None and reason == "https://example.org/a is not on a publishers domain in references/authorities.yaml"
    )


def test_by_doi_resolves_only_articles_and_books() -> None:
    from add_reference import by_doi
    from refs.parse import parse_source

    found, _, reason = by_doi(parse_source("Dirks v. SEC, 463 U.S. 646 (1983)"), "10.1/x")
    assert found is None and reason == "source parses as 'primary'; only articles and books resolve by DOI"


def test_a_primary_document_is_admitted_only_from_its_issuer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    import add_reference
    from refs import registry

    monkeypatch.setattr(registry, "load", lambda: [])  # a refusal must never reach the real registry
    monkeypatch.setattr(registry, "save", lambda entries: pytest.fail("a refused document was saved"))

    monkeypatch.setattr(add_reference, "CACHE_DIR", tmp_path)
    source = "Federal Reserve SR 11-7, Guidance on Model Risk Management (2011) (primary)"
    monkeypatch.setattr(
        "sys.argv",
        ["add_reference.py", "--url", "https://example.org/sr1107.htm", "--source", source, "--used-by", "S7"],
    )
    assert add_reference.main() == 1
    assert "is not on an issuers domain" in capsys.readouterr().err


def test_a_primary_document_must_carry_its_own_title(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    import add_reference
    from refs import registry

    monkeypatch.setattr(registry, "load", lambda: [])  # a refusal must never reach the real registry
    monkeypatch.setattr(registry, "save", lambda entries: pytest.fail("a refused document was saved"))

    monkeypatch.setattr(add_reference, "CACHE_DIR", tmp_path)
    from refs.web import Fetcher

    monkeypatch.setattr(Fetcher, "get", lambda self, page, **kwargs: (page, "<title>Monetary Policy Report</title>"))
    source = "Federal Reserve SR 11-7, Guidance on Model Risk Management (2011) (primary)"
    url = "https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm"
    monkeypatch.setattr("sys.argv", ["add_reference.py", "--url", url, "--source", source, "--used-by", "S7"])
    assert add_reference.main() == 1
    assert "the page's title covers" in capsys.readouterr().err


def _admitted_by_mode(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, argv: list[str], patch: dict[str, object]
) -> dict[str, object]:
    import copy

    import add_reference
    from refs import registry

    saved: list[list[dict[str, object]]] = []
    monkeypatch.setattr(add_reference, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(registry, "load", lambda: [])
    monkeypatch.setattr(registry, "save", lambda entries: saved.append(copy.deepcopy(entries)))
    for name, value in patch.items():
        monkeypatch.setattr(add_reference, name, value)
    monkeypatch.setattr("sys.argv", ["add_reference.py", *argv])
    assert add_reference.main() == 0
    ((entry,),) = saved
    return entry


def test_an_isbn_admission_is_verified_by_open_library(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from dataclasses import replace

    book = replace(
        work(),
        doi="",
        type="book",
        container=(),
        volume=None,
        issue=None,
        isbn=("9780914098911",),
        url="https://openlibrary.org/books/OL28292750M",
    )
    entry = _admitted_by_mode(
        monkeypatch,
        tmp_path,
        ["--isbn", "9780914098911", *_SOURCE, "--used-by", "M2"],
        {"by_isbn": lambda cand, isbn, fetcher: (book, {}, "")},
    )
    assert entry["verified_by"] == "openlibrary"


def test_a_landing_page_admission_is_verified_by_its_landing_page(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from dataclasses import replace

    url = "https://www.jmlr.org/papers/v12/pedregosa11a.html"
    article = replace(work(), url=url)
    entry = _admitted_by_mode(
        monkeypatch,
        tmp_path,
        ["--url", url, *_SOURCE, "--used-by", "S7"],
        {"by_landing": lambda cand, page, fetcher: (article, {}, "")},
    )
    assert entry["verified_by"] == "landing"


def test_a_primary_document_admission_is_verified_by_its_issuer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    url = "https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm"
    source = "Federal Reserve SR 11-7, Guidance on Model Risk Management (2011) (primary)"
    entry = _issuer_admitted(monkeypatch, tmp_path, url, source)
    assert entry["verified_by"] == "issuer"


def _issuer_admitted(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, url: str, source: str) -> dict[str, object]:
    import copy

    import add_reference
    from refs import registry

    saved: list[list[dict[str, object]]] = []
    monkeypatch.setattr(add_reference, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(registry, "load", lambda: [])
    monkeypatch.setattr(registry, "save", lambda entries: saved.append(copy.deepcopy(entries)))
    from refs.web import Fetcher

    monkeypatch.setattr(
        Fetcher,
        "get",
        lambda self, page, **kwargs: (
            page,
            "<title>Federal Reserve SR 11-7, Guidance on Model Risk Management</title>",
        ),
    )
    monkeypatch.setattr("sys.argv", ["add_reference.py", "--url", url, "--source", source, "--used-by", "S7"])
    assert add_reference.main() == 0
    ((entry,),) = saved
    return entry


def test_judged_refuses_a_citation_whose_string_differs_from_the_record() -> None:
    from dataclasses import replace

    from add_reference import judged
    from refs.parse import parse_source

    record = replace(work(), authors=(Author(family="Smith", given=""), Author(family="Jones", given="")))
    found, _, reason = judged(parse_source("Smith (1995), Journal of Finance 50(1)"), record)
    assert found is None and reason.startswith("citation string differs from the record: {'authors'")


def test_judged_says_why_a_record_does_not_match() -> None:
    from add_reference import judged
    from refs.parse import parse_source

    found, _, reason = judged(parse_source("Smith (1995), Journal of Finance 50(2)"), work())
    assert found is None and reason.startswith("record does not match the citation (")
    assert reason.endswith("record: Smith (1995) 'A Title', Journal of Finance 50(1)")
