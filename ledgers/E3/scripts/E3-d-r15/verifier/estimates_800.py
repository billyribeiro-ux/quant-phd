"""Pinned-reference estimates for the suite's participants: own (seed s) and second (s + 7919), s in 0..399.

Usage: estimates_800.py <grader-dir>. Prints one line per participant and a summary. Uses only the grader's own
instance.py and reference.py (no copies of the engine).
"""
import json
import sys
from concurrent.futures import ProcessPoolExecutor

GRADER = sys.argv[1]
sys.path.insert(0, GRADER)


def one(task):
    import instance as inst_mod
    import reference as ref

    kind, seed = task
    s = seed if kind == "own" else seed + 7919
    inst = inst_mod.make_instance(s)
    resp = json.loads(str(inst["responses_json"]))
    try:
        r = ref.estimate(resp)
        return (kind, seed, "ok", r["gamma_hat"], r["lambda_hat"], r["kappa_hat"])
    except Exception as e:  # the outcome is the point of this scan
        return (kind, seed, type(e).__name__ + ": " + str(e)[:80], None, None, None)


if __name__ == "__main__":
    tasks = [(k, s) for s in range(400) for k in ("own", "second")]
    with ProcessPoolExecutor(max_workers=6) as ex:
        rows = list(ex.map(one, tasks, chunksize=4))
    for row in rows:
        print(*row)
    ok = [r for r in rows if r[2] == "ok"]
    print("SUMMARY total", len(rows), "ok", len(ok), "raised", len(rows) - len(ok))
    print("SUMMARY raised_list", [(r[0], r[1], r[2][:60]) for r in rows if r[2] != "ok"])
    mx = max(ok, key=lambda r: r[3])
    mn = min(ok, key=lambda r: r[3])
    print("SUMMARY max_gamma_hat", mx[3], mx[0], mx[1])
    print("SUMMARY min_gamma_hat", mn[3], mn[0], mn[1])
    print("SUMMARY count_below_0.11", sum(1 for r in ok if r[3] < 0.11), "count_above_0.71", sum(1 for r in ok if r[3] > 0.71))
