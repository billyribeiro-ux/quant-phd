"""Counts how often the stall branch of _maximise (the `break` that replaced the r14 raise) executes.

Usage: stall_branch_probe.py <grader-dir> <work-dir>. Copies reference.py into <work-dir> with one counter line added
at the break, then runs the suite's own (seed s) and second (seed s + 7919) participants for s in 0..399.
"""
import json
import os
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor

GRADER, WORK = sys.argv[1], sys.argv[2]
os.makedirs(WORK, exist_ok=True)
src = open(os.path.join(GRADER, "reference.py"), encoding="utf-8").read()
old = '            break\n    raise RuntimeError("the likelihood maximisation did not converge")'
assert src.count(old) == 1, src.count(old)
instr = src.replace(old, '            _HIT.append(1)\n            break\n    raise RuntimeError("the likelihood maximisation did not converge")')
instr = instr.replace("def _maximise(", "_HIT: list[int] = []\n\n\ndef _maximise(", 1)
open(os.path.join(WORK, "reference_instr.py"), "w", encoding="utf-8").write(instr)
shutil.copy(os.path.join(GRADER, "instance.py"), WORK)
sys.path.insert(0, WORK)


def one(task):
    import instance as inst_mod
    import reference_instr as ref

    kind, seed = task
    s = seed if kind == "own" else seed + 7919
    inst = inst_mod.make_instance(s)
    resp = json.loads(str(inst["responses_json"]))
    ref._HIT.clear()
    try:
        ref.estimate(resp)
        outcome = "ok"
    except Exception as e:
        outcome = type(e).__name__ + ": " + str(e)[:60]
    return (kind, seed, outcome, len(ref._HIT))


if __name__ == "__main__":
    tasks = [(k, s) for s in range(400) for k in ("own", "second")]
    with ProcessPoolExecutor(max_workers=6) as ex:
        rows = list(ex.map(one, tasks, chunksize=4))
    hits = [r for r in rows if r[3]]
    print("TOTAL", len(rows), "STALL_BRANCH_HITS", sum(r[3] for r in rows), "RUNS_WITH_HIT", len(hits))
    print("HIT_RUNS", hits)
    print("RAISED", sorted((r[0], r[1], r[2]) for r in rows if r[2] != "ok"))
