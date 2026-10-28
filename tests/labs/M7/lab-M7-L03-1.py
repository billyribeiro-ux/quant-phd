"""M7 lab L03: KKT residuals for a two-asset problem with a budget and a non-negativity constraint.

The problem is minimize f(w) = (1/2) w'Sigma w - mu'w over w in R^2, subject to 1'w = 1 and w >= 0.
Sigma is a given symmetric positive-definite matrix and mu a given vector. Both are chosen by hand
for this lab as illustrative inputs, SIMULATED and not market data. The returns are in one period,
with no annualization.

Every number is an exact fractions.Fraction, so each residual is exact and nothing is rounded.
The lab checks the four KKT conditions at a candidate point and its multipliers, and it compares
the candidate with a grid of 101 feasible points. The grid is numerical evidence and not a proof:
the proof that a KKT point is optimal is Theorem 2.1 on the page.

Standard library only. No randomness and no network.
"""

from __future__ import annotations

from fractions import Fraction

Vector = tuple[Fraction, Fraction]

SIGMA: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]] = (
    (Fraction(2), Fraction(1)),
    (Fraction(1), Fraction(2)),
)
GRID_STEPS = 100


def matvec(m: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]], v: Vector) -> Vector:
    """The product m v for a 2 by 2 matrix m and a vector v."""
    return (m[0][0] * v[0] + m[0][1] * v[1], m[1][0] * v[0] + m[1][1] * v[1])


def dot(u: Vector, v: Vector) -> Fraction:
    """The inner product u'v of two vectors in R^2."""
    return u[0] * v[0] + u[1] * v[1]


def objective(w: Vector, mu: Vector) -> Fraction:
    """f(w) = (1/2) w'Sigma w - mu'w, with Sigma from SIGMA."""
    return Fraction(1, 2) * dot(w, matvec(SIGMA, w)) - dot(mu, w)


def kkt_residuals(w: Vector, nu: Fraction, lam: Vector, mu: Vector) -> dict[str, object]:
    """The four KKT residuals at (w, nu, lam) for the budget h(w) = 1'w - 1 and constraints g_i(w) = -w_i.

    Stationarity: grad f + nu * 1 - lam (the gradient of lam_i g_i is -lam_i e_i), a vector.
    Primal: the largest violation of 1'w = 1 and of w_i >= 0, which is 0 when both hold.
    Dual: the largest violation of lam_i >= 0, which is 0 when all multipliers are non-negative.
    Complementary slackness: the largest of |lam_i * w_i|, since g_i(w) = -w_i.
    """
    grad = (matvec(SIGMA, w)[0] - mu[0], matvec(SIGMA, w)[1] - mu[1])
    stationarity = (grad[0] + nu - lam[0], grad[1] + nu - lam[1])
    primal = max(abs(w[0] + w[1] - 1), max(-w[0], Fraction(0)), max(-w[1], Fraction(0)))
    dual = max(-lam[0], -lam[1], Fraction(0))
    slack = max(abs(lam[0] * w[0]), abs(lam[1] * w[1]))
    exact = stationarity == (Fraction(0), Fraction(0)) and primal == 0 and dual == 0 and slack == 0
    return {
        "stationarity": stationarity,
        "primal": primal,
        "dual": dual,
        "slack": slack,
        "holds exactly": exact,
    }


def grid_minimum(mu: Vector) -> tuple[Fraction, Fraction]:
    """The smallest objective over w = (k/N, 1 - k/N) for k = 0..N, and the w1 that attains it."""
    best_w1 = Fraction(0)
    best = objective((Fraction(0), Fraction(1)), mu)
    for k in range(GRID_STEPS + 1):
        w1 = Fraction(k, GRID_STEPS)
        value = objective((w1, 1 - w1), mu)
        if value < best:
            best, best_w1 = value, w1
    return best, best_w1


def report(label: str, mu: Vector, w: Vector, nu: Fraction, lam: Vector) -> None:
    print(f"{label}: mu = ({mu[0]}, {mu[1]})")
    print(f"  candidate w = ({w[0]}, {w[1]}), nu = {nu}, lambda = ({lam[0]}, {lam[1]})")
    res = kkt_residuals(w, nu, lam, mu)
    s = res["stationarity"]
    assert isinstance(s, tuple)
    print(f"  stationarity residual: ({s[0]}, {s[1]})")
    print(f"  primal residual: {res['primal']}")
    print(f"  dual residual: {res['dual']}")
    print(f"  complementary slackness max |lambda_i w_i|: {res['slack']}")
    print(f"  all four KKT conditions hold exactly: {res['holds exactly']}")
    print(f"  objective at the candidate: {objective(w, mu)}")
    best, best_w1 = grid_minimum(mu)
    print(f"  smallest objective on the {GRID_STEPS + 1} grid points: {best} at w1 = {best_w1}")
    print(f"  the grid minimum equals the candidate objective: {best == objective(w, mu)}")


def main() -> None:
    half = Fraction(1, 2)
    # Active instance: the candidate puts all weight on asset 1, so the constraint w2 >= 0 binds.
    # Stationarity in row 1 gives nu = mu1 - 2 = -1/2; row 2 gives lambda2 = 1 - mu2 + nu = 3/10.
    report(
        "active instance",
        (Fraction(3, 2), Fraction(1, 5)),
        (Fraction(1), Fraction(0)),
        Fraction(-1, 2),
        (Fraction(0), Fraction(3, 10)),
    )
    # Inactive instance: both weights are positive, so the non-negativity multipliers are zero.
    report(
        "inactive instance",
        (Fraction(1), Fraction(1)),
        (half, half),
        Fraction(-1, 2),
        (Fraction(0), Fraction(0)),
    )
    # Two deliberate failures on the active instance, to show what each condition detects.
    active_mu = (Fraction(3, 2), Fraction(1, 5))
    off = kkt_residuals((half, half), Fraction(-1, 2), (Fraction(0), Fraction(3, 10)), active_mu)
    s = off["stationarity"]
    assert isinstance(s, tuple)
    print(f"off-solution point w = (1/2, 1/2) with the active multipliers: stationarity residual ({s[0]}, {s[1]})")
    flipped = kkt_residuals((Fraction(1), Fraction(0)), Fraction(-1, 2), (Fraction(0), Fraction(-3, 10)), active_mu)
    print(f"flipped sign lambda2 = -3/10 at the active candidate: dual residual {flipped['dual']}")


main()
