"""Round-12 slice e: for each learner seed in a window, run the reference engine (elicit.py = grader/reference.py) on
the own participant make_instance(seed) and on the second participant make_instance(seed + 7919), exactly as the suite
does, and report exceptions, score failures (min over steps 1e-5 and 1e-6 above 2e-5) and local-maximum failures
(a 0.1 percent move of gamma/lambda/kappa raising the likelihood by more than 1e-9).
usage: seed_scan_r12.py <dir> <lo-hi>   (dir holds test_project.py, instance.py, elicit.py)"""
import json
import os
import sys
from pathlib import Path

work = Path(sys.argv[1])
sys.path.insert(0, str(work))
os.environ.setdefault("QF_SEED", "0")
import instance  # noqa: E402
import test_project as tp  # noqa: E402

lo, hi = (int(x) for x in sys.argv[2].split("-"))


def check(resp):
    try:
        est = tp.sol.estimate(resp)
    except Exception as err:  # the scan records every exception type
        return ("raised", type(err).__name__, str(err)[:70])
    parsed = [tp.parse(r) for r in resp]
    g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
    score = min(tp._largest_score_component(parsed, g, l, k, 1e-5), tp._largest_score_component(parsed, g, l, k, 1e-6))
    if score > 2e-5:
        return ("score", f"{score:.3e}")
    here = tp.oracle_loglik(parsed, g, l, k)
    for step in (1e-3, -1e-3):
        for moved in (
            tp.oracle_loglik(parsed, g * (1 + step), l, k),
            tp.oracle_loglik(parsed, g, l * (1 + step), k),
            tp.oracle_loglik(parsed, g, l, k * (1 + step)),
        ):
            if moved > here + 1e-9:
                return ("localmax", f"{moved - here:.3e}")
    return None


fails = {"own": [], "second": []}
for seed in range(lo, hi + 1):
    own = json.loads(str(instance.make_instance(seed)["responses_json"]))
    sec = json.loads(str(instance.make_instance(seed + 7919)["responses_json"]))
    r1 = check(own)
    r2 = check(sec)
    if r1:
        fails["own"].append((seed, r1))
    if r2:
        fails["second"].append((seed, r2))
print(f"window {lo}-{hi}")
print("own participant failures:", fails["own"])
print("second participant failures:", fails["second"])
