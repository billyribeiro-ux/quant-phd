"""Diagnostic: estimate on the B-side set, the 26-response fixture and seed 0 for one engine; prints the score."""
import math
import os
import shutil
import sys
import tempfile

engine, grader = sys.argv[1], sys.argv[2]
work = tempfile.mkdtemp(prefix="e3d-diag-")
for f in ("test_project.py", "instance.py"):
    shutil.copy(os.path.join(grader, f), work)
shutil.copy(engine, os.path.join(work, "elicit.py"))
sys.path.insert(0, work)
os.environ["QF_SEED"] = "0"
import test_project as tp  # noqa: E402

alt = tp.sol
resp = [
    {"pair_id": i, "choice": tp.B_SIDE_CHOICES[i], "prizes_a": [tp.B_SIDE_SURE_A[i]], "probs_a": ["1"],
     "prizes_b": tp.B_SIDE_LOTTERIES[i][0], "probs_b": tp.B_SIDE_LOTTERIES[i][1]}
    for i in range(12)
]
f26 = [{"pair_id": i, "choice": c, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb}
       for i, c, pa, qa, pb, qb in tp.FIXED_26_ANSWERS]
for name, rs in (("b-side12", resp), ("fixed26", f26), ("seed0", tp.RESPONSES)):
    try:
        r = alt.estimate(rs)
    except Exception as e:  # noqa: BLE001
        print(name, "RAISED", type(e).__name__, str(e)[:90])
        continue
    parsed = [tp.parse(x) for x in rs]
    xi = [math.log(r["gamma_hat"] / (1 - r["gamma_hat"])), math.log(r["lambda_hat"]), math.log(r["kappa_hat"])]
    print(name, "gamma %.6f lambda %.6f kappa %.6f" % (r["gamma_hat"], r["lambda_hat"], r["kappa_hat"]),
          "max|score|(1e-5) %.3g" % tp._largest_score_component(parsed, r["gamma_hat"], r["lambda_hat"], r["kappa_hat"], 1e-5))
shutil.rmtree(work, ignore_errors=True)
