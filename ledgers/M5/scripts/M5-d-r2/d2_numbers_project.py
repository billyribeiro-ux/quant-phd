"""Independent recomputation of every number on course/modules/M/M5/project.html (round 2, verifier).

Written from the page's conventions, not from the lab code. Prints unrounded values.
"""

import math
import random


def run(beta, alpha, grid, tol_stop, start=None):
    """Value iteration from start (default zero), synchronous sweeps, returns list of (n, change, certified, values)."""
    v = [0.0] * len(grid) if start is None else list(start)
    hist = []
    n = 0
    while True:
        n += 1
        new = []
        for k in grid:
            cap = k**alpha
            cands = [math.sqrt(cap - kp) + beta * v[j] for j, kp in enumerate(grid) if kp <= cap]
            new.append(max(cands))
        change = max(abs(a - b) for a, b in zip(new, v))
        cert = beta / (1 - beta) * change
        hist.append((n, change, cert, new))
        v = new
        if tol_stop is not None and cert <= tol_stop:
            return hist
        if tol_stop is None and n >= 400:
            return hist


def B(beta, alpha, grid, v):
    out = []
    for k in grid:
        cap = k**alpha
        out.append(max(math.sqrt(cap - kp) + beta * v[j] for j, kp in enumerate(grid) if kp <= cap))
    return out


def sup(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


print("== Lab 1 (grid 0.5,0.9,1.4; beta .9; alpha .5)")
G1 = [0.5, 0.9, 1.4]
b1, a1 = 0.9, 0.5
V1 = B(b1, a1, G1, [0.0, 0.0, 0.0])
print("V1 unrounded:", V1)
print("contraction lhs/rhs:", sup(B(b1, a1, G1, [0, 0, 0]), B(b1, a1, G1, V1)), b1 * sup([0, 0, 0], V1))
h1 = run(b1, a1, G1, 1e-6)
for n, ch, c, _ in h1[:3]:
    print("sweep", n, "change", ch, "cert", c)
n_stop, ch_stop, c_stop, vstop = h1[-1]
print("stop sweep", n_stop, "change", ch_stop, "cert", c_stop, "values", vstop)
# reference fixed point to 1e-12
ref = run(b1, a1, G1, 1e-12)[-1][3]
actual = sup(vstop, ref)
print("actual error unrounded", actual, "certified unrounded", c_stop)
print("difference actual - certified", actual - c_stop, "ratio actual/cert", actual / c_stop)
print("9.495187e-7 check: cert_stop =", c_stop, " prints 9.495e-07 :", f"{c_stop:.3e}", " 9dp:", f"{c_stop:.9f}")

print("== Lab 2 ratio for V=0, W=(0.1,0.2,0.3)")
W = [0.1, 0.2, 0.3]
ratio = sup(B(b1, a1, G1, [0, 0, 0]), B(b1, a1, G1, W)) / sup([0, 0, 0], W)
print("ratio unrounded", ratio, "ratio <= beta", ratio <= b1)
h2 = run(b1, a1, G1, 1e-6)
print("lab2 stop sweep", h2[-1][0], "cert", h2[-1][2], "change", h2[-1][1])

print("== Lab 3 (beta .9 alpha .3, 10 points 0.45+0.25j)")
G3 = [0.45 + 0.25 * j for j in range(10)]
b3, a3, tol3 = 0.9, 0.3, 1e-10
gap = min(abs(kp - k**a3) for k in G3 for kp in G3)
print("smallest gap unrounded", gap)
h3 = run(b3, a3, G3, tol3)
n3, ch3, c3, v3 = h3[-1]
print("sweeps", n3, "change", ch3, "cert", c3)
U = math.sqrt(max(G3) ** a3)
na = 0
while b3**na * U / (1 - b3) > tol3:
    na += 1
print("a priori count (own loop)", na, " sweeps <= count+1:", n3 <= na + 1)
res = sup(B(b3, a3, G3, v3), v3)
print("residual unrounded", res, " (1+beta)*cert", (1 + b3) * c3, " holds", res <= (1 + b3) * c3)
rng = random.Random(7)
worst = 0.0
for _ in range(200):
    v = [rng.uniform(0.0, 4.0) for _ in G3]
    w = [rng.uniform(0.0, 4.0) for _ in G3]
    worst = max(worst, sup(B(b3, a3, G3, v), B(b3, a3, G3, w)) / sup(v, w))
print("largest ratio over 200 seeded pairs (seed 7, own RNG draws)", worst, " <= beta+1e-12", worst <= b3 + 1e-12)
for k, val in zip(G3, v3):
    print(f"V({k}) = {val:.6f}   unrounded {val!r}")
print("G3[-1] repr", repr(G3[-1]))
