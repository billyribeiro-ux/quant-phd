"""E3 lesson L05 lab: two-period Epstein-Zin values, checked against CRRA expected utility.

Standard library only (fractions, math). No randomness and no network: every case is fixed, so
the output is the same on every run. Consumption is a number of units of one good, and every value
is a dimensionless number. Exact cases use fractions.Fraction. Other cases use floats, and the
output prints them to at most four decimals or as True or False against a stated tolerance.

Formulas (Definition 1.1 and Theorem 1.3 of the lesson):
    a = 1 - 1/psi                       (psi > 0, psi != 1)
    CE1 = (sum_s p_s c1_s^(1-gamma))^(1/(1-gamma))     (gamma != 1)
    V0 = ((1-beta) c0^a + beta CE1^a)^(1/a)
CRRA expected utility of the same plan, with u(c) = c^(1-gamma)/(1-gamma):
    U = (1-beta) u(c0) + beta sum_s p_s u(c1_s)
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Sequence
from fractions import Fraction

Num = Fraction | float
Plan = Sequence[tuple[Num, Num]]  # (probability, consumption at date 1) for each state


def power(base: Num, exponent: Num) -> Num:
    """base ** exponent: exact when base is a Fraction and the exponent is a whole number."""
    if isinstance(exponent, int) or (isinstance(exponent, Fraction) and exponent.denominator == 1):
        return base ** int(exponent)
    return math.pow(float(base), float(exponent))


def crra_ce(plan: Plan, gamma: Num) -> Num:
    """CRRA certainty equivalent CE1 of the date-1 lottery plan, for positive consumption and gamma != 1."""
    if gamma == 1:
        raise ValueError("gamma = 1 is outside the power form")
    mean_power: Num = sum((p * power(c, 1 - gamma) for p, c in plan), Fraction(0))
    return power(mean_power, 1 / (1 - gamma))


def crra_utility(c: Num, gamma: Num) -> Num:
    """CRRA utility u(c) = c^(1-gamma) / (1-gamma), for c > 0 and gamma != 1."""
    return power(c, 1 - gamma) / (1 - gamma)


def ez_value(c0: Num, plan: Plan, beta: Num, gamma: Num, psi: Num) -> Num:
    """Two-period Epstein-Zin value V0 of a plan: sure consumption c0 and a date-1 lottery."""
    if psi == 1:
        raise ValueError("psi = 1 is outside this formula: the exponent a = 1 - 1/psi is zero")
    a = 1 - 1 / psi
    bracket = (1 - beta) * power(c0, a) + beta * power(crra_ce(plan, gamma), a)
    return power(bracket, 1 / a)


def crra_eu(c0: Num, plan: Plan, beta: Num, gamma: Num) -> Num:
    """CRRA expected utility of the same plan: discounted sum of u(c0) and the expected u(c1)."""
    expected_u1: Num = sum((p * crra_utility(c, gamma) for p, c in plan), Fraction(0))
    return (1 - beta) * crra_utility(c0, gamma) + beta * expected_u1


def theta(gamma: Num, psi: Num) -> Num:
    """The exponent ratio theta = (1-gamma)/(1-1/psi); theta equals 1 exactly when psi = 1/gamma."""
    return (1 - gamma) / (1 - 1 / psi)


def mrs_numeric(c0: float, c1: float, beta: float, psi: float, h: float = 1e-6) -> float:
    """MRS = (dV0/dc0)/(dV0/dc1) for a deterministic plan, by central differences of ez_value."""

    def value(x: float, y: float) -> float:
        result = ez_value(x, [(1.0, y)], beta, 2.0, psi)
        return float(result)

    dv_dc0 = (value(c0 * (1 + h), c1) - value(c0 * (1 - h), c1)) / (2 * c0 * h)
    dv_dc1 = (value(c0, c1 * (1 + h)) - value(c0, c1 * (1 - h))) / (2 * c1 * h)
    return dv_dc0 / dv_dc1


def eis_numeric(c0: float, c1: float, beta: float, psi: float) -> float:
    """EIS = d ln(c1/c0) / d ln MRS, estimated over c1 in [0.999, 1.001] times c1."""
    lo, hi = 0.999 * c1, 1.001 * c1
    numerator = math.log(hi / c0) - math.log(lo / c0)
    denominator = math.log(mrs_numeric(c0, hi, beta, psi)) - math.log(mrs_numeric(c0, lo, beta, psi))
    return numerator / denominator


def main() -> None:
    beta = Fraction(9, 10)
    gamma = Fraction(2)
    psi = Fraction(1, 2)
    c0 = Fraction(2)
    tree: list[tuple[Fraction, Fraction]] = [(Fraction(1, 2), Fraction(1)), (Fraction(1, 2), Fraction(4))]

    v0 = ez_value(c0, tree, beta, gamma, psi)
    u = crra_eu(c0, tree, beta, gamma)
    ce1 = crra_ce(tree, gamma)
    mean1 = sum((p * c for p, c in tree), Fraction(0))
    print("exact tree: gamma = 2, psi = 1/2, beta = 9/10, c0 = 2, c1 = 1 or 4 with probability 1/2 each")
    print(f"EZ value V0 = {v0}")
    print(f"CRRA expected utility U = {u}")
    print(f"(1 - gamma) U equals V0 ** (1 - gamma): {(1 - gamma) * u == power(v0, 1 - gamma)}")
    print(f"theta = (1 - gamma)/(1 - 1/psi) = {theta(gamma, psi)}")
    print(f"mean of c1 = {mean1}; CRRA certainty equivalent CE1 = {ce1}")
    sure = ez_value(c0, [(Fraction(1), ce1)], beta, gamma, psi)
    print(f"EZ value of the sure plan with c1 = CE1: {sure}; equal to V0: {sure == v0}")
    try:
        ez_value(c0, tree, beta, gamma, Fraction(1))
    except ValueError as err:
        print(f"psi = 1 is refused: {err}")

    plans: list[list[tuple[Fraction, Fraction]]] = [
        [(Fraction(1, 2), Fraction(1)), (Fraction(1, 2), Fraction(4))],
        [(Fraction(1, 4), Fraction(1)), (Fraction(3, 4), Fraction(3))],
        [(Fraction(1), Fraction(2))],
        [(Fraction(1, 3), Fraction(1)), (Fraction(2, 3), Fraction(5))],
    ]
    values = [ez_value(c0, p, beta, gamma, psi) for p in plans]
    utilities = [crra_eu(c0, p, beta, gamma) for p in plans]
    order_v = sorted(range(len(plans)), key=lambda i: values[i])
    order_u = sorted(range(len(plans)), key=lambda i: utilities[i])
    print(f"ranking of four plans by V0 equals ranking by U: {order_v == order_u}")

    risky_float: list[tuple[float, float]] = [(0.5, 1.0), (0.5, 4.0)]
    for g in (0.5, 2.0, 3.0):
        ce_g = float(crra_ce(risky_float, g))
        print(f"risky tree with gamma = {g}: CE1 = {ce_g:.4f}")
    gamma_grid = (0.5, 2.0, 3.0)
    ces = [float(crra_ce(risky_float, g)) for g in gamma_grid]
    print(f"CE1 falls as gamma rises over this grid: {all(a > b for a, b in itertools.pairwise(ces))}")

    worst_gap = 0.0
    for g in (0.5, 2.0, 3.0):
        fplan: list[tuple[float, float]] = [(0.3, 0.5), (0.7, 3.0)]
        vf = float(ez_value(1.5, fplan, 0.95, g, 1.0 / g))
        uf = float(crra_eu(1.5, fplan, 0.95, g))
        lhs = (1 - g) * uf
        rhs = float(power(vf, 1 - g))
        worst_gap = max(worst_gap, abs(lhs - rhs) / abs(rhs))
    print(f"psi = 1/gamma identity holds to 1e-12 relative for gamma in 0.5, 2, 3: {worst_gap < 1e-12}")

    sure_values = [float(ez_value(2.0, [(1.0, 4.0)], 0.9, g, 0.5)) for g in (0.5, 2.0, 3.0)]
    same = all(math.isclose(v, sure_values[0], rel_tol=1e-12) for v in sure_values)
    print(f"deterministic plan: EZ value the same for gamma 0.5, 2, 3 at psi = 1/2: {same}")

    eu_a = float(crra_eu(4.0, [(1.0, 4.0)], 0.5, 2.0))
    eu_b = float(crra_eu(1.0, [(1.0, 10.0)], 0.5, 2.0))
    ez_a = float(ez_value(4.0, [(1.0, 4.0)], 0.5, 2.0, 2.0))
    ez_b = float(ez_value(1.0, [(1.0, 10.0)], 0.5, 2.0, 2.0))
    print(f"gamma = 2, psi = 2, beta = 1/2: U(4, 4) = {eu_a:.4f}, U(1, 10) = {eu_b:.4f}")
    print(f"same gamma and psi: V0(4, 4) = {ez_a:.4f}, V0(1, 10) = {ez_b:.4f}")
    print(f"CRRA expected utility ranks (4, 4) above (1, 10): {eu_a > eu_b}")
    print(f"Epstein-Zin ranks (1, 10) above (4, 4): {ez_b > ez_a}")

    for psi_f in (0.5, 2.0, 0.25):
        eis = eis_numeric(2.0, 4.0, 0.9, psi_f)
        print(f"psi = {psi_f}: EIS estimate {eis:.4f}")
    analytic = ((1 - 0.9) / 0.9) * (4.0 / 2.0) ** (1 / 0.5)
    numeric = mrs_numeric(2.0, 4.0, 0.9, 0.5)
    print(
        f"MRS at (c0, c1) = (2, 4), psi = 1/2: closed form agrees with the numeric MRS: "
        f"{math.isclose(analytic, numeric, rel_tol=1e-6)}"
    )


main()
