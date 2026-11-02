"""Independent check of the project page's numeric claims over seeds 0-299, using the reference solver.

Usage: python3 -I claims_seeds.py <grader_dir>   (grader_dir holds instance.py and reference.py)
Recomputes every certificate field from the page's definitions, not from the suite.
"""
import importlib.util
import json
import sys
from pathlib import Path

grader = Path(sys.argv[1])


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


inst = load("instance_v", grader / "instance.py")
ref = load("reference_v", grader / "reference.py")

max_cert = 0.0
min_ineq_zero_seeds = 0
bound_zero_ok = 0
starts = []
min_inequality_positive = []
worst_dual = 0.0
for seed in range(300):
    case = json.loads(inst.make_instance(seed)["payload"])
    out = ref.allocate(case)
    n = len(case["mu"])
    z = len(case["sector_caps"])
    w = out["weights"]
    m = out["multipliers"]
    d = [w[i] - case["w0"][i] for i in range(n)]
    t = [abs(v) for v in d]
    ineq = {
        "lower": [case["lower"][i] - w[i] for i in range(n)],
        "upper": [w[i] - case["upper"][i] for i in range(n)],
        "sector": [sum(w[i] for i in range(n) if case["sector"][i] == k) - case["sector_caps"][k] for k in range(z)],
        "plus": [d[i] - t[i] for i in range(n)],
        "minus": [-d[i] - t[i] for i in range(n)],
        "kappa": [sum(t) - case["turnover_limit"]],
    }
    mults = {"lower": m["lower"], "upper": m["upper"], "sector": m["sector"],
             "plus": m["turnover_plus"], "minus": m["turnover_minus"], "kappa": [m["turnover_total"]]}
    all_m = [x for k in mults for x in mults[k]]
    if min(all_m) == 0:
        min_ineq_zero_seeds += 1
    else:
        min_inequality_positive.append(seed)
    bound_zeros = sum(1 for x in m["lower"] + m["upper"] if x == 0)
    if bound_zeros >= n + 1:
        bound_zero_ok += 1
    if all(abs(w[i] - case["w0"][i]) <= 1e-12 for i in range(n)):
        starts.append(seed)
    # independent certificate from the page definitions
    primal = max([0.0, abs(sum(w) - 1)] + [g for k in ineq for g in ineq[k]])
    dual = max(0.0, -min(all_m))
    worst_dual = max(worst_dual, dual)
    comp = max(abs(mults[k][j] * ineq[k][j]) for k in mults for j in range(len(mults[k])))
    rw = []
    rt = []
    for i in range(n):
        grad = case["gamma"] * sum(case["sigma"][i][j] * w[j] for j in range(n)) - case["mu"][i]
        rw.append(grad + m["budget"] - m["lower"][i] + m["upper"][i] + m["sector"][case["sector"][i]]
                  + m["turnover_plus"][i] - m["turnover_minus"][i])
        rt.append(m["turnover_total"] - m["turnover_plus"][i] - m["turnover_minus"][i])
    stat = max(max(abs(v) for v in rw), max(abs(v) for v in rt))
    cert = out["certificate"]
    for name, mine in (("primal_residual", primal), ("stationarity_residual", stat),
                       ("dual_residual", dual), ("complementary_slackness", comp)):
        max_cert = max(max_cert, abs(cert[name] - mine), mine)
print("seeds 0-299")
print("seeds whose minimum inequality multiplier is exactly 0:", min_ineq_zero_seeds)
print("seeds with minimum inequality multiplier > 0:", min_inequality_positive)
print("seeds with at least n+1 zero bound multipliers:", bound_zero_ok)
print("seeds where w equals w0 to 1e-12:", starts)
print("worst dual residual (own recomputation):", worst_dual)
print("max |reported - recomputed| or recomputed value over all certificate fields:", max_cert)
