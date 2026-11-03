"""Re-derive the instance.py docstring counts. The offset of each seed is read from the generator's own draw order
(random.Random(seed): randint(20, 400) for the length, then choice(OFFSETS) for the offset), not guessed from the values.
Naive formula as the docstring states: s += x; ss += x*x; mean = s/n; var = (ss - n*mean*mean)/(n-1).
A failure is a result not within the suite's close() rule of the exact Fraction sample variance.
Usage: python -I naive_offsets.py <grader_dir>"""

import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from instance import OFFSETS, make_instance  # noqa: E402

grader = Path(sys.argv[1])


def close(a: float, b: float) -> bool:
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= max(1e-9, 1e-9 * max(abs(a), abs(b)))


groups: dict[float, dict[str, list[int]]] = {}
for seed in range(50):
    rng = random.Random(seed)
    rng.randint(20, 400)
    offset = rng.choice(OFFSETS)
    vals = [float(x) for x in json.loads(make_instance(seed)["payload"])["values"]]
    n = len(vals)
    fr = [Fraction(x) for x in vals]
    mean_e = sum(fr) / n
    var_e = sum((x - mean_e) ** 2 for x in fr) / (n - 1)
    s = 0.0
    ss = 0.0
    for x in vals:
        s += x
        ss += x * x
    mean = s / n
    var = (ss - n * mean * mean) / (n - 1)
    g = groups.setdefault(offset, {"seeds": [], "fail": []})
    g["seeds"].append(seed)
    if not close(var, float(var_e)):
        g["fail"].append(seed)
for k in sorted(groups):
    g = groups[k]
    print(f"offset {k:>12}: seeds={len(g['seeds'])} naive_fail={len(g['fail'])} passing={[s for s in g['seeds'] if s not in g['fail']]}")
