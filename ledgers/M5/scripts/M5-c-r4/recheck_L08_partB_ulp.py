import importlib.util, sys, random, math
spec = importlib.util.spec_from_file_location("L08", "/tmp/verifyB4-M5-c/tests/labs/M5/lab-M5-L08-1.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rng = random.Random(m.SEED); worst = 0.0; worst_raw = None
for _ in range(m.PAIRS):
    v = [rng.uniform(-10.0, 10.0) for _ in m.GRID]
    w = [rng.uniform(-10.0, 10.0) for _ in m.GRID]
    bv, _ = m.bellman(v, m.GRID, m.BETA); bw, _ = m.bellman(w, m.GRID, m.BETA)
    num = max(abs(a - b) for a, b in zip(bv, bw, strict=True))
    den = max(abs(a - b) for a, b in zip(v, w, strict=True))
    r = num / den
    if r > worst: worst = r
print("worst ratio repr", repr(worst), "excess over beta", repr(worst - 0.9), "ulps", (worst - 0.9) / math.ulp(0.9))
