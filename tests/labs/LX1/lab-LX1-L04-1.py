"""LX1 L04 lab 1: exchange-rate dispersion of one embedded H.10 column, in two windows, against a parity model.

Data. The lab reads data/fx_monthly.csv, the exchange rates of the Board of Governors of the Federal Reserve
System, G.5/H.10 Foreign Exchange Rates (noon buying rates in New York), one per month. Each value is the column's
last value in its month, as the MANIFEST transform states (month-end, each column's last value in the month). The
snapshot was retrieved 2026-10-19 and holds 669 months, 1971-01 to 2026-09. The column read is GBP, in US dollars per
pound sterling. The MANIFEST transform inverts CAD, CHF, DKK, JPY, NOK and SEK only, so GBP is a direct quote. The
file holds exchange-rate columns only: it has no interest-rate column and no forward-rate column.

Conventions. A monthly log change at month m is ln(x_m / x_(m-1)), with x_m the rate of month m, the natural
logarithm, per month, and no annualization. A window's dispersion is the sample standard deviation of its monthly log
changes, with denominator n - 1. Window one holds every change in the file, dated 1971-02 to 2026-09 (668 changes).
Window two holds the changes dated 2000-01 to 2026-09; its first change uses the rate of 1999-12. The window two start
is the first month from which the other two embedded snapshots, fx_daily and ust_daily, have data (both start
2000-01-03 in the MANIFEST).

Every rate is an exact Fraction parsed from its text. A blank cell, a non-decimal cell, a month that does not follow
the previous one, or a missing column raises ValueError. No row is skipped or filled.

Rounding. Log changes are floats computed from exact ratios. Printed values are the exact binary value of each float,
rounded half away from zero (Decimal ROUND_HALF_UP) to the number of places stated on the line.

Part A is a SIMULATED model check, not data: a parity held at 2.0000 dollars per pound for 12 months gives zero
monthly log changes and zero dispersion, which is the model's claim in Proposition 2.2 of the lesson. Part B reads
the GBP column and counts its changes and its exactly zero changes. Part C prints the count, the dispersion and the
largest absolute change for each window, and checks the telescoping identity of Proposition 1.2 of the lesson: the
sum of a window's log changes equals the log of its last rate over the rate before the window. Part D prints the
difference and the ratio of the two windows' dispersions.
"""

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
MODEL_PARITY = Fraction(2)
MODEL_MONTHS = 12
SUM_TOLERANCE = 1e-12

MONTH_PATTERN = re.compile(r"(\d{4})-(\d{2})")
DECIMAL_PATTERN = re.compile(r"\d+(\.\d+)?")


def month_index(month: str) -> int:
    """Return a serial number for a 'YYYY-MM' label, so that consecutive months differ by one.

    Raises ValueError when the label is not a YYYY-MM month with a month number from 1 to 12.
    """
    match = MONTH_PATTERN.fullmatch(month)
    if match is None:
        raise ValueError(f"not a YYYY-MM month: {month!r}")
    year, number = int(match.group(1)), int(match.group(2))
    if not 1 <= number <= 12:
        raise ValueError(f"month number out of range: {month!r}")
    return 12 * year + (number - 1)


def month_label(index: int) -> str:
    """Return the 'YYYY-MM' label of a serial number from month_index."""
    year, offset = divmod(index, 12)
    return f"{year:04d}-{offset + 1:02d}"


def parse_rate(text: str, month: str) -> Fraction:
    """Parse one published rate, a decimal written without sign or exponent, as an exact positive Fraction.

    Raises ValueError for a blank cell, any other text, or a zero rate. The lab never fills a cell.
    """
    if not DECIMAL_PATTERN.fullmatch(text):
        raise ValueError(f"{month}: {COLUMN} cell is {text!r}, not a decimal rate")
    rate = Fraction(text)
    if rate <= 0:
        raise ValueError(f"{month}: {COLUMN} rate must be positive")
    return rate


def load_column(path: Path, column: str) -> list[tuple[str, Fraction]]:
    """Read one column of the snapshot as (month, rate) pairs in file order.

    Raises ValueError when the header lacks the column, when a month label is not YYYY-MM, when two months are not
    consecutive, or when a cell is not a decimal rate.
    """
    rows: list[tuple[str, Fraction]] = []
    previous: int | None = None
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or column not in reader.fieldnames:
            raise ValueError(f"{path.name} has no column {column!r}")
        for record in reader:
            month = str(record["month"])
            index = month_index(month)
            if previous is not None and index != previous + 1:
                raise ValueError(f"{month} does not follow the previous month in {path.name}")
            previous = index
            rows.append((month, parse_rate(str(record[column]), month)))
    return rows


def log_changes(rows: Sequence[tuple[str, Fraction]]) -> list[tuple[str, float]]:
    """Return (month, ln(x_m / x_(m-1))) for every month after the first, in file order.

    The ratio is an exact Fraction; only the logarithm is a float. Each change is dated by the later month.
    """
    return [(month, math.log(float(rate / previous))) for (_, previous), (month, rate) in itertools.pairwise(rows)]


def sample_sd(values: Sequence[float]) -> float:
    """Sample standard deviation with denominator n - 1, in the units of the values.

    Raises ValueError with fewer than two values, because the n - 1 denominator is then zero.
    """
    n = len(values)
    if n < 2:
        raise ValueError("a sample standard deviation needs at least two values")
    mean = math.fsum(values) / n
    return math.sqrt(math.fsum((v - mean) ** 2 for v in values) / (n - 1))


def show(value: float, places: int) -> str:
    """Show a float with a fixed number of decimal places, rounded half away from zero, for display only."""
    return str(Decimal(value).quantize(Decimal(f"1e-{places}"), rounding=ROUND_HALF_UP))


def largest_move(changes: Sequence[tuple[str, float]]) -> tuple[str, float]:
    """Return the change with the largest absolute value; on a tie, the earliest month."""
    return max(changes, key=lambda item: abs(item[1]))


def main() -> None:
    """Print Parts A to D in a fixed order."""
    # Part A: a SIMULATED model check, not data.
    model_rows = [(month_label(month_index("2000-01") + i), MODEL_PARITY) for i in range(MODEL_MONTHS)]
    model = log_changes(model_rows)
    model_values = [c for _, c in model]
    print(f"Part A: SIMULATED model check, not data: a parity held at {show(float(MODEL_PARITY), 4)} dollars per pound")
    print(f"model monthly log changes: {len(model)}; all exactly zero: {all(c == 0.0 for c in model_values)}")
    print(f"model sample standard deviation: {show(sample_sd(model_values), 6)}")

    # Part B: the embedded column.
    rows = load_column(DATA_PATH, COLUMN)
    changes = log_changes(rows)
    zero = [month for (_, previous), (month, rate) in itertools.pairwise(rows) if rate == previous]
    print(f"Part B: {DATA_PATH.name}, column {COLUMN} (USD per pound sterling), exchange rates")
    print(f"months read: {len(rows)}, from {rows[0][0]} to {rows[-1][0]}; cells read as decimal rates: {len(rows)}")
    print(f"monthly log changes: {len(changes)}, dated {changes[0][0]} to {changes[-1][0]}")
    print(f"months with an exactly zero change: {len(zero)}: {', '.join(zero)}")

    # Part C: the two windows.
    before_window_two = month_label(month_index(WINDOW_TWO_FROM) - 1)
    rate_before_two = dict(rows)[before_window_two]
    name_one = "window one (1971-02 to 2026-09)"
    name_two = f"window two ({WINDOW_TWO_FROM} to 2026-09)"
    windows = {
        name_one: (changes, rows[0][1]),
        name_two: ([item for item in changes if item[0] >= WINDOW_TWO_FROM], rate_before_two),
    }
    print("Part C: dispersion of monthly log changes, sample standard deviation with n - 1")
    sds: dict[str, float] = {}
    for name, (window, start_rate) in windows.items():
        values = [c for _, c in window]
        sd = sample_sd(values)
        sds[name] = sd
        biggest_month, biggest = largest_move(window)
        print(f"{name}: changes {len(values)}; standard deviation {show(sd, 6)}")
        print(f"  largest absolute change {show(abs(biggest), 6)} at {biggest_month} (signed {show(biggest, 6)})")
        last_rate = rows[-1][1]
        identity = abs(math.fsum(values) - math.log(float(last_rate / start_rate))) <= SUM_TOLERANCE
        print(f"  sum of the changes equals ln(last rate / rate before the window) within 1e-12: {identity}")

    # Part D: the difference between the windows.
    one, two = sds[name_one], sds[name_two]
    print("Part D: window two minus window one")
    print(f"difference in standard deviation: {show(two - one, 6)}")
    print(f"ratio of window two to window one standard deviation, four decimals: {show(two / one, 4)}")


main()
