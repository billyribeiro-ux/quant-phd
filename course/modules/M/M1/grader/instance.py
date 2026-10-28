"""Per-learner instances for the M1 autograder: the annuity and mortgage engine. All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws:

* a loan: principal in integer cents (50,000.00 to 600,000.00), a nominal annual rate in whole basis points
  (1.50 % to 12.00 %), and a term of 60, 120, 180, 240, 300 or 360 months;
* an ordinary annuity: a per-period rate (0.10 % to 20.00 %) and 1 to 60 periods;
* a growing perpetuity: a per-period rate (2.00 % to 20.00 %) and a growth rate in whole basis points, at least
  100 basis points below the rate, and above -2.00 %.

Every instance is valid under the contract in project.html. A draw is rejected, and the next draw taken, when the
exact schedule would put a level payment or an interest amount within 1e-6 of a half cent. Such an amount has no
unique nearest cent once floating point is involved, so the contract's rule would then not be a fair test of a
correct implementation.

Nothing here is a real loan, a real rate or market data.
"""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Any

_TIE_MARGIN = 1e-6
_TERMS = (60, 120, 180, 240, 300, 360)


def _nearest_cent(x: Fraction) -> int:
    """The nearest integer to a non-negative exact amount, a tie going up: floor(x + 1/2)."""
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def _clear_of_half_cent(x: Fraction) -> bool:
    """True when the fractional part of x is at least 1e-6 away from one half."""
    fraction = x - (x.numerator // x.denominator)
    return abs(float(fraction) - 0.5) > _TIE_MARGIN


def _schedule_is_clear(principal: int, annual_bps: int, months: int) -> bool:
    """True when every level payment and every interest amount of the exact schedule is clear of a half cent."""
    i = Fraction(annual_bps, 120_000)  # the monthly rate: (annual_bps / 10 000) / 12
    level = Fraction(principal) * i / (1 - (1 + i) ** (-months))
    if not _clear_of_half_cent(level):
        return False
    payment = _nearest_cent(level)
    balance = principal
    for month in range(1, months + 1):
        interest_exact = balance * i
        if not _clear_of_half_cent(interest_exact):
            return False
        interest = _nearest_cent(interest_exact)
        if month < months:
            balance -= payment - interest
    return True


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED instance for ``seed``. Every instance is valid."""
    for attempt in range(10_000):
        rng = random.Random(1_000_003 * int(seed) + 7_919 * attempt + 17)
        principal = rng.randrange(5_000_000, 60_000_001)
        annual_bps = rng.randrange(150, 1201)
        months = rng.choice(_TERMS)
        if not _schedule_is_clear(principal, annual_bps, months):
            continue
        annuity_bps = rng.randrange(10, 2001)
        annuity_periods = rng.randrange(1, 61)
        perpetuity_bps = rng.randrange(200, 2001)
        growth_bps = rng.randrange(-200, perpetuity_bps - 99)
        return {
            "seed": int(seed),
            "label": "SIMULATED",
            "principal_cents": principal,
            "annual_bps": annual_bps,
            "annual_rate": annual_bps / 10_000,
            "months": months,
            "annuity_bps": annuity_bps,
            "annuity_rate": annuity_bps / 10_000,
            "annuity_periods": annuity_periods,
            "perpetuity_bps": perpetuity_bps,
            "perpetuity_rate": perpetuity_bps / 10_000,
            "growth_bps": growth_bps,
            "growth_rate": growth_bps / 10_000,
        }
    raise RuntimeError("no clear instance found in 10 000 draws")  # a guard against an endless loop
