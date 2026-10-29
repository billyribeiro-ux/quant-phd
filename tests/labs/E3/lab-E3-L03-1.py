"""E3 lab L03: the CRRA certainty equivalent in integer cents, checked on one fixed lottery.

The lottery is fixed in the code: three final-wealth outcomes in cents, with exact probabilities 1/4, 1/2 and 1/4.
No random numbers are drawn, and no data is read, so nothing here is SIMULATED. Standard library only (itertools,
math and fractions), no network. Exact values use fractions.Fraction. The power forms are floating-point, so their
checks use stated tolerances. A certainty equivalent is a money amount: it is computed once as a float and rounded to
whole cents by floor(value + 1/2), which rounds halves up. Both the unrounded float and the rounded cents are printed.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

PRIZES_CENTS = (5000, 10000, 20000)
PROBS = (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4))
GAMMAS = (0.0, 0.25, 0.5, 1.0, 2.0, 4.0)
TOL = 1e-9


def crra_utility(w: float, gamma: float) -> float:
    """CRRA utility of positive wealth w in cents: (w**(1 - gamma) - 1) / (1 - gamma) if gamma != 1, else ln(w).

    The subtracted 1 is a constant. It changes no certainty equivalent and no Pratt measure, and it makes the
    utility continuous in gamma at gamma = 1. Raises ValueError when w is not positive, because the power form is
    defined on positive wealth only.
    """
    if w <= 0.0:
        raise ValueError(f"CRRA utility needs positive wealth, got {w}")
    if gamma == 1.0:
        return math.log(w)
    return float((w ** (1.0 - gamma) - 1.0) / (1.0 - gamma))


def certainty_equivalent(prizes: tuple[int, ...], probs: tuple[Fraction, ...], gamma: float) -> float:
    """Unrounded certainty equivalent in cents: the amount c with u(c) equal to the expected CRRA utility.

    For gamma != 1 it equals (sum of p * x**(1 - gamma)) ** (1 / (1 - gamma)); for gamma = 1 it equals
    exp(sum of p * ln x). All prizes must be positive, so every power is defined.
    """
    p = [float(q) for q in probs]
    if gamma == 1.0:
        return math.exp(float(sum(pi * math.log(x) for pi, x in zip(p, prizes, strict=True))))
    s = 1.0 - gamma
    return float(sum(pi * x**s for pi, x in zip(p, prizes, strict=True)) ** (1.0 / s))


def to_cents(value: float) -> int:
    """Round a non-negative money amount, in cents, to the nearest whole cent, with halves rounded up."""
    if value < 0.0:
        raise ValueError(f"money amounts here are non-negative, got {value}")
    return math.floor(value + 0.5)


def close(x: float, y: float) -> bool:
    """True when |x - y| <= TOL * max(1, |y|): an absolute tolerance near 1, a relative one above 1."""
    return abs(x - y) <= TOL * max(1.0, abs(y))


def main() -> None:
    mean = sum(q * x for q, x in zip(PROBS, PRIZES_CENTS, strict=True))
    print(f"prizes in cents: {list(PRIZES_CENTS)}; probabilities: {[str(q) for q in PROBS]}")
    print(f"expected prize in cents, exact: {mean}")

    ces: dict[float, float] = {}
    for g in GAMMAS:
        ce = certainty_equivalent(PRIZES_CENTS, PROBS, g)
        ces[g] = ce
        print(f"gamma {g:g}: certainty equivalent {ce:.4f} cents, rounded to {to_cents(ce)} cents")

    harmonic = 1 / sum(q / x for q, x in zip(PROBS, PRIZES_CENTS, strict=True))
    print(f"gamma 2 exact value 1 / sum of p/x: {harmonic} cents")
    print(f"gamma 2 float agrees with the exact value: {close(ces[2.0], float(harmonic))}")
    print(f"gamma 0 equals the expected prize: {close(ces[0.0], float(mean))}")
    print(f"gamma 1 equals the exact geometric mean 10000 cents: {close(ces[1.0], 10000.0)}")

    falling = all(ces[a] >= ces[b] for a, b in itertools.pairwise(GAMMAS))
    below = all(ces[g] <= float(mean) + TOL * float(mean) for g in GAMMAS)
    print(f"certainty equivalent falls as gamma rises on this grid: {falling}")
    print(f"every certainty equivalent is at most the expected prize on this grid: {below}")

    gap = max(abs(certainty_equivalent(PRIZES_CENTS, PROBS, 1.0 + s * 1e-6) - ces[1.0]) for s in (-1.0, 1.0))
    print(f"certainty equivalent at gamma 1 +/- 1e-6 is within 0.01 cents of gamma 1: {gap <= 0.01}")
    slopes = []
    for h in (1e-3, 1e-6):
        up = certainty_equivalent(PRIZES_CENTS, PROBS, 1.0 + h)
        down = certainty_equivalent(PRIZES_CENTS, PROBS, 1.0 - h)
        slopes.append((up - down) / (2.0 * h))
    agree = abs(slopes[0] - slopes[1]) <= 1e-3 * abs(slopes[1])
    print(f"central slope in gamma at gamma 1 agrees for h = 1e-3 and h = 1e-6 to 0.1 percent: {agree}")

    # The error of (w**s - 1) / s against ln(w), with s = 1 - gamma, is about s * (ln w)**2 / 2 (a first-order
    # term), so the check allows 1e-6 * (ln w)**2 at s = 1e-6.
    limit_ok = True
    for w in (0.5, 2.0, 10000.0):
        err = abs(crra_utility(w, 1.0 - 1e-6) - math.log(w))
        limit_ok = limit_ok and err <= 1e-6 * math.log(w) ** 2
    print(f"CRRA utility at gamma 1 - 1e-6 matches ln(w) within 1e-6 (ln w)^2 for w in 0.5, 2 and 10000: {limit_ok}")

    worst_rel = 0.0
    cents_ok = True
    for k in (2, 3, 10):
        scaled = tuple(k * x for x in PRIZES_CENTS)
        for g in GAMMAS:
            scaled_ce = certainty_equivalent(scaled, PROBS, g)
            worst_rel = max(worst_rel, abs(scaled_ce / (k * ces[g]) - 1.0))
            if abs(to_cents(scaled_ce) - k * to_cents(ces[g])) > (k + 1) / 2:
                cents_ok = False
    print(
        f"homogeneity CE(kx) = k CE(x) for k in 2, 3, 10 on the lab grid of gamma values, "
        f"unrounded: {worst_rel <= 1e-12}"
    )
    print(f"cents bound |round(CE(kx)) - k round(CE(x))| <= (k + 1) / 2 holds on this grid: {cents_ok}")


main()
