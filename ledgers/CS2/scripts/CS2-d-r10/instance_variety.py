"""Sample 20 seeds: each instance is valid and its answers differ (reference Welford mean/variance, sketch median, rolling max)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "course/modules/CS/CS2/grader")
import importlib.util  # noqa: E402

from instance import make_instance  # type: ignore[import-not-found]  # noqa: E402

spec = importlib.util.spec_from_file_location("ref", Path("course/modules/CS/CS2/grader/reference.py").resolve())
assert spec and spec.loader
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
answers = []
for seed in range(0, 50, 2)[:20]:
    p = json.loads(make_instance(seed)["payload"])
    vals = [float(v) for v in p["values"]]
    acc = ref.WelfordAccumulator()
    for x in vals:
        acc.update(x)
    sk = ref.QuantileSketch(p["epsilon"])
    for x in vals:
        sk.add(x)
    rm = ref.RollingMinMax(p["window"])
    for x in vals:
        rm.push(x)
    ok = len(vals) >= 20 and all(abs(x) < 1e7 for x in vals[:1]) and 2 <= p["window"] <= 30
    answers.append((seed, len(vals), p["epsilon"], round(acc.mean(), 6), round(acc.variance(1), 6), sk.quantile(0.5), rm.maximum(), ok))
for row in answers:
    print(row)
print("distinct (mean, variance) pairs:", len({(r[3], r[4]) for r in answers}), "of", len(answers))
print("distinct median answers:", len({r[5] for r in answers}), "; all valid:", all(r[7] for r in answers))
