"""Slice d round 1: recompute every number in the project page's labs and prose from first principles (own code).

Run from the checkout root: python3 -I ledgers/M5/scripts/M5-d-r1/d_numbers_project.py
Independent of the page's twins: a fresh implementation of the model with exact floats printed in full.
"""

import math
import random

BETA, ALPHA = 0.9, 0.5
G1 = [0.5, 0.9, 1.4]


def res(k, a):
    return k**a


def bell(grid, beta, alpha, V):
    out = []
    for k in grid:
        r = res(k, alpha)
        out.append(max(math.sqrt(r - kp) + beta * V[j] for j, kp in enumerate(grid) if kp <= r))
    return out


def supd(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


print("== Lab 1 (grid 0.5, 0.9, 1.4; beta 0.9; alpha 0.5)")
print("resources", [repr(res(k, ALPHA)) for k in G1])
V0 = [0.0] * 3
V1 = bell(G1, BETA, ALPHA, V0)
print("V1", [repr(x) for x in V1])
print("B V0 vs B V1 sup:", repr(supd(bell(G1, BETA, ALPHA, V0), bell(G1, BETA, ALPHA, V1))), " beta*sup|V0-V1|:", repr(BETA * supd(V0, V1)))
print("sweep1 change", repr(supd(V1, V0)), "certified", repr(BETA / (1 - BETA) * supd(V1, V0)))
V = V0
n = 0
cert = math.inf
hist = []
while cert > 1e-6:
    n += 1
    new = bell(G1, BETA, ALPHA, V)
    ch = supd(new, V)
    cert = BETA / (1 - BETA) * ch
    V = new
    hist.append((n, ch, cert))
print("sweep 2 cert", repr(hist[1][2]), "sweep3 change", repr(hist[2][1]), "sweep3 cert", repr(hist[2][2]))
print("stop sweep", n, "last change", repr(hist[-1][1]), "certified", repr(hist[-1][2]))
# reference fixed point at 1e-12
R = [0.0] * 3
while True:
    nx = bell(G1, BETA, ALPHA, R)
    small = BETA / (1 - BETA) * supd(nx, R) <= 1e-12
    R = nx
    if small:
        break
actual = supd(V, R)
print("actual error", repr(actual), "certified", repr(hist[-1][2]), "diff", repr(hist[-1][2] - actual))
print("V after stop", [repr(x) for x in V])

print("== Lab 2 completion")
ratio_v = [0.0, 0.0, 0.0]
ratio_w = [0.1, 0.2, 0.3]
ratio = supd(bell(G1, BETA, ALPHA, ratio_v), bell(G1, BETA, ALPHA, ratio_w)) / supd(ratio_v, ratio_w)
print("ratio", repr(ratio), "ratio<=beta", ratio <= BETA)
# completed lines: certified = beta/(1-beta) * change
Vv = [0.0, 0.0, 0.0]
nn = 0
c = math.inf
while c > 1e-6 and nn < 300:
    nn += 1
    new = bell(G1, BETA, ALPHA, Vv)
    chg = supd(new, Vv)
    c = BETA / (1 - BETA) * chg
    Vv = new
print("lab2 sweeps", nn, "cert", repr(c), "last change", repr(chg), "values", [f"{x:.6f}" for x in Vv])
print("cert/1e-7 digits:", f"{c:.3e}", f"{chg:.3e}")
print("9.495187e-7 vs computed", repr(c), "abs diff", abs(c - 9.495187e-7))

print("== Lab 3 (beta 0.9, alpha 0.3, grid 0.45..2.70 step 0.25, tol 1e-10)")
A3 = 0.3
G3 = [0.45 + 0.25 * j for j in range(10)]
gap = min(abs(kp - res(k, A3)) for k in G3 for kp in G3)
print("smallest gap", repr(gap))
Vs = [0.0] * 10
sw = 0
cert = math.inf
chg = math.inf
while cert > 1e-10:
    new = bell(G3, BETA, A3, Vs)
    chg = supd(new, Vs)
    cert = BETA / (1 - BETA) * chg
    Vs = new
    sw += 1
print("sweeps", sw, "last change", repr(chg), "cert", repr(cert))
U = math.sqrt(max(G3) ** A3)
na = 0
while BETA**na * U / (1 - BETA) > 1e-10:
    na += 1
print("a priori count", na, "U", repr(U))
resid = supd(bell(G3, BETA, A3, Vs), Vs)
print("residual", repr(resid), "(1+beta)*cert", repr((1 + BETA) * cert))
rng = random.Random(7)
worst = 0.0
for _ in range(200):
    v = [rng.uniform(0.0, 4.0) for _ in G3]
    w = [rng.uniform(0.0, 4.0) for _ in G3]
    worst = max(worst, supd(bell(G3, BETA, A3, v), bell(G3, BETA, A3, w)) / supd(v, w))
print("worst ratio 200 pairs", repr(worst), "minus beta", worst - BETA)
print("V values", [f"{x:.6f}" for x in Vs])
print("prose: last change 1.025e-11 ->", f"{chg:.3e}", "; cert 9.226e-11 ->", f"{cert:.3e}")
print("Lab 3 Numerical check: 1.025e-11 *9 =", 1.025e-11 * 9, "; 9.226e-11 /9 =", 9.226e-11 / 9)
