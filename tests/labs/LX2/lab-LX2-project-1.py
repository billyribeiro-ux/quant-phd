"""LX2 project lab 1 (rung 1, worked example): the outcomes analysis of a SIMULATED forecasting model.

SIMULATED. The realised values below are illustrative numbers written into this file. They are not data. No random
draws are used, so every run prints the same lines.

The case model. The model forecasts a monthly planning figure in whole units. For month index t its forecast is
forecast(t) = 100 + 2 * t (assumption M1: the trend of 2 units per month is the model's stated assumption). The
forecast for month t is issued before month t starts and uses no information from month t (assumption M2). The
eight-month window is months 13 to 20, so H = 8 months.

Error and hit. The error of month t is e = forecast - realised, in units. A month is a hit when |e| <= 2 (a band of
2 units, inclusive). A month with |e| = 2 exactly is a hit at the edge of the band.

Hit rate. The hit rate is the number of hits divided by H.

Bias. The bias is the mean error over the eight-month window, (1 / H) times the sum of e, in units per month. A
positive bias means the model forecasts too high on average.

Part A: the forecast, realised value, error and hit of each month.
Part B: the number of hits and the hit rate, to four decimals.
Part C: the bias, in units per month, to four decimals.
Part D: the months with |e| = 2 exactly, which are hits at the edge of the band.

The hit rate and the bias are exact Fractions. A value is rounded once, when it is printed: half up (a tie goes away
from zero).
"""

from __future__ import annotations

import math
from fractions import Fraction

START_MONTH = 13
HIT_BAND = 2
REALISED = (125, 131, 128, 132, 138, 133, 140, 135)  # y_t for months 13 to 20, illustrative values


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
    magnitude = math.floor(abs(value) * scale + Fraction(1, 2))
    sign = "-" if value < 0 and magnitude != 0 else ""
    whole, part = divmod(magnitude, scale)
    if places == 0:
        return f"{sign}{whole}"
    return f"{sign}{whole}.{part:0{places}d}"


def main() -> None:
    print(
        "SIMULATED case model: forecast(t) = 100 + 2t units; eight-month window, months 13 to 20, H = 8; band 2 units"
    )
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
