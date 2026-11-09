"""E3 L01 lab 1: expected value and expected utility of finite lotteries, computed exactly.

Inputs are illustrative, not data. An outcome is a final amount in whole cents, and every probability is an exact
Fraction. A lottery is a list of (outcome in cents, probability) pairs; its probabilities are non-negative and sum to
exactly 1. Two Bernoulli utilities are used: u(x) = x (linear in cents) and u(x) = x^2 / 10000 (quadratic). Both return
exact Fractions, so no rounding occurs and every printed value is exact.

Part A: the expected value and the expected utility of three lotteries under both utilities.
Part B: linearity in the probabilities, checked exactly for three mixing weights under both utilities.
Part C: a positive affine transformation u_tilde = 3 + 2u leaves the ordering of each pair of A, B and C
unchanged; checked exactly for each of the three pairs under both utilities.
Part D: a lottery with negative probabilities, and one whose probabilities do not sum to 1, are
rejected with ValueError.

No random draws are used, so every run prints the same lines.
"""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction

Lottery = list[tuple[int, Fraction]]
Utility = Callable[[int], Fraction]

LOTTERIES: dict[str, Lottery] = {
    "A": [(0, Fraction(1, 4)), (10000, Fraction(1, 2)), (40000, Fraction(1, 4))],
    "B": [(5000, Fraction(1, 2)), (20000, Fraction(1, 2))],
    "C": [(0, Fraction(1, 3)), (15000, Fraction(1, 3)), (30000, Fraction(1, 3))],
}


def check_lottery(lottery: Lottery) -> None:
    """Raise ValueError unless every probability is non-negative and the probabilities sum to exactly 1."""
    if any(p < 0 for _, p in lottery):
        raise ValueError("probabilities must be non-negative")
    if sum((p for _, p in lottery), Fraction(0)) != 1:
        raise ValueError("probabilities must sum to 1")


def expected_value(lottery: Lottery) -> Fraction:
    """The expected value E X = sum of p_i * x_i, in cents, as an exact Fraction."""
    check_lottery(lottery)
    return sum((p * x for x, p in lottery), Fraction(0))


def expected_utility(lottery: Lottery, u: Utility) -> Fraction:
    """The expected utility sum of p_i * u(x_i) for a Bernoulli utility u, as an exact Fraction."""
    check_lottery(lottery)
    return sum((p * u(x) for x, p in lottery), Fraction(0))


def mixture(rho: Fraction, first: Lottery, second: Lottery) -> Lottery:
    """The lottery that pays the outcomes of first with probability rho and of second with probability 1 - rho.

    The probability of an outcome is rho times its probability in first plus (1 - rho) times its probability in
    second, with a probability of 0 where an outcome does not appear. The result is sorted by outcome.
    """
    weights: dict[int, Fraction] = {}
    for x, p in first:
        weights[x] = weights.get(x, Fraction(0)) + rho * p
    for x, p in second:
        weights[x] = weights.get(x, Fraction(0)) + (1 - rho) * p
    return sorted(weights.items())


def linear(x: int) -> Fraction:
    """u(x) = x, in cents: a linear utility, which is risk neutral."""
    return Fraction(x)


def quadratic(x: int) -> Fraction:
    """u(x) = x^2 / 10000: a quadratic utility, in cents squared over 10000."""
    return Fraction(x * x, 10000)


def affine_of(u: Utility) -> Utility:
    """The utility u_tilde(x) = 3 + 2 u(x), a positive affine transformation of u."""

    def u_tilde(x: int) -> Fraction:
        return Fraction(3) + 2 * u(x)

    return u_tilde


def order(a: Fraction, b: Fraction) -> str:
    """The ordering of two numbers as a word: greater, less or equal."""
    if a > b:
        return "greater"
    if a < b:
        return "less"
    return "equal"


def main() -> None:
    """Print Parts A to D. Every value is an exact Fraction, so the output is reproducible."""
    print("Part A: expected value and expected utility, exact")
    for name, lottery in LOTTERIES.items():
        print(
            f"lottery {name} expected_value_cents {expected_value(lottery)} "
            f"eu_linear {expected_utility(lottery, linear)} eu_quadratic {expected_utility(lottery, quadratic)}"
        )

    print("Part B: linearity in the probabilities for the mixture rho*A + (1 - rho)*C")
    linearity_holds = True
    for rho in (Fraction(1, 4), Fraction(1, 3), Fraction(1, 2)):
        mixed = mixture(rho, LOTTERIES["A"], LOTTERIES["C"])
        for label, u in (("linear", linear), ("quadratic", quadratic)):
            lhs = expected_utility(mixed, u)
            rhs = rho * expected_utility(LOTTERIES["A"], u) + (1 - rho) * expected_utility(LOTTERIES["C"], u)
            linearity_holds = linearity_holds and lhs == rhs
            print(f"rho {rho} utility {label} mixture_eu {lhs} linear_combination {rhs} equal {lhs == rhs}")
    print(f"all_linearity_checks {linearity_holds}")

    print("Part C: pairwise order under u and under u_tilde = 3 + 2u")
    orders_preserved = True
    for left, right in (("A", "B"), ("A", "C"), ("B", "C")):
        for label, u in (("linear", linear), ("quadratic", quadratic)):
            under_u = order(expected_utility(LOTTERIES[left], u), expected_utility(LOTTERIES[right], u))
            under_tilde = order(
                expected_utility(LOTTERIES[left], affine_of(u)),
                expected_utility(LOTTERIES[right], affine_of(u)),
            )
            orders_preserved = orders_preserved and under_u == under_tilde
            same = under_u == under_tilde
            print(f"pair {left} {right} utility {label} order_u {under_u} order_tilde {under_tilde} same {same}")
    print(f"all_affine_orders_preserved {orders_preserved}")

    print("Part D: invalid lotteries are rejected")
    negative = [(0, Fraction(-1, 2)), (100, Fraction(3, 2))]
    short = [(0, Fraction(1, 2)), (100, Fraction(1, 3))]
    for label, bad in (("negative", negative), ("short", short)):
        try:
            expected_utility(bad, linear)
        except ValueError as exc:
            print(f"rejected {label} message {exc}")


main()
