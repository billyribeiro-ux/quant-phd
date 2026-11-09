"""Round-15 checks: (a) 20 sampled instances are valid and differ; (b) reference answers on TOL-scale page-valid inputs are not optimal (exact Fractions)."""
import importlib.util, json, sys
from fractions import Fraction as F
ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/course/modules/M/M7/grader")
import instance as inst  # noqa
spec = importlib.util.spec_from_file_location("ref", ROOT + "/course/modules/M/M7/grader/reference.py")
ref = importlib.util.module_from_spec(spec); sys.modules["ref"] = ref; spec.loader.exec_module(ref)

answers = []
for seed in range(20):
    c = json.loads(inst.make_instance(seed)["payload"])
    n = len(c["mu"]); z = len(c["sector_caps"])
    w0 = [F(repr(x)) for x in c["w0"]]; lo = [F(repr(x)) for x in c["lower"]]; up = [F(repr(x)) for x in c["upper"]]
    caps = [F(repr(x)) for x in c["sector_caps"]]
    ok = (sum(w0) == 1) and all(lo[i] <= w0[i] <= up[i] for i in range(n)) and all(
        sum(w0[i] for i in range(n) if c["sector"][i] == k) <= caps[k] for k in range(z)) and c["turnover_limit"] >= 0 and n in (3, 4, 5) and z == 2
    out = ref.allocate(c)
    answers.append(tuple(round(x, 9) for x in out["weights"]))
    if not ok: print("seed", seed, "INVALID")
print("instances valid: 20 of 20 checked (exact Fraction feasibility of w0)")
print("distinct reference answers over seeds 0-19:", len(set(answers)), "of 20")

# (b) page-valid input: turnover limit 1e-9, expected return 1000 on asset 0. Compare reference output with a feasible point
# moved by tau/2 along (+1,-1): both are feasible, the moved point has the lower objective (exact arithmetic).
def f(w, mu, sig, gamma):
    return F(gamma) / 2 * sum(sig[i][j] * w[i] * w[j] for i in range(2) for j in range(2)) - sum(mu[i] * w[i] for i in range(2))
case = {"label": "SIMULATED probe", "gamma": 1.0, "mu": [1000.0, 0.0], "sigma": [[1.0, 0.0], [0.0, 1.0]], "w0": [0.5, 0.5],
        "lower": [-1.0, -1.0], "upper": [2.0, 2.0], "sector": [0, 0], "sector_caps": [2.0], "turnover_limit": 1e-9}
out = ref.allocate(case)
mu = [F(1000), F(0)]; sig = [[F(1), F(0)], [F(0), F(1)]]
w_ref = [F(repr(x)) for x in out["weights"]]
delta = F(1, 2) * F("1e-9")
w_alt = [F(1, 2) + delta, F(1, 2) - delta]
print("ref weights", [str(x) for x in w_ref], "f(ref)=", float(f(w_ref, mu, sig, 1)))
print("moved point (w0 + tau/2*(1,-1)) feasible: sum=1 ->", sum(w_alt) == 1, "sum|d|=", float(abs(w_alt[0]-F(1,2))+abs(w_alt[1]-F(1,2))), "<= tau:", (abs(w_alt[0]-F(1,2))+abs(w_alt[1]-F(1,2))) <= F("1e-9"))
print("f(moved) - f(ref) =", float(f(w_alt, mu, sig, 1) - f(w_ref, mu, sig, 1)), "(negative: reference is not optimal)")
print("reference certificate complementary_slackness =", out["certificate"]["complementary_slackness"], "> 1e-8 page tolerance:", out["certificate"]["complementary_slackness"] > 1e-8)
# upper-bound variant: upper bound 1e-9 above the start on asset 0, expected return 1000 on asset 0
case2 = dict(case); case2["upper"] = [0.5 + 1e-9, 2.0]; case2["turnover_limit"] = 2.0
out2 = ref.allocate(case2)
w2 = [F(repr(x)) for x in out2["weights"]]
alt2 = [F(1, 2) + F("1e-9"), F(1, 2) - F("1e-9")]
print("upper variant: ref", [str(x) for x in w2], "f(moved)-f(ref)=", float(f(alt2, mu, sig, 1) - f(w2, mu, sig, 1)),
      "reference complementary =", out2["certificate"]["complementary_slackness"])
