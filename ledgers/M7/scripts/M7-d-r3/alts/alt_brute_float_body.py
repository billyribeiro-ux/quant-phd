

def _rows(problem: Problem) -> list[tuple[list[float], float, tuple[object, ...]]]:
    """Rows a.w <= b: bounds, sector caps, and the 2**n sign forms of the turnover limit (floats)."""
    n = problem.n
    rows: list[tuple[list[float], float, tuple[object, ...]]] = []
    for i in range(n):
        rows.append(([-1.0 if j == i else 0.0 for j in range(n)], -float(problem.lower[i]), ("lower", i)))
        rows.append(([1.0 if j == i else 0.0 for j in range(n)], float(problem.upper[i]), ("upper", i)))
    for k, cap in enumerate(problem.caps):
        rows.append(([1.0 if problem.sector[j] == k else 0.0 for j in range(n)], float(cap), ("sector", k)))
    w0 = [float(v) for v in problem.w0]
    tau = float(problem.tau)
    for signs in product((1.0, -1.0), repeat=n):
        rows.append((list(signs), tau + sum(s * x for s, x in zip(signs, w0, strict=True)), ("turn", signs)))
    return rows


def _solve_float(matrix: list[list[float]], rhs: list[float]) -> list[float] | None:
    """Gauss elimination with partial pivoting; None when a pivot is numerically zero."""
    size = len(rhs)
    m = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for c in range(size):
        p = max(range(c, size), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-12:
            return None
        m[c], m[p] = m[p], m[c]
        for r in range(size):
            if r != c and m[r][c] != 0.0:
                factor = m[r][c] / m[c][c]
                m[r] = [x - factor * y for x, y in zip(m[r], m[c], strict=True)]
    return [m[i][size] / m[i][i] for i in range(size)]


def _kkt_for_set(
    hessian: list[list[float]],
    gradient_constant: list[float],
    rows: list[tuple[list[float], float, tuple[object, ...]]],
    chosen: tuple[int, ...],
) -> tuple[list[float], float, list[float]] | None:
    """Solve P w + q + nu 1 + sum_c lam_c a_c = 0, 1'w = 1, a_c'w = b_c for the chosen rows (unknowns w, nu, lam)."""
    n = len(gradient_constant)
    k = len(chosen)
    size = n + 1 + k
    matrix = [[0.0] * size for _ in range(size)]
    rhs = [0.0] * size
    for i in range(n):
        for j in range(n):
            matrix[i][j] = hessian[i][j]
        matrix[i][n] = 1.0
        for c, idx in enumerate(chosen):
            matrix[i][n + 1 + c] = rows[idx][0][i]
        rhs[i] = -gradient_constant[i]
    for j in range(n):
        matrix[n][j] = 1.0
    rhs[n] = 1.0
    for c, idx in enumerate(chosen):
        a, b, _ = rows[idx]
        for j in range(n):
            matrix[n + 1 + c][j] = a[j]
        rhs[n + 1 + c] = b
    solution = _solve_float(matrix, rhs)
    if solution is None:
        return None
    return solution[:n], solution[n], solution[n + 1 :]


def _enumerate(problem: Problem) -> tuple[list[float], float, dict[tuple[object, ...], float]]:
    """The first working set (smallest first) whose primal point is feasible and whose multipliers are non-negative."""
    n = problem.n
    rows = _rows(problem)
    hessian = [[float(problem.gamma) * float(problem.sigma[i][j]) for j in range(n)] for i in range(n)]
    gradient_constant = [-float(v) for v in problem.mu]
    for size in range(0, n):
        for chosen in combinations(range(len(rows)), size):
            found = _kkt_for_set(hessian, gradient_constant, rows, chosen)
            if found is None:
                continue
            w, nu, lam = found
            if not all(math.isfinite(v) for v in w):
                continue
            if any(sum(a[j] * w[j] for j in range(n)) - b > FLOAT_TOL for a, b, _ in rows):
                continue
            if any(v < -FLOAT_TOL for v in lam):
                continue
            return w, nu, {rows[idx][2]: max(lam[c], 0.0) for c, idx in enumerate(chosen)}
    raise RuntimeError("no working set satisfies the KKT conditions")


def _certificate_float(
    problem: Problem,
    w: list[float],
    budget: float,
    lower: list[float],
    upper: list[float],
    sector: list[float],
    plus: list[float],
    minus: list[float],
    kappa: float,
) -> dict[str, float]:
    n = problem.n
    w0 = [float(v) for v in problem.w0]
    lo = [float(v) for v in problem.lower]
    up = [float(v) for v in problem.upper]
    caps = [float(v) for v in problem.caps]
    tau = float(problem.tau)
    d = [w[i] - w0[i] for i in range(n)]
    t = [abs(x) for x in d]
    sums = [sum(w[i] for i in range(n) if problem.sector[i] == k) for k in range(len(caps))]
    gaps_bounds = [lo[i] - w[i] for i in range(n)] + [w[i] - up[i] for i in range(n)]
    gaps_sector = [sums[k] - caps[k] for k in range(len(caps))]
    gaps_turn = [d[i] - t[i] for i in range(n)] + [-d[i] - t[i] for i in range(n)]
    gaps_total = [sum(t) - tau]
    primal = max([0.0, abs(sum(w) - 1.0)] + gaps_bounds + gaps_sector + gaps_turn + gaps_total)
    mults = lower + upper + sector + plus + minus + [kappa]
    gaps = gaps_bounds + gaps_sector + gaps_turn + gaps_total
    dual = max(0.0, -min(mults))
    comp = max(abs(m * g) for m, g in zip(mults, gaps, strict=True))
    stat = 0.0
    for i in range(n):
        grad = float(problem.gamma) * sum(float(problem.sigma[i][j]) * w[j] for j in range(n)) - float(problem.mu[i])
        r_w = grad + budget - lower[i] + upper[i] + sector[problem.sector[i]] + plus[i] - minus[i]
        r_t = kappa - plus[i] - minus[i]
        stat = max(stat, abs(r_w), abs(r_t))
    return {
        "primal_residual": primal,
        "stationarity_residual": stat,
        "dual_residual": dual,
        "complementary_slackness": comp,
    }


def allocate(instance: dict[str, Any]) -> dict[str, Any]:
    problem = _parse(instance)
    n = problem.n
    w, nu, mult = _enumerate(problem)
    lower = [mult.get(("lower", i), 0.0) for i in range(n)]
    upper = [mult.get(("upper", i), 0.0) for i in range(n)]
    sector = [mult.get(("sector", k), 0.0) for k in range(len(problem.caps))]
    signs = {key[1]: value for key, value in mult.items() if key[0] == "turn"}
    kappa = sum(signs.values())
    plus = [(kappa + sum(eta * s[i] for s, eta in signs.items())) / 2 for i in range(n)]
    minus = [(kappa - sum(eta * s[i] for s, eta in signs.items())) / 2 for i in range(n)]
    certificate = _certificate_float(problem, w, nu, lower, upper, sector, plus, minus, kappa)
    return {
        "weights": w,
        "multipliers": {
            "budget": nu,
            "lower": lower,
            "upper": upper,
            "sector": sector,
            "turnover_plus": plus,
            "turnover_minus": minus,
            "turnover_total": kappa,
        },
        "certificate": certificate,
    }
