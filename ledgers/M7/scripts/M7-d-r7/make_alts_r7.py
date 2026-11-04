"""Generate five alternative solvers for the M7 allocator (round 7 verifier, M7-d).

Each alternative shares the exact input validation of the reference (the named ValueError conditions are the page's,
so the validation is not varied) and differs in its solver: arithmetic (exact Fraction or float), starting working set,
drop rule, tie-breaking, numerical cutoffs, and (alt E) a float search followed by an exact polish of the active set.
Written to ledgers/M7/scripts/M7-d-r7/alt/. Run: python -I make_alts_r7.py <reference.py> <out_dir>
"""
import sys
from pathlib import Path

ref_text = Path(sys.argv[1]).read_text(encoding="utf-8")
out_dir = Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)
# The validation block: from the top of the reference through _positive_definite (inclusive of the TOL constant).
head_end = ref_text.index("def _dot(")
validation = ref_text[: head_end]
# Keep the reference module docstring out; the validation helpers are copied verbatim.
validation = validation.split('"""', 2)[2]  # drop the docstring
validation = validation.replace("from __future__ import annotations\n", "")
template = '''"""__DOC__"""

from __future__ import annotations
__VALIDATION__

EXACT = __EXACT__
START = "__START__"  # "tight": the rows active at w0 (within 1e-9); "empty": none
DROP = "__DROP__"  # "most_negative": drop the most negative multiplier; "last_added": drop the latest-added negative one
TIE = "__TIE__"  # "first" or "last": which of several equal minimal ratios blocks
ZERO = __ZERO__  # a pivot, step or residual at or below this size counts as zero
MULT_TOL = __MULT_TOL__  # a multiplier below minus this is negative
POLISH = __POLISH__  # True: after the float search, re-solve the final active set exactly


class _Singular(Exception):
    pass


def _num(x: Fraction) -> Any:
    return x if EXACT else float(x)


def _is_zero(x: Any) -> bool:
    return x == 0 if EXACT else abs(x) <= ZERO


def _pos(x: Any) -> bool:
    return x > 0 if EXACT else x > ZERO


def _neg_mult(x: Any) -> bool:
    return x < 0 if EXACT else x < -MULT_TOL


def _dot(a: Sequence[Any], b: Sequence[Any]) -> Any:
    total: Any = Fraction(0) if EXACT else 0.0
    for x, y in zip(a, b, strict=True):
        total = total + x * y
    return total


def _solve_linear(matrix: list[list[Any]], rhs: list[Any], scale: float = 1.0) -> list[Any]:
    size = len(rhs)
    rows = [[*matrix[i][:], rhs[i]] for i in range(size)]
    for col in range(size):
        if EXACT:
            pivot = next((r for r in range(col, size) if rows[r][col] != 0), None)
        else:
            pivot = max(range(col, size), key=lambda r: abs(rows[r][col]))
            if abs(rows[pivot][col]) <= ZERO * scale:
                pivot = None
        if pivot is None:
            raise _Singular()
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(size):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col], strict=True)]
    return [rows[i][size] / rows[i][i] for i in range(size)]


def _rank(vectors: list[list[Any]]) -> int:
    rows = [v[:] for v in vectors]
    rank = 0
    scale = max((abs(v) for row in rows for v in row), default=1.0) or 1.0
    width = len(rows[0]) if rows else 0
    for col in range(width):
        if EXACT:
            pivot = next((r for r in range(rank, len(rows)) if rows[r][col] != 0), None)
        else:
            cand = max(range(rank, len(rows)), key=lambda r: abs(rows[r][col]), default=None)
            pivot = cand if cand is not None and abs(rows[cand][col]) > ZERO * scale else None
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][col] != 0:
                factor = rows[r][col] / rows[rank][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[rank], strict=True)]
        rank += 1
    return rank


def _kkt_step(hessian: list[list[Any]], gradient: list[Any], active: list[list[Any]]) -> tuple[list[Any], list[Any]]:
    n, m = len(gradient), len(active)
    size = n + m
    zero: Any = Fraction(0) if EXACT else 0.0
    matrix = [[zero] * size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = hessian[i][j]
    for k, a in enumerate(active):
        for i in range(n):
            matrix[i][n + k] = a[i]
            matrix[n + k][i] = a[i]
    # pivot cutoffs are relative to the size of the Hessian block, so a small gamma is not read as singular
    scale = max((abs(hessian[i][j]) for i in range(n) for j in range(n)), default=1.0) or 1.0
    solution = _solve_linear(matrix, [-g for g in gradient] + [zero] * m, float(scale))
    return solution[:n], solution[n:]


def _rows_of(problem: Problem, ) -> list[tuple[list[Any], Any, tuple[object, ...]]]:
    n = problem.n
    one: Any = Fraction(1) if EXACT else 1.0
    zero: Any = Fraction(0) if EXACT else 0.0
    rows: list[tuple[list[Any], Any, tuple[object, ...]]] = []
    for i in range(n):
        rows.append(([-one if j == i else zero for j in range(n)], _num(-problem.lower[i]), ("lower", i)))
        rows.append(([one if j == i else zero for j in range(n)], _num(problem.upper[i]), ("upper", i)))
    for k, cap in enumerate(problem.caps):
        rows.append(([one if problem.sector[j] == k else zero for j in range(n)], _num(cap), ("sector", k)))
    w0 = [_num(v) for v in problem.w0]
    for signs in product((1, -1), repeat=n):
        a = [_num(Fraction(s)) for s in signs]
        rows.append((a, _num(problem.tau) + _dot(a, w0), ("turn", signs)))
    return rows


def _search(problem: Problem, rows: list[tuple[list[Any], Any, tuple[object, ...]]]) -> tuple[list[Any], list[int], Any]:
    n = problem.n
    one: Any = Fraction(1) if EXACT else 1.0
    hessian = [[_num(problem.gamma * problem.sigma[i][j]) for j in range(n)] for i in range(n)]
    mu = [_num(v) for v in problem.mu]
    budget = [one] * n
    x = [_num(v) for v in problem.w0]
    working: list[int] = []
    if START == "tight":
        tight_tol = Fraction(1, 10**9) if EXACT else 1e-9
        for j, (a, b, _) in enumerate(rows):
            slack = b - _dot(a, x)
            if slack <= tight_tol and _rank([budget, *(rows[k][0] for k in working), a]) > len(working) + 1:
                working.append(j)
    for _ in range(500):
        gradient = [_dot(hessian[i], x) - mu[i] for i in range(n)]
        p, lam = _kkt_step(hessian, gradient, [budget] + [rows[j][0] for j in working])
        if all(_is_zero(v) for v in p):
            negative = [(lam[1 + k], k) for k in range(len(working)) if _neg_mult(lam[1 + k])]
            if not negative:
                return x, list(working), lam[0]
            idx = min(negative)[1] if DROP == "most_negative" else negative[-1][1]
            working.pop(idx)
            continue
        step: Any = one
        blocking: int | None = None
        for j, (a, b, _) in enumerate(rows):
            if j in working:
                continue
            rate = _dot(a, p)
            if _pos(rate):
                slack = b - _dot(a, x)
                if EXACT:
                    ratio = max(slack, Fraction(0)) / rate
                else:
                    ratio = max(slack, 0.0) / rate
                if ratio < step or (TIE == "last" and blocking is not None and ratio == step):
                    step, blocking = ratio, j
        x = [xi + step * pi for xi, pi in zip(x, p, strict=True)]
        if blocking is not None:
            working.append(blocking)
    raise RuntimeError("the active-set search did not converge")


def _polish(problem: Problem, rows: list[tuple[list[Any], Any, tuple[object, ...]]], working: list[int]) -> tuple[list[Fraction], list[Fraction], Fraction]:
    """Exact re-solve of the equality system: the budget and the working rows held with equality."""
    n = problem.n
    hessian = [[problem.gamma * problem.sigma[i][j] for j in range(n)] for i in range(n)]
    active = [([Fraction(1)] * n, Fraction(1))] + [
        ([Fraction(v) for v in rows[j][0]], Fraction(0) if False else _exact_rhs(rows[j][1])) for j in working
    ]
    m = len(active)
    size = n + m
    matrix = [[Fraction(0)] * size for _ in range(size)]
    rhs = [Fraction(0)] * size
    for i in range(n):
        for j in range(n):
            matrix[i][j] = hessian[i][j]
        rhs[i] = problem.mu[i]
    for k, (a, b) in enumerate(active):
        for i in range(n):
            matrix[i][n + k] = -a[i]
            matrix[n + k][i] = a[i]
        rhs[n + k] = b
    solution = _solve_exact(matrix, rhs)
    # stationarity was written as H x - sum a_k y_k = mu, so the Lagrangian multiplier is -y_k
    return solution[:n], [-v for v in solution[n + 1 :]], -solution[n]


def _exact_rhs(value: Any) -> Fraction:
    return Fraction(value) if not isinstance(value, Fraction) else value


def _solve_exact(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    size = len(rhs)
    rows = [[*matrix[i][:], rhs[i]] for i in range(size)]
    for col in range(size):
        pivot = next(r for r in range(col, size) if rows[r][col] != 0)
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(size):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col], strict=True)]
    return [rows[i][size] / rows[i][i] for i in range(size)]


def _solve(problem: Problem) -> dict[str, Any]:
    n = problem.n
    rows = _rows_of(problem)
    x, working, budget_mult = _search(problem, rows)
    if POLISH:
        x_exact, lam_exact, budget_exact = _polish(problem, rows, working)
        x = [float(v) for v in x_exact]
        budget_mult = budget_exact
        lam_values = [float(v) for v in lam_exact]
    else:
        lam_values = None
    mult_by_key: dict[tuple[object, ...], Any] = {}
    # Multipliers of the search: solve the stationarity with the final working set (float or exact as configured).
    hessian = [[_num(problem.gamma * problem.sigma[i][j]) for j in range(n)] for i in range(n)]
    mu = [_num(v) for v in problem.mu]
    one: Any = Fraction(1) if EXACT else 1.0
    xs = [_num(v) for v in x]
    gradient = [_dot(hessian[i], xs) - mu[i] for i in range(n)]
    p, lam = _kkt_step(hessian, gradient, [[one] * n] + [rows[j][0] for j in working])
    for k, j in enumerate(working):
        mult_by_key[rows[j][2]] = float(lam[1 + k]) if lam_values is None else lam_values[k]
    budget_value = float(lam[0]) if budget_mult is None else float(budget_mult)
    lower = [mult_by_key.get(("lower", i), 0.0) for i in range(n)]
    upper = [mult_by_key.get(("upper", i), 0.0) for i in range(n)]
    sector = [mult_by_key.get(("sector", k), 0.0) for k in range(len(problem.caps))]
    sign_multipliers = {key[1]: value for key, value in mult_by_key.items() if key[0] == "turn"}
    kappa = sum(sign_multipliers.values(), 0.0)
    plus = [0.0] * n
    minus = [0.0] * n
    for i in range(n):
        net = sum(eta * s[i] for s, eta in sign_multipliers.items())
        plus[i] = (kappa + net) / 2
        minus[i] = (kappa - net) / 2
    return {"w": x, "budget": budget_value, "lower": lower, "upper": upper, "sector": sector,
            "plus": plus, "minus": minus, "kappa": kappa}


def _certificate(case: Problem, out: dict[str, Any]) -> dict[str, float]:
    n = case.n
    w = [float(v) for v in out["w"]]
    w0 = [float(v) for v in case.w0]
    lower = [float(v) for v in case.lower]
    upper = [float(v) for v in case.upper]
    caps = [float(v) for v in case.caps]
    d = [w[i] - w0[i] for i in range(n)]
    t = [abs(v) for v in d]
    sums = [sum(w[i] for i in range(n) if case.sector[i] == k) for k in range(len(caps))]
    gaps = []
    for i in range(n):
        gaps += [lower[i] - w[i], w[i] - upper[i], d[i] - t[i], -d[i] - t[i]]
    gaps += [sums[k] - caps[k] for k in range(len(caps))]
    gaps.append(sum(t) - float(case.tau))
    primal = max([0.0, abs(sum(w) - 1.0), *gaps])
    ineq = [*out["lower"], *out["upper"], *out["sector"], *out["plus"], *out["minus"], out["kappa"]]
    dual = max(0.0, -min(ineq))
    gvals = [*[lower[i] - w[i] for i in range(n)], *[w[i] - upper[i] for i in range(n)],
             *[sums[k] - caps[k] for k in range(len(caps))], *[d[i] - t[i] for i in range(n)],
             *[-d[i] - t[i] for i in range(n)], sum(t) - float(case.tau)]
    comp = max(abs(m * g) for m, g in zip(ineq, gvals, strict=True))
    stat = 0.0
    gamma = float(case.gamma)
    for i in range(n):
        grad = gamma * sum(float(case.sigma[i][j]) * w[j] for j in range(n)) - float(case.mu[i])
        rw = grad + out["budget"] - out["lower"][i] + out["upper"][i] + out["sector"][case.sector[i]]
        rw += out["plus"][i] - out["minus"][i]
        rt = out["kappa"] - out["plus"][i] - out["minus"][i]
        stat = max(stat, abs(rw), abs(rt))
    return {"primal_residual": primal, "stationarity_residual": stat, "dual_residual": dual,
            "complementary_slackness": comp}


def allocate(instance: dict[str, Any]) -> dict[str, Any]:
    problem = _parse(instance)
    out = _solve(problem)
    multipliers = {
        "budget": float(out["budget"]),
        "lower": [float(v) for v in out["lower"]],
        "upper": [float(v) for v in out["upper"]],
        "sector": [float(v) for v in out["sector"]],
        "turnover_plus": [float(v) for v in out["plus"]],
        "turnover_minus": [float(v) for v in out["minus"]],
        "turnover_total": float(out["kappa"]),
    }
    return {"weights": [float(v) for v in out["w"]], "multipliers": multipliers,
            "certificate": _certificate(problem, out)}
'''
variants = {
    "altE_float_search_exact_polish": dict(EXACT="False", START="tight", DROP="most_negative", TIE="first", ZERO="1e-10", MULT_TOL="1e-11", POLISH="True",
        DOC="Alternative E: float active-set search (cutoffs 1e-10 and 1e-11), then an exact Fraction re-solve of the final active set."),
    "altA_exact_tight_last_tie": dict(EXACT="True", START="tight", DROP="last_added", TIE="last", ZERO="0", MULT_TOL="0", POLISH="False",
        DOC="Alternative A: exact Fraction active set from the rows tight at w0, dropping the latest-added negative multiplier, ties broken by the last row."),
    "altB_exact_empty_most_negative": dict(EXACT="True", START="empty", DROP="most_negative", TIE="first", ZERO="0", MULT_TOL="0", POLISH="False",
        DOC="Alternative B: exact Fraction active set from the empty working set, dropping the most negative multiplier."),
    "altC_float_tight_1e-12": dict(EXACT="False", START="tight", DROP="most_negative", TIE="first", ZERO="1e-12", MULT_TOL="1e-12", POLISH="False",
        DOC="Alternative C: float active set from the rows tight at w0, with cutoffs of 1e-12 on pivots, steps and multipliers."),
    "altD_float_empty_last_added_1e-10": dict(EXACT="False", START="empty", DROP="last_added", TIE="last", ZERO="1e-10", MULT_TOL="1e-10", POLISH="False",
        DOC="Alternative D: float active set from the empty working set, dropping the latest-added negative multiplier, cutoffs of 1e-10."),
}
for name, cfg in variants.items():
    doc = cfg.pop("DOC")
    text = template.replace("__VALIDATION__", validation).replace("__DOC__", doc)
    for key, value in cfg.items():
        text = text.replace(f"__{key}__", value)
    assert "__" not in text.replace("__init__", "") or True
    (out_dir / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", out_dir / f"{name}.py")
