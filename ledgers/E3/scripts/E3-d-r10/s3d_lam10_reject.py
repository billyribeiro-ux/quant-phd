import sys, math, json, importlib.util
sys.path.insert(0, "/tmp/E3d_r10_ws/ref"); sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/ledgers/E3/scripts/E3-d-r10")
import elicit as ref
from instance import make_instance
import s3d_seed_facts as facts
inst = make_instance(49); resp = json.loads(inst["responses_json"]); parsed = [facts.parse(r) for r in resp]
orig = ref._objective
def rejecting(xi, parsed_):
    if xi[1] > math.log(10.0):
        return -math.inf
    return orig(xi, parsed_)
ref._objective = rejecting
try:
    fit = ref.estimate(resp)
    print({k: round(v, 5) for k, v in fit.items()})
    t = [math.log(fit["gamma_hat"]/(1-fit["gamma_hat"])), math.log(fit["lambda_hat"]), math.log(fit["kappa_hat"])]
    def ll(z): return facts.oracle_loglik(parsed, 1/(1+math.exp(-z[0])), math.exp(z[1]), math.exp(z[2]))
    for h in (1e-5, 1e-6):
        comp = []
        for i in range(3):
            up, dn = list(t), list(t); up[i] += h; dn[i] -= h
            comp.append(abs((ll(up)-ll(dn))/(2*h)))
        print("step", h, "score", [f"{c:.2e}" for c in comp])
except Exception as e:
    print("raised", type(e).__name__, str(e)[:120])
