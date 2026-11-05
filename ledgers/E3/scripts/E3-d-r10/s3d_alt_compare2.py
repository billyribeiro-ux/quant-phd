"""Round-10 E3-d: each alternative vs the reference on seeds 0-49: recovery count, likelihood gap, score, exceptions."""
import importlib.util, json, math, sys
sys.path.insert(0, "/tmp/E3d_r10_ws/ref")
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/ledgers/E3/scripts/E3-d-r10")
from instance import make_instance
import s3d_seed_facts as facts
import elicit as ref

name = sys.argv[1]
spec = importlib.util.spec_from_file_location("alt", f"/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/ledgers/E3/scripts/E3-d-r10/alts/{name}/elicit.py")
alt = importlib.util.module_from_spec(spec); spec.loader.exec_module(alt)

def score_comp(parsed, g, l, k, h):
    t = [math.log(g / (1 - g)), math.log(l), math.log(k)]
    def ll(z):
        return facts.oracle_loglik(parsed, 1 / (1 + math.exp(-z[0])), math.exp(z[1]), math.exp(z[2]))
    out = []
    for i in range(3):
        up, dn = list(t), list(t)
        up[i] += h; dn[i] -= h
        out.append(abs((ll(up) - ll(dn)) / (2 * h)))
    return max(out)

recovery = 0; worst_gap = -1e9; exc = []; bad = []
for seed in range(50):
    inst = make_instance(seed)
    resp = json.loads(inst["responses_json"])
    parsed = [facts.parse(r) for r in resp]
    fr = ref.estimate(resp)
    try:
        fa = alt.estimate(resp)
    except Exception as e:
        exc.append((seed, type(e).__name__, str(e)[:80])); continue
    truth = {"gamma": inst["gamma"], "lambda": inst["lambda"], "kappa": inst["kappa"]}
    ok = all(abs(fa[k + "_hat"] - truth[k]) <= 4 * fa["se_" + k] for k in truth)
    recovery += ok
    gap = fa["log_likelihood"] - fr["log_likelihood"]
    worst_gap = max(worst_gap, -gap)  # how far the alt is BELOW the reference (positive = alt worse)
    sc = min(score_comp(parsed, fa["gamma_hat"], fa["lambda_hat"], fa["kappa_hat"], 1e-5),
             score_comp(parsed, fa["gamma_hat"], fa["lambda_hat"], fa["kappa_hat"], 1e-6))
    if gap < -1e-7 or sc > 2e-5 or not ok:
        bad.append((seed, round(gap, 9), f"{sc:.2e}", ok))
print(name, "recovery", recovery, "of 50 | exceptions", exc)
print(name, "max shortfall of alt loglik below ref (positive = alt worse):", f"{worst_gap:.3e}")
print(name, "seeds with alt loglik below ref, score>2e-5, or not within 4SE:", bad)
