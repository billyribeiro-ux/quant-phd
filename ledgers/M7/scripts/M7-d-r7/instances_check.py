"""Sample every seed 0-49: instance validity, the Sigma structure, feasibility, binding sets and answer diversity.

Usage: python -I instances_check.py <grader_dir>   (run from the checkout; uses grader/instance.py and grader/reference.py)
"""
import json
import math
import sys
from fractions import Fraction

grader = sys.argv[1]
sys.path.insert(0, grader)
from instance import make_instance  # noqa: E402
import reference as ref  # noqa: E402

def pd(m):
    n = len(m)
    a = [r[:] for r in m]
    for k in range(n):
        if a[k][k] <= 0:
            return False
        for i in range(k + 1, n):
            f = a[i][k] / a[k][k]
            for j in range(k + 1, n):
                a[i][j] -= f * a[k][j]
    return True

rows = []
answers = {}
ok_all = True
for seed in range(50):
    case = json.loads(make_instance(seed)["payload"])
    n = len(case["mu"]); Z = len(case["sector_caps"])
    sig = case["sigma"]
    sym = all(sig[i][j] == sig[j][i] for i in range(n) for j in range(n))
    # Sigma = (A'A + I)/1000 for some integer A in [-2,2]: check the integer numerators are A'A + I for some A -> numerators
    nums = [[round(sig[i][j] * 1000) for j in range(n)] for i in range(n)]
    diag_ok = all(nums[i][i] >= 1 for i in range(n))
    labels = case["sector"]
    s_ok = Z == 2 and set(labels) == {0, 1} and len(labels) == n
    w0 = case["w0"]
    budget_ok = abs(sum(w0) - 1) <= 1e-9
    box_ok = all(case["lower"][i] - 1e-9 <= w0[i] <= case["upper"][i] + 1e-9 for i in range(n))
    sector_ok = all(sum(w0[i] for i in range(n) if labels[i] == k) <= case["sector_caps"][k] + 1e-9 for k in range(Z))
    tau_ok = case["turnover_limit"] >= 0
    lab_ok = "SIMULATED" in make_instance(seed)["label"]
    out = ref.allocate(case)
    w = out["weights"]; m = out["multipliers"]
    binding = []
    for i in range(n):
        if abs(w[i] - case["lower"][i]) < 1e-12: binding.append(f"lo{i}")
        if abs(w[i] - case["upper"][i]) < 1e-12: binding.append(f"up{i}")
    for k in range(Z):
        if abs(sum(w[i] for i in range(n) if labels[i] == k) - case["sector_caps"][k]) < 1e-12: binding.append(f"sec{k}")
    turn = sum(abs(w[i] - w0[i]) for i in range(n))
    if abs(turn - case["turnover_limit"]) < 1e-12: binding.append("turn")
    ok = all([sym, diag_ok, s_ok, budget_ok, box_ok, sector_ok, tau_ok, lab_ok, pd([[float(x) for x in r] for r in sig])])
    ok_all &= ok
    key = tuple(round(x, 9) for x in w)
    answers.setdefault(key, []).append(seed)
    rows.append((seed, n, Z, ok, ",".join(binding) or "-", [round(x, 4) for x in w]))
for r in rows:
    print("seed %2d n=%d Z=%d valid=%s binding=%s w=%s" % r)
print("all instance checks ok:", ok_all)
print("distinct answers:", len(answers), "of 50 seeds")
from collections import Counter
print("binding-set counts:", Counter(r[4] for r in rows).most_common(12))
print("n counts:", Counter(r[1] for r in rows))
