"""Student error: decimal_text rounds ties to even (Python round) where the page states half up.

SIMULATED. The realised values below are illustrative numbers written into this file, not data. No random draws are
used. This file is the completed solution: the page shows the same program with the hit-rate line and the bias line
blanked, and the printed output of this file is the expected output of the instant check.

The case model and both definitions are those of rung 1 (lab 1 of this page). The case model forecasts
forecast(t) = 100 + 2 * t units for month index t (assumption M1; the forecast for month t uses no information from
month t, assumption M2). The six-month window is months 13 to 18, so H = 6 months.

A month is a hit when |e| <= 2 units, with error e = forecast - realised. The hit rate is hits / H. The bias is
(1 / H) times the sum of e, in units per month.

Part A: the forecast, realised value, error and hit of each month.
Part B: the number of hits and the hit rate, to four decimals.
Part C: the bias, in units per month, to four decimals.
Part D: the months with |error| = 2 exactly, which are hits at the edge of the band.

The hit rate and the bias are exact Fractions. A value is rounded once, when it is printed: half up (a tie goes away
from zero).
"""

from __future__ import annotations

import math
from fractions import Fraction

START_MONTH = 13
HIT_BAND = 2
REALISED = (127, 126, 124, 131, 136, 141)  # y_t for months 13 to 18, illustrative values


def forecast(t: int) -> int:
    """The case model's forecast for month index t, in units: 100 + 2 * t (assumption M1)."""
    return 100 + 2 * t


def is_hit(predicted: int, realised: int) -> bool:
    """True when the absolute error is at most the band of 2 units: |forecast - realised| <= 2."""
    if realised <= 0:
        raise ValueError(f"the realised value must be a positive count of units, got {realised}")
    return abs(predicted - realised) <= HIT_BAND


def decimal_text(value: Fraction, places: int) -> str:
    """The value rounded half up (a tie goes away from zero) to places decimals, with exactly places digits."""
    scale = 10**places
    magnitude = round(abs(value) * scale)
    sign = "-" if value < 0 and magnitude != 0 else ""
    whole, part = divmod(magnitude, scale)
    if places == 0:
        return f"{sign}{whole}"
    return f"{sign}{whole}.{part:0{places}d}"


def main() -> None:
    print("SIMULATED case model: forecast(t) = 100 + 2t units; six-month window, months 13 to 18, H = 6; band 2 units")
    print("Part A: month, forecast, realised, error (forecast - realised), hit")
    errors: list[int] = []
    hits = 0
    for offset, realised in enumerate(REALISED):
        t = START_MONTH + offset
        predicted = forecast(t)
        error = predicted - realised
        errors.append(error)
        hit = is_hit(predicted, realised)
        if hit:
            hits += 1
        print(f"  t={t} forecast={predicted} realised={realised} error={error:+d} hit={'yes' if hit else 'no'}")
    horizon = len(REALISED)
    hit_rate = Fraction(hits, horizon)
    print(f"Part B: hits {hits} of {horizon}; hit rate {decimal_text(hit_rate, 4)}")
    bias = Fraction(sum(errors), horizon)
    print(f"Part C: bias {decimal_text(bias, 4)} units per month")
    edge = [START_MONTH + i for i, e in enumerate(errors) if abs(e) == HIT_BAND]
    print(f"Part D: months with |error| = 2 exactly (hits at the edge): {edge}")


main()
