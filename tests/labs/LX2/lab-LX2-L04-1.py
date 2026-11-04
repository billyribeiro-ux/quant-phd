"""LX2 L04 lab 1: outcomes analysis of a SIMULATED forecast path, with both measures in exact arithmetic.

SIMULATED. The path of Parts A and B is drawn from the generator below with a fixed seed. Part D enumerates the
generator's distribution, and the path of Part C is hand-built, with fixed values. No value is observed data, and no
value describes a real firm, a real planning figure or a real model.

Standard library only. Seed 20261103, with random.Random(seed) and no other source of randomness. No network.

The generator: for each period t = 1, ..., H with H = 24, the realised value is y_t = 100 + U_t, where U_t is
uniform on the integers -6 to 6. The forecast is yhat_t = 101 + V_t, where V_t is uniform on the integers -4 to 4.
The draws are made in the order U_1, V_1, U_2, V_2, ... All values are integers in index units.

The two measures, defined before any number is computed:
* forecast error e_t = yhat_t - y_t, in index units;
* hit indicator h_t = 1 if |e_t| <= 2 (a hit within an inclusive band of 2 index units), and h_t = 0 otherwise;
* hit rate = (sum over t of h_t) / H, a share of periods;
* bias = (1/H) * sum over t of e_t, in index units; a positive bias means the forecasts sit above the realised
  values on average.

Rounding rule: both measures are computed as exact Fractions. A value is shown rounded to four decimal places,
with ties rounded away from zero, which is floor(|x| * 10^4 + 1/2) / 10^4 with the sign of x. The exact Fraction is
printed next to every rounded value, in lowest terms.

Part A: the two measures over the full 24-period path, with the path printed period by period.
Part B: the same two measures over the first 12 and the last 12 periods, to show that the window is part of the
definition.
Part C: a hand-built path with errors +3, -3, +3, -3, to show that a bias of zero does not mean small errors.
Part D: exact expectations under the generator, by enumerating all 9 x 13 pairs (V, U), with V the forecast draw
and U the realised draw, printed as Fractions.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction

SEED = 20261103
HORIZON = 24
BAND = 2
PLACES = 4
SCALE = 10**PLACES
REALISED_CENTRE = 100
FORECAST_CENTRE = 101
REALISED_SPREAD = 6
FORECAST_SPREAD = 4


@dataclass(frozen=True)
class Period:
    """One period of a path: t is the period index from 1, both values are integers in index units."""

    t: int
    forecast: int
    realised: int


def simulate(seed: int, horizon: int) -> list[Period]:
    """SIMULATED path of horizon periods from random.Random(seed), in the draw order stated in the module docstring."""
    rng = random.Random(seed)
    path: list[Period] = []
    for t in range(1, horizon + 1):
        realised = REALISED_CENTRE + rng.randint(-REALISED_SPREAD, REALISED_SPREAD)
        forecast = FORECAST_CENTRE + rng.randint(-FORECAST_SPREAD, FORECAST_SPREAD)
        path.append(Period(t, forecast, realised))
    return path


def error(p: Period) -> int:
    """Forecast error yhat_t - y_t in index units. Positive when the forecast is above the realised value."""
    return p.forecast - p.realised


def is_hit(p: Period, band: int = BAND) -> bool:
    """True when |yhat_t - y_t| <= band, with band in index units. The inequality is inclusive."""
    return abs(error(p)) <= band


def hit_rate(periods: Sequence[Period]) -> Fraction:
    """Share of the periods in the window that are hits. The denominator is the number of periods in the window."""
    return Fraction(sum(is_hit(p) for p in periods), len(periods))


def bias(periods: Sequence[Period]) -> Fraction:
    """Mean forecast error over the window, in index units. The denominator is the number of periods in the window."""
    return Fraction(sum(error(p) for p in periods), len(periods))


def round_half_away(x: Fraction) -> str:
    """Round x to PLACES decimal places, ties away from zero, and return the decimal string. Exact: no float is used."""
    sign = "-" if x < 0 else ""
    scaled = abs(x) * SCALE
    units = math.floor(scaled + Fraction(1, 2))
    return f"{sign}{units // SCALE}.{units % SCALE:0{PLACES}d}"


def show(x: Fraction) -> str:
    """The exact Fraction in lowest terms, then the rounded decimal in parentheses."""
    return f"{x} (rounded {round_half_away(x)})"


def part_a(path: Sequence[Period]) -> None:
    """Print the path period by period, then both measures over the whole path."""
    print("Part A: outcomes analysis over the full path")
    print(f"generator seed {SEED}, horizon H = {len(path)}, band = {BAND} index units (inclusive)")
    print("t  forecast  realised  error  hit")
    for p in path:
        print(f"{p.t:>2} {p.forecast:>9} {p.realised:>9} {error(p):>6} {int(is_hit(p)):>4}")
    print(f"hits = {sum(is_hit(p) for p in path)} of {len(path)}")
    print(f"hit rate = {show(hit_rate(path))}")
    print(f"bias = {show(bias(path))}")
    total = sum(error(p) for p in path)
    print(f"sum of errors = {total}; sum / H = {Fraction(total, len(path))}")
    mae = Fraction(sum(abs(error(p)) for p in path), len(path))
    print(f"mean absolute error = {mae} (not one of the two measures)")


def part_b(path: Sequence[Period]) -> None:
    """Print both measures for the first 12 and the last 12 periods, each over its own denominator of 12."""
    print("Part B: the same measures over two windows of 12 periods")
    half = len(path) // 2
    for label, window in (("first 12", path[:half]), ("last 12", path[half:])):
        print(f"{label}: periods {window[0].t} to {window[-1].t}, n = {len(window)}")
        print(f"  hit rate = {show(hit_rate(window))}")
        print(f"  bias = {show(bias(window))}")


def part_c() -> None:
    """A hand-built path with errors +3, -3, +3, -3 against realised values of 100."""
    print("Part C: a bias of zero beside large errors")
    errors = (3, -3, 3, -3)
    path = [Period(t, REALISED_CENTRE + e, REALISED_CENTRE) for t, e in enumerate(errors, start=1)]
    print("errors " + " ".join(f"{e:+d}" for e in errors) + f"; band = {BAND}")
    print(f"hits = {sum(is_hit(p) for p in path)} of {len(path)}")
    print(f"hit rate = {show(hit_rate(path))}")
    print(f"bias = {show(bias(path))}")


def part_d() -> None:
    """Exact expectations under the generator, by enumerating all 9 x 13 equally likely pairs (V, U).

    V is the forecast draw, over the 9 values -4 to 4, and U is the realised draw, over the 13 values -6 to 6.
    """
    print("Part D: exact expectations under the generator, by enumeration")
    pairs = [
        (FORECAST_CENTRE + v - (REALISED_CENTRE + u))
        for v in range(-FORECAST_SPREAD, FORECAST_SPREAD + 1)
        for u in range(-REALISED_SPREAD, REALISED_SPREAD + 1)
    ]
    count = len(pairs)
    hits = sum(1 for e in pairs if abs(e) <= BAND)
    print(f"pairs = {count} (9 forecast draws times 13 realised draws, each pair with probability 1/{count})")
    print(f"P(hit) = {show(Fraction(hits, count))}")
    expected_error = Fraction(sum(pairs), count)
    print(f"E[error] = {expected_error} index units")


def main() -> None:
    """Run Parts A to D. Every printed number is an exact Fraction, an integer count or a rounded exact value."""
    path = simulate(SEED, HORIZON)
    part_a(path)
    part_b(path)
    part_c()
    part_d()


main()
