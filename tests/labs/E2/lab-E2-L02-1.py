"""E2 lab L02: symmetric first-price auction. The closed-form bid is checked on an exact bid grid.

Standard library only: exact rational arithmetic with fractions.Fraction. No randomness and no network.
Model: n bidders, n from 2 to 5. Each bidder's value is an independent draw from the uniform distribution
on [0, 1], and every other bidder uses the symmetric bid beta * value, with beta = (n - 1) / n. A bidder
with value v who bids b earns (v - b) times the probability that b is the highest bid. That probability is
(b / beta) ** (n - 1) for 0 <= b <= beta, because the other n - 1 bids are below b exactly when their values
are below b / beta, and it is 1 for b >= beta.

The lab tests the closed-form bid beta * v against every bid j / 1200 for j = 0 to 1200, on values k / 20
for k = 0 to 20. A check passes when the closed-form bid earns at least as much as every grid bid. The lab
also integrates exactly, term by term, the first-price revenue and the mean of the second-highest
value, for n from 2 to 5.
A grid check is a finite test of deviations on one grid. It is not a proof, and the page states the proof.
"""

from __future__ import annotations

from fractions import Fraction

GRID_STEPS = 1200
VALUE_STEPS = 20


def beta(n: int) -> Fraction:
    """The symmetric bid multiplier (n - 1) / n."""
    return Fraction(n - 1, n)


def win_probability(bid: Fraction, n: int) -> Fraction:
    """Probability that bid is the highest of n bids when the other n - 1 bidders use beta times their values."""
    if bid >= beta(n):
        return Fraction(1)
    return (bid / beta(n)) ** (n - 1)


def payoff(value: Fraction, bid: Fraction, n: int) -> Fraction:
    """Expected payoff of bidding bid with the given value, in units of value."""
    return (value - bid) * win_probability(bid, n)


def closed_form_is_grid_best(n: int, value: Fraction) -> bool:
    """True when beta * value earns at least as much as every bid on the grid."""
    closed = beta(n) * value
    closed_payoff = payoff(value, closed, n)
    best_grid = max(payoff(value, Fraction(j, GRID_STEPS), n) for j in range(GRID_STEPS + 1))
    return closed_payoff >= best_grid


def integrate(terms: dict[int, Fraction]) -> Fraction:
    """Exact integral over [0, 1] of the polynomial sum of coefficient * x ** exponent."""
    return sum((c / (e + 1) for e, c in terms.items()), Fraction(0))


def first_price_revenue(n: int) -> Fraction:
    """E[beta * highest value], with highest-value density n x ** (n - 1): beta * n times the integral of x ** n."""
    return integrate({n: Fraction(n - 1)})


def second_highest_mean(n: int) -> Fraction:
    """E[second-highest value], with density n (n - 1) x ** (n - 2) (1 - x)."""
    return integrate({n - 1: Fraction(n * (n - 1)), n: Fraction(-n * (n - 1))})


def second_density_mass(n: int) -> Fraction:
    """Integral of the density n (n - 1) x ** (n - 2) (1 - x) over [0, 1], which must equal 1."""
    return integrate({n - 2: Fraction(n * (n - 1)), n - 1: Fraction(-n * (n - 1))})


def main() -> None:
    print(f"symmetric first-price auction: value grid k/{VALUE_STEPS}, bid grid j/{GRID_STEPS}")
    for n in range(2, 6):
        values = [Fraction(k, VALUE_STEPS) for k in range(VALUE_STEPS + 1)]
        passed = sum(closed_form_is_grid_best(n, v) for v in values)
        print(f"n = {n}, beta = {beta(n)}: closed-form bid best on the grid for {passed} of {len(values)} values")
    for n in range(2, 6):
        first = first_price_revenue(n)
        second = second_highest_mean(n)
        print(
            f"n = {n}: first-price revenue {first}, mean second-highest value {second}, "
            f"equal {first == second}, density mass {second_density_mass(n)}"
        )


main()
