"""Correct alternative: lab 2 blanks written as len(errors), float division and a half-up Decimal rounding."""
import math
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

START_MONTH = 13
HIT_BAND = 2
REALISED = (127, 126, 124, 131, 136, 141)


def forecast(t: int) -> int:
    return 100 + 2 * t


def is_hit(predicted: int, realised: int) -> bool:
    if realised <= 0:
        raise ValueError("bad")
    return abs(predicted - realised) <= HIT_BAND


def decimal_text(value, places: int) -> str:
    q = Decimal(value.numerator) / Decimal(value.denominator) if isinstance(value, Fraction) else Decimal(value)
    return str(q.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def main() -> None:
    print("SIMULATED case model: forecast(t) = 100 + 2t units; six-month window, months 13 to 18, H = 6; band 2 units")
    print("Part A: month, forecast, realised, error (forecast - realised), hit")
    errors = []
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
    hit_rate = Fraction(hits, len(errors))
    print(f"Part B: hits {hits} of {horizon}; hit rate {decimal_text(hit_rate, 4)}")
    bias = sum(errors) / horizon
    print(f"Part C: bias {decimal_text(bias, 4)} units per month")
    edge = [START_MONTH + i for i, e in enumerate(errors) if abs(e) == HIT_BAND]
    print(f"Part D: months with |error| = 2 exactly (hits at the edge): {edge}")


main()
