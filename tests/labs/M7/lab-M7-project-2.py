"""Rung 2 completed solution: the worked example of Lab 1 with its three blanks filled.

SIMULATED three-asset problem, not market data. The objective is (gamma / 2) w' Sigma w - mu' w with gamma = 2, so the
quadratic term is w' Sigma w. The constraints are that the weights sum to one and that each weight is at least
zero. The code imposes no upper limit on a weight; the largest weight at the answer is below one, and step 5 prints it.
Every input is an exact decimal read as a Fraction, so the printed values are exact, except the approximation in step 7.
"""

from fractions import Fraction

# SIMULATED three-asset problem, not market data.
GAMMA = Fraction(2)
SIGMA = [
    [Fraction(4, 100), Fraction(1, 100), Fraction(0)],
    [Fraction(1, 100), Fraction(9, 100), Fraction(2, 100)],
    [Fraction(0), Fraction(2, 100), Fraction(16, 100)],
]
MU = [Fraction(5, 100), Fraction(3, 100), Fraction(-2, 100)]
N = 3


def solve(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    """Solve a square linear system by Gauss-Jordan elimination in exact arithmetic."""
    size = len(rhs)
    rows = [[*matrix[i], rhs[i]] for i in range(size)]
    for col in range(size):
        pivot = next(r for r in range(col, size) if rows[r][col] != 0)
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(size):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col], strict=True)]
    return [rows[i][size] / rows[i][i] for i in range(size)]


def kkt_solution(held_at_zero: list[int]) -> tuple[list[Fraction], Fraction, list[Fraction]]:
    """The weights, the budget multiplier and the lower-bound multipliers, with the listed assets held at zero.

    The unknowns are the N weights, the budget multiplier, and one multiplier per held asset. The equations are the
    stationarity of each weight, the budget, and each held weight equal to zero: as many equations as unknowns.
    """
    size = N + 1 + len(held_at_zero)
    matrix = [[Fraction(0)] * size for _ in range(size)]
    rhs = [Fraction(0)] * size
    for i in range(N):
        for j in range(N):
            matrix[i][j] = GAMMA * SIGMA[i][j]
        matrix[i][N] = Fraction(1)
        for c, j in enumerate(held_at_zero):
            if i == j:
                matrix[i][N + 1 + c] = Fraction(-1)
        rhs[i] = MU[i]
    for j in range(N):
        matrix[N][j] = Fraction(1)
    rhs[N] = Fraction(1)
    for c, j in enumerate(held_at_zero):
        matrix[N + 1 + c][j] = Fraction(1)
    solution = solve(matrix, rhs)
    return solution[:N], solution[N], solution[N + 1 :]


def main() -> None:
    # Step 1. Budget only. Why: without the bounds, the answer shows which bound the optimum would break.
    free, _, _ = kkt_solution([])
    print("step 1 budget-only weights:", [str(w) for w in free])

    # Step 2. Active set. Why: a lower bound is active when the budget-only weight below it is negative.
    held = [i for i in range(N) if free[i] < 0]
    print("step 2 assets held at zero:", held)

    # Step 3. Constrained solution. Why: with the held assets at zero, the remaining equations are linear.
    w, nu, lam = kkt_solution(held)
    print("step 3 weights:", [str(x) for x in w])
    print("step 3 budget multiplier nu:", str(nu))
    print("step 3 lower-bound multipliers of the held assets:", [str(x) for x in lam])

    # Step 4. Stationarity. Why: at the optimum, the gradient plus the multipliers is zero in every weight.
    residual = [GAMMA * sum(SIGMA[i][j] * w[j] for j in range(N)) - MU[i] + nu for i in range(N)]
    for c, j in enumerate(held):
        residual[j] -= lam[c]
    print("step 4 stationarity residuals:", [str(r) for r in residual])

    # Step 5. Primal feasibility. Why: the weights must sum to one; the smallest and largest weight are printed.
    print("step 5 budget gap:", str(sum(w) - 1))
    print("step 5 smallest weight:", str(min(w)), "largest weight:", str(max(w)))

    # Step 6. Dual feasibility and complementary slackness. Why: a bound multiplier is non-negative, and it is zero
    # unless its weight sits on the bound.
    signs = [x >= 0 for x in lam]
    dual_feasible = all(signs)
    print("step 6 lower-bound multipliers non-negative:", dual_feasible)
    print("step 6 weight times multiplier, held assets:", [str(w[j] * lam[c]) for c, j in enumerate(held)])

    # Step 7. Objective at the solution. Why: this is the minimized value of the objective at the answer.
    quadratic = sum(SIGMA[i][j] * w[i] * w[j] for i in range(N) for j in range(N))
    objective = GAMMA / 2 * quadratic - sum(MU[i] * w[i] for i in range(N))
    print("step 7 objective (exact):", str(objective), "approximately", f"{float(objective):.6f}")


main()
