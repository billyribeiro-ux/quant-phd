"""Round-9: instance validity, distinctness, and the naive-formula counts printed in instance.py's docstring."""
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course" / "modules" / "CS" / "CS2" / "grader"))
from instance import make_instance  # noqa: E402

OFFSETS = [0.0, 10_000.0, 1_000_000.0]


def exact_sample_var(vals):
    fr = [Fraction(x) for x in vals]
    n = len(fr)
    mean = sum(fr) / n
    return sum((x - mean) ** 2 for x in fr) / (n - 1), mean


def naive(vals):
    s = ss = 0.0
    for x in vals:
        s += x
        ss += x * x
    n = len(vals)
    mean = s / n
    return (ss - n * mean * mean) / (n - 1)


def close(a, b):
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= max(1e-9, 1e-9 * max(abs(a), abs(b)))


# 1. validity and distinctness for seeds 0..19
rows = []
for seed in range(20):
    inst = make_instance(seed)
    p = json.loads(inst["payload"])
    inv = json.loads(inst["invalid"])
    vals = p["values"]
    assert 20 <= len(vals) <= 400, seed
    assert all(math.isfinite(v) for v in vals), seed
    assert 2 <= p["window"] <= 30, seed
    assert p["epsilon"] in (0.05, 0.1, 0.2), seed
    assert len(p["probes"]) == 10 and all(0 <= q <= 1 for q in p["probes"]), seed
    assert "SIMULATED" in inst["label"], seed
    assert inv["kind"] in ("window_zero", "epsilon_one", "q_above_one", "welford_nan", "rolling_nan", "sketch_nan")
    var, mean = exact_sample_var(vals)
    rows.append((len(vals), p["window"], p["epsilon"], float(var), float(mean)))
print("seeds 0-19 valid: True")
print("distinct (n, window, eps, exact sample variance) tuples:", len({r[:4] for r in rows}), "of 20")
print("distinct exact means:", len({r[4] for r in rows}), "of 20")

# 2. naive-formula counts (docstring of instance.py lines 8-13) over seeds 0-49
fails = {o: [] for o in OFFSETS}
ok_seeds = {o: [] for o in OFFSETS}
offset_of = {}
for seed in range(50):
    inst = make_instance(seed)
    vals = json.loads(inst["payload"])["values"]
    # recover the offset drawn by make_instance: the stream lies within 5 of the offset
    off = min(OFFSETS, key=lambda o: min(abs(v - o) for v in vals[:1]))
    offset_of[seed] = off
    var, _ = exact_sample_var(vals)
    if close(naive(vals), float(var)):
        ok_seeds[off].append(seed)
    else:
        fails[off].append(seed)
for o in OFFSETS:
    total = len(fails[o]) + len(ok_seeds[o])
    print(f"offset {o:>12.0f}: seeds {total}, naive fails {len(fails[o])}, naive passes {ok_seeds[o]}")
