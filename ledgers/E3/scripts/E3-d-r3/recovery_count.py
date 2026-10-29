"""Round-3: how many of seeds 0-49 recover the true parameters within 4 and within 5 standard errors (reference engine).
Plan section 6.7 / Q12 proposes '4 SE on at least 47 of seeds 0-49'; the suite tests 5 SE per seed.
Usage (from the checkout): .venv/bin/python -I ledgers/E3/scripts/E3-d-r3/recovery_count.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course/modules/E/E3/grader"))
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

within4 = within5 = 0
worst = []
for s in range(50):
    inst = make_instance(s)
    est = ref.estimate(json.loads(inst["responses_json"]))
    t = {"gamma_hat": inst["gamma"], "lambda_hat": inst["lambda"], "kappa_hat": inst["kappa"]}
    z = []
    for name, key in (("gamma_hat", "se_gamma"), ("lambda_hat", "se_lambda"), ("kappa_hat", "se_kappa")):
        z.append(abs(est[name] - t[name]) / est[key])
    within4 += all(v <= 4 for v in z)
    within5 += all(v <= 5 for v in z)
    worst.append((round(max(z), 2), s))
print("seeds within 4 SE on all three:", within4, "of 50")
print("seeds within 5 SE on all three:", within5, "of 50")
print("largest z per seed (top 5):", sorted(worst, reverse=True)[:5])
