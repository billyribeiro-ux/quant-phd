"""Round-10 E3-d: compare each alternative's estimate with the reference's on seeds 0-49 (likelihood, score, recovery)."""
import importlib.util
import json
import math
import sys

sys.path.insert(0, "/tmp/E3d_r10_ws/ref")
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/ledgers/E3/scripts/E3-d-r10")
from instance import make_instance  # noqa: E402
import s3d_seed_facts as facts  # noqa: E402  (oracle helpers; module-level code guarded by __main__)
import elicit as ref  # noqa: E402

ALT = sys.argv[1]
ALT_PATH = f"/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/ledgers/E3/scripts/E3-d-r10/alts/{ALT}/elicit.py"
spec = importlib.util.spec_from_file_location("alt", ALT_PATH)
alt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alt)


def score(parsed, fit):
    t = [math.log(fit["gamma_hat"] / (1 - fit["gamma_hat"])), math.log(fit["lambda_hat"]), math.log(fit["kappa_hat"])]
    worst = 0.0
    for h in (1e-5, 1e-6):
        comp = []
        for i in range(3):
            up, dn = list(t), list(t)
            up[i] += h
            dn[i] -= h
            def ll(z):
                return facts.oracle_loglik(parsed, 1 / (1 + math.exp(-z[0])), math.exp(z[1]), math.exp(z[2]))
            comp.append(abs((ll(up) - ll(dn)) / (2 * h)))
        worst_h = max(comp)
        worst = worst_h if h == 1e-5 and worst == 0.0 else min(worst if worst else 1e9, worst_h)
    return worst


rows = []
for seed in range(50):
    inst = make_instance(seed)
    resp = json.loads(inst["responses_json"])
    parsed = [facts.parse(r) for r in resp]
    fr = ref.estimate(resp)
    fa = alt.estimate(resp)
    truth = {"gamma": inst["gamma"], "lambda": inst["lambda"], "kappa": inst["kappa"]}
    within = all(abs(fa[k + "_hat"] - truth[k]) <= 4 * fa["se_" + k] for k in truth)
    rows.append((seed, fr["log_likelihood"], fa["log_likelihood"], within, fa["gamma_hat"], fa["lambda_hat"], fa["kappa_hat"], fr["lambda_hat"], fr["kappa_hat"]))
    sc = score(parsed, fa)
    if fa["log_likelihood"] < fr["log_likelihood"] - 1e-7 or sc > 2e-5 or not within:
        print(f"seed {seed}: ref_ll={fr['log_likelihood']:.9f} alt_ll={fa['log_likelihood']:.9f} alt_score={sc:.3e} within4se={within} alt=(g {fa['gamma_hat']:.5f}, l {fa['lambda_hat']:.4f}, k {fa['kappa_hat']:.4f}) ref=(l {fr['lambda_hat']:.4f}, k {fr['kappa_hat']:.4f})", flush=True)
print("count within 4 SE (alt):", sum(r[3] for r in rows), "of 50")
print("max ll gap alt-ref:", max(r[2] - r[1] for r in rows))
print("min ll gap alt-ref:", min(r[2] - r[1] for r in rows))
