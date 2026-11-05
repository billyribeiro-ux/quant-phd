"""Round-10 verifier (E3-d): builds five alternative correct elicit.py implementations plus one step-size variant.

Each alternative is the reference validation (the exception table) with a different numerical method, written by the
verifier, not copied from the builder's solution. Output: alts/altN/elicit.py.
"""
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
REF = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")


def replace_function(src: str, name: str, new_body: str) -> str:
    """Replace the top-level function `name` (from its def line to the next top-level def/class or EOF)."""
    pat = re.compile(rf"^def {name}\(.*?(?=^def |\Z)", re.S | re.M)
    m = pat.search(src)
    assert m, name
    return src[: m.start()] + new_body.rstrip() + "\n\n\n" + src[m.end():]


# alt1: closed-form CRRA, prospect CE closed form; MLE by a zooming 11x11x11 grid, then Newton polish.
ALT1_MAXIMISE = '''
def _newton_polish(f, xi: list[float]) -> list[float]:
    for _ in range(200):
        grad, hess = _gradient_and_hessian(f, xi)
        if max(abs(g) for g in grad) < 1e-9:
            return xi
        neg = [[-h for h in row] for row in hess]
        lower = _cholesky([[neg[i][j] + (1e-6 if i == j else 0.0) for j in range(3)] for i in range(3)])
        if lower is None:
            step = [0.05 * g for g in grad]
        else:
            step = _solve(lower, grad)
        scale = 1.0
        base = f(xi)
        while scale > 1e-12 and f([x + scale * s for x, s in zip(xi, step, strict=True)]) <= base:
            scale /= 2.0
        if scale <= 1e-12:
            return xi
        xi = [x + scale * s for x, s in zip(xi, step, strict=True)]
    return xi


def _maximise(parsed: list[Parsed]) -> list[float]:
    def f(t: list[float]) -> float:
        return _objective(t, parsed)

    lo = [-6.0, -3.0, -3.0]
    hi = [6.0, 4.0, 3.0]
    best_t: list[float] = [0.0, 0.0, 0.0]
    best_v = -math.inf
    n = 11
    for _ in range(6):
        for c in [lo[0] + (hi[0] - lo[0]) * k / (n - 1) for k in range(n)]:
            for a in [lo[1] + (hi[1] - lo[1]) * k / (n - 1) for k in range(n)]:
                for b in [lo[2] + (hi[2] - lo[2]) * k / (n - 1) for k in range(n)]:
                    v = f([c, a, b])
                    if v > best_v:
                        best_v, best_t = v, [c, a, b]
        half = [(hi[i] - lo[i]) / (n - 1) for i in range(3)]
        lo = [best_t[i] - half[i] for i in range(3)]
        hi = [best_t[i] + half[i] for i in range(3)]
    return _newton_polish(f, best_t)
'''

# alt2: pure Newton with a finite-difference gradient at step 1e-6 (no damping, Gaussian elimination), from a 3x3x3 start.
ALT2_MAXIMISE = '''
def _gauss_solve(a: list[list[float]], rhs: list[float]) -> list[float] | None:
    n = len(rhs)
    m = [list(a[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-300:
            return None
        m[col], m[piv] = m[piv], m[col]
        for r in range(n):
            if r != col:
                fct = m[r][col] / m[col][col]
                m[r] = [x - fct * y for x, y in zip(m[r], m[col], strict=True)]
    return [m[i][n] / m[i][i] for i in range(n)]


def _maximise(parsed: list[Parsed]) -> list[float]:
    def f(t: list[float]) -> float:
        return _objective(t, parsed)

    h = 1e-6
    best_t = [0.0, 0.0, 0.0]
    best_v = -math.inf
    for c in (-2.0, 0.0, 2.0):
        for a in (-1.0, 0.5, 2.0):
            for b in (-1.0, 0.0, 1.0):
                if f([c, a, b]) > best_v:
                    best_v, best_t = f([c, a, b]), [c, a, b]
    xi = best_t
    for _ in range(300):
        g = [0.0] * 3
        H = [[0.0] * 3 for _ in range(3)]
        for i in range(3):
            up = list(xi); dn = list(xi); up[i] += h; dn[i] -= h
            g[i] = (f(up) - f(dn)) / (2 * h)
        for i in range(3):
            for j in range(3):
                pp = list(xi); pm = list(xi); mp = list(xi); mm = list(xi)
                pp[i] += h; pp[j] += h
                pm[i] += h; pm[j] -= h
                mp[i] -= h; mp[j] += h
                mm[i] -= h; mm[j] -= h
                H[i][j] = (f(pp) - f(pm) - f(mp) + f(mm)) / (4 * h * h)
        if max(abs(x) for x in g) < 1e-9:
            return xi
        step = _gauss_solve([[-x for x in row] for row in H], g)
        if step is None:
            return xi
        if f([x + s for x, s in zip(xi, step, strict=True)]) > f(xi) or max(abs(s) for s in step) < 1e-7:
            xi = [x + s for x, s in zip(xi, step, strict=True)]
        else:
            xi = [x + 0.5 * s for x, s in zip(xi, step, strict=True)]
    return xi
'''

# alt3: Nelder-Mead written by hand on the negative log-likelihood, then Newton polish.
ALT3_MAXIMISE = '''
def _nelder_mead(f, x0: list[float], scale: float = 0.5) -> list[float]:
    n = len(x0)
    simplex = [list(x0)]
    for i in range(n):
        p = list(x0)
        p[i] += scale
        simplex.append(p)
    vals = [f(p) for p in simplex]
    for _ in range(20000):
        order = sorted(range(n + 1), key=lambda k: vals[k])
        simplex = [simplex[k] for k in order]
        vals = [vals[k] for k in order]
        if abs(vals[-1] - vals[0]) < 1e-15 and max(abs(simplex[k][i] - simplex[0][i]) for k in range(1, n + 1) for i in range(n)) < 1e-11:
            break
        centroid = [sum(simplex[k][i] for k in range(n)) / n for i in range(n)]
        worst = simplex[-1]
        xr = [centroid[i] + (centroid[i] - worst[i]) for i in range(n)]
        fr = f(xr)
        if fr < vals[0]:
            xe = [centroid[i] + 2.0 * (centroid[i] - worst[i]) for i in range(n)]
            fe = f(xe)
            if fe < fr:
                simplex[-1], vals[-1] = xe, fe
            else:
                simplex[-1], vals[-1] = xr, fr
        elif fr < vals[-2]:
            simplex[-1], vals[-1] = xr, fr
        else:
            xc = [centroid[i] + 0.5 * (worst[i] - centroid[i]) for i in range(n)]
            fc = f(xc)
            if fc < vals[-1]:
                simplex[-1], vals[-1] = xc, fc
            else:
                for k in range(1, n + 1):
                    simplex[k] = [simplex[0][i] + 0.5 * (simplex[k][i] - simplex[0][i]) for i in range(n)]
                    vals[k] = f(simplex[k])
    best = min(range(n + 1), key=lambda k: vals[k])
    return simplex[best]


def _maximise(parsed: list[Parsed]) -> list[float]:
    def f(t: list[float]) -> float:
        value = _objective(t, parsed)
        return -value if math.isfinite(value) else math.inf

    best_t = _nelder_mead(f, [0.0, 0.5, 0.0])
    best_t = _nelder_mead(f, best_t, 0.05)
    return _newton_polish(lambda t: _objective(t, parsed), best_t)
'''

# the polish used by alt3 (same Newton as alt1)
POLISH = ALT1_MAXIMISE[ALT1_MAXIMISE.index("def _newton_polish"): ALT1_MAXIMISE.index("def _maximise")]

# alt4: prospect CE by bisection inversion of v on [min prize, max prize] (no closed form), then the same half-up rule.
ALT4_PROSPECT = '''
def _prospect_ce(prizes: list[int], probs: list[Fraction], gamma: float, lam: float) -> float:
    """Unrounded prospect CE by bisection on the monotone value function, to a width of 1e-9 cents."""
    total = sum(float(p) * _value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))
    lo, hi = float(min(prizes)), float(max(prizes))
    if lo == hi:
        return lo
    while hi - lo > 1e-9:
        mid = 0.5 * (lo + hi)
        v = _value(mid, gamma, lam) if mid >= 0 else -lam * math.pow(-mid, 1.0 - gamma)
        if v < total:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)
'''

# alt5: prospect CE computed in Decimal (50 digits) and rounded once to a float, then half-up on the float value.
ALT5_PROSPECT = '''
def _prospect_ce(prizes: list[int], probs: list[Fraction], gamma: float, lam: float) -> float:
    """Unrounded prospect CE in 50-digit Decimal arithmetic, returned as a float."""
    from decimal import Decimal, localcontext

    with localcontext() as ctx:
        ctx.prec = 50
        g = Decimal(repr(gamma))
        L = Decimal(repr(lam))
        expo = Decimal(1) - g
        total = Decimal(0)
        for x, p in zip(prizes, probs, strict=True):
            pd = Decimal(p.numerator) / Decimal(p.denominator)
            if x >= 0:
                val = Decimal(x) ** expo if x > 0 else Decimal(0)
            else:
                val = -L * (Decimal(-x) ** expo)
            total += pd * val
        if total >= 0:
            ce = total ** (Decimal(1) / expo) if total > 0 else Decimal(0)
        else:
            ce = -((-total / L) ** (Decimal(1) / expo))
        return float(ce)
'''

base = REF
out = {
    "alt1_grid_zoom_newton": replace_function(base, "_maximise", ALT1_MAXIMISE),
    "alt2_pure_newton_fd1e-6": replace_function(base, "_maximise", ALT2_MAXIMISE),
    "alt3_nelder_mead": replace_function(base, "_maximise", ALT3_MAXIMISE.replace("def _maximise", POLISH + "def _maximise", 1)),
    "alt4_bisection_ce": replace_function(base, "_prospect_ce", ALT4_PROSPECT),
    "alt5_decimal_ce": replace_function(base, "_prospect_ce", ALT5_PROSPECT),
    "alt6_fd_step_1e-4": base.replace("_H = 1e-5  # finite-difference step", "_H = 1e-4  # finite-difference step", 1),
}
for name, text in out.items():
    d = HERE / "alts" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "elicit.py").write_text(text, encoding="utf-8")
    print("wrote", d / "elicit.py", len(text), "bytes", "H changed" if "_H = 1e-4" in text else "")
