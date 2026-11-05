"""Dense random check of the exception-table scope claim: every (noise volume, cost) with noise volume log-uniform in
[1e-300, 1e150] and cost uniform in [0, 350] returns the three keys, finite, in range, with no exception.

Run: python3 -I scope_dense_r9.py <path-to-reference.py>   (seeded: random.Random(9))
"""
import importlib.util
import math
import random
import sys

spec = importlib.util.spec_from_file_location("ref", sys.argv[1])
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
rng = random.Random(9)
keys = {"informed_fraction", "price_informativeness", "indifference_gap"}
bad = []
N = 20000
for _ in range(N):
    sd = 10 ** rng.uniform(-300.0, 150.0)
    cost = rng.uniform(0.0, 350.0)
    try:
        out = ref.solve_model(sd, cost)
    except Exception as err:  # noqa: BLE001
        bad.append((sd, cost, type(err).__name__))
        continue
    good = set(out) == keys and all(math.isfinite(v) for v in out.values())
    good = good and 0.0 <= out["informed_fraction"] <= 1.0 and 0.0 <= out["price_informativeness"] <= 1.0
    if not good:
        bad.append((sd, cost, out))
print(f"dense scope check: {N} random points, {len(bad)} invalid")
for b in bad[:10]:
    print("  ", b)
