"""E3 L07 lab 1: a probability weighting function, and a dominated pair that the weighted value ranks higher.

Amounts are in currency units (CU). Probabilities are exact fractions. The weighting function, the value of an
outcome and the weighted value are floats, printed to four decimals.

Part A: the weighting function omega(p) = p**eta / (p**eta + (1 - p)**eta)**(1/eta) at eta = 0.5. It prints the
endpoints omega(0) and omega(1) and the values at small and large probabilities beside p itself. On a grid of 1001
equally spaced probabilities it checks that omega is nondecreasing and lies in [0, 1], checks the closed form
sqrt(p) / (1 + 2 sqrt(p (1 - p))) against the formula, and prints the number of sign changes of omega(p) - p and the
last grid point with omega(p) > p.
Part B: two finite lotteries on gains, A and B. The distribution-function test of first-order dominance (the
test of Lesson 4) shows that B dominates A: its distribution function is at or below A's at every outcome,
with strict inequality somewhere.
Part C: the non-cumulative weighted value Gamma(L) = sum over outcomes of omega(p_i) * v(x_i), with v(x) = x**alpha
for gains, at alpha = 1 and alpha = 0.5. It prints Gamma(A) and Gamma(B) and which lottery is ranked higher.
Part D: a finite family of nondecreasing utilities (power functions and step functions). For each one it checks
whether the expected utility of B is at least that of A, prints any utility that ranks A above B, and prints the count.

Standard library only; no randomness and no network access.
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Callable
from fractions import Fraction

ETA = 0.5
ALPHAS: tuple[float, ...] = (1.0, 0.5)
LOTTERY_A: tuple[tuple[int, Fraction], ...] = ((0, Fraction(2, 5)), (50, Fraction(3, 10)), (100, Fraction(3, 10)))
LOTTERY_B: tuple[tuple[int, Fraction], ...] = ((0, Fraction(2, 5)), (100, Fraction(3, 5)))
GRID_POINTS = 1001


def omega(p: float, eta: float = ETA) -> float:
    """Weight of a probability p in [0, 1]: p**eta / (p**eta + (1 - p)**eta)**(1/eta). Dimensionless."""
    if not 0.0 <= p <= 1.0:
        raise ValueError("a probability must lie in [0, 1]")
    return float(p**eta / (p**eta + (1.0 - p) ** eta) ** (1.0 / eta))


def distribution_at(lottery: tuple[tuple[int, Fraction], ...], t: int) -> Fraction:
    """P(X <= t) for a finite lottery given as (outcome in CU, probability) pairs."""
    return sum((p for x, p in lottery if x <= t), Fraction(0))


def dominates_fosd(b: tuple[tuple[int, Fraction], ...], a: tuple[tuple[int, Fraction], ...]) -> tuple[bool, bool]:
    """Return (B first-order dominates A, strictly somewhere): F_B(t) <= F_A(t) at every outcome t of either lottery."""
    points = sorted({x for x, _ in a} | {x for x, _ in b})
    at_or_below = all(distribution_at(b, t) <= distribution_at(a, t) for t in points)
    strict = any(distribution_at(b, t) < distribution_at(a, t) for t in points)
    return at_or_below, strict


def weighted_value(lottery: tuple[tuple[int, Fraction], ...], alpha: float) -> float:
    """Non-cumulative weighted value: sum of omega(p_i) * v(x_i), with v(x) = x**alpha for gains (x >= 0)."""
    return float(sum(omega(float(p)) * float(x) ** alpha for x, p in lottery))


def expected_utility(lottery: tuple[tuple[int, Fraction], ...], u: Callable[[float], float]) -> float:
    """Expected utility sum of p_i * u(x_i) for a utility function u on outcomes in CU."""
    return float(sum(float(p) * u(float(x)) for x, p in lottery))


def part_a() -> None:
    print(f"part A: eta = {ETA:g}; omega(0) = {omega(0.0):.4f}; omega(1) = {omega(1.0):.4f}")
    for p in (0.01, 0.05, 0.3, 0.5, 0.6, 0.95, 0.99):
        side = "above p" if omega(p) > p else "below p"
        print(f"part A: p = {p:<5g} omega(p) = {omega(p):.4f} ({side})")
    grid = [i / (GRID_POINTS - 1) for i in range(GRID_POINTS)]
    values = [omega(p) for p in grid]
    nondecreasing = all(values[i] <= values[i + 1] for i in range(len(values) - 1))
    in_unit = all(0.0 <= v <= 1.0 for v in values)
    print(
        f"part A: on {GRID_POINTS} equally spaced probabilities: nondecreasing = {nondecreasing}, in [0, 1] = {in_unit}"
    )
    closed_gap = max(abs(omega(p) - math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))) for p in grid)
    agrees = "agrees with" if closed_gap < 1e-12 else "differs from"
    print(f"part A: closed form sqrt(p) / (1 + 2 sqrt(p (1 - p))) {agrees} the formula, largest gap {closed_gap:.2e}")
    interior = grid[1:-1]
    above = [omega(p) > p for p in interior]
    changes = sum(1 for a, b in itertools.pairwise(above) if a != b)
    above_points = [p for p in interior if omega(p) > p]
    last_text = "none" if not above_points else f"{max(above_points):.3f}"
    print(
        f"part A: interior grid points: sign changes of omega(p) - p = {changes}; last point with omega(p) > p = "
        f"{last_text}"
    )


def part_b() -> None:
    print("part B: distribution functions F(t) = P(X <= t) at the outcomes")
    for t in (0, 50, 100):
        print(
            f"part B: t = {t:3d}  F_A(t) = {float(distribution_at(LOTTERY_A, t)):.4f}  "
            f"F_B(t) = {float(distribution_at(LOTTERY_B, t)):.4f}"
        )
    at_or_below, strict = dominates_fosd(LOTTERY_B, LOTTERY_A)
    print(f"part B: B first-order dominates A (F_B <= F_A everywhere) = {at_or_below}; strict somewhere = {strict}")


def part_c() -> None:
    for alpha in ALPHAS:
        va = weighted_value(LOTTERY_A, alpha)
        vb = weighted_value(LOTTERY_B, alpha)
        ranked = "A above B" if va > vb else "B at or above A"
        print(f"part C: alpha = {alpha:g}  Gamma(A) = {va:.4f}  Gamma(B) = {vb:.4f}  weighted ranking: {ranked}")


def power_utility(a: float) -> Callable[[float], float]:
    """Utility x**a on outcomes x >= 0; nondecreasing for a > 0."""

    def u(x: float) -> float:
        return float(x**a)

    return u


def step_utility(t: float) -> Callable[[float], float]:
    """Indicator utility 1 if x >= t, else 0; nondecreasing in x."""

    def u(x: float) -> float:
        return 1.0 if x >= t else 0.0

    return u


def part_d() -> None:
    utilities: list[tuple[str, Callable[[float], float]]] = []
    for a in (0.25, 0.5, 1.0, 2.0, 4.0):
        utilities.append((f"x**{a:g}", power_utility(a)))
    for t in (1.0, 50.0, 51.0, 100.0, 101.0):
        utilities.append((f"indicator of x >= {t:g}", step_utility(t)))
    agree = 0
    for name, u in utilities:
        eu_a = expected_utility(LOTTERY_A, u)
        eu_b = expected_utility(LOTTERY_B, u)
        if eu_b >= eu_a:
            agree += 1
        else:
            print(f"part D: utility {name} ranks A above B")
    print(f"part D: nondecreasing utilities with E u(B) >= E u(A): {agree} of {len(utilities)}")


def main() -> None:
    part_a()
    part_b()
    part_c()
    part_d()


main()
