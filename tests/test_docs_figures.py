"""The computed figures that BLUEPRINT.md and README.md quote equal curriculum/curriculum.json (CLAUDE.md rule 5).

Hours, credential sizes and concept counts are computed by tools/render_curriculum.py. The documents copy them;
these tests fail when a curriculum change moves a figure and the copy was not refreshed.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
STATS: dict[str, Any] = json.loads((ROOT / "curriculum" / "curriculum.json").read_text(encoding="utf-8"))["stats"]
CREDENTIALS: dict[str, dict[str, Any]] = {c["id"]: c for c in STATS["credentials"]}
# BLUEPRINT §1.2: full-time years are hours at 45 hours a week for 48 weeks a year.
HOURS_PER_YEAR = 45 * 48


def text(doc: str) -> str:
    return (ROOT / doc).read_text(encoding="utf-8")


def row(doc: str, label: str) -> list[str]:
    """The cells of the one table row in ``doc`` whose first cell is ``label``."""
    rows = [line for line in text(doc).splitlines() if line.startswith("|")]
    cells = [[c.strip() for c in line.strip().strip("|").split("|")] for line in rows]
    found = [c for c in cells if c[0] == label]
    assert len(found) == 1, f"{doc}: expected one table row labelled {label!r}, found {len(found)}"
    return found[0]


def thousands(value: int) -> str:
    return f"{value:,}"


@pytest.mark.parametrize(
    ("label", "credential"),
    [
        ("**Finance Degree — Bachelor's Level**", "BS-FIN"),
        ("**Master's in Finance / Financial Engineering**", "MS-FIN"),
        ("**PhD in Finance**", "PHD-FIN"),
    ],
)
def test_blueprint_credential_table(label: str, credential: str) -> None:
    c = CREDENTIALS[credential]
    _, _, modules, projects, hours, credits, years = row("BLUEPRINT.md", label)
    assert (modules, projects, hours) == (str(c["modules"]), str(c["projects"]), thousands(c["hours"]))
    assert credits == f"≈{c['credit_equivalent']} credits"
    assert years == f"{c['full_time_years']:.2f}"


@pytest.mark.parametrize(
    ("label", "credential"),
    [
        ("Finance Degree, bachelor's level", "BS-FIN"),
        ("Master's in Finance / Financial Engineering", "MS-FIN"),
        ("PhD in Finance", "PHD-FIN"),
    ],
)
def test_readme_credential_table(label: str, credential: str) -> None:
    c = CREDENTIALS[credential]
    _, modules, projects, hours, years = row("README.md", label)
    assert (modules, projects, hours) == (str(c["modules"]), str(c["projects"]), thousands(c["hours"]))
    assert years == f"{c['full_time_years']:.2f}"


@pytest.mark.parametrize(
    ("label", "milestone"),
    [
        ("All F + U tiers (whole major incl. economics & computing)", "MAJOR"),
        ("+ all M tier (Master's-equivalent breadth)", "MASTERS"),
        ("+ all D tier, quals (Doctoral Candidate)", "CANDIDATE"),
        ("+ thesis (Doctoral)", "DOCTORAL"),
    ],
)
def test_blueprint_milestone_table(label: str, milestone: str) -> None:
    hours = STATS["milestone_hours"][milestone]
    _, shown, years = row("BLUEPRINT.md", label)
    assert shown == thousands(hours)
    assert years == f"{hours / HOURS_PER_YEAR:.2f}"


def test_the_doctoral_milestone_is_the_whole_program() -> None:
    assert STATS["milestone_hours"]["DOCTORAL"] == STATS["total_hours"]
    assert round(STATS["total_hours"] / HOURS_PER_YEAR, 2) == STATS["full_time_years"]


@pytest.mark.parametrize("doc", ["BLUEPRINT.md", "README.md"])
def test_concept_counts(doc: str) -> None:
    counts = re.findall(r"its\s+(\d[\d,]*)\s+concepts", text(doc)) + re.findall(r"(\d[\d,]*) concepts\b", text(doc))
    assert counts, f"{doc} quotes no concept count"
    assert set(counts) == {thousands(STATS["concepts"])}


def test_readme_module_count() -> None:
    assert re.findall(r"([\d,]+) modules, [\d,]+ concepts", text("README.md")) == [str(STATS["modules"])]
