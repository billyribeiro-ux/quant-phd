"""FC2 lab L01: arbitrage in a two-date, two-state price set, in exact arithmetic.

The two price sets are typed in for this lab. Holdings are integers searched over a finite box, so a count of zero
means zero portfolios in that box; the algebra in the lesson, not the box, decides the general claims. Prices and
payoffs are fractions.Fraction, so every printed value is exact. Standard library only; no network; no randomness.

Conventions: a portfolio is a pair (bond units, stock units). Its cost is the sum of holdings times prices at date 0.
Its payoff in a state is the sum of holdings times that asset's payoff in that state, at date 1. An arbitrage
opportunity is a portfolio whose cost is at most zero, whose payoff is at least zero in both states, and which is
not free of profit: its cost is strictly negative or its payoff is strictly positive in some state.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

BOX = range(-10, 11)
SMALL = range(-2, 3)

Holding = tuple[int, int]


def payoff_of(holding: Holding, payoffs: list[list[Fraction]]) -> list[Fraction]:
    """Payoff at date 1 in each state: payoffs[state][asset] times holding[asset], summed over assets."""
    return [sum((holding[j] * row[j] for j in range(len(row))), Fraction(0)) for row in payoffs]


def cost_of(holding: Holding, prices: list[Fraction]) -> Fraction:
    """Cost at date 0: prices[asset] times holding[asset], summed over assets."""
    return sum((holding[j] * prices[j] for j in range(len(prices))), Fraction(0))


def is_arbitrage(holding: Holding, prices: list[Fraction], payoffs: list[list[Fraction]]) -> bool:
    """True when the cost is at most zero, the payoff is at least zero in every state, and the portfolio is not
    free of profit: its cost is strictly negative or its payoff is strictly positive in some state."""
    cost = cost_of(holding, prices)
    pay = payoff_of(holding, payoffs)
    if cost > 0 or any(x < 0 for x in pay):
        return False
    return cost < 0 or any(x > 0 for x in pay)


def arbitrages_in_box(prices: list[Fraction], payoffs: list[list[Fraction]]) -> list[Holding]:
    """Every arbitrage portfolio with holdings in BOX, in lexicographic order."""
    return [h for h in product(BOX, BOX) if is_arbitrage(h, prices, payoffs)]


def state_prices(prices: list[Fraction], payoffs: list[list[Fraction]]) -> tuple[Fraction, Fraction]:
    """Solve psi_u * X[u][j] + psi_d * X[d][j] = price_j for j = 0, 1 (Cramer's rule on the 2 by 2 system)."""
    a, b = payoffs[0][0], payoffs[1][0]
    c, d = payoffs[0][1], payoffs[1][1]
    det = a * d - b * c
    psi_u = (prices[0] * d - b * prices[1]) / det
    psi_d = (a * prices[1] - c * prices[0]) / det
    return psi_u, psi_d


def dominance_violations(prices: list[Fraction], payoffs: list[list[Fraction]]) -> tuple[int, int]:
    """Over holdings in SMALL: count pairs (a, b) with payoff(a) >= payoff(b) in both states, and the number of
    those pairs for which cost(a) < cost(b)."""
    holdings = list(product(SMALL, SMALL))
    dominating = 0
    violating = 0
    for a in holdings:
        pa = payoff_of(a, payoffs)
        for b in holdings:
            pb = payoff_of(b, payoffs)
            if all(x >= y for x, y in zip(pa, pb, strict=True)):
                dominating += 1
                if cost_of(a, prices) < cost_of(b, prices):
                    violating += 1
    return dominating, violating


def main() -> None:
    # Rows are states (u, d); columns are the bond and the stock, each paying the amount shown at date 1.
    payoffs = [[Fraction(1), Fraction(3)], [Fraction(1), Fraction(1)]]
    consistent = [Fraction(9, 10), Fraction(1)]
    mispriced = [Fraction(9, 10), Fraction(1, 2)]

    print("A. Consistent prices: bond 9/10, stock 1; state u pays bond 1 and stock 3; state d pays bond 1 and stock 1")
    print("arbitrage portfolios with holdings in the box:", len(arbitrages_in_box(consistent, payoffs)))
    psi_u, psi_d = state_prices(consistent, payoffs)
    print("state prices (state u, state d):", psi_u, psi_d)
    print("both state prices strictly positive:", psi_u > 0 and psi_d > 0)
    reprices = all(psi_u * payoffs[0][j] + psi_d * payoffs[1][j] == consistent[j] for j in range(2))
    print("state prices reproduce both prices exactly:", reprices)
    dom, bad = dominance_violations(consistent, payoffs)
    print("holdings pairs in SMALL with payoff(a) at least payoff(b) in both states:", dom)
    print("of those, pairs whose cost(a) is below cost(b):", bad)

    print()
    print("B. Mispriced stock: bond 9/10, stock 1/2, same payoffs")
    found = arbitrages_in_box(mispriced, payoffs)
    print("arbitrage portfolios with holdings in the box:", len(found))
    zero_cost = [
        h for h in product(BOX, BOX) if cost_of(h, mispriced) == 0 and all(x > 0 for x in payoff_of(h, payoffs))
    ]
    holding = zero_cost[0]
    print("first zero-cost portfolio with payoff strictly positive in both states, holdings (bond, stock):", holding)
    print("cost at date 0:", cost_of(holding, mispriced))
    pay = payoff_of(holding, payoffs)
    print("payoff in state u:", pay[0])
    print("payoff in state d:", pay[1])
    psi_u_b, psi_d_b = state_prices(mispriced, payoffs)
    print("state prices (state u, state d):", psi_u_b, psi_d_b)
    print("one state price is negative:", psi_u_b < 0 or psi_d_b < 0)
    value_by_states = psi_u_b * pay[0] + psi_d_b * pay[1]
    print("state prices applied to that payoff equal its cost:", value_by_states == cost_of(holding, mispriced))
    dom_b, bad_b = dominance_violations(mispriced, payoffs)
    print("holdings pairs in SMALL with payoff(a) at least payoff(b) in both states:", dom_b)
    print("of those, pairs whose cost(a) is below cost(b):", bad_b)


main()
