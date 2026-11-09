"""Independent recomputation of every number the M5 project page states (round 3, slice d).

Written by the verifier from the page's definitions only (not from the lab twins). Run: python3 -I <this file>.
"""

import math
import random

BETA, ALPHA, GRID = 0.9, 0.5, [0.5, 0.9, 1.4]


def res(k, a=ALPHA):
    return k**a


def bell(v, beta=BETA, alpha=ALPHA, grid=GRID):
    out = []
    for k in grid:
        r = res(k, alpha)
        out.append(max(math.sqrt(r - kp) + beta * v[j] for j, kp in enumerate(grid) if kp <= r))
    return out


def sup(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


print("Lab1 resources", [f"{res(k):.6f}" for k in GRID])
v0 = [0.0] * 3
v1 = bell(v0)
print("Lab1 V1", [f"{x:.6f}" for x in v1])
print("Lab1 contraction lhs/rhs", f"{sup(bell(v0), bell(v1)):.6f}", f"{BETA * sup(v0, v1):.6f}")
print("Lab1 sweep1 change/cert", f"{sup(v1, v0):.6f}", f"{BETA / (1 - BETA) * sup(v1, v0):.6f}", "exact cert", BETA / (1 - BETA) * sup(v1, v0))
vals = v0
n = 0
cert = math.inf
change = None
chg_hist = []
while cert > 1e-6:
    n += 1
    new = bell(vals)
    change = sup(new, vals)
    cert = BETA / (1 - BETA) * change
    vals = new
    chg_hist.append((n, change, cert))
print("Lab1 stop sweep", n, "change", f"{change:.12e}", "cert", f"{cert:.12e}")
ref = v0
for _ in range(100000):
    nxt = bell(ref)
    small = BETA / (1 - BETA) * sup(nxt, ref) <= 1e-12
    ref = nxt
    if small:
        break
actual = sup(vals, ref)
print("Lab1 actual error", f"{actual:.12e}", "cert", f"{cert:.12e}", "diff", f"{cert - actual:.3e}")
print("Lab1 values after stop", [f"{x:.6f}" for x in vals])

# Lab 2: ratio for V=0, W=(0.1,0.2,0.3)
v, w = [0.0] * 3, [0.1, 0.2, 0.3]
ratio = sup(bell(v), bell(w)) / sup(v, w)
print("Lab2 ratio", f"{ratio:.12f}", "beta", BETA)
vals = [0.0] * 3
n = 0
cert = math.inf
while cert > 1e-6 and n < 300:
    n += 1
    new = bell(vals)
    change = sup(new, vals)
    cert = BETA / (1 - BETA) * change
    vals = new
print("Lab2 sweeps", n, "cert", f"{cert:.12e}", "change", f"{change:.12e}")

# Lab 3
B3, A3 = 0.9, 0.3
G3 = [0.45 + 0.25 * j for j in range(10)]
TOL3 = 1e-10
gap = min(abs(kp - res(k, A3)) for k in G3 for kp in G3)
print("Lab3 gap", f"{gap:.9f}")
vals = [0.0] * 10
sweeps = 0
cert = math.inf
change = math.inf
while cert > TOL3:
    new = bell(vals, B3, A3, G3)
    change = sup(new, vals)
    cert = B3 / (1 - B3) * change
    vals = new
    sweeps += 1
print("Lab3 sweeps", sweeps, "change", f"{change:.12e}", "cert", f"{cert:.12e}")
U = math.sqrt(max(G3) ** A3)
na = 0
while B3**na * U / (1 - B3) > TOL3:
    na += 1
print("Lab3 a priori", na, "sweeps<=na+1", sweeps <= na + 1)
resid = sup(bell(vals, B3, A3, G3), vals)
print("Lab3 residual", f"{resid:.12e}", "<= (1+b)cert", resid <= (1 + B3) * cert, "ratio resid/cert", resid / cert)
rng = random.Random(7)
worst = 0.0
for _ in range(200):
    a = [rng.uniform(0.0, 4.0) for _ in G3]
    b = [rng.uniform(0.0, 4.0) for _ in G3]
    worst = max(worst, sup(bell(a, B3, A3, G3), bell(b, B3, A3, G3)) / sup(a, b))
print("Lab3 worst ratio", f"{worst:.15f}", "<= beta+1e-12", worst <= B3 + 1e-12)
print("Lab3 V", [f"{x:.6f}" for x in vals])
print("Lab3 hours sum", 1 + 2 + 8 + 7 + 3 + 5, "share", f"{26/130*100:.1f}")
