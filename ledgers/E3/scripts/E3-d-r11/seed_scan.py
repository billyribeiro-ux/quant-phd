"""Round-11: for the suite's instance generator (grader/instance.py), estimate each seed in a window with a given engine dir
and report exceptions, the score at the output (min over steps 1e-5/1e-6), and the local-max excess. usage: seed_scan.py <dir> <lo-hi>"""
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
raised, bad = [], []
for seed in range(lo, hi + 1):
    resp = json.loads(str(instance.make_instance(seed)["responses_json"]))
    try:
        est = tp.sol.estimate(resp)
    except Exception as err:
        raised.append((seed, type(err).__name__, str(err)[:80]))
        continue
    parsed = [tp.parse(r) for r in resp]
    g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
    score = min(tp._largest_score_component(parsed, g, l, k, 1e-5), tp._largest_score_component(parsed, g, l, k, 1e-6))
    if score > 2e-5:
        bad.append((seed, score))
print(f"window {lo}-{hi}: raised={len(raised)} score_fail={len(bad)}")
for r in raised[:12]:
    print("  raised seed", r[0], r[1], r[2])
for b in bad[:12]:
    print("  score_fail seed", b[0], f"{b[1]:.3e}")
