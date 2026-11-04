"""Samples 20 seeds: each instance is valid under project.html, and the reference answers differ across seeds.

Usage: python -I ledgers/M4/scripts/M4-d-r8/checks/instances_sample_r8.py
"""

import importlib.util
import math
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-M4-d")
G = ROOT / "course/modules/M/M4/grader"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


inst_mod = load(G / "instance.py", "instance_mod")
ref = load(G / "reference.py", "ref_mod")
seeds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 50, 123, 400, 777, 1000, 1093, 1500, 1999, 2500, 4096]
rows = []
for s in seeds:
    inst = inst_mod.make_instance(s)
    pos, cov, nu, n = inst["positions_cents"], inst["cov"], inst["nu"], inst["n_draws"]
    valid = (
        inst["label"] == "SIMULATED"
        and all(type(w) is int and w > 0 for w in pos)
        and 3 <= nu <= 8
        and n % 100 != 0 and n <= 20_000
        and all(cov[i][j] == cov[j][i] for i in range(len(pos)) for j in range(len(pos)))
        and len(cov) == len(pos)
    )
    losses = ref.simulate_losses(pos, cov, n, s, "student_t", nu)
    q = ref.quantile_99(losses)
    rows.append((s, len(pos), nu, n, valid, q))
    print(f"seed {s:5d}: assets {len(pos)} nu {nu} draws {n:5d} valid {valid} student_t_99pct_loss {q}")
print("all valid:", all(r[4] for r in rows))
print("distinct 99% losses:", len({r[5] for r in rows}), "of", len(rows))
print("distinct (nu, draws, assets):", len({(r[1], r[2], r[3]) for r in rows}))
