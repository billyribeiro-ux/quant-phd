"""Independent re-derivation of every number on the M5 project page (slice d, round 4)."""
import math
import random

def run_model(beta, alpha, grid):
    def res(k):
        return k**alpha
    def sweep(values):
        out = []
        for k in grid:
            r = res(k)
            out.append(max(math.sqrt(r - kp) + beta * values[j] for j, kp in enumerate(grid) if kp <= r))
        return out
    return res, sweep

def sup(a, b):
    return max(abs(x - y) for x, y in zip(a, b))

# ---- Lab 1 model
B1, A1, G1 = 0.9, 0.5, [0.5, 0.9, 1.4]
res1, sw1 = run_model(B1, A1, G1)
print("L1 resources", [f"{res1(k):.6f}" for k in G1])
print("L1 feasible", {k: [kp for kp in G1 if kp <= res1(k)] for k in G1})
v0 = [0.0] * 3
v1 = sw1(v0)
print("L1 V1", [f"{x:.6f}" for x in v1], [repr(x) for x in v1])
lhs = sup(sw1(v0), sw1(v1))
rhs = B1 * sup(v0, v1)
print(f"L1 contraction lhs {lhs:.9f} rhs {rhs:.9f}")
vals = v0
n = 0
cert = math.inf
changes = []
while cert > 1e-6:
    n += 1
    new = sw1(vals)
    ch = sup(new, vals)
    cert = B1 / (1 - B1) * ch
    vals = new
    changes.append((n, ch, cert))
    if n <= 3:
        print(f"L1 sweep {n}: change {ch:.9f} cert {cert:.9f}")
print(f"L1 stop sweep {n}: change {ch:.12e} cert {cert:.12e} cert9 {cert:.9f}")
ref = v0
for _ in range(100000):
    nxt = sw1(ref)
    small = B1 / (1 - B1) * sup(nxt, ref) <= 1e-12
    ref = nxt
    if small:
        break
actual = sup(vals, ref)
print(f"L1 actual error {actual:.12e} cert {cert:.12e} diff {abs(actual-cert):.3e}")
print("L1 values", [f"{x:.6f}" for x in vals], [f"{x:.12f}" for x in vals])
print("L1 ref", [f"{x:.12f}" for x in ref])
print("L1 sweep 146 change exact", changes[145][1], "cert", changes[145][2])
print("L1 sweep 145 cert", changes[144][2], "(must be >1e-6)")

# ---- Lab 2 completion
v = [0.0, 0.0, 0.0]
w = [0.1, 0.2, 0.3]
ratio = sup(sw1(v), sw1(w)) / sup(v, w)
print(f"L2 ratio {ratio:.9f}  print {ratio:.6f} <= beta {ratio <= B1}")
vals2 = [0.0] * 3
n2 = 0
cert2 = math.inf
ch2 = math.inf
while cert2 > 1e-6 and n2 < 300:
    n2 += 1
    new = sw1(vals2)
    ch2 = sup(new, vals2)
    cert2 = B1 / (1 - B1) * ch2
    vals2 = new
print(f"L2 sweeps {n2} cert {cert2:.3e} last change {ch2:.3e} values {[f'{x:.6f}' for x in vals2]}")
print(f"L2 cert exact {cert2:.12e} (L1 narrative says 9.495187e-7?)")

# ---- Lab 3 instance
B3, A3 = 0.9, 0.3
G3 = [0.45 + 0.25 * j for j in range(10)]
TOL = 1e-10
res3, sw3 = run_model(B3, A3, G3)
gap = min(abs(kp - res3(k)) for k in G3 for kp in G3)
print(f"L3 gap {gap:.9f} clear {gap > 1e-6}")
vals3 = [0.0] * 10
sweeps = 0
cert3 = math.inf
ch3 = math.inf
while cert3 > TOL:
    new = sw3(vals3)
    ch3 = sup(new, vals3)
    cert3 = B3 / (1 - B3) * ch3
    vals3 = new
    sweeps += 1
print(f"L3 sweeps {sweeps} last change {ch3:.6e} cert {cert3:.6e}")
bu = math.sqrt(max(G3) ** A3)
na = 0
while B3**na * bu / (1 - B3) > TOL:
    na += 1
print(f"L3 a priori {na} within+1 {sweeps <= na + 1}  bu={bu!r}")
resid = sup(sw3(vals3), vals3)
print(f"L3 residual {resid:.6e} bound (1+b)cert {(1+B3)*cert3:.6e} ok {resid <= (1+B3)*cert3}")
rng = random.Random(7)
worst = 0.0
worst_pair = None
for _ in range(200):
    v_ = [rng.uniform(0.0, 4.0) for _ in G3]
    w_ = [rng.uniform(0.0, 4.0) for _ in G3]
    r = sup(sw3(v_), sw3(w_)) / sup(v_, w_)
    if r > worst:
        worst = r
print(f"L3 worst ratio over 200 pairs {worst!r} print {worst:.6f} <= beta+1e-12 {worst <= B3 + 1e-12}")
print("L3 V", [f"{x:.6f}" for x in vals3])
print("L3 V exact", [f"{x:.9f}" for x in vals3])
# a priori count bound check: is the sweep count within "a priori + 1" for all instances? (not needed)
