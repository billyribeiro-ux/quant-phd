import sys, random, math
sys.path.insert(0, sys.argv[1])
import importlib
m = importlib.import_module("l08_mod")
rng = random.Random(m.SEED)
worst = 0.0
ratios = []
for _ in range(m.PAIRS):
    v = [rng.uniform(-10.0, 10.0) for _ in m.GRID]
    w = [rng.uniform(-10.0, 10.0) for _ in m.GRID]
    bv, _ = m.bellman(v, m.GRID, m.BETA)
    bw, _ = m.bellman(w, m.GRID, m.BETA)
    num = max(abs(a - b) for a, b in zip(bv, bw, strict=True))
    den = max(abs(a - b) for a, b in zip(v, w, strict=True))
    r = num / den
    ratios.append(r)
    worst = max(worst, r)
print("worst repr", repr(worst), "minus beta", worst - 0.9, "in ulps", (worst - 0.9) / (math.ulp(0.9)))
print("sum-check worst > beta count", sum(1 for r in ratios if r > 0.9))
print("beta+TOL check", worst <= 0.9 + 1e-12)
