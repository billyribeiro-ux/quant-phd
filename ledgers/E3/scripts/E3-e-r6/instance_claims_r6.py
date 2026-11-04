# Checks the instance.py docstring claims over seeds 0-49, their second participants (seed+7919) and seed 30
import json, sys
from fractions import Fraction as F
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD6-E3-e/course/modules/E/E3/grader")
from instance import make_instance
seeds = list(range(50)) + [s + 7919 for s in range(50)] + [30]
mags = []; prizes_n = set(); dens = set(); mixed_counts = []; kap = {}; gam=[]; lam=[]; wealth=[]; k_lt1 = []
for s in seeds:
    inst = make_instance(s)
    resp = json.loads(str(inst["responses_json"]))
    if s in range(50) or s == 30:
        kap[s] = float(inst["kappa"])
    gam.append(float(inst["gamma"])); lam.append(float(inst["lambda"])); kap.setdefault("all", []).append(float(inst["kappa"]))
    wealth.append(int(inst["wealth_cents"]))
    m = 0
    for r in resp:
        mixed = False
        for pr, qr in ((r["prizes_a"], r["probs_a"]), (r["prizes_b"], r["probs_b"])):
            prizes_n.add(len(pr))
            for x, q in zip(pr, qr):
                mags.append(abs(int(x)))
                dens.add(F(q).denominator)
            g = any(int(x) > 0 and F(q) > 0 for x, q in zip(pr, qr)); l = any(int(x) < 0 and F(q) > 0 for x, q in zip(pr, qr))
            mixed = mixed or (g and l)
        m += mixed
    mixed_counts.append((s, len(resp), m))
print("seeds", len(seeds), "pairs per instance", sorted({n for _, n, _ in mixed_counts}), "min mixed", min(m for *_, m in mixed_counts))
print("prizes per lottery", sorted(prizes_n), "denominators", sorted(dens))
print("prize magnitude min/max cents", min(mags), max(mags))
print("gamma range", min(gam), max(gam), "lambda range", min(lam), max(lam), "kappa range", min(kap["all"]), max(kap["all"]))
print("wealth range", min(wealth), max(wealth))
print("seed 30 kappa", kap[30], "gamma", make_instance(30)["gamma"], "lambda", make_instance(30)["lambda"])
print("seeds 0-49 kappa below 1:", [s for s in range(50) if kap[s] < 1])
