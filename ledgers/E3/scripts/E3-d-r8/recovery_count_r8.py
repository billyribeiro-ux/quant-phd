# Verifier r8: count seeds 0-49 whose estimate lies within k standard errors of truth, for k in 3, 4, 5.
import json, os, sys
sys.path.insert(0, os.getcwd())
import elicit as sol
from instance import make_instance
for k in (3.0, 4.0, 5.0):
    ok, worst = 0, []
    for seed in range(50):
        inst = make_instance(seed)
        fit = sol.estimate(json.loads(str(inst["responses_json"])))
        truth = {"gamma": float(inst["gamma"]), "lambda": float(inst["lambda"]), "kappa": float(inst["kappa"])}
        z = {n: abs(fit[n + "_hat"] - truth[n]) / fit["se_" + n] for n in truth}
        worst.append((max(z.values()), seed))
        if all(v <= k for v in z.values()):
            ok += 1
    print("k=%g within on %d of 50 seeds; max z over seeds %.3f (seed %d)" % (k, ok, *max(worst)))
