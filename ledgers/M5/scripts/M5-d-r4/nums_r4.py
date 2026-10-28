"""Independent unrounded recomputation of every number the M5 project page prints or quotes (round 4).

Run: python -I nums_r4.py  (standard library only; no lab code is imported).
"""
import math
import random

def run(beta, alpha, grid, tol, values=None):
    def res(k): return k**alpha
    def sweep(v):
        out = []
        for k in grid:
            out.append(max(math.sqrt(res(k) - kp) + beta * v[j] for j, kp in enumerate(grid) if kp <= res(k)))
        return out
    def dist(a, b): return max(abs(x - y) for x, y in zip(a, b))
    v = [0.0] * len(grid); n = 0; cert = math.inf; change = math.inf; hist = []
    while cert > tol and n < 100000:
        new = sweep(v); change = dist(new, v); cert = beta / (1 - beta) * change; v = new; n += 1
        hist.append((change, cert))
    return v, n, change, cert, hist, sweep, dist

# Lab 1 / Lab 2 instance
G1 = [0.5, 0.9, 1.4]
v1, n1, ch1, ce1, h1, sweep1, dist1 = run(0.9, 0.5, G1, 1e-6)
print("Lab1 sweep1 change", repr(h1[0][0]), "cert", repr(h1[0][1]), "9x", 9 * h1[0][0])
print("Lab1 stop n", n1, "cert", repr(ce1), "change", repr(ch1))
ref = [0.0] * 3
for _ in range(100000):
    nxt = sweep1(ref)
    small = 0.9 / (1 - 0.9) * dist1(nxt, ref) <= 1e-12
    ref = nxt
    if small: break
print("Lab1 actual error", repr(dist1(v1, ref)), "9-dec", f"{dist1(v1, ref):.9f}", f"{ce1:.9f}")
V1 = sweep1([0.0] * 3)
print("V1 unrounded", V1)
lhs = dist1(sweep1(V1), sweep1([0.0] * 3)); print("contraction lhs", lhs, "rhs", 0.9 * dist1(V1, [0.0] * 3))
# Lab 2 ratio and stop
v = [0.0, 0.0, 0.0]; w = [0.1, 0.2, 0.3]
print("Lab2 ratio", dist1(sweep1(v), sweep1(w)) / dist1(v, w))
print("Lab2 at n=146: cert", repr(h1[145][1]), "change", repr(h1[145][0]), "n", n1)

# Lab 3 instance
G3 = [0.45 + 0.25 * j for j in range(10)]
v3, n3, ch3, ce3, h3, sweep3, dist3 = run(0.9, 0.3, G3, 1e-10)
print("Lab3 sweeps", n3, "change", repr(ch3), "cert", repr(ce3), "cert/change", ce3 / ch3)
print("Lab3 9x printed change", 9 * 1.025e-11, "9x unrounded change", 9 * ch3)
resid = dist3(sweep3(v3), v3)
print("Lab3 residual", repr(resid), "(1+b)cert", 1.9 * ce3, "resid/cert", resid / ce3, "1.9*printed cert", 1.9 * 9.226e-11)
gap = min(abs(kp - k**0.3) for k in G3 for kp in G3)
print("Lab3 gap", repr(gap))
bu = math.sqrt(max(G3) ** 0.3); na = 0
while 0.9**na * bu / 0.1 > 1e-10: na += 1
print("Lab3 a priori", na)
rng = random.Random(7); worst = 0.0
for _ in range(200):
    a = [rng.uniform(0.0, 4.0) for _ in G3]; b = [rng.uniform(0.0, 4.0) for _ in G3]
    worst = max(worst, dist3(sweep3(a), sweep3(b)) / dist3(a, b))
print("Lab3 worst ratio", repr(worst), "minus beta", worst - 0.9)
print("cert/change check 9.0 =", 0.9 / (1 - 0.9))

# L07 c117 (cosine Part A, n=5 printed bound 2.661258 and error 5.439523e-2)
print("c117 ratio", 2.661258 / 0.05439523)
# L09 c154: four-point grid, ||V1-V0|| = sqrt(3)/2
for n in (151, 152):
    print("c154 bound n", n, 0.9**n * (math.sqrt(3) / 2) / (1 - 0.9))
print("c154 smallest n", min(n for n in range(1, 400) if 0.9**n * (math.sqrt(3)/2) / 0.1 <= 1e-6))
