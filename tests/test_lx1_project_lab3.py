"""LX1 project lab 3 fails loud on the damaged snapshots that project.html says it fails on.

The page's Check paragraph states that a blank or non-decimal GBP cell raises ValueError, and that a month which does
not follow the previous one raises ValueError. The embedded snapshot has neither, so the lab's own run cannot show
either claim; these tests run the twin on copies of the snapshot with one damaged cell or one removed month, in a
scratch directory, as run_labs.py runs a twin.
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest

from coursekit import MARKET_DATA, ROOT

TWIN = ROOT / "tests" / "labs" / "LX1" / "lab-LX1-project-3.py"
SNAPSHOT = MARKET_DATA / "fx_monthly.csv"


def snapshot() -> tuple[list[str], list[list[str]]]:
    """The header and every row of the committed snapshot, cells as text."""
    with SNAPSHOT.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        return header, [row for row in reader]


def run_twin_on(
    tmp_path: Path, header: list[str], rows: list[list[str]], twin: Path = TWIN
) -> subprocess.CompletedProcess[str]:
    """Writes data/fx_monthly.csv under tmp_path and runs the twin there with -I -W error."""
    data = tmp_path / "data"
    data.mkdir()
    with (data / "fx_monthly.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)
    return subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin)],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
    )


def with_gbp_cell(header: list[str], rows: list[list[str]], month: str, value: str) -> list[list[str]]:
    """The rows with the GBP cell of one month replaced by value."""
    index = header.index("GBP")
    out = [list(row) for row in rows]
    for row in out:
        if row[0] == month:
            row[index] = value
    return out


def without_month(rows: list[list[str]], month: str) -> list[list[str]]:
    """The rows with one month removed."""
    return [row for row in rows if row[0] != month]


def test_the_twin_runs_on_the_untouched_snapshot(tmp_path: Path) -> None:
    header, rows = snapshot()
    done = run_twin_on(tmp_path, header, rows)
    assert done.returncode == 0, done.stderr
    assert "months in file: 669, 1971-01 to 2026-09" in done.stdout


@pytest.mark.parametrize("value", ["", "n/a"], ids=["blank", "non-decimal"])
def test_a_blank_or_non_decimal_gbp_cell_raises_value_error(tmp_path: Path, value: str) -> None:
    header, rows = snapshot()
    done = run_twin_on(tmp_path, header, with_gbp_cell(header, rows, "2000-06", value))
    assert done.returncode != 0, "a damaged cell must not produce a result"
    assert done.stdout == "", "the lab must stop before it prints anything"
    assert f"ValueError: 2000-06: GBP cell {value!r} is blank or not a decimal number" in done.stderr


def test_a_month_that_does_not_follow_the_previous_one_raises_value_error(tmp_path: Path) -> None:
    header, rows = snapshot()
    done = run_twin_on(tmp_path, header, without_month(rows, "1990-06"))
    assert done.returncode != 0, "a gap in the months must not produce a result"
    assert done.stdout == "", "the lab must stop before it prints anything"
    assert "ValueError: month 1990-07 does not follow 1990-05" in done.stderr


def test_a_population_sd_variant_of_the_two_pass_check_raises(tmp_path: Path) -> None:
    """Dividing by n instead of n - 1 moves the standard deviation far past the 1e-9 percent agreement tolerance."""
    source = TWIN.read_text(encoding="utf-8")
    needle = "math.fsum((value - mean) ** 2 for value in values) / (n - 1)"
    assert source.count(needle) == 1, "the two-pass denominator must appear exactly once in the twin"
    variant = tmp_path / "population_sd_twin.py"
    variant.write_text(
        source.replace(needle, "math.fsum((value - mean) ** 2 for value in values) / n"), encoding="utf-8"
    )
    header, rows = snapshot()
    done = run_twin_on(tmp_path, header, rows, twin=variant)
    assert done.returncode != 0, "a population-sd variant must not pass the agreement check"
    assert "ValueError: the two-pass and statistics.stdev standard deviations disagree" in done.stderr
