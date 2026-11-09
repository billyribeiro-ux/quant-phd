"""Independent recomputation of the project page numbers and the grader docstring claims (CS2 slice d, round 14).

Usage: python -I numbers_r14.py   (run from the checkout root; reads the grader instance and reference only)
"""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "CS" / "CS2" / "grader"


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


inst = load("instance_r14", GRADER / "instance.py")
ref = load("reference_r14", GRADER / "reference.py")
import json  # noqa: E402


def close(a: float, b: float) -> bool:
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= max(1e-9, 1e-9 * max(abs(a), abs(b)))


def exact(values: list[float]) -> tuple[Fraction, Fraction]:
    fr = [Fraction(x) for x in values]
    n = len(fr)
    mean = sum(fr, Fraction(0)) / n
    m2 = sum(((x - mean) ** 2 for x in fr), Fraction(0))
    return mean, (m2 / (n - 1) if n > 1 else Fraction(0))


# ---- A. instance docstring: offsets, naive formula failures, reference Welford
groups: dict[float, list[int]] = {0.0: [], 10000.0: [], 1000000.0: []}
naive_fail: dict[float, list[int]] = {0.0: [], 10000.0: [], 1000000.0: []}
ref_fail: list[int] = []
streams: dict[int, tuple[float, ...]] = {}
offset_of: dict[int, float] = {}
for seed in range(50):
    d = inst.make_instance(seed)
    payload = json.loads(d["payload"])
    values = [float(x) for x in payload["values"]]
    streams[seed] = tuple(values)
    # the offset make_instance draws (replicates its rng draws)
    rng = random.Random(seed)
    rng.randint(20, 400)
    offset = rng.choice(inst.OFFSETS)
    offset_of[seed] = offset
    groups[offset].append(seed)
    mean_e, var_e = exact(values)
    s = 0.0
    ss = 0.0
    for x in values:
        s += x
        ss += x * x
    n = len(values)
    naive_var = (ss - n * (s / n) * (s / n)) / (n - 1)
    naive_mean = s / n
    if not (close(naive_var, float(var_e)) and close(naive_mean, float(mean_e))):
        naive_fail[offset].append(seed)
    acc = ref.WelfordAccumulator()
    for x in values:
        acc.update(x)
    if not (close(acc.mean(), float(mean_e)) and close(acc.variance(1), float(var_e))):
        ref_fail.append(seed)
print("A. offsets: " + ", ".join(f"{k:g}: {len(v)} seeds" for k, v in groups.items()))
for k in groups:
    print(f"A. naive formula fails at offset {k:g}: {len(naive_fail[k])} of {len(groups[k])} seeds {naive_fail[k]}")
print(f"A. reference Welford fails: {len(ref_fail)} of 50 {ref_fail}")
print(f"A. distinct streams: {len(set(streams.values()))} of 50")
print(f"A. seeds 0-9 offsets: {[offset_of[s] for s in range(10)]}")
print(f"A. seeds 0-9 lengths: {[len(streams[s]) for s in range(10)]}")

# ---- B. the lab 2 and lab 3 numbers, recomputed with exact Fractions
lab2 = [1000002, 1000005, 1000001, 1000004, 1000009, 1000003, 1000006, 1000000]
m, v = exact([float(x) for x in lab2])
print(f"B. lab2 exact mean {float(m):.6f} sample variance {float(v):.6f}")
lab3 = ["10003.2", "10001.7", "10007.5", "10000.4", "10004.9", "10002.1", "10009.6", "10001.0", "10006.3", "10003.8", "10005.5"]
ex = [Fraction(s) for s in lab3]
print(f"B. lab3 sum {sum(ex)} mean {float(sum(ex)/11):.6f}")
m3, v3 = exact([float(s) for s in lab3])
print(f"B. lab3 exact mean {float(m3):.6f} exact sample variance {float(v3):.6f}")
print(f"B. lab3 last4 min {min(float(s) for s in lab3[-4:]):.1f} max {max(float(s) for s in lab3[-4:]):.1f}")
tgt = max(1, math.ceil(Fraction(1, 2) * 11 - Fraction("0.1") * 11))
print(f"B. lab3 median target {tgt}; qn-eps*n = {Fraction(1,2)*11 - Fraction('0.1')*11} (= {float(Fraction(1,2)*11 - Fraction('0.1')*11)}); {tgt}th smallest {sorted(ex)[tgt-1]}")

# ---- C. the two witnesses in the rank-target tests and the 'floats give 1' claim
qn_e = Fraction(0.1) * 20 - Fraction(0.05) * 20
print(f"C. q=0.1 n=20 eps=0.05 exact qn-eps*n = {float(qn_e):.20f} ceil={math.ceil(qn_e)}; float version = {0.1*20 - 0.05*20} ceil={math.ceil(0.1*20-0.05*20)}")
qn2 = Fraction(0.2500004) * 20
print(f"C. q=0.2500004 n=20 qn={float(qn2)} exact target ceil(qn-eps*n)={math.ceil(qn2 - Fraction(0.05)*20)}; q=0.25 target={math.ceil(Fraction(0.25)*20 - Fraction(0.05)*20)}")

# ---- D. the reference sketch's docstring claims: g sums to n, g+delta <= floor(2 eps n)+1, rank interval
bad_sum = bad_cap = bad_rank = 0
rng = random.Random(14)
for trial in range(400):
    eps = rng.choice([0.05, 0.1, 0.2, 0.3, 0.5, 0.9])
    n = rng.randint(1, 300)
    kind = trial % 4
    if kind == 0:
        xs = [round(rng.uniform(-5, 5), 1) for _ in range(n)]
    elif kind == 1:
        xs = sorted(round(rng.uniform(0, 1e6), 6) for _ in range(n))
    elif kind == 2:
        xs = [float(rng.randint(0, 3)) for _ in range(n)]
    else:
        xs = [rng.random() for _ in range(n)]
    sk = ref.QuantileSketch(eps)
    for x in xs:
        sk.add(x)
    if sum(sk._g) != len(xs):
        bad_sum += 1
    cap = math.floor(2 * Fraction(eps) * len(xs)) + 1
    if any(g + d > cap for g, d in zip(sk._g, sk._delta, strict=True)):
        bad_cap += 1
    # rank interval: for each stored value, some copy has rank in [rmin, rmin + delta]
    rmin = 0
    for val, g, d in zip(sk._values, sk._g, sk._delta, strict=True):
        rmin += g
        lo = sum(1 for x in xs if x < val) + 1
        hi = sum(1 for x in xs if x <= val)
        if max(lo, rmin) > min(hi, rmin + d):
            bad_rank += 1
            break
print(f"D. reference sketch: trials 400, sum(g)!=n {bad_sum}, g+delta>floor(2 eps n)+1 {bad_cap}, rank-interval violations {bad_rank}")

# ---- E. rank guarantee battery on the reference (exact counts, the page's two inequalities)
viol = 0
checks = 0
rng = random.Random(1414)
for trial in range(600):
    eps = rng.choice([0.05, 0.1, 0.2, 0.3, 0.5, 0.9])
    n = rng.randint(1, 400) if trial % 3 else rng.randint(1, 40)
    kind = trial % 5
    if kind == 0:
        xs = [round(rng.uniform(-5, 5), 1) for _ in range(n)]
    elif kind == 1:
        xs = sorted(round(rng.uniform(1e4, 1e4 + 10), 6) for _ in range(n))
    elif kind == 2:
        xs = [float(rng.randint(0, 4)) for _ in range(n)]
    elif kind == 3:
        xs = sorted((round(rng.uniform(-5, 5), 1) for _ in range(n)), reverse=True)
    else:
        xs = [rng.uniform(0, 1) for _ in range(n)]
    sk = ref.QuantileSketch(eps)
    for x in xs:
        sk.add(x)
    qs = [k / 200 for k in range(201)] + [rng.random() for _ in range(20)]
    for q in qs:
        v = sk.quantile(q)
        below = sum(1 for x in xs if x < v)
        at_or_below = sum(1 for x in xs if x <= v)
        qn = Fraction(q) * n
        sl = Fraction(eps) * n
        checks += 1
        if not (below <= qn + sl and at_or_below >= qn - sl):
            viol += 1
print(f"E. reference guarantee battery: {checks} checks, violations {viol}")
