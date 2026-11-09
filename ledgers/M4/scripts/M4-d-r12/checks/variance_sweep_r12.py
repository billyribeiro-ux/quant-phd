"""Re-derive the grader's variance comments (test_project.py lines 31-39) over seeds 0-1999 (verifier round 12).

Uses the reference solution (grader/reference.py) and instance.make_instance from the grader directory. The
'missing matched factor' variant is the same simulator with matched_scale patched to 1.0 (scale sqrt(nu / W)).
"""
import importlib.util
import math
import sys
from pathlib import Path

G = Path("/Users/billyribeiro/.fanout/wt/verifyD12-M4-d/course/modules/M/M4/grader")
sys.path.insert(0, str(G))
import instance  # noqa: E402

spec = importlib.util.spec_from_file_location("ref", G / "reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
orig_matched = ref.matched_scale


def fsum_var(xs):
    m = math.fsum(xs) / len(xs)
    return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def wsig(inst):
    p, c = inst["positions_cents"], inst["cov"]
    n = len(p)
    return math.fsum(p[i] * p[j] * c[i][j] for i in range(n) for j in range(n))


N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
rows = []
for seed in range(N):
    inst = instance.make_instance(seed)
    target = wsig(inst)
    g = ref.simulate_losses(inst["positions_cents"], inst["cov"], inst["n_draws"], seed, "gaussian", None)
    eg = abs(fsum_var(g) / target - 1)
    nu = inst["nu"]
    et = None
    em = None
    if nu >= 5:
        t = ref.simulate_losses(inst["positions_cents"], inst["cov"], inst["n_draws"], seed, "student_t", nu)
        et = abs(fsum_var(t) / target - 1)
    ref.matched_scale = lambda v: 1.0
    try:
        mt = ref.simulate_losses(inst["positions_cents"], inst["cov"], inst["n_draws"], seed, "student_t", nu)
        em = abs(fsum_var(mt) / target - 1)
    finally:
        ref.matched_scale = orig_matched
    rows.append((seed, nu, eg, et, em))
    if seed % 200 == 0:
        print("progress", seed, flush=True)

print("seeds", N)
print("gaussian max rel err", max(r[2] for r in rows), "at seed", max(rows, key=lambda r: r[2])[0])
for nu in range(3, 9):
    sub = [r for r in rows if r[1] == nu]
    if not sub:
        continue
    tmax = max((r[3] for r in sub if r[3] is not None), default=None)
    print(f"nu={nu}: seeds {len(sub)}", end=" ")
    if tmax is not None:
        best = max((r for r in sub if r[3] is not None), key=lambda r: r[3])
        print(f"reference t max rel err {tmax:.4f} at seed {best[0]}", end=" ")
        over = sum(1 for r in sub if r[3] is not None and r[3] > 0.30)
        print(f"ref over 0.30: {over}", end=" ")
        mis = [r for r in sub if r[4] is not None and r[4] > 0.30]
        print(f"missing-factor over 0.30: {len(mis)}/{len(sub)}", end="")
    else:
        print("(t variance not checked at this nu)", end="")
    print()
r3 = [r for r in rows if r[1] == 3]
print("nu=3 reference t rel err at seed 1093:", [r[3] for r in rows if r[0] == 1093])
print("nu=3 seeds with largest rel err (top 3):", sorted(((r[4], r[0]) for r in r3), reverse=True)[:3])
