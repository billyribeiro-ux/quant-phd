"""Verifier probe (round 18): the reference's estimate on the suite's own participant (seed s) and second participant
(seed s + 7919) for s in 0..399. Prints the outcome per participant, then the counts, the largest and smallest gamma_hat.
Usage (repo root): .venv/bin/python -I ledgers/E3/scripts/E3-d-r18/estimates_800_r18.py
"""

import json
import os
import shutil
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path.cwd()
GRADER = ROOT / "course/modules/E/E3/grader"
WORK = Path(tempfile.mkdtemp(prefix="e3d-r18-est-"))
shutil.copy(GRADER / "instance.py", WORK)
shutil.copy(GRADER / "reference.py", WORK / "elicit.py")
sys.path.insert(0, str(WORK))


def one(task: tuple[str, int]) -> tuple[str, int, str, float | None]:
    import elicit as ref
    import instance as inst_mod

    kind, seed = task
    s = seed if kind == "own" else seed + 7919
    resp = json.loads(str(inst_mod.make_instance(s)["responses_json"]))
    try:
        r = ref.estimate(resp)
    except Exception as err:
        return (kind, seed, f"ERR {type(err).__name__}", None)
    return (kind, seed, "OK", r["gamma_hat"])


if __name__ == "__main__":
    tasks = [(k, s) for s in range(400) for k in ("own", "second")]
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one, tasks, chunksize=4))
    shutil.rmtree(WORK, ignore_errors=True)
    for kind, seed, outcome, g in rows:
        print(kind, seed, outcome, "" if g is None else f"{g:.6f}")
    ok = [(g, k, s) for k, s, o, g in rows if g is not None]
    print("TOTAL", len(rows), "ESTIMATES", len(ok), "RAISED", len(rows) - len(ok))
    print("MAX gamma_hat", max(ok), "MIN gamma_hat", min(ok))
