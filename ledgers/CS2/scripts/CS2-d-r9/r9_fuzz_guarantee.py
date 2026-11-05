"""Round-9 fuzz: the rank guarantee of the spec (Conventions) for each sketch candidate, plus the reference
docstring's internal claims (g + delta <= floor(2 eps n) + 1 after every add; rank copy invariant).
Usage: python -I r9_fuzz_guarantee.py <streams> <seed>"""
import importlib.util
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
CANDS = {
    "reference": ROOT / "course/modules/CS/CS2/grader/reference.py",
    "alt_a": HERE / "alts/alt_r9_a_exact.py",
    "alt_b": HERE / "alts/alt_r9_b_twopass.py",
    "alt_c": HERE / "alts/alt_r9_c_west_list_deque.py",
    "alt_d": HERE / "alts/alt_r9_d_rank_stats.py",
    "alt_e": HERE / "alts/alt_r9_e_exact_block.py",
    "equiv_d8_01": ROOT / "ledgers/CS2/equivalent/d8_01_sketch_cap_counts_previous_value.py",
    "equiv_d8_02": ROOT / "ledgers/CS2/equivalent/d8_02_sketch_insert_bisect_left.py",
    "equiv_d9_04": ROOT / "ledgers/CS2/equivalent/d9_04_sketch_cap_without_plus_one.py",
    "equiv_rank_clamp": ROOT / "ledgers/CS2/equivalent/rank_target_without_clamp.py",
    "mutant_r9v_03": ROOT / "ledgers/CS2/mutants/r9v_03_sketch_new_tuple_delta_drops_successor_delta.py",
}
STREAMS = int(sys.argv[1]) if len(sys.argv) > 1 else 300
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 9
PROBES = [0.0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1.0, 0.1, 0.2500004, 1 / 3, 0.5000001]
EPS = [0.05, 0.1, 0.2, 0.3, 0.5, 0.9, 0.01]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_stream(rng):
    n = rng.randint(1, 300)
    kind = rng.choice(["uniform", "ties", "sorted", "offset", "sorted_desc"])
    if kind == "uniform":
        vals = [rng.uniform(-5, 5) for _ in range(n)]
    elif kind == "ties":
        vals = [float(rng.randint(0, 4)) for _ in range(n)]
    elif kind == "sorted":
        vals = sorted(rng.uniform(0, 100) for _ in range(n))
    elif kind == "sorted_desc":
        vals = sorted((rng.uniform(0, 100) for _ in range(n)), reverse=True)
    else:
        vals = [round(1e6 + rng.uniform(-5, 5), 1) for _ in range(n)]
    return kind, vals


def guarantee_ok(stream, v, q, eps):
    qn = Fraction(q) * len(stream)
    sl = Fraction(eps) * len(stream)
    below = sum(1 for x in stream if x < v)
    at = sum(1 for x in stream if x <= v)
    return below <= qn + sl and at >= qn - sl


rng = random.Random(SEED)
streams = [make_stream(rng) for _ in range(STREAMS)]
results = {}
for name, path in CANDS.items():
    mod = load(path, f"cand_{name}")
    fails = []
    probes = 0
    for kind, vals in streams:
        for eps in EPS:
            sk = mod.QuantileSketch(eps)
            for x in vals:
                sk.add(x)
            for q in PROBES:
                probes += 1
                v = sk.quantile(q)
                if not guarantee_ok(vals, v, q, eps):
                    fails.append((kind, len(vals), eps, q))
    results[name] = (probes, len(fails), fails[:3])
    print(f"{name}: probes {probes}, guarantee violations {len(fails)}, first {fails[:3]}")

# reference docstring claims: cap bound and rank copy invariant, after every add
ref = load(CANDS["reference"], "ref_internal")
bad_cap = 0
bad_copy = 0
checked = 0
for kind, vals in streams[:120]:
    for eps in (0.05, 0.1, 0.2):
        sk = ref.QuantileSketch(eps)
        for n, x in enumerate(vals, start=1):
            sk.add(x)
            cap = math.floor(2 * Fraction(eps) * n) + 1
            checked += 1
            if any(g + d > cap for g, d in zip(sk._g, sk._delta)):
                bad_cap += 1
            # copy invariant: some copy of stored value i has rank in [R_i, R_i + delta_i]
            ordered = sorted(vals[:n])
            R = 0
            for i, (val, g) in enumerate(zip(sk._values, sk._g)):
                R += g
                d = sk._delta[i]
                ranks = [r for r in range(R, R + d + 1) if 1 <= r <= n and ordered[r - 1] == val]
                if not ranks:
                    bad_copy += 1
                    break
print(f"reference docstring claim g+delta <= floor(2 eps n)+1: violations {bad_cap} in {checked} (stream, eps, n) steps")
print(f"reference docstring claim rank copy invariant: violations {bad_copy}")
