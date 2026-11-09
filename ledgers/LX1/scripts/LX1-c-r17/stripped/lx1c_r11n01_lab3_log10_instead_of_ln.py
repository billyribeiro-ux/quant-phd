"""Student takes the base-10 logarithm where the page defines the natural log, so every change and the dispersion are scaled by 1 / ln(10). LX1 project lab 3 (rung 3 check)."""

from __future__ import annotations

import csv
import itertools
import math
import re
from collections.abc import Sequence
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction
from pathlib import Path

DATA_PATH = Path("data") / "fx_monthly.csv"
COLUMN = "GBP"
WINDOW_TWO_FROM = "2000-01"
WINDOW_THREE_FROM = "2025-10"
MONTH_PATTERN = re.compile(r"(\d{4})-(\d{2})")
DECIMAL_PATTERN = re.compile(r"\d+(\.\d+)?")


def month_index(month: str) -> int:
    """The month as a count of months from year 0, so that consecutive months differ by one."""
    found = MONTH_PATTERN.fullmatch(month)
    if found is None:
        raise ValueError(f"not a month written YYYY-MM: {month!r}")
    return int(found.group(1)) * 12 + int(found.group(2)) - 1


def load_column(path: Path, column: str) -> list[tuple[str, Fraction]]:
    """Every row of one column as an exact Fraction, in file order. Fails on a blank cell or a gap in the months."""
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or column not in reader.fieldnames:
            raise ValueError(f"column {column} is missing from {path}")
        rows: list[tuple[str, Fraction]] = []
        for row in reader:
            month = row["month"]
            cell = row.get(column) or ""
            if DECIMAL_PATTERN.fullmatch(cell) is None:
                raise ValueError(f"{month}: {column} cell {cell!r} is blank or not a decimal number")
            rows.append((month, Fraction(Decimal(cell))))
    for (previous, _), (current, _) in itertools.pairwise(rows):
        if month_index(current) != month_index(previous) + 1:
            raise ValueError(f"month {current} does not follow {previous}")
    return rows


def log_changes(rows: Sequence[tuple[str, Fraction]]) -> list[tuple[str, float]]:
    """The monthly log change ln(S_m / S_(m-1)), labelled by its month m, for every month after the first."""
    return [(month, math.log10(float(rate / previous))) for (_, previous), (month, rate) in itertools.pairwise(rows)]


def sample_sd_two_pass(values: Sequence[float]) -> float:
    """The sample standard deviation with denominator n - 1, from the mean and the squared deviations."""
    n = len(values)
    mean = math.fsum(values) / n
    return math.sqrt(math.fsum((value - mean) ** 2 for value in values) / (n - 1))


def show(value: float, places: int) -> str:
    """The float rounded half up (a tie away from zero) to the given number of decimal places."""
    return str(Decimal(value).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def window_report(window: Sequence[tuple[str, float]]) -> float:
    """Prints the figures of one window and returns its sample standard deviation, in unrounded form."""
    values = [change for _, change in window]
    sd = sample_sd_two_pass(values)
    zeros = sum(1 for value in values if value == 0.0)
    biggest_month, biggest = max(window, key=lambda item: abs(item[1]))
    print(f"  changes: {len(values)}")
    print(f"  exact zero changes: {zeros}")
    print(f"  sample sd, percent per month: {show(100 * sd, 2)}")
    print(f"  largest monthly log change by size, percent, with its sign: {show(100 * biggest, 2)} ({biggest_month})")
    return sd


def main() -> None:
    rows = load_column(DATA_PATH, COLUMN)
    print(f"{COLUMN} exchange rate, US dollars per pound, H.10 snapshot retrieved 2026-10-19")
    print(f"months in file: {len(rows)}, {rows[0][0]} to {rows[-1][0]}")
    changes = log_changes(rows)
    window_one = changes
    window_two = [item for item in changes if item[0] >= WINDOW_TWO_FROM]
    window_three = [item for item in changes if item[0] >= WINDOW_THREE_FROM]
    print(f"Window one, {window_one[0][0]} to {window_one[-1][0]}:")
    sd_one = window_report(window_one)
    print(f"Window two, {window_two[0][0]} to {window_two[-1][0]}:")
    sd_two = window_report(window_two)
    print(f"Window three, {window_three[0][0]} to {window_three[-1][0]}:")
    window_report(window_three)
    print(f"ratio of window two to window one sd, two decimals: {show(sd_two / sd_one, 2)}")
    difference = show(100 * (sd_one - sd_two), 2)
    print(f"difference of window one minus window two sd, percent per month, two decimals: {difference}")


main()
