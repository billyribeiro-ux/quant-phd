"""Verify instance.py docstring counts: naive one-pass variance failures per offset group over seeds 0-49.
Usage: python -I naive_counts.py <grader_dir>. Fail = not within rel 1e-9 / abs 1e-9 of the exact Fraction sample variance
(the suite's close() rule), computed with s += x, ss += x*x, mean = s / n, var = (ss - n*mean*mean)/(n-1)."""
import json, math, sys
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from instance import make_instance  # noqa: E402

def close(a, b):
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= max(1e-9, 1e-9 * max(abs(a), abs(b)))

groups = {}
for seed in range(50):
    inst = make_instance(seed)
    payload = json.loads(inst["payload"])
    vals = [float(x) for x in payload["values"]]
    offset = min(vals, key=lambda v: 0)  # placeholder, replaced below
    n = len(vals)
    fr = [Fraction(x) for x in vals]
    mean_e = sum(fr) / n
    var_e = sum((x - mean_e) ** 2 for x in fr) / (n - 1)
    s = 0.0; ss = 0.0
    for x in vals:
        s += x; ss += x * x
    mean = s / n
    var = (ss - n * mean * mean) / (n - 1)
    offset_guess = round(sum(vals) / n, -1)  # the common offset, rounded to tens (uniform noise is within +-5)
    key = 0.0 if abs(offset_guess) < 100 else (10000.0 if abs(offset_guess - 10000) < 100 else 1000000.0)
    g = groups.setdefault(key, {"seeds": [], "fail": []})
    g["seeds"].append(seed)
    if not close(var, float(var_e)):
        g["fail"].append(seed)
for k in sorted(groups):
    g = groups[k]
    print(f"offset {k:>12}: seeds={len(g['seeds'])} naive_fail={len(g['fail'])} passing={[s for s in g['seeds'] if s not in g['fail']]}")
