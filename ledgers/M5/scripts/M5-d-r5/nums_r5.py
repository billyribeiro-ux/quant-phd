"""Independent recomputation (verifier, round 5) of every project-page number from unrounded values.

Own implementation of the operator; no import of the course code. Prints unrounded values and the displayed digits.
usage: python -I nums_r5.py
"""
import math
import random

def run(beta, alpha, grid, tol_stop=None, max_sweeps=10**6):
    def B(V):
        out = []
        for k in grid:
            r = k**alpha
            out.append(max(math.sqrt(r - kp) + beta * v for kp, v in zip(grid, V) if kp <= r))
        return out
    return B

def sup(a, b):
    return max(abs(x - y) for x, y in zip(a, b))

# ---- Lab 1 instance
beta, alpha = 0.9, 0.5
G1 = [0.5, 0.9, 1.4]
B1 = run(beta, alpha, G1)
print("Lab1 resources", [f"{k**alpha:.9f}" for k in G1])
V0 = [0.0] * 3
V1 = B1(V0)
print("Lab1 V1 unrounded", [f"{x:.10f}" for x in V1])
print("Lab1 sup|BV-BW| (V0,V1)", f"{sup(B1(V0), B1(V1)):.10f}", " beta*sup|V0-V1|", f"{beta*sup(V0,V1):.10f}")
print("Lab1 first sweep change", f"{sup(V1, V0):.10f}", "cert", f"{beta/(1-beta)*sup(V1,V0):.10f}")
vals = V0; n = 0; cert = math.inf
while cert > 1e-6:
    new = B1(vals); n += 1; ch = sup(new, vals); cert = beta/(1-beta)*ch; vals = new
    if n <= 3: print("  sweep", n, f"change {ch:.10f} cert {cert:.10f}")
print("Lab1 stop sweep", n, "change", f"{ch:.12e}", "cert", f"{cert:.12e}")
ref = [0.0]*3
for _ in range(100000):
    nxt = B1(ref); small = beta/(1-beta)*sup(nxt, ref) <= 1e-12; ref = nxt
    if small: break
print("Lab1 value", [f"{x:.9f}" for x in vals], "actual error", f"{sup(vals, ref):.12e}")

# ---- Lab 2 ratio and bound
v = [0.0]*3; w = [0.1, 0.2, 0.3]
print("Lab2 ratio", f"{sup(B1(v), B1(w))/sup(v, w):.10f}")
vals = [0.0]*3; n = 0; cert = math.inf
while cert > 1e-6 and n < 300:
    new = B1(vals); n += 1; ch = sup(new, vals); cert = beta/(1-beta)*ch; vals = new
print("Lab2 sweeps", n, "cert", f"{cert:.10e}", "last change", f"{ch:.10e}", "unrounded cert vs 9.495187e-7 ->", f"{cert*1e7:.6f}e-7")

# ---- Lab 3 instance
beta3, alpha3 = 0.9, 0.3
G3 = [0.45 + 0.25*j for j in range(10)]
B3 = run(beta3, alpha3, G3)
gap = min(abs(kp - k**alpha3) for k in G3 for kp in G3)
print("Lab3 gap", f"{gap:.10f}")
vals = [0.0]*10; sweeps = 0; cert = math.inf; ch = math.inf
while cert > 1e-10:
    new = B3(vals); ch = sup(new, vals); cert = beta3/(1-beta3)*ch; vals = new; sweeps += 1
print("Lab3 sweeps", sweeps, "last change", f"{ch:.12e}", "cert", f"{cert:.12e}")
U = math.sqrt(max(G3)**alpha3); na = 0
while beta3**na*U/(1-beta3) > 1e-10: na += 1
print("Lab3 a priori count", na, "U", f"{U:.10f}", "sweeps <= na+1", sweeps <= na+1)
res = sup(B3(vals), vals)
print("Lab3 residual", f"{res:.12e}", "bound (1+b)cert", f"{(1+beta3)*cert:.12e}", "ratio residual/cert", f"{res/cert:.6f}")
print("Lab3 residual/last change", f"{res/ch:.10f}", "(1-beta)*cert/ch", f"{(1-beta3)*cert/ch:.10f}")
rng = random.Random(7); worst = 0.0
for _ in range(200):
    v = [rng.uniform(0.0, 4.0) for _ in G3]; w = [rng.uniform(0.0, 4.0) for _ in G3]
    worst = max(worst, sup(B3(v), B3(w))/sup(v, w))
print("Lab3 worst ratio 200 pairs", f"{worst:.15f}", "minus beta", f"{worst-beta3:.3e}")
for k, x in zip(G3, vals):
    print(f"V({k}) = {x:.9f}")
print("cert/last change", f"{cert/ch:.10f}")
