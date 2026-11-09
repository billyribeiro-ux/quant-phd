"""Build alt_v12_F1 (float active set, scaled, with refinement) from the reference's validation and certificate code.

The solver core (linear solves, rank, active-set search) is replaced by a float implementation with partial pivoting
and one step of iterative refinement; validation, the turnover sign-form mapping and the certificate are the
reference's. Usage: python -I make_alt_F1.py <repo_root> <output_file>
"""

import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
ref = (repo / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8").splitlines(keepends=True)
start = next(i for i, line in enumerate(ref) if line.startswith("def _solve_linear("))
end = next(i for i, line in enumerate(ref) if line.startswith("def _certificate("))
core = '''def _solve_float(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    """Gaussian elimination with partial pivoting in floats (a pivot below 1e-300 is a singular system)."""
    size = len(rhs)
    rows = [[*matrix[i], rhs[i]] for i in range(size)]
    for col in range(size):
        pivot = max(range(col, size), key=lambda r: abs(rows[r][col]))
        if abs(rows[pivot][col]) < 1e-300:
            raise RuntimeError("singular KKT system")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(size):
            if r != col and rows[r][col] != 0.0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col], strict=True)]
    return [rows[i][size] / rows[i][i] for i in range(size)]


def _rank_float(vectors: list[list[float]], tol: float = 1e-10) -> int:
    rows = [list(v) for v in vectors]
    rank = 0
    width = len(rows[0]) if rows else 0
    for col in range(width):
        pivot = max(range(rank, len(rows)), key=lambda r: abs(rows[r][col]), default=None)
        if pivot is None or abs(rows[pivot][col]) <= tol:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][col] != 0.0:
                factor = rows[r][col] / rows[rank][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[rank], strict=True)]
        rank += 1
    return rank


def _kkt_step(
    hessian: list[list[float]], gradient: list[float], active: list[list[float]]
) -> tuple[list[float], list[float]]:
    """Solve H p + g + A' lambda = 0 and A p = 0, then one step of iterative refinement."""
    n, m = len(gradient), len(active)
    size = n + m
    matrix = [[0.0] * size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = hessian[i][j]
    for k, a in enumerate(active):
        for i in range(n):
            matrix[i][n + k] = a[i]
            matrix[n + k][i] = a[i]
    rhs = [-g for g in gradient] + [0.0] * m
    sol = _solve_float(matrix, rhs)
    residual = [
        rhs[r] - sum(matrix[r][c] * sol[c] for c in range(size)) for r in range(size)
    ]
    correction = _solve_float(matrix, residual)
    sol = [s + c for s, c in zip(sol, correction, strict=True)]
    return sol[:n], sol[n:]


def _inequalities(problem: Problem) -> list[tuple[list[Fraction], Fraction, tuple[object, ...]]]:
    """Rows a.w <= b with a key: lower and upper bounds, sector caps, and the 2**n sign forms of the turnover limit."""
    n = problem.n
    rows: list[tuple[list[Fraction], Fraction, tuple[object, ...]]] = []
    for i in range(n):
        rows.append(([Fraction(-1) if j == i else Fraction(0) for j in range(n)], -problem.lower[i], ("lower", i)))
        rows.append(([Fraction(1) if j == i else Fraction(0) for j in range(n)], problem.upper[i], ("upper", i)))
    for k, cap in enumerate(problem.caps):
        rows.append(([Fraction(1) if problem.sector[j] == k else Fraction(0) for j in range(n)], cap, ("sector", k)))
    for signs in product((1, -1), repeat=n):
        a = [Fraction(s) for s in signs]
        rows.append((a, problem.tau + _dot(a, problem.w0), ("turn", signs)))
    return rows


def _active_set(
    problem: Problem, rows: list[tuple[list[Fraction], Fraction, tuple[object, ...]]]
) -> tuple[list[float], dict[tuple[object, ...], float], float]:
    n = problem.n
    hessian = [[float(problem.gamma * problem.sigma[i][j]) for j in range(n)] for i in range(n)]
    mu = [float(m) for m in problem.mu]
    frows = [([float(v) for v in a], float(b), key) for a, b, key in rows]
    budget = [1.0] * n
    x = [float(v) for v in problem.w0]
    eps = 1e-12
    working: list[int] = []
    for j, (a, b, _) in enumerate(frows):
        slack = b - sum(p * q for p, q in zip(a, x, strict=True))
        if slack <= eps and _rank_float([budget, *(frows[k][0] for k in working), a]) > len(working) + 1:
            working.append(j)
    for _ in range(400):
        gradient = [sum(hessian[i][j] * x[j] for j in range(n)) - mu[i] for i in range(n)]
        p, lam = _kkt_step(hessian, gradient, [budget] + [frows[j][0] for j in working])
        if max(abs(v) for v in p) <= 1e-13:
            negative = [(lam[1 + k], k) for k in range(len(working)) if lam[1 + k] < -1e-12]
            if not negative:
                multipliers = {frows[j][2]: lam[1 + k] for k, j in enumerate(working)}
                return x, multipliers, lam[0]
            working.pop(min(negative)[1])
            continue
        step = 1.0
        blocking: int | None = None
        for j, (a, b, _) in enumerate(frows):
            if j in working:
                continue
            rate = sum(p_ * q for p_, q in zip(a, p, strict=True))
            if rate > 1e-14:
                slack = max(b - sum(p_ * q for p_, q in zip(a, x, strict=True)), 0.0)
                ratio = slack / rate
                if ratio < step:
                    step, blocking = ratio, j
        x = [xi + step * pi for xi, pi in zip(x, p, strict=True)]
        if blocking is not None:
            working.append(blocking)
    raise RuntimeError("the active-set search did not converge")


def _solve(problem: Problem) -> dict[str, Any]:
    n = problem.n
    rows = _inequalities(problem)
    x, mult, budget_mult = _active_set(problem, rows)
    lower = [mult.get(("lower", i), 0.0) for i in range(n)]
    upper = [mult.get(("upper", i), 0.0) for i in range(n)]
    sector = [mult.get(("sector", k), 0.0) for k in range(len(problem.caps))]
    sign_multipliers = {cast(tuple[int, ...], key[1]): value for key, value in mult.items() if key[0] == "turn"}
    kappa = sum(sign_multipliers.values(), 0.0)
    plus = [0.0] * n
    minus = [0.0] * n
    for i in range(n):
        net = sum((eta * s[i] for s, eta in sign_multipliers.items()), 0.0)
        plus[i] = (kappa + net) / 2
        minus[i] = (kappa - net) / 2
    return {
        "w": x,
        "budget": budget_mult,
        "lower": lower,
        "upper": upper,
        "sector": sector,
        "plus": plus,
        "minus": minus,
        "kappa": kappa,
    }


'''
text = "".join(ref[:start]) + core + "".join(ref[end:])
header = "# ALT v12 F1: float active set with partial pivoting and refinement; validation and certificate from the reference.\n"
out.write_text(header + text, encoding="utf-8")
print("wrote", out)
