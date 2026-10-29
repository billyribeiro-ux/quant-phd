"""Round-7 verifier script: instance validity, materiality (answers differ across seeds) and the naive-formula counts
that instance.py's docstring states (sample variance by (ss - n*mean*mean)/(n-1) with running float sums).

Usage (from the checkout root): .venv/bin/python ledgers/CS2/scripts/CS2-d-r7/instances_r7.py
"""

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course/modules/CS/CS2/grader"))
from instance import make_instance  # noqa: E402

fails_by_offset = {0.0: 0, 10000.0: 0, 1000000.0: 0}
totals = {0.0: 0, 10000.0: 0, 1000000.0: 0}
means, variances, bad = set(), set(), []
for seed in range(50):
    inst = make_instance(seed)
    p = json.loads(inst["payload"])
    vals = [float(x) for x in p["values"]]
    n = len(vals)
    if not (20 <= n <= 400 and 2 <= p["window"] <= 30 and p["epsilon"] in (0.05, 0.1, 0.2)):
        bad.append(seed)
    if len(p["probes"]) != 10 or not all(0 <= q <= 1 for q in p["probes"]) or not all(math.isfinite(v) for v in vals):
        bad.append(seed)
    fr = [Fraction(v) for v in vals]
    mean = sum(fr) / n
    var = sum((x - mean) ** 2 for x in fr) / (n - 1)
    means.add(float(mean))
    variances.add(float(var))
    # naive formula, order as in the instance docstring
    s = ss = 0.0
    for v in vals:
        s += v
        ss += v * v
    naive_mean = s / n
    naive = (ss - n * naive_mean * naive_mean) / (n - 1)
    offset = min(fails_by_offset, key=lambda o: abs(o - (sum(vals) / n)) if False else 0)  # placeholder, replaced below
    # the offset is the one make_instance drew: recover it from the stream median (values lie within 5 of it)
    med = sorted(vals)[n // 2]
    off = min(fails_by_offset, key=lambda o: abs(o - med))
    totals[off] += 1
    rel = abs(Fraction(naive) - var) / var if var != 0 else Fraction(0)
    if not (rel <= Fraction(1, 10**9)):
        fails_by_offset[off] += 1
print("invalid instances:", bad)
print("distinct exact sample variances across seeds 0-49:", len(variances), "; distinct exact means:", len(means))
print("seeds grouped by offset (median-based):", totals)
print("naive formula fails (relative error > 1e-9) by offset:", fails_by_offset)
print("naive failures total:", sum(fails_by_offset.values()), "of", sum(totals.values()))
