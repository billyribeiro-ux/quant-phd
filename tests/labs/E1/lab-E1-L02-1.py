"""E1 lab L02: the profit-maximising output of a price-taking firm, on a grid, against the closed form.

Standard library only (fractions, math). No randomness and no network. The cost of output q is
C(q) = F + c q + k q^2, with fixed cost F >= 0, unit cost c >= 0 and k > 0, in the currency unit of the
example. For price p the profit is pi(q) = p q - C(q). The lab evaluates pi exactly on the grid
q = j / 12 for j = 0 to 72 (outputs 0 to 6) and reports the grid maximiser. It compares that maximiser with the
closed form q* = (p - c) / (2 k), the output at which price equals marginal cost MC(q) = c + 2 k q. Every case
has q* on the grid. The lab also computes the profit at q = 0 (shutdown, profit -F), and it checks that cases
1 and 4 differ only in F and so have the same grid output. Last, for case 1 it computes the profit at sqrt(F/k),
the output that minimises average cost C(q) / q, in floating point to four decimals, and compares it with the
profit at q*. The check is finite: it tests these cases only, and the proof for every input is on the page.
"""

from __future__ import annotations

import math
from fractions import Fraction

STEPS_PER_UNIT = 12  # grid spacing 1 / 12 of a unit of output
MAX_OUTPUT_STEP = 72  # grid points j = 0 to 72, that is outputs 0 to 6


def cost(q: Fraction, fixed: Fraction, c: Fraction, k: Fraction) -> Fraction:
    """Total cost C(q) = F + c q + k q^2 of output q >= 0."""
    return fixed + c * q + k * q * q


def profit(q: Fraction, p: Fraction, fixed: Fraction, c: Fraction, k: Fraction) -> Fraction:
    """Profit pi(q) = p q - C(q) of a firm that takes the price p as given."""
    return p * q - cost(q, fixed, c, k)


def closed_form(p: Fraction, c: Fraction, k: Fraction) -> Fraction:
    """The profit-maximising output q* = (p - c) / (2 k) when p >= c and k > 0."""
    return (p - c) / (2 * k)


def marginal_cost(q: Fraction, c: Fraction, k: Fraction) -> Fraction:
    """Marginal cost MC(q) = dC/dq = c + 2 k q."""
    return c + 2 * k * q


def grid_optimum(p: Fraction, fixed: Fraction, c: Fraction, k: Fraction) -> tuple[int, Fraction, Fraction]:
    """Index, output and profit of the grid point with the largest profit."""
    best_j, best_q, best_pi = 0, Fraction(0), None
    for j in range(MAX_OUTPUT_STEP + 1):
        q = Fraction(j, STEPS_PER_UNIT)
        pi = profit(q, p, fixed, c, k)
        if best_pi is None or pi > best_pi:
            best_j, best_q, best_pi = j, q, pi
    assert best_pi is not None
    return best_j, best_q, best_pi


CASES = (
    # (p, c, k, F): the reference case
    (Fraction(10), Fraction(2), Fraction(1), Fraction(12)),
    (Fraction(7), Fraction(3), Fraction(1, 2), Fraction(5)),
    (Fraction(9), Fraction(1), Fraction(3), Fraction(0)),
    (Fraction(10), Fraction(2), Fraction(1), Fraction(100)),
)


def main() -> None:
    print(f"grid: outputs j / {STEPS_PER_UNIT} for j = 0 to {MAX_OUTPUT_STEP}, so outputs 0 to 6")
    for n, (p, c, k, fixed) in enumerate(CASES, start=1):
        qs = closed_form(p, c, k)
        j, q_grid, pi_grid = grid_optimum(p, fixed, c, k)
        pi_star = profit(qs, p, fixed, c, k)
        print(f"case {n}: p={p}, c={c}, k={k}, F={fixed}: closed form q*={qs}, profit {pi_star}")
        print(f"  grid maximiser: j={j}, q={q_grid}, profit {pi_grid}; equals closed form: {q_grid == qs}")
        print(f"  price equals marginal cost at q*: {marginal_cost(qs, c, k) == p}")
        print(
            f"  shutdown profit -F = {profit(Fraction(0), p, fixed, c, k)}; producing q* is better: "
            f"{pi_star > profit(Fraction(0), p, fixed, c, k)}"
        )
    fixed_cost_changed = grid_optimum(CASES[3][0], CASES[3][3], CASES[3][1], CASES[3][2])[1]
    base = grid_optimum(CASES[0][0], CASES[0][3], CASES[0][1], CASES[0][2])[1]
    print(
        f"cases 1 and 4 differ only in F (12 and 100): grid output {base} and {fixed_cost_changed}, "
        f"equal: {base == fixed_cost_changed}"
    )
    p, c, k, fixed = CASES[0]
    q_avg = math.sqrt(float(fixed / k))
    pi_avg = float(p) * q_avg - (float(fixed) + float(c) * q_avg + float(k) * q_avg * q_avg)
    print(
        f"case 1 at the minimum-average-cost output sqrt(F/k) = {q_avg:.4f}: profit {pi_avg:.4f}, "
        f"below the profit {float(profit(closed_form(p, c, k), p, fixed, c, k)):.4f} at q*"
    )


main()
