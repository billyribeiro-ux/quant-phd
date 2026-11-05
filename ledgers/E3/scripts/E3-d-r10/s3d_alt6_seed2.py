import sys, json, math, importlib.util
sys.path.insert(0, "/tmp/E3d_r10_ws/ref"); sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/ledgers/E3/scripts/E3-d-r10")
from instance import make_instance
import s3d_seed_facts as facts
import elicit as ref
spec = importlib.util.spec_from_file_location("a6", "/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/ledgers/E3/scripts/E3-d-r10/alts/alt6_fd_step_1e-4/elicit.py")
alt = importlib.util.module_from_spec(spec); spec.loader.exec_module(alt)
inst = make_instance(2); resp = json.loads(inst["responses_json"]); parsed = [facts.parse(r) for r in resp]
def comp(fit, h):
    t = [math.log(fit["gamma_hat"]/(1-fit["gamma_hat"])), math.log(fit["lambda_hat"]), math.log(fit["kappa_hat"])]
    def ll(z): return facts.oracle_loglik(parsed, 1/(1+math.exp(-z[0])), math.exp(z[1]), math.exp(z[2]))
    out = []
    for i in range(3):
        up, dn = list(t), list(t); up[i] += h; dn[i] -= h
        out.append((ll(up)-ll(dn))/(2*h))
    return [f"{v:.2e}" for v in out]
for label, mod in (("ref", ref), ("alt6", alt)):
    fit = mod.estimate(resp)
    print(label, {k: round(v, 6) for k, v in fit.items()})
    print("   score(1e-5)", comp(fit, 1e-5), "score(1e-6)", comp(fit, 1e-6))
    inst_truth = {"gamma": inst["gamma"], "lambda": inst["lambda"], "kappa": inst["kappa"]}
    print("   within 4SE:", all(abs(fit[k+"_hat"]-inst_truth[k]) <= 4*fit["se_"+k] for k in inst_truth))
