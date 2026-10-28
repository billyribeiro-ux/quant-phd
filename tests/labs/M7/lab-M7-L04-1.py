"""M7 lab L04: the dual function, weak duality and the duality gap for the two-asset problem of Lesson 3's lab.

The primal problem is minimize f(w) = (1/2) w'Sigma w - mu'w over w in R^2, subject to 1'w = 1 and
w >= 0, with the active instance mu = (3/2, 1/5) and Sigma = [[2, 1], [1, 2]] from Lesson 3's lab. These are
illustrative inputs, SIMULATED and not market data, in one period with no annualization.

For lambda >= 0 and any nu, the Lagrangian is L(w, lambda, nu) = (1/2) w'Sigma w - r'w - nu with
r = mu + lambda - nu 1. Minimizing over w gives the dual function
g(lambda, nu) = -(1/2) r'Sigma^{-1} r - nu, which this lab evaluates in closed form.

Every value is an exact fractions.Fraction. The lab checks weak duality, g <= f, on a finite grid of
dual points and feasible primal points, and it reports the grid's duality gap. Because the arithmetic is
exact, the grid results are exact statements about the grid. The grid gap bounds the true gap from above
(Proposition 1.4 on the page), and weak duality bounds it from below by zero, so the printed zero grid gap
settles the true gap for this instance. The zero gap at the KKT point is Proposition 2.1 on the page.

Standard library only. No randomness and no network.
"""

from __future__ import annotations

from fractions import Fraction

Vector = tuple[Fraction, Fraction]

SIGMA: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]] = (
    (Fraction(2), Fraction(1)),
    (Fraction(1), Fraction(2)),
)
MU: Vector = (Fraction(3, 2), Fraction(1, 5))
DET = SIGMA[0][0] * SIGMA[1][1] - SIGMA[0][1] * SIGMA[1][0]
SIGMA_INV: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]] = (
    (SIGMA[1][1] / DET, -SIGMA[0][1] / DET),
    (-SIGMA[1][0] / DET, SIGMA[0][0] / DET),
)
DUAL_STEPS = 10
PRIMAL_STEPS = 20


def quad(m: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]], v: Vector) -> Fraction:
    """The quadratic form v'm v for a 2 by 2 matrix m."""
    return v[0] * (m[0][0] * v[0] + m[0][1] * v[1]) + v[1] * (m[1][0] * v[0] + m[1][1] * v[1])


def primal(w: Vector) -> Fraction:
    """The primal objective f(w) = (1/2) w'Sigma w - mu'w."""
    return Fraction(1, 2) * quad(SIGMA, w) - (MU[0] * w[0] + MU[1] * w[1])


def dual(lam: Vector, nu: Fraction) -> Fraction:
    """The dual function g(lambda, nu) = -(1/2) r'Sigma^{-1} r - nu, with r = mu + lambda - nu 1."""
    r = (MU[0] + lam[0] - nu, MU[1] + lam[1] - nu)
    return -Fraction(1, 2) * quad(SIGMA_INV, r) - nu


def dual_grid() -> list[tuple[Vector, Fraction]]:
    """Points (lambda, nu) with lambda_i in {0, 1/10, ..., 1} and nu in {-1, -9/10, ..., 0}."""
    lams = [Fraction(j, DUAL_STEPS) for j in range(DUAL_STEPS + 1)]
    nus = [Fraction(j - DUAL_STEPS, DUAL_STEPS) for j in range(DUAL_STEPS + 1)]
    return [((a, b), nu) for a in lams for b in lams for nu in nus]


def primal_grid() -> list[Vector]:
    """Feasible points (k/20, 1 - k/20) for k = 0..20, which satisfy 1'w = 1 and w >= 0."""
    return [(Fraction(k, PRIMAL_STEPS), Fraction(PRIMAL_STEPS - k, PRIMAL_STEPS)) for k in range(PRIMAL_STEPS + 1)]


def main() -> None:
    print("primal: minimize (1/2) w'Sigma w - mu'w, with Sigma = [[2, 1], [1, 2]], mu = (3/2, 1/5)")
    print("subject to 1'w = 1 and w >= 0 (exact fractions)")
    duals = dual_grid()
    primals = primal_grid()
    print(
        f"dual grid: lambda_1, lambda_2 in steps of 1/{DUAL_STEPS} on [0, 1] and nu in steps of 1/{DUAL_STEPS} "
        f"on [-1, 0]: {len(duals)} dual points"
    )
    print(f"primal grid: w = (k/{PRIMAL_STEPS}, 1 - k/{PRIMAL_STEPS}) for k = 0..{PRIMAL_STEPS}: {len(primals)} points")

    values = [(lam, nu, dual(lam, nu)) for lam, nu in duals]
    prim = [(w, primal(w)) for w in primals]
    holds = sum(g <= f for _, _, g in values for _, f in prim)
    total = len(values) * len(prim)
    print(f"weak duality g(lambda, nu) <= f(w) on the grid: {holds} of {total} pairs")

    best_lam, best_nu, best_g = max(values, key=lambda t: t[2])
    attaining = sum(1 for _, _, g in values if g == best_g)
    print(f"largest dual value on the grid: {best_g} at lambda = ({best_lam[0]}, {best_lam[1]}), nu = {best_nu}")
    print(f"dual grid points attaining that value: {attaining}")

    best_w, best_f = min(prim, key=lambda t: t[1])
    print(f"smallest primal objective on the grid: {best_f} at w = ({best_w[0]}, {best_w[1]})")
    print(f"grid duality gap (smallest primal minus largest dual): {best_f - best_g}")

    test_point = (Fraction(1, 2), Fraction(1, 2))
    print(
        "point (1/2, 1/2), with both inequality constraints strict and the budget exact: "
        f"{test_point[0] > 0 and test_point[1] > 0 and test_point[0] + test_point[1] == 1}"
    )
    print(f"dual value at lambda = (0, 0), nu = 0 (no multipliers): {dual((Fraction(0), Fraction(0)), Fraction(0))}")

    kkt_lam: Vector = (Fraction(0), Fraction(3, 10))
    kkt_nu = Fraction(-1, 2)
    kkt_w: Vector = (Fraction(1), Fraction(0))
    print(
        "KKT point: dual value at (lambda*, nu*) equals the primal value at w* = (1, 0): "
        f"{dual(kkt_lam, kkt_nu) == primal(kkt_w) == Fraction(-1, 2)}"
    )


main()
