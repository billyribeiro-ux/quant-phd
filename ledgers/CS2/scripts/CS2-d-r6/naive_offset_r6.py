"""Re-derive the instance docstring's naive-formula counts (seeds 0-49) against the exact Fraction reference."""
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1])  # grader dir, passed as an argument
from instance import make_instance  # noqa: E402

def close(a, b, rel=1e-9, absolute=1e-9):
    import math
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= max(absolute, rel * max(abs(a), abs(b)))

by_offset = {}
for seed in range(50):
    inst = make_instance(seed)
    import json
    p = json.loads(inst["payload"])
    vals = [float(x) for x in p["values"]]
    n = len(vals)
    fr = [Fraction(x) for x in vals]
    mean = sum(fr) / n
    sample = sum((x - mean) ** 2 for x in fr) / (n - 1) if n > 1 else Fraction(0)
    s = 0.0
    ss = 0.0
    for x in vals:
        s += x
        ss += x * x
    m = s / n
    naive = (ss - n * m * m) / (n - 1)
    # offset recovered from the seed exactly as make_instance draws it
    import random
    rng = random.Random(seed)
    rng.randint(20, 400)
    off = rng.choice([0.0, 10_000.0, 1_000_000.0])
    fails = not close(naive, float(sample))
    by_offset.setdefault(off, []).append((seed, fails, n))
for off in sorted(by_offset):
    rows = by_offset[off]
    print(f"offset {off:>10.0f}: seeds {len(rows)}, naive fails {sum(f for _, f, _ in rows)}, passes seeds {[s for s, f, _ in rows if not f]}")
