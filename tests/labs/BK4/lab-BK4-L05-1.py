"""BK4 L05 lab 1: the expected cost of settlement failures for three trades, by enumeration and in closed form.

SIMULATED. The failure probability, the cost per day and the delays are illustrative parameters. They describe no real
trade, no real market and no real failure rate. Every probability is an exact Fraction. Every cost is an integer number
of cents, except an expected cost, which is exact and may be a fraction of a cent. The only rounding in the program is
one step: an exact expected cost is rounded to the nearest whole cent, with an exact half cent going up.

The model. Trade i fails with the same probability p for each trade. A failed trade i is delayed by DELAYS_DAYS[i]
business days, and each business day of delay costs COST_PER_DAY_CENTS cents. The cost C of the three trades is the
sum of the costs of the failed trades. Two joint laws for the three failure events are compared. Both give each trade
the marginal probability p:

* independent failures: a fail pattern with k failed trades has probability p^k (1 - p)^(3 - k);
* comonotone failures: all three trades fail together with probability p, and none fails with probability 1 - p.

Part A prints the parameters. Part B lists the eight fail patterns under independent failures, with their
probabilities and costs, and compares the enumerated expected cost with the closed form p * kappa * (sum of the
delays). Part C takes equal delays ell and compares the enumeration with 3 * p * kappa * ell. Part D gives the mean
and the variance of the cost under both joint laws. Standard library only; no randomness and no network, so every run
prints the same lines.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

P_FAIL = Fraction(1, 8)
COST_PER_DAY_CENTS = 2500
DELAYS_DAYS = (1, 2, 4)
EQUAL_DELAY_DAYS = 2

Pattern = tuple[bool, ...]
Outcomes = list[tuple[Fraction, int]]


def all_patterns(count: int) -> list[Pattern]:
    """Every fail pattern of count trades, as tuples of booleans (True means the trade fails)."""
    return list(itertools.product((False, True), repeat=count))


def pattern_probability(pattern: Pattern, p: Fraction) -> Fraction:
    """Probability of one fail pattern under independent failures: the product of p or 1 - p over the trades."""
    prob = Fraction(1)
    for failed in pattern:
        prob *= p if failed else 1 - p
    return prob


def pattern_cost_cents(pattern: Pattern, delays: tuple[int, ...], cost_per_day: int) -> int:
    """Cost in cents of one fail pattern: cost_per_day times the delay of each failed trade, summed."""
    return sum(cost_per_day * delay for failed, delay in zip(pattern, delays, strict=True) if failed)


def independent_outcomes(p: Fraction, delays: tuple[int, ...], cost_per_day: int) -> Outcomes:
    """The (probability, cost in cents) pair of every fail pattern under independent failures."""
    return [
        (pattern_probability(pat, p), pattern_cost_cents(pat, delays, cost_per_day))
        for pat in all_patterns(len(delays))
    ]


def comonotone_outcomes(p: Fraction, delays: tuple[int, ...], cost_per_day: int) -> Outcomes:
    """The two outcomes under comonotone failures: no failure with probability 1 - p, all failing with probability p."""
    return [(1 - p, 0), (p, cost_per_day * sum(delays))]


def mean(outcomes: Outcomes) -> Fraction:
    """Exact expected cost in cents of a finite distribution given as (probability, cost) pairs."""
    return sum((prob * cost for prob, cost in outcomes), Fraction(0))


def variance(outcomes: Outcomes) -> Fraction:
    """Exact variance in square cents of a finite distribution given as (probability, cost) pairs."""
    second = sum((prob * cost * cost for prob, cost in outcomes), Fraction(0))
    return second - mean(outcomes) ** 2


def closed_form_mean(p: Fraction, delays: tuple[int, ...], cost_per_day: int) -> Fraction:
    """The closed form p * kappa * (sum of the delays), in cents. It uses only the marginal probability p."""
    return p * cost_per_day * sum(delays)


def round_half_up(amount: Fraction) -> int:
    """The nearest whole cent of a nonnegative exact amount, with an exact half cent going up."""
    if amount < 0:
        raise ValueError("round_half_up needs a nonnegative amount")
    return math.floor(amount + Fraction(1, 2))


def main() -> None:
    """Print Parts A to D. Probabilities are exact fractions; costs are cents; variances are square cents."""
    print("A. Parameters (SIMULATED, illustrative)")
    print(f"failure probability per trade p = {P_FAIL}")
    print(f"cost per business day of delay kappa = {COST_PER_DAY_CENTS} cents")
    print(f"delays ell_1, ell_2, ell_3 = {DELAYS_DAYS} business days")

    print("B. Independent failures: each fail pattern, with its probability and cost")
    total = Fraction(0)
    for pat in all_patterns(len(DELAYS_DAYS)):
        prob = pattern_probability(pat, P_FAIL)
        total += prob
        label = " ".join("fail" if failed else "ok" for failed in pat)
        cost = pattern_cost_cents(pat, DELAYS_DAYS, COST_PER_DAY_CENTS)
        print(f"pattern ({label}): probability {prob}, cost {cost} cents")
    enumerated = mean(independent_outcomes(P_FAIL, DELAYS_DAYS, COST_PER_DAY_CENTS))
    closed = closed_form_mean(P_FAIL, DELAYS_DAYS, COST_PER_DAY_CENTS)
    print(f"probabilities sum to one: {total == 1}")
    print(f"expected cost by enumeration: {enumerated} cents")
    print(f"closed form p * kappa * sum of delays: {closed} cents")
    print(f"enumeration equals closed form: {enumerated == closed}")
    print(f"closed form rounded half up to the cent: {round_half_up(closed)} cents")
    no_failure = pattern_probability((False,) * len(DELAYS_DAYS), P_FAIL)
    print(f"probability that no trade fails: {no_failure}")
    print(f"probability that at least one trade fails: {1 - no_failure}")
    print(f"three times p, for comparison: {3 * P_FAIL}")
    print(f"probability that at least one trade fails is below three times p: {1 - no_failure < 3 * P_FAIL}")

    print(f"C. Equal delays of {EQUAL_DELAY_DAYS} business days for each trade")
    equal_delays = (EQUAL_DELAY_DAYS,) * len(DELAYS_DAYS)
    enumerated_equal = mean(independent_outcomes(P_FAIL, equal_delays, COST_PER_DAY_CENTS))
    three_p_kappa_ell = 3 * P_FAIL * COST_PER_DAY_CENTS * EQUAL_DELAY_DAYS
    print(f"expected cost by enumeration: {enumerated_equal} cents")
    print(f"closed form 3 * p * kappa * ell: {three_p_kappa_ell} cents")
    print(f"enumeration equals 3 * p * kappa * ell: {enumerated_equal == three_p_kappa_ell}")

    print("D. Same marginal probability, two joint laws: no-cost probability, mean and variance")
    comonotone = comonotone_outcomes(P_FAIL, DELAYS_DAYS, COST_PER_DAY_CENTS)
    independent = independent_outcomes(P_FAIL, DELAYS_DAYS, COST_PER_DAY_CENTS)
    for name, outcomes in (("comonotone", comonotone), ("independent", independent)):
        zero = sum((prob for prob, cost in outcomes if cost == 0), Fraction(0))
        print(
            f"{name}: probability of no cost {zero}, mean {mean(outcomes)} cents, "
            f"variance {variance(outcomes)} square cents"
        )
    print(f"the two means are equal: {mean(comonotone) == mean(independent)}")
    print(f"the comonotone variance is larger: {variance(comonotone) > variance(independent)}")


main()
