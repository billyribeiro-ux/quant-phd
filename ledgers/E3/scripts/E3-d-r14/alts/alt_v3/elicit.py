"""Verifier alternative (round 14) to the E3 engine: Gauss-Seidel coordinate sweeps with bisection on the slope, then Newton polish; Nelder-Mead fallback if the information is not positive definite.

Written independently of grader/reference.py. Standard library only. Shared pieces: input checks, the prospect value,
the CRRA certainty equivalent, the logit log-likelihood with a stable log(1 + exp), and the observed information.
"""

from __future__ import annotations

import math
from decimal import ROUND_FLOOR, Decimal
from fractions import Fraction
from typing import Any

_MODELS = ("crra", "prospect")
def _half_up(y: float) -> int:
    """The nearest whole cent of a float, an exact half going toward plus infinity: floor(y + 1/2)."""
    return math.floor(y + 0.5)



def _check_model(model: object) -> str:
    if model not in _MODELS:
        raise ValueError('model must be "crra" or "prospect"')
    assert isinstance(model, str)
    return model


def _ints(values: Any) -> list[int]:
    out: list[int] = []
    for x in values:
        if isinstance(x, bool) or not isinstance(x, int):
            raise ValueError("prizes must be whole numbers of cents")
        out.append(x)
    if not out:
        raise ValueError("a lottery needs at least one prize")
    return out


def _probs(values: Any, count: int) -> list[Fraction]:
    if len(values) != count:
        raise ValueError("each prize needs exactly one probability")
    out: list[Fraction] = []
    for p in values:
        if isinstance(p, str):
            try:
                out.append(Fraction(p))
            except (ValueError, ZeroDivisionError) as err:
                raise ValueError("probabilities written as text must read numerator/denominator") from err
        elif isinstance(p, Fraction) or (isinstance(p, int) and not isinstance(p, bool)):
            out.append(Fraction(p))
        else:
            raise ValueError("probabilities must be exact fractions")
    if any(p < 0 for p in out) or sum(out, Fraction(0)) != 1:
        raise ValueError("probabilities must sum to 1 exactly, and none may be negative")
    return out


def _value(x: int, gamma: float, lam: float) -> float:
    if x >= 0:
        return float(x) ** (1.0 - gamma)
    return -lam * float(-x) ** (1.0 - gamma)


def _prospect_float(prizes: list[int], probs: list[Fraction], gamma: float, lam: float) -> float:
    total = sum(float(p) * _value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))
    if total >= 0.0:
        return total ** (1.0 / (1.0 - gamma))
    return -((-total / lam) ** (1.0 / (1.0 - gamma)))


def _crra_exact_or_float(prizes: list[int], probs: list[Fraction], gamma: float, wealth: int) -> int:
    if gamma == 0.0:
        expected = sum((p * x for p, x in zip(probs, prizes, strict=True)), Fraction(0))
        return math.floor(expected + Fraction(1, 2))
    finals = [wealth + x for x in prizes]
    if gamma == 1.0:
        change = math.exp(sum(float(p) * math.log(w) for p, w in zip(probs, finals, strict=True))) - wealth
    else:
        change = sum(float(p) * float(w) ** (1.0 - gamma) for p, w in zip(probs, finals, strict=True))
        change = change ** (1.0 / (1.0 - gamma)) - wealth
    return _half_up(change)


def _parse_response(r: Any) -> tuple[list[int], list[Fraction], list[int], list[Fraction], str]:
    pa = _ints(r["prizes_a"])
    qa = _probs(r["probs_a"], len(pa))
    pb = _ints(r["prizes_b"])
    qb = _probs(r["probs_b"], len(pb))
    choice = r["choice"]
    if choice not in ("A", "B"):
        raise ValueError('choice must be "A" or "B"')
    return pa, qa, pb, qb, choice


def _log1pexp(t: float) -> float:
    if t > 0.0:
        return t + math.log1p(math.exp(-t))
    return math.log1p(math.exp(t))


def _loglik(parsed: list[tuple[list[int], list[Fraction], list[int], list[Fraction], str]], gamma: float, lam: float, kappa: float) -> float:
    total = 0.0
    for pa, qa, pb, qb, choice in parsed:
        z = kappa * (_prospect_float(pa, qa, gamma, lam) - _prospect_float(pb, qb, gamma, lam)) / 10_000.0
        total += -_log1pexp(-z) if choice == "A" else -_log1pexp(z)
    return total


def _f(xi: list[float], parsed: list[Any]) -> float:
    gamma = 1.0 / (1.0 + math.exp(-xi[0]))
    if xi[0] > 60.0 or xi[0] < -60.0 or abs(xi[1]) > 60.0 or abs(xi[2]) > 60.0:
        return -math.inf
    return _loglik(parsed, gamma, math.exp(xi[1]), math.exp(xi[2]))


def _grid_start(parsed: list[Any]) -> list[float]:
    best: tuple[float, list[float]] | None = None
    for g in (0.1, 0.3, 0.5, 0.7, 0.9):
        for lam in (0.5, 1.0, 2.0, 4.0, 8.0):
            for kappa in (0.3, 1.0, 3.0, 6.0):
                xi = [math.log(g / (1.0 - g)), math.log(lam), math.log(kappa)]
                v = _f(xi, parsed)
                if best is None or v > best[0]:
                    best = (v, xi)
    assert best is not None
    return best[1]


def _grad(xi: list[float], parsed: list[Any], h: float) -> list[float]:
    out = []
    for i in range(3):
        up, down = list(xi), list(xi)
        up[i] += h
        down[i] -= h
        out.append((_f(up, parsed) - _f(down, parsed)) / (2.0 * h))
    return out


def _hessian_neg(xi: list[float], parsed: list[Any], h: float) -> list[list[float]]:
    f0 = _f(xi, parsed)
    m = [[0.0] * 3 for _ in range(3)]

    def at(*moves: tuple[int, float]) -> float:
        y = list(xi)
        for k, d in moves:
            y[k] += d
        return _f(y, parsed)

    for i in range(3):
        m[i][i] = -(at((i, h)) - 2.0 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4.0 * h * h)
            m[i][j] = m[j][i] = v
    return m


def _inverse3(m: list[list[float]]) -> list[list[float]]:
    a, b, c = m[0]
    d, e, f = m[1]
    g, hh, i = m[2]
    det = a * (e * i - f * hh) - b * (d * i - f * g) + c * (d * hh - e * g)
    return [
        [(e * i - f * hh) / det, (c * hh - b * i) / det, (b * f - c * e) / det],
        [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
        [(d * hh - e * g) / det, (b * g - a * hh) / det, (a * e - b * d) / det],
    ]


def _newton(xi: list[float], parsed: list[Any], h: float = 1e-4, steps: int = 60) -> list[float]:
    """Newton polish with central-difference gradient and Hessian; halves the step while the likelihood falls."""
    for _ in range(steps):
        g = _grad(xi, parsed, h)
        if max(abs(v) for v in g) < 1e-9:
            break
        neg_h = _hessian_neg(xi, parsed, h)
        det = neg_h[0][0] * (neg_h[1][1] * neg_h[2][2] - neg_h[1][2] * neg_h[2][1]) - neg_h[0][1] * (
            neg_h[1][0] * neg_h[2][2] - neg_h[1][2] * neg_h[2][0]) + neg_h[0][2] * (
            neg_h[1][0] * neg_h[2][1] - neg_h[1][1] * neg_h[2][0])
        if det <= 0.0 or neg_h[0][0] <= 0.0:
            break  # not a maximum locally: leave the point to the caller's check
        inv = _inverse3(neg_h)
        step = [sum(inv[i][j] * g[j] for j in range(3)) for i in range(3)]
        t, f0, s = 1.0, _f(xi, parsed), 1.0
        for _ in range(60):
            cand = [x + t * d for x, d in zip(xi, step, strict=True)]
            if _f(cand, parsed) >= f0:
                break
            t *= 0.5
        xi = cand
        if max(abs(t * d) for d in step) < 1e-15:
            break
        _ = s
    return xi


def _is_pd(m: list[list[float]]) -> bool:
    """True when the symmetric 3 by 3 matrix is positive definite (Cholesky succeeds with positive pivots)."""
    lower = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(i + 1):
            s = m[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if not s > 0.0:
                    return False
                lower[i][i] = math.sqrt(s)
            else:
                lower[i][j] = s / lower[j][j]
    return True


def _estimate_from(xi: list[float], parsed: list[Any], h_se: float) -> dict[str, float]:
    if min(max(abs(v) for v in _grad(xi, parsed, h)) for h in (1e-5, 1e-6)) > 1e-5:
        raise RuntimeError("the search stopped before a stationary point: the maximisation did not converge")
    gamma = 1.0 / (1.0 + math.exp(-xi[0]))
    lam, kappa = math.exp(xi[1]), math.exp(xi[2])
    cov = _inverse3(_hessian_neg(xi, parsed, h_se))
    return {
        "gamma_hat": gamma,
        "lambda_hat": lam,
        "kappa_hat": kappa,
        "se_gamma": gamma * (1.0 - gamma) * math.sqrt(cov[0][0]),
        "se_lambda": lam * math.sqrt(cov[1][1]),
        "se_kappa": kappa * math.sqrt(cov[2][2]),
        "log_likelihood": _f(xi, parsed),
    }


def _prepare(responses: Any) -> list[Any]:
    if not responses:
        raise ValueError("need at least one response, and mixed-sign lotteries, to identify loss aversion")
    parsed = [_parse_response(r) for r in responses]
    def mixed(prizes: list[int], probs: list[Fraction]) -> bool:
        return any(x > 0 and p > 0 for x, p in zip(prizes, probs, strict=True)) and any(
            x < 0 and p > 0 for x, p in zip(prizes, probs, strict=True))
    if not any(mixed(a, qa) or mixed(b, qb) for a, qa, b, qb, _ in parsed):
        raise ValueError("need mixed-sign lotteries to identify loss aversion")
    return parsed


def log_likelihood(responses: list[dict[str, object]], params: dict[str, float]) -> float:
    gamma, lam, kappa = float(params["gamma"]), float(params["lambda"]), float(params["kappa"])
    if not 0.0 <= gamma < 1.0 or not lam > 0.0 or not kappa > 0.0:
        raise ValueError("the prospect model needs 0 <= gamma < 1, lambda > 0 and kappa > 0")
    return _loglik([_parse_response(r) for r in responses], gamma, lam, kappa)


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
    return _half_up(_prospect_float(prizes, probs, gamma, lam))


def estimate(responses: list[dict[str, object]]) -> dict[str, float]:
    """Maximum-likelihood estimates under the prospect model, with standard errors from the observed information."""
    parsed = _prepare(responses)
    start = _grid_start(parsed)
    xi = _coordinate_sweeps(start, parsed)
    xi = _polish(xi, parsed)
    if not _is_pd(_hessian_neg(xi, parsed, 1e-5)):
        xi = _polish(_bfgs(_nelder_mead(lambda x: -_f(x, parsed), start), parsed), parsed)
    return _estimate_from(xi, parsed, 1e-5)
