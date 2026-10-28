"""Verifier CS2-d round 4: recount the naive-formula failures per offset group that grader/instance.py states (seeds 0-49).

Usage: python -I naive_by_offset_r4.py <checkout>
The naive order is s += x, ss += x*x, mean = s/n, variance = (ss - n*mean*mean)/(n-1), compared with an exact Fraction
reference under the grader's tolerance (relative 1e-9, absolute floor 1e-9). The Welford reference is reference.py.
The offset of each seed is recovered by repeating the first two draws of make_instance (randint, then choice).
"""

import importlib.util
import json
import random
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

checkout = Path(sys.argv[1])
grader = checkout / "course/modules/CS/CS2/grader"
sys.path.insert(0, str(grader))
from instance import make_instance  # noqa: E402

spec = importlib.util.spec_from_file_location("ref", grader / "reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


def close(a: float, b: float) -> bool:
    return abs(a - b) <= max(1e-9, 1e-9 * max(abs(a), abs(b)))


total: Counter[float] = Counter()
fail: Counter[float] = Counter()
welford_fail = 0
for seed in range(50):
    payload = json.loads(make_instance(seed)["payload"])
    xs = [float(x) for x in payload["values"]]
    fr = [Fraction(x) for x in xs]
    n = len(fr)
    mean_e = sum(fr) / n
    var_e = sum((x - mean_e) ** 2 for x in fr) / (n - 1)
    rng = random.Random(seed)
    rng.randint(20, 400)
    offset = rng.choice([0.0, 10_000.0, 1_000_000.0])
    total[offset] += 1
    s = 0.0
    ss = 0.0
    for x in xs:
        s += x
        ss += x * x
    mean_n = s / n
    var_n = (ss - n * mean_n * mean_n) / (n - 1)
    naive_ok = close(mean_n, float(mean_e)) and close(var_n, float(var_e))
    if not naive_ok:
        fail[offset] += 1
    acc = ref.WelfordAccumulator()
    for x in xs:
        acc.update(x)
    if not (close(acc.mean(), float(mean_e)) and close(acc.variance(1), float(var_e))):
        welford_fail += 1
    if seed in (41, 47):
        print(f"seed {seed} offset {offset} naive {'ok' if naive_ok else 'fails'}")
for offset in sorted(total):
    print(f"offset {offset}: seeds {total[offset]}, naive fails {fail[offset]}")
print("welford fails", welford_fail)
