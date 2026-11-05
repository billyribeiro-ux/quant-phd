"""Round-10 verifier (E3-d): repaired alternatives after the first run (alt1 polish stop rule, alt2 damping, alt4 full precision)."""
import pathlib, re
import importlib.util
HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("mk", HERE / "s3d_make_alts.py")
src = (HERE / "s3d_make_alts.py").read_text(encoding="utf-8")
REF = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")

def replace_function(text, name, new_body):
    pat = re.compile(rf"^def {name}\(.*?(?=^def |\Z)", re.S | re.M)
    m = pat.search(text)
    assert m, name
    return text[: m.start()] + new_body.rstrip() + "\n\n\n" + text[m.end():]

NEWTON_POLISH = '''
def _newton_polish(f, xi: list[float]) -> list[float]:
    """Damped Newton with the reference's stopping rule (max |score| < 1e-7) and a step only when f increases."""
    for _ in range(300):
        grad, hess = _gradient_and_hessian(f, xi)
        if max(abs(g) for g in grad) < 1e-7:
            return xi
        neg = [[-h for h in row] for row in hess]
        lower = None
        mu = 0.0
        while lower is None and mu < 1e6:
            lower = _cholesky([[neg[i][j] + (mu if i == j else 0.0) for j in range(3)] for i in range(3)])
            mu = max(mu * 10.0, 1e-8)
        step = _solve(lower, grad) if lower is not None else [0.05 * g for g in grad]
        base = f(xi)
        scale = 1.0
        while scale > 1e-14 and f([x + scale * s for x, s in zip(xi, step, strict=True)]) <= base:
            scale /= 2.0
        if scale <= 1e-14:
            return xi
        xi = [x + scale * s for x, s in zip(xi, step, strict=True)]
    return xi
'''

ALT1 = '''
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

ALT2 = '''
def _maximise(parsed: list[Parsed]) -> list[float]:
    """Newton on the log-likelihood with a central-difference gradient and Hessian at step 1e-6 (Gaussian elimination)."""
    def f(t: list[float]) -> float:
        return _objective(t, parsed)

    best_t = [0.0, 0.0, 0.0]
    best_v = -math.inf
    for c in (-2.0, 0.0, 2.0):
        for a in (-1.0, 0.5, 2.0):
            for b in (-1.0, 0.0, 1.0):
                v = f([c, a, b])
                if v > best_v:
                    best_v, best_t = v, [c, a, b]
    h = 1e-6
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
        if max(abs(x) for x in g) < 1e-7:
            return xi
        neg = [[-x for x in row] for row in H]
        lower = _cholesky(neg)
        step = _solve(lower, g) if lower is not None else [0.05 * x for x in g]
        scale = 1.0
        base = f(xi)
        while scale > 1e-14 and f([x + scale * s for x, s in zip(xi, step, strict=True)]) <= base:
            scale /= 2.0
        if scale <= 1e-14:
            return xi
        xi = [x + scale * s for x, s in zip(xi, step, strict=True)]
    return xi
'''

ALT4 = '''
def _prospect_ce(prizes: list[int], probs: list[Fraction], gamma: float, lam: float) -> float:
    """Unrounded prospect CE by bisection on the monotone value function, run to adjacent floats (full precision)."""
    total = sum(float(p) * _value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))
    lo, hi = float(min(prizes)), float(max(prizes))
    if lo == hi:
        return lo
    while True:
        mid = 0.5 * (lo + hi)
        if mid <= lo or mid >= hi:
            break
        v = _value(mid, gamma, lam) if mid >= 0 else -lam * math.pow(-mid, 1.0 - gamma)
        if v < total:
            lo = mid
        else:
            hi = mid
    return hi
'''

out = {
    "alt1b_grid_zoom_newton_damped": replace_function(REF, "_maximise", ALT1).replace("def _maximise", NEWTON_POLISH + "\n\ndef _maximise", 1),
    "alt2b_damped_newton_fd1e-6": replace_function(REF, "_maximise", ALT2),
    "alt4b_bisection_full_precision": replace_function(REF, "_prospect_ce", ALT4),
}
for name, text in out.items():
    d = HERE / "alts" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "elicit.py").write_text(text, encoding="utf-8")
    print("wrote", d / "elicit.py")
