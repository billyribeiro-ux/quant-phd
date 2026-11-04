# Diagnose alternative 6 (finite-difference step 1e-4 in the optimiser) on seed 2: score at its estimate, and the true optimum.
import sys, json, math
sys.path.insert(0, "/Users/billyribeiro/.fanout/scratch-E3-d-r8")
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD8-E3-d/course/modules/E/E3/grader")
import alt6 as alt
import reference as ref
from instance import make_instance
inst = make_instance(2)
resp = json.loads(inst["responses_json"])
a = alt.estimate(resp)
r = ref.estimate(resp)
print("alt6 estimate:", {k: round(v, 6) for k, v in a.items()})
print("reference estimate:", {k: round(v, 6) for k, v in r.items()})
from fractions import Fraction
parsed = [ref._parse(x) for x in resp]
def ll(t):
    return ref._objective(t, parsed)
def largest(theta, h):
    out = []
    for i in range(3):
        up, dn = list(theta), list(theta)
        up[i] += h; dn[i] -= h
        out.append(abs((ll(up) - ll(dn)) / (2 * h)))
    return max(out)
for name, est in (("alt6", a), ("reference", r)):
    th = [math.log(est["gamma_hat"] / (1 - est["gamma_hat"])), math.log(est["lambda_hat"]), math.log(est["kappa_hat"])]
    print(name, "largest score at 1e-5:", f"{largest(th, 1e-5):.3e}", "at 1e-6:", f"{largest(th, 1e-6):.3e}")
