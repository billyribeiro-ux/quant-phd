"""Recovery count (the suite's test_estimate_recovers... check) for one engine on seeds 0-49, with per-seed misses."""
import json
import os
import shutil
import sys
import tempfile

engine, grader = sys.argv[1], sys.argv[2]
work = tempfile.mkdtemp(prefix="e3d-rec-")
for f in ("test_project.py", "instance.py"):
    shutil.copy(os.path.join(grader, f), work)
shutil.copy(engine, os.path.join(work, "elicit.py"))
sys.path.insert(0, work)
os.environ["QF_SEED"] = "0"
import elicit  # noqa: E402
from instance import make_instance  # noqa: E402

within = 0
misses = []
for seed in range(50):
    inst = make_instance(seed)
    resp = json.loads(str(inst["responses_json"]))
    try:
        fit = elicit.estimate(resp)
    except Exception as err:  # noqa: BLE001
        misses.append((seed, type(err).__name__))
        continue
    truth = {"gamma": float(inst["gamma"]), "lambda": float(inst["lambda"]), "kappa": float(inst["kappa"])}
    ok = all(abs(fit[n + "_hat"] - truth[n]) <= 4.0 * fit["se_" + n] for n in truth)
    if ok:
        within += 1
    else:
        misses.append((seed, {n: round(fit[n + "_hat"], 4) for n in truth}, {n: round(truth[n], 4) for n in truth}))
print("within-4SE count:", within, "of 50")
for m in misses:
    print(" miss", m)
shutil.rmtree(work, ignore_errors=True)
