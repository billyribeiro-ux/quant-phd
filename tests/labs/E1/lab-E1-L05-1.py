"""E1 L05 lab 1: the monopoly price on linear demand, and the Lerner index against 1/|elasticity| at the optimum.

Inputs are illustrative parameters, not data. Demand is Q(p) = a - b p units, with the price p in cents per unit.
The monopolist has a constant marginal cost of c cents per unit. Three cases are run: the reference case
(a, b, c) = (120, 1, 20), and two further cases that test the same identities away from it. No random draws are
used, and no file is read.

Part A: the monopoly profit (p - c) Q(p) in cents is evaluated on a grid of prices in steps of 1/10 cent, from 0 to
the choke price a/b, in exact Fractions. The grid argmax is compared with the closed form p_m = (a + b c) / (2 b).
Part B: at p_m, the Lerner index (p - c) / p is compared with 1/|e|, where e = -b p / (a - b p) is the price
elasticity of demand. The two are exact Fractions, and the lab checks that they are equal.
Part C: the monopoly quantity, the profit, the slope of the profit at p_m, the second difference of the profit, and
the gap between the monopoly price and the revenue-maximising price a / (2 b) are printed, and the profit is compared
with (a - b c)^2 / (4 b).
The second difference is exact for a quadratic profit.

Fractions are printed as decimals with ten places. The comparisons are made on the exact values.
"""

from __future__ import annotations

from fractions import Fraction

GRID_STEP = Fraction(1, 10)
CASES = ((120, 1, 20), (90, 3, 10), (200, 4, 5))  # (a, b, c): demand intercept, slope, marginal cost


def demand(price: Fraction, a: int, b: int) -> Fraction:
    """Quantity demanded in units at a price in cents per unit: a - b p."""
    return a - b * price


def profit(price: Fraction, a: int, b: int, c: int) -> Fraction:
    """Monopoly profit in cents: (p - c) (a - b p), for a constant marginal cost c cents per unit."""
    return (price - c) * demand(price, a, b)


def closed_form_price(a: int, b: int, c: int) -> Fraction:
    """The monopoly price (a + b c) / (2 b) in cents per unit, from the first-order condition a - 2 b p + b c = 0."""
    return Fraction(a + b * c, 2 * b)


def elasticity(price: Fraction, a: int, b: int) -> Fraction:
    """The price elasticity of demand -b p / (a - b p), a dimensionless ratio."""
    return -b * price / demand(price, a, b)


def grid_prices(a: int, b: int) -> list[Fraction]:
    """Prices from 0 to the choke price a/b in steps of 1/10 cent."""
    last = int(Fraction(a, b) * 10)
    return [Fraction(k, 10) for k in range(last + 1)]


def main() -> None:
    """Print Parts A, B and C for the three cases. Each line is a fixed label or a number."""
    print("Part A: grid search of the monopoly profit in steps of 1/10 cent, against the closed form")
    for a, b, c in CASES:
        best = max(grid_prices(a, b), key=lambda p: profit(p, a, b, c))
        closed = closed_form_price(a, b, c)
        print(
            f"case a {a} b {b} c {c} grid_argmax {float(best):.10f} closed_form {float(closed):.10f} "
            f"agree {best == closed}"
        )

    print("Part B: Lerner index at the monopoly price against 1/|elasticity|")
    for a, b, c in CASES:
        p_m = closed_form_price(a, b, c)
        lerner = (p_m - c) / p_m
        inverse_abs_elasticity = 1 / abs(elasticity(p_m, a, b))
        print(
            f"case a {a} b {b} c {c} lerner_index {float(lerner):.10f} "
            f"inverse_abs_elasticity {float(inverse_abs_elasticity):.10f} "
            f"equal {lerner == inverse_abs_elasticity}"
        )

    print("Part C: quantity, profit, slope and curvature of the profit at the monopoly price")
    for a, b, c in CASES:
        p_m = closed_form_price(a, b, c)
        quantity = demand(p_m, a, b)
        slope = (profit(p_m + GRID_STEP, a, b, c) - profit(p_m - GRID_STEP, a, b, c)) / (2 * GRID_STEP)
        curvature = (profit(p_m + GRID_STEP, a, b, c) - 2 * profit(p_m, a, b, c) + profit(p_m - GRID_STEP, a, b, c)) / (
            GRID_STEP * GRID_STEP
        )
        revenue_price = Fraction(a, 2 * b)
        print(
            f"case a {a} b {b} c {c} quantity {float(quantity):.10f} profit_cents {float(profit(p_m, a, b, c)):.10f} "
            f"slope_at_optimum {float(slope):.10f} second_difference {float(curvature):.10f} "
            f"monopoly_minus_revenue_price {float(p_m - revenue_price):.10f} "
            f"half_cost {p_m - revenue_price == Fraction(c, 2)} "
            f"profit_closed_form {profit(p_m, a, b, c) == Fraction((a - b * c) ** 2, 4 * b)}"
        )


main()
