"""E3 L02 lab 1: certainty equivalents, risk premia and the second-order approximation on one gamble.

Inputs are illustrative, not data. The initial wealth is w = 100 CU. The gamble is X, with outcomes -60, 0 and 60 CU
and probabilities 1/4, 1/2 and 1/4 (exact Fractions). Its mean is 0 and its variance is 1800 CU squared. The wealth
lottery at scale eps is W = w + eps X, so its mean is w for every eps.

Two Bernoulli utilities are compared on this one gamble: u(w) = sqrt(w), which is strictly concave, and u(w) = w,
which is linear. The certainty equivalent is CE = u^{-1}(E u(W)); for sqrt, u^{-1}(y) = y^2 for y >= 0, and for the
linear utility u^{-1}(y) = y. The risk premium is w - CE. The Arrow-Pratt measures are r_A(w) = -u''(w)/u'(w) and
r_R(w) = w r_A(w). The second-order approximation of the premium is 0.5 r_A(w) Var(eps X) = 0.5 r_A(w) eps^2 Var(X).

Floating-point arithmetic is used, at full double precision. Money outputs are whole cents: a CU amount is multiplied
by 100 and rounded once, with a tie going up (half up), by the function half_up_cents. Other values are unrounded CU
quantities, printed with six decimal places.

Part A: at eps = 1, the certainty equivalent and the premium in cents, and the exact premium beside the approximation.
Part B: the ratio of the exact premium to eps^2 at five scales, beside the limit 0.5 r_A(w) Var(X).
Part C: for the linear utility, the premium is zero at each of three scales.
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Callable
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction

WEALTH = 100
GAMBLE: list[tuple[int, Fraction]] = [(-60, Fraction(1, 4)), (0, Fraction(1, 2)), (60, Fraction(1, 4))]


@dataclass(frozen=True)
class Utility:
    """A Bernoulli utility with its first and second derivatives and the inverse of u on its range."""

    name: str
    value: Callable[[float], float]
    slope: Callable[[float], float]
    curvature: Callable[[float], float]
    inverse: Callable[[float], float]

    def arrow_pratt(self, w: float) -> float:
        """The absolute risk aversion r_A(w) = -u''(w) / u'(w), in 1/CU."""
        return -self.curvature(w) / self.slope(w) + 0.0

    def relative(self, w: float) -> float:
        """The relative risk aversion r_R(w) = w r_A(w), which is dimensionless."""
        return w * self.arrow_pratt(w)


def sqrt_value(w: float) -> float:
    """u(w) = sqrt(w), for w > 0."""
    return math.sqrt(w)


def sqrt_slope(w: float) -> float:
    """u'(w) = 1/(2 sqrt(w)), for w > 0."""
    return 0.5 / math.sqrt(w)


def sqrt_curvature(w: float) -> float:
    """u''(w) = -1/(4 w^(3/2)), for w > 0."""
    return -0.25 / (w * math.sqrt(w))


def sqrt_inverse(y: float) -> float:
    """The inverse of sqrt on y >= 0: u^{-1}(y) = y^2."""
    return y * y


def linear_value(w: float) -> float:
    """u(w) = w."""
    return w


def linear_slope(w: float) -> float:
    """u'(w) = 1."""
    return 1.0


def linear_curvature(w: float) -> float:
    """u''(w) = 0."""
    return 0.0


def linear_inverse(y: float) -> float:
    """The inverse of the identity: u^{-1}(y) = y."""
    return y


SQRT = Utility("sqrt", sqrt_value, sqrt_slope, sqrt_curvature, sqrt_inverse)
LINEAR = Utility("linear", linear_value, linear_slope, linear_curvature, linear_inverse)


def half_up_cents(amount_cu: float) -> int:
    """The CU amount in whole cents: 100 times the amount, rounded once, with a tie going up."""
    return int(Decimal(amount_cu * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def mean_and_variance() -> tuple[float, float]:
    """The exact mean and variance of the gamble X, computed from its Fractions and returned as floats."""
    mean = sum((p * x for x, p in GAMBLE), Fraction(0))
    variance = sum((p * x * x for x, p in GAMBLE), Fraction(0)) - mean * mean
    return float(mean), float(variance)


def certainty_equivalent(u: Utility, eps: float) -> float:
    """The wealth CE = u^{-1}(E u(W)) of the lottery W = WEALTH + eps X, unrounded, in CU."""
    expected = 0.0
    for x, p in GAMBLE:
        expected += float(p) * u.value(WEALTH + eps * x)
    return u.inverse(expected)


def main() -> None:
    """Print Parts A, B and C. Every value comes from the formulas above, so the output is reproducible."""
    mean, variance = mean_and_variance()
    print(f"gamble mean_cu {mean:.6f} variance_cu2 {variance:.6f} wealth_cu {WEALTH}")

    print("Part A: eps = 1; CE and premium in whole cents; unrounded CU for the approximation")
    for u in (SQRT, LINEAR):
        ce = certainty_equivalent(u, 1.0)
        premium = WEALTH - ce
        r_a = u.arrow_pratt(WEALTH)
        approx = 0.5 * r_a * variance
        print(
            f"utility {u.name} ce_cents {half_up_cents(ce)} premium_cents {half_up_cents(premium)} "
            f"r_A {r_a:.6f} r_R {u.relative(WEALTH):.6f} exact_premium_cu {premium:.6f} "
            f"pratt_premium_cu {approx:.6f} error_cu {premium - approx:.6f} "
            f"ce_below_mean {ce < WEALTH}"
        )

    print("Part B: premium over eps^2 for the square-root utility, beside the limit 0.5 r_A(w) Var(X)")
    limit = 0.5 * SQRT.arrow_pratt(WEALTH) * variance
    gaps: list[float] = []
    for eps in (1.0, 0.5, 0.25, 0.1, 0.01):
        premium = WEALTH - certainty_equivalent(SQRT, eps)
        ratio = premium / (eps * eps)
        gaps.append(abs(ratio - limit))
        print(f"eps {eps} premium_over_eps_squared {ratio:.6f} limit {limit:.6f} gap {abs(ratio - limit):.6f}")
    shrinking = all(later < earlier for earlier, later in itertools.pairwise(gaps))
    print(f"gaps_shrink_as_eps_falls {shrinking}")

    print("Part C: the linear utility has zero premium at three scales")
    zero = True
    for eps in (1.0, 0.5, 0.1):
        premium = WEALTH - certainty_equivalent(LINEAR, eps)
        zero = zero and half_up_cents(premium) == 0
        print(f"eps {eps} linear_premium_cents {half_up_cents(premium)} linear_r_A {LINEAR.arrow_pratt(WEALTH):.6f}")
    print(f"linear_premium_zero_at_three_scales {zero}")


main()
