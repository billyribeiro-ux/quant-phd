"""Measure the stated-tolerance properties of projection_repair variants over random and seeded unit-diagonal inputs.

For each module file: unit-diagonal deviation, symmetry, smallest eigenvalue of the output, and the Frobenius
distance from the input compared with the reference. Also counts how often the variant's distance is smaller than the
reference's by more than 1e-6 (which would show it is not the nearest repair the reference finds).
"""
import importlib.util
import math
import random
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyD2-M3-d"
GRADER = f"{ROOT}/course/modules/M/M3/grader"
sys.path.insert(0, GRADER)
import instance as inst_mod  # noqa: E402


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(f"{GRADER}/reference.py", "ref")
files = {
    "reference": f"{GRADER}/reference.py",
    "r6d_gap_only": f"{ROOT}/ledgers/M3/equivalent/r6d_m04_projection_stops_on_gap_only.py",
    "r11d_step_only": f"{ROOT}/ledgers/M3/equivalent/r11d_m02_projection_stops_on_step_only.py",
    "r15d_never_early": f"{ROOT}/ledgers/M3/equivalent/r15d_m03_projection_repair_never_stops_early.py",
}
mods = {k: load(v, k) for k, v in files.items()}


def frob(a, b):
    n = len(a)
    return math.sqrt(sum((a[i][j] - b[i][j]) ** 2 for i in range(n) for j in range(n)))


def inputs():
    rng = random.Random(20261102)
    out = []
    for k in (2, 3, 4, 5):
        for _ in range(60):
            m = [[1.0] * k for _ in range(k)]
            for i in range(k):
                for j in range(i + 1, k):
                    v = rng.uniform(-1, 1)
                    m[i][j] = m[j][i] = v
            out.append(("random", k, m))
    for seed in range(50):
        d = inst_mod.make_instance(seed)
        out.append(("grader_seed", seed, d["corr"]))
    return out


worst = {name: {"diag": 0.0, "asym": 0.0, "min_eig": 0.0, "farther_than_ref": 0.0} for name in mods}
count = 0
for kind, key, corr in inputs():
    count += 1
    k = len(corr)
    rr = ref.projection_repair(corr)
    dref = frob(rr, corr)
    for name, mod in mods.items():
        y = mod.projection_repair(corr)
        diag = max(abs(y[i][i] - 1.0) for i in range(k))
        asym = max(abs(y[i][j] - y[j][i]) for i in range(k) for j in range(k))
        me = min(ref._eigh(y)[0])
        w = worst[name]
        w["diag"] = max(w["diag"], diag)
        w["asym"] = max(w["asym"], asym)
        w["min_eig"] = min(w["min_eig"], me) if w["min_eig"] else me
        w["farther_than_ref"] = max(w["farther_than_ref"], frob(y, corr) - dref)
print("inputs:", count)
for name, w in worst.items():
    print(name, {k: f"{v:.3e}" for k, v in w.items()})
