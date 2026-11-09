"""Round-3 independent recomputation of the numbers printed or derived on M5 L08, L09 and L10.

Written by the verifier from the page text, not from the twins. Standard library only.
Run: .venv/bin/python -I ledgers/M5/scripts/M5-c-r3/numbers_check.py
"""

import math
import random
from fractions import Fraction

GRID = (0.25, 0.5, 0.75, 1.0)
ALPHA = 0.5


def feas(k, grid):
    out = k**ALPHA
    return [j for j, kp in enumerate(grid) if kp <= out]


def B(V, beta, grid=GRID):
    res, pol = [], []
    for k in grid:
        out = k**ALPHA
        vals = [(math.sqrt(out - grid[j]) + beta * V[j], j) for j in feas(k, grid)]
        best, j = max(vals)
        res.append(best)
        pol.append(j)
    return res, pol


def iterate_gap(beta, tol=1e-12, grid=GRID):
    V = [0.0] * len(grid)
    n = 0
    while True:
        W, _ = B(V, beta, grid)
        n += 1
        gap = max(abs(a - b) for a, b in zip(W, V))
        V = W
        if gap <= tol:
            return n, V


print("== L08")
for beta in (0.5, 0.9, 0.95):
    n, V = iterate_gap(beta)
    print(f"L08 counts beta={beta} gap<=1e-12 iterations={n}")
n, V = iterate_gap(0.9)
W, pol = B(V, 0.9)
print("L08 fixed point", [f"{v:.9f}" for v in V], "policy idx", pol, "residual", f"{max(abs(a-b) for a,b in zip(W,V)):.4e}")
# Example 1.2 and M3
W1, _ = B([0.0, 0.0], 0.9, (0.25, 1.0))
print("L08 Ex1.2 BV", W1, "sqrt(0.75)", math.sqrt(0.75))
for k in GRID:
    print("L08 M3 F", k, [g for g in GRID if g <= k**ALPHA])
# seeded ratio (Part B draw order: v then w, each 4 uniforms, 2000 pairs)
rng = random.Random(20261028)
worst = 0.0
worst_exact_over = None
for _ in range(2000):
    v = [rng.uniform(-10.0, 10.0) for _ in GRID]
    w = [rng.uniform(-10.0, 10.0) for _ in GRID]
    bv, _ = B(v, 0.9)
    bw, _ = B(w, 0.9)
    num = max(abs(a - b) for a, b in zip(bv, bw))
    den = max(abs(a - b) for a, b in zip(v, w))
    r = num / den
    if r > worst:
        worst = r
print(f"L08 part B largest ratio {worst!r} minus beta {worst - 0.9!r} (ulps of beta: {(worst - 0.9) / (math.ulp(0.9)):.2f})")
# one-point grid
one = (0.25,)
n1, V1 = iterate_gap(0.9, grid=one)
print(f"L08 one-point beta=0.9 V*={V1[0]!r} iterations={n1}")
# E2
print("L08 E2 utility sqrt(0.707107-0.25)", math.sqrt(0.707107 - 0.25), "plus 0.9*5", math.sqrt(0.707107 - 0.25) + 4.5)
print("L08 E2 with exact fixed point: 0.9*V*(0.25)=", 0.9 * V[0], "V*(0.5)=", V[1])
# E1 thresholds
d = math.sqrt(3) / 2
for beta in (0.5, 0.9, 0.95):
    thr = math.log(1e-12 * (1 - beta) / d) / math.log(beta)
    print(f"L08 E1 a priori threshold beta={beta} n>={thr:.4f} least n={math.ceil(thr)}")

print("== L09")
V0 = [0.0] * 4


def cert(prev, cur, beta=0.9):
    return beta / (1 - beta) * max(abs(a - b) for a, b in zip(cur, prev))


def run_until(stop):
    prev = [0.0] * 4
    cur, _ = B(prev, 0.9)
    n = 1
    while not stop(prev, cur):
        prev, cur = cur, B(cur, 0.9)[0]
        n += 1
    return n, cur, prev


nref, vref, prevref = run_until(lambda p, c: cert(p, c) <= 1e-12)
print("L09 reference iterations", nref, "cert", f"{cert(prevref, vref):.4e}")
print("L09 reference values", [f"{v:.10f}" for v in vref])
for tol in (1e-2, 1e-4, 1e-6):
    n, v, p = run_until(lambda p_, c_, t=tol: cert(p_, c_) <= t)
    c = cert(p, v)
    err = max(abs(a - b) for a, b in zip(v, vref))
    steps = [a - b for a, b in zip(v, p)]
    print(f"L09 stop tol={tol:g} n={n} cert={c:.12f} actual={err:.12f} spread={max(steps)-min(steps):.3e} bound_holds={err <= c + 1e-12}")
v10 = [0.0] * 4
prev10 = [0.0] * 4
cur10 = B(prev10, 0.9)[0]
for _ in range(9):
    prev10, cur10 = cur10, B(cur10, 0.9)[0]
err10 = max(abs(a - b) for a, b in zip(cur10, vref))
print(f"L09 fixed count n=10 cert={cert(prev10, cur10):.12f} actual={err10:.12f}")
# naive rule
n, v, p = run_until(lambda p_, c_: max(abs(a - b) for a, b in zip(p_, c_)) <= 1e-6)
step = max(abs(a - b) for a, b in zip(v, p))
err = max(abs(a - b) for a, b in zip(v, vref))
print(f"L09 naive n={n} step={step!r} actual={err!r} 9*step={9*step!r} actual/step={err/step!r}")
print(f"L09 naive: 9*step printed to 10dp={9*step:.10f}, actual to 10dp={err:.10f}, ratio to 4dp={err/step:.4f}")
print("L09 sqrt3/2", d)
# a priori count
for n in (151, 152):
    print(f"L09 R2 apriori bound n={n}: {0.9**n / 0.1 * d:.6e}")
print("L09 M-count: n with 0.9^n/0.1*d <= 1e-6 first =",
      next(n for n in range(1, 1000) if 0.9**n / 0.1 * d <= 1e-6))
print(f"L09 Q beta^10/(1-beta) = {0.9**10 / 0.1:.9f}")
print(f"L09 M1: {0.5/0.5} {0.9/0.1} {0.99/0.01}")
print(f"L09 M2: 0.8/0.2*0.016 = {0.8/0.2*0.016}")
print(f"L09 M3: 1e-3*0.1/0.9 = {1e-3*0.1/0.9}")
print(f"L09 E2 ratio {0.0000085808/0.0000009534:.6f}")

print("== L10")
def rs_sum(pts, tags, G):
    return sum(t * (G(pts[i + 1]) - G(pts[i])) for i, t in enumerate(tags))
for n in (4, 10, 100, 1000):
    pts = [Fraction(i, n) for i in range(n + 1)]
    R = rs_sum(pts, pts[1:], lambda x: x * x)
    Lf = rs_sum(pts, pts[:-1], lambda x: x * x)
    print(f"L10 A n={n} right={float(R):.12f} left={float(Lf):.12f} right_err={float(R-Fraction(2,3)):.12f} left_err={float(Lf-Fraction(2,3)):.12f}")
rng = random.Random(20261028)
worst = 0.0
maxmesh = 0.0
allok = True
for _ in range(200):
    m = rng.randint(1, 30)
    interior = sorted(rng.random() for _ in range(m))
    bounds = [0.0, *interior, 1.0]
    tags = [lo + rng.random() * (hi - lo) for lo, hi in zip(bounds[:-1], bounds[1:])]
    S = sum(t * (bounds[i + 1] ** 2 - bounds[i] ** 2) for i, t in enumerate(tags))
    mesh = max(hi - lo for lo, hi in zip(bounds[:-1], bounds[1:]))
    err = abs(S - 2 / 3)
    allok = allok and err <= mesh + 1e-15
    worst = max(worst, err / mesh)
    maxmesh = max(maxmesh, mesh)
print(f"L10 B largest_mesh={maxmesh:.6f} largest_err_over_mesh={worst:.6f} P2_bound_all={allok}")
# Prop 4.2 random check and P2-type check with random tags
rng2 = random.Random(7)
ok42 = True
for _ in range(2000):
    m = rng2.randint(1, 20)
    xs = sorted({0.0, 1.0, *[rng2.random() for _ in range(m)]})
    tags = [lo + rng2.random() * (hi - lo) for lo, hi in zip(xs[:-1], xs[1:])]
    G = lambda x: 1.0 if x >= 0.5 else 0.0
    S = sum(t * (G(xs[i + 1]) - G(xs[i])) for i, t in enumerate(tags))
    mesh = max(hi - lo for lo, hi in zip(xs[:-1], xs[1:]))
    ok42 = ok42 and abs(S - 0.5) <= mesh + 1e-15
print("L10 Prop4.2 random check (|S-1/2|<=mesh)", ok42)
# Part C
for n in (10, 100):
    pts = [Fraction(i, n) for i in range(n + 1)]
    k = n // 2
    Gs = lambda x: 1 if x >= Fraction(1, 2) else 0
    left = Fraction(0)
    right = Fraction(0)
    for i in range(1, n + 1):
        dG = Gs(pts[i]) - Gs(pts[i - 1])
        if i == k:
            left += Gs(pts[i - 1]) * dG
            right += Gs(pts[i]) * dG
    print(f"L10 C n={n} left={left} right={right}")
# Part D
n = 1000
pts = [Fraction(i, n) for i in range(n + 1)]
print("L10 D", float(rs_sum(pts, pts[1:], lambda x: x)), float(rs_sum(pts, pts[:-1], lambda x: x)))
print("L10 E1 errors", Fraction(3*10-1, 6*100), -Fraction(3*10+1, 6*100), "gap", Fraction(31,600)-Fraction(29,600), float(Fraction(31,600)-Fraction(29,600)))
print("L10 q6 exact", float(Fraction(1001*3999, 6*10**6)))
print("L10 M1 S", Fraction(1,2)*Fraction(1,8)+Fraction(7,8))
print("L10 M2 2*int x^2 0..2", 2*Fraction(8,3))
