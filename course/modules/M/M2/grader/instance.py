"""Per-learner instances for the M2 autograder: the sensitivity engine. All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws:

* a bond: face value in whole cents (10,000.00 to 500,000.00), an annual coupon rate in whole basis points
  (0.00 % to 10.00 %), a maturity of 1 to 30 whole years, and an annual yield in whole basis points
  (1.00 % to 15.00 %);
* a smooth test function of one variable, a cubic with seeded coefficients, and a point x0 at which it is
  differentiated;
* a smooth test function of two variables, a quadratic with a cubic cross term, with seeded coefficients, and a
  point (u0, v0) at which its Hessian is taken.

Every instance is valid under the contract in project.html. A bond draw is rejected, and the next draw taken, when
its exact price would sit within 1e-6 of a half cent, because a price with no unique nearest cent would not be a
fair test of a correct implementation. A cubic draw is rejected when its second derivative at x0 is smaller than 1
in size, or its third-degree coefficient is smaller than 0.1 in size, because the finite-difference order checks
would then not be well conditioned.

Nothing here is a real bond, a real yield or market data.
"""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Any

_TIE_MARGIN = Fraction(1, 1_000_000)


def _exact_price_cents(face: int, coupon_bps: int, years: int, yield_bps: int) -> Fraction:
    """The exact unrounded price in cents of the annual-pay bond, in rational arithmetic."""
    coupon = Fraction(face * coupon_bps, 10_000)
    v = 1 / (1 + Fraction(yield_bps, 10_000))
    total = Fraction(0)
    for t in range(1, years + 1):
        cash = coupon + (face if t == years else 0)
        total += cash * v**t
    return total


def _clear_of_half_cent(x: Fraction) -> bool:
    """True when the fractional part of x is at least 1e-6 away from one half."""
    fraction = x - (x.numerator // x.denominator)
    return abs(fraction - Fraction(1, 2)) > _TIE_MARGIN


def _cubic_is_well_conditioned(coefficients: list[float], x0: float) -> bool:
    """True when the second derivative at x0 is at least 1 in size and the cubic coefficient at least 0.1."""
    _, _, p2, p3 = coefficients
    second = 2 * p2 + 6 * p3 * x0
    return abs(second) >= 1.0 and abs(p3) >= 0.1


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED instance for ``seed``. Every instance is valid."""
    for attempt in range(10_000):
        rng = random.Random(1_000_003 * int(seed) + 7_919 * attempt + 29)
        face = rng.randrange(1_000_000, 50_000_001)
        coupon_bps = rng.randrange(0, 1001)
        years = rng.randrange(1, 31)
        yield_bps = rng.randrange(100, 1501)
        if not _clear_of_half_cent(_exact_price_cents(face, coupon_bps, years, yield_bps)):
            continue
        x0 = rng.randrange(25, 176) / 100
        p0 = rng.randrange(-300, 301) / 100
        p1 = rng.randrange(-300, 301) / 100
        p2 = rng.randrange(200, 501) / 100
        sign = rng.choice((-1, 1))
        p3 = sign * rng.randrange(10, 101) / 100
        cubic = [p0, p1, p2, p3]
        if not _cubic_is_well_conditioned(cubic, x0):
            continue
        surface = [rng.randrange(-200, 201) / 100 for _ in range(7)]
        point = [rng.randrange(-100, 101) / 100, rng.randrange(-100, 101) / 100]
        return {
            "seed": int(seed),
            "label": "SIMULATED",
            "face_cents": face,
            "coupon_bps": coupon_bps,
            "maturity_years": years,
            "yield_bps": yield_bps,
            "x0": x0,
            "cubic": cubic,
            "surface": surface,
            "point": point,
        }
    raise RuntimeError("no valid instance found in 10 000 draws")  # a guard against an endless loop
