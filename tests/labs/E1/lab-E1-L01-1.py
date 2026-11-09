"""E1 lab L01: the consumer optimum for u(x, y) = x * y on the budget line, against the closed form.

Standard library only (fractions). No randomness and no network. Every number is an exact Fraction and nothing
is rounded. The budget is p_x * x + p_y * y = m with p_x, p_y and m all positive. For each case the lab takes
STEPS = 60 equal steps along the budget line, from x = 0 to x = m / p_x, so grid point 30 is the midpoint of the
line. It reports the grid point with the largest utility, the closed form x_bar = m / (2 p_x), y_bar = m / (2 p_y) and
the marginal rate of substitution y / x at the closed-form bundle, which is the ratio of the marginal utilities
u_x = y and u_y = x. The check is finite: it tests these cases only. The proof that the closed form is the optimum
for every price and income in the Setting (p_x, p_y, m > 0) is on the page.
"""

from __future__ import annotations

from fractions import Fraction

STEPS = 60  # equal steps along the budget line; grid point STEPS // 2 is the midpoint x = m / (2 p_x)


def utility(x: Fraction, y: Fraction) -> Fraction:
    """Utility u(x, y) = x * y for non-negative quantities x and y."""
    return x * y


def budget_y(px: Fraction, py: Fraction, m: Fraction, x: Fraction) -> Fraction:
    """The quantity of good y that exhausts income m when x units of good x are bought."""
    return (m - px * x) / py


def closed_form(px: Fraction, py: Fraction, m: Fraction) -> tuple[Fraction, Fraction]:
    """The optimal bundle x_bar = m / (2 p_x) and y_bar = m / (2 p_y) for u = x * y."""
    return m / (2 * px), m / (2 * py)


def mrs(x: Fraction, y: Fraction) -> Fraction:
    """Marginal rate of substitution of good x for good y: (du/dx) / (du/dy) = y / x, for x > 0."""
    return y / x


def grid_optimum(px: Fraction, py: Fraction, m: Fraction) -> tuple[int, Fraction, Fraction]:
    """Index, x and utility of the grid point on the budget line with the largest utility."""
    best_i, best_x, best_u = 0, Fraction(0), Fraction(-1)
    for i in range(STEPS + 1):
        x = (m / px) * i / STEPS
        u = utility(x, budget_y(px, py, m, x))
        if u > best_u:
            best_i, best_x, best_u = i, x, u
    return best_i, best_x, best_u


CASES = (
    (Fraction(2), Fraction(3), Fraction(120)),
    (Fraction(1), Fraction(1), Fraction(50)),
    (Fraction(5), Fraction(2), Fraction(70)),
    (Fraction(3), Fraction(4), Fraction(60)),
)


def main() -> None:
    print(f"grid: {STEPS + 1} points on the budget line, x from 0 to m / p_x; the midpoint is point {STEPS // 2}")
    for px, py, m in CASES:
        xs, ys = closed_form(px, py, m)
        us = utility(xs, ys)
        i, x_grid, u_grid = grid_optimum(px, py, m)
        y_grid = budget_y(px, py, m, x_grid)
        agrees = i == STEPS // 2 and x_grid == xs and y_grid == ys
        print(f"case p_x={px}, p_y={py}, m={m}: closed form x_bar={xs}, y_bar={ys}, u_bar={us}")
        print(f"  grid maximiser: point {i}, x={x_grid}, y={y_grid}, u={u_grid}; equals closed form: {agrees}")
        print(f"  budget exhausted at x_bar, y_bar: {px * xs + py * ys == m}")
        print(
            f"  MRS y/x at x_bar, y_bar: {mrs(xs, ys)}; price ratio p_x/p_y: {px / py}; equal: {mrs(xs, ys) == px / py}"
        )
    px, py, m = CASES[0]
    x_off = Fraction(20)
    y_off = budget_y(px, py, m, x_off)
    print(
        f"off the optimum, case p_x={px}, p_y={py}, m={m}, at x={x_off}: y={y_off}, "
        f"MRS={mrs(x_off, y_off)}, price ratio {px / py}, equal: {mrs(x_off, y_off) == px / py}"
    )


main()
