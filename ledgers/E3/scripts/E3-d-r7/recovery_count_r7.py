"""Recovery count over seeds 0-49 with the reference engine: how many seeds meet 4 SE and 5 SE on every parameter.
Run with the work dir (instance.py and elicit.py = reference) as the working directory."""
import sys, json
sys.path.insert(0, "/tmp/E3d_r7/work")
from instance import make_instance
import elicit
within4 = within5 = 0
worst = []
for seed in range(50):
    inst = make_instance(seed)
    resp = json.loads(inst["responses_json"])
    est = elicit.estimate(resp)
    tr = {"gamma": inst["gamma"], "lambda": inst["lambda"], "kappa": inst["kappa"]}
    ratios = {n: abs(est[n + "_hat"] - tr[n]) / est["se_" + n] for n in ("gamma", "lambda", "kappa")}
    within4 += all(r <= 4 for r in ratios.values())
    within5 += all(r <= 5 for r in ratios.values())
    if not all(r <= 5 for r in ratios.values()):
        worst.append((seed, ratios))
print("seeds within 4 SE on every parameter:", within4, "of 50")
print("seeds within 5 SE on every parameter:", within5, "of 50")
print("seeds failing 5 SE:", worst)
