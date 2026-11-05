import sys, json, math, importlib.util
sys.path.insert(0, "/tmp/E3d_r10_ws/ref"); sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/ledgers/E3/scripts/E3-d-r10")
from instance import make_instance
import s3d_seed_facts as facts
import elicit as ref
spec = importlib.util.spec_from_file_location("a1c", "/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/ledgers/E3/scripts/E3-d-r10/alts/alt1c_zoom_then_reference_newton/elicit.py")
alt = importlib.util.module_from_spec(spec); spec.loader.exec_module(alt)
inst = make_instance(2); resp = json.loads(inst["responses_json"]); parsed = [facts.parse(r) for r in resp]
def comp(fit):
    t = [math.log(fit["gamma_hat"]/(1-fit["gamma_hat"])), math.log(fit["lambda_hat"]), math.log(fit["kappa_hat"])]
    out = {}
    for h in (1e-5, 1e-6):
        vals = []
        for i in range(3):
            up, dn = list(t), list(t); up[i] += h; dn[i] -= h
            ll = lambda z: facts.oracle_loglik(parsed, 1/(1+math.exp(-z[0])), math.exp(z[1]), math.exp(z[2]))
            vals.append(abs((ll(up)-ll(dn))/(2*h)))
        out[h] = max(vals)
    return out
for label, mod in (("ref", ref), ("alt1c", alt)):
    fit = mod.estimate(resp)
    print(label, {k: round(v, 6) for k, v in fit.items()}, "score", {k: f"{v:.2e}" for k, v in comp(fit).items()})
