"""Citation display in the generated site data (tools/build_site.py) and the year check in tools/verify_refs.py."""

from __future__ import annotations

import json
from typing import Any

import pytest

from build_site import REGISTRY, _fix_case, family_name, full_cite, plain_title, references_payload, short_cite
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


@pytest.mark.parametrize(
    ("title", "shown"),
    [
        pytest.param(
            "When is the Student $t$-statistic asymptotically standard normal?",
            "When is the Student t-statistic asymptotically standard normal?",
            id="tex-inline-math",
        ),
        pytest.param("A $p$-value and an $F$ test", "A p-value and an F test", id="two-spans"),
        pytest.param("Costs of $5 and more", "Costs of $5 and more", id="lone-dollar-kept"),
        pytest.param("From $5 to $10 a Share", "From $5 to $10 a Share", id="prices-kept"),
    ],
)
def test_tex_inline_math_in_a_title_is_shown_as_plain_text(title: str, shown: str) -> None:
    assert plain_title(title) == shown
    assert full_cite(full_entry(title=title)).split(" (2008). ", 1)[1].startswith(shown.rstrip("?"))


def test_no_displayed_reference_carries_tex_math_delimiters() -> None:
    payload = references_payload(json.loads(REGISTRY.read_text(encoding="utf-8"))["entries"])
    assert [key for key, shown in payload.items() if plain_title(shown["full"]) != shown["full"]] == []


@pytest.mark.parametrize(
    ("family", "source", "shown"),
    [
        pytest.param(
            "GORDON LAN",
            "Lan & DeMets (1983), 'Discrete Sequential Boundaries', Biometrika 70(3)",
            "Lan",
            id="given-name-filed-as-family",
        ),
        pytest.param(
            "POCOCK", "Pocock (1977), 'Group Sequential Methods', Biometrika 64(2)", "Pocock", id="whole-name-in-source"
        ),
        pytest.param(
            "GORDON LAN",
            "DeMets & Lan (1994), 'Interim Analysis', Statistics in Medicine 13",
            "Lan",
            id="not-first-author",
        ),
        pytest.param(
            "VAN DER LAAN", "van der Laan, Dudoit & Pollard (2004), SAGMB 3(1)", "van der Laan", id="particles-kept"
        ),
        pytest.param("GORDON LAN", "Planck (1900), 'Lanthanum', Annalen 4", "Gordon Lan", id="no-whole-word-match"),
        pytest.param(
            "GORDON LAN", "Smith (2001), 'On Lan's Test', Biometrika 88", "Gordon Lan", id="title-words-ignored"
        ),
    ],
)
def test_all_caps_family_names_take_the_citation_strings_surname(family: str, source: str, shown: str) -> None:
    assert family_name(family, [source]) == shown
