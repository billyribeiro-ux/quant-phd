"""Verifier check (round 17): every file in ledgers/M7/equivalent/ against the reference on the exact-start sweep cases.

Usage: python -I v17_equiv.py <repo_root> <n_random> <n_seeds>. Prints, per file, the number of cases on which the file
and the reference differ (any output field, any float difference above 0), and the number of cases answered by the
reference only and by the file only. Also checks that the reference's exact budget gap is 0 on every answered case.
"""

import importlib.util
import json
import random
import sys
from fractions import Fraction
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
N_RANDOM, N_SEEDS = int(sys.argv[2]), int(sys.argv[3])
sys.argv = ["v17_sweep.py", str(ROOT), "0", "0"]
sys.path.insert(0, str(Path(ROOT, "ledgers/M7/scripts/M7-d-r17")))
import v17_sweep as sw  # noqa: E402
from instance import make_instance  # noqa: E402

EQ = sorted((ROOT / "ledgers/M7/equivalent").glob("*.py"))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


MODS = {p.stem: load(p, "eq_" + p.stem) for p in EQ if p.stem != "README"}
REF = sw.ref


def answer(mod, case):
    try:
        return mod.allocate(json.loads(json.dumps(case)))
    except Exception as exc:  # noqa: BLE001 - recorded as a refusal
        return f"refused:{type(exc).__name__}"


def job(item):
    tag, case = item
    ref_out = answer(REF, case)
    res = {}
    budget_exact = None
    if not isinstance(ref_out, str):
        p = REF._parse(json.loads(json.dumps(case)))
        sol = REF._solve(p)
        budget_exact = sum(sol["w"], Fraction(0)) == 1
    for name, mod in MODS.items():
        out = answer(mod, case)
        if isinstance(ref_out, str) or isinstance(out, str):
            res[name] = ("refusal-differs" if isinstance(ref_out, str) != isinstance(out, str) else "both-refuse", out if isinstance(out, str) else "")
        else:
            res[name] = ("same" if out == ref_out else "differs", "")
    return tag, isinstance(ref_out, str), budget_exact, res


if __name__ == "__main__":
    rng = random.Random(1717)
    items = [(f"seed{s}", json.loads(make_instance(s)["payload"])) for s in range(N_SEEDS)]
    items += [(f"rand{i}", sw.random_case(rng)) for i in range(N_RANDOM)]
    with Pool(20) as pool:
        results = pool.map(job, items, chunksize=16)
    answered = sum(1 for _, refused, _, _ in results if not refused)
    print(f"cases {len(items)}; reference answered {answered}; reference refused {len(items) - answered}")
    print("budget gap exactly zero on every reference answer:", all(b for _, r, b, _ in results if not r))
    for name in MODS:
        differs = [t for t, r, _, res in results if res[name][0] == "differs"]
        ref_only = [t for t, r, _, res in results if res[name][0] == "refusal-differs" and not r]
        file_only = [t for t, r, _, res in results if res[name][0] == "refusal-differs" and r]
        print(f"{name}: differs {len(differs)}; reference answers and file refuses {len(ref_only)}; file answers and reference refuses {len(file_only)}")
