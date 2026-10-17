"""Citation display in the generated site data (tools/build_site.py) and the year check in tools/verify_refs.py."""

from __future__ import annotations

from typing import Any

import pytest

from build_site import _fix_case, short_cite
from refs.registry import cited_years, display_year
from verify_refs import integrity


def entry(year: int, print_year: int | None, years: list[int], source: str, **extra: Any) -> dict[str, Any]:
    return {
        "key": "x",
        "type": "journal-article",
        "year": year,
        "years": years,
        "print_year": print_year,
        "source_strings": [source],
        **extra,
    }


@pytest.mark.parametrize(
    ("record", "shown"),
    [
        pytest.param(entry(1995, 1995, [1995, 2018], "Benjamini & Hochberg (1995)"), 1995, id="re-hosted-later"),
        pytest.param(entry(2002, 2002, [2002, 2019], "Lo (2002), FAJ 58(4)"), 2002, id="re-hosted-later-2"),
        pytest.param(entry(2015, 2016, [2015, 2016], "Harvey, Liu & Zhu (2016)"), 2016, id="online-first-then-print"),
        pytest.param(entry(2021, None, [2021], "An online-only venue (2021)"), 2021, id="no-print-date"),
    ],
)
def test_the_displayed_year_is_the_print_year_else_the_issued_year(record: dict[str, Any], shown: int) -> None:
    assert display_year(record) == shown


def test_cited_years_reads_every_citation_string() -> None:
    record = entry(2015, 2016, [2015, 2016], "Harvey, Liu & Zhu (2016), RFS 29(1)")
    record["source_strings"].append("Harvey et al. (2016a)")
    assert cited_years(record) == {2016}


def full_entry(**overrides: Any) -> dict[str, Any]:
    record = entry(
        2008,
        2008,
        [2008, 2009],
        "Bollen & Pool (2008), 'Conditional Return Smoothing in the Hedge Fund Industry', JFQA 43(2)",
        doi="10.1/x",
        url=None,
        verified_by="crossref",
        title="Conditional Return Smoothing in the Hedge Fund Industry",
        authors=[{"family": "Bollen", "given": "Nicolas P.B."}, {"family": "Pool", "given": "Veronika K."}],
        status="verified",
        used_by=["S7"],
        container="Journal of Financial and Quantitative Analysis",
    )
    record.update(overrides)
    return record


def test_integrity_flags_a_citation_year_the_site_would_not_show() -> None:
    assert not [p for p in integrity([full_entry()]) if "the site shows" in p]
    wrong = full_entry(source_strings=["Bollen & Pool (2009), 'Conditional Return Smoothing', JFQA 43(2)"])
    assert [p for p in integrity([wrong]) if "citation strings name [2009] but the site shows 2008" in p]


def test_integrity_requires_a_recorded_print_year_on_crossref_entries() -> None:
    missing = full_entry()
    del missing["print_year"]
    assert [p for p in integrity([missing]) if "print_year not recorded" in p]


@pytest.mark.parametrize(
    ("word", "shown"),
    [
        ("HARVEY", "Harvey"),
        ("MCLEAN", "McLean"),
        ("COLLIN-DUFRESNE", "Collin-Dufresne"),
        ("P.B.", "P.B."),
        ("J.-P.", "J.-P."),
        ("NICOLAS", "Nicolas"),
        ("López", "López"),
        ("A", "A"),
    ],
)
def test_all_caps_names_are_recased_but_initials_are_kept(word: str, shown: str) -> None:
    assert _fix_case(word) == shown


def test_short_cite_uses_the_print_year() -> None:
    record = full_entry(print_year=2008, years=[2008, 2009])
    assert short_cite(record) == "Bollen & Pool (2008)"
