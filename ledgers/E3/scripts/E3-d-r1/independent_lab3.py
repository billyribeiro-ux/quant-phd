"""Independent check of Lab 3 printed numbers: pattern search in (gamma, lambda, kappa) with no shared code."""
import math, re, sys
from fractions import Fraction
src = open("course/modules/E/E3/project.html", encoding="utf-8").read()
blk = src[src.index("ANSWERS: list"):src.index("\n]\n", src.index("ANSWERS: list"))]
rows = re.findall(r"\((\d+), \"([AB])\", \[([^\]]*)\], \[([^\]]*)\], \[([^\]]*)\], \[([^\]]*)\]\)", blk)
data = []
for pid, ch, a, qa, b, qb in rows:
    pa = [int(x) for x in a.split(",")]; pb = [int(x) for x in b.split(",")]
    qa_ = [Fraction(t.strip().strip('"')) for t in qa.split(",")]
    qb_ = [Fraction(t.strip().strip('"')) for t in qb.split(",")]
    data.append((pa, qa_, pb, qb_, ch))
def ce(prizes, probs, g, lam):
    tot = 0.0
    for x, p in zip(prizes, probs):
        pf = float(p)
        tot += pf * (x ** (1 - g) if x >= 0 else -lam * (-x) ** (1 - g))
    if tot >= 0:
        return tot ** (1 / (1 - g))
    return -((-tot / lam) ** (1 / (1 - g)))
def ll(th):
    g = 1 / (1 + math.exp(-th[0])); lam = math.exp(th[1]); k = math.exp(th[2])
    s = 0.0
    for pa, qa, pb, qb, ch in data:
        z = k * (ce(pa, qa, g, lam) - ce(pb, qb, g, lam)) / 10000.0
        s += -math.log1p(math.exp(-z)) if ch == "A" else -math.log1p(math.exp(z))
    return s
# pattern search from several starts
best = None
for g0 in (0.2, 0.5, 0.8):
    for l0 in (1.0, 3.0, 8.0):
        for k0 in (0.5, 2.0, 6.0):
            th = [math.log(g0 / (1 - g0)), math.log(l0), math.log(k0)]
            f = ll(th); step = 0.5
            while step > 1e-10:
                improved = False
                for i in range(3):
                    for s in (step, -step):
                        t2 = list(th); t2[i] += s
                        f2 = ll(t2)
                        if f2 > f:
                            th, f, improved = t2, f2, True
                if not improved:
                    step /= 2
            if best is None or f > best[0]:
                best = (f, th)
f, th = best
g = 1 / (1 + math.exp(-th[0])); lam = math.exp(th[1]); k = math.exp(th[2])
print(f"independent: gamma_hat={g:.6f} lambda_hat={lam:.6f} kappa_hat={k:.6f} loglik={f:.6f}")
# numerical Hessian in theta coords, step 1e-4, for standard errors
h = 1e-4; n = 3
H = [[0.0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        def at(di, dj):
            t = list(th); t[i] += di; t[j] += dj
            return ll(t)
        if i == j:
            H[i][i] = (at(h, 0) - 2*f + at(-h, 0)) / (h*h)
        else:
            H[i][j] = (at(h, h) - at(h, -h) - at(-h, h) + at(-h, -h)) / (4*h*h)
I = [[-H[i][j] for j in range(n)] for i in range(n)]
def inv3(m):
    a = [row[:] + [1.0 if i == j else 0.0 for j in range(3)] for i, row in enumerate(m)]
    for c in range(3):
        p = max(range(c, 3), key=lambda r: abs(a[r][c])); a[c], a[p] = a[p], a[c]
        d = a[c][c]; a[c] = [x / d for x in a[c]]
        for r in range(3):
            if r != c:
                fct = a[r][c]; a[r] = [x - fct*y for x, y in zip(a[r], a[c])]
    return [row[3:] for row in a]
C = inv3(I)
se_g = g*(1-g)*math.sqrt(C[0][0]); se_l = lam*math.sqrt(C[1][1]); se_k = k*math.sqrt(C[2][2])
print(f"independent: se_gamma={se_g:.4f} se_lambda={se_l:.4f} se_kappa={se_k:.4f}")
gr = [(ll([th[0]+d, th[1], th[2]]) - ll([th[0]-d, th[1], th[2]]))/(2*d) for d in (1e-6,)]
print("score coords approx", [ (ll(th[:i]+[th[i]+1e-6]+th[i+1:]) - ll(th[:i]+[th[i]-1e-6]+th[i+1:]))/2e-6 for i in range(3)])
