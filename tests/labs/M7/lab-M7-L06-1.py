"""M7 L06 lab 1: the efficient frontier as a quadratic program, with and without the short-sale constraint.

SIMULATED: every input is generated from the fixed seed SEED below by an integer recurrence. Nothing here is
market data, and the four assets are labelled A1 to A4 only.

For one period, the inputs are a return vector mu (exact fractions) and a covariance-type matrix Sigma that is
given, not estimated (estimation is outside this unit). Sigma = M'M/16 + I/10 with M a 4 by 4 integer matrix, so
Sigma is symmetric positive definite. For a risk-aversion parameter gamma > 0 the portfolio solves

    minimise (gamma/2) w'Sigma w - mu'w   subject to  1'w = 1,

and the second case adds w >= 0. Every number is a fractions.Fraction, so each equality printed as True is exact.

Part A: no sign constraint. The KKT system [[gamma Sigma, 1], [1', 0]] [w; lambda] = [mu; 1] is solved exactly, and the
result is compared with the closed form w = (a - lambda b)/gamma, where a = Sigma^{-1} mu, b = Sigma^{-1} 1 and
lambda = (1'a - gamma)/(1'b).

Part B: with w >= 0. Each set S of assets fixed at zero (16 sets) gives a reduced equality problem on the other
assets. A candidate is kept only if its free weights are nonnegative and the multiplier nu_i = gamma (Sigma w)_i -
mu_i + lambda is nonnegative for each i in S. The number of kept candidates and the number of distinct weight
vectors among them are printed.

Part C: the variance w'Sigma w of the solution is checked to be nonincreasing in gamma for both cases, and the
constrained objective is checked to be at least the unconstrained objective at each gamma (the feasible set is
smaller).

Part D: turnover against the equal-weight portfolio w0 = (1/4, ..., 1/4), with the linear form: a vector t with
t_i >= w_i - w0_i and t_i >= w0_i - w_i has sum t_i >= sum |w_i - w0_i|, with equality at t_i = |w_i - w0_i|.

Money: none. CU is not used; the weights are fractions of wealth.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import pairwise, product

SEED = 2026
N_ASSETS = 4
GAMMAS = (Fraction(1), Fraction(2), Fraction(4), Fraction(8), Fraction(16))


class Lcg:
    """A linear congruential generator with fixed constants; integer output, so every run is identical."""

    def __init__(self, seed: int) -> None:
        self.state = seed

    def draw(self, modulus: int) -> int:
        """The next integer in 0 to modulus minus 1."""
        self.state = (1103515245 * self.state + 12345) % 2**31
        return self.state % modulus


def simulate_inputs() -> tuple[list[list[Fraction]], list[Fraction], list[list[Fraction]]]:
    """Return (M, mu, Sigma) generated from SEED: M has integers in -3..3, mu is in 0.02..0.14 per period."""
    gen = Lcg(SEED)
    m = [[Fraction(gen.draw(7) - 3) for _ in range(N_ASSETS)] for _ in range(N_ASSETS)]
    mu = [Fraction(gen.draw(13) + 2, 100) for _ in range(N_ASSETS)]
    sigma = [
        [
            sum((m[k][i] * m[k][j] for k in range(N_ASSETS)), Fraction(0)) / 16
            + (Fraction(1, 10) if i == j else Fraction(0))
            for j in range(N_ASSETS)
        ]
        for i in range(N_ASSETS)
    ]
    return m, mu, sigma


def solve(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    """Solve matrix x = rhs exactly by Gaussian elimination with row pivoting; raise ValueError if singular."""
    n = len(rhs)
    rows = [[*row, rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if rows[r][col] != 0), None)
        if pivot is None:
            raise ValueError("the matrix is singular")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(n):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[col], strict=True)]
    return [rows[i][n] / rows[i][i] for i in range(n)]


def dot(u: list[Fraction], v: list[Fraction]) -> Fraction:
    """The inner product u'v, exact."""
    return sum((a * b for a, b in zip(u, v, strict=True)), Fraction(0))


def matvec(a: list[list[Fraction]], v: list[Fraction]) -> list[Fraction]:
    """The product a v, exact."""
    return [dot(row, v) for row in a]


def submatrix(a: list[list[Fraction]], idx: list[int]) -> list[list[Fraction]]:
    """The rows and columns of a with indices in idx."""
    return [[a[i][j] for j in idx] for i in idx]


def equality_frontier_point(
    sigma: list[list[Fraction]], mu: list[Fraction], gamma: Fraction, idx: list[int]
) -> tuple[list[Fraction], Fraction]:
    """Minimiser over the assets in idx with budget 1'w = 1, and its multiplier lambda, from the KKT system."""
    k = len(idx)
    sub_s = submatrix(sigma, idx)
    kkt = [[gamma * sub_s[i][j] for j in range(k)] + [Fraction(1)] for i in range(k)]
    kkt.append([Fraction(1)] * k + [Fraction(0)])
    rhs = [mu[i] for i in idx] + [Fraction(1)]
    sol = solve(kkt, rhs)
    return sol[:k], sol[k]


def closed_form(sigma: list[list[Fraction]], mu: list[Fraction], gamma: Fraction) -> list[Fraction]:
    """The same minimiser from the closed form (a - lambda b)/gamma, with a = Sigma^{-1} mu and b = Sigma^{-1} 1."""
    ones = [Fraction(1)] * N_ASSETS
    a = solve(sigma, mu)
    b = solve(sigma, ones)
    lam = (sum(a, Fraction(0)) - gamma) / sum(b, Fraction(0))
    return [(a[i] - lam * b[i]) / gamma for i in range(N_ASSETS)]


def variance(sigma: list[list[Fraction]], w: list[Fraction]) -> Fraction:
    """w'Sigma w, exact."""
    return dot(w, matvec(sigma, w))


def objective(sigma: list[list[Fraction]], mu: list[Fraction], gamma: Fraction, w: list[Fraction]) -> Fraction:
    """(gamma/2) w'Sigma w - mu'w, exact."""
    return gamma / 2 * variance(sigma, w) - dot(mu, w)


def nonnegative_candidates(
    sigma: list[list[Fraction]], mu: list[Fraction], gamma: Fraction
) -> list[tuple[tuple[int, ...], list[Fraction]]]:
    """Every active set fixed at zero whose candidate passes primal and dual checks, as (zero set, weights)."""
    kept: list[tuple[tuple[int, ...], list[Fraction]]] = []
    for mask in product((0, 1), repeat=N_ASSETS):
        zeros = [i for i in range(N_ASSETS) if mask[i]]
        free = [i for i in range(N_ASSETS) if not mask[i]]
        if not free:
            continue
        w_free, lam = equality_frontier_point(sigma, mu, gamma, free)
        w = [Fraction(0)] * N_ASSETS
        for pos, value in zip(free, w_free, strict=True):
            w[pos] = value
        sw = matvec(sigma, w)
        nu = [gamma * sw[i] - mu[i] + lam for i in range(N_ASSETS)]
        if all(v >= 0 for v in w) and all(nu[i] >= 0 for i in zeros):
            kept.append((tuple(zeros), w))
    return kept


def main() -> None:
    """Print the simulated inputs, both frontiers, the monotonicity and inequality checks, and the turnover check."""
    _m, mu, sigma = simulate_inputs()
    print("lab M7 L06 1, SIMULATED inputs from a fixed seed, one period, no random draws")
    print("mu " + " ".join(str(v) for v in mu))
    print("sigma_diagonal " + " ".join(str(sigma[i][i]) for i in range(N_ASSETS)))
    print(f"sigma_symmetric {all(sigma[i][j] == sigma[j][i] for i in range(N_ASSETS) for j in range(N_ASSETS))}")
    print("part_a equality_only gamma return variance objective budget_exact kkt_matches_closed_form")
    eq_vars: list[Fraction] = []
    eq_objs: list[Fraction] = []
    for gamma in GAMMAS:
        w, _ = equality_frontier_point(sigma, mu, gamma, list(range(N_ASSETS)))
        closed = closed_form(sigma, mu, gamma)
        budget = sum(w, Fraction(0)) == 1
        same = w == closed
        ret, var, obj = dot(mu, w), variance(sigma, w), objective(sigma, mu, gamma, w)
        eq_vars.append(var)
        eq_objs.append(obj)
        print(f"equality {float(gamma):g} {float(ret):.6f} {float(var):.6f} {float(obj):.6f} {budget} {same}")
        print("equality_weights " + " ".join(f"{float(v):.6f}" for v in w))

    print("part_b nonneg gamma zero_set candidates_passing distinct_points return variance objective")
    nn_vars: list[Fraction] = []
    nn_objs: list[Fraction] = []
    for gamma, eq_obj in zip(GAMMAS, eq_objs, strict=True):
        kept = nonnegative_candidates(sigma, mu, gamma)
        distinct = {tuple(w) for _, w in kept}
        best = min(kept, key=lambda item: objective(sigma, mu, gamma, item[1]))
        zeros, w = best
        ret, var, obj = dot(mu, w), variance(sigma, w), objective(sigma, mu, gamma, w)
        nn_vars.append(var)
        nn_objs.append(obj)
        label = "{" + ",".join(f"A{i + 1}" for i in zeros) + "}"
        print(
            f"nonneg {float(gamma):g} {label} {len(kept)} {len(distinct)} "
            f"{float(ret):.6f} {float(var):.6f} {float(obj):.6f}"
        )
        print("nonneg_weights " + " ".join(f"{float(v):.6f}" for v in w))
        print(f"nonneg_objective_at_least_equality {obj >= eq_obj}")

    def nonincreasing(values: list[Fraction]) -> bool:
        return all(later <= earlier for earlier, later in pairwise(values))

    print(f"variance_nonincreasing_in_gamma equality {nonincreasing(eq_vars)} nonneg {nonincreasing(nn_vars)}")

    w0 = [Fraction(1, N_ASSETS)] * N_ASSETS
    _, w = min(nonnegative_candidates(sigma, mu, GAMMAS[2]), key=lambda item: objective(sigma, mu, GAMMAS[2], item[1]))
    diff = [w[i] - w0[i] for i in range(N_ASSETS)]
    turnover = sum((abs(d) for d in diff), Fraction(0))
    t_star = [abs(d) for d in diff]
    feasible = all(t_star[i] >= diff[i] and t_star[i] >= -diff[i] for i in range(N_ASSETS))
    print(f"turnover_at_gamma 4 {float(turnover):.6f} linear_form_feasible {feasible}")
    print(f"linear_form_sum_equals_turnover {sum(t_star, Fraction(0)) == turnover}")
    gen = Lcg(SEED + 1)
    bigger = 0
    for _ in range(20):
        extra = [Fraction(gen.draw(5), 100) for _ in range(N_ASSETS)]
        t = [t_star[i] + extra[i] for i in range(N_ASSETS)]
        ok = all(t[i] >= diff[i] and t[i] >= -diff[i] for i in range(N_ASSETS))
        bigger += ok and sum(t, Fraction(0)) >= turnover
    print(f"feasible_perturbations_at_least_turnover {bigger} of 20")


main()
