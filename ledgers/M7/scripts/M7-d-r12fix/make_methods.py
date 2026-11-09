"""Write alternatives (2) to (5) of plan 7.4 item 2 from the repaired alternative D.

Usage: python -I make_methods.py <repo_root>

Each file keeps the validation, the certificate and allocate() of alternative D (float arithmetic, gamma folded into the
linear term). Only the search differs: a front end of the named method returns an approximate point and row multipliers;
the rows near-active or with a positive multiplier form a working set; the KKT system on that working set is solved
exactly and returned only if it is feasible and dual feasible (sufficiency of the KKT conditions on the page). If the
check fails, the active-set search of alternative D runs from the starting portfolio, so every returned answer is
verified. LAST_PATH records which path produced the answer.
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
base_path = root / "ledgers/M7/scripts/M7-d-r12fix/alts_repaired/alt_D_r12fix_float_1e-12_gamma_folded_refined.py"
out_dir = root / "ledgers/M7/scripts/M7-d-r12fix/methods"
base = base_path.read_text(encoding="utf-8")

DOC_OLD_START = base.index('"""Reference solution')
DOC_OLD_END = base.index('"""', DOC_OLD_START + 3) + 3
SOLVE_START = base.index("def _solve(problem: Problem)")
CERT_START = base.index("def _certificate(")
SOLVE_BODY_TAIL_MARK = "    lower = [mult.get((\"lower\", i), Fraction(0)) for i in range(n)]"
assert SOLVE_BODY_TAIL_MARK in base or "    lower = [mult.get((\"lower\", i), 0.0) for i in range(n)]" in base
TAIL_MARK = "    lower = [mult.get((\"lower\", i), 0.0) for i in range(n)]"
TAIL_MARK = TAIL_MARK if TAIL_MARK in base else SOLVE_BODY_TAIL_MARK
solve_tail = base[base.index(TAIL_MARK, SOLVE_START) :]

SHARED = '''
LAST_PATH = "none"  # "front-end": the KKT system on the front end's working set was verified; "fallback": active set
ADMM_ITERS = 400
IPM_ITERS = 80
DUAL_ITERS = 2000
PG_OUTER = 20
PG_INNER = 40


def _dotf(a: Sequence[float], x: Sequence[float]) -> float:
    return sum(p * q for p, q in zip(a, x, strict=True))


def _matvec(matrix: list[list[float]], v: Sequence[float]) -> list[float]:
    return [_dotf(row, v) for row in matrix]


def _inverse(matrix: list[list[float]]) -> list[list[float]]:
    size = len(matrix)
    rows = [[*matrix[i], *[1.0 if j == i else 0.0 for j in range(size)]] for i in range(size)]
    for col in range(size):
        pivot = max(range(col, size), key=lambda r: abs(rows[r][col]))
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [v / scale for v in rows[col]]
        for r in range(size):
            if r != col and rows[r][col] != 0.0:
                factor = rows[r][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col], strict=True)]
    return [row[size:] for row in rows]


def _project_budget_box(v: Sequence[float], lower: Sequence[float], upper: Sequence[float]) -> list[float]:
    """Euclidean projection onto {w: sum w = 1, lower <= w <= upper}: clip(v - theta) with theta found by bisection."""

    def total(theta: float) -> float:
        return sum(min(max(vi - theta, li), ui) for vi, li, ui in zip(v, lower, upper, strict=True))

    lo_t = min(v) - max(upper) - 1.0
    hi_t = max(v) - min(lower) + 1.0
    for _ in range(80):
        mid = (lo_t + hi_t) / 2
        if total(mid) > 1.0:
            lo_t = mid
        else:
            hi_t = mid
    theta = (lo_t + hi_t) / 2
    return [min(max(vi - theta, li), ui) for vi, li, ui in zip(v, lower, upper, strict=True)]


def _lambda_max(matrix: list[list[float]]) -> float:
    """Largest eigenvalue of a symmetric positive semidefinite matrix by power iteration, with a 5 % margin."""
    size = len(matrix)
    v = [1.0 / math.sqrt(size)] * size
    norm = 0.0
    for _ in range(300):
        w = _matvec(matrix, v)
        norm = math.sqrt(_dotf(w, w))
        if norm == 0.0:
            return 1.0
        v = [wi / norm for wi in w]
    return 1.05 * norm


def _guess(rows: list[tuple[list[float], float, tuple[object, ...]]], x: list[float], lam: list[float]) -> list[int]:
    """Working-set guess: rows with a positive multiplier or a slack within 1e-7, largest multiplier first."""
    slack = [float(b) - _dotf(a, x) for a, b, _ in rows]
    order = sorted(range(len(rows)), key=lambda j: (-lam[j], abs(slack[j])))
    return [j for j in order if lam[j] > 1e-9 or abs(slack[j]) <= 1e-7]


def _polish(problem: Problem, rows: list[tuple[list[float], float, tuple[object, ...]]], guess: list[int]) -> Any:
    """Exact KKT solve on a working set of the guess; returned only if feasible and dual feasible, else None."""
    n = problem.n
    budget = [1.0] * n
    working: list[int] = []
    for j in guess:
        if _rank([budget, *(rows[k][0] for k in working), rows[j][0]]) > len(working) + 1:
            working.append(j)
    size = n + 1 + len(working)
    matrix = [[0.0] * size for _ in range(size)]
    rhs = [0.0] * size
    for i in range(n):
        for j in range(n):
            matrix[i][j] = float(problem.sigma[i][j])
        matrix[i][n] = 1.0
        for k, row_index in enumerate(working):
            matrix[i][n + 1 + k] = rows[row_index][0][i]
        rhs[i] = float(problem.mu[i])
    for j in range(n):
        matrix[n][j] = 1.0
    rhs[n] = 1.0
    for k, row_index in enumerate(working):
        for i in range(n):
            matrix[n + 1 + k][i] = rows[row_index][0][i]
        rhs[n + 1 + k] = rows[row_index][1]
    sol = _solve_linear(matrix, rhs)
    x = sol[:n]
    nu = sol[n]
    lam_w = sol[n + 1 :]
    if any(v < -1e-10 for v in lam_w):
        return None
    if abs(sum(x) - 1.0) > 1e-9:
        return None
    if any(_dotf(a, x) - b > 1e-9 for a, b, _ in rows):
        return None
    mult = {rows[row_index][2]: lam_w[k] for k, row_index in enumerate(working)}
    return x, mult, nu

'''

FRONT = {
    "pg": (
        "projected-gradient",
        "2",
        '''
def _front_end(problem: Problem, rows: list[tuple[list[float], float, tuple[object, ...]]]) -> tuple[list[float], list[float]]:
    """Projected gradient on the augmented Lagrangian (method of multipliers). The budget and the box are projected
    exactly; the sector and turnover rows enter through the penalty and the multiplier update."""
    n, m = problem.n, len(rows)
    hessian = [[float(v) for v in row] for row in problem.sigma]
    mu = [float(v) for v in problem.mu]
    a_rows = [list(a) for a, _, _ in rows]
    bound = [float(b) for _, b, _ in rows]
    lo = [float(v) for v in problem.lower]
    hi = [float(v) for v in problem.upper]
    rho = 1.0
    augmented = [[hessian[i][j] + rho * sum(a[i] * a[j] for a in a_rows) for j in range(n)] for i in range(n)]
    step = 1.0 / _lambda_max(augmented)  # 1 / Lipschitz constant of the augmented Lagrangian in w
    x = _project_budget_box([float(v) for v in problem.w0], lo, hi)
    lam = [0.0] * m
    for _ in range(PG_OUTER):
        for _ in range(PG_INNER):
            grad = [_dotf(hessian[i], x) - mu[i] for i in range(n)]
            for j in range(m):
                t = max(0.0, lam[j] + rho * (_dotf(a_rows[j], x) - bound[j]))
                if t:
                    grad = [grad[i] + t * a_rows[j][i] for i in range(n)]
            x = _project_budget_box([x[i] - step * grad[i] for i in range(n)], lo, hi)
        lam = [max(0.0, lam[j] + rho * (_dotf(a_rows[j], x) - bound[j])) for j in range(m)]
    return x, lam

''',
    ),
    "admm": (
        "ADMM (operator splitting, OSQP-style)",
        "3",
        '''
def _front_end(problem: Problem, rows: list[tuple[list[float], float, tuple[object, ...]]]) -> tuple[list[float], list[float]]:
    """ADMM on the stacked constraints l <= A w <= u: the budget is the equality row, every other row is an upper bound.
    The w-step solves one fixed linear system; the z-step projects onto [l, u]; y carries the multipliers."""
    n, m = problem.n, len(rows)
    hessian = [[float(v) for v in row] for row in problem.sigma]
    q = [-float(v) for v in problem.mu]
    a_rows = [[1.0] * n] + [list(a) for a, _, _ in rows]
    lower = [1.0] + [-math.inf] * m
    upper = [1.0] + [float(b) for _, b, _ in rows]
    rho = [1e3] + [0.1] * m
    sigma_reg = 1e-6
    alpha = 1.6
    kkt = [[hessian[i][j] + (sigma_reg if i == j else 0.0) for j in range(n)] for i in range(n)]
    for r, a in enumerate(a_rows):
        for i in range(n):
            for j in range(n):
                kkt[i][j] += rho[r] * a[i] * a[j]
    kinv = _inverse(kkt)
    x = [0.0] * n
    z = [0.0] * (m + 1)
    y = [0.0] * (m + 1)
    for _ in range(ADMM_ITERS):
        rhs = [
            sigma_reg * x[i] - q[i] + sum(a_rows[r][i] * (rho[r] * z[r] - y[r]) for r in range(m + 1)) for i in range(n)
        ]
        x_tilde = _matvec(kinv, rhs)
        z_tilde = [_dotf(a, x_tilde) for a in a_rows]
        x = [alpha * x_tilde[i] + (1 - alpha) * x[i] for i in range(n)]
        z_relax = [alpha * z_tilde[r] + (1 - alpha) * z[r] for r in range(m + 1)]
        z_new = [min(max(z_relax[r] + y[r] / rho[r], lower[r]), upper[r]) for r in range(m + 1)]
        y = [y[r] + rho[r] * (z_relax[r] - z_new[r]) for r in range(m + 1)]
        z = z_new
    return x, [max(0.0, y[r + 1]) for r in range(m)]

''',
    ),
    "ipm": (
        "primal-dual log-barrier interior point",
        "4",
        '''
def _front_end(problem: Problem, rows: list[tuple[list[float], float, tuple[object, ...]]]) -> tuple[list[float], list[float]]:
    """Primal-dual log-barrier interior point from an infeasible start: Newton steps on the perturbed KKT system
    (stationarity, budget, primal rows with slacks, and lambda_j s_j = sigma mu), with the step kept inside the cone."""
    n, m = problem.n, len(rows)
    hessian = [[float(v) for v in row] for row in problem.sigma]
    mu = [float(v) for v in problem.mu]
    a_rows = [list(a) for a, _, _ in rows]
    bound = [float(b) for _, b, _ in rows]
    x = [float(v) for v in problem.w0]
    nu = 0.0
    lam = [1.0] * m
    s = [max(bound[j] - _dotf(a_rows[j], x), 1.0) for j in range(m)]
    for _ in range(IPM_ITERS):
        r_d = [
            _dotf(hessian[i], x) - mu[i] + nu + sum(a_rows[j][i] * lam[j] for j in range(m)) for i in range(n)
        ]
        r_e = sum(x) - 1.0
        r_p = [_dotf(a_rows[j], x) + s[j] - bound[j] for j in range(m)]
        gap = sum(lam[j] * s[j] for j in range(m)) / m
        target = 0.2 * gap
        r_c = [lam[j] * s[j] - target for j in range(m)]
        if max(abs(v) for v in [*r_d, r_e, *r_p]) < 1e-11 and gap < 1e-11:
            break
        d = [lam[j] / s[j] for j in range(m)]
        schur = [
            [hessian[i][k] + sum(a_rows[j][i] * d[j] * a_rows[j][k] for j in range(m)) for k in range(n)]
            for i in range(n)
        ]
        rhs1 = [
            -r_d[i] - sum(a_rows[j][i] * ((-r_c[j] + lam[j] * r_p[j]) / s[j]) for j in range(m)) for i in range(n)
        ]
        big = [[*schur[i], 1.0] for i in range(n)] + [[*([1.0] * n), 0.0]]
        sol = _solve_linear(big, [*rhs1, -r_e])
        dx = sol[:n]
        d_nu = sol[n]
        ds = [-r_p[j] - _dotf(a_rows[j], dx) for j in range(m)]
        dl = [(-r_c[j] - lam[j] * ds[j]) / s[j] for j in range(m)]
        alpha = 1.0
        for j in range(m):
            if ds[j] < 0.0:
                alpha = min(alpha, -0.995 * s[j] / ds[j])
            if dl[j] < 0.0:
                alpha = min(alpha, -0.995 * lam[j] / dl[j])
        x = [x[i] + alpha * dx[i] for i in range(n)]
        nu += alpha * d_nu
        lam = [lam[j] + alpha * dl[j] for j in range(m)]
        s = [s[j] + alpha * ds[j] for j in range(m)]
    return x, lam

''',
    ),
    "dual": (
        "dual ascent on the Lagrangian",
        "5",
        '''
def _front_end(problem: Problem, rows: list[tuple[list[float], float, tuple[object, ...]]]) -> tuple[list[float], list[float]]:
    """Dual ascent: for given multipliers the minimum over w is the linear solve H w = mu - nu 1 - A' lambda; the
    multipliers then move along the dual gradient (A w - b for lambda, sum w - 1 for nu), lambda kept non-negative."""
    n, m = problem.n, len(rows)
    hessian = [[float(v) for v in row] for row in problem.sigma]
    mu = [float(v) for v in problem.mu]
    a_rows = [list(a) for a, _, _ in rows]
    bound = [float(b) for _, b, _ in rows]
    hinv = _inverse(hessian)
    ones = [1.0] * n

    def quad(u: Sequence[float], v: Sequence[float]) -> float:
        return _dotf(u, _matvec(hinv, v))

    step = 1.0 / (sum(quad(a, a) for a in a_rows) + quad(ones, ones) + 1e-12)
    lam = [0.0] * m
    nu = 0.0
    x = [0.0] * n
    for _ in range(DUAL_ITERS):
        rhs = [mu[i] - nu - sum(a_rows[j][i] * lam[j] for j in range(m)) for i in range(n)]
        x = _matvec(hinv, rhs)
        lam = [max(0.0, lam[j] + step * (_dotf(a_rows[j], x) - bound[j])) for j in range(m)]
        nu = nu + step * (sum(x) - 1.0)
    return x, lam

''',
    ),
}

DRIVER = '''

def _solve(problem: Problem) -> dict[str, Any]:
    global LAST_PATH
    n = problem.n
    g = problem.gamma
    scaled = Problem(
        problem.n, Fraction(1), [m / g for m in problem.mu], problem.sigma, problem.w0, problem.lower, problem.upper,
        problem.sector, problem.caps, problem.tau,
    )
    rows = _inequalities(scaled)
    found = None
    try:
        x0, lam0 = _front_end(scaled, rows)
        found = _polish(scaled, rows, _guess(rows, x0, lam0))
    except (ArithmeticError, StopIteration, RuntimeError):
        found = None  # a singular or non-finite front-end step: the verified active-set search below still answers
    if found is None:
        LAST_PATH = "fallback"
        x, mult, budget_mult = _active_set(scaled, rows)
    else:
        LAST_PATH = "front-end"
        x, mult, budget_mult = found
    mult = {k: v * g for k, v in mult.items()}
    budget_mult = budget_mult * g
'''

for key, (name, number, front) in FRONT.items():
    head = base[:DOC_OLD_START] + (
        '"""Alternative ({number}) of plan 7.4 item 2, {name}: a complete solver for the page\'s problem.\n\n'
        "The front end is the named method. Its working-set guess is finished by an exact KKT solve that is accepted only if\n"
        "it is feasible and dual feasible; otherwise the active-set search of the round-12 alternative D answers. Float\n"
        'arithmetic; gamma is folded into the linear term. Nothing here is a real portfolio: every input is SIMULATED.\n"""'
    ).replace("{number}", number).replace("{name}", name) + base[DOC_OLD_END:SOLVE_START]
    text = head.replace("from typing import Any, cast", "from typing import Any, cast")
    text += SHARED + front + DRIVER + solve_tail
    text = text[:]
    cert = base[CERT_START:]
    if not text.rstrip().endswith(cert.rstrip()):
        text = text.rstrip() + "\n\n\n" + cert
    out = out_dir / f"alt_{number}_{key}.py"
    out.write_text(text, encoding="utf-8")
    print(out.name, len(text.splitlines()))
