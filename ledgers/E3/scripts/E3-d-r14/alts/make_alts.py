"""Writes the five verifier alternatives (round 14) as complete elicit.py modules next to this script.

Each alternative shares input checks, the prospect value and the likelihood (common_head.py) and differs in the
numerical method: alt_v1 Nelder-Mead then Newton; alt_v2 BFGS then Newton; alt_v3 coordinate root bisection sweeps then
Newton; alt_v4 Nelder-Mead then Newton, with the public certainty equivalent by bisection inversion of v (no closed
form); alt_v5 Nelder-Mead then BFGS, with the half-cent rule applied to the decimal value of the float.
"""

from __future__ import annotations

import pathlib

HERE = pathlib.Path(__file__).resolve().parent
HEAD = (HERE / "common_head.py").read_text(encoding="utf-8")

HALF_FLOAT = '''def _half_up(y: float) -> int:
    """The nearest whole cent of a float, an exact half going toward plus infinity: floor(y + 1/2)."""
    return math.floor(y + 0.5)
'''

HALF_DECIMAL = '''def _half_up(y: float) -> int:
    """The nearest whole cent, an exact half toward plus infinity, applied to the decimal value of the float itself."""
    return int((Decimal(repr(y)) + Decimal("0.5")).to_integral_value(rounding=ROUND_FLOOR))
'''

NELDER_MEAD = '''

def _nelder_mead(f: Any, x0: list[float], max_iter: int = 4000) -> list[float]:
    """Nelder-Mead simplex on f (minimised), written out by hand: reflection, expansion, contraction, shrink."""
    pts = [list(x0)]
    for i in range(3):
        p = list(x0)
        p[i] += 0.5
        pts.append(p)
    vals = [f(p) for p in pts]
    for _ in range(max_iter):
        order = sorted(range(4), key=lambda k: vals[k])
        pts = [pts[k] for k in order]
        vals = [vals[k] for k in order]
        size = max(max(abs(a - b) for a, b in zip(p, pts[0], strict=True)) for p in pts[1:])
        if vals[3] - vals[0] < 1e-12 and size < 1e-10:
            break
        c = [sum(p[i] for p in pts[:3]) / 3.0 for i in range(3)]
        xr = [c[i] + (c[i] - pts[3][i]) for i in range(3)]
        fr = f(xr)
        if vals[0] <= fr < vals[2]:
            pts[3], vals[3] = xr, fr
            continue
        if fr < vals[0]:
            xe = [c[i] + 2.0 * (c[i] - pts[3][i]) for i in range(3)]
            fe = f(xe)
            pts[3], vals[3] = (xe, fe) if fe < fr else (xr, fr)
            continue
        xc = [c[i] + 0.5 * (pts[3][i] - c[i]) for i in range(3)]
        fc = f(xc)
        if fc < vals[3]:
            pts[3], vals[3] = xc, fc
            continue
        best = pts[0]
        pts = [best] + [[best[i] + 0.5 * (p[i] - best[i]) for i in range(3)] for p in pts[1:]]
        vals = [vals[0]] + [f(p) for p in pts[1:]]
    return pts[0]
'''

BFGS = '''

def _bfgs(xi: list[float], parsed: list[Any], h: float = 1e-6, max_iter: int = 400) -> list[float]:
    """BFGS on the log-likelihood with central-difference gradients and Armijo backtracking."""
    x = list(xi)
    fx = _f(x, parsed)
    g = _grad(x, parsed, h)
    hinv = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    for _ in range(max_iter):
        if max(abs(v) for v in g) < 1e-9:
            break
        d = [-sum(hinv[i][j] * g[j] for j in range(3)) for i in range(3)]
        slope = sum(di * gi for di, gi in zip(d, g, strict=True))
        if slope >= 0.0:
            hinv = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
            d = [-v for v in g]
            slope = sum(di * gi for di, gi in zip(d, g, strict=True))
        t = 1.0
        while True:
            xn = [x[i] + t * d[i] for i in range(3)]
            fn = _f(xn, parsed)
            if fn >= fx + 1e-4 * t * slope or t < 1e-12:
                break
            t *= 0.5
        if t < 1e-12:
            break
        gn = _grad(xn, parsed, h)
        s = [xn[i] - x[i] for i in range(3)]
        y = [gn[i] - g[i] for i in range(3)]
        sy = sum(s[i] * y[i] for i in range(3))
        if sy > 1e-18:
            rho = 1.0 / sy
            v = [[(1.0 if i == j else 0.0) - rho * s[i] * y[j] for j in range(3)] for i in range(3)]
            hinv = [
                [
                    sum(v[i][k] * hinv[k][m] * v[j][m] for k in range(3) for m in range(3)) + rho * s[i] * s[j]
                    for j in range(3)
                ]
                for i in range(3)
            ]
        x, fx, g = xn, fn, gn
    return x


def _polish(xi: list[float], parsed: list[Any]) -> list[float]:
    """Newton polish; where Newton stops short of a stationary point, BFGS again, then Newton, up to four rounds."""
    for _ in range(4):
        xi = _newton(xi, parsed, h=1e-6)
        if max(abs(v) for v in _grad(xi, parsed, 1e-5)) <= 1e-6:
            break
        xi = _bfgs(xi, parsed, h=1e-6, max_iter=200)
    return xi
'''

SWEEPS = '''

def _coordinate_sweeps(xi: list[float], parsed: list[Any], sweeps: int = 8) -> list[float]:
    """Gauss-Seidel sweeps: in each coordinate, bisect the sign of the central-difference slope within one unit."""
    x = list(xi)
    for _ in range(sweeps):
        for i in range(3):

            def slope(t: float, i: int = i) -> float:
                y = list(x)
                y[i] = t + 1e-7
                up = _f(y, parsed)
                y[i] = t - 1e-7
                return up - _f(y, parsed)

            lo, hi = x[i] - 1.0, x[i] + 1.0
            if slope(lo) > 0.0 and slope(hi) < 0.0:
                for _ in range(50):
                    mid = 0.5 * (lo + hi)
                    if slope(mid) > 0.0:
                        lo = mid
                    else:
                        hi = mid
                x[i] = 0.5 * (lo + hi)
    return x
'''

BISECT_CE = '''

def _prospect_bisect(prizes: list[int], probs: list[Fraction], gamma: float, lam: float) -> float:
    """The sure change c with v(c) equal to the lottery value, found by bisection on [least prize, greatest prize]."""
    total = sum(float(p) * _value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))
    lo, hi = float(min(prizes)), float(max(prizes))
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _value(mid, gamma, lam) < total:  # type: ignore[arg-type]
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)
'''

PUBLIC_CE = '''

def certainty_equivalent_cents(
    model: str,
    prizes_cents: list[int],
    probabilities: list[Fraction],
    params: dict[str, float],
    wealth_cents: int,
) -> int:
    """The certainty equivalent in whole cents, rounded once with an exact half going up."""
    name = _check_model(model)
    prizes = _ints(prizes_cents)
    probs = _probs(probabilities, len(prizes))
    if isinstance(wealth_cents, bool) or not isinstance(wealth_cents, int):
        raise ValueError("wealth_cents must be a whole number of cents")
    gamma = float(params["gamma"])
    if name == "crra":
        if any(wealth_cents + x <= 0 for x in prizes):
            raise ValueError("wealth plus prize must stay positive")
        return _crra_exact_or_float(prizes, probs, gamma, wealth_cents)
    lam = float(params["lambda"])
    if not (0.0 <= gamma < 1.0 and lam > 0.0):
        raise ValueError("the prospect model needs 0 <= gamma < 1 and lambda > 0")
    return _half_up(__PCE__(prizes, probs, gamma, lam))
'''

ESTIMATE = '''

def estimate(responses: list[dict[str, object]]) -> dict[str, float]:
    """Maximum-likelihood estimates under the prospect model, with standard errors from the observed information."""
    parsed = _prepare(responses)
    start = _grid_start(parsed)
    __SEARCH__
    return _estimate_from(xi, parsed, __HSE__)
'''

VARIANTS = {
    "alt_v1": dict(
        doc="Nelder-Mead on the negative log-likelihood, then a Newton polish (central differences, step 1e-4).",
        round=HALF_FLOAT, pce="_prospect_float", extra=NELDER_MEAD + BFGS,
        search="xi = _nelder_mead(lambda x: -_f(x, parsed), start)\n    xi = _polish(xi, parsed)",
        hse="1e-5",
    ),
    "alt_v2": dict(
        doc="BFGS from the grid start; if that stops short of a stationary point, Nelder-Mead then BFGS; then Newton.",
        round=HALF_FLOAT, pce="_prospect_float", extra=NELDER_MEAD + BFGS,
        search=(
            "xi = _bfgs(start, parsed)\n    if min(max(abs(v) for v in _grad(xi, parsed, h)) for h in (1e-5, 1e-6)) > 1e-6:\n"
            "        xi = _bfgs(_nelder_mead(lambda x: -_f(x, parsed), start), parsed)\n"
            "    xi = _polish(xi, parsed)"
        ),
        hse="1e-6",
    ),
    "alt_v3": dict(
        doc="Gauss-Seidel coordinate sweeps with bisection on the slope, then Newton polish; Nelder-Mead fallback if the information is not positive definite.",
        round=HALF_FLOAT, pce="_prospect_float", extra=NELDER_MEAD + SWEEPS + BFGS,
        search=(
            "xi = _coordinate_sweeps(start, parsed)\n    xi = _polish(xi, parsed)\n"
            "    if not _is_pd(_hessian_neg(xi, parsed, 1e-5)):\n"
            "        xi = _polish(_bfgs(_nelder_mead(lambda x: -_f(x, parsed), start), parsed), parsed)"
        ),
        hse="1e-5",
    ),
    "alt_v4": dict(
        doc="Nelder-Mead and Newton as alt_v1; the public certainty equivalent is a bisection inversion of v.",
        round=HALF_FLOAT, pce="_prospect_bisect", extra=NELDER_MEAD + BFGS + BISECT_CE,
        search="xi = _nelder_mead(lambda x: -_f(x, parsed), start)\n    xi = _polish(xi, parsed)",
        hse="1e-5",
    ),
    "alt_v5": dict(
        doc="Nelder-Mead then BFGS (no Newton); the half-cent rule is applied to the decimal value of the float.",
        round=HALF_DECIMAL, pce="_prospect_float", extra=NELDER_MEAD + BFGS,
        search="xi = _nelder_mead(lambda x: -_f(x, parsed), start)\n    xi = _bfgs(xi, parsed, h=1e-6)",
        hse="1e-5",
    ),
}


def build(name: str) -> str:
    v = VARIANTS[name]
    head = HEAD.replace("__DOC__", v["doc"]).replace("__ROUND__", v["round"]).replace("__HALF__", "_half_up")
    head = head.replace("__HALF__", "_half_up")
    body = v["extra"] + PUBLIC_CE.replace("__PCE__", v["pce"])
    if v["pce"] == "_prospect_bisect":
        pass
    est = ESTIMATE.replace("__SEARCH__", v["search"]).replace("__HSE__", v["hse"])
    return head + body + est


if __name__ == "__main__":
    for name in VARIANTS:
        out = HERE / name / "elicit.py"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build(name), encoding="utf-8")
        print("wrote", out)
