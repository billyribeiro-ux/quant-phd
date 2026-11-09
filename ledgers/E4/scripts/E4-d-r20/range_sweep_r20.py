"""Round-20 check of the exception table's stated range (not a grader change): the reference over random inputs in
noise volume 1e-50..1e150 (log-uniform) and cost 0..350. Counts exceptions, non-finite outputs and out-of-range fractions.
Usage: python3 -I range_sweep_r20.py <checkout-root> <draws> <seed>
"""
import importlib.util
import math
import random
import sys

spec = importlib.util.spec_from_file_location("ref", sys.argv[1] + "/course/modules/E/E4/grader/reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
n, seed = int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)
exc, nonfinite, bad_range, interior, examples = 0, 0, 0, 0, []
for _ in range(n):
    sd = 10 ** rng.uniform(-50, 150)
    c = rng.uniform(0, 350) if rng.random() < 0.5 else rng.uniform(0, 0.4)
    try:
        out = ref.solve_model(sd, c)
    except Exception as e:  # counted, with examples
        exc += 1
        if len(examples) < 5:
            examples.append((sd, c, type(e).__name__))
        continue
    if not all(math.isfinite(v) for v in out.values()):
        nonfinite += 1
        if len(examples) < 5:
            examples.append((sd, c, "nonfinite"))
    if not (0.0 <= out["informed_fraction"] <= 1.0 and 0.0 <= out["price_informativeness"] <= 1.0):
        bad_range += 1
    interior += 0.0 < out["informed_fraction"] < 1.0
print(f"draws {n} seed {seed}: exceptions {exc}, nonfinite {nonfinite}, out of [0,1] {bad_range}, interior {interior}, examples {examples}")
