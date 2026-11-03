"""Round-4 verifier (E3-d): independent check of Lab 3's estimate, SEs and optimum (own Nelder-Mead, own Hessian).

Reads ANSWERS from the page's Lab 3 code block (data only). Method is independent of reference.py and of the twin:
a grid of starts, a self-written Nelder-Mead (restarted) on the negative log-likelihood, then the observed information
at the best point by central differences at steps 1e-4 and 1e-5. Also evaluates the page's printed estimate.
"""
import html
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
src = (ROOT / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
block = html.unescape(re.search(r'id="lab-E3-project-3".*?<pre><code class="language-python" data-run>(.*?)</code></pre>', src, flags=re.S).group(1))
ANSWERS = eval(re.search(r"ANSWERS: list\[.*?\] = (\[.*?\n\])", block, flags=re.S).group(1), {})


def pv(x, g, lam):
    return float(x) ** (1 - g) if x >= 0 else -lam * float(-x) ** (1 - g)


def ce(prizes, probs, g, lam):
    w = sum(float(Fraction(p)) * pv(x, g, lam) for x, p in zip(prizes, probs))
    return w ** (1 / (1 - g)) if w >= 0 else -((-w / lam) ** (1 / (1 - g)))


def ll_g(g, lam, kap):
    t = 0.0
    for _, c, pa, qa, pb, qb in ANSWERS:
        z = kap * (ce(pa, qa, g, lam) - ce(pb, qb, g, lam)) / 10000.0
        t += -math.log1p(math.exp(-z)) if c == "A" else -math.log1p(math.exp(z))
    return t


def ll(xi):
    return ll_g(1 / (1 + math.exp(-xi[0])), math.exp(xi[1]), math.exp(xi[2]))


def nelder_mead(f, x0, step=0.5, iters=4000, tol=1e-12):
    n = len(x0)
    pts = [list(x0)] + [[x0[j] + (step if j == i else 0.0) for j in range(n)] for i in range(n)]
    vals = [f(p) for p in pts]
    for _ in range(iters):
        order = sorted(range(n + 1), key=lambda k: vals[k])
        pts = [pts[k] for k in order]
        vals = [vals[k] for k in order]
        if abs(vals[-1] - vals[0]) < tol and max(abs(a - b) for p in pts[1:] for a, b in zip(p, pts[0])) < 1e-10:
            break
        cen = [sum(p[j] for p in pts[:-1]) / n for j in range(n)]
        xr = [cen[j] + (cen[j] - pts[-1][j]) for j in range(n)]
        fr = f(xr)
        if vals[0] <= fr < vals[-2]:
            pts[-1], vals[-1] = xr, fr
        elif fr < vals[0]:
            xe = [cen[j] + 2 * (cen[j] - pts[-1][j]) for j in range(n)]
            fe = f(xe)
            pts[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        else:
            xc = [cen[j] + 0.5 * (pts[-1][j] - cen[j]) for j in range(n)]
            fc = f(xc)
            if fc < vals[-1]:
                pts[-1], vals[-1] = xc, fc
            else:
                pts = [pts[0]] + [[pts[0][j] + 0.5 * (p[j] - pts[0][j]) for j in range(n)] for p in pts[1:]]
                vals = [vals[0]] + [f(p) for p in pts[1:]]
    k = min(range(n + 1), key=lambda k: vals[k])
    return pts[k], -vals[k]


f_neg = lambda xi: -ll(xi)  # noqa: E731
best = None
results = []
for g0 in (0.1, 0.4, 0.7, 0.9):
    for l0 in (0.5, 2.0, 8.0):
        for k0 in (0.5, 2.0, 6.0):
            x = [math.log(g0 / (1 - g0)), math.log(l0), math.log(k0)]
            xb, val = nelder_mead(f_neg, x)
            xb, val = nelder_mead(f_neg, xb, step=0.05)
            results.append(val)
            if best is None or val > best[1]:
                best = (xb, val)
xi_best, val_best = best
print("own Nelder-Mead over 36 starts: best loglik", f"{val_best:.6f}", "| worst start result", f"{min(results):.6f}")
print("optimum: gamma", f"{1 / (1 + math.exp(-xi_best[0])):.6f}", "lambda", f"{math.exp(xi_best[1]):.6f}",
      "kappa", f"{math.exp(xi_best[2]):.6f}")
page = [math.log(0.6352 / (1 - 0.6352)), math.log(6.1503), math.log(2.0201)]
print("loglik at the page's printed estimate (rounded inputs):", f"{ll(page):.6f}")


def hess(xi, h):
    H = [[0.0] * 3 for _ in range(3)]
    f0 = ll(xi)
    for i in range(3):
        u = list(xi); u[i] += h
        d = list(xi); d[i] -= h
        H[i][i] = -(ll(u) - 2 * f0 + ll(d)) / (h * h)
        for j in range(i + 1, 3):
            pp = list(xi); pp[i] += h; pp[j] += h
            pm = list(xi); pm[i] += h; pm[j] -= h
            mp = list(xi); mp[i] -= h; mp[j] += h
            mm = list(xi); mm[i] -= h; mm[j] -= h
            H[i][j] = H[j][i] = -(ll(pp) - ll(pm) - ll(mp) + ll(mm)) / (4 * h * h)
    return H


def inv3(M):
    A = [list(r) + [1.0 if i == j else 0.0 for j in range(3)] for i, r in enumerate(M)]
    for c in range(3):
        p = max(range(c, 3), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        d = A[c][c]
        A[c] = [x / d for x in A[c]]
        for r in range(3):
            if r != c:
                fct = A[r][c]
                A[r] = [x - fct * y for x, y in zip(A[r], A[c])]
    return [r[3:] for r in A]


for label, xi in (("page estimate (rounded inputs)", page), ("own optimum", xi_best)):
    g, lam, kap = 1 / (1 + math.exp(-xi[0])), math.exp(xi[1]), math.exp(xi[2])
    for h in (1e-4, 1e-5, 1e-6):
        cov = inv3(hess(xi, h))
        if min(cov[i][i] for i in range(3)) <= 0:
            print(label, "step", h, "information not positive definite")
            continue
        print(label, "| step", f"{h:g}", "| se_gamma", f"{g * (1 - g) * math.sqrt(cov[0][0]):.4f}",
              "se_lambda", f"{lam * math.sqrt(cov[1][1]):.4f}", "se_kappa", f"{kap * math.sqrt(cov[2][2]):.4f}")
    sc = max(abs(ll([x + (1e-5 if k == i else 0) for k, x in enumerate(xi)]) -
                 ll([x - (1e-5 if k == i else 0) for k, x in enumerate(xi)])) / 2e-5 for i in range(3))
    print(label, "| largest score component (step 1e-5):", f"{sc:.3e}")
