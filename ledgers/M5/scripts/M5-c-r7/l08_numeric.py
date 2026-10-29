import math, random, sys
from fractions import Fraction
# Independent recomputation of L08 claims. Run with: python3 -I this.py
GRID = (0.25, 0.5, 0.75, 1.0)
ALPHA = 0.5
def bellman(values, grid, beta):
    new, pol = [], []
    for k in grid:
        out = k ** ALPHA
        feas = [j for j, kp in enumerate(grid) if kp <= out]
        best, bi = -math.inf, -1
        for j in feas:
            c = math.sqrt(out - grid[j]) + beta * values[j]
            if c > best:
                best, bi = c, j
        new.append(best); pol.append(bi)
    return new, pol
def solve(grid, beta, tol=1e-12):
    v = [0.0] * len(grid); n = 0
    while True:
        nv, _ = bellman(v, grid, beta); n += 1
        gap = max(abs(a - b) for a, b in zip(nv, v))
        v = nv
        if gap <= tol:
            return v, n
for beta in (0.5, 0.9, 0.95):
    v, n = solve(GRID, beta)
    print("solver count beta=", beta, n)
# a priori threshold, d = sqrt(3)/2 from V_1 - V_0
d = math.sqrt(3) / 2
v1, _ = bellman([0.0]*4, GRID, 0.9)
print("d computed =", max(abs(x) for x in v1), "vs sqrt(3)/2 =", d)
for beta in (0.5, 0.9, 0.95):
    t = math.log(1e-12 * (1 - beta) / d) / math.log(beta)
    nmin = next(n for n in range(0, 100000) if beta**n * d / (1 - beta) <= 1e-12)
    print("beta", beta, "threshold", round(t, 2), "least n", nmin)
# ratio check with seed, same draw order as lab
rng = random.Random(20261028)
worst = 0.0
worst_exact = None
for _ in range(2000):
    v = [rng.uniform(-10.0, 10.0) for _ in GRID]
    w = [rng.uniform(-10.0, 10.0) for _ in GRID]
    bv, _ = bellman(v, GRID, 0.9); bw, _ = bellman(w, GRID, 0.9)
    num = max(abs(a - b) for a, b in zip(bv, bw)); den = max(abs(a - b) for a, b in zip(v, w))
    r = num / den
    if r > worst: worst = r
print("largest ratio float", repr(worst), "minus beta", worst - 0.9)
# 1-point grid: fixed point and iterate at beta=1
print("E2 check", math.sqrt(0.707107 - 0.25), math.sqrt(0.457107) + 0.9*5.0)
print("E1 at 0.5 converged first value check", solve((0.25,), 0.9)[1])
