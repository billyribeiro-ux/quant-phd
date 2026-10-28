"""Verifier round 5: L08 card numbers recomputed from the lab's own functions in copies with BETA changed,
and the unrounded seeded contraction ratio (Lab 1 Part B, seed 20261028, 2000 pairs)."""
import math, random, sys
sys.path.insert(0, "/tmp/verifyB5-M5-d/ledgers/M5/scripts/M5-d-r5")
ALPHA = 0.5
GRID = (0.25, 0.5, 0.75, 1.0)
TOL = 1e-12
def bellman(values, grid, beta):
    out = []
    for k in grid:
        output = k**ALPHA
        feas = [j for j, kp in enumerate(grid) if kp <= output]
        out.append(max(math.sqrt(output - grid[j]) + beta * values[j] for j in feas))
    return out
def solve(grid, beta):
    values = [0.0] * len(grid); count = 0
    while True:
        new = bellman(values, grid, beta); count += 1
        gap = max(abs(a - b) for a, b in zip(new, values))
        values = new
        if gap <= TOL:
            return values, count
for b in (0.5, 0.9, 0.95):
    v, c = solve(GRID, b)
    print("beta", b, "count", c, "V*(0.25)", f"{v[0]:.6f}")
rng = random.Random(20261028)
worst = 0.0; worst_exact = -1.0
for _ in range(2000):
    v = [rng.uniform(-10.0, 10.0) for _ in GRID]
    w = [rng.uniform(-10.0, 10.0) for _ in GRID]
    bv = bellman(v, GRID, 0.9); bw = bellman(w, GRID, 0.9)
    num = max(abs(a - b) for a, b in zip(bv, bw)); den = max(abs(a - b) for a, b in zip(v, w))
    r = num / den
    worst = max(worst, r)
print("largest ratio", repr(worst), "minus beta", f"{worst - 0.9:.6e}", "in ulps of 0.9:", (worst - 0.9) / (math.ulp(0.9)))
print("printed", f"{worst:.6f}")
