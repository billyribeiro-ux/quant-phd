"""Verifier probe (round 18): the fixed fixtures' estimates and the CRRA tie value, against the numbers the suite and the
page state. Usage (repo root): .venv/bin/python -I ledgers/E3/scripts/E3-d-r18/fixtures_r18.py <repo-root>"""

import json
import os
import shutil
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1])
work = Path(tempfile.mkdtemp(prefix="e3d-r18-fix-"))
for f in ("test_project.py", "instance.py"):
    shutil.copy(root / "course/modules/E/E3/grader" / f, work)
shutil.copy(root / "course/modules/E/E3/grader/reference.py", work / "elicit.py")
sys.path.insert(0, str(work))
os.environ["QF_SEED"] = "0"
import elicit  # noqa: E402
import test_project as tp  # noqa: E402
from instance import make_instance  # noqa: E402

for seed in (30, 49):
    resp = json.loads(str(make_instance(seed)["responses_json"]))
    f = elicit.estimate(resp)
    print(f"seed {seed}: gamma_hat {f['gamma_hat']:.4f} lambda_hat {f['lambda_hat']:.4f} kappa_hat {f['kappa_hat']:.4f}")
responses = [
    {"pair_id": i, "choice": c, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb}
    for i, c, pa, qa, pb, qb in tp.FIXED_26_ANSWERS
]
f = elicit.estimate(responses)
print(f"FIXED_26 gamma_hat {f['gamma_hat']:.4f} (n={len(responses)})")
bside = [
    {
        "pair_id": i,
        "choice": tp.B_SIDE_CHOICES[i],
        "prizes_a": [tp.B_SIDE_SURE_A[i]],
        "probs_a": ["1"],
        "prizes_b": tp.B_SIDE_LOTTERIES[i][0],
        "probs_b": tp.B_SIDE_LOTTERIES[i][1],
    }
    for i in range(len(tp.B_SIDE_CHOICES))
]
f = elicit.estimate(bside)
print(f"B-side gamma_hat {f['gamma_hat']:.4f} (n={len(bside)})")
got = elicit.certainty_equivalent_cents("crra", [97, 391], [Fraction(1, 2), Fraction(1, 2)], {"gamma": 0.5}, 1)
print("CRRA tie gamma 1/2, wealth 1, prizes 97/391:", got, "(exact 219.5; test accepts 219 or 220)")
print("raw float of the CRRA change:", repr(elicit._crra_change([97, 391], [Fraction(1, 2), Fraction(1, 2)], 0.5, 1)))
shutil.rmtree(work, ignore_errors=True)
