"""LX1 L01 lab 1: the fundamental value of a constant-growth asset, a finite sum, and a simulated price gap.

Inputs are illustrative, not data: a first-period dividend of 400 cents, a per-period discount rate of 9 percent and a
per-period dividend growth rate of 3 percent. The price path is SIMULATED: each period's wedge over the fundamental is
one draw from a seeded generator, so every run prints the same lines. No market is described by these numbers.

Amounts are in cents. Each amount is an exact Fraction, and Part A prints F_0 as that fraction. A whole-cent amount
is the Fraction rounded once, half up, and each printed gap is the difference of two whole-cent amounts.

Part A: the closed form F_0 = d_1 / (r - g) and the finite sum S_N of the first N discounted dividends, with the exact
identity S_N = F_0 (1 - q^N) for q = (1 + g) / (1 + r).
Part B: the fundamental F_t = d_1 (1 + g)^t / (r - g) at t = 0 to 12, a seeded price path A_t = F_t (1 + w_t), and the
gap A_t - F_t in cents.
Part C: the same price path compared with the fundamental under an alternative growth rate of 1 percent.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction

DIVIDEND_1_CENTS = 400
DISCOUNT_RATE = Fraction(9, 100)
GROWTH_RATE = Fraction(3, 100)
ALT_GROWTH_RATE = Fraction(1, 100)
HORIZON = 12
SEED = 20261103
WEDGE_LOW_PERCENT = -8
WEDGE_HIGH_PERCENT = 25


def round_half_up(amount: Fraction) -> int:
    """Round a Fraction to the nearest whole number, with a tie going up (toward plus infinity)."""
    return math.floor(amount + Fraction(1, 2))


def fundamental(dividend_1: int, rate: Fraction, growth: Fraction, t: int) -> Fraction:
    """Value at time t, in cents, of dividends d_s = dividend_1 (1 + growth)^(s - 1) paid at the end of periods s > t.

    The closed form is d_{t+1} / (rate - growth) = dividend_1 (1 + growth)^t / (rate - growth). It needs
    rate > growth and 1 + growth > 0; a violation raises ValueError rather than returning a number.
    """
    if not rate > growth:
        raise ValueError("the closed form needs rate > growth")
    if not 1 + growth > 0:
        raise ValueError("the closed form needs 1 + growth > 0")
    return Fraction(dividend_1) * (1 + growth) ** t / (rate - growth)


def partial_sum(dividend_1: int, rate: Fraction, growth: Fraction, terms: int) -> Fraction:
    """Sum of the first `terms` discounted dividends, in cents: the sum over s = 1..N of d_s / (1 + rate)^s."""
    total = Fraction(0)
    for s in range(1, terms + 1):
        total += Fraction(dividend_1) * (1 + growth) ** (s - 1) / (1 + rate) ** s
    return total


def main() -> None:
    """Print Parts A, B and C in a fixed order."""
    # Part A: the closed form and the finite sum, exact.
    f0 = fundamental(DIVIDEND_1_CENTS, DISCOUNT_RATE, GROWTH_RATE, 0)
    print(f"Part A: closed form F_0 = d_1 / (r - g) = {f0} cents, rounded {round_half_up(f0)} cents")
    q = (1 + GROWTH_RATE) / (1 + DISCOUNT_RATE)
    print(f"ratio q = (1 + g) / (1 + r) = {q}; 0 < q < 1: {0 < q < 1}")
    for terms in (10, 60, 200):
        s_n = partial_sum(DIVIDEND_1_CENTS, DISCOUNT_RATE, GROWTH_RATE, terms)
        identity = s_n == f0 * (1 - q**terms)
        residual = f0 * q**terms
        print(
            f"N = {terms}: sum rounded {round_half_up(s_n)} cents; "
            f"identity S_N = F_0 (1 - q^N) holds exactly: {identity}; "
            f"F_0 q^N rounded {round_half_up(residual)} cents"
        )
    s_200_cents = round_half_up(partial_sum(DIVIDEND_1_CENTS, DISCOUNT_RATE, GROWTH_RATE, 200))
    print(f"200-term sum rounds to the closed form: {s_200_cents == round_half_up(f0)}")

    # Part B: the fundamental path and a seeded simulated price path.
    rng = random.Random(SEED)
    print("Part B: SIMULATED price path; wedge w_t drawn from a seeded generator, price = F_t (1 + w_t)")
    gaps: list[int] = []
    for t in range(HORIZON + 1):
        fund_cents = round_half_up(fundamental(DIVIDEND_1_CENTS, DISCOUNT_RATE, GROWTH_RATE, t))
        wedge = Fraction(rng.randint(WEDGE_LOW_PERCENT, WEDGE_HIGH_PERCENT), 100)
        price_cents = round_half_up(fundamental(DIVIDEND_1_CENTS, DISCOUNT_RATE, GROWTH_RATE, t) * (1 + wedge))
        gap = price_cents - fund_cents
        gaps.append(gap)
        print(
            f"t = {t:2d}: wedge {float(wedge):+.2f}; fundamental {fund_cents} cents; "
            f"price {price_cents} cents; gap {gap} cents"
        )
    positive = [t for t, gap in enumerate(gaps) if gap > 0]
    top = max(range(HORIZON + 1), key=lambda t: gaps[t])
    print(f"periods with price above fundamental: {len(positive)} of {HORIZON + 1}")
    print(f"largest gap {gaps[top]} cents at t = {top}")

    # Part C: the same price path against the fundamental under an alternative growth rate.
    print(f"Part C: the same prices against the fundamental with growth {float(ALT_GROWTH_RATE):.2f} per period")
    rng = random.Random(SEED)
    alt_positive = 0
    for t in range(HORIZON + 1):
        wedge = Fraction(rng.randint(WEDGE_LOW_PERCENT, WEDGE_HIGH_PERCENT), 100)
        price_cents = round_half_up(fundamental(DIVIDEND_1_CENTS, DISCOUNT_RATE, GROWTH_RATE, t) * (1 + wedge))
        alt_fund = round_half_up(fundamental(DIVIDEND_1_CENTS, DISCOUNT_RATE, ALT_GROWTH_RATE, t))
        alt_gap = price_cents - alt_fund
        alt_positive += alt_gap > 0
        print(f"t = {t:2d}: alternative fundamental {alt_fund} cents; gap {alt_gap} cents")
    print(f"periods with price above the alternative fundamental: {alt_positive} of {HORIZON + 1}")
    print(f"the count changes with the assumed growth rate: {alt_positive != len(positive)}")


main()
