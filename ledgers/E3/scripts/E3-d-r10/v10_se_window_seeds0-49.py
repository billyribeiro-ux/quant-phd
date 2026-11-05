"""For seeds 0-49: exact (60-digit) SEs vs the suite's float oracle SEs at steps 1e-5 and 1e-6 (same formulas as test_project)."""
import sys, json, math
sys.path.insert(0, "/tmp/E3d_r10_ws/scripts")
sys.path.insert(0, "/tmp/E3d_r10_ws/ref")
import elicit as sol
import test_project as tp
from instance import make_instance
from fractions import Fraction
import exact_se_r10 as ex

def float_oracle_se(parsed, est, h):
    g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
    theta = [math.log(g/(1-g)), math.log(l), math.log(k)]
    def at(*mv):
        y = list(theta)
        for i, a in mv:
            y[i] += a
        gg = 1.0/(1.0+math.exp(-y[0]))
        return tp.oracle_loglik(parsed, gg, math.exp(y[1]), math.exp(y[2]))
    f0 = at()
    info = [[0.0]*3 for _ in range(3)]
    for i in range(3):
        info[i][i] = -(at((i,h)) - 2*f0 + at((i,-h)))/(h*h)
        for j in range(i+1,3):
            v = -(at((i,h),(j,h)) - at((i,h),(j,-h)) - at((i,-h),(j,h)) + at((i,-h),(j,-h)))/(4*h*h)
            info[i][j] = info[j][i] = v
    cov = tp._invert3(info)
    return [g*(1-g)*math.sqrt(cov[0][0]), l*math.sqrt(cov[1][1]), k*math.sqrt(cov[2][2])]

def within(a, b):
    return b is not None and b > 0 and abs(a - b) <= 0.1 * b

rows = []
for seed in range(50):
    inst = make_instance(seed)
    resp = json.loads(inst["responses_json"])
    est = sol.estimate(resp)
    parsed = [tp.parse(r) for r in resp]
    ref = [est["se_gamma"], est["se_lambda"], est["se_kappa"]]
    o5 = float_oracle_se(parsed, est, 1e-5)
    o6 = float_oracle_se(parsed, est, 1e-6)
    out, _ = ex.exact_se(resp, est)
    exact = [out["se_gamma"], out["se_lambda"], out["se_kappa"]]
    ok5 = all(within(e, o) for e, o in zip(exact, o5))
    ok6 = all(within(e, o) for e, o in zip(exact, o6))
    ref5 = all(within(r, o) for r, o in zip(ref, o5))
    rows.append((seed, ok5, ok6, ref5))
    print(seed, "exact_passes_at_1e-5:", ok5, "exact_passes_at_1e-6:", ok6, "ref_passes_at_1e-5:", ref5,
          "exact", [round(x, 5) for x in exact], "o5", [round(x, 5) for x in o5], "o6", [round(x, 5) for x in o6], flush=True)
print("SUMMARY exact passes (1e-5 or 1e-6) on", sum(1 for r in rows if r[1] or r[2]), "of 50 seeds")
print("SUMMARY exact fails both on seeds", [r[0] for r in rows if not (r[1] or r[2])])
