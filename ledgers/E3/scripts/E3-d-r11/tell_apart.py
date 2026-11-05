"""Round-11: does an engine pass the suite's own score and local-maximum checks on many participants?
usage: tell_apart.py <dir containing elicit.py, instance.py, test_project.py> <seed-list e.g. 0-49>
Prints, per participant, the score (min over steps 1e-5/1e-6), the local-max violation and the B-side/A-side sets."""
import importlib.util
import json
import math
import os
import sys
from pathlib import Path

work = Path(sys.argv[1])
sys.path.insert(0, str(work))
os.environ.setdefault("QF_SEED", "0")
import instance  # noqa: E402
import test_project as tp  # noqa: E402  (imports elicit from work dir)

lo, hi = (int(x) for x in sys.argv[2].split("-"))
worst = (0.0, None)
fails = []
for seed in list(range(lo, hi + 1)) + [7919, 30, 49]:
    resp = json.loads(str(instance.make_instance(seed)["responses_json"]))
    parsed = [tp.parse(r) for r in resp]
    est = tp.sol.estimate(resp)
    g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
    score = min(tp._largest_score_component(parsed, g, l, k, 1e-5), tp._largest_score_component(parsed, g, l, k, 1e-6))
    here = tp.oracle_loglik(parsed, g, l, k)
    lm = 0.0
    for step in (1e-3, -1e-3):
        for v in (tp.oracle_loglik(parsed, g * (1 + step), l, k), tp.oracle_loglik(parsed, g, l * (1 + step), k), tp.oracle_loglik(parsed, g, l, k * (1 + step))):
            lm = max(lm, v - here)
    if score > 2e-5 or lm > 1e-9:
        fails.append((seed, score, lm))
    if score > worst[0]:
        worst = (score, seed)
print(f"participants={hi - lo + 4} score_fail_or_localmax_fail={len(fails)} worst_score={worst[0]:.3e} at seed {worst[1]}")
for f in fails[:10]:
    print("  FAIL seed", f[0], "score", f"{f[1]:.3e}", "localmax_excess", f"{f[2]:.3e}")
