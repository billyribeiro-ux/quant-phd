"""Student error (band): the hit test is half-open, -2 <= error < 2, so a month at +2 exactly is a miss."""

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
    return -HIT_BAND <= predicted - realised < HIT_BAND


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
